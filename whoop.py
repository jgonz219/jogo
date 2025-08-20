from google_secrets import SecretManager
import urllib.parse
import requests
import json
import pandas as pd

class Whoop:
    def __init__(self):
        # Initial Token was created with oauth2 in postman following Whoop docs
        self.base_url = 'https://api.prod.whoop.com/developer/v1'
        self.secrets_manager = SecretManager()
        self.client_id = self.secrets_manager.access('whoop_client_id')
        self.client_secret = self.secrets_manager.access('whoop_client_secret')
        self.refresh_token = self.secrets_manager.access('whoop_refresh_token')
        self.access_token = self.secrets_manager.access('whoop_access_token')
        self.__refresh_token()
        self.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
