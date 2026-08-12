import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from starlette_graphene3 import GraphQLApp
from .query import Query
from .mutation import Mutation

from api.models import User


class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return "Hello World"

schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)