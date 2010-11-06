from django.db import models
from django.contrib import admin

# Create your models here.
class Ticket(models.Model):
    datetime = models.DateTimeField()
    date = models.DateField()
    time = models.DateField()
    plate = models.CharField(max_length=10)
    make_denorm = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    street_num = models.IntegerField()
    street_name = models.CharField(max_length=50)
    offence_denorm = models.CharField(max_length=100)
    record_id = models.IntegerField(unique=True)
    make = models.ForeignKey('Make')
    offence = models.ForeignKey('Offence')

    details = models.TextField(blank=True)
    fine = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        ordering = ('date',)

    def __unicode__(self):
        return "%d: %s, %s, %s at %s %s (%s)" % (self.record_id, self.date, self.plate, self.make, self.street_num, self.street_name, self.offence)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('date', 'plate', 'make', 'address', 'offence',)
    list_filter = ('make', 'offence', 'time',)
    search_fields = ('plate',)

class Offence(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return unicode(self.name)

class Make(models.Model):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return unicode(self.name)


#admin.site.register(Offence)
#admin.site.register(Ticket, TicketAdmin)
#admin.site.register(Make)
