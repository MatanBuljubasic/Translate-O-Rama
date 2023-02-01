from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator
from accounts.models import User

# Create your models here.


FIELD_CHOICES = (
    ("STATE_ART", "Art"),
    ("STATE_BUSINESS", "Business"),
    ("STATE_COMPUTERS", "Computers"),
    ("STATE_EDUCATION", "Education"),
    ("STATE_ENGINEERING", "Engineering"),
    ("STATE_FINANCE", "Finance"),
    ("STATE_LAW", "Law"),
    ("STATE_LITERATURE", "Literature"),
    ("STATE_MEDICINE", "Medicine"),
    ("STATE_SCIENCE", "Science"),
    ("STATE_SOCIAL", "Social Sciences"),
    ("STATE_TECHNOLOGY", "Technology"),
)

STATUS_CHOICES = (
    ("STATE_NOT_ASSIGNED", "Not assigned"),
    ("STATE_IN_PROGRESS", "In Progress"),
    ("STATE_COMPLETED", "Completed"),
)

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(unique=True, max_length=120)
    description = models.TextField(blank=True)
    source_language = models.CharField(max_length=20)
    target_language = models.CharField(max_length=20)
    field = models.CharField(choices=FIELD_CHOICES, max_length=20)
    budget = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0.01'))])
    source_text = models.TextField()
    translated_text = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0], max_length=20)


