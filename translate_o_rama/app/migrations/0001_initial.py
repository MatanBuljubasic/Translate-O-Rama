# Generated by Django 4.1.4 on 2023-02-01 14:33

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True)),
                ('description', models.TextField(blank=True)),
                ('source_language', models.CharField(max_length=20)),
                ('target_language', models.CharField(max_length=20)),
                ('field', models.CharField(choices=[('STATE_ART', 'Art'), ('STATE_BUSINESS', 'Business'), ('STATE_COMPUTERS', 'Computers'), ('STATE_EDUCATION', 'Education'), ('STATE_ENGINEERING', 'Engineering'), ('STATE_FINANCE', 'Finance'), ('STATE_LAW', 'Law'), ('STATE_LITERATURE', 'Literature'), ('STATE_MEDICINE', 'Medicine'), ('STATE_SCIENCE', 'Science'), ('STATE_SOCIAL', 'Social Sciences'), ('STATE_TECHNOLOGY', 'Technology')], max_length=20)),
                ('budget', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('source_text', models.TextField()),
                ('translated_text', models.TextField()),
                ('status', models.CharField(choices=[('STATE_NOT_ASSIGNED', 'Not assigned'), ('STATE_IN_PROGRESS', 'In Progress'), ('STATE_COMPLETED', 'Completed')], default=('STATE_NOT_ASSIGNED', 'Not assigned'), max_length=20)),
            ],
        ),
    ]
