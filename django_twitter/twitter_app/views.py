from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import UserOAuthTokens, User, TimeLine
from django.contrib.auth import login

# Create your views here.

def home(request):
    return render(request,'home.html',{'twitter_login_url':UserOAuthTokens.get_login_url()})

def callback(request):
    oauth_token = UserOAuthTokens.objects.get(oauth_token=request.GET['oauth_token'])
    oauth_token.set_access_token(request.GET['oauth_verifier'])
    timelines = oauth_token.get_timeline_data()
    TimeLine.bulk_create(oauth_token.owner, timelines)
    user = User.objects.get(username=oauth_token.owner.user_data["email"])
    login(request,user)
    if user is not None:
        return JsonResponse({
            "message":"success",
            "oauth_token_id":oauth_token.id,
            "user_profile_data":oauth_token.get_user_data()
        })

@login_required
def get_profile(request):
    print(request.user)
    return JsonResponse(request.user.profile.tokens.last().get_user_data())

@login_required
def get_timeline(request):
    return JsonResponse({"timeline":request.user.profile.tokens.last().get_timeline_data()})

@login_required
def get_timeline_from_db(request):
    print (request.user)
    filter_options = {
        'text__icontains':request.GET.get('search',"")
    }
    posts = [
        timeline.post for timeline in
        request.user.profile.timelines.filter(**filter_options).order_by('date_time')
    ]
    return JsonResponse({"timeline":posts})


def update_timeline_job(request):
    for user in User.objects.all():
        timelines = user.profile.tokens.last().get_timeline_data({"since_id":user.profile.since_id})
        if len(timelines)>0:
            TimeLine.bulk_create(user.profile, timelines)