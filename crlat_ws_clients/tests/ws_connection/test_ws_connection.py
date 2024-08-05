import asyncio

from crlat_ws_clients.abc_base.domain_event import subscribe, publish
from crlat_ws_clients.clients.vis_client_model import vis_client_domain as vcd
from crlat_ws_clients.protocol_proxy.sockjs import sockjs_proxy as sjs
from crlat_ws_clients.transports.ws_transports import aio_ws_gateway as aiows
from crlat_ws_clients.transports.ws_transports import gevent_ws_gateway as gvntws
from crlat_ws_clients.utils.async_helpers import perform_sync
from crlat_ws_clients.utils.loggers import test_logger
from tests.mocks import MockListener

logger = test_logger.getChild(__name__)


def test_gevent_ws_connection():
    listener = MockListener()
    subscribe(listener.match_event, listener.apply_event)
    ws_handler = gvntws.GeventWsGateway(gvntws.GeventWsGateway.Created)
    connect_event = gvntws.GeventWsGateway.ConnectWsServer(
        url='wss://vis-stg2-coral.symphony-solutions.eu/generic/960/nyfcodek/websocket'
    )
    logger.debug(connect_event)
    publish(connect_event)
    logger.debug('')
    received_event_types = [e.__class__ for e in listener.received_events]

    publish(gvntws.GeventWsGateway.DisconnectWsServer())



def test_aiows_connection():
    listener = MockListener()
    subscribe(listener.match_event, listener.apply_event)
    ws_handler = aiows.create_ws_connection_handler()
    connect_event = aiows.AioWsGateway.ConnectWsServer(
        url='wss://vis-stg2-coral.symphony-solutions.eu/generic/960/nyfcodek/websocket'
    )
    logger.debug(connect_event)
    publish(connect_event)
    logger.debug('')
    received_event_types = [e.__class__ for e in listener.received_events]
    # perform_sync(asyncio.sleep(1))
    publish(aiows.AioWsGateway.DisconnectWsServer())

    # perform_sync(asyncio.sleep(3))
    assert aiows.AioWsGateway.WsGwConnectionInit in received_event_types
    assert aiows.AioWsGateway.WsGwConnectionEstablished in received_event_types



def test_sockjs_connection():
    listener = MockListener()
    subscribe(listener.match_event, listener.apply_event)
    sjs.create_sockjs()
    connect_event = sjs.SockJsProxy.ConnectSockJsServer(base_url='wss://vis-tst2-coral.symphony-solutions.eu/generic')
    logger.debug(connect_event)
    publish(connect_event)

    # perform_sync(asyncio.sleep(1))
    publish(sjs.SockJsProxy.DisconnectSockJsServer())

    received_event_types = [e.__class__ for e in listener.received_events]
    # perform_sync(asyncio.sleep(3))
    assert aiows.AioWsGateway.WsGwConnectionInit in received_event_types
    assert aiows.AioWsGateway.WsGwConnectionEstablished in received_event_types

def test_vis_connection():
    def vizz(ob_event_id=11369194):
        listener = MockListener()
        subscribe(listener.match_event, listener.apply_event)
        vis = vcd.create_vis_client_entity()
        vis.fire_event(vcd.VisClientEntity.ConnectVisServer,
                       base_url='wss://vis-tst2-coral.symphony-solutions.eu/generic')
        vis.fire_event(vcd.VisClientEntity.UnsubscribeVisMatch, openbet_id=ob_event_id)
        # vis.fire_event(
        #     vce.VisClientEntity.SubscribeVisMatch,
        #     openbet_id=ob_event_id
        # )
        # asyncio.get_event_loop().run_until_complete(asyncio.sleep(1))
        vis.fire_event(vcd.VisClientEntity.DisconnectVisServer)
        received_event_types = [e.__class__ for e in listener.received_events]
        assert aiows.AioWsGateway.WsGwConnectionInit in received_event_types
        assert aiows.AioWsGateway.WsGwConnectionEstablished in received_event_types

    vizz(ob_event_id=11449284)