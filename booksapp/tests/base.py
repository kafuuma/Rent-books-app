from django.test import TestCase
from graphene.test import Client
from schema import schema
from books.models import Book, Customer


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

    def create_customers(self):
        customer_1 = Customer.objects.create(username='kafuuma')
        customer_2 = Customer.objects.create(username='henry3')
        return customer_1.id, customer_2.id
