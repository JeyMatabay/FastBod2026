from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuadrillas', '0020_bajamaterial_equipo_retirado_detalle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bajamaterial',
            name='tipo_uso',
            field=models.CharField(
                blank=True,
                choices=[
                    ('Instalacion', 'Instalacion'),
                    ('Cambio de domicilio', 'Cambio de domicilio'),
                    ('Cambio', 'Cambio'),
                    ('Migracion', 'Migracion'),
                    ('Soporte', 'Soporte'),
                ],
                default='',
                max_length=20,
            ),
        ),
    ]
