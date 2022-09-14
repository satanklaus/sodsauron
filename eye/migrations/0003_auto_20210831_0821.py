# Generated by Django 3.2.6 on 2021-08-31 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eye', '0002_auto_20210831_0742'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('orgbranch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eye.orgbranch')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='location',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='eye.location'),
            preserve_default=False,
        ),
    ]