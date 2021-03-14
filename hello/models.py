from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Staff(User):
    pass

class Faculty(User):
    assigned_student = models.ForeignKey(User, on_delete=models.CASCADE)

class Device(models.Model):
    type = models.CharField(max_length=100, blank=False)
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


class Hostname(models.Model):
    Hostname = models.CharField(max_length=64)
    Aliases = models.CharField(max_length=64)  # Aliases/cnames
    IP_Address = models.CharField(max_length=64)     # IP Address
    IPv6_Address = models.CharField(max_length=64)   # IPv6 Address
    MAC_Address = models.CharField(max_length=64)               #  MAC Address
    create_time = models.DateTimeField(auto_now=True)  # create time (automatic)
    

class NetworkInterface(models.Model):
    NetworkID = models.IntegerField(primary_key = True)
    DeviceID =  models.ForeignKey(Device, on_delete=models.CASCADE)  # 关联发布会id
    Hostname = models.CharField(max_length=64)
    Aliases = models.CharField(max_length=64)  # Aliases/cnames
    IPv4 = models.GenericIPAddressField()      # IPv6 Address
    IPv6 = models.GenericIPAddressField()    # IPv6 Address
    BuildingID = models.ForeignKey(Building, on_delete=models.CASCADE)  # 关联发布会id
    create_Date = models.DateField(auto_now=True)  # create time (automatic)

class Building(models.Model):
    BuildingID = models.IntegerField(primary_key = True)
    Building_Name = models.CharField(max_length=64)  # Aliases/cnames
    Building_Addr = models.CharField(max_length=64)  # Aliases/cnames