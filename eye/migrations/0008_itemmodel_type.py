# Generated by Django 3.2.6 on 2021-08-31 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eye', '0007_auto_20210831_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemmodel',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='eye.itemtype'),
            preserve_default=False,
        ),
    ]