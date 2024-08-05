import time

import asyncio
from collections import deque
from functools import singledispatch

from aiohttp import ClientSession

from crlat_ws_clients.abc_base.domain_entity import AbcDomainEntity, _handler
from crlat_ws_clients.abc_base.domain_event import DomainEvent, publish, subscribe
from crlat_ws_clients.transports.ws_transports.base_ws_gw import BaseWsGateway
from crlat_ws_clients.transports.ws_transports.ws_events import ws_server_events as ws_srv
from crlat_ws_clients.utils.loggers import conn_logger

logger = conn_logger.getChild(__name__)


class AioWsGateway(BaseWsGateway):

    async def _dispatch_ws(self):
        # logger.debug('Starting Dispatch Loop')
        while self._i_will_survive:
            # logger.debug('Awaiting messages from server')
            msg = await self._ws_session.receive()
            self._doing_sync_staff = True
            time_received = time.time()
            # logger.debug('Got WS message type %s' % msg.type)
            srv_event_class = ws_srv.server_messages_map[msg.type]

            event = srv_event_class(
                event_time=time_received,
                source_message=msg,
            )
            self.apply_event(event)
            self._doing_sync_staff = False
            while len(self._cached_async_actions):
                action, args, kwargs = self._cached_async_actions.popleft()

                logger.debug('Doing %s(%s)' % (action, args))
                await action(*args, **kwargs)
        # logger.info('Dispatch loop closed')
        self._ws_session.close()
        self._client_session.close()
        # logger.info('FIRE: Disconnect event')
        self.fire_event(self.WsGwDisconnected)

    def _connect(self, url):
        self.fire_event(
            AioWsGateway.WsGwConnectionInit,
            url=url,
        )
        self._ws_session = asyncio.get_event_loop().run_until_complete(self._inner_connect(url))
        if self._ws_session:
            self.fire_event(
                AioWsGateway.WsGwConnectionEstablished,
                url=url
            )
            asyncio.get_event_loop().create_task(self._dispatch_ws())
        else:
            logger.error('Exiting due to connection error')

    def _disconnect(self):
        self.fire_event(self.WsGwDisconnecting)
        return self

    def _send_raw(self, raw_msg):

        if self._doing_sync_staff:
            logger.debug('Cached %s' % raw_msg)
            self._cached_async_actions.append((self._ws_session.send_str, (raw_msg,), {}))
        else:
            logger.debug('Sent %s' % raw_msg)
            asyncio.get_event_loop().run_until_complete(self._ws_session.send_str(raw_msg))

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


def create_ws_connection_handler() -> AioWsGateway:
    event = AioWsGateway.Created()
    return _handler(event)


@_handler.register(AioWsGateway.Created)
def _(event, unused=None):
    assert unused is None
    ws_handler = AioWsGateway(event)
    return ws_handler


@_handler.register(AioWsGateway.ConnectWsServer)
def _(event, ws_handler):
    ws_handler._connect(event.url)
    return ws_handler


@_handler.register(AioWsGateway.SendWsMessage)
def _(event, ws_handler: AioWsGateway):
    ws_handler._send_raw(event.data)
    return ws_handler


@_handler.register(AioWsGateway.DisconnectWsServer)
def _(event, ws_handler):
    ws_handler._disconnect()
    return ws_handler


@_handler.register(ws_srv.WsServerTextMessage)
def _(event, ws_handler: AioWsGateway):
    ws_handler.fire_event(
        AioWsGateway.WsGwIncomingSrvMsg,
        event_time=event.event_time,
        raw_data=event.source_message.data
    )
    return ws_handler


@_handler.register(ws_srv.WsServerClosed)
def _(event, ws_handler: AioWsGateway):
    ws_handler._i_will_survive = False
    ws_handler.fire_event(AioWsGateway.WsGwSrvConnClosed)
    return ws_handler


@_handler.register(ws_srv.WsServerClosing)
def _(event, ws_handler: AioWsGateway):
    ws_handler.fire_event(AioWsGateway.WsGwSrvConnClosed)
    return ws_handler


@_handler.register(ws_srv.WsServerClosing)
def _(event, ws_handler: AioWsGateway):
    ws_handler.fire_event(AioWsGateway.WsGwSrvConnClosed)
    return ws_handler
