# Generated by Django 2.2.6 on 2019-10-03 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_book_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_kind',
            field=models.CharField(choices=[('Rugular', 'Regular'), ('Fiction', 'Fiction'), ('Novels', 'Novels')], default='Rugular', max_length=50),
        ),
    ]
