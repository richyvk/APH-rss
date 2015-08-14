import os
import urllib2
from bs4 import BeautifulSoup
from rss import create_feed, ftp_feed
import config

#change directory to APH-rss root dir, required for Pythonanywhere scheduled task only
os.chdir(config.run_path)

#Create variable to trigger RSS update
new_bills_added = None

#convert txt file storing existing bills to a list
with open('bills_output.txt', 'a+') as f:
    existing_bills = f.read().splitlines()

#This section scrapes the latest updates to bills section of the APH homepage,
#http://www.aph.gov.au/, extracting the update date, bill name and bill
#homepage URL, and adding this information to a text file for later convertion
#to an RSS feed.

#Open and read the APH homepage
source = urllib2.urlopen("http://www.aph.gov.au/").read()

#Create BeutifulSoup object of APH site
soup = BeautifulSoup(source)

#Locate Bills section of APH page
bills_div = soup.find(id="tabBills")
bills_table_rows = bills_div.find_all('tr')
bills_table_rows.reverse()

#Create string for each Bill containing date, Bill name, and Bill URL
for item in bills_table_rows[:-1]:
    bill_date = item.find("td", { "class" : "date" }).string
    bill_name = item.find("a").string
    bill_anchor = item.find("a")
    bill_link = "http://www.aph.gov.au{0}".format(bill_anchor['href'])
    bill_string = "{0}: {1}, {2}".format(bill_date.encode('utf-8'),
                                            bill_name.encode('utf-8'),
                                            bill_link.encode('utf-8'))

    #Add Bill string to existing bills list if not already present
    if bill_string not in existing_bills:
        print "Adding new bill: {0}".format(bill_name.encode('utf-8'))
        existing_bills.append(bill_string)
        new_bills_added = True

with open('bills_output.txt', 'w') as f:
    for item in existing_bills:
        f.write('{0}\n'.format(item))


#This section runs the RSS update and FTP functions if new bills are added
if new_bills_added:
    print "Updating RSS"
    create_feed()
    ftp_feed()
    print "RSS update complete"
else:
    print "No new bills added, RSS up to date"