# Generated by Django 3.2.3 on 2021-05-23 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='slug',
            field=models.SlugField(editable=False, max_length=255),
        ),
    ]
