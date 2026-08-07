from django.contrib import admin
from .models import Categoria, Marca, ModeloEquipo, TipoFibra, Producto

from .models import (
    Categoria,
    Marca,
    ModeloEquipo,
    TipoFibra,
    Producto
)

admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(ModeloEquipo)
admin.site.register(TipoFibra)
admin.site.register(Producto)
