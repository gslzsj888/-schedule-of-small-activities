from django.db import models
from django.contrib.auth.models 
import Userimport django.utils.timezone as timezone
# Create your models here.

class MyUser(models.Model):
	user = models.OneToOneField(User)
	email = models.CharField(max_length=30)

class Agenda(models.Model):
	user = models.ForeignKey(MyUser)
	activity = models.ForeignKey(Activity)
	checked = models.IntegerField(default=0)
	overdue = models.IntegerField(default=0)

class Activity(models.Model):
	builder = models.ForeignKey(MyUser)
	title = models.CharField(max_length=50)
	date = models.DateField(max_length=20)
	time_start = models.CharField(max_length=20)
	time_end = models.CharField(max_length=20)
	release = models.DateField(auto_now=True)
	introduce = models.TextField()
	img = models.ImageField(upload_to="media/activity_pic/%Y-%m-%d")
	cancered = models.IntegerField(default=0)
	stage_num = models.IntegerField(default=0)
	popular = models.IntegerField(default=0)

class Stage(models.Model):
	sub_title = models.CharField(max_length=50)
	brief = models.TextField()
	time = models.CharField(max_length=20)
	number = models.IntegerField()
	activity = models.ForeignKey(Activity,related_name="stage")
