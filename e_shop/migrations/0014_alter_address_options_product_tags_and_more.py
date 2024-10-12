# Generated by Django 4.2.2 on 2024-09-17 10:25

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('e_shop', '0013_rename_adress_address_rename_adress_address_address_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name_plural': 'Address'},
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='product_status',
            field=models.CharField(choices=[('disabled', 'Disabled'), ('rejected', 'Rejected'), ('published', 'Published'), ('in_review', 'In Review'), ('draft', 'Processing')], default='processing', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('disabled', 'Disabled'), ('rejected', 'Rejected'), ('published', 'Published'), ('in_review', 'In Review'), ('draft', 'Processing')], default='in_review', max_length=10),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[('4', '⭐⭐⭐⭐☆'), ('1', '⭐☆☆☆☆'), ('3', '⭐⭐⭐☆☆'), ('2', '⭐⭐☆☆☆'), ('5', '⭐⭐⭐⭐⭐')], default=None),
        ),
    ]
