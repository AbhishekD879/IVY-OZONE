import gevent
import time
import websocket

from crlat_ws_clients.transports.ws_transports.base_ws_gw import BaseWsGateway
from crlat_ws_clients.utils.loggers import conn_logger

logger = conn_logger.getChild(__name__)


class GeventWsGateway(BaseWsGateway):

    def __init__(self, *args, **kwargs):
        self._dispatcher = None
        super().__init__(*args, **kwargs)

    def _connect(self, url):
        def _inner_connect(url):
            ws = websocket.WebSocket()
            ws.connect(url)
            return ws

        def _dispatch_ws():
            previous = None
            duplicates_counter = 0
            while self._i_will_survive:
                msg = self._ws_session.recv()
                if msg == previous:
                    duplicates_counter += 1
                    continue
                elif duplicates_counter > 0:
                    logger.warning('Num copies: %s' % duplicates_counter)
                    previous = msg
                else:
                    duplicates_counter = 0
                time_received = time.time()
                logger.debug('<<<: %s' % msg[:100])
                self.fire_event(
                    self.WsGwIncomingSrvMsg,
                    event_time=time_received,
                    raw_data=msg
                )
                # previous = msg
                gevent.sleep(.1)
            if self._ws_session.connected:
                self._ws_session.close()
            self.fire_event(self.WsGwDisconnected)

        self.fire_event(
            self.WsGwConnectionInit,
            url=url,
        )
        try:
            self._ws_session = _inner_connect(url)
            self.fire_event(
                self.WsGwConnectionEstablished,
                url=url
            )
            self._dispatcher = gevent.spawn(_dispatch_ws)
        except Exception as err:
            self.fire_event(
                self.WsGwConnectionError,
                url=url,
                exception=err
            )
            logger.error('Exiting due to connection error')

    def _send_raw(self, raw_msg):
        logger.debug('>>>: %s' % raw_msg)
        return self._ws_session.send(raw_msg)

    def _disconnect(self):
        self._i_will_survive = False
        if self._dispatcher:
            self._dispatcher.kill()
        if self._ws_session.connected:
            self._ws_session.close()
        self.fire_event(self.WsGwDisconnected)
