from typing import List

from fastapi import APIRouter, Depends

from apps.posts.dependencies import PostRepository, get_post_repository
from apps.posts.models import Post, CreatePostParams, DetailPost, UpdatePostParams

router = APIRouter()


@router.get("/", response_model=List[Post])
async def list_posts(repository: PostRepository = Depends(get_post_repository)):
    posts = await repository.list_posts()
    return posts


@router.get("/{id_}", response_model=DetailPost)
async def particular_post(id_: int, repository: PostRepository = Depends(get_post_repository)):
    post = await repository.detail_post(id_)
    return post


@router.post("/", response_model=Post, status_code=201)
async def create_user(params: CreatePostParams, repository: PostRepository = Depends(get_post_repository)):
    post = await repository.create_post(params)
    return post

@router.patch("/{id_}", status_code=200)
async def update_post(post: UpdatePostParams, id_: int, repository: PostRepository = Depends(get_post_repository)):
    post = await repository.update_post(post, id_)
    return post
