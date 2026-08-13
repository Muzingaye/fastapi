import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from api.db import database
from api.utls import utils

# from schema import UserType
from .types import PostType, UserType


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


class CreatePost(graphene.Mutation):

    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        published = graphene.Boolean(default_value=True)

    post = graphene.Field(PostType)

    def mutate(self, info, title, content, published=True):

        db = info.context["db"]
        current_user = info.context.get("current_user")

        if current_user is None:
            raise Exception("Not authenticated")

        new_post = models.Post(
            title=title,
            content=content,
            published=published,
            userId=current_user.id
        )

        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return CreatePost(post=new_post)


class Mutation(graphene.ObjectType):

    create_post = CreatePost.Field()
    create_user = CreateUser.Field()