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
    if request.method=='POST':
        username=request.POST.get('username') #AS IN HTML NAME FIELD
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        if len(password) < 3 :
            messages.error(request,'Password must be atleast 3 characters')
            return redirect('register')
        
        # Restrict if user already exists
        get_users_by_username=User.objects.filter(username=username) #match username with database stored username
        if get_users_by_username:
            messages.error(request,'Error , username already exists')
            return redirect('register')
        
        newUser=User.objects.create_user(username=username,email=email,password=password) #create and save in database
        newUser.save()
        messages.success(request,'User successfully created.')
        
    return render(request,'todoapp/register.html',{})

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