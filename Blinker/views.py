from django.shortcuts import render
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

def home(request):
    context = {}
    print "haha"
    return render(request, 'Blinker/index.html', context)

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

    print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response

def search(term, locationCordinates, miles):

    print "location coordinates " + locationCordinates
    url_params = {
        'term': term.replace(' ', '+'),
        'll': locationCordinates,
        'radius_filter':miles
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def get_business(business_id):
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)

def query_api(term, lloc, llong, miles):

    response = search(term, lloc+','+llong, miles)

    businesses = response.get('businesses')

    if not businesses:
        print u'No businesses for {0} in {1} found.'
        return

    business_id = businesses[0]['id']

    print u'{0} businesses found, querying business info for the top result "{1}" ...'.format(
        len(businesses),
        business_id
    )

    response = get_business(business_id)

    print u'Result for business "{0}" found:'.format(business_id)
    pprint.pprint(response, indent=2)

def searchyelp(request):

    context = {}

    if request.method == 'POST':

        searchterm = request.POST.get('term', False)
        searchslatitude = request.POST.get('latitude', False)
        searchlongitude = request.POST.get('longitude', False)
        searchmiles = request.POST.get('miles', False)

        print searchterm
        print searchslatitude
        print searchlongitude
        print searchmiles

        try:
            query_api(searchterm, searchslatitude, searchlongitude, searchmiles)
        except urllib2.HTTPError as error:
            sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))


    return render(request, 'Blinker/index.html', context)



def cleanJson(request):
    context = {}
    return render(request, 'Blinker/displayCleanJason.html', context)
