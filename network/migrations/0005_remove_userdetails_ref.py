# Generated by Django 3.2.5 on 2021-10-22 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_userdetails_ref'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='ref',
        ),
    ]
