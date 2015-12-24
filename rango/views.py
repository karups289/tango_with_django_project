from django.shortcuts import render

from rango.models import Category, Page
from rango.forms import CategoryForm


# Create your views here.

def index(request):
	# return HttpResponse("Rango says: Hello world! <br/> <a
	# href='/rango/about'>About</a>")
	# context_dict = {'boldmessage': "Please contact system administrator"}
	# return render(request, 'rango/index.html', context_dict)
	# query the database for a list of all categories currently stored
	# Order the categories by no. of likes in descending order.
	# Retrieve the top 5 only - or all if less than 5
	# place the list in our context_dict dictionary which will be passed to
	# the template engine
	category_list = Category.objects.order_by('-likes')[:5]


	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list , 'page_list': page_list}

	# Render teh response and send it back
	return render(request, 'rango/index.html', context_dict)


def about(request):
	# return HttpResponse('Rango says here is the about page.<a
	# href="/rango/">Index</a>')
	context_dict = {'boldmessage': "Please contact system admin about"}
	return render(request, 'rango/about.html', context_dict)


def category(request, category_name_slug):
	context_dict = {}
	try:
		category = Category.objects.get(slug = category_name_slug)
		context_dict['category_name'] = category.name

		pages = Page.objects.filter(category = category)

		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		pass
	return render(request, 'rango/category.html', context_dict)


def add_category(request):
	# A HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		#if valid form
		if form.is_valid():
			# save the new category to database
			form.save(commit = True)
			# user will then be redirected to home page
			return index(request)
		else:
			# the supplied form contained errors - just print them to terminal
			print(form.errors)
	else:
		# if the request was not a POST, display the form to enter details
		form = CategoryForm()
	return render(request, 'rango/add_category.html', {'form': form})