# Generated by Django 4.2.6 on 2023-11-29 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0036_alter_employernotification_notification_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseekerprofile',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='educational_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]