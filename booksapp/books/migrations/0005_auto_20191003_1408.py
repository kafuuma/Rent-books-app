# Generated by Django 2.2.6 on 2019-10-03 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20191003_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_kind',
            field=models.CharField(default='Regular', max_length=50),
        ),
    ]