from django.contrib import admin

# Register your models here.
from .models import *
from import_export.admin import ImportExportModelAdmin
# class JobUpdateInline(admin.StackedInline):
#     model = JobUpdate
#     extra = 1
#     max_num = 48

# class JobApplicationAdmin(admin.ModelAdmin):
#     inlines = [JobUpdateInline]
#     model = JobApplication

#     list_filter = (
#         'place',
#         'job_type',
#         'active'
#     )
#     list_display = ('company', 'place', 'job_type', 'created_on', 'updated_on')

# admin.site.register(JobApplication, JobApplicationAdmin)
# @admin.register(Device, Ticket)
class ViewAdmin(ImportExportModelAdmin):
	pass

class HostnameAdmin(admin.ModelAdmin):
    model = Hostname

    list_filter =(
        'Hostname',
        'Aliases',
        'IP_Address',
        'IPv6_Address',
        'MAC_Address',
        'create_time'
    )

    list_display = (
        'Hostname',
        'Aliases',
        'IP_Address',
        'IPv6_Address',
        'MAC_Address',
        'create_time'
    )

class DeviceAdmin(admin.ModelAdmin):
    model = Device

class TicketAdmin(admin.ModelAdmin):
    model = Ticket

class GuestAdmin(admin.ModelAdmin):
    model = Guest

    list_filter =("realname","phone","email")
    list_display =("realname","phone","email")

admin.site.register(Hostname, HostnameAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Guest, GuestAdmin)