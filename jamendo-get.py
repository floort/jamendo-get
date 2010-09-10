#!/usr/bin/env python

import urllib2
import os
import gzip

DB_FILE = "jamendo_db.xml.tgz"


# Download the database if it doesn't exsists yet.
if not os.path.isfile(DB_FILE):
	print "Downloading", DB_FILE
	f = open(DB_FILE,"w")
	f.write(urllib2.urlopen("http://img.jamendo.com/data/dbdump_artistalbumtrack.xml.gz").read())
	f.close()
else:
	print "Database allready downloaded."

print "Reading the database"
xml = gzip.open(DB_FILE, "r").read()

print "Downloading files"
artist_start = 0
artist_end = artist_start
while artist_start > -1:
	artist_start = xml.find("<artist>", artist_end)+8
	artist_end = xml.find("</artist>", artist_start)
	artist = xml[xml.find("<name>",artist_start)+6:xml.find("</name>",artist_start)].replace("/","_")
	if not os.path.isdir("download/"+artist):
		os.mkdir("download/"+artist)
	album_start = artist_start
	album_end = album_start
	while album_start < artist_end:
		album_start = xml.find("<album>", album_end)+7
		album_end = xml.find("</album>", album_start)
		album = xml[xml.find("<name>",album_start)+6:xml.find("</name>",album_start)].replace("/", "_")
		album_id = xml[xml.find("<id>",album_start)+4:xml.find("</id>",album_start)]
		if not os.path.isdir("download/"+artist+"/"+album):
			os.mkdir("download/"+artist+"/"+album)
		open("download/"+artist+"/"+album+"/cover.jpg","w").write(urllib2.urlopen("http://api.jamendo.com/get2/image/album/redirect/?id=%s&imagesize=600" %(album_id)).read())
		track_start = album_start
		track_end = track_start
		while track_start < album_end:
			track_start = xml.find("<track>", track_end)+7
			track_end = xml.find("</track>", track_start)
			track_id = xml[xml.find("<id>",track_start)+4:xml.find("</id>",track_start)]
			track_filename = xml[xml.find("<filename>",track_start)+10:xml.find("</filename>",track_start)].replace("/","_")
			print "download/"+artist+"/"+album+"/"+track_filename+".mp3"
			open("download/"+artist+"/"+album+"/"+track_filename+".mp3","w").write(urllib2.urlopen("http://api.jamendo.com/get2/stream/track/redirect/?id=%s&streamencoding=mp31" %(track_id)).read())




