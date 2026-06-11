# Универсальный Django-шаблон для квалификационного экзамена

Готовая обвязка под задание «реализуйте бэкенд для управления данными».
Вся инфраструктура (CRUD, админка, формы, список, middleware метрик,
`.env`, `/ping/`, статика при `DEBUG=False`, тесты) **не зависит от модели**
и подстраивается автоматически.

> Под конкретный вариант ты редактируешь по сути **только `core/models.py`** —
> описываешь поля и правила валидации. Форма, админка и таблица списка
> строятся по модели сами.

## Что внутри

```
django_exam/
├── manage.py
├── requirements.txt
├── .env                      # DEBUG, SECRET_KEY, параметры БД
├── config/
│   ├── settings.py           # читает .env (без зависимостей), whitenoise, middleware
│   ├── urls.py               # /admin/, /ping/, собственный интерфейс
│   └── wsgi.py / asgi.py
└── core/
    ├── models.py             # ⟵ ЕДИНСТВЕННЫЙ файл, который ты меняешь под вариант
    ├── forms.py              # ModelForm fields="__all__" + bootstrap (универсально)
    ├── admin.py              # list_display/search строятся по модели (универсально)
    ├── views.py              # CRUD через псевдоним Model/ModelForm + /ping/
    ├── urls.py               # index/create/update/delete
    ├── middleware.py         # метрики 2xx/4xx/5xx -> metrics.log + консоль
    ├── tests.py              # тест /ping/ == 200 (+ smoke-тесты, модель-агностичные)
    └── templates/core/       # base/index/form/confirm_delete (Bootstrap, generic)
```

## Запуск

```bash
cd django_exam
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Админка: http://127.0.0.1:8000/admin/
- Свой интерфейс: http://127.0.0.1:8000/
- Тест-эндпоинт: http://127.0.0.1:8000/ping/

## Проверка перед сдачей

```bash
python manage.py test            # /ping/ -> 200 (+ smoke)
python manage.py showmigrations  # миграции применены
```
Метрики: открой несколько страниц — статистика в консоли и в `metrics.log`.

## Статика при DEBUG=False (чтобы админка была со стилями)

```bash
python manage.py collectstatic --noinput
# в .env: DEBUG=False
python manage.py runserver
```
Стили админки отдаёт WhiteNoise. После проверки верни `DEBUG=True`.

---

# Как адаптировать под свой вариант

## Шаг 1. Описать поля в `core/models.py`

Меняешь поля класса `Item` под таблицу из задания. Шпаргалка по типам:

| В задании | Поле модели |
|-----------|-------------|
| VARCHAR(n), текст | `models.CharField("Метка", max_length=n)` |
| Длинный текст | `models.TextField("Метка", blank=True)` |
| INTEGER | `models.IntegerField("Метка")` |
| Целое > 0 | `models.PositiveIntegerField("Метка", validators=[MinValueValidator(1)])` |
| DECIMAL(10,2) | `models.DecimalField("Метка", max_digits=10, decimal_places=2)` |
| TIMESTAMP (вводимый) | `models.DateTimeField("Метка")` |
| Дата создания (авто) | `models.DateTimeField("Создано", auto_now_add=True)` |
| Уникальное поле | добавь `unique=True` |
| Необязательное | добавь `blank=True` (для текста) / `null=True, blank=True` |
| Логический флаг | `models.BooleanField("Метка", default=False)` |

`unique=True` сам даёт ошибку при дубликате (в форме и в админке) — отдельно проверять не надо.

## Шаг 2. Прописать валидацию в `clean()`

Метод `clean()` модели вызывается и формой, и админкой. Типовые правила:

```python
def clean(self):
    # текст не пустой (и не из одних пробелов)
    if self.name:
        self.name = self.name.strip()
    if not self.name:
        raise ValidationError({"name": "Поле не может быть пустым."})

    # число строго больше 0
    if self.amount is not None and self.amount <= 0:
        raise ValidationError({"amount": "Значение должно быть больше 0."})

    # дата только в будущем (нужно: from django.utils import timezone)
    if self.start_at and self.start_at <= timezone.now():
        raise ValidationError({"start_at": "Дата должна быть в будущем."})

    # дата только в прошлом
    if self.birth_date and self.birth_date > timezone.now().date():
        raise ValidationError({"birth_date": "Дата не может быть в будущем."})
```

Ключ в словаре `ValidationError({...})` — это **имя поля**, под которым в форме
покажется сообщение.

## Шаг 3. Пересоздать миграции

```bash
rm core/migrations/0001_initial.py
python manage.py makemigrations
python manage.py migrate
```

## Готово

Менять `forms.py`, `admin.py`, `views.py`, шаблоны и `urls.py` **не нужно** —
они работают по любой модели:
- форма берёт все редактируемые поля (`fields="__all__"`), даты получают
  виджет-календарь, поля — стили Bootstrap;
- админка показывает все поля в списке, ищет по текстовым, поля `auto_now*`
  делает read-only;
- таблица на главной строит колонки по `verbose_name` полей.

Если в `models.py` переименуешь класс `Item`, поправь только импорт в двух
строках `core/views.py` (`Item as Model`, `ItemForm as ModelForm`) и в
`core/forms.py` / `core/admin.py`.

