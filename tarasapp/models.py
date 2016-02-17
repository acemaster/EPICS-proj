from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    """
    Description: User profile of the person
    """
    user=models.OneToOneField(User,null=True,blank=True)
    mobile=models.CharField(max_length=180)
    status=models.IntegerField(default=0)
    otp=models.CharField(max_length=180,null=True)
    created_at=models.DateTimeField(auto_now=True)
    def __unicode__(self):
    	return self.user.username




    


    
