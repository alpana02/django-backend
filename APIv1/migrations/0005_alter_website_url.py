# Generated by Django 4.1.3 on 2023-02-14 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIv1', '0004_alter_website_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='url',
            field=models.CharField(max_length=200),
        ),
    ]
