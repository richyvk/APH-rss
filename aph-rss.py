import datetime
import urllib2
import PyRSS2Gen
from bs4 import BeautifulSoup

new_bills = []
with open('bills_output.txt', 'a+') as f:
    for line in f:
        new_bills.append(line.rstrip())

source = urllib2.urlopen("http://www.aph.gov.au/").read()

soup = BeautifulSoup(source)

bills_div = soup.find(id="tabBills")
bills_table_rows = bills_div.find_all('tr')
bills_table_rows.reverse()

for item in bills_table_rows[:-1]:
    bill_date = item.find("td", { "class" : "date" }).string
    bill_name = item.find("a").string
    bill_anchor = item.find("a")
    bill_link = "http://www.aph.gov.au{0}".format(bill_anchor['href'])
    bill_string = "{0}: {1}, {2}".format(bill_date.encode('utf-8'), bill_name.encode('utf-8'), bill_link.encode('utf-8'))

    if bill_string not in new_bills:
        print "Adding new bill: {0}".format(bill_name.encode('utf-8'))
        with open('bills_output.txt', 'a') as f:
            f.write('{0}\n'.format(bill_string))

bills_list = open('bills_output.txt').read().splitlines()

bill_items = []

for bill in bills_list:
    date = bill[:bill.find(':')]
    bill_url = bill[bill.find('http'):]
    bill_title = bill[bill.find(':')+2:bill.find('http')-2]

    item = PyRSS2Gen.RSSItem(title = bill_title,
            link = bill_url,
            description = bill_title + " - bill homepage updated " + date)

    bill_items.append(item)

bill_items.reverse()

rss = PyRSS2Gen.RSS2(title = "Richard's APH Bills RSS",
        link = "http://www.pittstreetpress.com/APH-RSS",
        description = "An RSS feed of Bill updates from the APH homepage",
        lastBuildDate = datetime.datetime.now(),
        items = bill_items)

rss.write_xml(open("feed.xml", "w"))

#soup = BeautifulSoup(open('feed.xml'))

#print soup.prettify()