from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuadrillas', '0023_equiporetiradomanual'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equiporetiradomanual',
            name='origen',
            field=models.CharField(choices=[('Cambio', 'Cambio'), ('Retirado', 'Retirado')], default='Retirado', max_length=20),
        ),
    ]
