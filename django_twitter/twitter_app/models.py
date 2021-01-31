from django.db import models
from requests_oauthlib import OAuth1Session
from .twitter_api_manager import TwitterAPIHandler
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from email.utils import parsedate_tz

s = 'Tue Mar 29 08:11:25 +0000 2011'


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_data = models.JSONField(blank=True,null=True)
    since_id = models.CharField(max_length=50)

class TimeLine(models.Model):
    owner = models.ForeignKey(
                    Profile,
                    on_delete=models.CASCADE,
                    related_name='timelines',
                    null=True,
                )
    post = models.JSONField()
    date_time = models.DateTimeField()
    id_str = models.CharField(max_length=50, unique=True)
    text = models.TextField(default="")

    @staticmethod
    def to_datetime(datestring):
        time_tuple = parsedate_tz(datestring.strip())
        dt = datetime(*time_tuple[:6])
        return dt - timedelta(seconds=time_tuple[-1])
    
    @classmethod
    def bulk_create(cls,owner,timelines):
        posts = []
        for post in timelines:
            if cls.objects.filter(id_str=post["id_str"]).first()==None:
                posts.append(cls(
                    owner=owner,
                    post=post,
                    date_time=cls.to_datetime(post["created_at"]),
                    id_str=post["id_str"],
                    text=post["text"]
                ))
        res = cls.objects.bulk_create(posts)
        owner.since_id = timelines[0]['id_str']
        owner.save()

class UserOAuthTokens(models.Model):
    oauth_token = models.CharField(max_length=50)
    oauth_token_secret = models.CharField(max_length=50)
    oauth_callback_confirmed = models.CharField(max_length=10)
    oauth_verifier = models.CharField(blank=True,null=True,max_length=50)
    user_oauth_token = models.CharField(blank=True,null=True,max_length=50)
    user_oauth_token_secret = models.CharField(blank=True,null=True,max_length=50)
    user_id = models.CharField(blank=True,null=True,max_length=10)
    screen_name = models.CharField(blank=True,null=True,max_length=30)
    valid = models.BooleanField(default=False)

    owner = models.ForeignKey(
                        Profile,
                        on_delete=models.CASCADE,
                        related_name='tokens',
                        null=True,
                    )
    def __str__(self):
        return self.screen_name

    @classmethod
    def get_login_url(cls):
        t = TwitterAPIHandler()
        login_url = t.get_login_url()
        cls.objects.create(**t.get_oatuh_creds())
        return login_url

    def set_user(self):
        user_data = self.get_user_data()
        user,created = User.objects.get_or_create(username=user_data["email"])
        print (">>>> model",user.id,created,user.password,user_data["id_str"])
        profile, created = Profile.objects.get_or_create(
            user=user,
        )
        profile.user_data=user_data
        profile.save()
        self.owner = profile
        self.save()

    def set_access_token(self, oauth_verifier):
        self.oauth_verifier = oauth_verifier
        access_token_data = TwitterAPIHandler.twitter_get_access_token(
                                oauth_token=self.oauth_token,
                                oauth_token_secret=self.oauth_token_secret,
                                oauth_verifier=self.oauth_verifier)
        self.user_oauth_token = access_token_data['oauth_token'] 
        self.user_oauth_token_secret = access_token_data['oauth_token_secret']
        self.user_id = access_token_data['user_id']
        self.screen_name = access_token_data['screen_name']
        self.valid = True
        self.save()
        self.set_user()
        

    def get_authorized_user_object(self):
        oauth_user = OAuth1Session(
            client_key=TwitterAPIHandler.consumer_key,
            client_secret=TwitterAPIHandler.consumer_secret,
            resource_owner_key=self.user_oauth_token,
            resource_owner_secret=self.user_oauth_token_secret)
        return oauth_user

    def get_user_data(self):
        return TwitterAPIHandler.get_user_data(self.get_authorized_user_object())
    
    def get_timeline_data(self):
        return TwitterAPIHandler.get_timeline_data(self.get_authorized_user_object())