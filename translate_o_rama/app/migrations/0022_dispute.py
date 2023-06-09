# Generated by Django 4.1.4 on 2023-02-04 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_job_translated_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dispute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('STATE_OPEN', 'Open'), ('STATE_CLOSED', 'Closed')], default='STATE_OPEN', max_length=20)),
                ('reason', models.TextField()),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.job')),
            ],
        ),
    ]
