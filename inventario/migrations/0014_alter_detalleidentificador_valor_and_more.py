from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0013_producto_metraje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimientoinventario',
            name='tipo',
            field=models.CharField(choices=[('ENTRADA', 'Entrada'), ('SALIDA', 'Salida'), ('ASIGNACION', 'Asignación')], max_length=20),
        ),
    ]