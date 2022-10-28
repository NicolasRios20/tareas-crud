from django.utils import timezone
from django.db import IntegrityError
from django.forms import PasswordInput
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from .forms import TareaForm
from .models import tarea
from django.contrib.auth.decorators import login_required


# Create your views here.
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
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tareas')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'el usuario ya existe'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'contrasenas no coinciden'
        })

@login_required
def tasks(request):
    tareas = tarea.objects.filter(user =request.user, fechacumplida__isnull = True)
    return render(request, 'tareas.html',{'tareas': tareas})

@login_required
def tasksCompleto(request):
    tareas = tarea.objects.filter(user =request.user, fechacumplida__isnull = False).order_by('-fechacumplida')
    return render(request, 'tareas.html',{'tareas': tareas})


@login_required
def crearTareas(request):
    if request.method == "GET":
        return render(request, 'creartareas.html', {"form": TareaForm})
    else:
        try:
            form = TareaForm(request.POST)
            new_tarea = form.save(commit=False)
            new_tarea.user = request.user
            new_tarea.save()
            return redirect('tareas')
        except ValueError:
            return render(request, 'creartareas.html', {"form": TareaForm, "error": "Error al crear tarea."})


@login_required
def detalleTarea(request, idt):
    if request.method == 'GET':
        tareas = get_object_or_404(tarea, pk = idt, user = request.user)
        form = TareaForm(instance=tareas)
        return render(request, 'detalletarea.html',{'tarea': tareas, 'form':form})
    else:
        try:
            tareas = get_object_or_404(tarea, pk = idt, user = request.user)
            form = TareaForm(request.POST, instance=tareas)
            form.save()
            return redirect('tareas')
        except:
            return render(request, 'detalletarea', {'tarea': tareas, 'form':form, 'error': 'Error al actualizar.'})


@login_required
def completo(request, idt):
    tareas = get_object_or_404(tarea, pk=idt, user=request.user)
    if request.method == 'POST':
        tareas.fechacumplida = timezone.now()
        tareas.save()
        return redirect('tareas')


@login_required
def borrar(request, idt):
    tareas = get_object_or_404(tarea, pk=idt, user=request.user)
    if request.method == 'POST':
        tareas.delete()
        return redirect('tareas')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('tareas')
