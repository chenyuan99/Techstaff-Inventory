from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class Ticket(models.Model):
    address = models.CharField(max_length=200)        
    start_time = models.DateTimeField(auto_now=True)   
    create_time = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.address



class Guest(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)  # 关联发布会id
    realname = models.CharField(max_length=64)  # 姓名
    phone = models.CharField(max_length=16)     # 手机号
    email = models.EmailField()                 # 邮箱
    sign = models.BooleanField()                # 签到状态
    create_time = models.DateTimeField(auto_now=True)  # 创建时间（自动获取当前时间）

    class Meta:
        unique_together = ('phone', 'ticket')
        ordering = ['-id']

    def __str__(self):
        return self.realname

job_types = ( ('remote', 'Remote'), ('visa', 'Visa'), ('intern', 'Intern') )

class JobApplication(models.Model):

    company = models.CharField(max_length=255)
    place = models.CharField(max_length=255)

    source = models.CharField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)

    application_type = models.CharField(max_length=255, blank=True)
    response = models.CharField(max_length=255, blank=True)
    active = models.BooleanField()

    comments = models.TextField(max_length=512, blank=True)
    job_type = models.CharField(choices=job_types, max_length=32)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return ' - '.join([self.company, self.place])

class JobUpdate(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='updates')
    update = models.TextField(max_length=1024)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.update

# Create your models here.

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


# class Laptop(Device):
#     pass

# class Desktop(Device):
#     pass

# class Mobile(Device):
#     pass

class Hostname(models.Model):
    Hostname = models.CharField(max_length=64)
    # models.ForeignKey(Ticket, on_delete=models.CASCADE)  # Hostname
    Aliases = models.CharField(max_length=64)  # Aliases/cnames
    IP_Address = models.CharField(max_length=64)     # IP Address
    IPv6_Address = models.CharField(max_length=64)   # IPv6 Address
    MAC_Address = models.CharField(max_length=64)               #  MAC Address
    create_time = models.DateTimeField(auto_now=True)  # create time (automatic)
