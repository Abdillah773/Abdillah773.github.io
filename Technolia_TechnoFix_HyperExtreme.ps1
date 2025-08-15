<# 
Technolia TechnoFix Hyper Extreme — Windows 10/11
Author: Abdillah Technojia Tools Store
#>

$ErrorActionPreference = "Stop"
$logDir = "$env:USERPROFILE\Desktop\TechnoFix_Logs"
if (!(Test-Path $logDir)) { New-Item -Path $logDir -ItemType Directory | Out-Null }
$logFile = "$logDir\TechnoFix_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

function Log($msg) { "$((Get-Date).ToString('HH:mm:ss')) - $msg" | Tee-Object -FilePath $logFile -Append }

function Good($text){ Write-Host "[OK] $text" -ForegroundColor Green; Log $text }
function Warn($text){ Write-Host "[!] $text" -ForegroundColor Yellow; Log $text }
function ErrorMsg($text){ Write-Host "[X] $text" -ForegroundColor Red; Log $text }

function Get-SystemOverview {
    Write-Host "`n=== SYSTEM OVERVIEW ===" -ForegroundColor Cyan
    $os = Get-CimInstance Win32_OperatingSystem
    $cpu = Get-CimInstance Win32_Processor | Select-Object -ExpandProperty Name
    $ram = [math]::Round($os.TotalVisibleMemorySize/1MB,1)
    $uptime = (Get-Date) - ($os.LastBootUpTime)
    Write-Host "OS: $($os.Caption)" -ForegroundColor Cyan
    Write-Host "CPU: $cpu" -ForegroundColor Cyan
    Write-Host "RAM: ${ram}MB" -ForegroundColor Cyan
    Write-Host "Uptime: $($uptime.Days) Days $($uptime.Hours) Hours" -ForegroundColor Cyan
}

function Create-RestorePoint {
    try {
        Checkpoint-Computer -Description "TechnoFix_RestorePoint" -RestorePointType "MODIFY_SETTINGS"
        Good "Restore Point created successfully."
    } catch {
        Warn "Restore Point failed. Continue with caution."
    }
}

function OneClick-Repair {
    Write-Host "`nStarting One-Click Deep Repair..." -ForegroundColor Magenta
    Create-RestorePoint
    DISM /Online /Cleanup-Image /RestoreHealth | Out-Null; Good "DISM complete"
    sfc /scannow | Out-Null; Good "SFC complete"
    Remove-Item "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue; Good "Temp files cleaned"
    netsh winsock reset | Out-Null; ipconfig /flushdns | Out-Null; Good "Network reset complete"
}

function Show-MainMenu {
    Clear-Host
    Write-Host "=== TECHNOLIA HYPER EXTREME ===" -ForegroundColor Cyan
    Write-Host "1 - One-Click Deep Repair"
    Write-Host "2 - Create Restore Point"
    Write-Host "3 - DISM /RestoreHealth"
    Write-Host "4 - SFC /scannow"
    Write-Host "5 - Cleanup Temp caches"
    Write-Host "6 - Network Reset"
    Write-Host "7 - System Overview"
    Write-Host "8 - Exit"
    $choice = Read-Host "Enter choice [1-8]"
    switch ($choice) {
        1 { OneClick-Repair; Pause }
        2 { Create-RestorePoint; Pause }
        3 { DISM /Online /Cleanup-Image /RestoreHealth; Pause }
        4 { sfc /scannow; Pause }
        5 { Remove-Item "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue; Good "Temp cleaned"; Pause }
        6 { netsh winsock reset; ipconfig /flushdns; Good "Network reset done"; Pause }
        7 { Get-SystemOverview; Pause }
        8 { Exit }
        default { Warn "Invalid choice"; Pause }
    }
    Show-MainMenu
}

Show-MainMenu
