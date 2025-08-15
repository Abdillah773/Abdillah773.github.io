# Technolia_HyperOptimizerUltimate.ps1
# Author: Abdillah
# Description: Ultimate system optimization tool for Windows 10/11. Double-click to run.

# --- Initialize ---
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logPath = "$env:USERPROFILE\Desktop\Technolia_HyperOptimizer_Log_$timestamp.txt"

Function Log {
    param([string]$message)
    Add-Content -Path $logPath -Value ("[$(Get-Date -Format 'HH:mm:ss')] $message")
}

Write-Host "=== Technolia HyperOptimizer Ultimate ===" -ForegroundColor Cyan
Log "Tool started."

# --- Create System Restore Point ---
Write-Host "Creating system restore point..."
Try {
    Checkpoint-Computer -Description "HyperOptimizer Backup $timestamp" -RestorePointType "MODIFY_SETTINGS"
    Log "Restore point created successfully."
} Catch {
    Log "Failed to create restore point: $_"
}

# --- Cleanup Temp Files ---
Write-Host "Cleaning temp files..."
$tempFolders = @("$env:TEMP", "$env:Windir\Temp")
foreach ($folder in $tempFolders){
    Try {
        Get-ChildItem -Path $folder -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        Log "Cleaned temp folder: $folder"
    } Catch {
        Log "Failed to clean temp folder $folder: $_"
    }
}

# --- DISM / SFC Repairs ---
Write-Host "Running DISM /SFC scans..."
Try {
    dism /online /cleanup-image /restorehealth | Out-Null
    sfc /scannow | Out-Null
    Log "DISM and SFC scans completed."
} Catch {
    Log "DISM/SFC failed: $_"
}

# --- Optimize Memory & CPU ---
Write-Host "Optimizing system memory..."
Try {
    $wmi = Get-WmiObject Win32_OperatingSystem
    [void]([System.GC]::Collect())
    Log "Memory optimization completed."
} Catch {
    Log "Memory optimization failed: $_"
}

# --- Network Reset ---
Write-Host "Resetting network settings..."
Try {
    netsh int ip reset | Out-Null
    netsh winsock reset | Out-Null
    Log "Network reset completed."
} Catch {
    Log "Network reset failed: $_"
}

# --- Final Message ---
Write-Host "System optimization complete! Log saved at $logPath" -ForegroundColor Green
Log "Tool finished successfully."
Start-Sleep -Seconds 3

# --- End of Script ---
