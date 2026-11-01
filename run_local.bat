@echo off
title AI-IDS Launcher
:: Delegate to PowerShell to prevent Windows cmd.exe crashing on the '&' in the directory name
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_local.ps1"
pause
