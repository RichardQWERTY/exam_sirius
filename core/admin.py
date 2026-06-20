from django.contrib import admin
from django.db import models

from .models import Test


@admin.register(Test)
class ItemAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [f.name for f in self.model._meta.fields]

    def get_search_fields(self, request):
        return [
            f.name
            for f in self.model._meta.fields
            if isinstance(f, (models.CharField, models.TextField))
        ]

    def get_readonly_fields(self, request, obj=None):
        return [
            f.name
            for f in self.model._meta.fields
            if getattr(f, "auto_now_add", False) or getattr(f, "auto_now", False)
        ]
