import os
import re
import urllib2
from bs4 import BeautifulSoup
from rss import create_feed, ftp_feed
import config

# change directory to APH-rss root dir, required for
# Pythonanywhere scheduled task only
# os.chdir(config.run_path)

# Create variable to trigger RSS update
new_bills_added = False

# convert txt file storing existing bills to a list
# create new file if not already present
try:
    with open('bills_output.txt', 'r') as f:
        existing_bills = f.read().splitlines()
except IOError:
    open('bills_output.txt', 'w').close()
    with open('bills_output.txt', 'r') as f:
        existing_bills = f.read().splitlines()

# This section scrapes the latest updates to bills section of the APH homepage,
# http://www.aph.gov.au/, extracting the update date, bill name and bill
# homepage URL, and adding this information to a text file for later convertion
# to an RSS feed.

# Open and read the APH homepage
source_url = "http://www.aph.gov.au/Parliamentary_Business/Bills_Legislation"
source = urllib2.urlopen(source_url).read()

# Create BeautifulSoup object of APH site
soup = BeautifulSoup(source, "html.parser")

# Locate Bills section of APH page
bills_table = soup.find("table", {"class": "documents"})
bills_table_rows = bills_table.find_all("tr")
del bills_table_rows[0]
bills_table_rows.reverse()

# Create string for each Bill containing date, Bill name, and Bill URL
for row in bills_table_rows:
    bill_date = row.find("td", {"class": "date"}).string.encode("utf-8").lstrip()
    bill_name = row.find("a").string.encode("utf-8")
    bill_anchor = row.find("a")
    bill_url = "http://www.aph.gov.au{0}".format(bill_anchor["href"].encode("utf-8"))

    bill_string = "{0}: {1}, {2}".format(bill_date,
                                         bill_name,
                                         bill_url)

    # Add Bill string to existing bills list if not already present
    if bill_string not in existing_bills:
        print "Adding new bill: {0}".format(bill_name)
        existing_bills.append(bill_string)
        new_bills_added = True
    else:
        print "{0} already added today".format(bill_name)

with open('bills_output.txt', 'w') as f:
    for item in existing_bills:
        f.write('{0}\n'.format(item))

# This section runs the RSS update and FTP functions if new bills are added
if new_bills_added:
    print "Updating RSS"
    create_feed()
    ftp_feed()
    print "RSS update complete"
else:
    print "No new bills added, RSS up to date"
