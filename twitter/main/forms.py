from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models import Profile, Tweet


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2", 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'This email is already in use.')
        return email


class Log_inForm(forms.Form):
    username = forms.CharField(label=('User Name'))
    password = forms.CharField(label=('Password'), widget=forms.PasswordInput(render_value=False))


class Edit_ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'follow',)


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        exclude = ('owner',)
