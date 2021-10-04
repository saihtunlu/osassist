from django.contrib import admin
from .models import Billing, BillingImage, BillingPayment, PaymentMethod

# Register your models here.
models = [Billing, BillingImage, BillingPayment, PaymentMethod]
admin.site.register(models)
