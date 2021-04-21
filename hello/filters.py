import django_filters
from django_filters import DateFilter, CharFilter
from .models import *


class deviceFilter(django_filters.FilterSet):
    description = CharFilter(field_name='description', lookup_expr='icontains')
    VT_Tag = CharFilter(field_name='VT_Tag', lookup_expr='icontains')
    CS_Tag = CharFilter(field_name='CS_Tag', lookup_expr='icontains')
    Serial_Number = CharFilter(field_name='Serial_Number', lookup_expr='icontains')

    class Meta:
        model = Device
        exclude = ['price', 'issue']


class networkFilter(django_filters.FilterSet):
    class Meta:
        model = NetworkInterface
        fields = '__all__'


class UserDeviceFilter(django_filters.FilterSet):
    class Meta:
        model = UserDevice
        fields = '__all__'


class buildingFilter(django_filters.FilterSet):
    class Meta:
        model = Building
        fields = '__all__'


class facultyFilter(django_filters.FilterSet):
    class Meta:
        model = Faculty
        fields = '__all__'


class ipFilter(django_filters.FilterSet):
    class Meta:
        model = IPAddr
        fields = '__all__'


class useCaseDeviceFilter(django_filters.FilterSet):
    description = CharFilter(field_name='description', lookup_expr='icontains')
    VT_Tag = CharFilter(field_name='VT_Tag', lookup_expr='icontains')
    CS_Tag = CharFilter(field_name='CS_Tag', lookup_expr='icontains')
    Serial_Number = CharFilter(field_name='Serial_Number', lookup_expr='icontains')

    class Meta:
        model = Device
        fields = '__all__'
        exclude =['issue', 'acq_date', 'price']


class useCaseFacultyFilter(django_filters.FilterSet):
    class Meta:
        model = Faculty
        fields = '__all__'
