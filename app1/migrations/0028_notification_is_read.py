# Generated by Django 4.2.6 on 2023-11-26 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0027_job_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
