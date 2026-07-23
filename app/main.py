from fastapi import FastAPI, status, Response, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import uvicorn
import pyodbc
import time

app = FastAPI(debug=True)




class Post(BaseModel):
    # id: int
    title: str
    content: str
    published: bool


while True:
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=FastApi;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        cursor = conn.cursor()
        print('Database was successful')
        break
    except Exception as err:
        print("Connection to database failed.")
        print("Error ", err)
        time.sleep(5)



    published: bool = True

my_post = [
    {"title": "title to post", "content":"content to post 1", "id":1},
    {"title": "title to post2", "content":"content to post 2", "id":2},
    ]

@app.get("/")
async def root():
    return {"message": "Hello World!!"}


@app.get('/posts')
def get_post():
    cursor.execute(""" select * from Posts """)
    c = [col[0] for col  in cursor.description]
    posts =  [
        dict(zip(c, r))
        for r in cursor.fetchall()
    ]
    return {"data": posts}


@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM Posts where Id = ? """, (id,))
    post = cursor.fetchone()
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Post not found"}
    
    response.status_code = status.HTTP_200_OK
    # response.status_code = status.HTTP_404_NOT_FOUND if not post else status.HTTP_201_CREATED
    columns = [column[0] for column in cursor.description]
    post_dict = dict(zip(columns, post))
    return {"data": post_dict}

def find_post(id):
    return (p for p in my_post if p['id'] == id)

@app.post( '/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO Posts (title, content, published) 
        OUTPUT inserted.title
        VALUES (?, ?, ?)""", (
            post.title, post.content, post.published
    ))
    inserted_title = cursor.fetchone()[0]
    conn.commit()
    return {"data": inserted_title}


@app.delete('/posts/{id}')
def delete_post(id: int, response: Response):
    cursor.execute("""
        DELETE FROM Posts 
        OUTPUT deleted.title
        WHERE Id = ? 
    """, (id,))
    del_post = cursor.fetchone()
    if not del_post:
        response.status_code = status.HTTP_404_NOT_FOUND 
        return {"message": "Post not found"}
    response.status_code = status.HTTP_204_NO_CONTENT
    return



@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute("""
           UPDATE Posts
           SET title  = ?, content =?, published=?
          OUTPUT inserted.Id, inserted.title, inserted.content, inserted.published
           WHERE Id = ? 
       """, (post.title, post.content, post.published,  id,)
    )
    updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    conn.commit()

    c = [col[0] for col in cursor.description]
    data = dict(zip(c, updated_post))
    return {"data": data}



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )