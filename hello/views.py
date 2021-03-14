from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from hello.forms import *
from hello.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, ListView
from django.db.models import Q 
import logging


class HomePageView(TemplateView):
    template_name = 'home.html'

class SearchResultsView(ListView):
    model = Device
    template_name = 'main/search_results.html'  
    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Device.objects.filter(
            Q(CS_Tag__icontains=query) | Q(VT_Tag__icontains=query)
        )
        return object_list

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return login_request(request)
    else:
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

def mcbrydehall(request):
    return render(request, "building/mcbryde-hall.html")

def faq(request):
    return render(request, "main/faq.html")

def privacy(request):
    return render(request, "main/privacy-policy.html")

def check_out(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    context = {
        'VT_Property': "VT000320684",
        'CS_Property': "CS0002824",
        "is_student_user": False,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "check-out.html", context=context)

def account(request):
    query_results = UserDevice.objects.all()
    return render(request, "main/account.html",{'query_results':query_results})
    # return render(request, "main/account.html")

def dashboard(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    query_results = UserDevice.objects.all()
    return render(request, "main/dashboard.html",{'query_results':query_results})

def guest_dashboard(request):
    query_results = UserDevice.objects.all()
    return render(request, "main/guest-dashboard.html",{'query_results':query_results})

def display_devices(request):
    items = Device.objects.all()
    # .filter()
    context = {
        'items': items,
        'header': 'Device'
    }

    return render(request, 'index.html', context)

def display_hostnames(request):
    items = Hostname.objects.all()
    context = {
        'items': items,
        'header': 'Hostname'
    }

    return render(request, 'index.html', context)

def display_tickets(request):
    items = Ticket.objects.all()
    context = {
        'items': items,
        'header': 'Ticket'
    }

    return render(request, 'main/account.html', context)

def display_faculty(request):
    items = UserDevice.objects.all()
    context = {
        'items': items,
        'header': 'UserDevice'
    }
    return render(request, 'main/account.html', context)

def display_equipment_checkout_form(request):
    return render(request, "check-out.html")

def add_item(request, cls):
    if not request.user.is_authenticated:
        raise PermissionDenied    
    if request.method == 'POST':
        form = cls(request.POST)

        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = cls()
        return render(request, 'add_new.html', {'form': form})



def add_device(request):
    return add_item(request, deviceForm)

def add_hostname(request):
    return add_item(request, AddHostnameForm)

def add_ticket(request):
    return add_item(request, AddTicketForm)

def add_faculty(request):
    return add_item(request, AddGuestForm)

def edit_item(request, pk, model, cls):
    if not request.user.is_authenticated:
        raise PermissionDenied
    item = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        form = cls(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = cls(instance=item)

        return render(request, 'edit_item.html', {'form': form})


def edit_device(request, pk):
    return edit_item(request, pk, Device, deviceForm)


def delete_device(request, pk):
    if request.user.is_authenticated:
        Device.objects.filter(id=pk).delete()
        items = Device.objects.all()
        context = {
            'items': items
        }
        return render(request, 'index.html', context)
    else:
        raise PermissionDenied

def delete_hostname(request, pk):
    Hostname.objects.filter(id=pk).delete()
    items = Hostname.objects.all()
    context = {
        'items': items
    }
    return render(request, 'index.html', context)

def delete_ticket(request, pk):
    Ticket.objects.filter(id=pk).delete()
    items = Hostname.objects.all()
    context = {
        'items': items
    }
    return render(request, 'main/account.html', context)

def checkout_device(request, pk):
    if request.user.is_authenticated:
        Device.objects.filter(id=pk).status = 'Item Sold'
        items = Device.objects.all()
        context = {
            'items': items
        }
        return render(request, 'checkout.html', context)
    else:
        raise PermissionDenied

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