# Generated by Django 4.2.6 on 2023-11-24 01:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0012_remove_notification_created_at_notification_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='employer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employer_notifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='job_seeker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_seeker_notifications', to=settings.AUTH_USER_MODEL),
        ),
    ]
