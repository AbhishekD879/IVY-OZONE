import { HandleLiveServeUpdatesService } from './handle-live-serve-updates.service';
import * as _ from 'underscore';

describe('HandleLiveServeUpdatesService', () => {
  let service: HandleLiveServeUpdatesService;

  let liveServConnectionService;

  beforeEach(() => {
    liveServConnectionService = {
      connect: jasmine.createSpy().and.returnValue({
        subscribe: jasmine.createSpy('subscribe').and.callFake(cb => cb())
      }),
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      onDisconnect: jasmine.createSpy(),
      isDisconnected: jasmine.createSpy('isDisconnected')
    };

    service = new HandleLiveServeUpdatesService(liveServConnectionService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('subscribe', () => {
    let channels;

    beforeEach(() => {
      channels = ['a', 'b'];
    });

    it('should call liveServConnectionService.connect', () => {
      service.subscribe(channels, () => {
      });

      expect(service['callbacks']).toEqual({ channels, handler: jasmine.any(Function) });
      expect(liveServConnectionService.connect).toHaveBeenCalled();
    });

    describe('updatesHandler', () => {
      let onUpdateCallback;
      let updateObj;

      beforeEach(() => {
        onUpdateCallback = jasmine.createSpy('onUpdateCallback');
        updateObj = {
          type: 'MESSAGE',
          channel: { id: 0, type: '' },
          message: 'test'
        };
      });

      it('should call onUpdateCallback', () => {
        service.subscribe(channels, onUpdateCallback);
        service['callbacks'].handler(updateObj);

        expect(service['callbacks']).toEqual({ channels, handler: jasmine.any(Function) });
        expect(onUpdateCallback).toHaveBeenCalled();
      });

      it('should not call onUpdateCallback', () => {
        service.subscribe(channels, null);
        service['callbacks'].handler(updateObj);

        expect(onUpdateCallback).not.toHaveBeenCalled();
      });

      it('should handle update.type !== "MESSAGE"', () => {
        updateObj.type = 'TEST';
        spyOn(_, 'isFunction');

        service.subscribe(channels, null);
        service['callbacks'].handler(updateObj);

        expect(onUpdateCallback).not.toHaveBeenCalled();
        expect(_.isFunction).not.toHaveBeenCalled();
      });
    });
  });

  it('reconnect', () => {
    service['callbacks'] = { channels: [] };
    service.unsubscribe = jasmine.createSpy('unsubscribe');
    service['updateConnection'] = jasmine.createSpy('updateConnection');

    service.reconnect();

    expect(liveServConnectionService.connect).toHaveBeenCalled();
    expect(liveServConnectionService.subscribe).toHaveBeenCalled();
    expect(service.unsubscribe).toHaveBeenCalled();
    expect(service['updateConnection']).toHaveBeenCalled();
  });

  describe('unsubscribe', () => {
    beforeEach(() => {
      service['callbacks'] = {
        handler: () => {
        }
      };
    });

    it('should call liveServConnectionService.unsubscribe', () => {
      const channels = ['a', 'b'];

      service.unsubscribe(channels);

      expect(liveServConnectionService.unsubscribe).toHaveBeenCalledWith(channels, service['callbacks'].handler);
    });

    it('should not call liveServConnectionService.unsubscribe', () => {
      const channels = [];

      service.unsubscribe(channels);

      expect(liveServConnectionService.unsubscribe).not.toHaveBeenCalled();
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
