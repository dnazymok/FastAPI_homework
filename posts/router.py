from typing import List

from fastapi import APIRouter, Depends

from posts.dependencies import PostRepository, get_post_repository
from posts.models import Post

router = APIRouter()


@router.get("/", response_model=List[Post])
async def list_posts(repository: PostRepository = Depends(get_post_repository)):
    posts = await repository.list_posts()
    return posts
