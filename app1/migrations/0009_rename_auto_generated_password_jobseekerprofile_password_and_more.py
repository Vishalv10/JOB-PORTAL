# Generated by Django 4.2.6 on 2023-11-23 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_jobseekerprofile_auto_generated_password_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobseekerprofile',
            old_name='auto_generated_password',
            new_name='password',
        ),
        migrations.RenameField(
            model_name='jobseekerprofile',
            old_name='auto_generated_username',
            new_name='username',
        ),
    ]
