# Generated by Django 4.2.7 on 2023-12-10 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0009_rename_cid_contact_uid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='uid',
        ),
        migrations.AddField(
            model_name='contact',
            name='uname',
            field=models.CharField(default=123, max_length=255),
            preserve_default=False,
        ),
    ]