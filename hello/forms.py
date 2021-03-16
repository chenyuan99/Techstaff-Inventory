from django import forms
from django.contrib.auth.forms import UserCreationForm
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

# add event form
class AddUserDeviceForm(forms.ModelForm):
    class Meta:
        model = UserDevice
        fields = '__all__'


# add guest
class AddFacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'

class deviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'

    helper = FormHelper()

    
        

# class userDeviceForm(forms.ModelForm):
#     class Meta:
#         model = UserDevice
#         field = '__all__'

class AddNetworkForm(forms.ModelForm):
    class Meta:
        model = NetworkInterface
        fields = '__all__'





#search
# class deviceSearchFrom(forms.ModelForm):
#     class Meta:
#         model = Device
#         fields = '__all__'

