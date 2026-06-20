from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Client(models.Model):
    full_name = models.CharField("Полное имя", max_length=200)
    email = models.EmailField("Email", max_length=100, unique=True)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)
    registration_date = models.DateField("Дата регистрации", default=timezone.localdate)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        db_table = "clients"
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name

    def clean(self):
        if self.full_name:
            self.full_name = self.full_name.strip()
        if not self.full_name:
            raise ValidationError({"full_name": "Имя не может быть пустым."})

        if self.email:
            self.email = self.email.strip()
        if not self.email:
            raise ValidationError({"email": "Email не может быть пустым."})

        if self.phone:
            self.phone = self.phone.strip()
            if Client.objects.exclude(pk=self.pk).filter(phone=self.phone).exists():
                raise ValidationError({"phone": "Клиент с таким номером телефона уже существует."})
        else:
            self.phone = None