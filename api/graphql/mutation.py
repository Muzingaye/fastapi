import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from api.db import database
from api.utls import utils
from models import models
from schema import UserType

class CreateUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(root, info, email, password):

        with database.SessionLocal() as db:
            existing = db.query(models.User).filter(models.User.email == email).first()

            if existing: raise Exception("Email already exists")

            new_user = models.User(email= email, password = utils.hash(password))
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        return CreateUser(user=new_user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
