from django import forms
from decimal import Decimal
from .models import Producto, Marca, ModeloEquipo, TipoFibra, DetalleIdentificador, Proveedor, Categoria


def es_categoria_activa(nombre_categoria):
    nombre = (nombre_categoria or '').lower().strip()
    palabras_activo = ['activo', 'onu', 'onue', 'ont', 'router', 'routher', 'modem', 'ktv']
    return any(p in nombre for p in palabras_activo)


def es_categoria_fibra(nombre_categoria):
    nombre = (nombre_categoria or '').lower().strip()
    palabras_fibra = ['fibra', 'cable', 'drop', 'adss', 'fo', 'hilo', 'utp', 'coaxial']
    return any(p in nombre for p in palabras_fibra)


def es_categoria_con_metraje(nombre_categoria):
    nombre = (nombre_categoria or '').lower().strip()
    palabras_metraje = ['fibra', 'utp', 'coaxial', 'adss']
    return any(p in nombre for p in palabras_metraje)


def es_categoria_fibra_optica(nombre_categoria):
    nombre = (nombre_categoria or '').lower().strip()
    palabras_opticas = ['fibra', 'fo', 'adss', 'hilo']
    return any(p in nombre for p in palabras_opticas)


def es_categoria_material(nombre_categoria):
    nombre = (nombre_categoria or '').lower().strip()
    return 'material' in nombre


def es_categoria_codigo_unico(nombre_categoria):
    nombre = (nombre_categoria or '').lower().strip()
    palabras = ['caja', 'cajas', 'manga', 'mangas']
    return any(p in nombre for p in palabras)

HILO_CHOICES = [
    (2, '2'),
    (6, '6'),
    (8, '8'),
    (12, '12'),
    (24, '24'),
]

class ProductoForm(forms.ModelForm):

    metraje_por_bobina = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        max_digits=12,
        label='Metraje por bobina',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01'})
    )

    nueva_marca = forms.CharField(
        required=False,
        label='Nueva marca',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Huawei'})
    )

    nuevo_modelo = forms.CharField(
        required=False,
        label='Nuevo modelo',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: C80'})
    )

    nuevo_tipo_fibra = forms.CharField(
        required=False,
        label='Nuevo tipo de fibra',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: ADSS'})
    )

    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(),
        required=False,
        label='Proveedor',
        empty_label='-- Sin proveedor --',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    nuevo_proveedor = forms.CharField(
        required=False,
        label='Nuevo proveedor',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'})
    )

    nueva_categoria = forms.CharField(
        required=False,
        label='Nueva categoria',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Nueva categoria'}),
    )

    class Meta:

        model = Producto

        fields = [
            'nombre',
            'categoria',
            'codigo',
            'mac',
            'serial',
            'marca',
            'modelo',
            'tipo_fibra',
            'hilo',
            'stock',
            'metraje',
            'fecha_pedido_factura',
            'proveedor',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'mac': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: A1:B2:C3:D4:E5:F6'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: SN12345678'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'modelo': forms.Select(attrs={'class': 'form-control'}),
            'tipo_fibra': forms.Select(attrs={'class': 'form-control'}),
            'hilo': forms.Select(attrs={'class': 'form-control'}, choices=[('', '---------')] + HILO_CHOICES),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'metraje': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'min': 0, 'step': '0.01'}),
            'fecha_pedido_factura': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].required = False
        self.fields['metraje'].required = False

        categoria_nombre = self.instance.categoria.nombre if getattr(self.instance, 'categoria_id', None) else ''
        if self.instance and self.instance.pk and es_categoria_con_metraje(categoria_nombre):
            stock = self.instance.stock or 0
            if stock > 0:
                self.fields['metraje_por_bobina'].initial = self.instance.metraje / Decimal(str(stock))
            else:
                self.fields['metraje_por_bobina'].initial = self.instance.metraje

    def _get_or_create_by_name(self, model_class, nombre):
        nombre = (nombre or '').strip()
        if not nombre:
            return None
        existente = model_class.objects.filter(nombre__iexact=nombre).first()
        if existente:
            return existente
        return model_class.objects.create(nombre=nombre)

    def clean(self):
        cleaned_data = super().clean()

        categoria = cleaned_data.get('categoria')
        nueva_categoria = (cleaned_data.get('nueva_categoria') or '').strip()
        mac = (cleaned_data.get('mac') or '').strip()
        serial = (cleaned_data.get('serial') or '').strip()
        codigo = (cleaned_data.get('codigo') or '').strip()

        if nueva_categoria:
            categoria = self._get_or_create_by_name(Categoria, nueva_categoria)
            cleaned_data['categoria'] = categoria

        if not categoria:
            self.add_error('categoria', 'Seleccione una categoria o cree una nueva categoria.')
            return cleaned_data

        categoria_nombre = (categoria.nombre if categoria else '')
        es_activo = es_categoria_activa(categoria_nombre)
        es_material = es_categoria_material(categoria_nombre)

        # Valida campos requeridos para equipos activos
        if es_activo:
            if not codigo:
                self.add_error('codigo', 'Codigo es obligatorio para equipos activos.')
            if not mac:
                self.add_error('mac', 'MAC es obligatoria para equipos activos.')
            if not serial:
                self.add_error('serial', 'Serial de ingreso es obligatorio para equipos activos.')

        if es_material:
            if not codigo:
                self.add_error('codigo', 'Codigo es obligatorio para material.')
            stock = cleaned_data.get('stock') or 0
            if stock <= 0:
                self.add_error('stock', 'Cantidad debe ser mayor que 0 para material.')

            # Material se controla solo por codigo y cantidad.
            cleaned_data['mac'] = ''
            cleaned_data['serial'] = ''
            cleaned_data['marca'] = None
            cleaned_data['modelo'] = None
            cleaned_data['tipo_fibra'] = None
            cleaned_data['hilo'] = None
            cleaned_data['metraje_por_bobina'] = Decimal('0')

        if codigo:
            codigo_qs = Producto.objects.filter(codigo__iexact=codigo)
            if self.instance and self.instance.pk:
                codigo_qs = codigo_qs.exclude(pk=self.instance.pk)
            if codigo_qs.exists():
                self.add_error('codigo', 'Este codigo ya existe. Debe ser unico.')

        if es_categoria_con_metraje(categoria_nombre):
            metraje_por_bobina = cleaned_data.get('metraje_por_bobina') or Decimal('0')
            stock = cleaned_data.get('stock') or 0
            cleaned_data['metraje'] = Decimal(str(metraje_por_bobina)) * Decimal(str(stock))
        else:
            cleaned_data['metraje'] = Decimal('0')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data.get('categoria'):
            instance.categoria = self.cleaned_data.get('categoria')

        nueva_marca = (self.cleaned_data.get('nueva_marca') or '').strip()
        nuevo_modelo = (self.cleaned_data.get('nuevo_modelo') or '').strip()
        nuevo_tipo_fibra = (self.cleaned_data.get('nuevo_tipo_fibra') or '').strip()

        marca = self.cleaned_data.get('marca')
        if nueva_marca:
            marca = self._get_or_create_by_name(Marca, nueva_marca)
            instance.marca = marca

        if nuevo_modelo:
            if not marca:
                marca = instance.marca
            if marca:
                modelo_existente = ModeloEquipo.objects.filter(
                    marca=marca,
                    nombre__iexact=nuevo_modelo
                ).first()
                if modelo_existente:
                    instance.modelo = modelo_existente
                else:
                    instance.modelo = ModeloEquipo.objects.create(marca=marca, nombre=nuevo_modelo)

        if nuevo_tipo_fibra:
            instance.tipo_fibra = self._get_or_create_by_name(TipoFibra, nuevo_tipo_fibra)

        nuevo_proveedor = (self.cleaned_data.get('nuevo_proveedor') or '').strip()
        if nuevo_proveedor:
            prov = Proveedor.objects.filter(nombre__iexact=nuevo_proveedor).first()
            if not prov:
                prov = Proveedor.objects.create(nombre=nuevo_proveedor)
            instance.proveedor = prov

        categoria_nombre = instance.categoria.nombre if instance.categoria else ''

        if es_categoria_material(categoria_nombre):
            instance.mac = ''
            instance.serial = ''
            instance.marca = None
            instance.modelo = None
            instance.tipo_fibra = None
            instance.hilo = None

        if not es_categoria_con_metraje(categoria_nombre):
            instance.metraje = 0

        if commit:
            instance.save()
        return instance


class DetalleIdentificadorForm(forms.ModelForm):

    metraje = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        max_digits=12,
        initial=0,
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'min': 0, 'step': '0.01', 'placeholder': 'Metraje por unidad'}
        )
    )

    class Meta:
        model = DetalleIdentificador
        fields = ['tipo', 'codigo_individual', 'valor', 'metraje']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'codigo_individual': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Codigo unico del equipo'}
            ),
            'valor': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: E4604D290944 o A1:B2:C3:D4:E5:F6'}
            ),
        }

    def clean_codigo_individual(self):
        codigo = (self.cleaned_data.get('codigo_individual') or '').strip().upper()
        return codigo

    def clean_valor(self):
        valor = (self.cleaned_data.get('valor') or '').strip().upper()
        return valor

    def clean_metraje(self):
        metraje = self.cleaned_data.get('metraje')
        return metraje if metraje is not None else 0


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'ruc', 'telefono', 'email', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUC / NIT'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
        }