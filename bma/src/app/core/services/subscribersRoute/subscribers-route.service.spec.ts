import { SubscribersRouteService } from './subscribers-route.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { fakeAsync, tick } from '@angular/core/testing';

describe('SubscribersRouteService', () => {
  let service: SubscribersRouteService;
  let pubsub;
  let liveServe;
  let callbacks;
  let data;
  let newData;
  let eventListener;

  beforeEach(() => {
    data = {
      module: 'myModule',
      channel: ['E001', 'M002']
    };
    newData = {
      module: 'myModule',
      channel: ['E001', 'M002', 'E003']
    };
    callbacks = {};
    pubsub = {
      API: pubSubApi,
      subscribe: jasmine.createSpy().and.callFake((subscriber, method, callback) => {
        callbacks[method] = callback;
      })
    };
    liveServe = {
      psRegister: jasmine.createSpy().and.callFake((subscriber, callback, updates, msg) => {
        eventListener = callback;
      })
    };

    service = new SubscribersRouteService(pubsub, liveServe);
  });

  it('constructor', () => {
    expect(service).toBeDefined();
  });

  it('should init', () => {
    service.init();
    expect(pubsub.subscribe).toHaveBeenCalledWith(
      'SubscribersRouteService',
      pubsub.API.SUBSCRIBE_LS,
      jasmine.any(Function)
    );
    expect(pubsub.subscribe).toHaveBeenCalledWith(
      'SubscribersRouteService',
      pubsub.API.UNSUBSCRIBE_LS,
      jasmine.any(Function)
    );
    expect(pubsub.subscribe).toHaveBeenCalledWith(
      'SubscribersRouteService',
      pubsub.API.APP_IS_LOADED,
      jasmine.any(Function)
    );
  });

  it('should subscribe liveServe events', () => {
    service.init();
    callbacks[pubsub.API.SUBSCRIBE_LS](data);
    callbacks[pubsub.API.APP_IS_LOADED]();
    callbacks[pubsub.API.SUBSCRIBE_LS](newData);
    expect(liveServe.psRegister).toHaveBeenCalledWith('oxygenApp', jasmine.any(Function), jasmine.any(Array), '0');
  });

  it('should not subscribe liveServe events if there no updates', () => {
    service.init();
    callbacks[pubsub.API.APP_IS_LOADED]();
    expect(liveServe.psRegister).not.toHaveBeenCalledWith('oxygenApp', jasmine.any(Function), jasmine.any(Array), '0');
  });

  it('should unsubscribe liveServe events', () => {
    service.init();
    callbacks[pubsub.API.SUBSCRIBE_LS](data);
    callbacks[pubsub.API.APP_IS_LOADED]();
    callbacks[pubsub.API.UNSUBSCRIBE_LS]();
    expect(liveServe.psRegister).toHaveBeenCalledWith('oxygenApp', jasmine.any(Function), jasmine.any(Array), '0');
  });

  it('should dispatch document event in case of liveServe updates', fakeAsync(() => {
    let testEventFired = false;
    const func = () => {
      testEventFired = true;
    };
    document.addEventListener('LIVE_SERVE_UPDATE', func);
    service.init();
    callbacks[pubsub.API.SUBSCRIBE_LS](data);
    callbacks[pubsub.API.APP_IS_LOADED]();
    eventListener([{
      payload: '{"test":true}'
    }]);
    tick(500);
    expect(testEventFired).toBe(true);
  }));

  describe('unsubscribeEventHandler', () => {
    it('should unsubscribe from group', () => {
      service['updates'] = {
        'sb': {
          'all': ['ch1']
        },
        'live-serve-module': {
          'football': ['ch2'],
          'tennis': ['ch3'],
        }
      };
      service['cache'] = ['ch1', 'ch2', 'ch3'];
      service['unsubscribeEventHandler']({module: 'live-serve-module', group: 'tennis'});

      expect(service['updates']['live-serve-module']['tennis']).toBeUndefined();
      expect(service['cache']).toEqual(['ch1', 'ch2']);
    });

    it('should unsubscribe from module', () => {
      service['updates'] = {
        'sb': {
          'all': ['ch1']
        },
        'live-serve-module': {
          'football': ['ch2'],
          'tennis': ['ch3'],
        }
      };
      service['cache'] = ['ch1', 'ch2', 'ch3'];
      service['unsubscribeEventHandler']({ module: 'live-serve-module' });

      expect(service['updates']['live-serve-module']).toBeUndefined();
      expect(service['cache']).toEqual(['ch1']);
    });

    it('should unsubscribe from module by name', () => {
      service['updates'] = {
        'sb': {
          'all': ['ch1']
        },
        'live-serve-module': {
          'football': ['ch2'],
          'tennis': ['ch3'],
        }
      };
      service['cache'] = ['ch1', 'ch2', 'ch3'];
      service['unsubscribeEventHandler']('live-serve-module');

      expect(service['updates']['live-serve-module']).toBeUndefined();
      expect(service['cache']).toEqual(['ch1']);
    });
  });

  describe('cacheCheck', () => {
    let updData;

    beforeEach(() => {
      service['updates'] = {};
      service['cache'] = ['s01', 's02'];

      updData = {
        events: ['s02', 's03', 's04'],
        module: 'moduleName'
      };
      service['subscribeHandler'] = jasmine.createSpy('subscribeHandler');
    });

    it('should set updates in proper group', () => {
      service['cacheCheck'](updData.events, updData.module, 'football');
      service['cacheCheck'](updData.events, 'moduleName2');

      expect(service['updates'][updData.module]['football']).toEqual(updData.events);
      expect(service['cache']).toEqual(['s01', 's02', 's03', 's04']);
      expect(service['subscribeHandler']).toHaveBeenCalled();
    });

    it('should set updates in all group', () => {
      service['cache'] = ['s01', 's02', 's03', 's04'];
      service['updates'] = {
        'moduleName': {
          'all': ['s02', 's03', 's04']
        }
      };
      service['cacheCheck'](updData.events, updData.module);

      expect(service['updates'][updData.module]['all']).toEqual(updData.events);
      expect(service['cache']).toEqual(['s01', 's02', 's03', 's04']);
      expect(service['subscribeHandler']).not.toHaveBeenCalled();
    });
  });
});
