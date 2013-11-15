'''
Created on Oct 2, 2013

@author: tbowker
'''

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer




class LoginPage(APIView):
    
    renderer_classes = (TemplateHTMLRenderer,)
    
    def get(self, request):
        """ Return a page for logging in. """
        return Response(template_name='login.html')
    
  
class RegisterPage(APIView):
    
    renderer_classes = (TemplateHTMLRenderer,)
    
    def get(self, request):
        """ Return a page for user registration. """
        return Response(template_name='register.html')        
    
        
class LandingPage(APIView):
    
    renderer_classes = (TemplateHTMLRenderer,)
    
    def get(self, request):
        """ Return a page for logging in. """
        return Response(template_name='landing.html')        