import asyncio
from collections import deque
from functools import singledispatch

from crlat_ws_clients.abc_base.domain_entity import AbcDomainEntity, _handler
from crlat_ws_clients.abc_base.domain_event import DomainEvent
from crlat_ws_clients.protocol_proxy.sockjs import sockjs_proxy as sjsp
from crlat_ws_clients.utils.loggers import domain_logger

logger = domain_logger.getChild(__name__)

try:
    import ujson as json
except ImportError:
    import json


class VisClientEntity(AbcDomainEntity):
    class Created(DomainEvent):
        pass

    # SUB Events #
    ## SockJs ##
    supported_server_events = [
        sjsp.SockJsProxy.SockJsUnknown,
        sjsp.SockJsProxy.SockJsOpenFrame,
        sjsp.SockJsProxy.SockJsHeartBeat,
        sjsp.SockJsProxy.SockJsClose,
        sjsp.SockJsProxy.SockJsArray,
        sjsp.SockJsProxy.SockJsConnectionError
    ]

    ## User events ##

    class VisCliConnectServer(DomainEvent):
        pass

    class VisCliDisconnectServer(DomainEvent):
        pass

    class VisSrvConnectionError(DomainEvent):
        pass

    class VisCliSubscribeFBMatch(DomainEvent):
        pass

    class VisCliUnsubscribeFBMatch(DomainEvent):
        pass

    class VisCliSubscribeTennisMatch(DomainEvent):
        pass

    class VisCliUnsubscribeTennisMatch(DomainEvent):
        pass


    supported_app_events = [
        VisCliConnectServer,
        VisCliDisconnectServer,
        VisCliSubscribeFBMatch,
        VisCliUnsubscribeFBMatch,
        VisCliSubscribeTennisMatch,
        VisCliUnsubscribeTennisMatch,
    ]

    subscribe_list = supported_server_events + supported_app_events

    # PUB Events #
    ## Match Events ##

    class VisSrvMatchDetails(DomainEvent):
        vis_msg_id = 'details'

    class VisSrvMatchGeneric(DomainEvent):
        vis_msg_id = 'generic'

    class VisSrvMatchStatistics(DomainEvent):
        vis_msg_id = 'statistics'

    class VisSrvMatchHistory(DomainEvent):
        vis_msg_id = 'history'

    class VisSrvMatchIncident(DomainEvent):
        vis_msg_id = 'incident'

    class VisSrvUnsubscribe(DomainEvent):
        vis_msg_id = 'unsubscribe'

    class VisSrvMatchMapping(DomainEvent):
        vis_msg_id = 'mapping'

    class VisSrvMatchStatUpdate(DomainEvent):
        vis_msg_id = 'statUpdate'

    class VisSrvMatchUnknownMsg(DomainEvent):
        vis_msg_id = 'unknown'

    vis_srv_events_map = {
        e.vis_msg_id: e for e in [
            VisSrvUnsubscribe,
            VisSrvMatchDetails,
            VisSrvMatchGeneric,
            VisSrvMatchStatistics,
            VisSrvMatchHistory,
            VisSrvMatchIncident,
            VisSrvMatchMapping,
            VisSrvMatchStatUpdate,
            VisSrvMatchUnknownMsg
        ]
    }

    def __init__(self, event=None, *args, **kwargs):
        super().__init__(event=event, *args, **kwargs)
        sjs_event = sjsp.SockJsProxy.Created(application=event.application)
        self._sockjs_entity = sjsp.SockJsProxy(event=sjs_event)
        self._msg_cache = deque()  # Cache client requests when connection is not ready
        # ToDo: deprecate below
        self._sockjs_ready = False  # True after SockJsOpenFrame
        self._subscribed_events = {}

    _subscribe_events = supported_server_events + supported_app_events

    def fire_event(self, event_class, *event_args, **event_kwargs):
        logger.debug('Sent %s' %event_class.__qualname__)
        event = event_class(
            event_source=self.__class__.__qualname__,
            *event_args,
            **event_kwargs
        )
        self._app.publish(event)

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


@_handler.register(VisClientEntity.Created)
def _(event, unused=None):
    assert unused is None
    vis = VisClientEntity(event)
    return vis


@_handler.register(VisClientEntity.VisCliConnectServer)
def _(event, vis: VisClientEntity):
    vis.fire_event(
        sjsp.SockJsProxy.ConnectSockJsServer,
        base_url=event.base_url,
        source_event=event
    )
    return vis


@_handler.register(VisClientEntity.VisCliUnsubscribeFBMatch)
def _(event, vis: VisClientEntity):
    vis.fire_event(
        sjsp.SockJsProxy.SendSockJsMessages,
        data=json.dumps(
            {
                'unsubscribeOB': {
                    'openBetId': str(event.openbet_id)
                }
            }
        ),
        source_event=event
    )
    return vis


@_handler.register(VisClientEntity.VisCliSubscribeFBMatch)
def _(event, vis: VisClientEntity):
    vis.fire_event(
        sjsp.SockJsProxy.SendSockJsMessages,
        data=json.dumps(
            {
                'subscribeOB': {
                    'openBetId': str(event.openbet_id)
                }
            }
        ),
        source_event=event
    )
    return vis


@_handler.register(VisClientEntity.VisCliUnsubscribeTennisMatch)
def _(event, vis: VisClientEntity):
    vis.fire_event(
        sjsp.SockJsProxy.SendSockJsMessages,
        data=json.dumps(
            {
                'unsubscribeOB': str(event.openbet_id)
            }
        ),
        source_event=event
    )
    return vis


@_handler.register(VisClientEntity.VisCliSubscribeTennisMatch)
def _(event, vis: VisClientEntity):
    vis.fire_event(
        sjsp.SockJsProxy.SendSockJsMessages,
        data=json.dumps(
            {
                'subscribeOB': str(event.openbet_id)
            }
        ),
        source_event=event
    )
    return vis


@_handler.register(VisClientEntity.VisCliDisconnectServer)
def _(event, vis: VisClientEntity):

    vis.fire_event(
        sjsp.SockJsProxy.DisconnectSockJsServer,
        source_event=event
    )
    return vis


@_handler.register(sjsp.SockJsProxy.SockJsOpenFrame)
def _(event, vis: VisClientEntity):
    vis._sockjs_ready = True
    # vis.publish_cached()
    return vis


@_handler.register(sjsp.SockJsProxy.SockJsArray)
def _(event, vis: VisClientEntity):
    logger.debug('Got msg: %s' % repr(event))
    for data_item in event.data_array:
        dict_data = json.loads(data_item)
        for k, v in dict_data.items():
            event_type = vis.vis_srv_events_map.get(k, vis.VisSrvMatchUnknownMsg)
            logger.debug('firing %s' % event_type.__qualname__)
            vis.fire_event(
                event_type,
                data=v,
                event_time=event.event_time,
                source_event=event
            )
    return vis


@_handler.register(sjsp.SockJsProxy.SockJsHeartBeat)
def _(event, vis: VisClientEntity):
    logger.debug('Got msg: %s' % repr(event))
    return vis


@_handler.register(sjsp.SockJsProxy.SockJsClose)
def _(event, vis: VisClientEntity):
    logger.debug('Got msg: %s' % repr(event))
    return vis


@_handler.register(sjsp.SockJsProxy.SockJsUnknown)
def _(event, vis: VisClientEntity):
    logger.debug('Got msg: %s' % repr(event))
    return vis


@_handler.register(sjsp.SockJsProxy.SockJsConnectionError)
def _(event, vis: VisClientEntity):
    vis.fire_event(
        vis.VisSrvConnectionError,
        excetion=event.exception,
        source_message=event
    )
    return vis
