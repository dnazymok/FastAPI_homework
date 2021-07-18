from fastapi import FastAPI

import users, posts


def create_app():
    app = FastAPI()
    app.include_router(users.router, prefix="/users")
    app.include_router(posts.router, prefix="/posts")
    return app


app = create_app()
