'''
Created on Oct 2, 2013

@author: tbowker
'''

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render_to_response

from registerweb.models import User


class LoginPage(APIView):
    
    renderer_classes = (TemplateHTMLRenderer,)
    
    def get(self, request):
        """ Return a page for logging in. """
        return Response(template_name='login.html')
    
  
class RegisterPage(APIView):
    
    renderer_classes = (TemplateHTMLRenderer,)
    
    def get(self, request):
        """ Return a page for user registration. """
        user = User()
        return render_to_response('register.html',{'user':user,'mode':'add'})
                
    
        
class LandingPage(APIView):
    
    renderer_classes = (TemplateHTMLRenderer,)
    
    def get(self, request):
        """ Return a page for logging in. """
        return Response(template_name='landing.html')
    
    
class TestPage(APIView):
    
    renderer_classes = (TemplateHTMLRenderer,)
    
    def get(self, request):
        return Response(template_name='test.html')                    