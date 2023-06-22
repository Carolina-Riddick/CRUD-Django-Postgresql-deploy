from django.contrib import admin
from .models import Task


class Task_admin(admin.ModelAdmin):
    readonly_fields = ("created",)


# Register your models here.
admin.site.register(Task, Task_admin)


