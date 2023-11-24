from django.db import migrations


def move_backward(apps, schema_editor):
    Owner = apps.get_model('property', 'Owner')
    for owner in Owner.objects.all():
        owner.flats.clear()


def link_owners_flats(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Owner = apps.get_model('property', 'Owner')
    for flat in Flat.objects.all():
        owner = Owner.objects.filter(
            full_name=flat.owner,
            pure_phone_number=flat.owner_pure_phone
        ).first()
        if owner:
            owner.flats.add(flat)


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0010_auto_20231124_0741'),
    ]

    operations = [
        migrations.RunPython(link_owners_flats, move_backward),
    ]
