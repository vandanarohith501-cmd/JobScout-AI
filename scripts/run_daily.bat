@echo off
cd /d "%~dp0\.."
C:\Python313\python.exe main.py >> output\job_bot.log 2>&1
