# Generated by Django 5.0.3 on 2024-03-18 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorapp', '0012_alter_videomodel_instructor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videomodel',
            name='instructor',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
