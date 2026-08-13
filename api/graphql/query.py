import graphene
from sqlalchemy import func

from api.db import database
# from api.schemas import schemas
from api.models import Post, User, Vote

from .types import PostType, UserType


class Query(graphene.ObjectType):

    posts = graphene.List(
        PostType,
        limit=graphene.Int(default_value=10),
        skip=graphene.Int(default_value=0),
        search=graphene.String(default_value="")
    )

    post = graphene.Field(
        PostType,
        id=graphene.Int(required=True)
    )

    def resolve_posts(self, info, limit=10, skip=0, search=""):

        db = info.context["db"]

        results = (
            db.query(
                Post,
                func.count(Vote.postId).label("votes")
            )
            .outerjoin(
                Vote,
                Vote.postId == Post.id
            )
            .filter(
                Post.title.contains(search)
            )
            .group_by(
                Post.id,
                Post.title,
                Post.content,
                Post.published,
                Post.createdDate,
                Post.userId
            )
            .order_by(
                Post.createdDate.desc()
            )
            .limit(limit)
            .offset(skip)
            .all()
        )

        posts = []

        for post, votes in results:
            post.votes = votes
            posts.append(post)

        return posts

    def resolve_post(self, info, id):

        db = info.context["db"]

        result = (
            db.query(
                Post,
                func.count(Vote.postId).label("votes")
            )
            .outerjoin(
                Vote,
                Vote.postId == Post.id
            )
            .filter(Post.id == id)
            .group_by(
                Post.id,
                Post.title,
                Post.content,
                Post.published,
                Post.createdDate,
                Post.userId
            )
            .first()
        )

        if not result:
            return None

        post, votes = result
        post.votes = votes

        return post

class Query(graphene.ObjectType):

    users = graphene.List(UserType)
    user =graphene.Field(UserType, id=graphene.Int())

    def resolve_users(root, info):
        with database.SessionLocal() as db:
            users = db.query(User).all()
        return users

    def resolve_user(root, info, id):
        with database.SessionLocal() as db:
            user = db.query(User).filter(User.id == id).first()
        return user