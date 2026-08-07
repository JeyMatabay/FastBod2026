from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuadrillas', '0012_asignacionmaterial_metraje_bajamaterial_metraje'),
    ]

    operations = [
        migrations.AddField(
            model_name='bajamaterial',
            name='observacion',
            field=models.TextField(blank=True, default=''),
        ),
    ]