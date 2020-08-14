@echo off

taskkill /F /IM pc-client.exe
echo Disabling rrx...
disablerrx
echo restarting in 3 minutes press enter...
pause
shutdown -r -t 180