# Generated by Django 3.2.6 on 2021-08-31 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eye', '0005_auto_20210831_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='item',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='eye.item'),
            preserve_default=False,
        ),
    ]
