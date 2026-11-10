# Setup or update the daily JobScout AI Windows Task
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$BatchPath = Join-Path $ScriptDir "run_daily.bat"

Write-Host "Configuring Windows Scheduled Task for JobScout AI..." -ForegroundColor Cyan
Write-Host "Project Root: $ProjectRoot"
Write-Host "Batch Path: $BatchPath"

$Action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$BatchPath`"" -WorkingDirectory $ProjectRoot
$Trigger = New-ScheduledTaskTrigger -Daily -At "17:00"
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -WakeToRun

Register-ScheduledTask -TaskName "DailyJobResearchReport" -Action $Action -Trigger $Trigger -Settings $Settings -Force

Write-Host "Successfully registered DailyJobResearchReport to trigger daily at 5:00 PM IST with catch-up mode enabled." -ForegroundColor Green
