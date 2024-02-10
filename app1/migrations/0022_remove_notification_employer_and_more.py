# Generated by Django 4.2.6 on 2023-11-24 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0021_rename_employer_job_employer_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='employer',
        ),
        migrations.AddField(
            model_name='notification',
            name='employer_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.employerprofile'),
        ),
    ]