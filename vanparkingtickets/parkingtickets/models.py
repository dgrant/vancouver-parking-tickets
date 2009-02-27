from django.db import models

# Create your models here.
class Ticket(models.Model):
    ticket_number = models.CharField(max_length=10)
    date = models.DateTimeField()
    plate = models.ForeignKey("Plate")
    make = models.ForeignKey("Make")
    street_num = models.IntegerField()
    street_name = models.CharField(max_length=50)
    offence = models.ForeignKey("Offence")
    details = models.TextField()
    fine = models.DecimalField()

class Plate(models.Model):
    plate = models.CharField(max_length=10, unique=True)

class Make(models.Model):
    name = models.CharField(max_length=20, unique=True)

class Offence(models.Model):
    name = models.CharField(max_length=100, unique=True)
