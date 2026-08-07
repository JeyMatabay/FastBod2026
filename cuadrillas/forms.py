from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import BajaMaterial, Cuadrilla, SoporteTecnico, AsignacionMaterial, BajaIdentificador
from inventario.models import DetalleIdentificador
from inventario.forms import es_categoria_activa, es_categoria_fibra


class CuadrillaForm(forms.ModelForm):

    def _normalizar(self, texto):
        return (texto or '').strip().lower().replace('cuadrilla', '').strip()

    def clean(self):
        cleaned_data = super().clean()

        nombre = cleaned_data.get('nombre')
        responsable = cleaned_data.get('responsable')

        if not nombre or not responsable:
            return cleaned_data

        nombre_norm = self._normalizar(nombre)
        user_norm = self._normalizar(getattr(responsable, 'username', ''))

        # Permite casos como: "C1" y responsable "C1", o "Cuadrilla C1" y "C1".
        coincide = (
            nombre_norm == user_norm
            or nombre_norm in user_norm
            or user_norm in nombre_norm
        )

        if not coincide:
            self.add_error(
                'responsable',
                f'El responsable ({responsable.username}) no coincide con el nombre de cuadrilla ({nombre}).'
            )

        return cleaned_data

    class Meta:
        model = Cuadrilla
        fields = '__all__'

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.Select(attrs={'class': 'form-control'})
        }


class CrearCuadrillaConResponsableForm(CuadrillaForm):
    nuevo_responsable_username = forms.CharField(
        required=False,
        label='Nuevo responsable (usuario)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
    )
    nuevo_responsable_password1 = forms.CharField(
        required=False,
        label='Contrasena',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'})
    )
    nuevo_responsable_password2 = forms.CharField(
        required=False,
        label='Confirmar contrasena',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsable'].required = False
        self.fields['responsable'].widget.attrs['class'] = 'form-select'
        self.fields['responsable'].empty_label = '-- Seleccione responsable existente --'
        self.order_fields([
            'nombre',
            'responsable',
            'nuevo_responsable_username',
            'nuevo_responsable_password1',
            'nuevo_responsable_password2',
        ])

    def clean(self):
        cleaned_data = super().clean()

        responsable = cleaned_data.get('responsable')
        username = (cleaned_data.get('nuevo_responsable_username') or '').strip()
        password1 = cleaned_data.get('nuevo_responsable_password1')
        password2 = cleaned_data.get('nuevo_responsable_password2')

        usa_nuevo = bool(username or password1 or password2)

        if responsable and usa_nuevo:
            raise forms.ValidationError('Seleccione un responsable existente o cree uno nuevo, no ambos.')

        if not responsable and not usa_nuevo:
            self.add_error('responsable', 'Debe seleccionar un responsable o crear uno nuevo.')

        if usa_nuevo:
            if not username:
                self.add_error('nuevo_responsable_username', 'Ingrese el usuario del nuevo responsable.')
            if not password1:
                self.add_error('nuevo_responsable_password1', 'Ingrese la contrasena.')
            if not password2:
                self.add_error('nuevo_responsable_password2', 'Confirme la contrasena.')
            if password1 and password2 and password1 != password2:
                self.add_error('nuevo_responsable_password2', 'Las contrasenas no coinciden.')

            User = get_user_model()
            if username and User.objects.filter(username__iexact=username).exists():
                self.add_error('nuevo_responsable_username', 'Ese usuario ya existe.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        username = (self.cleaned_data.get('nuevo_responsable_username') or '').strip()
        password1 = self.cleaned_data.get('nuevo_responsable_password1')

        if username and password1:
            User = get_user_model()
            nuevo_usuario = User.objects.create_user(
                username=username,
                password=password1,
            )

            if hasattr(nuevo_usuario, 'is_cuadrilla'):
                nuevo_usuario.is_cuadrilla = True
                nuevo_usuario.save(update_fields=['is_cuadrilla'])

            nombre_cuadrilla = (self.cleaned_data.get('nombre') or '').strip()
            if nombre_cuadrilla:
                grupo, _ = Group.objects.get_or_create(name=f'CUADRILLA {nombre_cuadrilla}')
                nuevo_usuario.groups.add(grupo)

            instance.responsable = nuevo_usuario

        if commit:
            instance.save()

        return instance


class SoporteTecnicoForm(forms.ModelForm):

    def _normalizar(self, texto):
        return (texto or '').strip().lower().replace('soporte', '').replace('tecnico', '').strip()

    def clean(self):
        cleaned_data = super().clean()

        nombre = cleaned_data.get('nombre')
        responsable = cleaned_data.get('responsable')

        if not nombre or not responsable:
            return cleaned_data

        nombre_norm = self._normalizar(nombre)
        user_norm = self._normalizar(getattr(responsable, 'username', ''))

        coincide = (
            nombre_norm == user_norm
            or nombre_norm in user_norm
            or user_norm in nombre_norm
        )

        if not coincide:
            self.add_error(
                'responsable',
                f'El responsable ({responsable.username}) no coincide con el nombre de soporte ({nombre}).'
            )

        return cleaned_data

    class Meta:
        model = SoporteTecnico
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.Select(attrs={'class': 'form-control'})
        }


class CrearSoporteConResponsableForm(SoporteTecnicoForm):
    nuevo_responsable_username = forms.CharField(
        required=False,
        label='Nuevo responsable (usuario)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
    )
    nuevo_responsable_password1 = forms.CharField(
        required=False,
        label='Contrasena',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'})
    )
    nuevo_responsable_password2 = forms.CharField(
        required=False,
        label='Confirmar contrasena',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsable'].required = False
        self.fields['responsable'].widget.attrs['class'] = 'form-select'
        self.fields['responsable'].empty_label = '-- Seleccione responsable existente --'
        self.order_fields([
            'nombre',
            'responsable',
            'nuevo_responsable_username',
            'nuevo_responsable_password1',
            'nuevo_responsable_password2',
        ])

    def clean(self):
        cleaned_data = super().clean()

        responsable = cleaned_data.get('responsable')
        username = (cleaned_data.get('nuevo_responsable_username') or '').strip()
        password1 = cleaned_data.get('nuevo_responsable_password1')
        password2 = cleaned_data.get('nuevo_responsable_password2')

        usa_nuevo = bool(username or password1 or password2)

        if responsable and usa_nuevo:
            raise forms.ValidationError('Seleccione un responsable existente o cree uno nuevo, no ambos.')

        if not responsable and not usa_nuevo:
            self.add_error('responsable', 'Debe seleccionar un responsable o crear uno nuevo.')

        if usa_nuevo:
            if not username:
                self.add_error('nuevo_responsable_username', 'Ingrese el usuario del nuevo responsable.')
            if not password1:
                self.add_error('nuevo_responsable_password1', 'Ingrese la contrasena.')
            if not password2:
                self.add_error('nuevo_responsable_password2', 'Confirme la contrasena.')
            if password1 and password2 and password1 != password2:
                self.add_error('nuevo_responsable_password2', 'Las contrasenas no coinciden.')

            User = get_user_model()
            if username and User.objects.filter(username__iexact=username).exists():
                self.add_error('nuevo_responsable_username', 'Ese usuario ya existe.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        username = (self.cleaned_data.get('nuevo_responsable_username') or '').strip()
        password1 = self.cleaned_data.get('nuevo_responsable_password1')

        if username and password1:
            User = get_user_model()
            nuevo_usuario = User.objects.create_user(
                username=username,
                password=password1,
            )

            if hasattr(nuevo_usuario, 'is_cuadrilla'):
                nuevo_usuario.is_cuadrilla = False
                nuevo_usuario.save(update_fields=['is_cuadrilla'])

            nombre_soporte = (self.cleaned_data.get('nombre') or '').strip()
            if nombre_soporte:
                grupo, _ = Group.objects.get_or_create(name=f'SOPORTE {nombre_soporte}')
                nuevo_usuario.groups.add(grupo)

            instance.responsable = nuevo_usuario

        if commit:
            instance.save()

        return instance


class AsignacionMaterialForm(forms.ModelForm):

    metraje = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        max_digits=12,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01'}),
        label='Metraje'
    )

    identificadores = forms.ModelMultipleChoiceField(
        queryset=DetalleIdentificador.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': 8}),
        label='Seriales / MAC a enviar'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        producto_id = None
        if self.data.get('producto'):
            producto_id = self.data.get('producto')
        elif self.initial.get('producto'):
            producto_id = self.initial.get('producto')

        if producto_id:
            try:
                producto = self.fields['producto'].queryset.get(pk=producto_id)
                if es_categoria_activa(producto.categoria.nombre if producto.categoria else ''):
                    identificadores_en_baja = BajaIdentificador.objects.filter(
                        identificador__producto=producto
                    ).values_list('identificador_id', flat=True)

                    self.fields['identificadores'].queryset = DetalleIdentificador.objects.filter(
                        producto=producto,
                        tipo__in=['SERIAL', 'MAC']
                    ).exclude(
                        id__in=identificadores_en_baja
                    ).filter(
                        asignacion_detalle__isnull=True
                    ).order_by('tipo', 'valor')
            except Exception:
                self.fields['identificadores'].queryset = DetalleIdentificador.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad') or 0
        metraje = cleaned_data.get('metraje') or 0

        if not producto:
            return cleaned_data

        categoria_nombre = producto.categoria.nombre if producto.categoria else ''

        if cantidad <= 0:
            self.add_error('cantidad', 'La cantidad debe ser mayor a cero.')

        if es_categoria_fibra(categoria_nombre):
            if metraje <= 0:
                self.add_error('metraje', 'Debe ingresar el metraje para productos de fibra.')
        else:
            cleaned_data['metraje'] = 0

        return cleaned_data

    class Meta:
        model = AsignacionMaterial
        fields = ['cuadrilla', 'producto', 'cantidad', 'metraje']

        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cuadrilla': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'})
        }

class BajaMaterialForm(forms.ModelForm):
    class Meta:
        model = BajaMaterial
        fields = ['asignacion', 'cantidad']