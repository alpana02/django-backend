# Generated by Django 4.1.3 on 2023-02-14 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIv1', '0003_website_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='url',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
