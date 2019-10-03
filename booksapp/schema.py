import graphene
from books.schema.mutations import Mutation as books_mutation
from books.schema.query import Query as books_query


class Query(books_query, graphene.ObjectType):
    pass


class Mutation(books_mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
