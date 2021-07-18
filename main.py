from fastapi import FastAPI

from apps import posts, users


def create_app():
    app = FastAPI()
    app.include_router(users.router, prefix="/users")
    app.include_router(posts.router, prefix="/posts")
    return app


app = create_app()
