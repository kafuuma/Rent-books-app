import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from ..models import Customer, Book, BorrowedBooks, RentedDuration
from ..helpers import GetObjectList, map_book_ids_to_rented_days


class bookKindEnum(graphene.Enum):
    regular = 'Regular'
    fiction = 'Fiction'
    novel = 'Novel'


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
        book_kind = bookKindEnum()

    def mutate(self, info, **kwargs):
        title = kwargs.get('title')
        total_number = kwargs.get('total_number')
        book_kind = kwargs.get('book_kind')
        errors = list()
        try:
            book = Book.objects.create(
                title=title, total_number=total_number, book_kind=book_kind)
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
        rented_days = graphene.List(graphene.Int, required=True)

    def mutate(self, info, **kwargs):
        errors = list()
        borrower_id = kwargs.get('borrower_id')
        books_ids = kwargs.get('books_ids')
        rented_days = kwargs.get('rented_days')
        if len(books_ids) != len(rented_days):
            raise GraphQLError(
                'The number of booksIds should match rentedDays')
        number_of_days = dict(zip(books_ids, rented_days))
        borrower = Customer.objects.filter(id=borrower_id).first()
        if not borrower:
            raise GraphQLError('This customer is not in the system')
        books_to_borrow = GetObjectList.get_objects(
            Book, books_ids)
        ids_to_days = map_book_ids_to_rented_days(
            number_of_days, books_to_borrow)
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
                for book_id, rented_days in ids_to_days.items():
                    rentend_duration = RentedDuration()
                    rentend_duration.book_id = book_id
                    rentend_duration.days = rented_days
                    rentend_duration.save()
                    borrowed_books.rented_days.add(rentend_duration)
        if errors:
            borrowed_books.delete()
            return BorrowBooks(errors=errors)
        borrowed_books.save()
        price = borrowed_books.price
        success = 'success'
        return BorrowBooks(
            borrowed_books=borrowed_books,
            price=price, errors=errors, success=success)


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    create_book = CreateBook.Field()
    lend_books = BorrowBooks.Field()
