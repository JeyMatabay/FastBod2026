from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuadrillas', '0015_bajamaterial_estado_equipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='bajamaterial',
            name='fecha_retirado',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bajamaterial',
            name='retirado',
            field=models.BooleanField(default=False),
        ),
    ]
