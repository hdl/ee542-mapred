#!/usr/bin/env python
import argparse
import json
import sys
import urllib2
import oauth2
#remember to use bootstrap script!
import csv

API_HOST = 'api.yelp.com'
SEARCH_PATH = '/v2/search/'

CONSUMER_KEY = "jVloKhUOwFLiro5HbCLLAQ"
CONSUMER_SECRET = "YArRQzDqP21-TxwpEvfypYESvO0"
TOKEN = "l82LTIQirsjrKPvKd57bs6b2K12Xwr-x"
TOKEN_SECRET = "xNb0aHRow5_ElvwcH8Ge2yJD324"

#request function code from Yelp API example
def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'http://{0}{1}?'.format(host, path)

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    #print 'Querying {0} ...'.format(url)
	
    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response

def search(s_lat, s_long):
	url_params = {
		'category_filter':"galleries,movietheaters,museums,coffee,restaurants",
		#searches for galleries, movie theaters, museums, coffee shops, and restaurants
		'll':s_lat+","+s_long,
		#uses latitude and longitude field of table
		'radius_filter':"100"
		#set search radius within 100m of each location
		}
	return request(API_HOST,SEARCH_PATH,url_params = url_params)

#due to Yelp returning utf-8 encoded chars	
def removeNonAscii(s):
	return "".join(i for i in s if ord(i)<128)
	
seenLocations = dict() #keeps track of already queried locations
reader = csv.reader(sys.stdin, delimiter = ',')
for line in reader:
	stationName = line[1]
	stationAddr = line[2]
	stationZip = line[6]
	coordLat = line[24]
	coordLong = line[25]
	intermediate_key = "("+line[24]+", "+line[25]+")"
	#key is string of coordinates
	#some stations are located at same location - should get same score
	if intermediate_key in seenLocations:
		seenLocations[intermediate_key] += 1
		# keeps track of how many stations in one location
		continue
		# does not do another Yelp query since it would double the score
	else:
		seenLocations[intermediate_key] = 1
		searchResults = search(coordLat,coordLong).get('businesses')
		for business in searchResults:
			print intermediate_key+'\t'+removeNonAscii(business['name'])
			#value is string of business name
