# Generated by Django 3.2.5 on 2021-10-03 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='balance',
            field=models.TextField(default='0', max_length=2000, null=True),
        ),
    ]