import requests
import json

import rbaskets

class Version:
    """Get service version."""
    def __init__(self) -> None:
        API_PATH = '/api/version'

        res = requests.get(rbaskets.host + API_PATH)
        
        if res.status_code == 200:
            self.body = json.loads(res.text)
        else:
            res.raise_for_status()

    @property
    def name(self) -> str:
        """Service name"""
        return self.body['name']

    @property
    def version(self) -> str:
        """Service version"""
        return self.body['version']

    @property
    def commit(self) -> str:
        """Git commit this service is build from"""
        return self.body['commit']

    @property
    def commit_short(self) -> str:
        """Short form of git commit this service is build from"""
        return self.body['commit_short']
    
    @property
    def source_code(self) -> str:
        """URL of the source code repository"""
        return self.body['source_code']