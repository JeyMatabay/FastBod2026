from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cuadrillas', '0022_cliente_ct_cedula'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipoRetiradoManual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('origen', models.CharField(choices=[('Cambio', 'Cambio'), ('Manual', 'Manual')], default='Manual', max_length=20)),
                ('producto_nombre', models.CharField(blank=True, default='', max_length=120)),
                ('producto_codigo', models.CharField(blank=True, default='', max_length=50)),
                ('proveedor_nombre', models.CharField(blank=True, default='', max_length=150)),
                ('cuadrilla_nombre', models.CharField(blank=True, default='', max_length=100)),
                ('cliente_nombre', models.CharField(blank=True, default='', max_length=150)),
                ('ct_cliente', models.CharField(blank=True, default='', max_length=40)),
                ('detalle_cambio', models.TextField(blank=True, default='')),
                ('categoria_retirado', models.CharField(blank=True, default='', max_length=100)),
                ('marca_retirado', models.CharField(blank=True, default='', max_length=100)),
                ('modelo_retirado', models.CharField(blank=True, default='', max_length=100)),
                ('serial_mac_retirado', models.CharField(blank=True, default='', max_length=120)),
                ('codigo_retirado', models.CharField(blank=True, default='', max_length=80)),
                ('cantidad', models.IntegerField(default=1)),
                ('metraje', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('reutilizado', models.BooleanField(default=False)),
                ('fecha_reutilizado', models.DateTimeField(blank=True, null=True)),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='retiros_manual', to='inventario.producto')),
            ],
        ),
    ]
