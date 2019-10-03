
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
