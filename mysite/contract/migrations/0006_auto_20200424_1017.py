# Generated by Django 3.0.4 on 2020-04-24 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20200410_1405'),
        ('contract', '0005_auto_20200424_1017'),
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
