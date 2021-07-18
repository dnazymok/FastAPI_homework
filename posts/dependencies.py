import aiohttp

from typing import Any, Dict, List
from .models import Post, CreatePostParams, DetailPost


class PostRepository:
    def __init__(self):
        self._post_endpoint = "https://jsonplaceholder.typicode.com/posts"
        self._author_endpoint = "https://jsonplaceholder.typicode.com/users/"
        self._comment_endpoint = "https://jsonplaceholder.typicode.com/comments?postId="

    async def list_posts(self) -> List[Post]:
        raw_posts = await self._list_posts()
        return [self._convert_post(raw_post) for raw_post in raw_posts]

    async def create_post(self, post: CreatePostParams) -> Post:
        raw_post = await self._create_post(post)
        return self._convert_post(raw_post)

    async def detail_post(self, id_: int):
        raw_post = await self._detail_post(id_)
        return DetailPost(**raw_post)

    async def _list_posts(self):
        async with aiohttp.ClientSession() as session:
            post_resp = await session.get(self._post_endpoint)
            author_resp = await session.get(self._author_endpoint)
            raw_posts = await post_resp.json()
            raw_authors = await author_resp.json()
            await self._match_authors_and_posts(raw_posts, raw_authors)
            return raw_posts

    async def _create_post(self, post: CreatePostParams) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            post_resp = await session.post(self._post_endpoint, json=post.dict())
            author_resp = await session.get(self._author_endpoint)
            raw_post = await post_resp.json()
            raw_authors = await author_resp.json()
            raw_post["author"] = await self._get_author_by_id(raw_post["userId"], raw_authors)
            return raw_post

    async def _detail_post(self, id_: int) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            post_resp = await session.get(self._post_endpoint + f"/{id_}")
            raw_post = await post_resp.json()
            raw_post["comments"] = await self._get_comments(id_)
            raw_post["author"] = await self._get_author(raw_post["userId"])
            return raw_post

    async def _get_author(self, id_: int) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self._author_endpoint + f"/{id_}")
            return await resp.json()

    async def _get_author_by_id(self, id_: int, raw_authors) -> Dict[str, Any]:
        for author in raw_authors:
            if author["id"] == id_:
                return author

    async def _get_comments(self, post_id: int):
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self._comment_endpoint + str(post_id))
            comments = await resp.json()
            return comments

    async def _match_authors_and_posts(self, raw_posts, raw_authors):
        for post in raw_posts:
            for author in raw_authors:
                if post["userId"] == author["id"]:
                    post["author"] = author

    def _convert_post(self, raw_post: Dict[str, Any]) -> Post:
        return Post(**raw_post)


class PostRepositoryFactory:
    def __init__(self):
        self._repo = None

    def __call__(self):
        if self._repo is None:
            self._repo = PostRepository()
        return self._repo


get_post_repository = PostRepositoryFactory()
