# Generated by Django 4.2.6 on 2023-11-25 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0023_job_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='employernotification',
            name='job_application',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.jobapplication'),
        ),
    ]
