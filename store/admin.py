from django.contrib import admin
from .models import Store,Plan
models = [Store,Plan]
# Register your models here.
admin.site.register(models)
