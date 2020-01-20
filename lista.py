
from urllib import request, error
from urllib.parse import urlencode
import json
import time
import re

# ----------------------------------------------------------------

__version__ = '2.4.1'

API_VERSION = '1.2'

URL = 'https://randomuser.me/api/{}/'.format(API_VERSION)



# ----------------------------------------------------------------

class RandomUser:
    #: Dictionary where the random user data will be stored
    _data = {}
    #: Dictionary where info section of results will be stored
    _info = {}

    # Constants

    class PictureSize:

        LARGE = 'large'
        MEDIUM = 'medium'
        THUMBNAIL = 'thumbnail'

    class Info:

        SEED = 'seed'
        RESULTS = 'results'
        PAGE = 'page'
        VERSION = 'version'

    # Exceptions

    class APIError(Exception):


        def __init__(self, message):
            super().__init__(
                'randomuser.me API returned an error: {}'.format(message)
            )

    # Functions

    def __init__(self, get_params=None, user_data=None, api_info=None):

        global URL
        if user_data is not None:
            self._data = user_data
            self._info = api_info
        else:
            self.request_url = URL
            if get_params:
                self.request_url += '?' + urlencode(get_params)
            self._generate_user()

    def _generate_user(self):

        results = json.loads(request.urlopen(self.request_url).read())
        if 'error' in results:
            raise RandomUser.APIError(results['error'])
        self._data = results['results'][0]
        self._info = results['info']

    # Personal Info
    # --------------------------------

    def get_first_name(self, capitalize=True):

        first_name = self._data['name']['first']
        return first_name.title() if capitalize else first_name

    def get_last_name(self, capitalize=True):

        last_name = self._data['name']['last']
        return last_name.title() if capitalize else last_name

    def get_full_name(self, capitalize=True):

        first_name = self.get_first_name(capitalize)
        last_name = self.get_last_name(capitalize)
        full_name = '{} {}'.format(first_name, last_name)
        return full_name

    def get_gender(self):

        return self._data['gender']

    def get_dob(self, parse_time=False):

        dob = self._data['dob']['date']
        if parse_time:
            dob = self._parse_time(dob)
        return dob

    def get_age(self):

        return self._data['dob']['age']

    def get_nat(self):

        return self._data['nat']


    def get_street(self, capitalize=True):

        street = self._data['location']['street']
        return street.title() if capitalize else street

    def get_city(self, capitalize=True):

        city = self._data['location']['city']
        return city.title() if capitalize else city

    def get_state(self, capitalize=True):

        state = self._data['location']['state']
        return state.title() if capitalize else state

    def get_postcode(self):

        return self._data['location']['postcode']

    def get_zipcode(self):

        return self.get_postcode()

    def get_coordinates(self):

        return self._data['location']['coordinates']



    def _format_phone_number(self, phone_string,
                             strip_parentheses=True, strip_hyphens=True):

        if strip_parentheses:
            phone_string = re.sub('[()]', '', phone_string)
        if strip_hyphens:
            phone_string = re.sub('-', '', phone_string)
        return phone_string

    def get_phone(self, strip_parentheses=False, strip_hyphens=False):

        return self._format_phone_number(self._data['phone'],
                                         strip_parentheses=strip_parentheses,
                                         strip_hyphens=strip_hyphens)

    def get_cell(self, strip_parentheses=False, strip_hyphens=False):

        return self._format_phone_number(self._data['cell'],
                                         strip_parentheses=strip_parentheses,
                                         strip_hyphens=strip_hyphens)

    def get_email(self):

        return self._data['email']


    # --------------------------------

    def get_username(self):

        return self._data['login']['username']

    def get_password(self):

        return self._data['login']['password']

    def get_registered(self, parse_time=False):

        registered = self._data['registered']['date']
        if parse_time:
            registered = self._parse_time(registered)
        return registered

    def get_registered_age(self):

        return self._data['registered']['age']

    def get_login_salt(self):

        return self._data['login']['salt']

    def get_login_md5(self):

        return self._data['login']['md5']

    def get_login_sha1(self):

        return self._data['login']['sha1']

    def get_login_sha256(self):

        return self._data['login']['sha256']

    def get_login_uuid(self):

        return self._data['login']['sha256']


    # --------------------------------

    def get_id_type(self):

        return self._data['id']['name']

    def get_id_number(self):

        return self._data['id']['value']

    def get_id(self):

        return {'type': self.get_id_type(), 'number': self.get_id_number()}


    # --------------------------------

    def get_picture(self, size=PictureSize.LARGE):

        return self._data['picture'][size]

    def get_info(self):

        return self._info


    # --------------------------------

    def _parse_time(self, date_string):

        date_format = '%Y-%m-%dT%H:%M:%SZ'
        return time.strptime(date_string, date_format)


    # --------------------------------

    @staticmethod
    def generate_users(amount, get_params=None):

        global URL
        if get_params is None:
            get_params = {}

        get_params['results'] = amount if amount <= 5000 else 5000
        request_url = URL + '?' + urlencode(get_params)
        results = json.loads(request.urlopen(request_url).read())
        if 'error' in results:
            raise RandomUser.APIError(results['error'])
        info = results['info']
        users = []
        for user_data in results['results']:
            user = RandomUser(user_data=user_data, api_info=info)
            users.append(user)
        return users

