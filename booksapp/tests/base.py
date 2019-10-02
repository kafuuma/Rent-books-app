import json

from django.test import TestCase
from graphene.test import Client
from schema import schema
from books.models import Book, Customer, BorrowedBooks


class BaseTestCase(TestCase):

    def setUp(self):
        self.client = Client(schema)
        self.customer = Customer.objects.create(username='henry')

    def create_books(self):
        book1 = self.books = Book.objects.create(
            title='test book1', total_number=5)
        book2 = self.books = Book.objects.create(
            title='test book2', total_number=3)
        return book1.id, book2.id
