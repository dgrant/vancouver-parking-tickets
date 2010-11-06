import datetime, os, sys

sys.path.append(os.path.join(os.path.abspath(os.path.split(__file__)[0]), 'vanparkingtickets'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'vanparkingtickets.settings'

from django.db.models import Count
import numpy as np
import matplotlib.pyplot as plt
from vanparkingtickets.parkingtickets.models import Ticket

hours = range(0,24)
counts = range(0,24)
for hour in hours:
    count = Ticket.objects.filter(datetime__hour=hour).aggregate(count=Count('datetime'))['count']
    counts[hour] = count
    print count

#plt.plot(hours, counts)
#plt.show()

week_days = range(0,8)
counts = range(0,8)
for week_day in week_days:
    count = Ticket.objects.filter(datetime__week_day=week_day).aggregate(count=Count('datetime'))['count']
    counts[week_day] = count
    print count

plt.plot(week_days, counts, 'ro')
plt.show()
