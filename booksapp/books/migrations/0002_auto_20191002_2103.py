# Generated by Django 2.2.6 on 2019-10-02 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='total_number',
            field=models.PositiveIntegerField(default=1),
        ),
    ]