# Generated by Django 3.2.6 on 2021-08-31 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eye', '0010_auto_20210831_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='eye.itemmodel'),
        ),
    ]
