#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Technolia EnglishMaster — All-In-One (Console, Offline)
Author: Abdillah Technojia Tools Store

Features:
- Lessons A→Z (Beginner → Advanced) in one file
- Interactive practice (SW → EN, EN → SW)
- Quizzes (MCQ & fill-in)
- Progress tracking (JSON file on first run)
- Zero external libraries
"""

import json, os, random, textwrap, datetime, sys

APP_NAME = "Technolia EnglishMaster"
PROGRESS_FILE = os.path.join(os.path.expanduser("~"), "Technolia_EnglishMaster_progress.json")

# --------------------------- DATA MODEL ---------------------------

LESSONS = [
    {
        "id": "L1",
        "level": "Beginner",
        "title": "Alphabet & Basic Pronunciation",
        "goals": [
            "Kutamka herufi A–Z",
            "Kuelewa sauti za msingi /æ/ /i:/ /ʌ/ /ɔ:/",
            "Kusalimia na kujitambulisha"
        ],
        "notes": [
            "A a (ei), B b (bi:), C c (si:), D d (di:), E e (i:), F (ef), G (dʒi:), H (eɪtʃ)",
            "Vowel samples: cat /kæt/, see /si:/, sun /sʌn/, talk /tɔ:k/",
            "Greetings: Hello, Hi, Good morning, What's your name? My name is ..."
        ],
        "vocab_sw_en": [
            ("habari", "hello"),
            ("jina", "name"),
            ("asante", "thank you"),
            ("tafadhali", "please"),
            ("samahani", "sorry"),
        ],
        "phrases": [
            ("Jina langu ni Abdillah.", "My name is Abdillah."),
            ("Habari za asubuhi.", "Good morning."),
            ("Asante sana.", "Thank you very much."),
        ]
    },
    {
        "id": "L2",
        "level": "Beginner",
        "title": "Basic Grammar — Present Simple",
        "goals": [
            "Kutumia Present Simple (I/You/We/They + base, He/She/It + -s)",
            "Kuunda maswali na sentensi za kukanusha (do/does)"
        ],
        "notes": [
            "I work, You work, We/They work; He/She/It works.",
            "Negative: I do not (don't) work; He does not (doesn't) work.",
            "Question: Do you work? Does she work?"
        ],
        "vocab_sw_en": [
            ("kazi", "work"),
            ("kusoma", "study"),
            ("nyumbani", "home"),
            ("chakula", "food"),
            ("shule", "school"),
        ],
        "phrases": [
            ("Mimi husoma kila siku.", "I study every day."),
            ("Yeye hufanya kazi benki.", "He works at a bank."),
            ("Je, unasoma Kiingereza?", "Do you study English?"),
        ]
    },
    {
        "id": "L3",
        "level": "Intermediate",
        "title": "Past Simple & Time Expressions",
        "goals": [
            "Kutumia Past Simple kwa vitendo vilivyopita",
            "Maneno ya wakati: yesterday, last week, ago"
        ],
        "notes": [
            "Regular: play → played, watch → watched",
            "Irregular: go → went, have → had, see → saw, make → made",
            "I went to school yesterday. We watched a movie two days ago."
        ],
        "vocab_sw_en": [
            ("jana", "yesterday"),
            ("wiki iliyopita", "last week"),
            ("miaka miwili iliyopita", "two years ago"),
            ("kuenda", "go"),
            ("kuona", "see"),
        ],
        "phrases": [
            ("Nilienda sokoni jana.", "I went to the market yesterday."),
            ("Tuliona filamu wiki iliyopita.", "We saw a movie last week."),
        ]
    },
    {
        "id": "L4",
        "level": "Intermediate",
        "title": "Prepositions & Descriptions",
        "goals": [
            "Prepositions: in, on, at, under, between, next to",
            "Kuelezea watu/vitu (adjectives)"
        ],
        "notes": [
            "in the box, on the table, at home, under the bed, between two houses",
            "Adjectives: tall, short, beautiful, modern, expensive, cheap"
        ],
        "vocab_sw_en": [
            ("ndani ya", "in"),
            ("juu ya", "on"),
            ("katika/saa", "at"),
            ("kati ya", "between"),
            ("karibu na", "next to"),
        ],
        "phrases": [
            ("Kitabu kipo juu ya meza.", "The book is on the table."),
            ("Nyumba yake iko kati ya miti miwili.", "Her house is between two trees."),
        ]
    },
    {
        "id": "L5",
        "level": "Advanced",
        "title": "Conditionals & Modals (Advice, Probability)",
        "goals": [
            "Zero, First, Second conditionals",
            "Modals: should, might, must"
        ],
        "notes": [
            "Zero: If you heat water, it boils.",
            "First: If it rains, I will stay home.",
            "Second: If I were rich, I would travel the world.",
            "Advice: You should study more. Probability: It might be true. Obligation: You must wear a seatbelt."
        ],
        "vocab_sw_en": [
            ("usisahau", "do not forget"),
            ("ushauri", "advice"),
            ("labda", "might/maybe"),
            ("lazima", "must"),
            ("ingekuwa", "would be"),
        ],
        "phrases": [
            ("Kama ningekuwa na muda, ningejifunza Kiingereza zaidi.", "If I had time, I would learn more English."),
            ("Unapaswa kufanya mazoezi kila siku.", "You should practice every day."),
        ]
    }
]

MCQ_TEMPLATES = [
    "Chagua tafsiri sahihi ya: '{sw}'",
    "Choose the correct English for: '{sw}'",
    "Tafsiri kwa Kiingereza: '{sw}'",
]

FILL_BLANK_TEMPLATES = [
    ("I __ to school every day.", "go"),
    ("She __ at a bank.", "works"),
    ("We __ a movie yesterday.", "watched"),
    ("You __ study more.", "should"),
]

# --------------------------- UTILITIES ---------------------------

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print("="*70)
    print(f"{APP_NAME} — Offline Console Edition")
    print("Learn English from Swahili: Beginner → Advanced | Lessons • Practice • Quizzes")
    print("="*70)

def press_enter():
    input("\nBonyeza [Enter] kuendelea...")

def wrap(txt, width=76):
    return textwrap.fill(txt, width=width)

def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --------------------------- PROGRESS I/O ---------------------------

def default_progress():
    return {
        "created_at": now(),
        "last_opened": now(),
        "lessons_completed": [],
        "practice_sessions": 0,
        "quiz_history": [],  # list of {score, total, time}
        "xp": 0
    }

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        save_progress(default_progress())
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except:
        return default_progress()

def save_progress(data):
    data["last_opened"] = now()
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_xp(p, amount):
    p["xp"] += amount
    save_progress(p)

# --------------------------- LESSONS ---------------------------

def list_lessons():
    clear(); banner()
    print("LESSONS (A→Z)\n")
    for i, L in enumerate(LESSONS, start=1):
        print(f"{i:>2}. [{L['level']}] {L['id']} — {L['title']}")
    print("\n0. Rudi kwenye menyu")

def show_lesson(idx, progress):
    L = LESSONS[idx]
    clear(); banner()
    print(f"Lesson {L['id']} — {L['title']}  [{L['level']}]\n")
    print("Malengo:")
    for g in L["goals"]:
        print("  -", g)
    print("\nMaelezo Muhimu:")
    for n in L["notes"]:
        print("  •", n)
    print("\nVocabulary (SW → EN):")
    for sw, en in L["vocab_sw_en"]:
        print(f"  - {sw}  →  {en}")
    print("\nPhrases:")
    for sw, en in L["phrases"]:
        print(f"  - {sw}\n    {en}")

    print("\n[1] Mark as Completed  |  [2] Practice vocabulary  |  [0] Rudi")
    choice = input("Chaguo: ").strip()
    if choice == "1":
        if L["id"] not in progress["lessons_completed"]:
            progress["lessons_completed"].append(L["id"])
            add_xp(progress, 10)
            print("✔ Imewekwa kama imekamilika. (+10 XP)")
        else:
            print("✓ Tayari imeshakamilishwa.")
        press_enter()
    elif choice == "2":
        practice_vocab(L, progress)

# --------------------------- PRACTICE ---------------------------

def practice_vocab(lesson, progress):
    clear(); banner()
    print(f"Practice — {lesson['id']} {lesson['title']}\n")
    items = lesson["vocab_sw_en"][:]
    random.shuffle(items)
    score = 0
    total = len(items)

    for sw, en in items:
        print(f"Tafsiri kwa Kiingereza: '{sw}'")
        ans = input("> ").strip().lower()
        if ans == en.lower():
            print("✔ Sahihi!")
            score += 1
            add_xp(progress, 2)
        else:
            print(f"✘ Si sahihi. Jibu sahihi: {en}")
        print("-"*40)

    progress["practice_sessions"] += 1
    save_progress(progress)
    print(f"\nMatokeo: {score}/{total}  |  XP +{score*2}")
    press_enter()

def practice_mix(progress):
    clear(); banner()
    print("Practice — Mixed (SW↔EN)\n")
    pool = []
    for L in LESSONS:
        pool.extend(L["vocab_sw_en"])
    random.shuffle(pool)
    pool = pool[:10] if len(pool) > 10 else pool
    score = 0
    for sw, en in pool:
        if random.random() < 0.5:
            prompt = f"Tafsiri kwa Kiingereza: '{sw}'"
            correct = en.lower()
        else:
            prompt = f"Tafsiri kwa Kiswahili: '{en}'"
            correct = sw.lower()
        print(prompt)
        ans = input("> ").strip().lower()
        if ans == correct:
            print("✔ Sahihi!"); score += 1; add_xp(progress, 2)
        else:
            print(f"✘ Si sahihi. Jibu sahihi: {correct}")
        print("-"*40)
    progress["practice_sessions"] += 1
    save_progress(progress)
    print(f"\nMatokeo: {score}/{len(pool)}  |  XP +{score*2}")
    press_enter()

# --------------------------- QUIZZES ---------------------------

def quiz_mcq(progress):
    clear(); banner()
    print("QUIZ — Multiple Choice (Vocabulary)\n")
    # Build pool
    pool = []
    for L in LESSONS:
        for sw, en in L["vocab_sw_en"]:
            pool.append((sw, en))
    random.shuffle(pool)
    pool = pool[:10] if len(pool) > 10 else pool

    score = 0
    for i, (sw, en_correct) in enumerate(pool, start=1):
        # pick 3 wrong answers
        wrongs = [en for _, en in pool if en != en_correct]
        wrongs = random.sample(wrongs, k=min(3, len(wrongs))) if wrongs else []
        options = wrongs + [en_correct]
        random.shuffle(options)
        q = random.choice(MCQ_TEMPLATES).format(sw=sw)
        print(f"{i}. {q}")
        for idx, opt in enumerate(options, start=1):
            print(f"   {idx}) {opt}")
        ans = input("Jibu (1-4): ").strip()
        try:
            pick = int(ans)
        except:
            pick = 0
        if pick in range(1, len(options)+1) and options[pick-1].lower() == en_correct.lower():
            print("✔ Sahihi!"); score += 1; add_xp(progress, 3)
        else:
            print(f"✘ Si sahihi. Jibu sahihi: {en_correct}")
        print("-"*40)

    progress["quiz_history"].append({"time": now(), "type": "MCQ", "score": score, "total": len(pool)})
    save_progress(progress)
    print(f"\nMCQ Score: {score}/{len(pool)}  |  XP +{score*3}")
    press_enter()

def quiz_fill_blank(progress):
    clear(); banner()
    print("QUIZ — Fill in the Blank (Grammar)\n")
    items = FILL_BLANK_TEMPLATES[:]
    random.shuffle(items)
    score = 0
    for i, (sentence, answer) in enumerate(items, start=1):
        print(f"{i}. {sentence}")
        ans = input("> ").strip().lower()
        if ans == answer.lower():
            print("✔ Sahihi!"); score += 1; add_xp(progress, 3)
        else:
            print(f"✘ Si sahihi. Jibu sahihi: {answer}")
        print("-"*40)

    progress["quiz_history"].append({"time": now(), "type": "FILL", "score": score, "total": len(items)})
    save_progress(progress)
    print(f"\nFill-in Score: {score}/{len(items)}  |  XP +{score*3}")
    press_enter()

# --------------------------- PROGRESS VIEW ---------------------------

def show_progress(progress):
    clear(); banner()
    print("PROGRESS OVERVIEW\n")
    print(f"XP: {progress['xp']}")
    print(f"Lessons completed: {len(progress['lessons_completed'])} / {len(LESSONS)}")
    if progress["lessons_completed"]:
        print("  - " + ", ".join(progress["lessons_completed"]))
    print(f"Practice sessions: {progress['practice_sessions']}")
    print(f"Quizzes taken: {len(progress['quiz_history'])}")
    if progress["quiz_history"]:
        last = progress["quiz_history"][-1]
        print(f"Last Quiz: {last['type']}  {last['score']}/{last['total']} at {last['time']}")
    print("\nProgress file:", PROGRESS_FILE)
    press_enter()

# --------------------------- MAIN MENUS ---------------------------

def lessons_menu(progress):
    while True:
        list_lessons()
        choice = input("\nChagua somo (namba) au 0 kurudi: ").strip()
        if choice == "0":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(LESSONS):
                show_lesson(idx, progress)
            else:
                print("Chaguo batili."); press_enter()
        except:
            print("Chaguo batili."); press_enter()

def practice_menu(progress):
    while True:
        clear(); banner()
        print("PRACTICE MENU\n")
        print("1) Practice kwa Lesson fulani")
        print("2) Practice Mixed (SW↔EN)")
        print("0) Rudi")
        ch = input("\nChaguo: ").strip()
        if ch == "0": return
        elif ch == "1":
            list_lessons()
            c = input("\nChagua somo (namba) au 0 kurudi: ").strip()
            if c == "0": continue
            try:
                idx = int(c) - 1
                if 0 <= idx < len(LESSONS):
                    practice_vocab(LESSONS[idx], progress)
                else:
                    print("Chaguo batili."); press_enter()
            except:
                print("Chaguo batili."); press_enter()
        elif ch == "2":
            practice_mix(progress)
        else:
            print("Chaguo batili."); press_enter()

def quiz_menu(progress):
    while True:
        clear(); banner()
        print("QUIZ MENU\n")
        print("1) Vocabulary — MCQ")
        print("2) Grammar — Fill in the Blank")
        print("0) Rudi")
        ch = input("\nChaguo: ").strip()
        if ch == "0": return
        elif ch == "1": quiz_mcq(progress)
        elif ch == "2": quiz_fill_blank(progress)
        else:
            print("Chaguo batili."); press_enter()

def main_menu():
    progress = load_progress()
    while True:
        clear(); banner()
        print("MAIN MENU\n")
        print("1) Lessons")
        print("2) Practice")
        print("3) Quizzes")
        print("4) Progress")
        print("5) Exit")
        ch = input("\nChaguo: ").strip()
        if ch == "1": lessons_menu(progress)
        elif ch == "2": practice_menu(progress)
        elif ch == "3": quiz_menu(progress)
        elif ch == "4": show_progress(progress)
        elif ch == "5":
            print("\nAsante! Endelea kujifunza kila siku. 👋")
            sys.exit(0)
        else:
            print("Chaguo batili."); press_enter()

# --------------------------- ENTRY ---------------------------
if __name__ == "__main__":
    main_menu()
