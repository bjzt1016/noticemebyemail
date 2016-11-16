#coding:utf-8
from django.db import models

# Create your models here.
class JobBoLe(models.Model):
	latest_news = models.CharField(max_length=100)

	def __unicode__(self):
		return self.latest_news