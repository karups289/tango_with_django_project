import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')
import django

django.setup()

from rango.models import Category, Page


def populate():
	python_cat = add_cat('Python', 265, 345)

	add_page(cat = python_cat,
	         title = "Official Python Tutorial",
	         url = "http://docs.python.org/2/tutorial/",
	         views = 12)

	add_page(cat = python_cat,
	         title = "How to Think like a Computer Scientist",
	         url = "http://www.greenteapress.com/thinkpython/",
	         views = 10)

	add_page(cat = python_cat,
	         title = "Learn Python in 10 Minutes",
	         url = "http://www.korokithakis.net/tutorials/python/",
	         views = 19)

	django_cat = add_cat("Django", 12, 45)

	add_page(cat = django_cat,
	         title = "Official Django Tutorial",
	         url = "https://docs.djangoproject.com/en/1.5/intro/tutorial01/",
	         views = 20)

	add_page(cat = django_cat,
	         title = "Django Rocks",
	         url = "http://www.djangorocks.com/")

	add_page(cat = django_cat,
	         title = "How to Tango with Django",
	         url = "http://www.tangowithdjango.com/",
	         views = 56)

	frame_cat = add_cat("Other Frameworks", 34, 78)

	add_page(cat = frame_cat,
	         title = "Bottle",
	         url = "http://bottlepy.org/docs/dev/",
	         views = 0)

	add_page(cat = frame_cat,
	         title = "Flask",
	         url = "http://flask.pocoo.org",
	         views = 16)

	# Print out what we have added to the user.
	for c in Category.objects.all():
		for p in Page.objects.filter(category = c):
			print("category:" + c.name + "-Page:" + p.title)


def add_page(cat, title, url, views = 0):
	p = Page.objects.get_or_create(category = cat, title = title)[0]
	p.url = url
	p.views = views
	p.save()
	return p


def add_cat(name, view, likes):
	c = Category.objects.get_or_create(name = name)[0]
	c.view = view
	c.likes = likes
	c.save()
	return c


# Start execution here!
if __name__ == '__main__':
	print("Starting Rango population script...")
	populate()
