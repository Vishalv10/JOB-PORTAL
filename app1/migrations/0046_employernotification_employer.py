# Generated by Django 4.2.6 on 2024-01-11 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0045_remove_employernotification_employer'),
    ]

    operations = [
        migrations.AddField(
            model_name='employernotification',
            name='employer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.employerprofile'),
        ),
    ]
