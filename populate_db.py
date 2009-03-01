import logging
import os
import pprint
import sys
import time

sys.path.append(os.path.join(os.path.abspath(os.path.split(__file__)[0]), 'vanparkingtickets'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'vanparkingtickets.settings'
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from vanparkingtickets.parkingtickets.models import Ticket

def setup_logger():
    LOG_FILENAME = 'log.txt'
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

#    ch = logging.StreamHandler()
#    ch.setFormatter(formatter)
#    logger.addHandler(ch)

    fh = logging.FileHandler(LOG_FILENAME)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logging.info('STARTING NEW SESSION')

if __name__ == '__main__':
    setup_logger()

    last_successful_loop = 0
    try:
        import scraper

        s = scraper.Scraper()
        pages = range(1, 54381)
        for page in pages:
            logging.debug("Fetching page %d", page)
            start_time = time.time()
            tickets = s.ScrapeTickets(page)
            for ticket in tickets:
                db_ticket = Ticket()
                db_ticket.date = ticket['date']
                db_ticket.plate = ticket['plate']
                db_ticket.make = ticket['make']
                db_ticket.street_num = int(ticket['street_num'])
                db_ticket.street_name = ticket['street_name']
                db_ticket.offence = ticket['offence']
                db_ticket.record_id = int(ticket['record_id'])
                if len(Ticket.objects.filter(record_id = db_ticket.record_id)) == 0:
                    logging.debug('Saving ticket with record_id=%d to the db', db_ticket.record_id)
                    db_ticket.save()
                else:
                    logging.error('Ticket with record_id=%d already exists in db', db_ticket.record_id)
            last_successful_loop = page
    except:
        logging.exception('Encountered an error')
    finally:
        logging.info('Last successful page was %d', last_successful_loop)
        logging.info('ENDING SESSION')
