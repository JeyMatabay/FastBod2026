from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuadrillas', '0026_usuario_registro_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='bajamaterial',
            name='usuario_registro',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]
