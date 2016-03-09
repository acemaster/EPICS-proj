import datetime
import csv
import time
import os
import requests
import re
import urllib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Traffic.settings')

import django
django.setup()
from datetime import datetime

from Accidents.models import *

import urllib
import json
from django.core import serializers

googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'

def get_coordinates(query, from_sensor=False):
    query = query.encode('utf-8')
    params = {
        'address': query,
        'sensor': "true" if from_sensor else "false"
    }
    url = googleGeocodeUrl + urllib.urlencode(params)
    json_response = urllib.urlopen(url)
    response = json.loads(json_response.read())
    if response['results']:
        location = response['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
        print query, latitude, longitude
    else:
        latitude, longitude = None, None
        print query, "<no results>"
    return latitude, longitude
all_accidents = []

def get_coordinates_map(query):
	q = query
	query = urllib.quote(query.strip())
	# police%20headquartera%2C%20warangal%2C%20india&oq=police%20headquartera%2C%20warangal%2C%20india&
	url = "https://www.google.co.in/search?tbm=map&fp=1&authuser=0&hl=en&pb=!4m9!1m3!1d13084.518433867801!2d79.53223145!3d17.983126149999997!2m0!3m2!1i787!2i662!4f13.1!7i10!10b1!12m6!2m3!5m1!2b0!20e3!10b1!16b1!19m3!2m2!1i392!2i106!20m44!2m2!1i203!2i100!3m1!2i4!6m6!1m2!1i86!2i86!1m2!1i408!2i256!7m30!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e3!2b0!3e3!1m3!1e4!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e3!2b1!3e2!2b1!4b1!9b0!22m6!1sivrfVtw_05W4BOK6tpAK!4m1!2i11887!7e81!12e3!18e15!24m3!2b1!5m1!5b1!26m3!2m2!1i80!2i92!30m28!1m6!1m2!1i0!2i0!2m2!1i458!2i662!1m6!1m2!1i737!2i0!2m2!1i787!2i662!1m6!1m2!1i0!2i0!2m2!1i787!2i20!1m6!1m2!1i0!2i642!2m2!1i787!2i662!37m1!1e81!42b1&q="+query+"&oq="+query+"&gs_l=maps.12..115i144.17203.38040.2.42035.44.44.0.0.0.0.6016.10631.3j17j5j2j9-1.28.0....0...1ac.1.64.maps..60.30.11312.0.&tch=1&ech=2&psi=ivrfVtw_05W4BOK6tpAK.1457519202769.1"
	r = requests.get(url)
	x = r.content
	pattern = "(?P<latlon>[0-9][0-9]\.[0-9]*\,[0-9][0-9]\.[0-9]*)"
	r = re.findall(pattern, x)
	lat_lon = r[0].split(",")
	print lat_lon
	lat = float(lat_lon[0])
	lon = float(lat_lon[1])
	print q, lat,lon
	return lat,lon


def upload_csv(file,start):
	all_accidents = []
	year = file.split(".")[0]
	finds = {}
	not_founds = []

	f = open(file, 'r')
	c = csv.reader(f)
	num = 0
	c.next()
	rows = []
	for row in c:
		rows.append(row)
	# print rows
	for row in rows:
		ind = int(row[0])
		if ind<start:
			continue
		# print row[1]
		# num += 1
		# print type(row)
		a = Accident()
		a.location = row[1]
		# print "______________________________", row[1]
		loc = row[1] + ", Warangal, India"
		print "FETCHING"
		lat, lon = get_coordinates_map(loc)
		valid = lat < 19.0
		# if valid:
		# 	not_founds.append(loc)
		# else:
		# 	finds[loc] = [lat,lon]
		if valid:
			a.lat = str(lat)
			a.lon = str(lon)
		elif not valid:
			all_others = Accident.objects.filter(location__startswith = loc[0])
			print "________________________________________________________________________"
			for index, accident in enumerate(all_others):
				print index, accident.location
			print "________________________________________________________________________"
			print "DId not find coordinates for "+ row[1]
			i = raw_input("Enter -1 if not found any previous location to enter. Else, enter the index")
			if i == "-1":
				lat = raw_input("Enter the latitude")
				lon = raw_input("enter the longitude")
				a.lat = (lat)
				a.lon = (lon)
			else:
				print "already exists"
				i = int(i)
				a.lat = (all_others[i].lat)
				a.lon =(all_others[i].lon)
		inj_death = row[3].split()
		if row[3] == "_" or row[3] == "-":
			a.deaths = 0
			a.injuries = 0
		else:
			if inj_death[1] == 'death':
				a.deaths = int(inj_death[0])
			elif inj_death[1] == 'injured':
				a.injuries = int(inj_death[0])
		a.vehicle = row[6]
		dt = datetime(int(year),1,1)
		a.date = dt
		a_dict = json.loads(serializers.serialize('json', [ a, ]))
		print type(a_dict)
		print len(a_dict)
		print a_dict[0]["fields"]
		all_accidents.append(a_dict[0]["fields"])

		time.sleep(1)
		a.save()
	# print num
	f = open(year+".json", "w")
	json.dump(all_accidents, f)
	f.close()
	# print finds
	# print not_founds


upload_csv("2008.csv",15)


print all_accidents

# lat,lon = get_coordinates("NIT main gate, Warangal, India")
# print lat, lon

# get_coordinates_map("Police headquarters, Warangal, India")