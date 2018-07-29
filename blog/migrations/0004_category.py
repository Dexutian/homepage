# Generated by Django 2.0.4 on 2018-07-06 02:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180705_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='分类名')),
                ('slug', models.SlugField(max_length=40, verbose_name='slug')),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Category', verbose_name='父级分类')),
            ],
            options={
                'verbose_name': '分类',
                'ordering': ['name'],
            },
        ),
    ]
