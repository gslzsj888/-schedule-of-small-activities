from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image


# Create your models here.

class MyUser(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	email = models.CharField(max_length=30)

class Activity(models.Model):
	builder = models.ForeignKey(MyUser)
	title = models.CharField(max_length=50)
	pub_date = models.DateField(max_length=20)
	time_start = models.CharField(max_length=20)
	time_end = models.CharField(max_length=20)
	release = models.DateTimeField(auto_now_add=True)
	introduce = models.TextField()
	img= models.ImageField(upload_to='media/activitypic/%Y/%m/%d', blank=True,null=True)
	cancered = models.IntegerField(default=0)
	popular = models.IntegerField(default=0)

class Agenda(models.Model):
	user = models.ForeignKey(MyUser)
	activity = models.ForeignKey(Activity)
	checked = models.IntegerField(default=0)
	overdue = models.IntegerField(default=0)

class Stage(models.Model):
	subtitle = models.CharField(max_length=50)
	brief = models.TextField()
	tim = models.CharField(max_length=20)
	activity = models.ForeignKey(Activity,related_name="stage")
