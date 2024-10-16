# Generated by Django 4.2.2 on 2024-09-19 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_shop', '0017_alter_cartorder_product_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='product_status',
            field=models.CharField(choices=[('disabled', 'Disabled'), ('in_review', 'In Review'), ('rejected', 'Rejected'), ('published', 'Published'), ('draft', 'Processing')], default='processing', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('disabled', 'Disabled'), ('in_review', 'In Review'), ('rejected', 'Rejected'), ('published', 'Published'), ('draft', 'Processing')], default='in_review', max_length=10),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[('4', '⭐⭐⭐⭐☆'), ('5', '⭐⭐⭐⭐⭐'), ('2', '⭐⭐☆☆☆'), ('3', '⭐⭐⭐☆☆'), ('1', '⭐☆☆☆☆')], default=None),
        ),
    ]
