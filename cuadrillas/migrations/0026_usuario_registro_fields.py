from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuadrillas', '0025_soportetecnico'),
    ]

    operations = [
        migrations.AddField(
            model_name='asignacionmaterial',
            name='usuario_registro',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='equiporetiradomanual',
            name='usuario_registro',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]
