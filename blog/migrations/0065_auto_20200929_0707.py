# Generated by Django 3.0.5 on 2020-09-29 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0064_author_request_encodededpk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='whatsapp',
            field=models.URLField(null=True),
        ),
    ]