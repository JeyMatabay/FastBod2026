from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuadrillas', '0017_bajamaterial_codigo_bobina'),
    ]

    operations = [
        migrations.AddField(
            model_name='bajamaterial',
            name='serial_mac_retirado',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
    ]
