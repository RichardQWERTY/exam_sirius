from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Item(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    content = models.TextField("Содержание")
    published_at = models.DateField("Дата публикации", default=timezone.localdate)
    views = models.IntegerField(
        "Просмотры",
        default=0,
        validators=[MinValueValidator(0, message="Просмотры не могут быть отрицательными.")],
    )
    is_published = models.BooleanField("Опубликован", default=False)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        db_table = "posts"
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def clean(self):
        if self.title:
            self.title = self.title.strip()
        if not self.title:
            raise ValidationError({"title": "Заголовок не может быть пустым."})

        if self.content:
            self.content = self.content.strip()
        if not self.content:
            raise ValidationError({"content": "Содержание не может быть пустым."})

        if self.published_at and self.published_at > timezone.localdate():
            raise ValidationError({"published_at": "Дата публикации не может быть в будущем."})

        if self.views is not None and self.views < 0:
            raise ValidationError({"views": "Просмотры не могут быть отрицательными."})
