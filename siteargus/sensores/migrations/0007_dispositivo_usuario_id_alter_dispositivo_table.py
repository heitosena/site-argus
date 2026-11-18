from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensores', '0006_leiturasalva'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispositivo',
            name='usuario_id',
            field=models.IntegerField(default=1),
        ),

        migrations.AlterModelTable(
            name='dispositivo',
            table='dispositivos',
        ),
    ]