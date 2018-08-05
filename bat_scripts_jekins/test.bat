@rem 启动测试程序
@echo off
cd /d %~d0\pycode\env_python3.6.5\Scripts
call activate.bat
cd /d %~d0\pycode\workspace\homepage
python manage.py test