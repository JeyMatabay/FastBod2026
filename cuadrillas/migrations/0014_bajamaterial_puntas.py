from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuadrillas', '0013_bajamaterial_observacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='bajamaterial',
            name='punta_final',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='bajamaterial',
            name='punta_inicial',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
