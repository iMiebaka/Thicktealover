# Generated by Django 3.0.5 on 2020-08-11 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20200811_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post_views',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=40)),
                ('session', models.CharField(max_length=40)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postview', to='blog.Post')),
            ],
        ),
        migrations.DeleteModel(
            name='CategoryToPost',
        ),
    ]
