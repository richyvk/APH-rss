import os
import datetime
import urllib2
import PyRSS2Gen
from ftplib import FTP
from bs4 import BeautifulSoup
import config

#Config setup example (save as config.py in APH-rss root dir):
#
#run_path = '/PATH/TO/APH-rss DIR/'
#
#ftp_url = 'ftp.yourdomain.com'
#ftp_username = 'YOUR_FTP_USERNAME'
#ftp_password = 'YOUR_FTP_PASSWORD'
#ftp_target = '/PATH/TO/REMOTE/FTP/DIR/FOR/XML/FILE/'

#change directory to APH-rss root dir, for Pythonanywhere scheduled task only
os.chdir(config.run_path)

#This section scrapes the latest updates to bills section of the APH homepage,
#http://www.aph.gov.au/, extracting the update date, bill name and bill
#homepage URL, and adding this information to a text file for later convertion
#to an RSS feed.

#open or create the txt file, and add each line to a list object
existing_bills = open('bills_output.txt', 'a+').read().splitlines()

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

    #Add Bill string to bill list if not already present and write resulting
    #list back to txt file
    if bill_string not in existing_bills:
        print "Adding new bill: {0}".format(bill_name.encode('utf-8'))
        with open('bills_output.txt', 'a') as f:
            f.write('{0}\n'.format(bill_string))

#This section converts the scraped data in the text file into an RSS2 feed using
#PyRSS2Gen.


#set date for RSS lastBuildDate variable
lastModified = os.path.getmtime('bills_output.txt')
lastModifiedDatetime = datetime.datetime.fromtimestamp(lastModified)
print "Assigning last modified date as: {0}".format(lastModifiedDatetime)

#open and read the txt file; add each line to a list object
bills_list = open('bills_output.txt').read().splitlines()

bill_items = []

#split each Bill string into parts and create PyRSS2Gem RSSItem objects from
#them
for bill in bills_list:
    #Extract relevant bits of each Bill string
    date = bill[:bill.find(':')]
    bill_url = bill[bill.find('http'):]
    bill_title = bill[bill.find(':')+2:bill.find('http')-2]

    #convert extracts into RRS items
    item = PyRSS2Gen.RSSItem(title = bill_title,
            link = bill_url,
            description = bill_title + " - bill homepage updated " + date)

    #Append all items to a list
    bill_items.append(item)

#List needs to be reversed to get newest Bills to the top
bill_items.reverse()

#Create the RSS feed and write it to file
rss = PyRSS2Gen.RSS2(title = "Richard's APH Bills RSS",
        link = "https://github.com/richyvk/APH-RSS",
        description = "An RSS feed of Bill updates from the APH homepage",
        lastBuildDate = lastModifiedDatetime,
        items = bill_items)

rss.write_xml(open("feed.xml", "w"))

#This section uploads the feed file via FTP

#establish ftp connection and login
ftp = FTP(config.ftp_url)
ftp.login(config.ftp_username,config.ftp_password)

ftp.cwd(config.ftp_target)
ftp.storbinary('STOR '+'feed.xml', open('feed.xml', 'rb'))
print "File FTPed successfully"
ftp.quit()