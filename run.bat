@echo off
REM Запуск проекта одной командой: run.bat
cd /d "%~dp0"

if not exist .venv (
    echo ^>^> Создаю виртуальное окружение...
    python -m venv .venv
)

.venv\Scripts\pip install -q -r requirements.txt
.venv\Scripts\python manage.py migrate

.venv\Scripts\python manage.py shell -c "from django.contrib.auth import get_user_model; U=get_user_model(); U.objects.filter(username='admin').exists() or U.objects.create_superuser('admin','admin@example.com','admin')"

echo.
echo Сервер:  http://127.0.0.1:8000/
echo Админка: http://127.0.0.1:8000/admin/   (admin / admin)
echo.
.venv\Scripts\python manage.py runserver
