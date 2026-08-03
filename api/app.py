from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.models import models
from api.models.database import engine
from .router import user, post, auth, vote
from .events.router import event
import graphene
from starlette_graphene3 import GraphQLApp
# from api.graphql.schema import schema

models.Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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