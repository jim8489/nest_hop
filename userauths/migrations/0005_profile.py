# Generated by Django 4.2.2 on 2024-09-28 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0004_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='image')),
                ('full_name', models.CharField(blank=True, max_length=200, null=True)),
                ('bio', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(max_length=200)),
                ('varified', models.BooleanField(default=False)),
            ],
        ),
    ]
