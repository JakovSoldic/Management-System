# Generated by Django 4.2.1 on 2023-06-07 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_alter_user_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('none', 'None'), ('redovni', 'Redovni'), ('izvanredni', 'Izvanredni')], max_length=20, null=True),
        ),
    ]