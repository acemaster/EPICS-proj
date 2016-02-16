from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    """
    Description: User profile of the person
    """
    user=models.OneToOneField(User)
    mobile=models.CharField(max_length=180)
    status=models.IntegerField()
    created_at=models.DateTimeField(auto_now=True)
    def __unicode__(self):
    	return self.user.username


class SmsCode(models.Model):
    """
    Description: SMS codes
    """
    user=models.OneToOneField(User)
    code=models.CharField(max_length=200)
    status=models.IntegerField()
    created_at=models.DateTimeField(auto_now=True)
    def __unicode__(self):
    	return self.user.username



    


    
