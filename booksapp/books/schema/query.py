import graphene
from graphene_django import DjangoObjectType
from ..models import Customer, Book
from .mutations import CustomerNode, BookNode


class BooksQuery(graphene.ObjectType):

    books = graphene.List(BookNode)

    def resolve_books(self, info, **kwargs):
        return Book.objects.all()


class CustomerQuery(graphene.ObjectType):
    customers = graphene.List(CustomerNode)

    def resolve_customers(self, info, **kwargs):
        return Customer.objects.all()


class Query(BooksQuery, CustomerQuery, graphene.ObjectType):
    pass
