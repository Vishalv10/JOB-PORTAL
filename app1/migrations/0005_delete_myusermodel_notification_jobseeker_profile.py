# Generated by Django 4.2.6 on 2023-11-23 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_myusermodel_remove_employerprofile_password'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUserModel',
        ),
        migrations.AddField(
            model_name='notification',
            name='jobseeker_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.jobseekerprofile'),
        ),
    ]