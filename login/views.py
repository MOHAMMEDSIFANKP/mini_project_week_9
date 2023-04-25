from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login,logout as dj_logout
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .models import card

# Login page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashbords')
        else:
            return redirect('home')
    if request.method =="POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user =authenticate(username=uname,password=pwd)

# Validation
        if uname.strip() == '' or pwd.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('login')
        if user is not None:
            dj_login(request, user)
            if request.user.is_superuser:
                return redirect('dashbords')
            else:
               return redirect('home')
        else:
            messages.error(request, "Your usename or password is Incorrect")
            return redirect('login')
    return render(request,'index.html')

# Signup
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.method == "POST":
        uname = request.POST['username']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        pwd = request.POST['password1']
        pwd2 = request.POST['password2']

# Validation
        if uname.strip() == '' or pwd.strip() == '' or pwd2.strip() =='' or fname.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('signup')
        
        if pwd!=pwd2:
            messages.error(request,"password dosen't Match")
            return redirect('signup')
        
        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        
        user = User.objects.create_user(username=uname,first_name=fname,last_name=lname,email=email,password=pwd)
        user.save()
        messages.success(request, 'User created successfully')
        return redirect('login')

    return render(request,'signup.html')

# Home
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def home(request):

    dict_docs={
        'cards':card.objects.all()
    }
    return render(request,'home.html',dict_docs)

# Logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def logout(request):
    dj_logout(request)
    return redirect('login')