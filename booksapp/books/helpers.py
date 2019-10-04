
from functools import reduce

from django.db.models import Q
from graphql import GraphQLError


class GetObjectList:
    error = 'Cannot query an empty list of object IDs'

    @staticmethod
    def get_objects(model, list_of_ids, message=None):
        """Queries the database to return a list of
        objects

        Arguments:
            list_of_ids(list): list of filed ids
            model (django model)
        Returns:
            A list of objetcs

        Raises:
            GraphQL error if empty id list supplied
        """
        if not list_of_ids:
            message = message or GetObjectList.error
            raise GraphQLError(message)
        query = reduce(lambda q, id: q | Q(id=id), list_of_ids, Q())
        queryset = model.objects.filter(query)
        if not queryset:
            ids = ', '.join(map(str, list_of_ids))
            raise GraphQLError(
                f'There are no {model.__name__}(s) matching IDs: {ids}.')
        return queryset


def map_book_ids_to_rented_days(number_of_days, books_to_borrow):
    ids = [book.id for book in books_to_borrow]
    ids_to_days = {key: value for key, value in number_of_days.items()
                   if int(key) in ids}
    return ids_to_days


def calculate_price_for_regular_books(regular_books, normal_price):
    price = 0.0
    for book in regular_books:
        if book.days < 2:
            price += 2*book.days
        elif book.days >= 2:
            # if days > 2 multipy by 1.5Rs and by 1Rs for first 2 days
            price += ((book.days-2)*normal_price+2*1)
    return price


def calculate_price_for_noval_books(novel_books, normal_price):
    price = 0.0
    for book in novel_books:
        if book.days < 3:
            price += 4.5*book.days
        else:
            price += normal_price*book.days
    return price
