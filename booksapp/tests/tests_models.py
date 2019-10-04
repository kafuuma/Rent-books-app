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
        book.add_books(2)
        self.assertEqual(3, book.total_number)
        book.remove_books(1)
        self.assertEqual(2, book.total_number)
        self.assertEqual(2, book.total_count)

    def test_borrowed_books(self):
        borrowed_books = BorrowedBooks.objects.create()
        book = Book.objects.create(title='rich dad poor dad')
        borrowed_books.books.add(book)
        self.assertEqual('BorrowedBooks(1)', str(borrowed_books))
