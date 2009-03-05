from django.db import models
from django.contrib import admin

# Create your models here.
class Ticket(models.Model):
    date = models.DateTimeField()
    plate = models.CharField(max_length=10)
    make = models.CharField(max_length=20)
    street_num = models.IntegerField()
    street_name = models.CharField(max_length=50)
    offence = models.CharField(max_length=100)
    record_id = models.IntegerField(unique=True)

    details = models.TextField(blank=True)
    fine = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        ordering = ('date',)

    def __unicode__(self):
        return "%d: %s, %s, %s at %s %s (%s)" % (self.record_id, self.date, self.plate, self.make, self.street_num, self.street_name, self.offence)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('date', 'plate', 'make', 'street_num', 'street_name', 'offence')

admin.site.register(Ticket, TicketAdmin)
