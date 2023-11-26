from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0013_auto_20231125_0256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='flat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints_to', to='property.Flat', verbose_name='Квартира, на которую пожалвались'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints_from', to=settings.AUTH_USER_MODEL, verbose_name='Кто жаловался'),
        ),
    ]
