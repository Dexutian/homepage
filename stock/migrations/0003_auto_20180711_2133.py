# Generated by Django 2.0.4 on 2018-07-11 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='name',
            name='companyabb',
            field=models.CharField(max_length=20),
        ),
    ]
