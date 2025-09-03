from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import hashlib
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devices.db'
db = SQLAlchemy(app)

# =========================
# MODELS
# =========================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(100), unique=True, nullable=False)
    location = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    phone_numbers = db.relationship('PhoneNumber', backref='device', lazy=True)

class PhoneNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    calls_made = db.Column(db.Integer, default=0)
    calls_received = db.Column(db.Integer, default=0)
    sms_sent = db.Column(db.Integer, default=0)
    sms_received = db.Column(db.Integer, default=0)
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')
    messages = db.relationship('Message', backref='phone_number', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    phone_number_id = db.Column(db.Integer, db.ForeignKey('phone_number.id'), nullable=False)

# =========================
# DEFAULT USER
# =========================

def create_default_user():
    if not User.query.filter_by(username='admin').first():
        hashed_password = hashlib.sha256('rafiki'.encode()).hexdigest()
        default_user = User(username='admin', password=hashed_password)
        db.session.add(default_user)
        db.session.commit()

# =========================
# ROUTES
# =========================

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = User.query.filter_by(username=username, password=hashed_password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        return "Login failed! Try again."
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    devices = Device.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', devices=devices)

@app.route('/add_device', methods=['GET', 'POST'])
def add_device():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        serial_number = request.form['serial_number']
        location = request.form['location']
        new_device = Device(name=name, serial_number=serial_number, location=location, user_id=session['user_id'])
        db.session.add(new_device)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_device.html')

@app.route('/add_phone/<int:device_id>', methods=['GET', 'POST'])
def add_phone(device_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    device = Device.query.get_or_404(device_id)
    if request.method == 'POST':
        number = request.form['number']
        new_number = PhoneNumber(number=number, device_id=device_id)
        db.session.add(new_number)
        db.session.commit()
        return redirect(url_for('view_device', device_id=device_id))
    return render_template('add_phone.html', device=device)

@app.route('/device/<int:device_id>')
def view_device(device_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    device = Device.query.get_or_404(device_id)
    return render_template('view_device.html', device=device)

@app.route('/messages/<int:phone_id>')
def view_messages(phone_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    phone = PhoneNumber.query.get_or_404(phone_id)
    return render_template('view_messages.html', phone=phone)

@app.route('/add_message/<int:phone_id>', methods=['POST'])
def add_message(phone_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    phone = PhoneNumber.query.get_or_404(phone_id)
    content = request.form['content']
    message_type = request.form['message_type']
    new_message = Message(content=content, message_type=message_type, phone_number_id=phone_id)
    db.session.add(new_message)

    if message_type == 'sent':
        phone.sms_sent += 1
    else:
        phone.sms_received += 1

    db.session.commit()
    return redirect(url_for('view_messages', phone_id=phone_id))

@app.route('/stats')
def stats():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    devices = Device.query.filter_by(user_id=session['user_id']).all()
    return render_template('stats.html', devices=devices)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# =========================
# SYNC / ATTACK ROUTES
# =========================

@app.route('/sync_all_sms', methods=['GET'])
def sync_all_sms():
    try:
        your_numbers = ['0793681705','0629111470','0613161707','0612345696','0687441594','0616482166']
        for number in your_numbers:
            api_url = "https://api.africastalking.com/version1/messaging"
            headers = {"apiKey": "YOUR_AFRICASTALKING_API_KEY","Content-Type": "application/json"}
            data = {"username": "YOUR_USERNAME","to": number,"message": "SYNC_SMS_REQUEST"}
            response = requests.post(api_url, headers=headers, json=data)
            if response.status_code == 200:
                print(f"Sync kwenye {number} imefanikiwa!")
            else:
                print(f"Sync kwenye {number} imeshindwa!")
        return "Sync imeanza kikamilifu!", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/attack_my_numbers', methods=['GET'])
def attack_my_numbers():
    try:
        my_numbers = ['0793681705','0629111470','0613161707','0612345696','0687441594','0616482166']
        for number in my_numbers:
            api_url = "https://api.africastalking.com/version1/messaging"
            headers = {"apiKey": "YOUR_API_KEY","Content-Type": "application/json"}
            data = {"username": "sandbox","to": number,"message": "SYNC_ALL_SMS"}
            response = requests.post(api_url, headers=headers, json=data)
            if response.status_code == 200:
                print(f"Attack successful on {number}! SMS zote zimesync!")
            else:
                print(f"Attack failed on {number}")
        return "Attack imefanikiwa! SMS zote zimesync kwenye mfumo!", 200
    except Exception as e:
        return f"Attack imeshindwa: {str(e)}", 500

# =========================
# MAIN
# =========================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_user()
    app.run(debug=True, port=5002)
