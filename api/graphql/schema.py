import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from starlette_graphene3 import GraphQLApp

from api.models import User

from .mutation import Mutation
from .query import Query


class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return f"Hello World {info}"

schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)