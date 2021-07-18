from typing import List

from pydantic import BaseModel
from apps.users.models import User


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User


class CreatePostParams(BaseModel):
    userId: int
    title: str
    body: str


class DetailPost(Post):
    comments: List


class UpdatePostParams(BaseModel):
    title: str
    body: str
