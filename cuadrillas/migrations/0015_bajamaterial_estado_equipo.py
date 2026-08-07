from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuadrillas', '0014_bajamaterial_puntas'),
    ]

    operations = [
        migrations.AddField(
            model_name='bajamaterial',
            name='estado_equipo',
            field=models.CharField(
                blank=True,
                choices=[('Nuevo', 'Nuevo'), ('Utilizado', 'Utilizado')],
                default='',
                max_length=20,
            ),
        ),
    ]
