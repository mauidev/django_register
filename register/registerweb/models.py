from django.db import models


class User(models.Model):
    """ 
    Represents a registered user in the database.
    """
    id = models.CharField(max_length=40,primary_key=True)
    login_id  =  models.CharField(max_length=50)
    first_name = models.CharField(max_length=100, blank=True, default='')
    last_name  = models.CharField(max_length=100, blank=True, default='')
    email = models.CharField(max_length=40, blank=True, default='')
    password = models.CharField(max_length=100)
    salt = models.CharField(max_length=100)
    active = models.BooleanField()
    modified_time = models.DateTimeField()
    created_time  = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        pass