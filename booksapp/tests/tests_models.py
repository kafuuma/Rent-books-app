from .base import BaseTestCase
from books.models import Book, Customer, BorrowedBooks


class CustomerTestcase(BaseTestCase):

    def test_customers(self):
        customer = Customer.objects.create(username='kafuuma')
        self.assertEqual('kafuuma', str(customer))

    def test_book(self):
        book = Book.objects.create(title='rich dad poor dad')
        self.assertEqual('rich dad poor dad', str(book))
        self.assertEqual(1, book.total_number)
        self.assertEqual(0, book.total_rented)

    def test_borrowed_books(self):
        borrowed_books = BorrowedBooks.objects.create(number_of_days=12)
        self.assertEqual('BorrowedBooks(12)', str(borrowed_books))
