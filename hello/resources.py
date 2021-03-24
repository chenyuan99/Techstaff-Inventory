from import_export import resources
from hello.models import *

class DeviceResource(resources.ModelResource):
    class Meta:
        model = Device