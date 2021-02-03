from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from hello.models import Guest
from django.forms import ModelForm

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
class AddEventForm(forms.Form):
    # name = forms.CharField(max_length=100)           
    # limit = forms.IntegerField()                      # 限制人数
    # status = forms.BooleanField(required=False)       # 状态
    address = forms.CharField(max_length=200)         # 地址
    # start_time = forms.DateTimeField()                # 发布会时间


# add guest
class AddGuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['event', 'realname', 'phone', 'email', 'sign']