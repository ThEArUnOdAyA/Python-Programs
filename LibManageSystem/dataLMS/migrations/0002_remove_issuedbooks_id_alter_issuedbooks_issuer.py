# Generated by Django 4.0.1 on 2022-02-17 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataLMS', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issuedbooks',
            name='id',
        ),
        migrations.AlterField(
            model_name='issuedbooks',
            name='issuer',
            field=models.EmailField(default=None, max_length=254, primary_key=True, serialize=False),
        ),
    ]