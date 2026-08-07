def _obtener_rol(user):
    if not user.is_authenticated:
        return ''

    if user.is_superuser or user.is_staff:
        return 'admin'

    if getattr(user, 'is_cuadrilla', False):
        return 'cuadrilla'

    if user.groups.filter(name__icontains='cuadrilla').exists():
        return 'cuadrilla'

    if user.groups.filter(name__icontains='soporte').exists():
        return 'soporte'

    return 'bodega'


def rol_usuario_context(request):
    return {
        'rol_usuario': _obtener_rol(request.user)
    }
