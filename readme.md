APH_RSS feed generator
======================

Update - 30/09/2016
-------------------

The APH site was revamped recently. I've fixed the main script so it now works with the new APH site, scraping the Bills info form this page: http://www.aph.gov.au/Parliamentary_Business/Bills_Legislation

In their wisdom APH have decided to truncate long Bill titles on the page and unfortunately I'm stuck with using those truncated titles for now. Apart from that issue everything else remains the same as with the previous version.

Update - 9/12/2015
------------------

I changed the link the Bill link URL from the original mirrored Bill homepage on the APH site to the Parlinfo Search Bill Homepage. 

I prefer this page, it has the samwe information but the layout is nicer I think, and I suspect it will be less likely to change over time.

Usage
-----

APH-rss creates an RSS feed from the Australian Parliament site's Latest updates to Bills section (under the Bill stab at http://www.aph.gov.au/).

The feed provides a way of receiving alerts when changes are made to a Bill's homepage, effectively allowing for the tracking of any changes made to a Bill currently before the Australian Parliament, e.g. intorduced, debated, passed.

I created this feed because I couldn't find any free source that offered an alerting service of this kind.

To use this feed:
-----------------

1. Clone this repo to your local computer
2. Create a text file named config.py and place it in the APH-rss directory. This contains ftp login, path where you want the rss file to be uploaded to on your remote site. See example content below.
3. From the APH-rss root directory run the command python APH-rss.py to run the script and create the feed

Example config.py
-----------------

    run_path = '/PATH/TO/APH-rss DIR/'

    ftp_url = 'ftp.yourdomain.com'
    ftp_username = 'YOUR_FTP_USERNAME'
    ftp_password = 'YOUR_FTP_PASSWORD'
    ftp_target = '/PATH/TO/REMOTE/FTP/DIR/FOR/XML/FILE/'

Requirements
------------

1. Python 2.7, I'm using 2.7.6
2. See requirements.txt for required Python packages

Issues
------

If a Bill appears in the Latest updates to Bills list more than once in any day (which occassionaly happens) it will only receive one entry in the feed for that day.
This is not ideal, but I thought it would be enough for most people that a Bill appears once each day only.
Getting around this issue was proving to hard to figure out in the time I had.


This is a work in progress so things may change, but I've been ruinning it for a while now and it seems pretty stable so I won't change it much. Feel free to use it as you wish.

