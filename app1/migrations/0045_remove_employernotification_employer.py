# Generated by Django 4.2.6 on 2024-01-10 23:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0044_rejectedjob'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employernotification',
            name='employer',
        ),
    ]