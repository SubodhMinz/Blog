from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import View, TemplateView
from .models import Blog
from .forms import SignupForm, LoginForm, ContactForm, UserEditForm, BlogForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView


# home view
class HomeView(View):
    def get(self, request):
        blogs = Blog.objects.all()
        return render(request, 'app/home.html', {'blogs':blogs})

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'app/detail-blog.html'
    contextt_object_name = 'blog'

# blog edit view
@login_required
def EditBlogView(request, pk):
    if request.method == "POST":
        blg_usr = Blog.objects.get(pk=pk).usr
        cur_usr = request.user
        if blg_usr == cur_usr:
            pi = Blog.objects.get(pk=pk)
            form = BlogForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your blog has been updated!!!')
                return redirect('/')
            else:
                return redirect('/')
        else:
            return HttpResponse('You are not authorised to edit this blog!!!')
    else:
        pi = Blog.objects.get(pk=pk)
        form = BlogForm(instance=pi)
        return render(request, 'app/blogcreate.html', {'form':form})


# Detail Blog View
class BlogDeleteView(DeleteView):
    model = Blog
    success_url = '/'

# Delete Blog View
@login_required
def BlogDeleteView(request, pk):
    if request.method == "POST":
        blg_usr = Blog.objects.get(pk=pk).usr
        cur_usr = request.user
        if blg_usr == cur_usr:
            pi = Blog.objects.get(pk=pk)
            pi.delete()
            return redirect('/')
        return redirect('/')
    return redirect('/')

# contact view
class ContactView(FormView):
    template_name = 'app/contact.html'
    form_class = ContactForm


# user profile
@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    def get(self, request):
        form = UserEditForm(instance=request.user)
        return render(request, 'app/profile.html', {'form':form})

    def post(self, request):
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated !!!')
        return redirect('/profile/')


# blog create view
@login_required
def BlogCreateView(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            photo = form.cleaned_data['photo']
            description = form.cleaned_data['description']
            blog = Blog(usr=request.user, title=title, category=category, photo=photo, description=description)
            blog.save()
            print('form valideted!!!')
            messages.success(request, 'Blog is successfully created!!!')
            return redirect('/')
        else:
            messages.info(request, 'Somthing is wrong!!!')
            return redirect('/blogcreate/')
    else:
        form = BlogForm()
        return render(request, 'app/blogcreate.html', {'form':form})


# signup view
def userSignupView(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'You have been successfully registered!!!')
                return redirect('/signup/')
        else:
            form = SignupForm()
        return render(request, 'app/signup.html', {'form':form})
    else:
        return redirect('/')

# login view
def UserLoginVie(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Successfully Logedin!!!')
                    return redirect('/')
            else:
                form = LoginForm()
            return render(request, 'app/login.html', {'form':form})
        else:
            form = LoginForm()
            return render(request, 'app/login.html', {'form':form})
    else:
        return redirect('/')   

# password change view
@method_decorator(login_required, name='dispatch')
class PassChangeView(View):
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, 'app/profile.html', {'form':form})
    
    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your Password Has Been Successfully Changed!!!')
        return redirect('/profile/')


# user logout view
def userLogout(request):
    logout(request)
    return redirect('/accounts/login/')


