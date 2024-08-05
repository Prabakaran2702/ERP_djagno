from django.db import models

# Create your models here.

EXAMPLE_CHOICES = [
        ("Good", "Good"),
        ("Bad", "Bad"),
        ("Average", "Average"),
    ]

class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    author = models.CharField(max_length=100)
    rateing = models.CharField(max_length=100, choices=EXAMPLE_CHOICES, default='Average')
    published_date = models.DateField()

    def __str__(self):
        return self.title