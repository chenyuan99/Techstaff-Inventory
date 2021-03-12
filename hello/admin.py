from django.contrib import admin
from django.contrib.admin.models import LogEntry

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

    search_fields = (
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

class FacultyAdmin(GuestAdmin):
    model = Faculty

    list_filter =("realname","phone","email","assigned_student")
    list_display =("realname","phone","email","assigned_student")
    search_fields =("realname","phone","email","assigned_student")

class StudentAdmin(admin.ModelAdmin):
    model = Student

    list_filter =("realname","phone","email")
    list_display =("realname","phone","email")

class StaffAdmin(admin.ModelAdmin):
    model = Staff

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]


admin.site.register(Hostname, HostnameAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Staff, StaffAdmin)