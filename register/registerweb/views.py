# Create your views here.

import datetime
import uuid
import hashlib

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from registerweb.models import User
from registerweb.serializers import UserSerializer

from rest_framework import status

import django.forms as forms


    

class UserForm(forms.Form):
    login_id = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    
          
        
        
class UserResource(APIView):    
    
    renderer_classes = (JSONRenderer,)
       
    def get(self, request, pk):
        """ 
        Return a user using the uuid. 
        """
        try:
            user = User.objects.get(id__exact = pk)
            serializer = UserSerializer(user)
            return Response({'data':serializer.data},status=status.HTTP_200_OK)
        except User.DoesNotExist:
            msg = {'status' : 'not found'}
            return Response(msg,status=status.HTTP_404_NOT_FOUND)      
                
    
        
    def post(self, request, format=None):
        """ 
        Add a user resource.
        """
        user_form = UserForm(request.DATA)
        
        if not user_form.is_valid():
            msg = {'status': 'error','errors':user_form.errors}
            return Response(msg,status=status.HTTP_400_BAD_REQUEST)
          
        if self._isLoginIdExists(request):
            msg = {'status' : 'duplicate'}
            print "record exists"
            return Response(msg,status=status.HTTP_400_BAD_REQUEST)  
        
        password = user_form.cleaned_data['password']
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(password + salt).hexdigest()

        user = User()
        user.id = str(uuid.uuid1())
        user.login_id = user_form.cleaned_data['login_id']
        user.first_name = user_form.cleaned_data['first_name']
        user.last_name = user_form.cleaned_data['last_name']
        user.email = user_form.cleaned_data['email']
        user.password = hashed_password
        user.salt = salt
        user.active = True
        user.created_time = datetime.datetime.now()
        user.modified_time = datetime.datetime.now()
        user.save()
         
        # return a 201 and a location link in the header
        return Response({'id': user.id},status=status.HTTP_201_CREATED)
    
    
    def put(self, request, pk, format=None):
        """ 
        Update a user resource 
        """
        user_form = UserForm(request.DATA)
        if not user_form.is_valid():
            msg = {'status': 'error','errors':user_form.errors}
            return Response(msg,status=status.HTTP_400_BAD_REQUEST)
        
        user = None
        try:
            user = User.objects.get(id__exact = pk)
            
        except User.DoesNotExist:
            msg = {'status' : 'not found'}
            return Response(msg,status=status.HTTP_404_NOT_FOUND)  
        
        user.first_name = user_form.cleaned_data['first_name']
        user.last_name = user_form.cleaned_data['last_name']
        user.email = user_form.cleaned_data['email']
        user.save()
        return Response({'id': user.id},status=status.HTTP_200_OK)
    
    
    def delete(self, request, pk, format=None):
        user = None
        try:
            user = User.objects.get(id__exact = pk)
        except User.DoesNotExist:
            msg = {'status' : 'not found'}
            return Response(msg,status=status.HTTP_404_NOT_FOUND)  
        user.delete()
        return Response(status=status.HTTP_200_OK)
               
    
    def _isLoginIdExists(self,request):
        try:
            login_id = request.DATA['login_id']
            if User.objects.get(login_id__exact = login_id):
                return True
        except User.DoesNotExist:
            return False  
        
    
    
    
class LoginApi(APIView):
    """ 
    Handle logging into the application. If successful, redirect
    to the next page.
    """
    
    renderer_classes = (JSONRenderer,)
    
    def post(self, request):
        """
          Authenticate a user. Compute a password hash and compare against
          the hash in the database.
        """
        user = None
        try:
            login_id = request.DATA['login_id']
            user = User.objects.get(login_id__exact = login_id)
        except User.DoesNotExist:
            return self._invalid_user()
       
        salt = user.salt
        password = request.DATA['password'] 
        hashed_password = hashlib.sha512(password + salt).hexdigest()
        if hashed_password != user.password:
            return self._invalid_user()
        
        data = {}
        data['redirect'] = 'http://localhost:8000/demo/landing'
        return Response(data)
    
    def _invalid_user(self):
        data = {}
        data['error'] = "Invalid user or password."
        data['fieldId'] = "generalError"
        return Response(data)
                 
        