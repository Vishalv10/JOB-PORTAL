# Generated by Django 4.2.6 on 2023-11-30 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0038_employerprofile_blocked_jobseekerprofile_blocked'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.jobseekerprofile'),
        ),
    ]
