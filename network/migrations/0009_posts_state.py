# Generated by Django 3.2.5 on 2021-11-12 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_auto_20211105_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='state',
            field=models.CharField(default='up', max_length=200),
        ),
    ]
