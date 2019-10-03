
from django.db import models

from django.contrib.auth.models import User
from django.conf import settings
from .helpers import (calculate_price_for_noval_books,
                      calculate_price_for_regular_books)


CHARGE_REGULAR = float(settings.PER_DAY_RENTAL_CHARGE_REGULAR)
CHARGE_FICTION = float(settings.PER_DAY_RENTAL_CHARGE_FICTION)
CHARGE_NOVEL = float(settings.PER_DAY_RENTAL_CHARGE_NOVEL)


class Book(models.Model):
    """ Book model, each book has a nique title. We assume
    many identical books in the store and record their number
    in the 'total_number field'

    """
    title = models.CharField(unique=True, max_length=200)
    book_kind = models.CharField(max_length=50, default='Regular')
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


class RentedDuration(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    days = models.PositiveIntegerField(default=1)


class BorrowedBooks(models.Model):
    borrower = models.ManyToManyField(Customer)
    books = models.ManyToManyField(Book)
    borrowed_on = models.DateField(auto_now_add=True)
    rented_days = models.ManyToManyField(RentedDuration)
    returned_on = models.DateField(null=True)

    def __str__(self):
        return f'BorrowedBooks({self.books.count()})'

    @property
    def price(self):
        regular_books = self.rented_days.filter(book_id__book_kind='Regular')
        novel_books = self.rented_days.filter(book_id__book_kind='Novel')
        fiction_books = self.rented_days.filter(book_id__book_kind='Fiction')

        return self.calculate_price(regular_books, novel_books, fiction_books)

    def calculate_price(self, regular_books, novel_books, fiction_books):
        number_fiction_books = fiction_books.count()
        fiction_book_days = sum(book.days for book in list(fiction_books))

        total_regular_books_price = calculate_price_for_regular_books(
            regular_books, CHARGE_REGULAR) if regular_books else 0.0

        total_noval_books_price = calculate_price_for_noval_books(
            novel_books, CHARGE_NOVEL) if regular_books else 0.0

        total_price = (
            total_regular_books_price + total_noval_books_price +
            number_fiction_books*fiction_book_days*CHARGE_FICTION

        )
        return total_price
