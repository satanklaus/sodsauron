# Generated by Django 3.2.6 on 2021-08-31 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eye', '0006_event_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='item',
            name='name',
        ),
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(default=' ', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='model',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='eye.itemmodel'),
            preserve_default=False,
        ),
    ]
