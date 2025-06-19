from datetime import datetime
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from post.interface.post_repo import IPostRepository
from post.interface.comment_repo import ICommentRepository
from post.schemas import (
    CreatePostRequest,
    CreatePostResponse,
    SavePost,
    GetPostResponse,
    GetPostListResponse,
    UpdatePostRequest,
    UpdatePostResponse,
    CreateCommentRequest,
    CreateCommentResponse,
    SaveComment,
    GetCommentResponse,
    UpdateCommentRequest,
    UpdateCommentResponse
)


class PostService:
    def __init__(
        self,
        post_repository: IPostRepository,
        comment_repository: ICommentRepository,
    ):
        self.post_repository = post_repository
        self.comment_repository = comment_repository

    ############################# 게시물 관련 메서드 #############################

    async def create_post(
        self, session: AsyncSession, create_post_request: CreatePostRequest, publisher_id: str,
    ) -> CreatePostResponse:
        """게시물 생성"""
        save_post = SavePost(
            member_id=publisher_id,
            title=create_post_request.title,
            content=create_post_request.content,
        )

        post = await self.post_repository.save(session, save_post)

        return CreatePostResponse(id=post.id)

    async def get_post(self, session: AsyncSession, post_id: str) -> GetPostResponse:
        """게시물 조회"""
        post = await self.post_repository.find_by_id(session, post_id)
        return GetPostResponse(
            id=post.id,
            publisher_name=post.member.name,
            title=post.title,
            content=post.content,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )

    async def get_posts(
        self, session: AsyncSession, offset: int = 0, limit: int = 10
    ) -> List[GetPostListResponse]:
        """게시물 목록 조회"""
        posts = await self.post_repository.find_all(session, offset, limit)
        return [GetPostListResponse(
            id=post.id,
            publisher_name=post.member.name,
            title=post.title,
            created_at=post.created_at,
            ) for post in posts
        ]

    async def update_post(
        self, session: AsyncSession, post_id: str, update_post_request: UpdatePostRequest, publisher_id: str,
    ) -> UpdatePostResponse:
        """게시물 수정"""
        _post = await self.post_repository.find_by_id(session, post_id)

        if _post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="게시물을 찾을 수 없습니다.",
            )
        if _post.member_id != publisher_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="게시물 수정 권한이 없습니다.",
            )
        
        save_post = SavePost(
            id=_post.id,
            member_id=publisher_id,
            title=update_post_request.title,
            content=update_post_request.content,
            like_count=_post.like_count,
            created_at=_post.created_at,
        )

        post = await self.post_repository.save(session, save_post)

        return post

    async def delete_post(self, session: AsyncSession, post_id: str, publisher_id: str) -> None:
        """게시물 삭제"""
        _post = await self.post_repository.find_by_id(session, post_id)

        if _post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="게시물을 찾을 수 없습니다.",
            )
        if _post.member_id != publisher_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="게시물 수정 권한이 없습니다.",
            )
        
        save_post = SavePost(
            id=_post.id,
            member_id=_post.member_id,
            title=_post.title,
            content=_post.content,
            like_count=_post.like_count,
            created_at=_post.created_at,
            is_deleted=True
        )

        await self.post_repository.save(session, save_post)

    async def toggle_post_like(
        self,
        session: AsyncSession,
        member_id: str,
        post_id: str,
    ) -> None:
        """게시물 좋아요 토글"""
        # 좋아요 상태 확인
        if await self.post_repository.is_liked(session, member_id, post_id):
            await self.post_repository.dec_like_count(session, member_id, post_id)
        else:
            await self.post_repository.inc_like_count(session, member_id, post_id)

    ############################# 댓글 관련 메서드 #############################

    async def create_comment(
        self, session: AsyncSession, post_id: str, publisher_id: str, create_comment_request: CreateCommentRequest
    ) -> CreateCommentResponse:
        """댓글 생성"""
        save_comment = SaveComment(
            member_id=publisher_id,
            post_id=post_id,
            content=create_comment_request.content
        )
        comment = await self.comment_repository.save(session, save_comment)

        return CreateCommentResponse(id=comment.id)

    async def get_comments(
        self, session: AsyncSession, post_id: str, offset: int = 0, limit: int = 50
    ) -> List[GetCommentResponse]:
        """댓글 목록 조회"""
        comments = await self.comment_repository.find_all(
            session, post_id, offset, limit
        )
        return [
            GetCommentResponse(
                id=comment.id,
                publisher_name=comment.member.name,
                content=comment.content,
                created_at=comment.created_at,
                updated_at=comment.updated_at
            ) for comment in comments
        ]

    async def update_comment(
        self, session: AsyncSession, post_id: str, comment_id: str, publisher_id: str, update_comment_request: UpdateCommentRequest
    ) -> UpdateCommentResponse:
        """댓글 수정"""
        _comment = await self.comment_repository.find_by_id(session, comment_id)

        if _comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="댓글을 찾을 수 없습니다.",
            )
        if _comment.member_id != publisher_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="댓글 수정 권한이 없습니다.",
            )
        if _comment.post_id != post_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="댓글에 대한 게시물 정보가 올바르지 않습니다."
            )
        
        save_comment = SaveComment(
            id=_comment.id,
            member_id=_comment.member_id,
            post_id=_comment.post_id,
            content=update_comment_request.content,
            like_count=_comment.like_count,
            created_at=_comment.created_at
        )

        comment = await self.comment_repository.save(session, save_comment)

        return UpdateCommentResponse(id=comment.id)

    async def delete_comment(self, session: AsyncSession, post_id: str, comment_id: str, publisher_id: str) -> None:
        """댓글 삭제"""
        _comment = await self.comment_repository.find_by_id(session, comment_id)

        if _comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="댓글을 찾을 수 없습니다.",
            )
        if _comment.member_id != publisher_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="댓글 수정 권한이 없습니다.",
            )
        if _comment.post_id != post_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="댓글에 대한 게시물 정보가 올바르지 않습니다."
            )
        
        save_comment = SaveComment(
            id=_comment.id,
            member_id=_comment.member_id,
            post_id=_comment.post_id,
            content=_comment.content,
            like_count=_comment.like_count,
            created_at=_comment.created_at,
            is_deleted=True
        )

        comment = await self.comment_repository.save(session, save_comment)

    async def toggle_comment_like(
        self,
        session: AsyncSession,
        member_id: str,
        comment_id: str,
    ) -> None:
        """댓글 좋아요 토글"""
        # 좋아요 상태 확인
        if await self.comment_repository.is_liked(session, member_id, comment_id):
            await self.comment_repository.dec_like_count(session, member_id, comment_id)
        else:
            await self.comment_repository.inc_like_count(session, member_id, comment_id)
        await session.commit()
