from fastapi import FastAPI

from todo_list_pf.routers import auth, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to to do list pf API!"}
