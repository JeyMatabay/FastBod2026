from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0012_detalleidentificador_codigo_individual'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='metraje',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]