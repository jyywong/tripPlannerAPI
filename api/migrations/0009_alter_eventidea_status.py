# Generated by Django 3.2.5 on 2021-07-22 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20210722_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventidea',
            name='status',
            field=models.CharField(choices=[('Suggested', 'Suggested'), ('Added', 'Added')], default='Suggested', max_length=100),
        ),
    ]