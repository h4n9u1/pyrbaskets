import requests
import rbaskets
import json
from datetime import datetime

class Request:
    def __init__(self, data) -> None:
        self.__request = data

    @property
    def date(self) -> datetime:
        """Date and time of request"""
        print(self.__request['date'])
        return datetime.fromtimestamp(self.__request['date'] / 1000)

    @property
    def headers(self) -> dict:
        """Map of HTTP headers, key represents name, value is array of values"""
        return self.__request['headers']
    
    @property
    def content_length(self) -> int:
        """Content length of request"""
        return self.__request['content_length']

    @property
    def body(self) -> str:
        """Content of request body"""
        return self.__request['body']
    
    @property
    def method(self) -> str:
        """HTTP method of request"""
        return self.__request['method']
    
    @property
    def path(self) -> str:
        """URL path of request"""
        return self.__request['path']

    @property
    def query(self) -> str:
        """Query parameters of request"""
        return self.__request['query']
        
class Requests:
    """
    Manage collected requests

    :param basket_token: Basket assigned secure token (required)
    :param name: The basket name (required)
    :param max: Maximum number of requets to return (default: 20)
    :param skip: Number of requests to skip (default: 0)
    :param q: Query string to filter result, only requests that match the query will be included in response (default: None)
    :param in: Defines what is taken into account when filtering is applied: `body` - search in content body of collected requests, `query` - search among query parameters of collected requests, `headers` - search among request header values, `any` - search anywhere (default: `any`)
    """
    def __init__(self, basket_token: str, name: str, max: int = 20, skip: int = 0, q: str = None, _in: str = 'any') -> None:
        self.__api_path = rbaskets.host
        self.__api_path += f'/api/baskets/{name}/requests'

        self.__headers = {'Authorization': basket_token}

        params = {
            'max' : max,
            'skip' : skip,
            'in': _in
        }

        if q != None:
            params['q'] = q


        res = requests.get(self.__api_path, headers=self.__headers, params=params)
        if res.status_code == 200:
            self.__body = json.loads(res.text)
        elif res.status_code == 204:
            self.__body = None
        elif res.status_code == 401:
            raise requests.HTTPError('Unauthorized. Invalid or missing basket token')
        elif res.status_code == 404:
            raise requests.HTTPError('Not Found. No basket with such name')
        else:
            res.raise_for_status()

        
    @property
    def count(self) -> int:
        """Current number of collected requests hold by basket; not present if query is applied"""
        try:
            return self.__body['count'] if self.__body != None else None
        except:
            return None
    
    @property
    def total_count(self) -> int:
        """Total number of all requests passed through this basket; not present if query is applied"""
        try:
            return self.__body['total_count'] if self.__body != None else None
        except:
            return None
    
    @property
    def requests(self) -> list:
        """Collection of collected requests"""
        return list(map(lambda x: Request(x), self.__body['requests']))

    @property
    def has_more(self) -> bool:
        """Indicates if there are more requests collected by basket to fetch"""
        return self.__body['has_more']


    def delete(self) -> bool:
        """
        Deletes all requests collected by this basket.
        """
        res = requests.delete(self.__api_path)

        if res.status_code == 204:
            return True
        elif res.status_code == 401:
            raise requests.HTTPError('Unauthorized. Invalid or missing basket token')
        elif res.status_code == 404:
            raise requests.HTTPError('Not Found. No basket with such name')
        else:
            res.raise_for_status()
        