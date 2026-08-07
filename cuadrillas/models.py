from django.db import models
from django.conf import settings
from django.db.models.functions import Lower
from django.utils import timezone
from inventario.models import Producto
from inventario.models import DetalleIdentificador

class Cuadrilla(models.Model):

    nombre = models.CharField(max_length=100)
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nombre


class SoporteTecnico(models.Model):

    nombre = models.CharField(max_length=100)
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nombre


class Cliente(models.Model):

    nombre = models.CharField(max_length=150, unique=True)
    ct = models.CharField(max_length=40, blank=True, default='')
    cedula = models.CharField(max_length=30, blank=True, default='')

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower('nombre'), name='uq_cliente_nombre_ci'),
        ]

    def __str__(self):
        return self.nombre


class AsignacionMaterial(models.Model):

    cuadrilla = models.ForeignKey(Cuadrilla, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    metraje = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    usuario_registro = models.CharField(max_length=150, blank=True, default='')
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto} - {self.cuadrilla}"
    
class BajaMaterial(models.Model):
    TIPO_USO_CHOICES = [
        ('Instalacion', 'Instalacion'),
        ('Cambio de domicilio', 'Cambio de domicilio'),
        ('Cambio', 'Cambio'),
        ('Migracion', 'Migracion'),
        ('Soporte', 'Soporte'),
        ('DANO', 'DAÑO'),
        ('CONSTRUCCION', 'CONSTRUCCION'),
    ]

    asignacion = models.ForeignKey(AsignacionMaterial, on_delete=models.CASCADE, related_name='bajas')
    cantidad = models.IntegerField()
    metraje = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    punta_inicial = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    punta_final = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario_registro = models.CharField(max_length=150, blank=True, default='')
    tipo_uso = models.CharField(max_length=20, choices=TIPO_USO_CHOICES, blank=True, default='')
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='bajas_material')
    cliente_nombre = models.CharField(max_length=150, blank=True, default='')
    producto_nombre = models.CharField(max_length=120, blank=True, default='')
    producto_codigo = models.CharField(max_length=50, blank=True, default='')
    codigo_bobina = models.CharField(max_length=80, blank=True, default='')
    es_equipo_activo = models.BooleanField(default=False)
    observacion = models.TextField(blank=True, default='')
    detalle_mac = models.TextField(blank=True, default='')
    detalle_serial = models.TextField(blank=True, default='')
    serial_mac_retirado = models.CharField(max_length=120, blank=True, default='')
    codigo_retirado = models.CharField(max_length=80, blank=True, default='')
    categoria_retirado = models.CharField(max_length=100, blank=True, default='')
    marca_retirado = models.CharField(max_length=100, blank=True, default='')
    modelo_retirado = models.CharField(max_length=100, blank=True, default='')
    estado_equipo = models.CharField(max_length=20, blank=True, default='', choices=[('Nuevo', 'Nuevo'), ('Utilizado', 'Utilizado')])
    retirado = models.BooleanField(default=False)
    fecha_retirado = models.DateTimeField(null=True, blank=True)
    reutilizado = models.BooleanField(default=False)
    fecha_reutilizado = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.asignacion.producto} - {self.cantidad}"


class AsignacionIdentificador(models.Model):
    asignacion = models.ForeignKey(
        AsignacionMaterial,
        on_delete=models.CASCADE,
        related_name='identificadores_asignados'
    )
    identificador = models.OneToOneField(
        DetalleIdentificador,
        on_delete=models.CASCADE,
        related_name='asignacion_detalle'
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asignacion.cuadrilla} - {self.identificador.valor}"


class BajaIdentificador(models.Model):
    baja = models.ForeignKey(BajaMaterial, on_delete=models.CASCADE, related_name='identificadores_baja')
    identificador = models.ForeignKey(DetalleIdentificador, on_delete=models.CASCADE)

    def __str__(self):
        return f"Baja {self.baja.id} - {self.identificador.valor}"


class EquipoRetiradoManual(models.Model):
    ORIGEN_CHOICES = [
        ('Cambio', 'Cambio'),
        ('Retirado', 'Retirado'),
    ]

    fecha = models.DateTimeField(default=timezone.now)
    origen = models.CharField(max_length=20, choices=ORIGEN_CHOICES, default='Retirado')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True, related_name='retiros_manual')
    producto_nombre = models.CharField(max_length=120, blank=True, default='')
    producto_codigo = models.CharField(max_length=50, blank=True, default='')
    proveedor_nombre = models.CharField(max_length=150, blank=True, default='')
    cuadrilla_nombre = models.CharField(max_length=100, blank=True, default='')
    cliente_nombre = models.CharField(max_length=150, blank=True, default='')
    ct_cliente = models.CharField(max_length=40, blank=True, default='')
    detalle_cambio = models.TextField(blank=True, default='')
    categoria_retirado = models.CharField(max_length=100, blank=True, default='')
    marca_retirado = models.CharField(max_length=100, blank=True, default='')
    modelo_retirado = models.CharField(max_length=100, blank=True, default='')
    usuario_registro = models.CharField(max_length=150, blank=True, default='')
    serial_mac_retirado = models.CharField(max_length=120, blank=True, default='')
    codigo_retirado = models.CharField(max_length=80, blank=True, default='')
    cantidad = models.IntegerField(default=1)
    metraje = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reutilizado = models.BooleanField(default=False)
    fecha_reutilizado = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.producto_nombre or self.producto_codigo or 'Retiro'} - {self.fecha}"