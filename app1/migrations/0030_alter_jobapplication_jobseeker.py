# Generated by Django 4.2.6 on 2023-11-26 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0029_job_job_seeker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='jobseeker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.jobseekerprofile'),
        ),
    ]
