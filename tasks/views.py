from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login  # Crea la cookie
from django.contrib.auth import logout, authenticate
from django.db import IntegrityError  # Errores de integridad de las BBDD
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                HttpResponse("User created succesfully")
                login(request, user)
                return redirect('/tasks')
            except IntegrityError as iex:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': f'ERROR -> USER ALREADY EXISTS {iex}'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'PASSWORDS DO NOT MATCH'
        })

@login_required
def tasks(request):
    try:
        many_tasks = Task.objects.filter(user=request.user, task_completed__isnull=True)
        return render(request, 'tasks.html', {
            'tasks': many_tasks
        })
    except Exception as ex:
        return f'ERROR -> {ex}'

@login_required
def task_details(request, task_id):
    try:
        if request.method == 'GET':
            one_task = get_object_or_404(Task, id=task_id, user=request.user)
            form_task = TaskForm(instance=one_task)
            return render(request, 'task_details.html', {
                'task': one_task,
                'form': form_task
            })
        else:
            print(request.POST)
            one_task = get_object_or_404(Task, id=task_id, user=request.user)
            updated_form = TaskForm(request.POST, instance=one_task)
            updated_form.save()
            return redirect('tasks')
    except ValueError as ve:
        return render(request, 'task_details.html', {
            'error': f'Error -> {ve}'
        })

@login_required
def task_completed(request, task_id):
    try:
        task = get_object_or_404(Task, id=task_id, user=request.user)
        if request.method == 'POST':
            task.task_completed = timezone.now()
            task.save()
            return redirect('tasks')
        else:
            return render('tasks', {
                'task': task })
    except Exception as ex:
        return render(request, 'task_details.html', {
            'error': f'ERROR = {ex}'
        })

@login_required
def task_deleted(request, task_id):
    try:
        task = get_object_or_404(Task, id=task_id, user=request.user)
        if request.method == 'POST':
            task.delete()
            # task.save()
            return redirect('tasks')
        else:
            return render('tasks', {
                'tasks': tasks})
    except Exception as ex:
        return render(request, 'task_details.html', {
            'error': f'ERROR = {ex}'
        })

@login_required
def list_completed_task(request):
    try:
        tasks = Task.objects.filter(user=request.user, task_completed__isnull=False).order_by('task_completed')
        return render(request, 'tasks.html', {
            'tasks': tasks
        })
    except Exception as ex:
        return render('tasks', {
            'error': f'ERROR = {ex}'
        })

@login_required
def signout(request):
    try:
        logout(request)
        return redirect('home')
    except Exception as ex:
        return f'ERROR -> {ex}'

def signin(request):
    try:
        if request.method == 'GET':
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
            })
        else:
            validate_user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if validate_user is None:
                return render(request, 'signin.html', {
                    'form': AuthenticationForm,
                    'error': 'USERNAME OR PASSWORD IS INCORRECT'
                })
            else:
                login(request, validate_user)
                return redirect('tasks')
    except Exception as ex:
        return f'ERROR -> {ex}'

@login_required
def create_task(request):
    try:
        if request.method == 'GET':
            return render(request, 'create_task.html', {
                'form': TaskForm
            })
        else:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
    except ValueError as value_error:
        return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': f'ERROR -> {value_error}'
            })