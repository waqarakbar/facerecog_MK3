# Generated by Django 2.2.6 on 2019-10-19 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facesapp', '0004_auto_20191019_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comparison',
            name='sent_back',
            field=models.BooleanField(),
        ),
    ]
