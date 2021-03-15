import django_filters

from .models import *

class orderFilter(django_filters.FilterSet):
    class Meta:
        model = Device
        fields = '__all__'