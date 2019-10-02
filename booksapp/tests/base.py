import json

from django.test import TestCase
from graphene.test import Client
from schema import schema


class BaseTestCase(TestCase):

    def setUp(self):
        self.client = Client(schema)
