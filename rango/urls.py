from django.conf.urls import url
from django.contrib import admin

from rango import views

admin.autodiscover()
urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^about/$', views.about, name = 'about'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name =
	'category')]
