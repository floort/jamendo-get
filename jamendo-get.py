#!/usr/bin/env python

import urllib2
import os


DB_FILE = "jamendo_db.xml.tgz"

# Download the database if it doesn't exsists yet.
if not os.path.isfile(DB_FILE):
	print "Downloading", DB_FILE
	f = open(DB_FILE,"w")
	f.write(urllib2.urlopen("http://img.jamendo.com/data/dbdump_artistalbumtrack.xml.gz").read())
	f.close()
else:
	print "Database allready downloaded."
