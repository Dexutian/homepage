@rem 初始化系统数据库
@echo off
cd /d %~d0\pycode\env_python3.6.5\Scripts
call activate.bat
cd /d %~d0\pycode\homepage
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata requirements\admin.json
python manage.py loaddata requirements\auth.json
python manage.py loaddata requirements\info.json
pause
