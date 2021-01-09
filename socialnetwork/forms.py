from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from socialnetwork.models import UserProfile


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'surname', 'email', 'country', 'city', 'employment']
