import { of as observableOf, Observable, throwError } from 'rxjs';
import { InplayConnectionService } from './inplay-connection.service';
import { inplayConfig } from '@app/inPlay/constants/config';
import { EVENTS } from '@core/constants/websocket-events.constant';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { ACTIONS } from '@lazy-modules/awsFirehose/constant/aws-firehose.constant';

describe('InplayConnectionService', () => {
  let service: InplayConnectionService;

  let wsConnectorService;
  let pubSubService;
  let windowRefService;
  let awsService;

  beforeEach(() => {
    wsConnectorService = {
      create: jasmine.createSpy().and.returnValue({
        state$: observableOf(null),
        addAnyMessagesHandler: jasmine.createSpy('addAnyMessagesHandler'),
        connection: true,
        isConnected: jasmine.createSpy('isConnected'),
        connect: jasmine.createSpy('connect'),
        disconnect: jasmine.createSpy('disconnect')
      })
    };

    pubSubService = {
      subscribe: jasmine.createSpy(),
      publish: jasmine.createSpy(),
      API: pubSubApi
    };

    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy()
      }
    };
    awsService = {
      addAction: jasmine.createSpy(),
      API: ACTIONS
    };

    service = new InplayConnectionService(
      wsConnectorService,
      pubSubService,
      windowRefService,
      awsService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('setConnectionErrorState', () => {
    const state: any = {};
    service.setConnectionErrorState(state);
    expect(service.status.reconnectFailed).toBe(state);
  });

  it('addWsEventsListeners', () => {
    service.startConnection = jasmine.createSpy().and.returnValue(observableOf(null));
    pubSubService.subscribe.and.callFake((name: string, method: string | string[], callback: Function) => {
      callback();
    });
    service.addWsEventsListeners();

    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'inplayService', `${inplayConfig.moduleName}.${EVENTS.SOCKET_RECONNECT_ERROR}`, jasmine.any(Function)
    );
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'inplayService', `${inplayConfig.moduleName}.${EVENTS.SOCKET_RECONNECT_SUCCESS}`, jasmine.any(Function)
    );
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'inplayService', pubSubService.API.RELOAD_COMPONENTS, jasmine.any(Function)
    );
    expect(pubSubService.publish).toHaveBeenCalledWith('RELOAD_IN_PLAY');
    expect(service.status.reconnectFailed).toBeFalsy();
  });

  it('connectComponent (connection not created)', () => {
    service.connection = null;
    service.createConnection = jasmine.createSpy().and.callFake(() => {
      service.connection = { isConnected: () => false } as any;
    });
    service.startConnection = jasmine.createSpy().and.returnValue(observableOf(null));

    expect(service.connectComponent()).toEqual(jasmine.any(Observable));
    expect(service.createConnection).toHaveBeenCalled();
    expect(service.startConnection).toHaveBeenCalled();
  });

  it('connectComponent (connection created)', () => {
    service.connection = {
      isConnected: jasmine.createSpy().and.returnValue(false)
    } as any;
    service.startConnection = jasmine.createSpy().and.returnValue(observableOf(null));
    service.disconnectComponentTimeout = 345;

    expect(service.connectComponent()).toEqual(jasmine.any(Observable));
    expect(service.disconnectComponentTimeout).toBeNull();
    expect(service.startConnection).toHaveBeenCalled();
  });
  it('connectComponent (existing connection)', () => {
    service.connection = {
      isConnected: jasmine.createSpy().and.returnValue(true)
    } as any;
    service.startConnection = jasmine.createSpy().and.returnValue(observableOf(null));

    expect(service.connectComponent()).toEqual(jasmine.any(Observable));
  });

  it('disconnectComponent', () => {
    windowRefService.nativeWindow.setTimeout.and.callFake(cb => {
      cb(); // call setTimeout callback
    });

    service.disconnectSocket = jasmine.createSpy();
    service.disconnectComponent();

    expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(
      jasmine.any(Function), service.websocketDisconnectionTimeout
    );
    expect(service.disconnectSocket).toHaveBeenCalled();
    expect(service.connection).toBeFalsy();
    expect(service.disconnectComponentTimeout).toBeFalsy();
  });
  it('disconnectComponent when timout exists', () => {
    windowRefService.nativeWindow.setTimeout.and.callFake(cb => {
      cb(); // call setTimeout callback
    });
    service.disconnectComponentTimeout = 500;
    service.disconnectSocket = jasmine.createSpy();
    service.disconnectComponent();

    expect(windowRefService.nativeWindow.setTimeout).not.toHaveBeenCalledWith(
      jasmine.any(Function), service.websocketDisconnectionTimeout
    );
    expect(service.disconnectSocket).not.toHaveBeenCalled();
  });
  describe('#startConnection', () => {
    it('should connect', () => {
      service.connection = {
        isConnected: jasmine.createSpy().and.returnValue(true)
      } as any;
      service.addAwsEventListeners = jasmine.createSpy();
      service.addWsEventsListeners =  jasmine.createSpy();
      expect(service.startConnection()).toEqual(jasmine.any(Observable));
      expect(service.connection.isConnected).toHaveBeenCalled();

      service.connection = {
        isConnected: jasmine.createSpy().and.returnValue(false),
        connect: jasmine.createSpy().and.returnValue(observableOf(null))
      } as any;
      const connection = service.startConnection();
      expect(connection).toEqual(jasmine.any(Observable));
      expect(service.connection.isConnected).toHaveBeenCalled();
      expect(service.connection.connect).toHaveBeenCalled();
      expect(service.status.reconnectFailed).toBeFalsy();
      connection.subscribe();
      expect(service.addAwsEventListeners).toHaveBeenCalled();
      expect(service.addWsEventsListeners).toHaveBeenCalled();
    });
    it('should throw error', () => {
      const error = 'someError';
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');
      service.connection = {
        isConnected: jasmine.createSpy().and.returnValue(false)
      } as any;
      service.addWsEventsListeners = jasmine.createSpy('addWsEventsListeners');
      service.connection.connect = jasmine.createSpy().and.returnValue(throwError(error));

      service.startConnection().subscribe(successHandler, errorHandler);
      service.addAwsEventListeners = jasmine.createSpy();

      expect(successHandler).not.toHaveBeenCalled();
      expect(errorHandler).toHaveBeenCalled();
      expect(service.addAwsEventListeners).not.toHaveBeenCalled();
      expect(service.addWsEventsListeners).toHaveBeenCalled();
      expect(awsService.addAction).toHaveBeenCalledWith(awsService.API.INPLAY_WS_CONNECTION_FAILED, {
        error
      });
    });
  });

  it('listenForAllWebsocketMessages', () => {
    const updatedItemId = 123;
    const messageBody: any = { message: 'someMessage' };
    service.listenForAllWebsocketMessages(updatedItemId, messageBody);
    expect(pubSubService.publish).toHaveBeenCalledWith(
      'WS_EVENT_LIVE_UPDATE', [updatedItemId, messageBody]
    );
  });

  it('listenForAllWebsocketMessages with error', () => {
    const updatedItemId: any = 'error';
    const messageBody: any = { message: 'someMessage' };
    service.listenForAllWebsocketMessages(updatedItemId, messageBody);
    expect(pubSubService.publish).not.toHaveBeenCalled();
  });

  it('disconnectSocket', () => {
    const disconnect = jasmine.createSpy();
    service.connection = { disconnect } as any;
    service.disconnectSocket();
    expect(disconnect).toHaveBeenCalled();
    expect(service.connection).toBeNull();
    expect(service.disconnectComponentTimeout).toBeNull();
  });

  describe('addEventListener', () => {
    it('should call createConnection', () => {
      service.connection = null;
      service.createConnection = jasmine.createSpy();
      service.startConnection = jasmine.createSpy().and.returnValue({
        subscribe: () => {}
      });
      service.addEventListener('reconnect', () => {}, false);
      expect(service.createConnection).toHaveBeenCalled();
      expect(service.startConnection).toHaveBeenCalled();
    });
    it('should call addEventListener', () => {
      service.connection = { addEventListener: jasmine.createSpy() } as any;
      service.createConnection = jasmine.createSpy();
      service.startConnection = jasmine.createSpy().and.returnValue(observableOf(true));
      service.addEventListener('reconnect', () => {}, false);
      expect(service.connection.addEventListener).toHaveBeenCalled();
    });
    it('should call addOnceEventListener', () => {
      service.connection = { addOnceEventListener: jasmine.createSpy() } as any;
      service.createConnection = jasmine.createSpy();
      service.startConnection = jasmine.createSpy().and.returnValue(observableOf(true));
      service.addEventListener('reconnect', () => {}, true);
      expect(service.connection.addOnceEventListener).toHaveBeenCalled();
    });
  });
  it('removeEventListener', () => {
    const eventName = 'status';
    const handler = () => {};
    service.connection = { removeEventListener: jasmine.createSpy() } as any;
    service.removeEventListener(eventName, handler);
    expect(service.connection.removeEventListener).toHaveBeenCalledWith(eventName, handler);
  });

  describe('emitSocket', () => {
    let emitEvent,
      data;

    beforeEach(() => {
      emitEvent = 'reconnect';
      data = {};
    });

    it('should emit connection', () => {
      service.connection = { emit: jasmine.createSpy() } as any;
      service.emitSocket(emitEvent, data);
      expect(service.connection.emit).toHaveBeenCalledWith(emitEvent, data);
    });

    it('should not emit connection', () => {
      const emit = jasmine.createSpy('connection.emit');

      service.connection = { emit } as any;
      service.connection = undefined;

      service.emitSocket(emitEvent, data);
      expect(emit).not.toHaveBeenCalled();
    });
  });

  describe('#addAwsEventListeners', () => {
    beforeEach(() => {
      service.connection = {
        connection: jasmine.createSpyObj({
          on: jasmine.createSpy()
        })
      } as any;
    });
    it('when connection is not present', () => {
      service.connection = {} as any;
      service.addAwsEventListeners();
      expect(awsService.addAction).not.toHaveBeenCalled();
    });
    it('when connection is present', () => {
      service.addAwsEventListeners();
      expect(awsService.addAction).not.toHaveBeenCalledTimes(5);
    });

    it('on connect_error', () => {
      const error = 'someError';
      service.connection.connection.on.and.callFake((action, cb) => {
        if (action === 'connect_error') {
          cb(error);
        }
      });
      service.addAwsEventListeners();
      expect(awsService.addAction).toHaveBeenCalledWith(awsService.API.INPLAY_WS_CONNECTION_FAILED, {
        error
      });
    });
    it('on reconnect', () => {
      const attemp = 1;
      service.connection.connection.on.and.callFake((action, cb) => {
        if (action === 'reconnect') {
          cb(attemp);
        }
      });
      service.addAwsEventListeners();
      expect(awsService.addAction).toHaveBeenCalledWith(awsService.API.INPLAY_WS_RECONNECTION_SUCCESS, {
        attemp
      });
    });
    it('on reconnect_failed', () => {
      service.connection.connection.on.and.callFake((action, cb) => {
        if (action === 'reconnect_failed') {
          cb();
        }
      });
      service.addAwsEventListeners();
      expect(awsService.addAction).toHaveBeenCalledWith(awsService.API.INPLAY_WS_RECONNECTION_FAILED);
    });
    it('on reconnect_attempt', () => {
      const attemp = 15;
      service.connection.connection.on.and.callFake((action, cb) => {
        if (action === 'reconnect_attempt') {
          cb(attemp);
        }
      });
      service.addAwsEventListeners();
      expect(awsService.addAction).toHaveBeenCalledWith(awsService.API.INPLAY_WS_RECONNECTION_ATTEMP, {
        attemp
      });
    });
    it('on INPLAY_STRUCTURE', () => {
      const structure = {
        someData: 'someData'
      } as any;
      service.connection.connection.on.and.callFake((action, cb) => {
        if (action === 'INPLAY_STRUCTURE') {
          cb(structure);
        }
      });
      service.addAwsEventListeners();
      expect(awsService.addAction(awsService.API.FEATURED_WS_DATA_RECEIVED, {
        payloadSize: JSON.stringify(structure).length
      }));
    });
  });

  describe('#createConnection', () => {
    it('should subscribe on "connect" event', () => {
      wsConnectorService.create.and.returnValue({
        state$: observableOf('connect'),
        addAnyMessagesHandler: jasmine.createSpy()
      });
      service.createConnection();
      expect(awsService.addAction).toHaveBeenCalledWith(awsService.API.INPLAY_WS_CONNECTION_SUCCESS);
    });
  });
});
