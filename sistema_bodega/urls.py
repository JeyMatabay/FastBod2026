"""
URL configuration for sistema_bodega project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cuadrillas.views import asignar_material, lista_asignaciones
from usuarios.views import login_usuario, menu, cerrar_sesion
from inventario.views import dashboard, recursos_sistema, recursos_sistema_data
from inventario.views import inventario_modelos
from inventario.views import reporte_inventario_pdf
from inventario.views import buscar_producto
from inventario.views import detalle_producto
from inventario.views import (
    lista_productos,
    crear_producto,
    editar_producto,
    eliminar_producto,
    lista_productos_construccion,
    crear_producto_construccion,
    editar_producto_construccion,
    eliminar_producto_construccion,
    lista_proveedores,
    crear_proveedor,
    editar_proveedor,
    eliminar_proveedor,
)

from cuadrillas.views import (
    lista_cuadrillas,
    crear_cuadrilla,
    editar_cuadrilla,
    eliminar_cuadrilla,
    lista_soportes,
    crear_soporte,
    editar_soporte,
    eliminar_soporte,
    asignar_material,
    lista_asignaciones,
    mis_asignaciones,
    dar_baja_material,
    devolver_a_stock,
    historial_bajas,
    historial_bajas_construccion,
    reporte_historial_bajas_construccion_excel,
    retirar_cliente_baja,
    purgar_historial_bajas,
    reporte_historial_bajas_excel,
    equipos_retirados,
    reutilizar_equipo_retirado,
    reutilizar_equipo_retirado_manual,
    importar_clientes,
)

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', login_usuario),
    path('menu/', menu),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('productos/', lista_productos),
    path('crear_producto/', crear_producto),
    path('producto/<int:id>/', detalle_producto),
    path('editar_producto/<int:id>/', editar_producto),
    path('eliminar_producto/<int:id>/', eliminar_producto),
    path('productos-construccion/', lista_productos_construccion, name='lista_productos_construccion'),
    path('crear_producto_construccion/', crear_producto_construccion, name='crear_producto_construccion'),
    path('producto-construccion/<int:id>/', detalle_producto, name='detalle_producto_construccion'),
    path('editar_producto_construccion/<int:id>/', editar_producto_construccion, name='editar_producto_construccion'),
    path('eliminar_producto_construccion/<int:id>/', eliminar_producto_construccion, name='eliminar_producto_construccion'),
    path('cuadrillas/', name='lista_cuadrillas', view=lista_cuadrillas),
    path('crear_cuadrilla/', crear_cuadrilla),
    path('editar_cuadrilla/<int:id>/', editar_cuadrilla),
    path('eliminar_cuadrilla/<int:id>/', eliminar_cuadrilla),
    path('soportes/', name='lista_soportes', view=lista_soportes),
    path('crear_soporte/', crear_soporte),
    path('editar_soporte/<int:id>/', editar_soporte),
    path('eliminar_soporte/<int:id>/', eliminar_soporte),
    path('asignar_material/', name='asignar_material', view=asignar_material),
    path('asignaciones/', name='lista_asignaciones', view=lista_asignaciones),
    path('baja_material/<int:asignacion_id>/', dar_baja_material, name='dar_baja_material'),
    path('devolver_stock/<int:asignacion_id>/', devolver_a_stock, name='devolver_a_stock'),
    path('historial_bajas/', historial_bajas, name='historial_bajas'),
    path('historial_bajas_construccion/', historial_bajas_construccion, name='historial_bajas_construccion'),
    path('historial_bajas_construccion/excel/', reporte_historial_bajas_construccion_excel, name='reporte_historial_bajas_construccion_excel'),
    path('equipos_retirados/', equipos_retirados, name='equipos_retirados'),
    path('equipos_retirados/reutilizar/<int:baja_id>/', reutilizar_equipo_retirado, name='reutilizar_equipo_retirado'),
    path('equipos_retirados/reutilizar-retirado/<int:retiro_id>/', reutilizar_equipo_retirado_manual, name='reutilizar_equipo_retirado_manual'),
    path('historial_bajas/retirar/<int:baja_id>/', retirar_cliente_baja, name='retirar_cliente_baja'),
    path('historial_bajas/purgar/', purgar_historial_bajas, name='purgar_historial_bajas'),
    path('reporte_historial_bajas_excel/', reporte_historial_bajas_excel, name='reporte_historial_bajas_excel'),
    path('importar_clientes/', importar_clientes, name='importar_clientes'),
    path('dashboard/', dashboard),
    path('recursos-sistema/', recursos_sistema, name='recursos_sistema'),
    path('recursos-sistema/data/', recursos_sistema_data, name='recursos_sistema_data'),
    path('inventario_modelos/', inventario_modelos),
    path('buscar_producto/', buscar_producto),
    path('reporte_inventario/', reporte_inventario_pdf),
    path('mis-materiales/', mis_asignaciones, name='mis_asignaciones'),
    path('proveedores/', lista_proveedores, name='lista_proveedores'),
    path('proveedores/nuevo/', crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:id>/', editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:id>/', eliminar_proveedor, name='eliminar_proveedor'),
]
