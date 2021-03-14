from django.contrib import admin
from django.contrib.admin.models import LogEntry

# Register your models here.
from .models import *
from import_export.admin import ImportExportModelAdmin
class ViewAdmin(ImportExportModelAdmin):
	pass

# class HostnameAdmin(admin.ModelAdmin):
#     model = Hostname

#     list_filter =(
#         'Hostname',
#         'Aliases',
#         'IP_Address',
#         'IPv6_Address',
#         'MAC_Address',
#         'create_time'
#     )

#     search_fields = (
#         'Hostname',
#         'Aliases',
#         'IP_Address',
#         'IPv6_Address',
#         'MAC_Address',
#         'create_time'
#     )


#     list_display = (
#         'Hostname',
#         'Aliases',
#         'IP_Address',
#         'IPv6_Address',
#         'MAC_Address',
#         'create_time'
#     )

class DeviceAdmin(admin.ModelAdmin):
    model = Device


class FacultyAdmin(admin.ModelAdmin):
    model = Faculty
    list_filter =("PID","Office_Addr")
    list_display =("PID","Office_Addr")
    search_fields =("PID","Office_Addr")

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

admin.site.register(Device, DeviceAdmin)
admin.site.register(Faculty, FacultyAdmin)