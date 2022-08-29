# Generated by Django 4.1 on 2022-08-12 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0008_alter_user_postcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200)),
                ('product_price', models.IntegerField()),
                ('product_disc', models.CharField(max_length=500)),
            ],
        ),
    ]