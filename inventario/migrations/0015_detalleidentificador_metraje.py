from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0014_alter_detalleidentificador_valor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleidentificador',
            name='metraje',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
