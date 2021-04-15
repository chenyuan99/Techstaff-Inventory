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

class DeviceResource(resources.ModelResource):
    class Meta:
        model = Device

class IPAddrResource(resources.ModelResource):
    class Meta:
        model = IPAddr