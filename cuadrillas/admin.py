from django.contrib import admin
from .models import Cuadrilla, SoporteTecnico, AsignacionMaterial, BajaMaterial

admin.site.register(Cuadrilla)
admin.site.register(SoporteTecnico)
admin.site.register(AsignacionMaterial)
admin.site.register(BajaMaterial)