from aiohttp import WSMsgType

from crlat_ws_clients.transports.ws_transports.ws_events.base_ws_events import BaseWsServerEvent


class WsServerPing(BaseWsServerEvent):
    aiohttp_type = WSMsgType.PING


class WsServerPong(BaseWsServerEvent):
    aiohttp_type = WSMsgType.PONG


class WsServerError(BaseWsServerEvent):
    aiohttp_type = WSMsgType.ERROR


class WsServerClose(BaseWsServerEvent):
    aiohttp_type = WSMsgType.CLOSE


class WsServerClosing(BaseWsServerEvent):
    aiohttp_type = WSMsgType.CLOSING


class WsServerClosed(BaseWsServerEvent):
    aiohttp_type = WSMsgType.CLOSED


class WsServerBinaryMessage(BaseWsServerEvent):
    aiohttp_type = WSMsgType.BINARY


class WsServerTextMessage(BaseWsServerEvent):
    aiohttp_type = WSMsgType.TEXT


server_messages_list = [
    WsServerPing,
    WsServerClose,
    WsServerClosing,
    WsServerClosed,
    WsServerError,
    WsServerTextMessage,
    WsServerBinaryMessage
]

server_messages_map = {
    msg_type.aiohttp_type: msg_type for msg_type in server_messages_list
}