# Generated by Django 4.2.6 on 2023-11-24 03:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0015_alter_job_employer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.employerprofile'),
        ),
    ]