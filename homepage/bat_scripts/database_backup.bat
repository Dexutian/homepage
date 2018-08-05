@rem 初始化系统数据库
@echo off
cd /d %~d0\pycode\env_python3.6.5\Scripts
call activate.bat
cd /d %~d0\pycode\homepage
python manage.py dumpdata admin --format=json > requirements\admin.json
python manage.py dumpdata auth --format=json > requirements\auth.json
python manage.py dumpdata info --format=json > requirements\info.json
pause
