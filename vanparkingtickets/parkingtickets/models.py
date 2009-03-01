from django.db import models

# Create your models here.
class Ticket(models.Model):
    recordID = models.CharField(max_length=10)
    date = models.DateTimeField()
    plate models.CharField(max_length=10, unique=True)
    make = models.CharField(max_length=20, unique=True)
    street_num = models.IntegerField()
    street_name = models.CharField(max_length=50)
    offence = models.CharField(max_length=100, unique=True)
    details = models.TextField()
    fine = models.DecimalField()
