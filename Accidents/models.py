from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Accident(models.Model):
	location = models.CharField(max_length = 100)
	injuries = models.IntegerField(default=0)
	deaths = models.IntegerField(default=0)
	vehicle = models.CharField(max_length = 100, null = True)
	lon = models.CharField(max_length = 100, null = True)
	lat = models.CharField(max_length = 100, null = True)
	date = models.DateTimeField(blank = True)

	def __unicode__(self):
		return self.location+":\t"+str(self.lat)+","+str(self.lon)