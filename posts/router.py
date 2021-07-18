from typing import List

from fastapi import APIRouter, Depends

from posts.dependencies import PostRepository, get_post_repository
from posts.models import Post, CreatePostParams

router = APIRouter()


@router.get("/", response_model=List[Post])
async def list_posts(repository: PostRepository = Depends(get_post_repository)):
    posts = await repository.list_posts()
    return posts


@router.post("/", response_model=Post, status_code=201)
async def create_user(params: CreatePostParams, repository: PostRepository = Depends(get_post_repository)):
    post = await repository.create_post(params)
    return post
