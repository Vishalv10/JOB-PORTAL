# Generated by Django 4.2.6 on 2023-11-30 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0039_notification_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='employerprofile',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]