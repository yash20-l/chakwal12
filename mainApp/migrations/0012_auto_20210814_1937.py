# Generated by Django 3.2.5 on 2021-08-14 14:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0011_auto_20210814_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Motivation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='notification')),
                ('content', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='notifications',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 8, 14, 14, 7, 8, 181950, tzinfo=utc)),
        ),
    ]
