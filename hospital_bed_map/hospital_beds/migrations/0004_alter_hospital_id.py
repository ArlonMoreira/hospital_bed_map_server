# Generated by Django 4.2 on 2023-04-09 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_beds', '0003_alter_hospital_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='Identificação'),
        ),
    ]
