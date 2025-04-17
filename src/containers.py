from dependency_injector import containers, providers

from utils.hash_handler import HashHandler
from member.repository import MemberRepository
from member.service import MemberService


class Container(containers.DeclarativeContainer):
    wire_config = containers.WiringConfiguration(packages=["member"])

    hash_handler = providers.Singleton(HashHandler)

    member_repository = providers.Singleton(MemberRepository)
    member_service = providers.Singleton(MemberService, member_repository=member_repository, hash_handler=hash_handler)
