from django.db import models

# Create your models here.

class person(models.Model):
	name = models.CharField(max_length=100)
	image = models.CharField(max_length=100)
	lives_in = models.CharField(max_length=100)
	contact = models.CharField(max_length=100)
	age = models.CharField(max_length=100)
	place_of_meeting = models.CharField(max_length=100)
	relation = models.CharField(max_length=100)
	notes = models.CharField(max_length=100)

	def __str__(self):
		return self.name