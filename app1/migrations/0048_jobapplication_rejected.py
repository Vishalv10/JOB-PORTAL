# Generated by Django 4.2.6 on 2024-01-25 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0047_jobapplication_selected'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
    ]
