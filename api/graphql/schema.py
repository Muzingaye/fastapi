import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import models

class UserType(SQLAlchemyObjectType):
    class Meta:
        models: models.User




import graphene

from .query import Query
from .mutation import Mutation

schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)