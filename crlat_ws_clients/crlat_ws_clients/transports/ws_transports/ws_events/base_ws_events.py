from crlat_ws_clients.abc_base.domain_event import DomainEvent


class BaseWsServerEvent(DomainEvent):
    aiohttp_type = None
