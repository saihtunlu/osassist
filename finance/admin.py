from django.contrib import admin
from django.contrib import admin

from .models import FinanceLabel,Finance
# Register your models here.
models=[FinanceLabel,Finance]
admin.site.register(models)
