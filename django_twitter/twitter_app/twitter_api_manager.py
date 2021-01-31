from requests_oauthlib import OAuth1Session
import os

class TwitterAPIHandler():

    consumer_key = "ZiwhxcmRaGO4Zm144TTIYpbDM" #os.environ.get('consumer_key') 
    consumer_secret = "VJvchdF1kgyyrxaWxQWbPFsaBNDyzQVucClfSKROnR1KoVmvsk" #os.environ.get('consumer_secret')

    request_token_url = 'https://api.twitter.com/oauth/request_token'
    access_tocken_url = 'https://api.twitter.com/oauth/access_token'

    login_url = "https://api.twitter.com/oauth/authenticate?oauth_token={oauth_token}"
    url_user = 'https://api.twitter.com/1.1/account/verify_credentials.json'

    user_timeline_url =  "https://api.twitter.com/1.1/statuses/user_timeline.json"

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
            client_key=TwitterAPIHandler.consumer_key,
            client_secret=TwitterAPIHandler.consumer_secret)

        data = request_token.get(TwitterAPIHandler.request_token_url)
        return TwitterAPIHandler.__get_url_data_parcer(data.text)
    
    @staticmethod
    def twitter_get_access_token(oauth_verifier, oauth_token, oauth_token_secret, **kwargs):
        oauth_token = OAuth1Session(client_key=TwitterAPIHandler.consumer_key,
                                    client_secret=TwitterAPIHandler.consumer_secret,
                                    resource_owner_key=oauth_token,
                                    resource_owner_secret=oauth_token_secret)
        access_token_data = oauth_token.post(
            TwitterAPIHandler.access_tocken_url,
            data={"oauth_verifier": oauth_verifier})
        return TwitterAPIHandler.__get_url_data_parcer(access_token_data.text)

    @staticmethod
    def __get_authorized_user_object(access_token_data):

        oauth_user = OAuth1Session(
            client_key=TwitterAPIHandler.consumer_key,
            client_secret=TwitterAPIHandler.consumer_secret,
            resource_owner_key=access_token_data['oauth_token'],
            resource_owner_secret=access_token_data['oauth_token_secret'])
        
        return oauth_user

    @staticmethod
    def __twitter_get_user_data(oauth_user):
        user_data = oauth_user.get(
            TwitterAPIHandler.url_user,
            params={"include_email": 'true'})
        return user_data.json()

    @staticmethod
    def json_to_get(params):
        s = []
        for k,v in params.items():
            s.append(k+"="+v)
        return "".join(s)


    @staticmethod
    def __twitter_get_user_timeline(oauth_user,**kwargs):
        get_params = TwitterAPIHandler.json_to_get(kwargs)
        user_data = oauth_user.get(
            TwitterAPIHandler.user_timeline_url+"?"+get_params)
        return user_data.json()

    def get_oatuh_creds(self):
        return self.__oauth_creds
    
    def get_call_back_creds(self):
        return self.__call_back_creds
    
    def get_user_access_token(self):
        return self.__access_token_data

    def get_login_url(self):
        self.__oauth_creds = TwitterAPIHandler.__get_resource_token()
        return TwitterAPIHandler.login_url.format(**self.__oauth_creds)

    def set_call_back_creds(self, call_back_get_url):
        self.__call_back_creds = TwitterAPIHandler.__get_url_data_parcer(call_back_get_url)

    def get_access_tocken(self):
        self.__access_token_data = TwitterAPIHandler.twitter_get_access_token(
            oauth_verifier=self.__call_back_creds['oauth_verifier'],
            **self.__oauth_creds,
        )

    @staticmethod
    def get_user_data(oauth_user):
        return TwitterAPIHandler.__twitter_get_user_data(oauth_user)   

    @staticmethod
    def get_timeline_data(oauth_user):
        return TwitterAPIHandler.__twitter_get_user_timeline(oauth_user)