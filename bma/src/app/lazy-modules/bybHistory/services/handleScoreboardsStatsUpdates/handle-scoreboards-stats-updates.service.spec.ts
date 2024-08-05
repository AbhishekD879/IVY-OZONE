import { of } from 'rxjs';
import {
  HandleScoreboardsStatsUpdatesService
} from '@lazy-modules/bybHistory/services/handleScoreboardsStatsUpdates/handle-scoreboards-stats-updates.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { IScoreboardStatsUpdate } from '@bybHistoryModule/models/scoreboards-stats-update.model';

describe('HandleScoreboardsStatsUpdatesService', () => {
  let service: HandleScoreboardsStatsUpdatesService;

  let liveServConnectionService;
  let coreToolsService;
  let pubSubService;

  beforeEach(() => {
    liveServConnectionService = {
      connect: jasmine.createSpy().and.returnValue({
        subscribe: jasmine.createSpy('subscribe').and.callFake(cb => cb())
      }),
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      onDisconnect: jasmine.createSpy(),
      isDisconnected: jasmine.createSpy('isDisconnected'),
      subscribeToScoreboards: jasmine.createSpy('subscribeToScoreboards'),
      unsubscribeFromScoreboards: jasmine.createSpy('unsubscribeFromScoreboards'),
    };

    coreToolsService = {
      deepMerge: jasmine.createSpy('coreToolsService')
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };

    service = new HandleScoreboardsStatsUpdatesService(
      liveServConnectionService,
      coreToolsService,
      pubSubService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('should return observable of statistics event ids', () => {
    const eventId = '123456';
    service['$statisticsEventIds'] = of(eventId) as any;
    service.getStatisticsEventIds().subscribe((id: string) => {
      expect(id).toEqual(eventId);
    });
  });

  describe('subscribeForUpdates', () => {
    it('should call liveServConnectionService.connect', () => {
      service.subscribeForUpdates('12345');

      expect(service['callbacks']).toEqual({ handler: jasmine.any(Function) });
      expect(service['channels']).toEqual(['12345']);
      expect(liveServConnectionService.connect).toHaveBeenCalled();
      expect(liveServConnectionService.subscribeToScoreboards).toHaveBeenCalledWith('12345', jasmine.any(Function));
    });

    it('should call onUpdateCallback when update for event id exists', () => {
      service['channels'] = ['12345'];
      service['statsStore'].set('12345', {} as any);
      service.subscribeForUpdates('12345');

      expect(service['channels']).toEqual(['12345', '12345']);
      expect(liveServConnectionService.connect).toHaveBeenCalled();
      expect(liveServConnectionService.subscribeToScoreboards).toHaveBeenCalledWith('12345', jasmine.any(Function));
    });

    describe('updatesHandler', () => {
      let updateObj;

      beforeEach(() => {
        updateObj = {
          obEventId: '12345'
        };
      });

      it('should publish pubsub event UPDATE_BYB_BET and add event Id to storeMap', () => {
        service.subscribeForUpdates('12345');
        service['callbacks'].handler(updateObj);

        expect(service['callbacks']).toEqual({ handler: jasmine.any(Function) });
        expect(service['statsStore'].size).toEqual(1);
        expect(pubSubService.publish).toHaveBeenCalledWith('UPDATE_BYB_BET', {
          obEventId: '12345'
        });
      });

      it('should publish pubsub event UPDATE_BYB_BET and extend existing update', () => {
        coreToolsService.deepMerge.and.returnValue({ match: 'Manchester vs Liverpool', obEventId: '12345'});
        service.subscribeForUpdates('12345');
        service['statsStore'].set('12345', { match: 'Manchester vs Liverpool'} as any);

        service['callbacks'].handler(updateObj);

        expect(service['callbacks']).toEqual({ handler: jasmine.any(Function) });
        expect(service['statsStore'].size).toEqual(1);
        expect(coreToolsService.deepMerge).toHaveBeenCalledWith({ match: 'Manchester vs Liverpool'}, { obEventId: '12345' });
        expect(pubSubService.publish).toHaveBeenCalledWith('UPDATE_BYB_BET', { match: 'Manchester vs Liverpool', obEventId: '12345'});
        expect(service['statsStore'].get('12345')).toEqual({ match: 'Manchester vs Liverpool', obEventId: '12345'} as any);
      });

      it('should not publish pubsub event UPDATE_BYB_BET', () => {
        service['channels'] = ['123456'];
        service.subscribeForUpdates('123456');

        expect(pubSubService.publish).not.toHaveBeenCalled();
      });
    });
  });

  it('reconnect', () => {
    const handler = () => {};
    service['callbacks'] = { handler };
    service['channels'] = ['123'];
    service.unsubscribe = jasmine.createSpy('unsubscribe');
    service['updateConnection'] = jasmine.createSpy('updateConnection');

    service.reconnect();

    expect(liveServConnectionService.connect).toHaveBeenCalled();
    expect(liveServConnectionService.subscribeToScoreboards).toHaveBeenCalled();
    expect(service.unsubscribe).toHaveBeenCalled();
    expect(service['updateConnection']).toHaveBeenCalled();
  });

  describe('unsubscribe', () => {
    beforeEach(() => {
      service['callbacks'] = {
        handler: () => {}
      };
    });

    it('should call liveServConnectionService.unsubscribe', () => {
      service['channels'] = ['1235'];
      service['statsStore'].set('1235', {} as IScoreboardStatsUpdate);
      service.unsubscribe('1235');

      expect(liveServConnectionService.unsubscribeFromScoreboards).toHaveBeenCalledWith('1235', service['callbacks'].handler);
      expect(service['statsStore'].size).toEqual(1);
      expect(service['channels'].length).toEqual(1);
    });

    it('should call liveServConnectionService.unsubscribe and remove one id from channels array', () => {
      service['channels'] = ['1235', '1235'];
      service['statsStore'].set('1235', {} as IScoreboardStatsUpdate);
      service.unsubscribe('1235');

      expect(liveServConnectionService.unsubscribeFromScoreboards).toHaveBeenCalledWith('1235', service['callbacks'].handler);
      expect(service['statsStore'].size).toEqual(1);
      expect(service['channels'].length).toEqual(2);
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

    service['connection'] = { id: 1 } as any;
    expect(service['isConnectionValid']({ connected: true, id: 2 } as any)).toBeTruthy();

    service['connection'] = { id: 1 } as any;
    expect(service['isConnectionValid']({ connected: true, id: 1 } as any)).toBeFalsy();
  });

  describe('setDisconnectHandler', () => {
    it('should set onDisconnect LS handler with properly bound context', () => {
      service['setDisconnectHandler']();

      expect(liveServConnectionService.onDisconnect).toHaveBeenCalledWith(service['disconnectHandler']);
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
