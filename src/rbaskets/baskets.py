import requests
import rbaskets
from datetime import datetime
import json
import string
import random

class Basketinfo:
    def __init__(self, json: dict) -> None:
        self.__basket = json

    @property
    def name(self) -> str:
        """Basket name"""
        return self.__basket['name']

    @property
    def request_count(self) -> int:
        """Current number of collected HTTP requests held by basket"""
        return self.__basket['request_count']

    @property
    def request_total_count(self) -> int:
        """Total number of all HTTP requests passed through this basket"""
        return self.__basket['request_total_count']

    @property
    def last_request_date(self) -> datetime:
        """Date and time of last request processed through this basket in Unix time ms. format (number of milliseconds elapsed since January 1, 1970 UTC).

        If no requests were collected by this basket `None` is returned.
        """
        timestamp = self.__basket['last_request_date']
        if timestamp == 0:
            return None
        return datetime.fromtimestamp(timestamp)

class Stats:
    """Get service statistics about baskets and collected HTTP requests. Require master token.

    Arguments:
    :param service_token(str): Service master token
    :param max(int): Maximum number of basket names to return (default: 5)
    """
    def __init__(self, service_token: str, max: int = 5) -> None:
        API_PATH = "/api/stats"
        headers = {'Authorization': service_token}
        
        res = requests.get(rbaskets.host + API_PATH, params={'max': max},headers=headers)

        if res.status_code == 200:
            self.body = json.loads(res.text)
        elif res.status_code == 401:
            raise requests.HTTPError('Unauthorized. Invalid or missing master token')
        else:
            res.raise_for_status()

    @property
    def baskets_count(self) -> int:
        """Total number of baskets managed by service"""
        return self.body['baskets_count']
    
    @property
    def empty_baskets_count(self) -> int:
        """Number of empty baskets"""
        return self.body['empty_baskets_count']

    @property
    def requests_count(self) -> int:
        """Number of HTTP requests currently stored by service"""
        return self.body['requests_count']

    @property
    def requests_total_count(self) -> int:
        """Total number of HTTP requests processed by service"""
        return self.body['requests_total_count']
    
    @property
    def max_basket_size(self) -> int:
        """Size of the biggest basket that processed the top most number of HTTP requests"""
        return self.body['max_basket_size']
    
    @property
    def avg_basket_size(self) -> int:
        """Average size of a basket in the system, empty baskets are not taken into account"""
        return self.body['avg_basket_size']

    @property
    def top_baskets_size(self) -> list:
        """Collection of top basket by size"""
        __top_backets_size = self.body['top_baskets_size']
        if __top_backets_size == None:
            return []

        __basketinfos = []

        for __basketinfo in __top_backets_size:
            __basketinfos.append(Basketinfo(__basketinfo))

        return __basketinfos

    @property
    def top_baskets_recent(self) -> list:
        """Collection of top baskets recently active"""
        __top_baskets_recent = self.body['top_baskets_recent']
        if __top_baskets_recent == None:
            return []

        __basketinfos = []

        for __basketinfo in __top_baskets_recent:
            __basketinfos.append(Basketinfo(__basketinfo))

        return __basketinfos

class Baskets:
    """Fetches a list of basket names managed by service. Require master token.
    
    :param service_token(str): Service master token
    :param max(int): Maximum number of basket names to return (default: 20)
    :param skip(int): Number of basket to skip (default: 0)
    :param q(str): Query string to filter result, only those basket names that match the query will be included in response (default: None)
    """
    def __init__(self, service_token : str, max = 20, skip = 0, q = None) -> None:
        API_PATH = "/api/baskets"
        headers = {'Authorization': service_token}

        params = {
            'max': max,
            'skip': skip,
        }

        if q != None:
            params['q'] = q

        res = requests.get(rbaskets.host + API_PATH, params=params, headers=headers)

        if res.status_code == 200:
            self.body = json.loads(res.text)
        elif res.status_coe == 204:
            return None
        elif res.status_code == 401:
            raise requests.HTTPError('Unauthorized. Invalid or missing master token')
        else:
            res.raise_for_status()

    @property
    def names(self) -> list:
        """Collection of basket names"""
        return list(self.body['names'])

    @property
    def count(self) -> int:
        """Total number of baskets in the system
        Not Present if query is applied"""
        try:
            return self.body['count']
        except:
            return None
        
    
    @property
    def has_more(self) -> bool:
        """Indicates if there ara more baskets to fetch"""
        return self.body['has_more']

class Basket:
    """
    Retrieves configuration settings of `basket_token`.

    :param basket_token: Basket assigned secure token. If `basket_token` is None, Create a basket with name. Basket are created with default setting. (defulat: None)
    :param name: The basket name. If `name` is None, It is assigned a 16-character random name. (default: None) 
    """

    def __init__(self, basket_token: str = None, name: str = None) -> None:
        if (basket_token != None and name == None):
            raise ValueError('Missing basket name')
        
        if (basket_token == None):
            if name == None:
                name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
            self.__name = name
            self.__create()
        else:
            self.__name = name
            self.token = basket_token

        self.api_path = f'/api/baskets/{self.__name}'
        self.headers = {'Authorization': self.token}
        self.request_url = rbaskets.host + self.api_path

        res = requests.get(self.request_url, headers=self.headers)

        if res.status_code == 200:
            self.body = json.loads(res.text)
        elif res.status_code == 401:
            raise requests.HTTPError('Unauthorized. Invaild or missing basket token')
        elif res.status_code == 404:
            raise requests.HTTPError('Not Found. No basket with such name')
        else:
            res.raise_for_status()

    def __create(self) -> str:
        """Creates a new basket with this name."""
        self.body = {
            'forward_url': '',
            'proxy_response': False,
            'insecure_tls': False,
            'expand_path': False,
            'capacity': 200
        }

        self.api_path= f'/api/baskets/{self.__name}'
        self.request_url = rbaskets.host + self.api_path
        res = requests.post(self.request_url, data=json.dumps(self.body))

        if res.status_code == 201:
            __body = json.loads(res.text)
        elif res.status_code == 400:
            raise requests.HTTPError('Bad Request. Failed to parse JSON info basket configuration object.')
        elif res.status_code == 403:
            raise requests.HTTPError('Forbidden. Indicates that basket name conflicts with reserved paths; e.g. `baskets`, `web`, etc.')
        elif res.status_code == 409:
            raise requests.HTTPError('Conflict. Indicates that basket with such name already exists')
        elif res.status_code == 422:
            raise requests.HTTPError('Unprocessable Entity. Basket configuration is not valid.')
        else:
            res.raise_for_status()

        self.token = __body['token']


    def update(self, forward_url: str = None, proxy_response: bool = None, insecure_tls: bool = None, expand_path: bool = None, capacity: int = 200) -> bool:
        """
        Updates configuration settings of this basket.

        Special configuration parameters for request forwarding:

        * `insecure_tls` controls certificate verification when forwarding requests. Setting this parameter to `true` allows to forward collected HTTP requests via HTTPS protocol even if the forward end-point is configured with self-signed TLS/SSL certificate. Warning: enabling this feature has known security implications.
        * `expand_path` changes the logic of constructing taget URL when forwarding requests. If this parameter is set to true the forward URL path will be expanded when original HTTP request contains compound path. For example, a basket with name server1 is configured to forward all requests to `http://server1.intranet:8001/myservice` and it has received an HTTP request like GET `http://baskets.example.com/server1/component/123/events?status=OK` then depending on `expand_path` settings the request will be forwarded to:
            * `true` => `GET http://server1.intranet:8001/myservice/component/123/events?status=O`
            * `false` => `GET http://server1.intranet:8001/myservice?status=OK`
        """
        print(self.request_url)
        self.body = {
            'forward_url': self.forward_url 
        }

        res = requests.put(self.request_url, json=json.dumps(self.body), headers=self.headers)

        if res.status_code == 204:
            return True
        elif res.status_code == 400:
            raise requests.HTTPError('Bad Request. Failed to parse JSON into basket configuration object.')
        elif res.status_code == 401:
            raise requests.HTTPError('Unauthorized. Invaild or missing basket token.')
        elif res.status_code == 404:
            raise requests.HTTPError('Not Found. No basket with such name')
        elif res.status_code == 422:
            raise requests.HTTPError('Unprocessable Entity. Basket configuration is not vaild.')
        else:
            res.raise_for_status()

    def delete(self) -> bool:
        res = requests.delete(self.request_url, headers=self.headers)

        if res.status_code == 204:
            return True
        elif res.status_code == 401:
            raise requests.HTTPError('Unauthorized. Invalid or missing basket token')
        elif res.status_code == 404:
            raise requests.HTTPError('Not Found. No basket with such name')
        else:
            res.raise_for_status()

    @property
    def basket_token(self) -> str:
        """Basket assigned secure token"""
        return self.token
    
    @property
    def name(self) -> str:
        """The basket name"""
        return self.__name

    @property
    def forward_url(self) -> str:
        """URL to forward all incoming requests of the basket, `None` value disables forwarding"""
        return self.body['forward_url']

    @property
    def proxy_response(self) -> bool:
        """If set to `true` this basket behaves as a full proxy: responses from underlying service configured in `forward_url` are passed back to clients of original requests. THe configuration of basket response is ignored in this case."""
        return self.body['proxy_response']

    @property
    def insecure_tls(self) -> bool:
        """If set to `true` the certificate verification will be disabled if forward URL indicates HTTPS scheme. **Warning:** enabling this feature has known security implications."""
        return self.body['insecure_tls']

    @property
    def expand_path(self) -> bool:
        """If set to `true` the forward URL path will be expanded when original HTTP request contains compound path."""
        return self.body['expand_path']

    @property
    def capacity(self) -> int:
        """Baskets capacity, defines maximum number of requests to store"""
        return self.body['capacity']