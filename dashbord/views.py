from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def dashbords(request):
    if request.method == 'POST':         
        searched = request.POST['searching']        
        searchresult = User.objects.filter(username__contains=searched)           
        return render(request,'search.html',{'result':searchresult})            
    else:
        users_data = User.objects.all().order_by('id')
        return render(request,'dashbord.html',{'users': users_data})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def create(request):
    if request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        uname = request.POST['username']
        email = request.POST['email']
        pwd1 = request.POST['password1']
        pwd2 = request.POST['password2']
        try:
            is_super = request.POST['is_superuser']
        except: 
            is_super = False
# Validation
        if fname.strip() == '' and uname.strip() == '' and pwd1.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('create')   
        if pwd1 != pwd2:
            messages.error(request, "Password dosen't match")
            return redirect('create')
        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists')
            return redirect('create')
        user = User.objects.create_user(first_name=fname,last_name=lname,username=uname,email=email,password=pwd1)  
        if is_super:
            user.is_superuser = True
        user.save()
        messages.success(request, 'User created successfully')
        return redirect('dashbords')
    return render(request,'createuser.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def edit(request,user_id):
    if request.method =='POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        uname = request.POST['username']
        email = request.POST['email']
        pwd = request.POST['password']
        if fname == '' and uname == '' and pwd == '':
            messages.error(request, "Fields can't be blank")
            return redirect('edit', user_id)
        
        # Validation
        if fname.strip() == '' or uname.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('edit', user_id)   
        
        user = User.objects.get(id=user_id)
        user.first_name = fname
        user.last_name = lname
        user.username = uname
        user.email = email
        if pwd.strip() =='':
            user.password = user.password
        else:
            user.set_password(pwd)
        messages.success(request, 'User updated successfully')
        user.save()
        # return redirect('dashbords')
    user = User.objects.get(id=user_id)
    return render(request, 'edituser.html',{'user': user})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def delete(request,user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('dashbords')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def search(request):
    if request.method == 'POST':            
        searched = request.POST['searching']        
        searchresult = User.objects.filter(username__contains=searched)           
        return render(request,'search.html',{'result':searchresult})  
    else:
        messages.error(request,'NOt found')

    return render(request,'search.html')
        