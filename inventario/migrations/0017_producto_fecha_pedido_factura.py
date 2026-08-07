from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0016_proveedor_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='fecha_pedido_factura',
            field=models.DateField(blank=True, null=True),
        ),
    ]
