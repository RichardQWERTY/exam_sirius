#!/usr/bin/env python
"""
Переключатель варианта.

Запуск:  python setup_variant.py

Берёт выбранный файл из папки variants/, кладёт его в core/models.py,
сбрасывает миграции и базу, пересоздаёт их и создаёт суперпользователя
admin / admin. После этого остаётся только: python manage.py runserver
"""

import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
VARIANTS_DIR = BASE / "variants"
MODELS = BASE / "core" / "models.py"
MIGRATIONS = BASE / "core" / "migrations"
DB = BASE / "db.sqlite3"

CREATE_SUPERUSER = (
    "from django.contrib.auth import get_user_model; "
    "U = get_user_model(); "
    "U.objects.filter(username='admin').exists() or "
    "U.objects.create_superuser('admin', 'admin@example.com', 'admin')"
)


def python_exe():
    for c in (BASE / ".venv" / "bin" / "python", BASE / ".venv" / "Scripts" / "python.exe"):
        if c.exists():
            return str(c)
    return sys.executable


def main():
    variants = sorted(p.stem for p in VARIANTS_DIR.glob("*.py"))
    if not variants:
        print("В папке variants/ нет ни одного варианта.")
        return

    print("Доступные варианты:")
    for i, name in enumerate(variants, 1):
        print(f"  {i}) {name}")

    raw = input("Выбери номер варианта: ").strip()
    try:
        name = variants[int(raw) - 1]
    except (ValueError, IndexError):
        print("Неверный выбор, отмена.")
        return

    MODELS.write_text((VARIANTS_DIR / f"{name}.py").read_text(encoding="utf-8"), encoding="utf-8")
    print(f"[1/4] core/models.py заменён на вариант '{name}'.")

    removed = 0
    for f in MIGRATIONS.glob("0*.py"):
        f.unlink()
        removed += 1
    if DB.exists():
        DB.unlink()
    print(f"[2/4] Удалены старые миграции ({removed}) и db.sqlite3.")

    py = python_exe()
    subprocess.run([py, "manage.py", "makemigrations"], cwd=BASE, check=True)
    subprocess.run([py, "manage.py", "migrate"], cwd=BASE, check=True)
    print("[3/4] Миграции пересозданы и применены.")

    subprocess.run([py, "manage.py", "shell", "-c", CREATE_SUPERUSER], cwd=BASE, check=True)
    print("[4/4] Суперпользователь admin / admin готов.")

    print("\nГотово. Запусти сервер:  python manage.py runserver")
    print("Админка: http://127.0.0.1:8000/admin/   (логин admin, пароль admin)")


if __name__ == "__main__":
    main()
