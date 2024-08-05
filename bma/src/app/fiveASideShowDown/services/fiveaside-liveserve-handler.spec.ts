import { FiveASideLiveServeHandlerService } from './fiveaside-liveserve-handler';

describe('FiveASideLiveServeHandlerService', () => {
  let service: FiveASideLiveServeHandlerService;

  let liveServConnectionService;

  beforeEach(() => {
    liveServConnectionService = {
      connect: jasmine.createSpy().and.returnValue({
        subscribe: jasmine.createSpy('subscribe').and.callFake(cb => cb()),
      }),
      subscribeToShowdown: jasmine.createSpy('subscribeToShowdown'),
      unsubscribeFromShowdown: jasmine.createSpy('unsubscribeFromShowdown'),
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      onDisconnect: jasmine.createSpy(),
      isDisconnected: jasmine.createSpy('isDisconnected'),
      addEventListner: jasmine.createSpy('addEventListner'),
      removeEventListner: jasmine.createSpy('removeEventListner'),
      removeAllEventListner: jasmine.createSpy('removeAllEventListner')
    };

    service = new FiveASideLiveServeHandlerService(liveServConnectionService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('subscribe', () => {
    let channels;

    beforeEach(() => {
      channels = ['a', 'b'],
        service['callbacks'] = [] as any;
    });

    it('should call liveServConnectionService.connect', () => {
      spyOn(service as any, 'updateConnection');
      service.showDownSubscribe(channels, () => {
      }, 'emit');
      const channel = ['a', 'b'];
      expect(service['callbacks'][0]).toEqual({ channel, handler: jasmine.any(Function), 'emitKey': 'emit' } as any);
      expect(liveServConnectionService.connect).toHaveBeenCalled();
    });

    describe('#showDownSubscribe', () => {
      let onUpdateCallback;
      let updateObj;

      beforeEach(() => {
        onUpdateCallback = jasmine.createSpy('onUpdateCallback');
        updateObj = {};
      });

      it('should call onUpdateCallback', () => {
        service.showDownSubscribe(channels, onUpdateCallback, 'emit');
        (service['callbacks'][0] as any).handler(updateObj);
        const channel = ['a', 'b'];
        expect(service['callbacks'][0]).toEqual({ channel, handler: jasmine.any(Function), 'emitKey': 'emit' } as any);
        expect(onUpdateCallback).toHaveBeenCalled();
      });

      it('should not call onUpdateCallback', () => {
        service.showDownSubscribe(channels, null, 'emit');
        (service['callbacks'][0] as any).handler(updateObj);
        expect(onUpdateCallback).not.toHaveBeenCalled();
      });
    });
    it('should add event listeners', () => {
      spyOn(service as any, 'updateConnection');
      service.addEventListner(channels, () => { });
      expect(service['updateConnection']).toHaveBeenCalled();
    });
    it('should remove event listeners, when channel is available', () => {
      service['eventsHandlers'] = { channel: () => { } } as any;
      service.removeEventListner('channel');
      expect(liveServConnectionService.removeEventListner).toHaveBeenCalled();
    });
    it('should not remove event listeners, when channel is not available', () => {
      service['eventsHandlers'] = { channel: () => { } } as any;
      service.removeEventListner('channelx');
      expect(liveServConnectionService.removeEventListner).not.toHaveBeenCalled();
    });
    it('should remove all event listeners', () => {
      service.removeEventAllListner(channels);
      expect(liveServConnectionService.removeAllEventListner).toHaveBeenCalledWith(channels);
    });
  });

  it('reconnect', () => {
    service['callbacks'] = [{ channel: 'a' }, { channel: 'a' }, { channel: 'b' }] as any;
    service.unsubscribe = jasmine.createSpy('unsubscribe');
    service['updateConnection'] = jasmine.createSpy('updateConnection');
    service['showDownSubscribe'] = jasmine.createSpy('showDownSubscribe');
    service.reconnect();
    expect(liveServConnectionService.connect).toHaveBeenCalled();
    expect(service.unsubscribe).toHaveBeenCalled();
    expect(service['updateConnection']).toHaveBeenCalled();
  });

  describe('unsubscribe', () => {
    beforeEach(() => {
      service['callbacks'] = {
        handler: () => {
        }
      } as any;
    });
    it('should call liveServConnectionService.unsubscribe', () => {
      const channels = ['a', 'b'];
      service['callbacks']=[];
      service['callbacks'].push({ channel: 'a', handler: () => { }, emitKey: 'emit' });
      service.unsubscribe(channels, () => { });
      expect(service['callbacks'].length).toBe(0);
      expect(liveServConnectionService.unsubscribeFromShowdown).toHaveBeenCalled();
    });
    it('should call liveServConnectionService.unsubscribe', () => {
      const channels = ['a', 'b'];
      service['callbacks']=[];
      service['callbacks'].push({ channel: 'c', handler: () => { }, emitKey: 'emit' });
      service.unsubscribe(channels, () => { });
      expect(service['callbacks'].length).not.toBe(0);
    });
    it('should call liveServConnectionService.unsubscribe', () => {
      const channels = ['a', 'b'];
      service['callbacks']=[];
      service['callbacks'].push({ channel: 'b', handler: () => { }, emitKey: 'emit' });
      service.unsubscribe(channels, () => { });
      expect(service['callbacks'].length).toBe(0);
      expect(liveServConnectionService.unsubscribeFromShowdown).toHaveBeenCalled();
    });
    it('should not call liveServConnectionService.unsubscribe', () => {
      const channels = [];
      service.unsubscribe(channels, () => { });
      expect(liveServConnectionService.unsubscribeFromShowdown).not.toHaveBeenCalled();
    });
  });

  describe('updateConnection', () => {
    beforeEach(() => {
      service['isConnectionValid'] = jasmine.createSpy().and.returnValue(true);
      service['setDisconnectHandler'] = jasmine.createSpy();
    });
    it('should call setDisconnectHandler', () => {
      const connection: any = {};
      service['updateConnection'](connection);
      expect(service['isConnectionValid']).toHaveBeenCalledWith(connection);
      expect(service['setDisconnectHandler']).toHaveBeenCalled();
    });
    it('should not call setDisconnectHandler', () => {
      (service['isConnectionValid'] as jasmine.Spy).and.returnValue(false);
      const connection: any = {};
      service['updateConnection'](connection);
      expect(service['isConnectionValid']).toHaveBeenCalledWith(connection);
      expect(service['setDisconnectHandler']).not.toHaveBeenCalled();
    });
  });

  it('isConnectionValid', () => {
    expect(service['isConnectionValid'](null)).toBeFalsy();

    service['connection'] = null;
    expect(service['isConnectionValid']({ connected: false } as any)).toBeFalsy();

    service['connection'] = null;
    expect(service['isConnectionValid']({ connected: true } as any)).toBeTruthy();

    service['connection'] = { id: 1 };
    expect(service['isConnectionValid']({ connected: true, id: 2 } as any)).toBeTruthy();

    service['connection'] = { id: 1 };
    expect(service['isConnectionValid']({ connected: true, id: 1 } as any)).toBeFalsy();
  });

  describe('setDisconnectHandler', () => {
    it('should set onDisconnect LS handler with properly bound context', () => {
      liveServConnectionService.onDisconnect.and.callFake(cb => cb());
      liveServConnectionService.isDisconnected.and.returnValue(true);
      spyOn(service, 'reconnect');
      service['setDisconnectHandler']();

      expect(liveServConnectionService.onDisconnect).toHaveBeenCalledWith(service['disconnectHandler']);
      expect(liveServConnectionService.isDisconnected).toHaveBeenCalled();
      expect(service.reconnect).toHaveBeenCalled();
    });
  });

  describe('disconnectHandler', () => {
    it('should disconnect on disconnection message', () => {
      service['reconnect'] = jasmine.createSpy();
      liveServConnectionService.isDisconnected = jasmine.createSpy('isDisconnected').and.returnValue(true);
      service['disconnectHandler']('transport error');
      expect(service['reconnect']).toHaveBeenCalled();
    });
    it('should`t disconnect on not disconnection message', () => {
      service['reconnect'] = jasmine.createSpy();
      liveServConnectionService.isDisconnected = jasmine.createSpy('isDisconnected').and.returnValue(false);
      service['disconnectHandler']('transport open');
      expect(service['reconnect']).not.toHaveBeenCalled();
    });
  });
});
