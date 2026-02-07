from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_store_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='store_description',
            field=models.TextField(blank=True),
        ),
    ]
