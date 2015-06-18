import os
import datetime
import PyRSS2Gen
from ftplib import FTP
import config

def run_rss():
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

def run_ftp():
    #establish ftp connection and login
    ftp = FTP(config.ftp_url)
    ftp.login(config.ftp_username,config.ftp_password)

    ftp.cwd(config.ftp_target)
    ftp.storbinary('STOR '+'feed.xml', open('feed.xml', 'rb'))
    print "File FTPed successfully"
    ftp.quit()