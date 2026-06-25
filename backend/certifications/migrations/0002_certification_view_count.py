from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='certification',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
