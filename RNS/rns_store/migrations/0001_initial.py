# Generated by Django 3.1.2 on 2020-10-24 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('description', models.CharField(default='', max_length=15)),
                ('logo', models.CharField(default='', max_length=30)),
                ('tags', models.CharField(default='', max_length=30)),
                ('likes', models.IntegerField(default=1)),
            ],
        ),
    ]
