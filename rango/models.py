from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length = 128, unique = True)
	view = models.IntegerField(default = 0)
	likes = models.IntegerField(default = 0)
	slug = models.SlugField(default ='')

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		# uncomment if you dont want the slug to change everytime the name
		# changes
		# if self.id is none:
		# self.slug = slugify(self.name)
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)


class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length = 128)
	url = models.URLField()
	views = models.IntegerField(default = 0)

	def __unicode__(self):
		return self.title

class UserProfile(models.Model):
	# This line is required. Links UserProfiles to a user model instance
	user = models.OneToOneField(User)

	# The additional attributes we wish to include
	website = models.URLField(blank = True)
	picture = models.ImageField(upload_to = 'profile_images', blank = True)

	# override the __uni_code__() method to return our something meaningful
	def __uni_code__(self):
		return self.user.username