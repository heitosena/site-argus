
from django.db import migrations


def preencher_usuario_id(apps, schema_editor):

    LeituraSalva = apps.get_model('sensores', 'LeituraSalva')

    # Associa as leituras antigas à conta de teste.
    LeituraSalva.objects.filter(
        usuario_id__isnull=True
    ).update(usuario_id=1)


class Migration(migrations.Migration):

    dependencies = [
        ('sensores', '0010_leiturasalva_usuario_id'),
    ]

    operations = [
        migrations.RunPython(
            preencher_usuario_id,
            migrations.RunPython.noop
        ),
    ]
