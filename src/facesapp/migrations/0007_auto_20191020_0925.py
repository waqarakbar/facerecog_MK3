# Generated by Django 2.2.6 on 2019-10-20 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facesapp', '0006_auto_20191019_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='features_encoding',
            field=models.TextField(null=True),
        ),
    ]
