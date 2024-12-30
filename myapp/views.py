from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate,login
from django.db.models import Q
from django.contrib import messages
from .decorators import hr_or_admin_required
from .models import User,Employee

def home(request):
    if request.user.is_authenticated:
        employee = Employee.objects.filter(user = request.user).first()
        return render(request, 'home.html',{'employee': employee})
    else:
        return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials !")
            return redirect('/login')
    return render(request,'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        designation = request.POST.get('designation')
        if password1 != password2:
            messages.info(request,"Passwords don't match !")
            return redirect('signup')
        elif User.objects.filter(email = email).exists():
            messages.info(request, "Email already taken !")
            return redirect('signup')
        elif User.objects.filter(username = username).exists():
            messages.info(request, "Username already taken !")
            return redirect('signup')
        else:
            user = User.objects.create_user(username = username,email = email, password = password1)
            user.save()
            Employee.objects.create(user = user,designation=designation)
            return redirect('login')
    else:
        return render(request, 'register.html') 

@login_required(login_url='/users/login')
def user_logout(request):
    logout(request)
    return redirect('/')   

@hr_or_admin_required
def employees(request):
    employee = Employee.objects.filter(user = request.user).first()
    if employee.designation == 'A':
        employees = Employee.objects.filter(Q(designation__in=['H', 'E']) | Q(user=request.user)).exclude(user = request.user)
    else:
        employees = Employee.objects.filter(designation='E')
    return render(request,'employees.html',{ 'employees' : employees,'employee':employee })

def employee(request,name):
    print(name)
    employee = Employee.objects.filter(user__username = name).first()
    return render(request,'employee.html',{ 'employee': employee })