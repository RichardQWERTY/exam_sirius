from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_view, name="index"),
    path("create/", views.create_view, name="create"),
    path("<int:pk>/update/", views.update_view, name="update"),
    path("<int:pk>/delete/", views.delete_view, name="delete"),
]
