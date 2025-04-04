# Generated by Django 4.2 on 2025-02-06 13:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=250)),
                ('lastName', models.CharField(max_length=250)),
                ('username', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
                ('email', models.EmailField(help_text='enter your correct email', max_length=254)),
                ('dateJoined', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(upload_to='img')),
            ],
        ),
    ]
