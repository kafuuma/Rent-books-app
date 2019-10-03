from .base import BaseTestCase
from .fixtures import query_book_string, query_cutomer_string


class QueryTestcase(BaseTestCase):

    def test_get_all_customers(self):
        self.create_customers()
        response = self.client.execute(
            query_cutomer_string
        )
        self.assertEqual(len(response['data']['customers']), 3)

    def test_get_all_books(self):
        self.create_books()
        response = self.client.execute(
            query_book_string
        )
        self.assertEqual(len(response['data']['books']), 2)
