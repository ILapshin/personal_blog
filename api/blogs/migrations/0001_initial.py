# Generated by Django 5.0.2 on 2024-02-07 18:28

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.CharField(blank=True, max_length=140, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2024, 2, 7, 18, 28, 16, 662677))),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('readers', models.ManyToManyField(blank=True, related_name='readers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]