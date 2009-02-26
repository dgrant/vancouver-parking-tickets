from mechanize import Browser
from lxml import html as HTML
import pprint

ENDPOINT = "http://b2.caspio.com/dp.asp?appSession=67071265414986&RecordID=&PageID=2&PrevPageID=2&cpipage=2&CPIsortType=desc&CPIorderby=DE_dDate"

class ParkingTicketScraper(object):
    def __init__(self):
        self.b = Browser()
        self.b.set_handle_robots(False)
        self.b.open(ENDPOINT)

    def run(self):
        self.doc = HTML.fromstring(self.b.response().read(), self.b.geturl())
        self._needle()

    def _needle(self):
        fields = ["Date", "Time", "License plate", "Make", "Street number", "Street", "Offence"]
        count=1
        for tr in self.doc.xpath("//table[1]/tr[@class='cbResultSetEvenRow'] | //table[1]/tr[@class='cbResultSetOddRow']"):
            print "row", count 
            values = [td.text for td in tr.getchildren()[:7]]
            pprint.pprint(zip(fields, values))
            count += 1

p = ParkingTicketScraper()
p.run()
