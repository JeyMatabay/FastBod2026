from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def _obtener_rol(user):
    if user.is_superuser or user.is_staff:
        return 'admin'
    if getattr(user, 'is_cuadrilla', False):
        return 'cuadrilla'
    if user.groups.filter(name__icontains='cuadrilla').exists():
        return 'cuadrilla'
    if user.groups.filter(name__icontains='soporte').exists():
        return 'soporte'
    return 'bodega'


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/')

            rol = _obtener_rol(request.user)
            if rol not in roles:
                messages.error(request, 'No tiene permisos para acceder a esta seccion.')
                return redirect('/menu/')

            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator
