from graphene_sqlalchemy import SQLAlchemyObjectType

from api.models.post import Post
# from api.models import User, Post
from api.models.user import User

print("Debug User =", User)
print("Debug User type =", type(User))

class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User


class PostType(SQLAlchemyObjectType):
    class Meta:
         model = Post

    # def resolve_created_date(self, info):
    #     return self.createdDate

    # def resolve_user_id(self, info):
    #     return self.userId

    # def resolve_owner(self, info):
    #     return self.owner