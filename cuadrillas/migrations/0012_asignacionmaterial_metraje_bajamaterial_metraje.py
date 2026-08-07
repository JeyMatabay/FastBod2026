from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuadrillas', '0011_bajamaterial_cliente_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='asignacionmaterial',
            name='metraje',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='bajamaterial',
            name='metraje',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]