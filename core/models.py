from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Item(models.Model):
    name = models.CharField("Название", max_length=150)
    code = models.CharField("Код", max_length=50, unique=True)
    amount = models.DecimalField(
        "Сумма",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"), message="Значение должно быть больше 0.")],
    )
    quantity = models.PositiveIntegerField(
        "Количество",
        validators=[MinValueValidator(1, message="Значение должно быть больше 0.")],
    )
    start_at = models.DateTimeField("Дата начала")
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        db_table = "items"
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def clean(self):
        if self.name:
            self.name = self.name.strip()
        if not self.name:
            raise ValidationError({"name": "Поле не может быть пустым."})
        if self.amount is not None and self.amount <= 0:
            raise ValidationError({"amount": "Значение должно быть больше 0."})
        if self.quantity is not None and self.quantity <= 0:
            raise ValidationError({"quantity": "Значение должно быть больше 0."})
