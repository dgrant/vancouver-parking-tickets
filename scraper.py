from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from lxml import html as HTML
import datetime
import pprint
import re
import time
import sys

recordID_regexp = re.compile("RecordID\=(\d*)")
date_regexp = re.compile("\S*, (?P<month>\S*) (?P<date>\d*) '(?P<year>\d*)")

ENDPOINT = "http://b2.caspio.com/dp.asp?AppKey=%s&RecordID=&PageID=2&PrevPageID=2&cpipage=%d&CPIsortType=desc&CPIorderby=DE_dDate"
#DETAIL_ENDPOINT = "http://b2.caspio.com/dp.asp?AppKey=2b931000e4a5f0b1i7f3d6e0b6i&RecordID=%d&PageID=3&PrevPageID=2&cpipage=1&CPIsortType=desc&CPIorderBy=DE_dDate"

class Scraper(object):
    def __init__(self):
        self.b = Browser()
        self.b.set_handle_robots(False)

        self.appkey = None
        self.GetAppKey()

    def GetAppKey(self):
        self.b.open("http://www.vancouversun.com/parking/basic-search.html")
        html = self.b.response().read()
        soup = BeautifulSoup(html)
        for div in soup.findAll('div'):
            if div.has_key('id') and div['id'] == 'cxkg':
                self.appkey = div.findAll('a')[0]['href'].split('AppKey=')[1].split('&')[0]
                break

    def ScrapeTickets(self, page):
        assert len(self.appkey) > 10
        url = ENDPOINT % (self.appkey, page)
        self.b.open(url)

        doc = HTML.fromstring(self.b.response().read(), self.b.geturl())

        tickets = []
        fields = ["Date", "Time", "LicensePlate", "Make", "StreetNumber", "Street", "Offence", "RecordId"]
        for tr in doc.xpath("//table[1]/tr[@class='cbResultSetEvenRow'] | //table[1]/tr[@class='cbResultSetOddRow']"):
            values = [td.text for td in tr.getchildren()[:7]]
            td_details=tr.getchildren()[7]
            # get the RecordID
            values.append(re.search(recordID_regexp, td_details.xpath("a/@href")[0]).group(1))

            ticket = Ticket(zip(fields, values))
            ticket.CleanUpRawTicket()
            tickets.append(ticket)
        return tickets

class Ticket(dict):
    def CleanUpRawTicket(self):
        print self
        date = datetime.datetime.strptime(self['Date'] + " " + self['Time'], "%a, %b %d '%y %H%M")
        assert 2004 <= date.year < 2009
        self['Date'] = date
        del self['Time']

s = Scraper()
for i in xrange(1,54380):
    start_time = time.time()
    tickets = s.ScrapeTickets(int(sys.argv[1]))
    pprint.pprint(tickets)
    print "took", time.time() - start_time, "seconds"
