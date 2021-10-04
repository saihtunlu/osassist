# Generated by Django 3.2.5 on 2021-10-03 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('membership_plan', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('total', models.TextField(blank=True, default='0', max_length=2000)),
                ('date', models.TextField(blank=True, default='0', max_length=2000)),
                ('price', models.TextField(blank=True, default='0', max_length=2000)),
                ('number_of_months', models.TextField(blank=True, default='0', max_length=2000)),
                ('note', models.TextField(blank=True, default='', max_length=2000)),
                ('status', models.TextField(default='Pending', max_length=2000, null=True)),
                ('payment_status', models.TextField(default='Unpaid', max_length=2000, null=True)),
                ('selected_plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_billings', to='membership_plan.membershipplan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.TextField(blank=True, default='0', max_length=2000)),
                ('payment_number', models.TextField(blank=True, default='0', max_length=2000)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BillingPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.TextField(blank=True, default='0', max_length=2000)),
                ('date', models.TextField(blank=True, default='0', max_length=2000)),
                ('billing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='billing.billing')),
                ('payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='method_billings', to='billing.paymentmethod')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BillingImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.TextField(default='/media/default.png', max_length=2000, null=True)),
                ('billing_payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='billing.billingpayment')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]