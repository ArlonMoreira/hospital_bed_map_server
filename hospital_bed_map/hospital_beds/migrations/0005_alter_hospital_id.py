# Generated by Django 4.2 on 2023-04-09 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_beds', '0004_alter_hospital_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='Identificação'),
        ),
    ]
