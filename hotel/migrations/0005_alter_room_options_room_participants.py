# Generated by Django 5.0.2 on 2024-02-20 16:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0004_room_host'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AddField(
            model_name='room',
            name='participants',
            field=models.ManyToManyField(related_name='participant', to=settings.AUTH_USER_MODEL),
        ),
    ]
