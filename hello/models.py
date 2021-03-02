from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Guest(models.Model):
    realname = models.CharField(max_length=64)  # 姓名
    phone = models.CharField(max_length=16)     # 手机号
    email = models.EmailField()                 # 邮箱
    sign = models.BooleanField()                # 签到状态
    create_time = models.DateTimeField(auto_now=True)  # 创建时间（自动获取当前时间）

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.realname

class Staff(User):
    pass

class Student(Guest):
    pass

class Faculty(Guest):
    assigned_student = models.ForeignKey(Student, on_delete=models.CASCADE)  # 关联发布会id

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

class Ticket(models.Model):
    address = models.CharField(max_length=200) 
    device = models.ForeignKey(Device, on_delete=models.CASCADE)  # 关联发布会id
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)  # 关联发布会id
    notes = models.CharField(max_length=200)
    hostname =  models.ForeignKey(Hostname, on_delete=models.CASCADE)  # 关联发布会id
    create_time = models.DateTimeField(auto_now=True)

    choices = (
        ('AVAILABLE', 'Item ready to be purchased'),
        ('SOLD', 'Item Sold'),
        ('RESTOCKING', 'Item restocking in few days')
    )

    action = models.CharField(max_length=10, choices=choices, default="SOLD") #Available, Sold, Restocking
    
    def __str__(self):
        return self.address