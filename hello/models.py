from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class Event(models.Model):
    address = models.CharField(max_length=200)        
    start_time = models.DateTimeField(auto_now=True)   
    create_time = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.address



class Guest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # 关联发布会id
    realname = models.CharField(max_length=64)  # 姓名
    phone = models.CharField(max_length=16)     # 手机号
    email = models.EmailField()                 # 邮箱
    sign = models.BooleanField()                # 签到状态
    create_time = models.DateTimeField(auto_now=True)  # 创建时间（自动获取当前时间）

    class Meta:
        unique_together = ('phone', 'event')
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
