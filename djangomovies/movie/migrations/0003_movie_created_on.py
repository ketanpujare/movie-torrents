# Generated by Django 2.2.3 on 2019-07-31 20:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_auto_20190730_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]