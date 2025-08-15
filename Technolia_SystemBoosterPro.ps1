<#
Technolia System Booster Pro
Author: Abdillah
Description: Kitufe kimoja cha kuboresha Windows 10/11. 
Inafanya: Cleanup temp files, optimize registry, speed up boot, improve network, repair system files.
#>

# FUNGA UI
Add-Type -AssemblyName PresentationFramework

[System.Windows.MessageBox]::Show("Technolia System Booster Pro inakwenda kuboresha mfumo wako. Bonyeza OK kuendelea.","Technolia System Booster","OK","Information")

# 1. Futa Temp Files
$tempPaths = @("$env:Temp","$env:Windir\Temp")
foreach ($path in $tempPaths) {
    try {
        Remove-Item "$path\*" -Recurse -Force -ErrorAction SilentlyContinue
    } catch {}
}

# 2. Disk Cleanup (Temporary & System files)
Start-Process cleanmgr -ArgumentList "/sagerun:1" -Wait

# 3. Run SFC /scannow
Start-Process "cmd.exe" -ArgumentList "/c sfc /scannow" -Verb RunAs -Wait

# 4. Run DISM RestoreHealth
Start-Process "cmd.exe" -ArgumentList "/c DISM /Online /Cleanup-Image /RestoreHealth" -Verb RunAs -Wait

# 5. Optimize Boot
Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" | ForEach-Object {
    Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" -Name "ClearPageFileAtShutdown" -Value 1
}

# 6. Disable Unnecessary Startup Apps
$startupApps = Get-CimInstance Win32_StartupCommand | Where-Object {$_.User -eq $env:USERNAME}
foreach($app in $startupApps){
    try {
        $app | Remove-CimInstance -ErrorAction SilentlyContinue
    } catch {}
}

# 7. Optimize Network (TCP/IP settings)
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name "TcpTimedWaitDelay" -PropertyType DWord -Value 30 -Force
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name "MaxUserPort" -PropertyType DWord -Value 65534 -Force

# 8. Registry Cleanup (basic)
$regPaths = @("HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU",
              "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs")
foreach($reg in $regPaths){
    Remove-ItemProperty -Path $reg -Name * -ErrorAction SilentlyContinue
}

# 9. System Info Summary
$sysInfo = Get-ComputerInfo | Select-Object CsName, WindowsVersion, OsHardwareAbstractionLayer, CsProcessors, CsTotalPhysicalMemory
[System.Windows.MessageBox]::Show("Umefanikiwa kuboresha mfumo wako! Hapa ni muhtasari wa kompyuta: `n`n$( $sysInfo | Out-String )","Technolia System Booster","OK","Information")
