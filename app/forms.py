from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from app.models import Blog

class  SignupForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password (again)', widget=forms.PasswordInput())
    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {'email':'Email'}

class LoginForm(AuthenticationForm):
    fields = '__all__'

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.IntegerField()
    desc = forms.CharField(widget=forms.Textarea(), label='Description')

class UserEditForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'category', 'photo', 'description')
        