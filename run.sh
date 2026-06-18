#!/usr/bin/env bash
# Запуск проекта одной командой: ./run.sh
set -e
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
    echo ">> Создаю виртуальное окружение..."
    python3 -m venv .venv
fi

.venv/bin/pip install -q -r requirements.txt

PY=.venv/bin/python
$PY manage.py migrate

# Суперпользователь admin / admin (создаётся, если ещё нет)
$PY manage.py shell -c "from django.contrib.auth import get_user_model; U=get_user_model(); U.objects.filter(username='admin').exists() or U.objects.create_superuser('admin','admin@example.com','admin')"

echo ""
echo "Сервер:  http://127.0.0.1:8000/"
echo "Админка: http://127.0.0.1:8000/admin/   (admin / admin)"
echo ""
$PY manage.py runserver
