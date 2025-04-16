from dependency_injector import containers, providers

from utils.hash_handler import HashHandler
from repositories.member import MemberRepository
from services.member import MemberService


class Container(containers.DeclarativeContainer):
    wire_config = containers.WiringConfiguration(packages=["routers"])

    hash_handler = providers.Singleton(HashHandler)

    member_repository = providers.Singleton(MemberRepository)
    member_service = providers.Singleton(MemberService, member_repository=member_repository, hash_handler=hash_handler)
