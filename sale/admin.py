from django.contrib import admin
from .models import Sale, SaleProduct, SalePayment,SaleAddress
# Register your models here.
models = [SaleProduct, Sale, SalePayment,SaleAddress]
admin.site.register(models)
