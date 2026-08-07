from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuadrillas', '0018_bajamaterial_serial_mac_retirado'),
    ]

    operations = [
        migrations.AddField(
            model_name='bajamaterial',
            name='reutilizado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bajamaterial',
            name='fecha_reutilizado',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
