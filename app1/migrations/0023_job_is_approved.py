# Generated by Django 4.2.6 on 2023-11-24 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0022_remove_notification_employer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
