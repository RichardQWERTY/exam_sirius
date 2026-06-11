from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Item as Model
from .forms import ItemForm as ModelForm


def ping_view(request):
    return HttpResponse("pong", status=200, content_type="text/plain")


def list_view(request):
    fields = Model._meta.fields
    headers = [f.verbose_name for f in fields]
    rows = [
        {"pk": obj.pk, "values": [getattr(obj, f.name) for f in fields]}
        for obj in Model.objects.all()
    ]
    return render(request, "core/index.html", {"headers": headers, "rows": rows})


def create_view(request):
    if request.method == "POST":
        form = ModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись успешно создана.")
            return redirect("index")
        messages.error(request, "Исправьте ошибки в форме.")
        return render(request, "core/form.html", {"form": form}, status=400)
    return render(request, "core/form.html", {"form": ModelForm()})


def update_view(request, pk):
    obj = get_object_or_404(Model, pk=pk)
    if request.method == "POST":
        form = ModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись успешно обновлена.")
            return redirect("index")
        messages.error(request, "Исправьте ошибки в форме.")
        return render(request, "core/form.html", {"form": form, "object": obj}, status=400)
    return render(request, "core/form.html", {"form": ModelForm(instance=obj), "object": obj})


def delete_view(request, pk):
    obj = get_object_or_404(Model, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Запись удалена.")
        return redirect("index")
    return render(request, "core/confirm_delete.html", {"object": obj})
