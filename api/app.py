from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.db.database import Base, engine
from .router import user, post, auth, vote
from .router import event
from .config import settings
import graphene
from starlette_graphene3 import GraphQLApp
# from api.graphql.schema import schema

Base.metadata.create_all(bind=engine)
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_route(
#     "/graphql",
#     GraphQLApp(schema=schema)
# )

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)
app.include_router(vote.router)
app.include_router(event.router)


@app.get("/healthz")
def read_ap_health():
    return {"status": "ok"}