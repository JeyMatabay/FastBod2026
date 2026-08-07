from django.db import models
from django.utils import timezone


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    ruc = models.CharField(max_length=20, blank=True, default='')
    telefono = models.CharField(max_length=30, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    direccion = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class ModeloEquipo(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.marca} - {self.nombre}"


class TipoFibra(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Producto(models.Model):

    BODEGA_GENERAL = 'GENERAL'
    BODEGA_CONSTRUCCION = 'CONSTRUCCION'
    BODEGA_CHOICES = [
        (BODEGA_GENERAL, 'General'),
        (BODEGA_CONSTRUCCION, 'Construccion'),
    ]

    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    mac = models.CharField(max_length=50, null=True, blank=True)
    serial = models.CharField(max_length=100, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True, blank=True)
    modelo = models.ForeignKey(ModeloEquipo, on_delete=models.CASCADE, null=True, blank=True)
    tipo_fibra = models.ForeignKey(TipoFibra, on_delete=models.CASCADE, null=True, blank=True)
    hilo = models.IntegerField(null=True, blank=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.IntegerField(default=0)
    metraje = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bodega = models.CharField(max_length=20, choices=BODEGA_CHOICES, default=BODEGA_GENERAL)
    fecha_ingreso = models.DateField(default=timezone.now)
    fecha_pedido_factura = models.DateField(null=True, blank=True)
    stock_minimo = models.IntegerField(default=5)

    def stock_bajo(self):
        return self.stock <= self.stock_minimo
    def __str__(self):
        return f"{self.nombre} - {self.marca.nombre if self.marca else 'Sin marca'}"
    
class MovimientoInventario(models.Model):

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    TIPO_MOVIMIENTO = [
    ('ENTRADA', 'Entrada'),
    ('SALIDA', 'Salida'),
    ('ASIGNACION', 'Asignación'),
]

    tipo = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto} {self.tipo}"


class DetalleIdentificador(models.Model):

    TIPO_CHOICES = [
        ('SERIAL', 'Serial'),
        ('MAC', 'MAC'),
        ('CABLE', 'Cable'),
    ]

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='identificadores'
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    codigo_individual = models.CharField(max_length=50, null=True, blank=True)
    valor = models.CharField(max_length=120)
    metraje = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('producto', 'tipo', 'valor')

    def __str__(self):
        return f"{self.producto.codigo} - {self.tipo}: {self.valor}"