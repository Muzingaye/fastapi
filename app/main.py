from fastapi import FastAPI, status, Response, HTTPException, Depends
from .models import models
from .models.database import engine
from .router import user, post, auth, vote


models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)




