# Generated by Django 4.1.3 on 2022-11-18 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0017_studioclass_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studioclass',
            options={'ordering': ['-start_time']},
        ),
    ]
