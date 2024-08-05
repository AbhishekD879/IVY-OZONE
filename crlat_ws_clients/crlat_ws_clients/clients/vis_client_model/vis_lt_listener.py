import time
from functools import singledispatch

from crlat_ws_clients.abc_base.domain_entity import AbcDomainEntity, _handler
from crlat_ws_clients.abc_base.domain_event import DomainEvent
from crlat_ws_clients.clients.vis_client_model import vis_client_domain as vcd
from crlat_ws_clients.protocol_proxy.sockjs import sockjs_proxy as sjs
from crlat_ws_clients.transports.ws_transports import base_ws_gw as wsgw
from crlat_ws_clients.utils.loggers import lt_logger

logger = lt_logger


class VisLoadTestTListenerEntity(AbcDomainEntity):
    class Created(DomainEvent):
        pass

    _subscribe_events = [
        wsgw.BaseWsGateway.WsGwConnectionInit,
        wsgw.BaseWsGateway.WsGwConnectionError,
        wsgw.BaseWsGateway.WsGwConnectionEstablished,
        wsgw.BaseWsGateway.WsGwDisconnected,
        sjs.SockJsProxy.ConnectSockJsServer,
        sjs.SockJsProxy.DisconnectSockJsServer,
        # sjs.SockJsProxy.SendSockJsMessages,
        sjs.SockJsProxy.SockJsConnectionError,
        sjs.SockJsProxy.SockJsHeartBeat,
        sjs.SockJsProxy.SockJsOpenFrame,
        vcd.VisClientEntity.VisCliUnsubscribeFBMatch,
        vcd.VisClientEntity.VisCliSubscribeFBMatch,
        vcd.VisClientEntity.VisCliUnsubscribeTennisMatch,
        vcd.VisClientEntity.VisCliSubscribeTennisMatch,
        vcd.VisClientEntity.VisSrvMatchGeneric,
        vcd.VisClientEntity.VisSrvMatchStatistics,
        vcd.VisClientEntity.VisSrvMatchHistory,
        vcd.VisClientEntity.VisSrvMatchIncident,
        vcd.VisClientEntity.VisSrvMatchMapping,
        vcd.VisClientEntity.VisSrvMatchStatUpdate,
        vcd.VisClientEntity.VisSrvMatchUnknownMsg
    ]

    def __init__(self, event=None, *args, **kwargs):
        super().__init__(event=event, *args, **kwargs)
        event = event if event else self.Created()
        self._failure_hooks = event.failure_hooks if hasattr(event, 'failure_hooks') else []
        self._success_hooks = event.success_hooks if hasattr(event, 'success_hooks') else []
        self._state_history = {}
        self._state = 'Created'

    @property
    def state(self):
        return self._state

    def update_state(self, new_state: str, change_time_stamp=None):
        change_time_stamp = change_time_stamp if change_time_stamp else time.time()
        self._state_history.update({new_state: change_time_stamp})

    def find_state_time_by_name(self, state_name):
        return self._state_history.get(state_name)

    def get_last_update_time(self, ):
        return list(self._state_history.values())[-1]

    def get_time_from_state(self, state_name, untill=None):
        ws_state_time = self.find_state_time_by_name(state_name)
        if not ws_state_time:
            return 0
        untill = untill if untill else time.time()
        return untill - ws_state_time

    def fire_success(
            self,
            name='Unset',
            response_time=0,
            response_length=0
    ):
        # logger.debug('##SUCCESS## %s[%s]: %s' % (name, response_length, response_time))
        for hook in self._success_hooks:
            hook(
                request_type='WS',
                name=name,
                response_time=int(response_time * 1000),
                response_length=response_length
            )

    def fire_failure(
            self,
            name='Unset',
            response_time=0,
            exception=None
    ):
        # logger.debug('##FAILURE## %s: %s' % (name, response_time))
        for hook in self._failure_hooks:
            hook(
                request_type='WS',
                name=name,
                response_time=int(response_time * 1000),
                exception=exception
            )

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


@_handler.register(wsgw.BaseWsGateway.WsGwConnectionInit)
def _(event, ltt: VisLoadTestTListenerEntity):
    ltt.update_state(event.__class__.__name__, event.event_time)
    return ltt


@_handler.register(wsgw.BaseWsGateway.WsGwConnectionError)
def _(event, ltt: VisLoadTestTListenerEntity):
    previous = wsgw.BaseWsGateway.WsGwConnectionInit  # just in case name changed
    ltt.update_state(event.__class__.__name__, event.event_time)
    logger.warning(event.exception)
    host = event.url.split('/')[2]
    ltt.fire_failure(
        name='%s(%s)' % (event.__class__.__name__, host),
        response_time=ltt.get_time_from_state(
            previous.__name__,
            untill=event.event_time
        ),
        exception=event.exception
    )
    return ltt


@_handler.register(wsgw.BaseWsGateway.WsGwConnectionEstablished)
def _(event, ltt: VisLoadTestTListenerEntity):
    host = event.url.split('/')[2]
    ltt.fire_success(
        name='%s(%s)' % (event.__class__.__name__, host),
        response_time=event.event_time - ltt.get_last_update_time()
    )
    ltt.update_state(event.__class__.__name__, event.event_time)
    return ltt


@_handler.register(wsgw.BaseWsGateway.WsGwDisconnected)
def _(event, ltt: VisLoadTestTListenerEntity):
    return ltt


@_handler.register(sjs.SockJsProxy.ConnectSockJsServer)
def _(event, ltt: VisLoadTestTListenerEntity):
    return ltt


@_handler.register(sjs.SockJsProxy.DisconnectSockJsServer)
def _(event, ltt: VisLoadTestTListenerEntity):
    return ltt


@_handler.register(sjs.SockJsProxy.SendSockJsMessages)
def _(event, ltt: VisLoadTestTListenerEntity):
    return ltt


@_handler.register(sjs.SockJsProxy.SockJsConnectionError)
def _(event, ltt: VisLoadTestTListenerEntity):
    return ltt


@_handler.register(sjs.SockJsProxy.SockJsHeartBeat)
def _(event, ltt: VisLoadTestTListenerEntity):
    return ltt


@_handler.register(sjs.SockJsProxy.SockJsOpenFrame)
def _(event, ltt: VisLoadTestTListenerEntity):
    previous = wsgw.BaseWsGateway.WsGwConnectionEstablished  # just in case name changed
    ltt.update_state(event.__class__.__name__, event.event_time)
    ltt.fire_success(
        name='%s' % (event.__class__.__name__),
        response_time=ltt.get_time_from_state(
            previous.__name__,
            untill=event.event_time
        ),
        response_length=1  # size of 'o'
    )
    return ltt


@_handler.register(vcd.VisClientEntity.VisCliUnsubscribeFBMatch)
def _(event, ltt: VisLoadTestTListenerEntity):
    ltt.update_state(event.__class__.__name__, event.event_time)
    return ltt


@_handler.register(vcd.VisClientEntity.VisCliSubscribeFBMatch)
def _(event, ltt: VisLoadTestTListenerEntity):
    ltt.update_state(event.__class__.__name__, event.event_time)
    return ltt


@_handler.register(vcd.VisClientEntity.VisCliUnsubscribeTennisMatch)
def _(event, ltt: VisLoadTestTListenerEntity):
    ltt.update_state(event.__class__.__name__, event.event_time)
    return ltt


@_handler.register(vcd.VisClientEntity.VisCliSubscribeTennisMatch)
def _(event, ltt: VisLoadTestTListenerEntity):
    ltt.update_state(event.__class__.__name__, event.event_time)
    return ltt


@_handler.register(vcd.VisClientEntity.VisSrvUnsubscribe)
def _(event, ltt: VisLoadTestTListenerEntity):
    previous = vcd.VisClientEntity.VisCliUnsubscribeFBMatch
    ltt.update_state(event.__class__.__name__, event.event_time)
    ltt.fire_success(
        name='%s' % (event.__class__.__name__),
        response_time=ltt.get_time_from_state(
            previous.__name__,
            untill=event.event_time
        ),
        response_length=len(event.source_event.source_event.raw_data)
    )
    return ltt


def _process_subscribe_events(event, ltt: VisLoadTestTListenerEntity):
    ltt.fire_success(
        name='%s' % (event.__class__.__name__),
        response_time=event.event_time - ltt.get_last_update_time(),
        response_length=len(event.source_event.source_event.raw_data)
    )
    ltt.update_state(event.__class__.__name__, event.event_time)
    return ltt



@_handler.register(vcd.VisClientEntity.VisSrvMatchDetails)
def _(event, ltt: VisLoadTestTListenerEntity):
    return _process_subscribe_events(event, ltt)


@_handler.register(vcd.VisClientEntity.VisSrvMatchGeneric)
def _(event, ltt: VisLoadTestTListenerEntity):
    return _process_subscribe_events(event, ltt)


@_handler.register(vcd.VisClientEntity.VisSrvMatchHistory)
def _(event, ltt: VisLoadTestTListenerEntity):
    return _process_subscribe_events(event, ltt)


@_handler.register(vcd.VisClientEntity.VisSrvMatchStatistics)
def _(event, ltt: VisLoadTestTListenerEntity):
    return _process_subscribe_events(event, ltt)


@_handler.register(vcd.VisClientEntity.VisSrvMatchMapping)
def _(event, ltt: VisLoadTestTListenerEntity):
    return _process_subscribe_events(event, ltt)


@_handler.register(vcd.VisClientEntity.VisSrvMatchMapping)
def _(event, ltt: VisLoadTestTListenerEntity):
    return _process_subscribe_events(event, ltt)


@_handler.register(vcd.VisClientEntity.VisSrvMatchUnknownMsg)
def _(event, ltt: VisLoadTestTListenerEntity):
    logger.warning('Unknown message received raw data: %s' % event.source_event.source_event.raw_data)
    return ltt


@_handler.register(vcd.VisClientEntity.VisSrvMatchIncident)
def _(event, ltt: VisLoadTestTListenerEntity):
    ltt.fire_success(
        name='%s' % (event.__class__.__name__),
        response_time=0,
        response_length=len(event.source_event.source_event.raw_data)
    )
    return ltt


@_handler.register(vcd.VisClientEntity.VisSrvMatchStatUpdate)
def _(event, ltt: VisLoadTestTListenerEntity):
    ltt.fire_success(
        name='%s' % (event.__class__.__name__),
        response_time=0,
        response_length=len(event.source_event.source_event.raw_data)
    )
    return ltt


def create_vis_lt_listener(
        success_hooks=None,
        failure_hooks=None,
):
    event = VisLoadTestTListenerEntity.Created(
        success_hooks=success_hooks,
        failure_hooks=failure_hooks
    )
    vis_ltl = VisLoadTestTListenerEntity(event)
    return vis_ltl
