# Generated by Django 5.0.3 on 2024-04-11 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorapp', '0041_alter_videomodel_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videomodel',
            name='description',
            field=models.TextField(max_length=1000),
        ),
    ]
