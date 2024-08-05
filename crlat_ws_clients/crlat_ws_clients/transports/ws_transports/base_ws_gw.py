import time

import asyncio
from collections import deque
from functools import singledispatch

from aiohttp import ClientSession

from crlat_ws_clients.abc_base.domain_entity import AbcDomainEntity, _handler
from crlat_ws_clients.abc_base.domain_event import DomainEvent
from crlat_ws_clients.transports.ws_transports.ws_events import ws_server_events as ws_srv
from crlat_ws_clients.utils.loggers import conn_logger

logger = conn_logger.getChild(__name__)


class BaseWsGateway(AbcDomainEntity):
    class Created(DomainEvent):
        pass

    class ConnectWsServer(DomainEvent):
        pass

    class SendWsMessage(DomainEvent):
        pass

    class DisconnectWsServer(DomainEvent):
        pass

    ### PUB ###

    class WsGwConnectionInit(DomainEvent):
        pass

    class WsGwConnectionEstablished(DomainEvent):
        pass

    class WsGwConnectionError(DomainEvent):
        pass

    class WsGwDisconnecting(DomainEvent):
        pass

    class WsGwDisconnected(DomainEvent):
        pass

    class WsGwIncomingSrvMsg(DomainEvent):
        pass

    class WsGwSrvConnClosed(DomainEvent):
        pass

    class WsGwSrvConnClosing(DomainEvent):
        pass

    _subscribe_events = [ConnectWsServer, DisconnectWsServer, SendWsMessage]
    def __init__(self, event=None, *args, **kwargs):
        self._i_will_survive = True
        self._client_session = None
        self._doing_sync_staff = False
        self._cached_async_actions = deque()
        super().__init__(event=event, *args, **kwargs)

    # def matcher(self, event):
    #     if event.__class__ in [self.ConnectWsServer, self.DisconnectWsServer, self.SendWsMessage]:
    #         return True
    #     return False

    def _connect(self, url):
        raise NotImplementedError()

    def _disconnect(self):
        raise NotImplementedError()

    def _send_raw(self, raw_msg):
        raise NotImplementedError()

    def apply_event(self, event):
        updated = mutate(event, self)
        self._increment_version()
        return updated


def mutate(event, obj):
    return _handler(event, obj)


@singledispatch
def _handler(event, entity):
    raise NotImplementedError(
        'No Handler implemention in "%s" for "%s"' % (
            entity.__class__.__qualname__,
            event.__class__.__qualname__,
        )
    )



@_handler.register(BaseWsGateway.Created)
def _(event, unused=None):
    assert unused is None
    if event.async_type=='gevent':
        ws_handler = GeventWsGateway(event)
    else:
        ws_handler = AioWsGateway(event)
    return ws_handler


@_handler.register(BaseWsGateway.ConnectWsServer)
def _(event, ws_handler):
    ws_handler._connect(event.url)
    return ws_handler


@_handler.register(BaseWsGateway.SendWsMessage)
def _(event, ws_handler: BaseWsGateway):
    ws_handler._send_raw(event.data)
    return ws_handler


@_handler.register(BaseWsGateway.DisconnectWsServer)
def _(event, ws_handler):
    ws_handler._disconnect()
    return ws_handler


@_handler.register(ws_srv.WsServerTextMessage)
def _(event, ws_handler: BaseWsGateway):
    ws_handler.fire_event(
        BaseWsGateway.WsGwIncomingSrvMsg,
        event_time=event.event_time,
        raw_data=event.source_message.data
    )
    return ws_handler


@_handler.register(ws_srv.WsServerClosed)
def _(event, ws_handler: BaseWsGateway):
    ws_handler._i_will_survive = False
    ws_handler.fire_event(BaseWsGateway.WsGwSrvConnClosed)
    return ws_handler


@_handler.register(ws_srv.WsServerClosing)
def _(event, ws_handler: BaseWsGateway):
    ws_handler.fire_event(BaseWsGateway.WsGwSrvConnClosed)
    return ws_handler


@_handler.register(ws_srv.WsServerClosing)
def _(event, ws_handler: BaseWsGateway):
    ws_handler.fire_event(BaseWsGateway.WsGwSrvConnClosed)
    return ws_handler
