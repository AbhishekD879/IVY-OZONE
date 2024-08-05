import { Observable, Subject } from 'rxjs';

import { LiveServConnectionService } from './live-serv-connection.service';
import environment from '@environment/oxygenEnvConfig';
import { EVENTS } from '@core/constants/websocket-events.constant';

describe('LiveServConnectionService', () => {
  let service: LiveServConnectionService;
  let windowRefService;
  let deviceService;
  let pubSubService;
  let subscriptionsManagerService;
  let ngZone;

  beforeEach(() => {
    windowRefService = {
      nativeWindow: {
        io: jasmine.createSpy()
      }
    };
    deviceService = {
      isSafari: false
    };
    pubSubService = {
      publish: jasmine.createSpy()
    };
    subscriptionsManagerService = {
      create: jasmine.createSpy().and.returnValue({
        checkForSubscribe: jasmine.createSpy('checkForUnsubscribe'),
        checkForUnsubscribe: jasmine.createSpy('checkForUnsubscribe')
      })
    };

    ngZone = {
      runOutsideAngular: jasmine.createSpy().and.callFake(fn => fn())
    };

    spyOn(console, 'warn');

    service = new LiveServConnectionService(
      windowRefService,
      deviceService,
      pubSubService,
      subscriptionsManagerService,
      ngZone
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect(subscriptionsManagerService.create).toHaveBeenCalledTimes(1);
  });


  describe('connect', () => {
    let connection, oldConnection, connectHandler;

    beforeEach(() => {
      connection = { close: jasmine.createSpy('close') };
      oldConnection = { close: jasmine.createSpy('close') };
      connectHandler = jasmine.createSpy('connectHandler');
      (service as any).connection = oldConnection;
      (service as any).connectionObserver = null;
      spyOn(service as any, 'isConnected').and.returnValue(true);
      spyOn(service as any, 'createConnection').and.returnValue(connection);
      spyOn(service as any, 'addConnectionCallbacks');
    });

    describe('when current connection is connected', () => {
      it('should resolve with existing connection', () => {
        const result = service.connect();
        expect(result).toEqual(jasmine.any(Observable));
        result.subscribe(connectHandler);
        expect(service['isConnected']).toHaveBeenCalled();
        expect(connectHandler).toHaveBeenCalledWith(oldConnection);
        expect((service as any).createConnection).not.toHaveBeenCalled();
        expect((service as any).addConnectionCallbacks).not.toHaveBeenCalled();
      });
    });

    describe('when current connection is not connected', () => {
      beforeEach(() => {
        (service as any).isConnected.and.returnValue(false);
      });
      it('should return existing connectionObservable if it is created and is not completed', () => {
        (service as any).connectionObserver = { isStopped: false };
        expect(service.connect()).toEqual({ isStopped: false } as any);
        expect(service['isConnected']).toHaveBeenCalled();
        expect((service as any).createConnection).not.toHaveBeenCalled();
        expect((service as any).addConnectionCallbacks).not.toHaveBeenCalled();
      });

      describe('should return new connectionObservable and create new connection', () => {
        let result;
        it('if connectionObservable does not exist (no old connection close)', () => {
          (service as any).connection = null;
          result = service.connect();
        });

        it('if connectionObservable does not exist (and close existing connection)', () => {
          result = service.connect();
          expect(oldConnection.close).toHaveBeenCalled();
        });

        it('if connectionObservable is completed (and close existing connection)', () => {
          (service as any).connectionObservable = { isStopped: true };
          result = service.connect();
          expect(oldConnection.close).toHaveBeenCalled();
        });

        afterEach(() => {
          expect(service['isConnected']).toHaveBeenCalled();
          expect(result).toEqual(jasmine.any(Subject));
          expect((service as any).createConnection).toHaveBeenCalled();
          expect((service as any).addConnectionCallbacks).toHaveBeenCalled();
          expect(service['connection']).toEqual(connection);
          expect(service['connectionObserver']).toEqual(result);
        });
      });
    });
  });

  it('subscribe', () => {
    const channels: any[] = [{}];
    const handler = () => {};

    service['subscriptionsManager'] = {
      checkForSubscribe: jasmine.createSpy().and.returnValue(channels)
    } as any;
    service.connection = {
      on: jasmine.createSpy(),
      emit: jasmine.createSpy()
    } as any;

    service.subscribe(channels, handler);

    expect(service['subscriptionsManager'].checkForSubscribe).toHaveBeenCalledWith(channels);
    expect(service.connection.on).toHaveBeenCalledWith(channels[0], handler);
    expect(service.connection.emit).toHaveBeenCalledWith('subscribe', channels);
  });

  it('subscribe with showdown', () => {
    const channels: any[] = [{}];
    const handler = () => {};

    service['subscriptionsManager'] = {
      checkForSubscribe: jasmine.createSpy().and.returnValue(channels)
    } as any;
    service.connection = {
      on: jasmine.createSpy(),
      emit: jasmine.createSpy()
    } as any;

    service.subscribe(channels, handler, true);

    expect(service['subscriptionsManager'].checkForSubscribe).toHaveBeenCalledWith(channels);
    expect(service.connection.on).toHaveBeenCalledWith(channels[0], handler);
    expect(service.connection.emit).toHaveBeenCalledWith('subscribeshowdown', channels);
  });

  describe('subscribe and unsubscribe scoreboard', () => {
    let handler;
    let channel;

    beforeEach(() => {
      handler = () => {};
      channel = 'channel';

      service.connection = {
        on: jasmine.createSpy('on'),
        emit: jasmine.createSpy('emit'),
        removeListener: jasmine.createSpy('removeListener'),
        removeAllListeners: jasmine.createSpy('removeAllListeners')
      } as any;
    });

    it('should subscribe to scoreboards', () => {
      service['subscriptionsManager'] = {
        checkForSubscribe: jasmine.createSpy('checkForSubscribe').and.returnValue([channel])
      };
      service.subscribeToScoreboards(channel, handler);

      expect(service['subscriptionsManager'].checkForSubscribe).toHaveBeenCalledWith([channel]);
      expect(service.connection.on).toHaveBeenCalledWith(channel, handler);
      expect(service.connection.emit).toHaveBeenCalledWith('scoreboard', channel);
    });

    it('should Not subscribe to scoreboards if subscription with this event Id already exists', () => {
      service['subscriptionsManager'] = {
        checkForSubscribe: jasmine.createSpy('checkForSubscribe').and.returnValue([])
      };
      service.subscribeToScoreboards(channel, handler);

      expect(service['subscriptionsManager'].checkForSubscribe).toHaveBeenCalledWith([channel]);
      expect(service.connection.on).toHaveBeenCalledWith(channel, handler);
      expect(service.connection.emit).not.toHaveBeenCalled();
    });
    it('should Not subscribe to showDown if subscription with this event Id already exists', () => {
      service['subscriptionsManager'] = {
        checkForSubscribe: jasmine.createSpy('checkForSubscribe').and.returnValue([])
      };
      service.subscribeToShowdown(channel, handler,'showdownsubscribe');

      expect(service['subscriptionsManager'].checkForSubscribe).toHaveBeenCalledWith([channel]);
      expect(service.connection.on).toHaveBeenCalledWith(channel, handler);
      expect(service.connection.emit).not.toHaveBeenCalled();
    });
    it('should subscribe to showDown (case: subscribeToShowdown)', () => {
      service['subscriptionsManager'] = {
        checkForSubscribe: jasmine.createSpy('checkForSubscribe').and.returnValue([channel])
      };
      service.subscribeToShowdown(channel, handler,'subscribeshowdown');

      expect(service['subscriptionsManager'].checkForSubscribe).toHaveBeenCalledWith([channel]);
      expect(service.connection.on).toHaveBeenCalledWith(channel, handler);
      expect(service.connection.emit).toHaveBeenCalledWith('subscribeshowdown', ['channel']);
    });
    it('should subscribe to showDown', () => {
      service['subscriptionsManager'] = {
        checkForSubscribe: jasmine.createSpy('checkForSubscribe').and.returnValue([channel])
      };
      service.subscribeToShowdown(channel, handler,'test');

      expect(service['subscriptionsManager'].checkForSubscribe).toHaveBeenCalledWith([channel]);
      expect(service.connection.on).toHaveBeenCalledWith(channel, handler);
      expect(service.connection.emit).toHaveBeenCalledWith('test', channel);
    });
    it('should subscribe to showDown', () => {
      service['subscriptionsManager'] = {
        checkForSubscribe: jasmine.createSpy('checkForSubscribe').and.returnValue([channel])
      };
      service.subscribeToShowdown(channel, handler,'showdownsubscribe');

      expect(service['subscriptionsManager'].checkForSubscribe).toHaveBeenCalledWith([channel]);
      expect(service.connection.on).toHaveBeenCalledWith(channel, handler);
      expect(service.connection.emit).toHaveBeenCalledWith('showdownsubscribe', channel);
    });
    it('should unsubscribe from scoreboards', () => {
      service['subscriptionsManager'] = {
        checkForUnsubscribe: jasmine.createSpy('checkForUnsubscribe').and.returnValue([channel])
      };
      service.unsubscribeFromScoreboards(channel, handler);

      expect(service['subscriptionsManager'].checkForUnsubscribe).toHaveBeenCalledWith([channel]);
      expect(service.connection.removeListener).toHaveBeenCalledWith(channel, handler);
      expect(service.connection.emit).toHaveBeenCalledWith('unsubscribeScoreboard', channel);
    });

    it('should Not unsubscribe from scoreboards when some active subscription exists yet', () => {
      service['subscriptionsManager'] = {
        checkForUnsubscribe: jasmine.createSpy('checkForUnsubscribe').and.returnValue([])
      };
      service.unsubscribeFromScoreboards(channel, handler);

      expect(service['subscriptionsManager'].checkForUnsubscribe).toHaveBeenCalledWith([channel]);
      expect(service.connection.removeListener).toHaveBeenCalledWith(channel, handler);
      expect(service.connection.emit).not.toHaveBeenCalled();
    });
    it('should unsubscribe from showdown', () => {
      service['subscriptionsManager'] = {
        checkForUnsubscribe: jasmine.createSpy('checkForUnsubscribe').and.returnValue([channel])
      };
      service.unsubscribeFromShowdown([channel], handler);

      expect(service['subscriptionsManager'].checkForUnsubscribe).toHaveBeenCalledWith([channel]);
      expect(service.connection.removeAllListeners).toHaveBeenCalled();
      expect(service.connection.emit).toHaveBeenCalled();
    });
    it('should Not unsubscribe from showdown when channels is empty', () => {
      service['subscriptionsManager'] = {
        checkForUnsubscribe: jasmine.createSpy('checkForUnsubscribe').and.returnValue([])
      };
      service.unsubscribeFromShowdown([], handler);
      expect(service['subscriptionsManager'].checkForUnsubscribe).not.toHaveBeenCalledWith([]);
      expect(service.connection.removeAllListeners).not.toHaveBeenCalled();
      expect(service.connection.emit).not.toHaveBeenCalled();
    });
    it('should Not unsubscribe from showdown when some active subscription exists yet', () => {
      service['subscriptionsManager'] = {
        checkForUnsubscribe: jasmine.createSpy('checkForUnsubscribe').and.returnValue([])
      };
      service.unsubscribeFromShowdown([channel], handler);

      expect(service['subscriptionsManager'].checkForUnsubscribe).toHaveBeenCalledWith([channel]);
      expect(service.connection.removeAllListeners).toHaveBeenCalled();
      expect(service.connection.emit).not.toHaveBeenCalled();
    });
    it('should remove listener', () => {
      service.removeEventListner(channel, handler);
      expect(service.connection.removeListener).toHaveBeenCalledWith(channel, handler);
    });
    it('should remove listeners', () => {
      service.removeAllEventListner([channel]);
      expect(service.connection.removeAllListeners).toHaveBeenCalledWith([channel]);
    });
  });

  it('unsubscribe', () => {
    const channels: any[] = [{}];
    const handler = () => {};

    service['subscriptionsManager'] = {
      checkForUnsubscribe: jasmine.createSpy().and.returnValue(channels)
    } as any;
    service.connection = {
      removeListener: jasmine.createSpy(),
      emit: jasmine.createSpy()
    } as any;

    service.unsubscribe(channels, handler);

    expect(service['subscriptionsManager'].checkForUnsubscribe).toHaveBeenCalledWith(channels);
    expect(service.connection.removeListener).toHaveBeenCalledWith(channels[0], handler);
    expect(service.connection.emit).toHaveBeenCalledWith('unsubscribe', channels);
  });

  it('onDisconnect', () => {
    const callback = () => {};

    service.connection = {
      removeListener: jasmine.createSpy(),
      on: jasmine.createSpy()
    } as any;

    service.onDisconnect(callback);
    expect(service.connection.removeListener).toHaveBeenCalledWith('disconnect', callback);
    expect(service.connection.on).toHaveBeenCalledWith('disconnect', jasmine.any(Function));
  });

  it('disconnect', () => {
    service.connection = {
      io: { disconnect: jasmine.createSpy() }
    } as any;

    service.disconnect();
    expect(service.connection.io.disconnect).toHaveBeenCalled();
  });

  describe('createConnection should create new WS connection', () => {
    let result, expectedUrl, connection;
    beforeEach(() => {
      connection = Symbol('connection');
      spyOn(service as any, 'getPath').and.returnValue('/websocket');
      spyOn(service as any, 'getTransports').and.returnValue(['websocket']);
      spyOn(service as any, 'isPooling').and.returnValue(true);
      windowRefService.nativeWindow.io.and.returnValue(connection);
    });
    it('when isPooling is true', () => {
      expectedUrl = `${environment.LIVESERVEMS}:444`;
      result = service['createConnection']();
    });

    it('when isPooling is false', () => {
      expectedUrl = environment.LIVESERVEMS;
      (service as any).isPooling.and.returnValue(false);
      result = service['createConnection']();
    });
    afterEach(() => {
      expect(ngZone.runOutsideAngular).toHaveBeenCalled();
      expect(service['getPath']).toHaveBeenCalled();
      expect(service['getTransports']).toHaveBeenCalled();
      expect(service['isPooling']).toHaveBeenCalled();
      expect(windowRefService.nativeWindow.io).toHaveBeenCalledWith(
        expectedUrl, {
          path: '/websocket',
          transports: ['websocket'],
          upgrade: false,
          reconnectionDelay: 2000,
          forceNew: true,
          timeout: 10000,
          reconnectionAttempts: 10
        }
      );
      expect(result).toEqual(connection);
    });
  });

  describe('addConnectionCallbacks', () => {
    const callbacks = {};
    let connectionObserver, connection;

    beforeEach(() => {
      connection = {
        on: jasmine.createSpy().and.callFake((method, cb) => callbacks[method] = cb)
      };
      connectionObserver = {
        next: jasmine.createSpy('next'),
        complete: jasmine.createSpy('complete')
      };
      spyOn(service as any, 'connectHandler').and.callThrough();
      spyOn(service as any, 'connectErrorHandler').and.callThrough();
      spyOn(service as any, 'disconnectHandler').and.callThrough();
      spyOn(service as any, 'reconnectHandler').and.callThrough();
      spyOn(service as any, 'reconnectErrorHandler').and.callThrough();
      (service as any).moduleName = 'moduleName';
      (service as any).connection = connection;
      (service as any).connectionObserver = connectionObserver;
    });

    describe('should subscribe on connection events', () => {
      it('when device isSafari is false', () => {
        service['addConnectionCallbacks']();
        expect(service.connection.on).toHaveBeenCalledWith('disconnect', jasmine.any(Function));
      });
      it('when device isSafari is true', () => {
        deviceService.isSafari = true;
        service['addConnectionCallbacks']();
        expect(service.connection.on).not.toHaveBeenCalledWith('disconnect', jasmine.any(Function));
      });
      afterEach(() => {
        expect(service.connection.on).toHaveBeenCalledWith('connect', jasmine.any(Function));
        expect(service.connection.on).toHaveBeenCalledWith('connect_error', jasmine.any(Function));
      });
    });
    describe('should call', () => {
      beforeEach(() => {
        service['addConnectionCallbacks']();
      });
      it('connectHandler on connect event', () => {
        callbacks['connect']();
        expect((service as any).connectHandler).toHaveBeenCalled();
        expect(console.warn).toHaveBeenCalledWith('liveServe WS connect');
        expect(connectionObserver.next).toHaveBeenCalledWith(connection);
        expect(connectionObserver.next).toHaveBeenCalledBefore(connectionObserver.complete);
        expect(connectionObserver.complete).toHaveBeenCalled();
        expect(pubSubService.publish).toHaveBeenCalledWith(`moduleName.${EVENTS.SOCKET_CONNECT_SUCCESS}`, connection);
      });
      it('connectErrorHandler on connect_error event', () => {
        callbacks['connect_error']('error');
        expect((service as any).connectErrorHandler).toHaveBeenCalledWith('error');
        expect(console.warn).toHaveBeenCalledWith('LS MS connect error', 'error');
        expect(connectionObserver.next).not.toHaveBeenCalled();
        expect(connectionObserver.complete).toHaveBeenCalled();
      });

      describe('disconnectHandler on disconnect event', () => {
        it('which should subscribe to reconnect events', () => {
          callbacks['disconnect']('error');
          expect((service as any).disconnectHandler).toHaveBeenCalledWith('error');
          expect(console.warn).toHaveBeenCalledWith('LS MS disconnect', 'error');
          expect(service.connection.on).toHaveBeenCalledWith('reconnect', jasmine.any(Function));
          expect(service.connection.on).toHaveBeenCalledWith('reconnect_failed', jasmine.any(Function));
          expect((service as any).connectionObserver).toEqual(jasmine.any(Subject));
        });
        describe('which then should call', () => {
          beforeEach(() => {
            callbacks['disconnect']('error');
            (service as any).connectionObserver = connectionObserver;
          });
          describe('reconnectHandler on reconnect event', () => {
            beforeEach(() => {
              spyOn(service as any, 'isConnected').and.returnValue(false);
            });
            it('that should not resolve connection observable if connection is not yet connected', () => {
              callbacks['reconnect']();
              expect(connectionObserver.next).not.toHaveBeenCalled();
              expect(connectionObserver.complete).not.toHaveBeenCalled();
            });
            it('that should resolve connection observable if connection is connected', () => {
              (service as any).isConnected.and.returnValue(true);
              callbacks['reconnect']();
              expect(connectionObserver.next).toHaveBeenCalledWith(connection);
              expect(connectionObserver.next).toHaveBeenCalledBefore(connectionObserver.complete);
              expect(connectionObserver.complete).toHaveBeenCalled();
            });
            afterEach(() => {
              expect((service as any).reconnectHandler).toHaveBeenCalled();
              expect(console.warn).toHaveBeenCalledWith('liveServe WS reconnect');
              expect(pubSubService.publish).toHaveBeenCalledWith(`moduleName.${EVENTS.SOCKET_RECONNECT_SUCCESS}`);
            });
          });
          it('reconnectErrorHandler on reconnect_error event', () => {
            callbacks['reconnect_failed']('error');
            expect((service as any).reconnectErrorHandler).toHaveBeenCalledWith('error');
            expect(console.warn).toHaveBeenCalledWith('liveServe WS reconnect_failed', 'error');
            expect(connectionObserver.next).not.toHaveBeenCalled();
            expect(connectionObserver.complete).toHaveBeenCalled();
          });
        });
      });
    });
  });

  it('isConnected', () => {
    service.connection = null;
    expect(service.isConnected()).toBeFalsy();

    service.connection = { connected: false } as any;
    expect(service.isConnected()).toBeFalsy();

    service.connection = { connected: true } as any;
    expect(service.isConnected()).toBeTruthy();
  });

  it('getTransports', () => {
    service['isPooling'] = jasmine.createSpy().and.returnValue(true);
    expect(service['getTransports']()).toEqual(['polling']);
    expect(service['isPooling']).toHaveBeenCalled();

    service['isPooling'] = jasmine.createSpy().and.returnValue(false);
    expect(service['getTransports']()).toEqual(['websocket']);
    expect(service['isPooling']).toHaveBeenCalled();
  });

  it('getPath', () => {
    service['isPooling'] = jasmine.createSpy().and.returnValue(true);
    expect(service['getPath']()).toEqual('/polling');
    expect(service['isPooling']).toHaveBeenCalled();

    service['isPooling'] = jasmine.createSpy().and.returnValue(false);
    expect(service['getPath']()).toEqual('/websocket');
    expect(service['isPooling']).toHaveBeenCalled();
  });

  it('isPooling', () => {
    deviceService.osVersion = '4.3';
    deviceService.isNativeAndroid = true;
    expect(service['isPooling']()).toBeTruthy();

    deviceService.osVersion = '5';
    deviceService.isNativeAndroid = true;
    expect(service['isPooling']()).toBeFalsy();
  });
  describe('isDisconnected', () => {
    it('should return true for disconnected code', () => {
      expect(service.isDisconnected('transport close')).toBeTruthy();
      expect(service.isDisconnected('ping timeout')).toBeTruthy();
      expect(service.isDisconnected('transport error')).toBeTruthy();
    });
    it('should return false for  not disconnected code', () => {
      expect(service.isDisconnected('transport open')).toBeFalsy();
    });
  });
  it('should create event listeners for channels', () => {
    service.connection = {
      on: jasmine.createSpy(),
      emit: jasmine.createSpy()
    } as any;
    spyOn(service,'subscribeToShowdown');
    service.addEventListner(['123'], () => {});
    expect(service.subscribeToShowdown).toHaveBeenCalled();
  });

  describe('#closeConnection', () => {
    it('should close and complete the connection', () => {
      service.connection = {
        close: jasmine.createSpy(),
      } as any;
      const connectionObserver = {
        next: jasmine.createSpy('next'),
        complete: jasmine.createSpy('complete')
      };
      (service as any).connectionObserver = connectionObserver;
      service.closeConnection();
      expect(connectionObserver.complete).toHaveBeenCalled();
    });
  });
  describe('#subscribeToMatchCommentary', () => {
    let handler;
    let channel;
    beforeEach(() => {
      handler = () => { };
      channel = 'channel';
      service.connection = {
        on: jasmine.createSpy('on'),
        emit: jasmine.createSpy('emit'),
        removeListener: jasmine.createSpy('removeListener'),
        removeAllListeners: jasmine.createSpy('removeAllListeners')
      } as any;
    });
    it('should subscribe to subscribeToMatchCommentary', () => {
      service['subscriptionsManager'] = {
        checkForSubscribe: jasmine.createSpy('checkForSubscribe').and.returnValue([channel])
      };
      service.subscribeToMatchCommentary(channel, handler);
      expect(service['subscriptionsManager'].checkForSubscribe).toHaveBeenCalledWith([channel]);
      expect(service.connection.on).toHaveBeenCalledWith(channel, handler);
      expect(service.connection.emit).toHaveBeenCalledWith('subMatchCmtry', channel);
    });
    it('should Not subscribe to subscribeToMatchCommentary if subscription with this event Id already exists', () => {
      service['subscriptionsManager'].checkForSubscribe = jasmine.createSpy('checkForSubscribe').and.returnValue(null);
      service.subscribeToMatchCommentary(channel, handler);
      expect(service['subscriptionsManager'].checkForSubscribe).toHaveBeenCalledWith([channel]);
      expect(service.connection.on).not.toHaveBeenCalledWith(channel, handler);
      expect(service.connection.emit).not.toHaveBeenCalled();
    });
  });
  describe('#unsubscribeFromMatchCommentary', () => {
    let handler;
    let channel;
    beforeEach(() => {
      handler = () => { };
      channel = 'channel';
      service.connection = {
        on: jasmine.createSpy('on'),
        emit: jasmine.createSpy('emit'),
        removeListener: jasmine.createSpy('removeListener'),
        removeAllListeners: jasmine.createSpy('removeAllListeners')
      } as any;
    });
    it('should unsubscribe from unsubscribeFromMatchCommentary', () => {
      service['subscriptionsManager'] = {
        checkForUnsubscribe: jasmine.createSpy('checkForUnsubscribe').and.returnValue([channel])
      };
      service.unsubscribeFromMatchCommentary(channel, handler);
      expect(service['subscriptionsManager'].checkForUnsubscribe).toHaveBeenCalledWith([channel]);
      expect(service.connection.removeAllListeners).toHaveBeenCalledWith([channel]);
      expect(service.connection.emit).toHaveBeenCalledWith('unsubMatchCmtry', channel);
    });
    it('should Not unsubscribe from unsubscribeFromMatchCommentary when some active subscription exists yet', () => {
      service['subscriptionsManager'] = {
        checkForUnsubscribe: jasmine.createSpy('checkForUnsubscribe').and.returnValue(null)
      };
      service.unsubscribeFromMatchCommentary(channel, handler);
      expect(service['subscriptionsManager'].checkForUnsubscribe).toHaveBeenCalledWith([channel]);
      expect(service.connection.removeListener).not.toHaveBeenCalledWith(channel, handler);
      expect(service.connection.emit).not.toHaveBeenCalled();
    });
  });

  describe('subscribeBP and unsubscribeBP', () => {
    let handler;
    let channel;

    beforeEach(() => {
      handler = () => {};
      channel = 'channel';

      service.connection = {
        on: jasmine.createSpy('on'),
        emit: jasmine.createSpy('emit'),
        removeListener: jasmine.createSpy('removeListener'),
        removeAllListeners: jasmine.createSpy('removeAllListeners')
      } as any;
    });

    it('should Not subscribe betpacks when channels is empty', () => {
      service.subscribeBP([], handler);
      expect(service['subscriptionsManager'].checkForUnsubscribe).not.toHaveBeenCalledWith([]);
      expect(service.connection.removeAllListeners).not.toHaveBeenCalled();
      expect(service.connection.emit).not.toHaveBeenCalled();
    });

    it('should Not subscribe from betpack signpostings when some active subscription exists yet', () => {
      channel = ['channel'];
      service['subscriptionsManager'] = {
        checkForSubscribe: jasmine.createSpy('checkForSubscribe').and.returnValue(['channel'])
      };
      service.subscribeBP(channel, handler);
      expect(service['subscriptionsManager'].checkForSubscribe).toHaveBeenCalledWith(channel);
      expect(service.connection.on).toHaveBeenCalledWith(channel[0], handler);
      expect(service.connection.emit).toHaveBeenCalledWith('bet-pack-subscribe', channel);
    });

    it('should Not subscribe from betpacks when no active subscription exists yet', () => {
      service['subscriptionsManager'] = {
        checkForSubscribe: jasmine.createSpy('checkForSubscribe').and.returnValue([])
      };
      service.subscribeBP([channel], handler);
      expect(service['subscriptionsManager'].checkForSubscribe).toHaveBeenCalledWith([channel]);
      expect(service.connection.on).toHaveBeenCalled();
      expect(service.connection.emit).not.toHaveBeenCalled();
    });

    it('should Not unsubscribe from betpacks when channels is empty', () => {
      service.unsubscribeBP([], handler);
      expect(service['subscriptionsManager'].checkForUnsubscribe).not.toHaveBeenCalledWith([]);
      expect(service.connection.on).not.toHaveBeenCalled();
      expect(service.connection.emit).not.toHaveBeenCalled();
    });

    it('should Not unsubscribe from betpack signpostings when some active subscription exists yet', () => {
      channel = ['channel'];
      service['subscriptionsManager'] = {
        checkForUnsubscribe: jasmine.createSpy('checkForUnsubscribe').and.returnValue(['channel'])
      };
      service.unsubscribeBP(channel, handler);

      expect(service['subscriptionsManager'].checkForUnsubscribe).toHaveBeenCalledWith(channel);
      expect(service.connection.removeAllListeners).toHaveBeenCalledWith(channel[0]);
      expect(service.connection.emit).toHaveBeenCalledWith('bet-pack-unsubscribe', channel);
    });
    
    it('should Not unsubscribe from betpacks when no active subscription exists yet', () => {
      service['subscriptionsManager'] = {
        checkForUnsubscribe: jasmine.createSpy('checkForUnsubscribe').and.returnValue([])
      };
      service.unsubscribeBP([channel], handler);

      expect(service['subscriptionsManager'].checkForUnsubscribe).toHaveBeenCalledWith([channel]);
      expect(service.connection.removeAllListeners).toHaveBeenCalled();
      expect(service.connection.emit).not.toHaveBeenCalled();
    });
  });
  describe('#subscribeToMatchCommentary', () => {
    let handler;
    let channels;
    beforeEach(() => {
      handler = () => { };
      channels = ['mFACTS123'];
      service.connection = {
        on: jasmine.createSpy('on'),
        emit: jasmine.createSpy('emit'),
      } as any;
    });
    it('send request to LastFactCode', () => {
      service.connection.connected = true;
      service.sendRequestForLastMatchFact(channels, handler);
      expect(service.connection.on).toHaveBeenCalledWith(channels[0], handler);
      expect(service.connection.emit).toHaveBeenCalledWith('subLastMatchCode', channels);
    });
    it('should not send request to channels if connection.connected is false', () => {
      service.connection.connected = false;
      service.sendRequestForLastMatchFact(channels, handler);
      expect(service.connection.on).toHaveBeenCalledWith(channels[0], handler);
      expect(service.connection.emit).not.toHaveBeenCalledWith('subLastMatchCode', channels);
    });
    it('should not send request to channels if connection is null', () => {
      service.connection = null;
      service.sendRequestForLastMatchFact(channels, handler);
      expect(service.connection).toBeNull();
    });
  });
});
