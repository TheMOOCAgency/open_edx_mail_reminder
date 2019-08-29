""" Views for a student's profile information. """

from django.conf import settings
import logging
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.decorators.http import require_http_methods
from django_countries import countries
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST,require_GET,require_http_methods
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)



import requests

# url = "http://localhost/user_api/v1/:18080"

# params = dict(
    # origin='Chicago,IL',
    # destination='Los+Angeles,CA',
    # waypoints='Joplin,MO|Oklahoma+City,OK',
    # sensor='false'
# )

# resp = requests.get(url=url)
# data = resp.json()

@csrf_exempt
def bon():
	r = requests.get('http://127.0.0.1/user_api/v1/users/')
	ruda = r.json()
	print(ruda)

# api_url2  = 'http://127.0.0.1/user_api/v1/users/166'
# api_url2  = 'http://127.0.0.1/api/courses/v1/courses/?course-v1:prorefei+ATEE+RE2019/users? enrollment_type=student&include=email'
api_url2  = 'http://127.0.0.1/api/courses/v1/courses/?course_id=course-v1:prorefei+ATEE+RE2019/users?enrollment_type=student&include=email'
# api_url2  = 'http://127.0.0.1/api/courses/v1/courses/course-v1:prorefei+ATEE+RE2019'


# api_url2  = 'http://127.0.0.1/api/courses/v1/courses/?course_id=course-v1:prorefei+ATEE+RE2019/instructor/api/get_students_features'

# "https://pprod1.the-mooc-agency.com/api/courses/v1/blocks/?course_id=course-v1%3ADTU%2BDTU101%2B2019
# api_url2  = 'http://127.0.0.1/courses/course-v1:prorefei+ATEE+RE2019/instructor/api/get_students_features'
# api_url2  = 'http://127.0.0.1/user_api/v1/user_prefs/'
# api_url2  = 'http://127.0.0.1/user_api/v1/user_prefs/155/'

class UserServiceException(Exception):
    pass

def _headers():
    return {'X-EDX-API-Key': settings.US_API_KEY}

def _auth():
    auth = {}
    if settings.US_HTTP_AUTH_USER:
        auth['auth'] = (settings.US_HTTP_AUTH_USER, settings.US_HTTP_AUTH_PASS)
    return auth

def _http_get(*a, **kw):
    try:
        logger.debug('GET {} {}'.format(a[0], kw))
        response = requests.get(*a, **kw)
    except requests.exceptions.ConnectionError, e:
        _, msg, tb = sys.exc_info()
        raise UserServiceException, "request failed: {}".format(msg), tb
    if response.status_code != 200:
        raise UserServiceException, "HTTP Error {}: {}".format(
            response.status_code,
            response.reason
        )
    return response
	
r = _http_get(api_url2, headers=_headers(), **_auth())
ruda = r.json()
print(ruda)
