from django.contrib import admin
from .models import Customer, CustomerAddress
# Register your models here.
models = [Customer, CustomerAddress]
admin.site.register(models)
