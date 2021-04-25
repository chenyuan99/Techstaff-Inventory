from import_export import resources
from hello.models import *

class DeviceResource(resources.ModelResource):
    class Meta:
        model = Device

class FacultyResource(resources.ModelResource):
    class Meta:
        model = Faculty

class BuildingResource(resources.ModelResource):
    class Meta:
        model = Building

class NetworkInterfaceResource(resources.ModelResource):
    class Meta:
        model = NetworkInterface

class UserDeviceResource(resources.ModelResource):
    class Meta:
        model = UserDevice

class IPAddrResource(resources.ModelResource):
    class Meta:
        model = IPAddr