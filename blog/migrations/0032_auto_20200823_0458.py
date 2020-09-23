# Generated by Django 3.0.5 on 2020-08-23 03:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0031_auto_20200820_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='author_request',
            name='modified_on',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='author_request_category',
            name='modified_on',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.CreateModel(
            name='Follower_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_user', to=settings.AUTH_USER_MODEL)),
                ('user_followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
