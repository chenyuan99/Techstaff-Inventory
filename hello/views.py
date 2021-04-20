from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from hello.forms import *
from hello.models import *
from hello.resources import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from .filters import *
import logging
from tablib import Dataset
from hello.ipv6_generator import *
import datetime
import csv


class HomePageView(TemplateView):
    template_name = 'home.html'


class SearchResultsView(ListView):
    model = Device
    template_name = 'main/search_results.html'
    def get_queryset(self):  # new
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
    elif request.user.is_staff:
        return render(request, "index.html")
    else:
        query_results = UserDevice.objects.all()
        return render(request, "main/account.html", {'query_results': query_results})


def about(request):
    return render(request, "main/about.html")

def legacy(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    items = Device.objects.all()
    context = {
        'items': items,
    }
    return render(request, "main/legacy.html",context)

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, "db.html", {"greetings": greetings})


def logout_request(request):
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return redirect("index")


def login_request(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        pass_word = request.POST['password']
        userobj = authenticate(request, username=user_name, password=pass_word)
        if userobj is not None:
            login(request, userobj)
            # messages.success(request, 'You are Logged in !')
            return redirect('/')
        else:
            # messages.success(request, 'Wrong credentials', extra_tags='red')
            return redirect('/')
    else:

        if request.user.is_authenticated:
            return redirect('/')
        else:
            form = LoginForm()
            context = {'form': form}
            return render(request, 'main/login.html', context)


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
            return render(request=request,
                          template_name="main/register.html",
                          context={"form": form})
    form = UserCreationForm
    return render(request=request,
                  template_name="main/register.html",
                  context={"form": form})


def faq(request):
    return render(request, "main/faq.html")


def privacy(request):
    return render(request, "main/privacy-policy.html")


def check_out(request, pk):
    if not request.user.is_authenticated:
        raise PermissionDenied

    userdevice = get_object_or_404(UserDevice, pk=pk)
    if request.method == 'POST':
        userdevice_form = UserDeviceCheckoutForm(request.POST, instance=userdevice)
        if userdevice_form.is_valid():
            userdevice_form.save()
            return display_userDevice(request)
    else:
        device = get_object_or_404(Device, pk=userdevice.DeviceID)
        user = get_object_or_404(Faculty, PID=userdevice.UserPID)
        context = {
            'VT_Property': device.VT_Tag,
            'CS_Property': device.CS_Tag,
            "is_student_user": False,
            "Office_Addr": user.Office_Addr,
            "pid": user.PID,
            "full_name": user.FirstName + ' ' + user.LastName,
            "description": device.description,
            "serial": device.Serial_Number,
            "serial": device.Serial_Number,
            "checkout_date": userdevice.CheckoutDate,
            "Note" : userdevice.Note
            
        }
        # Render the HTML template index.html with the data in the context variable
        return render(request, "check-out.html", context=context)

# display different userdevices based on their permissions
def account(request):
    if not request.user.is_authenticated:
        return login_request(request)
    if not request.user.is_staff:
        query_results = list(UserDevice.objects.filter(UserPID=request.username))
    else:
        query_results = UserDevice.objects.all()
    return render(request, "main/account.html", {'query_results': query_results})



def guest_dashboard(request):
    query_results = UserDevice.objects.all()
    return render(request, "main/guest-dashboard.html", {'query_results': query_results})


# -------------------------display-----------------------------------
def display_devices(request):
    items = Device.objects.all()
    # .filter()
    myFilter = deviceFilter(request.GET, queryset=items)
    items = myFilter.qs
    context = {
        'items': items,
        'header': 'Device',
        'myFilter': myFilter,
    }

    return render(request, 'index.html', context)


def display_hostnames(request):
    items = NetworkInterface.objects.all()
    myFilter = networkFilter(request.GET, queryset=items)
    items = myFilter.qs
    context = {
        'items': items,
        'header': 'Hostname',
        'myFilter': myFilter,
    }

    return render(request, 'index.html', context)


def display_buildings(request):
    items = Building.objects.all()
    myFilter = buildingFilter(request.GET, queryset=items)
    items = myFilter.qs
    context = {
        'items': items,
        'header': 'building',
        'myFilter': myFilter,
    }

    return render(request, 'index.html', context)


def display_faculty(request):
    items = Faculty.objects.all()
    myFilter = facultyFilter(request.GET, queryset=items)
    items = myFilter.qs
    context = {
        'items': items,
        'header': 'faculty',
        'myFilter': myFilter,
    }
    return render(request, 'index.html', context)


def display_userDevice(request):
    items = UserDevice.objects.all()
    myFilter = UserDeviceFilter(request.GET, queryset=items)
    items = myFilter.qs
    context = {
        'items': items,
        'header': 'UserDevice',
        'myFilter': myFilter
    }
    return render(request, 'main/account.html', context)

def display_userCase(request):
    devices = Device.objects.all()
    faculty = Faculty.objects.all()
    myFilter1 = useCaseDeviceFilter(request.GET, queryset=devices)
    myFilter2 = useCaseFacultyFilter(request.GET, queryset=faculty)
    devs = myFilter1.qs
    facs = myFilter2.qs
    content = {
        'devs': devs,
        'facs': facs,
        'myFilter1': myFilter1,
        'myFilter2': myFilter2,

    }
    return render(request, 'usecases/assign_device.html', content)

def display_ip(request):
    items = IPAddr.objects.all()
    myFilter = ipFilter(request.GET, queryset=items)
    items = myFilter.qs
    context = {
        'items': items,
        'header': 'ip',
        'myFilter': myFilter,
    }

    return render(request, 'index.html', context)

# -------------------------add-----------------------------------
def add_device(request):
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        form = deviceForm(request.POST)

        if form.is_valid():
            form.save()
            return display_devices(request)

    else:
        form = deviceForm
        return render(request, 'add_new.html', {'form': form})


def add_hostname(request):
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        existing_host = NetworkInterface.objects.filter(DeviceID=request.POST['DeviceID'])
        if (existing_host):
            return edit_network(request, existing_host[0].NetworkID)
        else:
            form = AddNetworkForm(request.POST)
            if form.is_valid():
                form.save()
                return display_hostnames(request)

    else:
        form = AddNetworkForm
        buildings = Building.objects.all()
        context={'form': form,
        'buildings':buildings}
        return render(request, 'add_hostname.html',context )


def add_building(request):
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        form = buildingForm(request.POST)

        if form.is_valid():
            form.save()
            return display_buildings(request)

    else:
        form = buildingForm
        return render(request, 'add_new.html', {'form': form})


def add_userDevice(request):
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        form = AddUserDeviceForm(request.POST)

        if form.is_valid():
            form.save()
            return display_userDevice(request)

    else:
        form = AddUserDeviceForm
        return render(request, 'add_new.html', {'form': form})


def add_faculty(request):
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        form = AddFacultyForm(request.POST)

        if form.is_valid():
            form.save()
            return display_faculty(request)

    else:
        form = AddFacultyForm
        return render(request, 'add_new.html', {'form': form})


def add_ip(request):
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        form = AddIpAddressForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('display_ip')

    else:
        form = AddIpAddressForm
        return render(request, 'add_new.html', {'form': form})

# -------------------------edit-----------------------------------
def edit_item(request, pk, model, cls):
    if not request.user.is_staff:
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


def edit_network(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied
    item = get_object_or_404(NetworkInterface, pk=pk)

    if request.method == 'POST':
        form = AddNetworkForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return display_hostnames(request)

    else:
        form = AddNetworkForm(instance=item)
        return render(request, 'edit_item.html', {'form': form})

def edit_ip(request, IPID, networkID=None):
    if not request.user.is_staff:
        raise PermissionDenied
    item = get_object_or_404(IPAddr, IPID=IPID)

    if request.method == 'POST':
        form = EditIpAddressForm(request.POST, instance=item)
        if form.is_valid():
            ip = form.save(commit=False)
            if request.POST.get('randomIPv6') == 'on':
                # look for Building abbr: 
                if ip.Building_Abbr:
                    building = Building.objects.filter(Building_Abbr=ip.Building_Abbr)
                    if building and building[0].IPv6_prefix:
                        prefix = building[0].IPv6_prefix
                        ip.IPv6 = ipv6_generator(prefix).split(',')[-1].strip()
                    else:
                        messages.info(request, 'Cannot find building IPv6 prefix. IP not updated.')
                        return redirect('display_ip')
                
                else:
                    messages.info(request, 'Building Abbr not filled in. IP not updated.')
                    return redirect('display_ip') 
            messages.success(request, 'IP updated!')
            ip.save()
            return redirect('display_ip')


    else:

        form = EditIpAddressForm(instance=item)
        return render(request, 'edit_item.html', {'form': form})

def edit_faculty(request, PID):
    if not request.user.is_staff:
        raise PermissionDenied
    item = get_object_or_404(Faculty, PID=PID)

    if request.method == 'POST':
        form = AddFacultyForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return display_faculty(request)

    else:
        form = AddFacultyForm(instance=item)
        return render(request, 'edit_item.html', {'form': form})


def edit_building(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied
    item = get_object_or_404(Building, pk=pk)

    if request.method == 'POST':
        form = buildingForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return display_buildings(request)

    else:
        form = buildingForm(instance=item)
        return render(request, 'edit_item.html', {'form': form})


def edit_userDevice(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied
    item = get_object_or_404(UserDevice, pk=pk)

    if request.method == 'POST':
        form = AddUserDeviceForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return display_userDevice(request)

    else:
        form = AddUserDeviceForm(instance=item)
        return render(request, 'edit_item.html', {'form': form})


# -------------------------delete-----------------------------------
# def delete_device(request, pk):
#     device = Device.objects.get(id=pk)
#     if request.method == "POST":
#         device.delete()
#         return display_devices(request)

#     form = deviceForm(request.POST, instance=device)
#     for fieldname in form.fields:
#         form.fields[fieldname].disabled = True

#     return render(request, 'delete_item.html', {'form': form})


def delete_device(request, CS_Tag):
    device = Device.objects.get(CS_Tag=CS_Tag)
    if request.method == "POST":
        device.delete()
        return display_devices(request)

    form = deviceForm(request.POST, instance=device)
    for fieldname in form.fields:
        form.fields[fieldname].disabled = True

    return render(request, 'delete_item.html', {'form': form})


def delete_network(request, pk):
    network = NetworkInterface.objects.get(pk=pk)
    if request.method == "POST":
        ip = IPAddr.objects.filter(NetworkID=network.NetworkID)

        if ip:
            # changing IP assignment status
            ip[0].status = 'Available'
            ip[0].NetworkID = None
            ip[0].save()
        network.delete()
        messages.success(request, 'Hostname for ' + network.DeviceID + ' deleted!')
        return redirect('display_hostnames')

    form = AddNetworkForm(request.POST, instance=network)
    for fieldname in form.fields:
        form.fields[fieldname].disabled = True

    return render(request, 'delete_item.html', {'form': form})


def delete_faculty(request, PID):
    faculty = Faculty.objects.get(PID=PID)
    if request.method == "POST":
        faculty.delete()
        return display_faculty(request)

    form = AddFacultyForm(request.POST, instance=faculty)
    for fieldname in form.fields:
        form.fields[fieldname].disabled = True

    return render(request, 'delete_item.html', {'form': form})


def delete_building(request, pk):
    building = Building.objects.get(pk=pk)
    if request.method == "POST":
        building.delete()
        return display_buildings(request)

    form = buildingForm(request.POST, instance=building)
    for fieldname in form.fields:
        form.fields[fieldname].disabled = True

    return render(request, 'delete_item.html', {'form': form})


def delete_userDevice(request, pk):
    userDevice = UserDevice.objects.get(pk=pk)
    if request.method == "POST":
        userDevice.delete()
        return display_userDevice(request)

    form = AddUserDeviceForm(request.POST, instance=userDevice)
    for fieldname in form.fields:
        form.fields[fieldname].disabled = True

    return render(request, 'delete_item.html', {'form': form})

def delete_ip(request, IPID):
    ip = IPAddr.objects.get(IPID=IPID)
    if request.method == "POST":
        ip.delete()
        
        return redirect('display_ip')

    form = EditIpAddressForm(request.POST, instance=ip)
    for fieldname in form.fields:
        form.fields[fieldname].disabled = True
    return render(request, 'delete_item.html', {'form': form})


# -------------------------    ------------------
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


def edit_device(request, CS_Tag):
    if not request.user.is_staff:
        raise PermissionDenied
    item = get_object_or_404(Device, CS_Tag=CS_Tag)

    if request.method == 'POST':
        form = deviceForm(request.POST, instance=item)
        
        if form.is_valid():
            form.save()
            return display_devices(request)

    else:
        form = deviceForm(instance=item)
        return render(request, 'edit_item.html', {'form': form})

# EDITING DEVICE FOR DETAIL PAGE
def edit_device_inDetailPage(request, CS_Tag):
    if not request.user.is_authenticated:
        raise PermissionDenied
    item = get_object_or_404(Device, CS_Tag=CS_Tag)

    if request.method == 'POST':
        form = deviceForm(request.POST, instance=item)

        if form.is_valid():
            form.save()
            return view_device(request, CS_Tag)

    else:
        form = deviceForm(instance=item)
        return render(request, 'edit_item.html', {'form': form})

#TODO: check IP address duplicates
def checkDuplicateIP(ip):
    ip_list = [ip for ip in IPAddr.objects.all()]
    

def assignip_new_hostname(request, CS_Tag):
    if not request.user.is_staff:
        raise PermissionDenied
    
    if request.method == 'POST':
        network_form = AddNetwork_assign_ip(request.POST)
        ip_form = AddIpAddressForm(request.POST)
        if network_form.is_valid():
            network_form.save()
        
        if ip_form.is_valid():
            ip = ip_form.save(commit=False)
            if request.POST.get('randomIPv6') == 'on':
                # look for Building abbr: 
                if ip.Building_Abbr:
                    building = Building.objects.filter(Building_Abbr=ip.Building_Abbr)
                    if building and building[0].IPv6_prefix:
                        prefix = building[0].IPv6_prefix
                        randomIP = ipv6_generator(prefix)
                        if (randomIP != 1):
                            ip.IPv6 = ipv6_generator(prefix).split(',')[-1].strip()
                        else: 
                            messages.info(request, 'Cannot generate IPv6 with given prefix. IP not assigned.')
                            return redirect('display_ip')
                    else:
                        messages.info(request, 'Cannot find building IPv6 prefix. IP not assigned.')
                        return redirect('display_ip')
                else:
                    messages.info(request, 'Building Abbr not filled in. IP not assigned.')
                    return redirect('display_ip')
                
            ip.status = 'Assigned'
            networkID = max([network.NetworkID for network in NetworkInterface.objects.all()])
            ip.NetworkID = networkID
            ip.save()
            messages.success(request, 'IP and hostname for ' + CS_Tag + ' assigned!')
        return redirect('display_ip')
    else:
        networkInitial = {
                'DeviceID' : CS_Tag
            }
        network_form = AddNetwork_assign_ip(initial=networkInitial)
        ip_form = AddIpAddressForm_no_hostname()
        return render(request, 'assign_hostname_ip.html', {'network': network_form,
            'assignip' : ip_form, 'DeviceID' : CS_Tag })


def assignip_to_device(request, CS_Tag):
    if not request.user.is_staff:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = AddIpAddressForm(request.POST)
        if form.is_valid():
            ip = form.save(commit=False)
            if request.POST.get('randomIPv6') == 'on':
                # look for Building abbr: 
                if ip.Building_Abbr:
                    building = Building.objects.filter(Building_Abbr=ip.Building_Abbr)
                    if building and building[0].IPv6_prefix:
                        prefix = building[0].IPv6_prefix
                        randomIP = ipv6_generator(prefix)
                        if (randomIP != 1):
                            ip.IPv6 = ipv6_generator(prefix).split(',')[-1].strip()
                        else: 
                            messages.info(request, 'Cannot generate IPv6 with given prefix. IP not assigned.')
                            return redirect('display_ip')
                    else:
                        messages.info(request, 'Cannot find building IPv6 prefix. IP not assigned.')
                        return redirect('display_ip')
                
                else:
                    messages.info(request, 'Building Abbr not filled in. IP not assigned.')
                    return redirect('display_ip') 
                
            ip.status = 'Assigned'
            networkID = max([network.NetworkID for network in NetworkInterface.objects.all()])
            ip.NetworkID = networkID
            ip.save()
            messages.success(request, 'IP address for ' + CS_Tag + ' assigned!')

        return redirect('display_ip')
    
    else:
        item = get_object_or_404(Device, CS_Tag=CS_Tag)
        form = EditIpAddressForm(instance=item)
        device = Device.objects.get(CS_Tag=CS_Tag)
        # look for matching hostname/netforkinterface
        network = NetworkInterface.objects.filter(DeviceID = device.CS_Tag)
        if network:
            ip = IPAddr.objects.filter(NetworkID=network[0].NetworkID)
            if ip: 
                messages.success(request, 'Edit IP address for ' + CS_Tag)
                print('editing ip: ', network[0].NetworkID)
                return redirect('edit_ip', ip[0].IPID)
            else:
                # adding IP:
                initial = {
                    'NetworkID' : network[0].NetworkID,
                    'Building_Abbr' : network[0].Building_Abbr
                }
                form = AssignIPForm(initial=initial)
                return render(request, 'assign_ip.html', {'form': form, 'DeviceID': CS_Tag })

        else:
            return redirect('assignip_new_hostname', CS_Tag)



def view_device(request, CS_Tag):
    device = Device.objects.get(CS_Tag=CS_Tag)
    userdevices = list(UserDevice.objects.filter(DeviceID=device.CS_Tag))
    networks = list(NetworkInterface.objects.filter(DeviceID=device.CS_Tag))
    history = device.history.all()
    diffHistory = list()
    delta = list()
    diffHistory.append(history[0])
    for i in range(0, history.count() - 1):
        nextHistory = history[i+1]
        tempDiff = history[i].diff_against(nextHistory)
        if len(tempDiff.changes) != 0:
             delta.append(tempDiff)
             diffHistory.append(nextHistory)
            #  print(tempDiff.changes)
    context = {
        'item': device,
        'userdevices':userdevices,
        'networks':networks,
        'history': diffHistory,
        'delta': delta

    }
    return render(request, "device_detail.html", context)


def view_hostname(request, NetworkID):
    network = NetworkInterface.objects.get(NetworkID=NetworkID)
    device = Device.objects.get(CS_Tag=network.DeviceID)
    ip = IPAddr.objects.filter(NetworkID=NetworkID)

    context = {}
    networkHistory = network.history.all()
    diffHistory = list()
    delta = list()
    diffHistory.append(networkHistory[0])
    for i in range(0, networkHistory.count() - 1):
        nextHistory = networkHistory[i + 1]
        tempDiff = networkHistory[i].diff_against(nextHistory)
        if len(tempDiff.changes) != 0:
            delta.append(tempDiff)
            diffHistory.append(nextHistory)



    if ip:
        for item in ip:
            ipHistory = item.history.all()
            diff = list()       #ip diff
            delta2 = list()     #ip delta
            diff.append(ipHistory[0])
            for i in range(0, ipHistory.count() - 1):
                nextHistory = ipHistory[i + 1]
                tempDiff = ipHistory[i].diff_against(nextHistory)
                if len(tempDiff.changes) != 0:
                    delta2.append(tempDiff)
                    diff.append(nextHistory)

            context = {
                'item': network,
                'device': device,
                'ip': ip,
                'history': diffHistory,
                'iphistory': ipHistory,
                'delta': delta,
                'delta2': delta2,
            }
    else:
        context = {
            'item': network,
            'device': device,
            'history': diffHistory,
            'delta': delta
        }
    return render(request, "hostname_detail.html", context)

def export_devices(request):
    device_resource = DeviceResource()
    dataset = device_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="deivices.csv"'
    return response


def simple_upload(request):
    if request.method == 'POST':
        person_resource = DeviceResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'import/import.html')

def upload_devices(request):
    if request.method == 'POST':
        person_resource = DeviceResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'import/import-devices.html')

def upload_hostnames(request):
    if request.method == 'POST':
        person_resource = NetworkInterfaceResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'import/import-hostnames.html')

def upload_buildings(request):
    if request.method == 'POST':
        person_resource = BuildingResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'import/import-buildings.html')

def upload_facultys(request):
    if request.method == 'POST':
        person_resource = FacultyResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'import/import-facultys.html')

def upload_ips(request):
    if request.method == 'POST':
        person_resource = IPAddrResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'import/import-ips.html')

def export_filter_devices(request):
    device = Device.objects.all()
    filter = deviceFilter(request.GET, queryset=device).qs
    response = HttpResponse(content_type='text/csv')
    file_name = "fltred_device_data" + str(datetime.datetime.today()) + ".csv"

    writer = csv.writer(response)
    fields = ["CS_Tag", "Serial_Number", "VT_Tag", "acq_date", "description", "issue", "price", "status", "type"]
    writer.writerow(fields)
    for i in filter.values_list("CS_Tag", "Serial_Number", "VT_Tag", "acq_date", "description", "issue", "price", "status", "type"):
        writer.writerow(i)
    response['Content-Disposition'] = 'attachment; filename = "' + file_name + '"'
    return response