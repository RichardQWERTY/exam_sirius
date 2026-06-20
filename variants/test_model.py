from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

def get_current_year():
    return datetime.date.today().year

class Test(models.Model):
    title = models.CharField(max_length=200,blank=False,null=False,verbose_name="Название")
    author = models.CharField(max_length=150,blank=False,null=False,verbose_name="Автор")
    publication_year = models.IntegerField(validators=[MinValueValidator(1, message="Год должен быть больше 0."),MaxValueValidator(get_current_year, message="Год публикации не может быть больше текущего.")],verbose_name="Год публикации")
    isbn = models.CharField(max_length=20,unique=True,verbose_name="ISBN")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Дата создания")

class Meta:
    db_table = 'books'
    verbose_name = 'Книга'
    verbose_name_plural = 'Книги'

def str(self):
    return f"{self.title} - {self.author}"