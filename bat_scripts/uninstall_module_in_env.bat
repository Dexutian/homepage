@rem 卸载必要的模块
@echo off
cd /d %~d0\pycode\env_python3.6.5\Scripts
call activate.bat
pip uninstall -r %~d0\pycode\homepage\requirements\requirements.txt -y
pause