from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Faculty(models.Model):
    PID = models.CharField(max_length=100, default = '',editable=False)
    Office_Addr = models.CharField(max_length=100, default = '')

class Device(models.Model):
    type = models.CharField(max_length=100, default = '')
    price = models.IntegerField()
    Manufacturer = models.CharField(max_length=100, default = '')     # Manufacturer
    Model = models.CharField(max_length=100, default = '')
    VT_Tag = models.CharField(max_length=100, default = '')
    CS_Tag = models.CharField(max_length=100, default = '')
    Serial_Number = models.CharField(max_length=100, default = '')
    #
    choices = (
        ('AVAILABLE', 'Item ready to be purchased'),
        ('SOLD', 'Item Sold'),
        ('RESTOCKING', 'Item restocking in few days')
    )

    status = models.CharField(max_length=10, choices=choices, default="SOLD") #Available, Sold, Restocking
    issue = models.CharField(max_length=100, default="No issues")

    class Meta:
        unique_together = ('VT_Tag', 'CS_Tag')
        ordering = ['-id']


    def _str_(self):
        return 'Type : {0} Price : {1}'.format(self.type, self.price)

class UserDevice(models.Model):
    UserPID =  models.CharField(max_length=100, default = '')
    DeviceID = models.CharField(max_length=100, default = '')
    Note = models.CharField(max_length=100, default = '')
    # Custodian = models.CharField(max_length=64, default = '')
    isHomeUse = models.BooleanField(default=False)
    CheckoutDate = models.DateField(auto_now=True)  # create time (automatic)
    ReturnDate = models.DateField()  # create time (automatic)

class Building(models.Model):
    BuildingID = models.IntegerField(primary_key = True)
    Building_Name = models.CharField(max_length=64)  # Aliases/cnames
    Building_Addr = models.CharField(max_length=64)  # Aliases/cnames
    

class NetworkInterface(models.Model):
    NetworkID = models.IntegerField(primary_key = True)
    DeviceID =  models.CharField(max_length=100, default = '')  
    Hostname = models.CharField(max_length=64)
    Aliases = models.CharField(max_length=64)  # Aliases/cnames
    IPv4 = models.GenericIPAddressField()      # IPv6 Address
    IPv6 = models.GenericIPAddressField()    # IPv6 Address
    BuildingID = models.IntegerField()  
    create_Date = models.DateField(auto_now=True)  # create time (automatic)