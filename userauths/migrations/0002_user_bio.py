# Generated by Django 4.2.2 on 2024-07-27 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
