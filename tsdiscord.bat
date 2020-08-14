@echo off
echo unInstalling Discord...
taskkill /F /IM discord.exe
del %APPDATA%\Discord
del C:\Users\localadmin\AppData\Local\Discord