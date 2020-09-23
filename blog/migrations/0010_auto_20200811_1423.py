# Generated by Django 3.0.5 on 2020-08-11 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0009_auto_20200811_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='number_of_post',
            field=models.IntegerField(null=True),
        ),
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='publisher', to=settings.AUTH_USER_MODEL),
        ),
    ]
