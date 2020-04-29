# Generated by Django 3.0.4 on 2020-04-28 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20200428_1801'),
        ('contract', '0023_auto_20200428_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compulsory_insurance',
            name='compulsory_car_use_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.Premium_Table'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.Person'),
        ),
        migrations.AlterField(
            model_name='insurance_policy',
            name='insurance_car_use_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.Car_Use_Type_Table'),
        ),
    ]
