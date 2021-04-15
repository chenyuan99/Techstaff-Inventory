from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
# Create your models here.

class Faculty(models.Model):
    PID = models.CharField(max_length=100, default = '', primary_key=True)
    Office_Addr = models.CharField(max_length=100, default = '')
    FirstName = models.CharField(max_length=100, default = 'First name')
    LastName = models.CharField(max_length=100, default = 'Last name')
    history = HistoricalRecords()

class Device(models.Model):
    Serial_Number = models.CharField(max_length=100, default = '', blank=True, null=True)
    type = models.CharField(max_length=100, default = '', blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=100, default = '', blank=True, null=True)
    VT_Tag = models.CharField(max_length=100, default = '', blank=True, null=True)
    CS_Tag = models.CharField(max_length=100, default = '', primary_key=True)
    acq_date = models.DateField(default='YYYY-MM-DD', blank=True, null=True)
    choices = (
        ('In Use', 'In Use'),
        ('In Storage', 'In Storage'),
        ('On Loan', 'On Loan'),
        ('Damaged', 'Damaged'),
        ('Missing', 'Missing'),
        ('Surplused', 'Surplused'),
        ('Transferred', 'Transferred'),
        ('Written Off', 'Written Off'),
        ('Orphaned', 'Orphaned')
    )

    status = models.CharField(max_length=15, choices=choices, default='In Use', blank=True, null=True) #Available, Sold, Restocking
    issue = models.CharField(max_length=100, default="No issues", blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['CS_Tag']


    def _str_(self):
        return 'Type : {0} Price : {1}'.format(self.type, self.price)
        ordering = ['CS_Tag']

class UserDevice(models.Model):
    UserPID =  models.CharField(max_length=100, default = '')
    DeviceID = models.CharField(max_length=100, default = '')
    Note = models.CharField(max_length=100, blank=True, null=True)
    isHomeUse = models.BooleanField(default=False)
    isCheckedOut = models.BooleanField(default=False)
    Address = models.CharField(max_length=100, blank=True, null=True)
    CheckoutDate = models.DateField(auto_now=True)  # create time (automatic)
    ReturnDate = models.DateField(default='YYYY-MM-DD', blank=True, null=True)  # create time (automatic)
    
    class Meta:
        unique_together = ('UserPID', 'DeviceID', 'CheckoutDate')
    history = HistoricalRecords()

class Building(models.Model):
    Building_Abbr = models.CharField(primary_key = True, max_length=64)
    Building_Name = models.CharField(max_length=64)
    Building_Addr = models.CharField(max_length=64)
    IPv6_prefix = models.CharField(max_length=64, blank=True, null=True)
    history = HistoricalRecords()
    

class NetworkInterface(models.Model):
    NetworkID = models.AutoField(primary_key = True)
    DeviceID =  models.CharField(max_length=100, default = '', unique=True)  
    Hostname = models.CharField(max_length=64, blank=True)
    Aliases = models.CharField(max_length=64, blank=True)  # Aliases/cnames
    Building_Abbr = models.CharField(max_length=64, blank=True)  
    create_Date = models.DateField(auto_now=True, blank=True)  # create time (automatic)
    history = HistoricalRecords()

class IPAddr(models.Model):
    IPID = models.AutoField(primary_key = True)
    NetworkID = models.IntegerField(blank=True,null=True, unique=True)
    Building_Abbr = models.CharField(max_length=64, blank=True)
    IPv4 = models.GenericIPAddressField(blank=True, null=True, unique=True)
    IPv6 = models.GenericIPAddressField(blank=True, null=True, unique=True)
    choices = (
        ('Assigned', 'Assigned'),
        ('Available', 'Available')
    )

    status = models.CharField(max_length=20, choices=choices, default='Available', blank=True, null=True) 
    history = HistoricalRecords()