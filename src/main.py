from fastapi import FastAPI

from src.apps.auth import routers as auth
from src.apps.tasks import routers as tasks
from src.apps.users import routers as users

app = FastAPI()


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Pixaflow's to do api!!"}
