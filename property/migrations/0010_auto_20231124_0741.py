from django.db import migrations


def move_backward(apps, schema_editor):
    Owner = apps.get_model('property', 'Owner')
    Owner.objects.all().delete()


def create_owners(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Owner = apps.get_model('property', 'Owner')
    for flat in Flat.objects.all():
        Owner.objects.get_or_create(
            full_name=flat.owner,
            pure_phone_number=flat.owner_pure_phone,
            defaults={
                "phone_number": flat.owners_phonenumber,
            }
        )


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0009_owner'),
    ]

    operations = [
        migrations.RunPython(create_owners, move_backward),
    ]
