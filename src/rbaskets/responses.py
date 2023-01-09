import requests
import rbaskets
import json


class __Result:
    def __init__(self, basket_token: str, name: str, method: str) -> None:
        self.api_path = rbaskets.host
        self.api_path += f'/api/baskets/{name}/responses'
        self.api_path += f'/{method}'

        self.__headers = {'Authorization': basket_token}

        res = requests.get(self.api_path, headers=self.__headers)

        if res.status_code == 200:
            self.__body = json.loads(res.text)
        elif res.status_code == 401:
            raise requests.HTTPError('Unauthorized. Invalid or missing basket token')
        elif res.status_code == 404:
            raise requests.HTTPError('Not Found. No basket with such name')

    def __update(self, key, value) -> bool:
        res = requests.put(self.api_path, headers=self.__headers, params={key: value})

        if res.status_code == 204:
            return True
        elif res.status_code == 400:
            raise requests.HTTPError('Bad Request. Failed to parse JSON into response configuration object.')
        elif res.status_code == 401:
            raise requests.HTTPError('Unauthorized. Invalid or missing basket token')
        elif res.status_code == 404:
            raise requests.HTTPError('Not Found. No basket with such name')
        elif res.status_code == 422:
            raise requests.HTTPError('Unprocessable Entity. Response configuration is not valid.')

    @property
    def status(self) -> int:
        """The HTTP status code to reply with"""
        return self.__body['status']

    def update_status(self, status: int) -> bool:
        """:param status: The HTTP status code to reply with"""
        return self.__update('status', status)


    @property
    def headers(self) -> dict:
        """Map of HTTP headeres, key represents name, value is array of values"""
        return self.__body['headers']

    def update_headers(self, headers) -> bool:
        """:param headers: Map of HTTP headeres, key represents name, value is array of values"""
        return self.__update('headers', headers)

    @property
    def body(self) -> str:
        """Content of response body"""
        return self.__body['body']

    def update_body(self, body) -> bool:
        """:param body: Content of response body""" 
        return self.__update('body', body)

    @property
    def is_template(self):
        """If set to `true` the body is streated as [HTML template](https://pkg.go.dev/html/template) that accepts input from request parameters"""
        return self.__body['is_template']

    def update_is_template(self, is_template) -> bool:
        """:param If set to `true` the body is streated as [HTML template](https://pkg.go.dev/html/template) that accepts input from request parameters"""
        return self.__update('is_template', is_template)

class Get(__Result):
    def __init__(self, basket_token: str, name: str) -> None:
        super().__init__(basket_token, name, "GET")

class Head(__Result):
    def __init__(self, basket_token: str, name: str) -> None:
        super().__init__(basket_token, name, "HEAD")

class Post(__Result):
    def __init__(self, basket_token: str, name: str) -> None:
        super().__init__(basket_token, name, "POST")

class Put(__Result):
    def __init__(self, basket_token: str, name: str) -> None:
        super().__init__(basket_token, name, "PUT")

class Patch(__Result):
    def __init__(self, basket_token: str, name: str) -> None:
        super().__init__(basket_token, name, "PATCH")

class Delete(__Result):
    def __init__(self, basket_token: str, name: str) -> None:
        super().__init__(basket_token, name, "DELETE")

class Connect(__Result):
    def __init__(self, basket_token: str, name: str) -> None:
        super().__init__(basket_token, name, "CONNECT")

class Options(__Result):
    def __init__(self, basket_token: str, name: str) -> None:
        super().__init__(basket_token, name, "OPTIONS")

class Trace(__Result):
    def __init__(self, basket_token: str, name: str) -> None:
        super().__init__(basket_token, name, "TRACE")

class Response:
    """
    # Configure basket responses
    ## Get response settings
    Retrieves information about configured response of the basket. Service will reply with this response to any HTTP request sent to the basket with appropriate HTTP method.

    ## Update response settings
    Allows to configure HTTP response of this basket. The service will reply with configured response to any HTTP request sent to the basket with appropriate HTTP method.
    
    :param basket_token: Basket assigned secure token
    :param name: The basket name
    """
    def __init__(self, basket_token: str, name: str) -> None:
        self.__basket_token = basket_token
        self.__name = name

    @property
    def get(self) -> Get:
        """
        Get/Update response settings (GET)
        """
        return Get(self.__basket_token, self.__name)

    @property
    def head(self) -> Head:
        """
        Get/Update response settings (HEAD) 
        """
        return Head(self.__basket_token, self.__name)

    @property
    def post(self) -> Post:
        """
        Get/Update response settings (POST) 
        """
        return Post(self.__basket_token, self.__name)
    
    @property
    def put(self) -> Post:
        """
        Get/Update response settings (PUT) 
        """
        return Put(self.__basket_token, self.__name)
    
    @property
    def patch(self) -> Patch:
        """
        Get/Update response settings (PATCH) 
        """
        return Patch(self.__basket_token, self.__name)

    @property
    def delete(self) -> Delete:
        """
        Get/Update response settings (DELETE) 
        """
        return Delete(self.__basket_token, self.__name)

    @property
    def connect(self) -> Connect:
        """
        Get/Update response settings (CONNECT) 
        """
        return Connect(self.__basket_token, self.__name)

    @property
    def options(self) -> Options:
        """
        Get/Update response settings (OPTIONS) 
        """
        return Options(self.__basket_token, self.__name)
    
    @property
    def trace(self) -> Trace:
        """
        Get/Update response settings (TRACE) 
        """
        return Trace(self.__basket_token, self.__name)