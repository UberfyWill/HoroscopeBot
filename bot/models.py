from django.db import models
from django.utils import timezone

# Create your models here.

class Horoscope(models.Model):
    horoscope_date = models.CharField(max_length=200)
    sign = models.CharField(max_length=100)
    horoscope = models.TextField()
    overview = models.TextField()
    created_date = models.CharField(max_length=100)

    def __unicode__(self):
        return self.sign

class UserData(models.Model):
	user_id = models.CharField(max_length=100)
	mid = models.CharField(max_length=200)
	msg_txt = models.CharField(max_length=10000)
	timestamp = models.CharField(max_length=100)
	page_id = models.CharField(max_length=100)
	recent_question = models.CharField(max_length=500)

	def __unicode__(self):
		return self.user_id

class Subscribe(models.Model):
	user_id = models.CharField(max_length=100)
	frequency = models.CharField(max_length=100)
	subscribed = models.BooleanField(default=False)