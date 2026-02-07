# Generated migration for adding vendor field to Store model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='vendor',
            field=models.ForeignKey(
                default=1,
                limit_choices_to={'user_type': 'vendor'},
                on_delete=django.db.models.deletion.CASCADE,
                related_name='stores',
                to=settings.AUTH_USER_MODEL
            ),
            preserve_default=False,
        ),
    ]
