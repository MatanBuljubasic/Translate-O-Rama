# Generated by Django 4.1.4 on 2023-02-02 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_job_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('STATE_NOT_ASSIGNED', 'Not assigned'), ('STATE_IN_PROGRESS', 'In Progress'), ('STATE_COMPLETED', 'Completed')], default='Not assigned', max_length=20),
        ),
    ]
