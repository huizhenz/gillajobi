from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
