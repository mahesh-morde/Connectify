# Generated by Django 4.2.7 on 2023-12-10 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='addtoFva',
            field=models.BooleanField(default=True),
        ),
    ]
