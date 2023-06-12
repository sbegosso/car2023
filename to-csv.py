import csv
import re
import os
from datetime import date

FIELDS = ['URL', 'Title']

DATA = [['https://electrek.co/2023/06/09/tesla-snaps-new-location-fremont-to-expand-4680-battery-cell-production-report/', 'Tesla snaps up new location in Fremont to expand 4680 battery cell production, report says | Electrek'], 
        ['https://www.constructiondive.com/news/toyota-first-us-assembled-battery-electric-suv-nc-factory/652034/', 'Toyota to invest another $2.1B in North Carolina EV battery factory | Construction Dive'], 
        ['https://electrek.co/guides/alibaba/', 'The most awesome (and weirdest) electric vehicles on Alibaba'], 
        ['https://electrek.co/2023/06/09/tesla-nacs-domino-ev-charging-companies-adopting-standard/', "Tesla's NAC enjoys domino effect as EV charging companies adopt the standard | Electrek"], 
        ['https://electrek.co/2023/06/08/porsche-says-electric-mission-x-concept-would-be-fastest-road-legal-car-ever/', 'Porsche says electric Mission X concept would be fastest road-legal car ever | Electrek'], 
        ['https://www.constructiondive.com/press-release/20230530-multi-disciplinary-design-collaborative-bergmeyer-releases-2022-corporate-s/', 'Multi-Disciplinary Design Collaborative Bergmeyer Releases 2022 Corporate Social Responsibility Report | Construction Dive'],
        ['https://electrek.co/2023/06/12/nio-slashes-ev-prices-removes-key-free-battery-swap-service/', 'NIO slashes EV prices and removes key free battery swap service'],
        ['https://www.constructiondive.com/news/despite-50b-of-investment-contech-is-being-held-back-by-its-fragmented-cu/652240/', 'Despite $50B of investment, contech is being held back by its fragmented customer base | Construction Dive'], 
        ['https://electrek.co/2023/06/09/kore-power-ev-battery-factory/', "KORE Power's big EV battery factory just got an $850M DOE boost"], 
        ['https://electrek.co/2023/06/09/aptera-pauses-accelerator-invest-program-sec-solar-ev/', "Aptera pauses Accelerator invest program at request of SEC"]
]

def create_csv(fields, rows):
    """
    Turning the above data into a csv file... kind of an experiment for now
    """
    curr_date = date.today()
    formatted_curr_date = curr_date.strftime('%m-%d-%Y')

    filename = '{}_scraped_urls.csv'.format(formatted_curr_date)
    with open(filename, 'w') as csvfile:

        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

if __name__ == "__main__":
    create_csv(FIELDS, DATA)