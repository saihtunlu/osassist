# Generated by Django 3.2.5 on 2021-10-22 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0003_alter_file_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='image',
            field=models.TextField(),
        ),
    ]