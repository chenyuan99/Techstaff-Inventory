from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from hello.models import *
from django.forms import ModelForm
from crispy_forms.helper import FormHelper


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.PasswordInput()

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = "input"
        # self.helper.field_class = "form-control"


class AddUserDeviceForm(forms.ModelForm):
    # ReturnDate = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))
    def __init__(self, *args, **kwargs):
        super(AddUserDeviceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        self.fields['Note'].required = False
        self.fields['Address'].required = False
        self.fields['ReturnDate'].required = False

    class Meta:
        model = UserDevice
        fields = '__all__'


# add guest
class AddFacultyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddFacultyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'


    class Meta:
        model = Faculty
        fields = '__all__'


class deviceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(deviceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        for key in self.fields:
            if key == 'CS_Tag':
                continue
            self.fields[key].required = False

    class Meta:
        model = Device
        exclude = ('CS_Tag',)


# class userDeviceForm(forms.ModelForm):
#     class Meta:
#         model = UserDevice
#         field = '__all__'

class AddNetworkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNetworkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        for key in self.fields:
            if key == 'DeviceID':
                continue
            self.fields[key].required = False

    class Meta:
        model = NetworkInterface
        fields = '__all__'


class buildingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(buildingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        self.fields['IPv6_prefix'].required = False

    class Meta:
        model = Building
        fields = '__all__'


class IpAddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IpAddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        for key in self.fields:
            if key == 'DeviceID':
                continue
            self.fields[key].required = False

    class Meta:
        model = IPAddr
        fields = '__all__'
