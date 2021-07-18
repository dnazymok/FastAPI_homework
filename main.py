from fastapi import FastAPI

import users


def create_app():
    app = FastAPI()
    app.include_router(users.router, prefix="/users")
    return app


app = create_app()
