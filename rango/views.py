from django.shortcuts import render

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime

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

    category_list = Category.objects.order_by('-likes')[:10]
    page_list = Page.objects.order_by('-views')[:10]
    context_dict = {'categories': category_list , 'page_list': page_list}
    # Get the number of visits to the site
    # We use the COKKIES.get() function
    visits = request.session.get('visits')
    if not visits:
        visits = 1

    reset_last_visit_time = False
    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - last_visit_time).seconds > 5:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True
        
    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits 
    context_dict['visits'] = visits
    response = render(request, 'rango/index.html',context_dict)
    # Render the response and send it back
    return response



def about(request):
    # return HttpResponse('Rango says here is the about page.<a
    # href="/rango/">Index</a>')
    
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 1
        request.session['visits'] = 1

    context_dict = {'boldmessage': "Please contact system admin about", 'visits': count}
    return render(request, 'rango/about.html', context_dict)



def category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug = category_name_slug)
        context_dict['category_name'] = category.name
        context_dict['category_name_slug'] = category_name_slug

        pages = Page.objects.filter(category = category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)


@login_required

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

@login_required

def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    print(cat)
    # A HTTP POST?
    if request.method == 'POST':
        form = PageForm(request.POST)
        # if valid form
        if form.is_valid():
            page = form.save(commit = False)
            page.category = cat
            page.views = 0
            page.save()

            # save the new Page to database

            # user will then be redirected to home page
            return category(request, category_name_slug)
        else:
            # the supplied form contained errors - just print them to terminal
            print(form.errors)
    else:
        # if the request was not a POST, display the form to enter details
        form = PageForm()
    context_dic = {'form': form, 'category': cat}
    return render(request, 'rango/add_page.html', context_dic)


def register(request):
    # A boolean value for telling the template whether the registration was
    # successful.
    # Set to False initially. Code changes value to True when registration
    # succeeds.

    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set
            # commit=False.
            # This delays saving the model until we're ready to avoid
            # integrity problems.
            profile = profile_form.save(commit = False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the
            # UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was
            # successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print
            user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'rango/register.html',
                  {
                      'user_form': user_form, 'profile_form': profile_form,
                      'registered': registered
                      })


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed to request.POST[
        # '<variable>'],
        # because the request.POST.get('<variable>') returns None, if the
        # value does not exist,
        # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username = username, password = password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value),
        # no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print
            "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', {})

@login_required

def restricted(request):
    return render(request, 'rango/restricted.html', {})

@login_required

def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')



def api(request):


    server_addr_api = "http://philipsthuat.specom.io/api/v2_soap?wsdl"
    service_action = "GdAuctionsBiddingWSAPI/GetAuctionList"

    body = """
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope
    /" xmlns:ns="http://www.example.com/services/wsdl/2.0">
    <soapenv:Header/>
    <soapenv:Body>
    <ns:serviceListRequest>
    <ns:userInfo>
    </ns:userInfo>
    </ns:serviceListRequest>
    </soapenv:Body>
    </soapenv:Envelope>"""

    request = httplib.HTTPConnection(server_addr)
    request.putrequest("POST", service_action)
    request.putheader("Accept",
                      "application/soap+xml, application/dime, "
                      "multipart/related, text/*")
    request.putheader("Content-Type", "text/xml; charset=utf-8")
    request.putheader("Cache-Control", "no-cache")
    request.putheader("Pragma", "no-cache")
    request.putheader("SOAPAction",
                      server_addr_api)
    request.putheader("Content-Length", "length")
    request.putheader("apiKey", "mahendrad")
    request.putheader("pageNumber", "1")
    request.putheader("rowsPerPage", "1")
    request.putheader("beginsWithKeyword", "word")
    request.endheaders()
    request.send(body)
    response = request.getresponse().read()

    print
    response