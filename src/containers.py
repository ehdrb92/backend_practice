from dependency_injector import containers, providers

from src.config import Settings
from src.utils.auth_handler import AuthHandler
from src.member.repository import MemberRepository
from src.member.service import MemberService


class Container(containers.DeclarativeContainer):
    wire_config = containers.WiringConfiguration(packages=["member"])

    project_settings = providers.Singleton(Settings)

    auth_handler = providers.Singleton(AuthHandler)

    member_repository = providers.Singleton(MemberRepository)
    member_service = providers.Singleton(
        MemberService, member_repository=member_repository, auth_handler=auth_handler
    )
