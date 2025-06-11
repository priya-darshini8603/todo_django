import random
import re
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task').strip()  # remove leading/trailing whitespace

        if not task:
            messages.error(request, "Task cannot be empty.")
        elif todo.objects.filter(user=request.user, todo_name__iexact=task).exists():
            messages.error(request, "Task already in the list.")
        else:
            new_todo = todo(user=request.user, todo_name=task)
            new_todo.save()
            messages.success(request, "Task added successfully.")
    
    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos
    }
    return render(request, 'todoapp/todo.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('register')

        if not re.search(r'[A-Z]', password):
            messages.error(request, 'Password must contain at least one uppercase letter.')
            return redirect('register')

        if not re.search(r'[a-z]', password):
            messages.error(request, 'Password must contain at least one lowercase letter.')
            return redirect('register')

        if not re.search(r'[0-9]', password):
            messages.error(request, 'Password must contain at least one digit.')
            return redirect('register')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.error(request, 'Password must contain at least one special character.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        newUser = User.objects.create_user(username=username, email=email, password=password)
        newUser.save()
        messages.success(request, 'User successfully created.')
        return redirect('login')  

    return render(request, 'todoapp/register.html')

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        validate_user = authenticate(username=username, password=password)
        
        if validate_user is not None:  
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request,'Error , Wrong user details or username does not exists')
            return redirect('login')
        
    return render(request,'todoapp/login.html',{})

def LogoutView(request):
    logout(request)
    return redirect('login')

@login_required
def DeleteTask(request,name):
    get_todo=todo.objects.get(user=request.user,todo_name=name)
    get_todo.delete()
    return redirect('home-page')

@login_required
def Update(request,name):
    get_todo=todo.objects.get(user=request.user,todo_name=name)
    get_todo.status=True
    get_todo.save()
    return redirect('home-page')

otp_store = {}

def request_otp_view(request): 
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            otp_store[email] = otp

            email_msg = EmailMessage(
                subject='🔒 Your OTP for Password Reset',
                body=f'Your OTP is: {otp}',
                from_email='darshini.devi8603@gmail.com',
                to=[email]
            )
            email_msg.content_subtype = 'plain'
            email_msg.encoding = 'utf-8'
            email_msg.send(fail_silently=False)

            messages.success(request, 'OTP sent to your email.')
            return render(request, 'todoapp/verify_otp.html', {'email': email})
        except User.DoesNotExist:
            messages.error(request, 'No account associated with that email.')
            return redirect('request_otp')

    return render(request, 'todoapp/reset_password_request.html')


def verify_otp_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        entered_otp = request.POST['otp']
        new_password = request.POST['new_password']

        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'todoapp/verify_otp.html', {'email': email})

        if not re.search(r'[A-Z]', new_password):
            messages.error(request, 'Password must contain at least one uppercase letter.')
            return render(request, 'todoapp/verify_otp.html', {'email': email})

        if not re.search(r'[a-z]', new_password):
            messages.error(request, 'Password must contain at least one lowercase letter.')
            return render(request, 'todoapp/verify_otp.html', {'email': email})

        if not re.search(r'[0-9]', new_password):
            messages.error(request, 'Password must contain at least one digit.')
            return render(request, 'todoapp/verify_otp.html', {'email': email})

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
            messages.error(request, 'Password must contain at least one special character.')
            return render(request, 'todoapp/verify_otp.html', {'email': email})

        original_otp = otp_store.get(email)
        if original_otp == entered_otp:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                otp_store.pop(email, None)
                messages.success(request, 'Password reset successfully.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
        else:
            messages.error(request, 'Invalid OTP.')
            return render(request, 'todoapp/verify_otp.html', {'email': email})

    return redirect('request_otp')
