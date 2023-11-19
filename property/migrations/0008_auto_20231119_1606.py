import phonenumbers
from django.db import migrations
from phonenumbers.phonenumberutil import NumberParseException


def is_valid_phone_number(number):
    try:
        parsed_number = phonenumbers.parse(number, "RU")
        return phonenumbers.is_valid_number(parsed_number)
    except NumberParseException:
        return False


def normalize_phone_number(number):
    parsed_number = phonenumbers.parse(number, "RU")
    formatted_number = phonenumbers.format_number(
        parsed_number,
        phonenumbers.PhoneNumberFormat.NATIONAL
    )
    formatted_number = formatted_number.replace("+7", "8")
    return formatted_number


def move_backward(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    for flat in Flat.objects.all():
        flat.owner_pure_phone = None
        flat.save()


def normalize_flat_numbers(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    for flat in Flat.objects.all():
        if not is_valid_phone_number(flat.owners_phonenumber):
            continue
        flat.owner_pure_phone = normalize_phone_number(
            flat.owners_phonenumber
        )
        flat.save()


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0007_flat_owner_pure_phone'),
    ]

    operations = [
        migrations.RunPython(normalize_flat_numbers, move_backward),
    ]
