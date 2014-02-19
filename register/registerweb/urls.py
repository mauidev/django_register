'''
Created on Aug 29, 2013

@author: tbowker
'''
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from registerweb import views
from registerweb import pages

urlpatterns = patterns('',
    url(r'^demo/login/$', pages.LoginPage.as_view()),
    url(r'^demo/landing/$', pages.LandingPage.as_view()),
    url(r'^demo/register/$', pages.RegisterPage.as_view()),
    url(r'^demo/test/$', pages.TestPage.as_view()),
    
    url(r'^demo/api/v1/login', views.LoginApi.as_view()),
    url(r'^demo/api/v1/users/(?P<pk>[\w,-]+)', views.UserResource.as_view()),
    url(r'^demo/api/v1/users', views.UserResource.as_view())
    
)

urlpatterns = format_suffix_patterns(urlpatterns)