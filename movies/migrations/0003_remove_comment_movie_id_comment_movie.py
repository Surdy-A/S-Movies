# Generated by Django 4.2 on 2025-03-21 15:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='movie_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='movie',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='movies.movie'),
            preserve_default=False,
        ),
    ]
