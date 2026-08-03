import graphene 
from models import models, schemas, database
from . schema import UserType

class Query(graphene.ObjectType):

    users = graphene.List(UserType)
    user =graphene.Field(UserType, id=graphene.Int)

    def resolve_users(root, info):
        with database.SessionLocal() as db:
            users = db.query(models.User).all()
        return users

    def resolve_user(root, info, id):
        with database.SessionLocal() as db:
            user = db.query(models.User).filter(models.User.id == id).first()
        return user