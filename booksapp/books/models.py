
from django.db import models

from django.contrib.auth.models import User
from django.conf import settings

REANTAL_CHARGE = float(settings.PER_DAY_RENTAL_CHARGE)


class Book(models.Model):
    """ Book model, each book has a nique title. We assume
    many identical books in the store and record their number
    in the 'total_number field'

    """
    title = models.CharField(unique=True, max_length=200)
    total_number = models.PositiveIntegerField(default=1)
    total_rented = models.PositiveIntegerField(default=0)

    def add_books(self, number=1):
        self.total_number += number
        self.save()

    def remove_books(self, number=1):
        self.total_number -= number
        self.save()

    @property
    def total_count(self):
        return self.total_number

    def lend_books(self, number=1):
        self.total_rented += number
        self.save()

    @property
    def avilable_books(self):
        number = self.total_number - self.total_rented
        return number if number > 0 else 0

    def __str__(self):
        return f'{self.title}'


class Customer(User):
    """Customer that inherits from the user model
    we shall take advantage of unique username field on
    the inbuilt username field to uniquely identify a
    customer plus the ID
    """
    pass

    def __str__(self):
        return f'{self.username}'


class BorrowedBooks(models.Model):
    borrower = models.ManyToManyField(Customer)
    books = models.ManyToManyField(Book)
    borrowed_on = models.DateField(auto_now_add=True)
    number_of_days = models.IntegerField(default=1)
    returned_on = models.DateField(null=True)

    def __str__(self):
        return f'BorrowedBooks({self.number_of_days})'

    @property
    def price(self):
        return self.books.all().count() \
            * REANTAL_CHARGE * self.number_of_days
