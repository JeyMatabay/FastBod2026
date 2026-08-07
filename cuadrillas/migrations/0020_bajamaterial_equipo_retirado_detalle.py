from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuadrillas', '0019_bajamaterial_reutilizado'),
    ]

    operations = [
        migrations.AddField(
            model_name='bajamaterial',
            name='codigo_retirado',
            field=models.CharField(blank=True, default='', max_length=80),
        ),
        migrations.AddField(
            model_name='bajamaterial',
            name='categoria_retirado',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='bajamaterial',
            name='marca_retirado',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='bajamaterial',
            name='modelo_retirado',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
