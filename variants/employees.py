from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Item(models.Model):
    full_name = models.CharField("Полное имя", max_length=200)
    position = models.CharField("Должность", max_length=100)
    hire_date = models.DateField("Дата приёма")
    salary = models.DecimalField(
        "Зарплата",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"), message="Зарплата должна быть больше 0.")],
    )
    email = models.EmailField("Email", max_length=100, unique=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        db_table = "employees"
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name

    def clean(self):
        if self.full_name:
            self.full_name = self.full_name.strip()
        if not self.full_name:
            raise ValidationError({"full_name": "Имя не может быть пустым."})

        if self.position:
            self.position = self.position.strip()
        if not self.position:
            raise ValidationError({"position": "Должность не может быть пустой."})

        if self.hire_date and self.hire_date > timezone.localdate():
            raise ValidationError({"hire_date": "Дата приёма не может быть в будущем."})

        if self.salary is not None and self.salary <= 0:
            raise ValidationError({"salary": "Зарплата должна быть больше 0."})

        if self.email and "@" not in self.email:
            raise ValidationError({"email": "Email должен содержать символ @."})
