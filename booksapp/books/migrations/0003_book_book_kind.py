# Generated by Django 2.2.6 on 2019-10-03 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20191002_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_kind',
            field=models.CharField(choices=[('Ruglar', 'Regular'), ('Fiction', 'Fiction'), ('Novels', 'Novels')], default='Ruglar', max_length=50),
        ),
    ]
