# Generated by Django 3.0.5 on 2020-08-17 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0013_profile_number_of_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='co_author',
            field=models.ManyToManyField(null=True, related_name='copublisher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='publisher', to=settings.AUTH_USER_MODEL),
        ),
    ]
