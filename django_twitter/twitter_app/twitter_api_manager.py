from requests_oauthlib import OAuth1Session
import os

class TwitterAPIHandler():

    request_token_url = 'https://api.twitter.com/oauth/request_token'
    access_tocken_url = 'https://api.twitter.com/oauth/access_token'

    login_url = "https://api.twitter.com/oauth/authenticate?oauth_token={oauth_token}"
    url_user = 'https://api.twitter.com/1.1/account/verify_credentials.json'

    def __init__(self, oauth_creds={}, call_back_creds={}, access_token_data={}):
        self.__oauth_creds = oauth_creds
        self.__call_back_creds = call_back_creds
        self.__access_token_data = access_token_data

    @staticmethod
    def __get_url_data_parcer(string):
        d  = {}
        for fields in string.split("&"):
            key, val = fields.split("=")
            d[key] = val
        return d

    @staticmethod
    def __get_resource_token():
        request_token = OAuth1Session(
            client_key=TwitterAPIHandler.__consumer_key,
            client_secret=TwitterAPIHandler.__consumer_secret)

        data = request_token.get(TwitterAPIHandler.request_token_url)
        return TwitterAPIHandler.__get_url_data_parcer(data.text)
    
    @staticmethod
    def __twitter_get_access_token(oauth_verifier, oauth_token, oauth_token_secret, **kwargs):
        oauth_token = OAuth1Session(client_key=TwitterAPIHandler.__consumer_key,
                                    client_secret=TwitterAPIHandler.__consumer_secret,
                                    resource_owner_key=oauth_token,
                                    resource_owner_secret=oauth_token_secret)
        access_token_data = oauth_token.post(
            TwitterAPIHandler.access_tocken_url,
            data={"oauth_verifier": oauth_verifier})
        return TwitterAPIHandler.__get_url_data_parcer(access_token_data.text)

    @staticmethod
    def __twitter_get_user_data(access_token_data):
        oauth_user = OAuth1Session(
            client_key=TwitterAPIHandler.__consumer_key,
            client_secret=TwitterAPIHandler.__consumer_secret,
            resource_owner_key=access_token_data['oauth_token'],
            resource_owner_secret=access_token_data['oauth_token_secret'])
        user_data = oauth_user.get(
            TwitterAPIHandler.url_user,
            params={"include_email": 'true'})
        
        return user_data.json()

    def get_login_url(self):
        self.__oauth_creds = TwitterAPIHandler.__get_resource_token()
        return TwitterAPIHandler.login_url.format(**self.__oauth_creds)

    def set_call_back_creds(self, call_back_get_url):
        self.__call_back_creds = TwitterAPIHandler.__get_url_data_parcer(call_back_get_url)

    def get_access_tocken(self):
        self.__access_token_data = TwitterAPIHandler.__twitter_get_access_token(
            oauth_verifier=self.__call_back_creds['oauth_verifier'],
            **self.__oauth_creds,
        )

    def get_user_data(self):
        return TwitterAPIHandler.__twitter_get_user_data(self.__access_token_data)   
