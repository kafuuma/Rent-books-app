from .base import BaseTestCase
from .fixtures import (create_customer_string,
                       create_book_string, borrow_books_string)


class MutationsTestcase(BaseTestCase):

    def test_create_customer(self):
        response = self.client.execute(
            create_customer_string.format(username='kafuuma')
        )
        self.assertEqual(response['data']['createCustomer']['success'],
                         'customer account kafuuma was created successfully')

    def test_create_duplicate_customer(self):
        self.client.execute(
            create_customer_string.format(username='kafuuma')
        )
        response = self.client.execute(
            create_customer_string.format(username='kafuuma')
        )
        self.assertIn('errors', response['data']['createCustomer'])

    def test_create_book(self):
        response = self.client.execute(
            create_book_string.format(
                title='how to learn c++ in 24hrs',
                total_number=25,
                book_kind='regular'
            )
        )
        self.assertEqual(
            response['data']['createBook']['success'],
            'book how to learn c++ in 24hrs was created successfully')
        self.assertEqual(response['data']['createBook']
                         ['book']['totalNumber'], 25)

    def test_create_dupilcate_title_book(self):
        self.client.execute(
            create_book_string.format(
                title='how to learn c++ in 24hrs',
                total_number=1,
                book_kind='novel'
            )
        )
        response = self.client.execute(
            create_book_string.format(
                title='how to learn c++ in 24hrs',
                total_number=25,
                book_kind='novel'
            )
        )
        self.assertIn('already exists',
                      response['data']['createBook']['errors'][0])

    def test_borrow_books(self):
        customer_id = self.customer.id
        books_ids = list(self.create_books())

        response = self.client.execute(
            borrow_books_string.format(
                customer_id=customer_id, books_ids=books_ids,
                days=[4, 5]
            )
        )

        self.assertEqual(
            len(response['data']['lendBooks']['borrowedBooks']), 2)
        self.assertEqual(response['data']['lendBooks']['price'], 27.0)

    def test_borrow_books_exceed_and_finish_all(self):
        customer_id = self.customer.id
        books_ids = list(self.create_books())

        for _ in range(6):
            response = self.client.execute(
                borrow_books_string.format(
                    customer_id=customer_id, books_ids=books_ids,
                    days=[7, 8]
                )
            )
        self.assertEqual(response['data']['lendBooks']['price'], None)
        self.assertIn('Books with test book2 are over',
                      response['data']['lendBooks']['errors'])
