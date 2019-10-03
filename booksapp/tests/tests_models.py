from .base import BaseTestCase
from books.models import Book, Customer, BorrowedBooks


class ModelsTestcase(BaseTestCase):

    def test_customers(self):
        customer = Customer.objects.create(username='kafuuma')
        self.assertEqual('kafuuma', str(customer))

    def test_book(self):
        book = Book.objects.create(title='rich dad poor dad')
        self.assertEqual('rich dad poor dad', str(book))
        self.assertEqual(1, book.total_number)
        self.assertEqual(0, book.total_rented)

    def test_borrowed_books(self):
        borrowed_books = BorrowedBooks.objects.create()
        book = Book.objects.create(title='rich dad poor dad')
        borrowed_books.books.add(book)
        self.assertEqual('BorrowedBooks(1)', str(borrowed_books))
