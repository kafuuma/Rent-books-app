import graphene
from graphene_django import DjangoObjectType
from django.conf import settings

from ..models import Customer, Book, BorrowedBooks
from ..helpers import GetObjectList


class BookNode(DjangoObjectType):

    class Meta:
        model = Book


class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer


class BorrowedBooksNode(DjangoObjectType):
    class Meta:
        model = BorrowedBooks


class CreateCustomer(graphene.Mutation):
    customer = graphene.Field(CustomerNode)
    success = graphene.String()
    errors = graphene.List(graphene.String)

    class Arguments:
        username = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        username = kwargs.get('username')
        errors = list()
        try:
            customer = Customer.objects.create(username=username)
        except Exception as e:
            errors.append(str(e))
        if errors:
            return CreateCustomer(errors=errors)
        success = f'customer account {username} was created successfully'
        customer.save()
        return CreateCustomer(customer=customer, success=success)


class CreateBook(graphene.Mutation):
    book = graphene.Field(BookNode)
    success = graphene.String()
    errors = graphene.List(graphene.String)

    class Arguments:
        title = graphene.String(required=True)
        total_number = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        title = kwargs.get('title')
        total_number = kwargs.get('total_number')
        errors = list()
        try:
            book = Book.objects.create(title=title, total_number=total_number)
        except Exception as e:
            errors.append(str(e))
        if errors:
            return CreateBook(errors=errors)
        success = f'book {title} was created successfully'
        book.save()
        return CreateBook(book=book, success=success)


class BorrowBooks(graphene.Mutation):
    borrowed_books = graphene.Field(BorrowedBooksNode)
    price = graphene.Float()
    success = graphene.String()
    errors = graphene.List(graphene.String)

    class Arguments:
        borrower_id = graphene.ID(required=True)
        books_ids = graphene.List(graphene.ID, required=True)
        number_of_days = graphene.Int()

    def mutate(self, info, **kwargs):
        errors = list()
        borrower_id = kwargs.get('borrower_id')
        books_ids = kwargs.get('books_ids')
        number_of_days = kwargs.get('number_of_days')
        borrower = Customer.objects.filter(id=borrower_id).first()
        if not borrower:
            errors.append('This customer is not in the system')
        books_to_borrow = GetObjectList.get_objects(
            Book, books_ids)
        borrowed_books = BorrowedBooks()
        borrowed_books.save()
        if books_to_borrow:
            for book in books_to_borrow:
                if book.avilable_books:
                    borrowed_books.books.add(book)
                    book.lend_books()
                else:
                    errors.append(f'Books with {book.title} are over')
            borrowed_books.borrower.add(borrower)
            if borrowed_books:
                borrowed_books.number_of_days = number_of_days
        borrowed_books.save()
        price = borrowed_books.price
        success = 'success'
        return BorrowBooks(borrowed_books=borrowed_books, price=price, errors=errors, success=success)


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    create_book = CreateBook.Field()
    lend_books = BorrowBooks.Field()
