# Generated by Django 3.0.5 on 2020-08-19 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_auto_20200819_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cover_image',
            field=models.ImageField(default='default_image.jpg', null=True, upload_to='profile/images/'),
        ),
    ]
