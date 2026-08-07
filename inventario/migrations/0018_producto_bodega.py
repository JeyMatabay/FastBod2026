from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0017_producto_fecha_pedido_factura'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='bodega',
            field=models.CharField(
                choices=[('GENERAL', 'General'), ('CONSTRUCCION', 'Construccion')],
                default='GENERAL',
                max_length=20,
            ),
        ),
    ]
