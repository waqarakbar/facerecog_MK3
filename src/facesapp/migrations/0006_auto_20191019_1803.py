# Generated by Django 2.2.6 on 2019-10-19 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facesapp', '0005_auto_20191019_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='path',
            field=models.ImageField(upload_to=''),
        ),
    ]
