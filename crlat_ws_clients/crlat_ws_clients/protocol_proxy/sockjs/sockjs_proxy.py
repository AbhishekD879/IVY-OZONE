import random
import string
from collections import deque
from functools import singledispatch

from crlat_ws_clients.abc_base.domain_entity import AbcDomainEntity, _handler
from crlat_ws_clients.abc_base.domain_event import DomainEvent
from crlat_ws_clients.transports.ws_transports import base_ws_gw as wsgw
# from crlat_ws_clients.transports.ws_transports.aio_ws_gateway import create_ws_connection_handler
from crlat_ws_clients.transports.ws_transports.gevent_ws_gateway import GeventWsGateway
from crlat_ws_clients.utils.loggers import domain_logger

logger = domain_logger.getChild(__name__)

try:
    import ujson as json
except ImportError:
    import json


def build_sockjs_url(base_url):
    return '%s/%s/%s/websocket' % (
        base_url.lstrip('/'),
        random.randint(0, 999),  # Server instance id
        ''.join([random.choice(string.ascii_lowercase + string.digits) for i in range(6)])  # Frame ID
    )


class SockJsProxy(AbcDomainEntity):
    class Created(DomainEvent):
        pass

    ### SUB Events ###
    class ConnectSockJsServer(DomainEvent):
        pass

    class DisconnectSockJsServer(DomainEvent):
        pass

    class SendSockJsMessages(DomainEvent):
        pass

    _subscribe_events = [
        ConnectSockJsServer,
        DisconnectSockJsServer,
        SendSockJsMessages,
        wsgw.BaseWsGateway.WsGwIncomingSrvMsg,
        wsgw.BaseWsGateway.WsGwDisconnecting,
        wsgw.BaseWsGateway.WsGwConnectionError
    ]

    ### PUB Events ###
    class SockJsConnectionError(DomainEvent):
        type_prefix = None

    class SockJsUnknown(DomainEvent):
        type_prefix = None

    class SockJsOpenFrame(DomainEvent):
        type_prefix = 'o'

    class SockJsHeartBeat(DomainEvent):
        type_prefix = 'h'

    class SockJsClose(DomainEvent):
        type_prefix = 'c'

    class SockJsArray(DomainEvent):
        type_prefix = 'a'

    _sockjs_known_msgs = [
        SockJsOpenFrame,
        SockJsHeartBeat,
        SockJsClose,
        SockJsArray,
    ]
    _sockjs_msg_map = {msg_type.type_prefix: msg_type for msg_type in _sockjs_known_msgs}

    def __init__(self, event, *args, **kwargs):
        super().__init__(event, *args, **kwargs)
        self._received_open_frame = False
        self._user_events_cache = deque()

    def _recognize_sockjs_event_type(self, msg_first_char):
        return self._sockjs_msg_map.get(msg_first_char, self.SockJsUnknown)

    def _cache_event(self, event_type, **kwargs):
        logger.debug('Cached: %s' % event_type.__qualname__)
        self._user_events_cache.append((event_type, kwargs))

    def _publish_cached_events(self):
        logger.debug('Num cached: %s' % len(self._user_events_cache))
        while len(self._user_events_cache)>0:
            event_type, event_kwargs = self._user_events_cache.popleft()
            logger.debug('Publishing: %s' % event_type.__qualname__)
            self.fire_event(event_type, **event_kwargs)

    def _connect_sockjs(self, base_url):
        GeventWsGateway(GeventWsGateway.Created(application=self._app))
        self.fire_event(wsgw.BaseWsGateway.ConnectWsServer, url=build_sockjs_url(base_url))

    def _disconnect_sockjs(self):
        self.fire_event(wsgw.BaseWsGateway.DisconnectWsServer)

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


@_handler.register(SockJsProxy.Created)
def _(event, unused=None):
    assert unused is None
    sockjs = SockJsProxy(event)
    return sockjs


@_handler.register(SockJsProxy.ConnectSockJsServer)
def _(event, sockjs: SockJsProxy):
    sockjs._connect_sockjs(event.base_url)
    return sockjs


@_handler.register(SockJsProxy.SendSockJsMessages)
def _(event, sockjs: SockJsProxy):
    ws_event_type = wsgw.BaseWsGateway.SendWsMessage
    event_kwargs = {
        'data': json.dumps([event.data]),
        'source_event': event
    }
    if sockjs._received_open_frame:
        sockjs.fire_event(ws_event_type, **event_kwargs)
    else:
        sockjs._cache_event(ws_event_type, **event_kwargs)
    return sockjs


@_handler.register(SockJsProxy.DisconnectSockJsServer)
def _(event, sockjs: SockJsProxy):
    sockjs._disconnect_sockjs()
    return sockjs


@_handler.register(wsgw.BaseWsGateway.WsGwDisconnecting)
def _(event, sockjs: SockJsProxy):
    # sockjs._disconnect_sockjs()
    return sockjs


@_handler.register(wsgw.BaseWsGateway.WsGwConnectionError)
def _(event, sockjs: SockJsProxy):
    sockjs.fire_event(
        sockjs.SockJsConnectionError,
        exception=event.exception,
        source_message=event
    )
    return sockjs


@_handler.register(wsgw.BaseWsGateway.WsGwIncomingSrvMsg)
def _(event, sockjs: SockJsProxy):
    # logger.debug(event)
    source_data = event.raw_data.strip()
    data_array = []
    sockjs_msg_type = sockjs.SockJsUnknown
    logger.debug('Got msg: %s' % repr(event))
    if len(source_data) > 0:
        type_prefix = source_data[0]
        sockjs_msg_type = sockjs._recognize_sockjs_event_type(type_prefix)

        logger.debug('Parsed as: %s' % sockjs_msg_type.__qualname__)
        if len(source_data) > 1:
            # ToDo: fire Parsing error event on json parsing error
            data_array = json.loads(source_data[1:])
        if sockjs_msg_type == sockjs.SockJsOpenFrame:
            sockjs._received_open_frame = True
            sockjs._publish_cached_events()
    sockjs.fire_event(sockjs_msg_type, data_array=data_array, source_event=event)
    return sockjs
