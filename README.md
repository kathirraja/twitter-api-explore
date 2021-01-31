### Twitter sigin in core
## How to use it.
1)Get consumer_key, and consumer_secret from twitter developer portal

2)Export it to environment variable
```bash
$export consumer_key="your consumer key"
$export consumer_secret="your consumer secret>"
```
## Local Test server
 ```bash
 $cd /path/to/django_twitter 
 $python manage.py makemigrations
 $python manage.py migrate
 
 $python manage.py crontab add
 
 $python manage.py runserver 127.0.0.1:8000
 ```

## API Docs 
1) go to http://localhost:8000

2) click on LoginwithTwitter

3) login to twitter account

4) profile api (login required)
    http://localhost/get_profile

5) timeline api (login required)
    http://localhost:8000/get_timeline

6) timline chronological from database
    http://localhost:8000/get_timeline_from_db

7) search on timeline
    http://localhost:8000/get_timeline_from_db?search=key_word
