# Generated by Django 4.2.6 on 2023-11-29 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0037_jobseekerprofile_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employerprofile',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
    ]