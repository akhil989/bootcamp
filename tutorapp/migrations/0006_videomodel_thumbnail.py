# Generated by Django 5.0.3 on 2024-03-15 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorapp', '0005_rename_lecture_videomodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='videomodel',
            name='thumbnail',
            field=models.ImageField(default='', upload_to='thumbnails'),
        ),
    ]
