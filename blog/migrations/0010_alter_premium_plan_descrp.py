# Generated by Django 4.1 on 2023-11-19 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_premium_plan_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='premium',
            name='plan_descrp',
            field=models.CharField(max_length=50),
        ),
    ]