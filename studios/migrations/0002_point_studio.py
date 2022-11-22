# Generated by Django 4.1.3 on 2022-11-18 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='studio',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='studio', to='studios.studio'),
            preserve_default=False,
        ),
    ]