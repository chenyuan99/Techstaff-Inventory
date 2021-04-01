from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import *
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin


class ViewAdmin(ImportExportModelAdmin):
	pass

class HostnameAdmin(ImportExportModelAdmin):
    model = NetworkInterface

    list_filter =(
        'Hostname',
        'Aliases',
        'IPv4',
        'IPv6',
        'create_Date',
            'DeviceID',
    'BuildingID',
    )

    search_fields =(
        'Hostname',
        'Aliases',
        'IPv4',
        'IPv6',
        'create_Date',
            'DeviceID',
    'BuildingID',
    )


    list_display = (
        'Hostname',
        'Aliases',
        'IPv4',
        'IPv6',
        'create_Date',
            'DeviceID',
    'BuildingID',
    )

class DeviceAdmin(ImportExportModelAdmin,SimpleHistoryAdmin):
    model = Device
    list_filter =("VT_Tag","CS_Tag","Serial_Number","type","status","issue")
    list_display =("VT_Tag","CS_Tag","Serial_Number","type","status","issue")
    search_fields =("VT_Tag","CS_Tag","Serial_Number","type","status","issue")
    history_list_display = ["status"]

class UserDeviceAdmin(ImportExportModelAdmin):
    model = UserDevice
    list_filter =("UserPID","DeviceID","CheckoutDate")
    list_display =("UserPID","DeviceID","CheckoutDate")
    search_fields =("UserPID","DeviceID","CheckoutDate")

class FacultyAdmin(ImportExportModelAdmin):
    model = Faculty
    list_filter =("PID","Office_Addr")
    list_display =("PID","Office_Addr")
    search_fields =("PID","Office_Addr")

class BuildingAdmin(ImportExportModelAdmin):
    model = Building
    list_filter =("BuildingID","Building_Name","Building_Addr")
    list_display =("BuildingID","Building_Name","Building_Addr")
    search_fields =("BuildingID","Building_Name","Building_Addr")

@admin.register(LogEntry)
class LogEntryAdmin(ImportExportModelAdmin):
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
admin.site.register(UserDevice, UserDeviceAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(NetworkInterface, HostnameAdmin)
admin.site.register(Building, BuildingAdmin)