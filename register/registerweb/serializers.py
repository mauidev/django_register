'''
Created on Sep 30, 2013

@author: tbowker
'''


from rest_framework import serializers
from registerweb import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('login_id', 'first_name', 'last_name', 'email', 'active', 'created_time', 'modified_time')
