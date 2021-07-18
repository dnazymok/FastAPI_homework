from typing import Optional

from pydantic import BaseModel
from users.models import User


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: Optional[User]
