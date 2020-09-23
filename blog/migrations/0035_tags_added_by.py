# Generated by Django 3.0.5 on 2020-08-23 17:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0034_author_request_category_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='tags',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cat_added', to=settings.AUTH_USER_MODEL),
        ),
    ]
