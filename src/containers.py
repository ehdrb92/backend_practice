from dependency_injector import containers, providers

from config import Settings
from utils.auth_handler import AuthHandler
from member.repository.member_orm import MemberORMRepository
from member.service.member import MemberService
from post.repository.post_orm import PostORMRepository
from post.repository.comment_orm import CommentORMRepository
from post.service.post import PostService


class Container(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)

    auth_handler = providers.Factory(AuthHandler, settings=settings)

    member_repository = providers.Factory(MemberORMRepository)
    member_service = providers.Factory(
        MemberService, member_repository=member_repository, auth_handler=auth_handler
    )

    post_repository = providers.Factory(PostORMRepository)
    comment_repository = providers.Factory(CommentORMRepository)
    post_service = providers.Factory(
        PostService,
        post_repository=post_repository,
        comment_repository=comment_repository,
    )
