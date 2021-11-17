# Generated by Django 3.2.5 on 2021-10-20 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='user', max_length=200)),
                ('post', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='name', max_length=200)),
                ('followers', models.CharField(default='names', max_length=200)),
            ],
        ),
    ]
