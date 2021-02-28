from django.contrib import admin

# Register your models here.
from .models import *
from import_export.admin import ImportExportModelAdmin
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