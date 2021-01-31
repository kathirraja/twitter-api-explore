from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('callback', views.callback, name="twitter_callback"),
    path('get_profile', views.get_profile, name="get_profile"),
    path('get_timeline', views.get_timeline, name="get_timeline"),
    path('get_timeline_from_db', views.get_timeline_from_db, name="get_timeline_from_db"),
    path('update_timeline_job', views.update_timeline_job, name="update_timeline_job"),
]