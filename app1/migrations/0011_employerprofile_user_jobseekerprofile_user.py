# Generated by Django 4.2.6 on 2023-11-23 19:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0010_employerprofile_password_employerprofile_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='employerprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employer_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobseeker_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]