from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Book(models.Model):
    title = models.CharField("Название", max_length=200)
    author = models.CharField("Автор", max_length=150)
    publication_year = models.IntegerField("Год издания")
    isbn = models.CharField("ISBN", max_length=20, unique=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        db_table = "books"
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def clean(self):
        if self.title:
            self.title = self.title.strip()
        if not self.title:
            raise ValidationError({"title": "Название не может быть пустым."})

        if self.author:
            self.author = self.author.strip()
        if not self.author:
            raise ValidationError({"author": "Автор не может быть пустым."})

        if self.publication_year is not None:
            current_year = timezone.localdate().year
            if self.publication_year <= 0:
                raise ValidationError({"publication_year": "Год издания должен быть больше 0."})
            if self.publication_year > current_year:
                raise ValidationError({"publication_year": "Год издания не может быть больше текущего года."})

        if self.isbn:
            self.isbn = self.isbn.strip()
        if not self.isbn:
            raise ValidationError({"isbn": "ISBN не может быть пустым."})