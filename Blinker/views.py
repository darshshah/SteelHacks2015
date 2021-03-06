from django.shortcuts import render,redirect
import argparse
import json
import pprint
import sys
import urllib
import urllib2

import oauth2


API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 20
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = 'ILOB-dShAji_vpNOVEMlyg'
CONSUMER_SECRET = 'plwiQyMEKFLYczIEsUoAS-rrpYU'
TOKEN = 'ya0NHVyyCHFAdWYAaUzFfTEcw4BKQQ99'
TOKEN_SECRET = '6PSzFL2hqhgRkITzHsPo0rQ1u2U'



# Constants to change
DISPLAY_NO = 5

def home(request):
    context = {}
    print "haha"
    return render(request, 'Blinker/multiple-points.html', context)

# Create your views here.
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
    url = 'http://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

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
    print signed_url
    #print u'Querying {0} ...'.format(signed_url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response

def searchingYelp(term, locationCordinates, miles):
    print 'in search'
    meter = 1609.34 * float(miles)
    print 'afer meter'
    #print "location coordinates " + locationCordinates
    url_params = {
        'term': term.replace(' ', '+'),
        'll': locationCordinates.replace(' ', ','),
        'radius_filter':meter
    }

    print url_params

    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def get_business(business_id):
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)

def query_api(term, lloc, llong, miles):

    print 'query sent'
    print 'le'
    response = searchingYelp(term, str(lloc)+' '+str(llong), miles)
    
    businesses = response.get('businesses')
    
    if not businesses:
        print u'No businesses for {0} in {1} found.'
        return null

    return businesses

def getGasStations(searchslatitude, searchslongitude, searchmiles):
    gasurl = 'http://devapi.mygasfeed.com/stations/radius/' + str(searchslatitude) + '/' + str(searchslongitude) + '/' + str(searchmiles) + '/reg/distance/rfej9napna.json?'

    conn = urllib2.urlopen(gasurl, None)

    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response


def searchyelp(request):
    
    context={}
    allBusinesses=[]
    gasBusiness=[]
    
    if request.method == 'GET':
        searchterm = 'food'
        data = json.loads(request.GET.get('position'))
        searchslatitude= data['k']
        searchslongitude =data['D']
        searchmiles = request.GET.get('distance')

        print searchslatitude
        print searchslongitude

    '''
    if request.method == 'POST':

        searchterm = request.POST.get('term', False)
        searchslatitude = request.POST.get('latitude', False)
        searchlongitude = request.POST.get('longitude', False)
        searchmiles = request.POST.get('miles', False)
    '''
    
    businessToClean = query_api(searchterm, searchslatitude, searchslongitude, searchmiles)

    #gasStationsNearMe = getGasStations(searchslatitude, searchslongitude, searchmiles)

    print "gas station info \n"
    #print gasStationsNearMe
    #print businessToClean

    try:
        for x in range(0,DISPLAY_NO):
            allBusinesses.append(cleanJson(businessToClean[x]))

        #for y in range(0,DISPLAY_NO):
            #gasBusiness.append(cleanJsonGas(gasStationsNearMe['stations'][y]))
            
    except urllib2.HTTPError as error:
        sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))

    print 'I am final'
    
    context['businesses'] = allBusinesses
    context['searchTerm'] = searchterm
    context['gasstations'] = gasBusiness

    return render(request, 'Blinker/displayCleanJason.html', context)


def pointsArray(request):
    print request.GET['array']
    return redirect('home')

def cleanJsonGas(gaspumps):
    context = {}

    context['business_name'] = gaspumps.get('station')
    context['business_address']= gaspumps.get('address')
    context['price'] = gaspumps.get('reg_price')

    return context


def cleanJson(business):
    
    context={}
    context['business_name'] = business.get('name')
    context['business_phone'] = business.get('phone')
    context['business_address']= business.get('location').get('address')[0]
    context['business_image'] = business.get('image_url')
    context['business_rating'] = business.get('rating')
    context['business_ratingImage'] = business.get('rating_img_url')
    context['business_url'] = business.get('mobile_url')
    context['business_lat'] = business.get('location').get('coordinate').get('latitude')
    context['business_long'] = business.get('location').get('coordinate').get('longitude')
    return context
