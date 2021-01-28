### Twitter sigin in core
## How to use it.
1)Get consumer_key, and consumer_secret from twitter developer portal

2)Export it to environment variable
```bash
$export consumer_key="your consumer key"
$export consumer_secret="your consumer secret>"
```
3)use this TwitterAPIHandler class

```python
twitter_client = TwitterAPIHandler()
login url = twitter_client.get_login_url()
```

use this **login url** for athourize application from browser

login_url will look like this

>https://api.twitter.com/oauth/authenticate?oauth_token=cso35345345kmfsdjvJs

once you loggedin successfully it will redirect to callback url

call_back url will look like this

>http://localhost/calback?oauth_token=cls2zAAAAAABMKic234d0UVvJs&oauth_verifier=NnZGPOosh9ba7vZr4uH32423ddVb0G 

use this call back url to set call back creds

```python
cbu = "oauth_token=cls2zAAAAAABMKic234d0UVvJs&oauth_verifier=NnZGPOosh9ba7vZr4uH32423ddVb0G"
```
string from **call_back_url** for verification

4)set call back creds

```python
twitter_client.set_call_back_creds(cbu)
```
5)Get access token to access user data

```python
twitter_client.get_access_tocken()
```
  

6)Get user data

```python
user_data = twitter_client.get_user_data()
```

the response will be like this

```python
{'id': 1338818395706277890,
'id_str': '1338818395706277890',
'name': 'Abi ',
'screen_name': 'AbiCaleb',
'location': '',
'description': '',
'url': None,
'entities': {'description': {'urls': []}},
'protected': False,
'followers_count': 1,
'friends_count': 16,
'listed_count': 0,
'created_at': 'Tue Dec 15 12:09:22 +0000 2020',
'favourites_count': 0,
'utc_offset': None,
'time_zone': None,
'geo_enabled': False,
'verified': False,
'statuses_count': 0,
'lang': None,
'contributors_enabled': False,
'is_translator': False,
'is_translation_enabled': False,
'profile_background_color': 'F5F8FA',
'profile_background_image_url': None,
'profile_background_image_url_https': None,
'profile_background_tile': False,
'profile_image_url': 'http://pbs.twimg.com/profile_images/1354470833322815493/w-h5KOvb_normal.jpg',
'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1354470833322815493/w-h5KOvb_normal.jpg',
'profile_link_color': '1DA1F2',
'profile_sidebar_border_color': 'C0DEED',
'profile_sidebar_fill_color': 'DDEEF6',
'profile_text_color': '333333',
'profile_use_background_image': True,
'has_extended_profile': True,
'default_profile': True,
'default_profile_image': False,
'following': False,
'follow_request_sent': False,
'notifications': False,
'translator_type': 'none',
'suspended': False,
'needs_phone_verification': False,
'email': 'abi@gmail.com'}
```

This module can be integrated with any web framework like flask, django
Api needs to be design for this application to expose data outside.
