# Generated by Django 4.1 on 2022-08-12 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0009_productmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='category',
            field=models.CharField(choices=[('mens', 'mens'), ('womens', 'womens'), ('kids', 'kids')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
