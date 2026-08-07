from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.cache import never_cache
from .forms import CustomUserCreationForm


def obtener_rol_usuario(user):
    if user.is_superuser or user.is_staff:
        return 'admin'
    if getattr(user, 'is_cuadrilla', False):
        return 'cuadrilla'
    if user.groups.filter(name__icontains='cuadrilla').exists():
        return 'cuadrilla'
    if user.groups.filter(name__icontains='soporte').exists():
        return 'soporte'
    return 'bodega'


def redireccion_por_rol(user):
    rol = obtener_rol_usuario(user)
    if rol == 'admin':
        return '/dashboard/'
    if rol == 'cuadrilla':
        return '/asignaciones/'
    if rol == 'soporte':
        return '/menu/'
    return '/productos/'


@ensure_csrf_cookie
@never_cache
@csrf_protect
def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(redireccion_por_rol(user))
        messages.error(request, 'Usuario o contrasena incorrectos.')
    return render(request, 'login.html')


def menu(request):
    if not request.user.is_authenticated:
        return redirect('/')
    return render(request, 'menu.html', {
        'rol': obtener_rol_usuario(request.user)
    })


def cerrar_sesion(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('base')  # Cambia 'base' por tu vista principal
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/register.html', {'form': form})

def login_view(request):
    return login_usuario(request)
