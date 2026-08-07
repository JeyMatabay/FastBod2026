from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuadrillas', '0021_alter_bajamaterial_tipo_uso'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='ct',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
        migrations.AddField(
            model_name='cliente',
            name='cedula',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]
