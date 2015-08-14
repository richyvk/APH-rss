APH-rss creates and RSS feed from the Australian Parliament site's Latest updates to Bills section (under the Bill stab at http://www.aph.gov.au/).

The feed offers alerts on when change are made to a Bill's homepage, effectively allowing for the tracking of any changes made to a Bill currently before the Australian Parliament, e.g. intorduced, debated, passed.

I creaetd this feed because I couldn't fidn any free source that offered an alerting service of this kind.

To use this feed:
=================

1. Clone this repo to your local computer
2. Create a text file named config.py and place it in the APH-rss directory. This contains ftp login, path where you want the rss file to be uploaded to on your remote site. See example content below:

Example content of config.py
----------------------------

run_path = '/PATH/TO/APH-rss DIR/'

ftp_url = 'ftp.yourdomain.com'
ftp_username = 'YOUR_FTP_USERNAME'
ftp_password = 'YOUR_FTP_PASSWORD'
ftp_target = '/PATH/TO/REMOTE/FTP/DIR/FOR/XML/FILE/'

3. From the APH-rss root directory run the command python APH-rss.py to run the script and create the feed

Requirements
============

1. Python 2.7, I'm using 2.7.6
2. See requirements.txt for required Python packages

Issues
======

If a Bill appears in the Latest updates to Bills list more than once in any day (which occassionaly happens) it will only receive one entry in the feed for that day.
This is not ideal, but I thought it would be enough for most people that a Bill appears once each day only.
Getting around this issue was proving to hard to figure out in the time I had.


This is a work in progress so things may change, but I've been ruinning it for a while now and it seems pretty stable so I won't change it much. Feel free to use it as you wish.

