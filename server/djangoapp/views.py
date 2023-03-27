from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.shortcuts import render

def my_view(request):
    context = {
        'title': 'My Title',
        'content': 'My Content',
    }
    return render(request, 'myapp/mytemplate.html', context)

from django.shortcuts import render

def my_view(request):
    return render(request, 'myapp/mytemplate.html')

from django.shortcuts import render

def about(request):
    return render(request, 'about.html')


from django.shortcuts import render

def contact(request):
    return render(request, 'contact.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
    else:
        return render(request, 'login.html')

from django.contrib.auth import logout
from django.shortcuts import redirect


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def logout_view(request):
    logout(request)
    return redirect('home')


# Create a `contact` view to return a static contact page
#def contact(request):

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...


from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        if user is not None:
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'signup.html')

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'signup.html', {'form': form})


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    context['dealerships'] = get_dealers_from_cf()
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealerships(request):
    if request.method == "GET":
        url = "your-cloud-function-domain/dealerships/dealer-get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
from django.http import HttpResponse
from django.template import loader
from .restapis import get_dealer_reviews_from_cf

def get_dealer_details(request, dealer_id):
        context = {}
    context['reviews'] = get_dealer_reviews_from_cf(dealer_id)
    reviews = get_dealer_reviews_from_cf(dealer_id)
    context = {'reviews': reviews}
    template = loader.get_template('dealer_reviews.html')
    return HttpResponse(template.render(context, request))

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .restapis import post_request

@login_required
def add_review(request, dealer_id):
    if request.method == 'POST':
        review = {
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'name': request.user.username,
            'dealership': dealer_id,
            'review': request.POST.get('review'),
            'purchase': request.POST.get('purchase')
        }
        url = f"https://your-cloud-function-url/reviews"
        post_request(url, json_payload=review)
        return HttpResponse("Review added successfully.")
    else:
        return HttpResponse("Invalid request.")
