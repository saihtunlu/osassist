# Generated by Django 3.2.5 on 2021-10-03 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billings', to='store.store'),
        ),
    ]
