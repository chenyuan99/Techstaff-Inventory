from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from hello.forms import NewUserForm,  AddEventForm, AddGuestForm
from hello.models import Greeting, Event, Guest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "main/about.html")

# def homepage(request):
#     return render(request = request,
#                   template_name='main/home.html',
#                   context = {"tutorials":Tutorial.objects.all})

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, "db.html", {"greetings": greetings})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})    

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("index")

        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = UserCreationForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

def allbuilding(request):
    return render(request, "building/all-building.html")

def newmanlibrary(request):
    return render(request, "building/newman-library.html")

def togressonhall(request):
    return render(request, "building/togresson-hall.html")

def mcbrydehall(request):
    return render(request, "building/mcbryde-hall.html")

def faq(request):
    return render(request, "main/faq.html")

def privacy(request):
    return render(request, "main/privacy-policy.html")

def event(request):
    username = request.user.get_username()
    # print(username)
    if request.method == 'POST':
        form = AddEventForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            Event.objects.create(address=address)
            return render(request, "check-in.html", {"user": username, "form": form, "success": "Clock In Successfully!"})
    else:
        form = AddEventForm()

    return render(request, "check-in.html", {"user": username, "form": form})


def add_guest(request):
    username = request.session.get('user', '')
    if request.method == 'POST':
        form = AddGuestForm(request.POST)

        if form.is_valid():
            event = form.cleaned_data['event']
            realname = form.cleaned_data['realname']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            sign = form.cleaned_data['sign']
            # if sign is True:
            #     sign = 1
            # else:
            #     sign = 0

            Guest.objects.create(event=event, realname=realname,
                                 phone=phone, email=email, sign=sign)
            return render(request, "add-guest.html", {"user": username, "form": form, "success": "Add Guest Successfully"})

    else:
        form = AddGuestForm()

    return render(request, "add-guest.html", {"user": username, "form": form})

def check_out(request):
    return render(request, "check-out.html")

def account(request):
    query_results = Event.objects.all()
    return render(request, "main/account.html",{'query_results':query_results})
    # return render(request, "main/account.html")