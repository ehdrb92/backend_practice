from dependency_injector import containers, providers

from utils.auth_handler import AuthHandler
from member.repository import MemberRepository
from member.service import MemberService


class Container(containers.DeclarativeContainer):
    wire_config = containers.WiringConfiguration(packages=["member"])

    auth_handler = providers.Singleton(AuthHandler)

    member_repository = providers.Singleton(MemberRepository)
    member_service = providers.Singleton(MemberService, member_repository=member_repository, auth_handler=auth_handler)
