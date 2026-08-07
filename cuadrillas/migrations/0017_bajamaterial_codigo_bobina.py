from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuadrillas', '0016_bajamaterial_retirado_fecha_retirado'),
    ]

    operations = [
        migrations.AddField(
            model_name='bajamaterial',
            name='codigo_bobina',
            field=models.CharField(blank=True, default='', max_length=80),
        ),
    ]
