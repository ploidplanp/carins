# Generated by Django 3.0.4 on 2020-04-24 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infocustomer', '0004_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='picture',
            field=models.CharField(default='https://i.stack.imgur.com/l60Hf.png', max_length=255),
        ),
    ]
