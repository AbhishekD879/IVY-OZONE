import asyncio
import random
import time
from functools import singledispatch

from crlat_ws_clients.abc_base.domain_event import DomainEvent
from crlat_ws_clients.utils.loggers import test_logger

loop = asyncio.get_event_loop()
logger = test_logger.getChild(__name__)

class MockListener:

    def __init__(self, *args, **kwargs):
        self.received_events = []
    @staticmethod
    def match_event(*args, **kwargs):
        return True

    def apply_event(self, event):
        logger.info('%s received an event: %s' % (self.__class__.__qualname__, event))
        self.received_events.append(event)


class WsHandlerMock:
    _listeners = []

    def __init__(self, *args, **kwargs):
        pass

    class Created(DomainEvent):
        pass

    class AppendListener(DomainEvent):
        pass

    class ConnectToServer(DomainEvent):
        pass

    class ConnectionInit(DomainEvent):
        pass

    class ConnectionEstablished(DomainEvent):
        pass

    def _increment_version(self):
        pass

    def _connect(self, url):
        self.fire_event(self.ConnectionInit, url=url, event_time=time.time())
        # mock connection delay
        loop.run_until_complete(asyncio.sleep(random.uniform(.1, .4)))
        self.fire_event(self.ConnectionEstablished, url=url, event_time=time.time())

    def fire_event(self, event_class, *event_args, **event_kwargs):
        event = event_class(
            event_source=self.__class__.__qualname__,
            *event_args,
            **event_kwargs
        )
        for listener in self._listeners:
            listener.apply_event(event)

    def apply_event(self, event):
        updated = mutate(event, self)
        self._increment_version()
        return updated


def create_ws_connection_handler() -> WsHandlerMock:
    event = WsHandlerMock.Created()
    return _handler(event)


def create_listener() -> MockListener:
    event = WsHandlerMock.Created()
    return _handler(event)


def mutate(event, obj):
    return _handler(event, obj)


@singledispatch
def _handler(event, entity):
    raise NotImplementedError()


@_handler.register(WsHandlerMock.Created)
def _(event, unused=None):
    assert unused is None
    ws_handler = WsHandlerMock(event)
    return ws_handler


@_handler.register(WsHandlerMock.ConnectToServer)
def _(event, ws_handler):
    ws_handler._connect(event.url)
    return ws_handler
