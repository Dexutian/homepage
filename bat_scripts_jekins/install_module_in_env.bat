@rem 安装必要的模块
@echo off
cd /d %~d0\pycode\env_python3.6.5\Scripts
call activate.bat
pip install -r %~d0\pycode\workspace\homepage\requirements\requirements.txt
pause
