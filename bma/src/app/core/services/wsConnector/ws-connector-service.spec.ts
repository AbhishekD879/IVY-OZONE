import { WsConnectorService } from './ws-connector.service';
import { WsConnector } from '@core/services/wsConnector/ws-connector';
describe('WsConnectorService', () => {
  let service: WsConnectorService;
  let windowRef;
  let device;
  let pubsub;
  let connection;
  let wsConnector;
  let callbacks;
  let ngZone;
  beforeEach(() => {
    callbacks = {};
    connection = {
      close: jasmine.createSpy(),
      on: jasmine.createSpy().and.callFake((method, cb) => {
        callbacks[method] = cb;
      }),
      once: jasmine.createSpy(),
      off: jasmine.createSpy(),
      emit: jasmine.createSpy(),
      connected: false
    };
    windowRef = {
      nativeWindow: {
        io: jasmine.createSpy().and.returnValue(connection)
      }
    };
    device = {};
    pubsub = {
      publish: jasmine.createSpy()
    };
    ngZone = {
      runOutsideAngular: jasmine.createSpy().and.callFake(fn => fn())
    };
    service = new WsConnectorService(windowRef, device, pubsub, ngZone);
  });
  it('should create wsConnector', () => {
    expect(service.create('test', {}) instanceof WsConnector).toBe(true);
  });
  it('should create wsConnector with options', () => {
    const connector: any = service.create('test', {
      timeout: 10000,
      reconnectionAttempts: 15,
      reconnectionDelay: 1000
    });
    expect(connector.options.timeout).toEqual(10000);
    expect(connector.options.reconnectionAttempts).toEqual(15);
    expect(connector.options.reconnectionDelay).toEqual(1000);
  });
  describe('WsConnector', () => {
    beforeEach(() => {
      wsConnector = service.create('test', {}, 'myModule');
    });
    describe('WsConnector connect', () => {
      it('should create new connection', () => {
        wsConnector.updateOptions({opt: true, opt2: false});
        wsConnector.removeOption('opt');
        wsConnector.addAnyMessagesHandler(() => {});
        wsConnector.connect();
        expect(windowRef.nativeWindow.io).toHaveBeenCalledWith('test', jasmine.objectContaining({
          opt2: false
        }));
      });
      it('should not create new connection while connecting', () => {
        wsConnector.connect();
        wsConnector.connect();
        expect(windowRef.nativeWindow.io).not.toHaveBeenCalledTimes(2);
      });
      it('should not create new connection if connected', () => {
        wsConnector.connect();
        callbacks.connect();
        connection.connected = true;
        wsConnector.connect();
        expect(windowRef.nativeWindow.io).not.toHaveBeenCalledTimes(2);
      });
      it('should not create new connection if reconnect started', () => {
        wsConnector.connect();
        connection.connected = true;
        callbacks.connect();
        wsConnector.reconnect();
        wsConnector.connect();
        expect(windowRef.nativeWindow.io).not.toHaveBeenCalledTimes(2);
      });
      it('should handle connect error', () => {
        wsConnector.connect();
        callbacks.connect();
        callbacks.connect_error('error');
        expect(pubsub.publish).toHaveBeenCalledWith('myModule.ws.connectionError');
      });
    });
    describe('WsConnector reconnect', () => {
      it('should reconnect', () => {
        wsConnector.connect();
        wsConnector.reconnect();
        expect(connection.close).toHaveBeenCalled();
      });
      it('should not reconnect if connected', () => {
        wsConnector.connect();
        connection.connected = true;
        wsConnector.reconnect();
        expect(connection.close).not.toHaveBeenCalled();
      });
      it('should not reconnect if reconnect started', () => {
        wsConnector.reconnect();
        wsConnector.reconnect();
        expect(connection.close).not.toHaveBeenCalledTimes(2);
      });
      it('should fire success connection event', () => {
        wsConnector.connect();
        callbacks.reconnect();
        expect(pubsub.publish).toHaveBeenCalledWith('myModule.ws.reconnectSuccess');
      });
      it('should fire reconnect attempt event', () => {
        wsConnector.connect();
        callbacks.reconnect_attempt();
        expect(pubsub.publish).toHaveBeenCalledWith('myModule.ws.reconnectAttempt');
      });
      it('should handle reconnect attempt event', () => {
        wsConnector.connect();
        callbacks.reconnect_failed();
        expect(pubsub.publish).toHaveBeenCalledWith('myModule.ws.reconnectError');
      });
    });
    describe('WsConnector events', () => {
      it('should add listener', () => {
        wsConnector.connect();
        wsConnector.addEventListener('onTest', () => {});
        expect(connection.on).toHaveBeenCalledWith('onTest', jasmine.any(Function));
      });
      it('should add once listener', () => {
        wsConnector.connect();
        wsConnector.addOnceEventListener('onceTest', () => {});
        expect(connection.once).toHaveBeenCalledWith('onceTest', jasmine.any(Function));
      });
      it('should remove listener', () => {
        wsConnector.connect();
        wsConnector.removeEventListener('removeTest', () => {});
        expect(connection.off).toHaveBeenCalledWith('removeTest', jasmine.any(Function));
        expect(connection.off).toHaveBeenCalledTimes(1);
      });
      it('should remove listeners', () => {
        wsConnector.connect();
        wsConnector.removeEventListener('removeTest', [() => {}, () => {}, () => {}]);
        expect(connection.off).toHaveBeenCalledWith('removeTest', jasmine.any(Function));
        expect(connection.off).toHaveBeenCalledTimes(3);
      });
      it('should emit event', () => {
        wsConnector.connect();
        connection.connected = true;
        wsConnector.emit('event', () => {});
        expect(connection.emit).toHaveBeenCalledWith('event', jasmine.any(Function));
      });
      it('should sub subscribe connect and then emit event ', () => {
        wsConnector.emit('event', () => {});
        wsConnector.connect();
        callbacks.connect();
        expect(connection.emit).toHaveBeenCalledWith('event', jasmine.any(Function));
      });
    });
    describe('WsConnector disconnect', () => {
      it('should disconnect', () => {
        wsConnector.connect();
        wsConnector.disconnect();
        expect(connection.close).toHaveBeenCalled();
      });
      it('should nor disconnect if not connected', () => {
        wsConnector.disconnect();
        expect(connection.close).not.toHaveBeenCalled();
      });
      it('should fire disconnect event', () => {
        wsConnector.connect();
        callbacks.disconnect();
        expect(pubsub.publish).toHaveBeenCalledWith('myModule.ws.disconnect');
      });
    });
  });
});