from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Faculty(models.Model):
    PID = models.CharField(max_length=100, default = '', primary_key=True)
    Office_Addr = models.CharField(max_length=100, default = '')
    FirstName = models.CharField(max_length=100, default = 'First name')
    LastName = models.CharField(max_length=100, default = 'Last name')

class Device(models.Model):
    Serial_Number = models.CharField(max_length=100, default = '')
    type = models.CharField(max_length=100, default = '')
    price = models.IntegerField()
    description = models.CharField(max_length=100, default = '')
    VT_Tag = models.CharField(max_length=100, default = '')
    CS_Tag = models.CharField(max_length=100, default = '')
    acq_date = models.DateField(default='YYYY-MM-DD')
    #purchase_order =  models.CharField(max_length=100, default = '')
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

    status = models.CharField(max_length=15, choices=choices, default='In Use') #Available, Sold, Restocking
    issue = models.CharField(max_length=100, default="No issues")

    class Meta:
        unique_together = ('VT_Tag', 'CS_Tag')
        ordering = ['-id']


    def _str_(self):
        return 'Type : {0} Price : {1}'.format(self.type, self.price)
        ordering = ['-id']

class UserDevice(models.Model):
    UserPID =  models.CharField(max_length=100, default = '')
    DeviceID = models.CharField(max_length=100, default = '')
    Note = models.CharField(max_length=100, default = '')
    isHomeUse = models.BooleanField(default=False)
    CheckoutDate = models.DateField(auto_now=True)  # create time (automatic)
    ReturnDate = models.DateField(default='YYYY-MM-DD')  # create time (automatic)

    class Meta:
        unique_together = ('UserPID', 'DeviceID', 'CheckoutDate')

class Building(models.Model):
    BuildingID = models.AutoField(primary_key = True)
    Building_Name = models.CharField(max_length=64)  
    Building_Addr = models.CharField(max_length=64)  
    # TODO: add IPv6_prefix

class NetworkInterface(models.Model):
    NetworkID = models.AutoField(primary_key = True)
    DeviceID =  models.CharField(max_length=100, default = '')  
    Hostname = models.CharField(max_length=64)
    Aliases = models.CharField(max_length=64)  # Aliases/cnames
    IPv4 = models.GenericIPAddressField()      # IPv6 Address
    IPv6 = models.GenericIPAddressField()    # IPv6 Address
    BuildingID = models.IntegerField()  
    create_Date = models.DateField(auto_now=True)  # create time (automatic)