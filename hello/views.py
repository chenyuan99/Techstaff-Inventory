from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from hello.forms import *
from hello.models import *
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


def display_laptops(request):
	items = Laptop.objects.all()
	context = {
		'items': items,
		'header': 'Laptops'
	}

	return render(request, 'index.html', context)


def display_desktops(request):
	items = Desktop.objects.all()
	context = {
		'items': items,
		'header': 'Desktops'
	}

	return render(request, 'index.html', context)


def display_mobiles(request):
	items = Mobile.objects.all()
	context = {
		'items': items,
		'header': 'Mobiles'
	}

	return render(request, 'index.html', context)


def add_device(request, cls):
	if request.method == 'POST':
		form = cls(request.POST)

		if form.is_valid():
			form.save()
			return redirect('index')

	else:
		form = cls()
		return render(request, 'add_new.html', {'form': form})


def add_laptop(request):
	return add_device(request, LaptopForm)

def add_desktop(request):
	return add_device(request, DesktopForm)

def add_mobile(request):
	return add_device(request, MobileForm)



def edit_device(request, pk, model, cls):
	item = get_object_or_404(model, pk=pk)

	if request.method == 'POST':
		form = cls(request.POST, instance=item)
		if form.is_valid():
			form.save()
			return redirect('index')

	else:
		form = cls(instance=item)

		return render(request, 'edit_item.html', {'form': form})


def edit_laptop(request, pk):
	return edit_device(request, pk, Laptop, LaptopForm)

def edit_desktop(request, pk):
	return edit_device(request, pk, Desktop, DesktopForm)

def edit_mobile(request, pk):
	return edit_device(request, pk, Mobile, MobileForm)


def delete_laptop(request, pk):

	Laptop.objects.filter(id=pk).delete()

	items = Laptop.objects.all()

	context = {
		'items': items
	}

	return render(request, 'index.html', context)


def delete_desktop(request, pk):

	Desktop.objects.filter(id=pk).delete()

	items = Desktop.objects.all()

	context = {
		'items': items
	}

	return render(request, 'index.html', context)


def delete_mobile(request, pk):

	Mobile.objects.filter(id=pk).delete()

	items = Mobile.objects.all()

	context = {
		'items': items
	}

	return render(request, 'index.html', context)

def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    # The data is hard-coded here, but you could load it from a database or
    # some other source.
    csv_data = (
        ('First row', 'Foo', 'Bar', 'Baz'),
        ('Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"),
    )

    t = loader.get_template('my_template_name.txt')
    c = {'data': csv_data}
    response.write(t.render(c))
    return response