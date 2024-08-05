import { fakeAsync, tick } from '@angular/core/testing';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { NavigationStart, NavigationEnd } from '@angular/router';
import decorateTick from './app-decorator';

declare let window: any;

window.setTimeout = jasmine.createSpy('setTimeout');

describe('decorateTick', () => {
  let baseMethod;
  let appRef;
  let ngZone;
  let pubSubService;
  let router;

  beforeEach(() => {
    window.tickOff = false;
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe')
    };

    baseMethod = jasmine.createSpy('baseMethod');
    router = {
      events: {
        subscribe: jasmine.createSpy('subscribe')
      }
    };

    appRef = {
      tick: function() {
        baseMethod();
      }
    };
    ngZone = {
      runOutsideAngular: jasmine.createSpy('runOutsideAngular').and.callFake((functionToRun) => {
        functionToRun();
      }),
      run: jasmine.createSpy('run').and.callFake((functionToRun) => {
        functionToRun();
      }),
    };
  });

  it('should decorate tick method', fakeAsync(() => {
    decorateTick(
      (appRef as any),
      ngZone,
      pubSubService,
      router
    );

    appRef.tick();

    expect(ngZone.runOutsideAngular).toHaveBeenCalled();

    tick(10);
    appRef.tick();

    expect(baseMethod).toHaveBeenCalledTimes(1);

    tick(300);

    expect(baseMethod).toHaveBeenCalledTimes(2);
  }));

  it('should decorate tick method and run one tick', fakeAsync(() => {
    decorateTick(
      (appRef as any),
      ngZone,
      pubSubService,
      router
    );

    appRef.tick();
    tick(500);

    expect(baseMethod).toHaveBeenCalledTimes(1);
  }));

  it('should subscribe to route change run tick method', fakeAsync(() => {
    router.events.subscribe = jasmine.createSpy('subscribe').and.callFake((fn) => {
      fn(new NavigationStart(1, '/'));

      expect(baseMethod).toHaveBeenCalled();

      fn(new NavigationEnd(1, '/', '/'));

      expect(baseMethod).toHaveBeenCalled();
    });

    decorateTick(
      (appRef as any),
      ngZone,
      pubSubService,
      router
    );
  }));

  it('should not decorate tick method if turned off', () => {
    window.tickOff = true;

    decorateTick(
      (appRef as any),
      ngZone,
      pubSubService,
      router
    );

    appRef.tick();

    expect(baseMethod).toHaveBeenCalled();
    expect(ngZone.runOutsideAngular).not.toHaveBeenCalled();
  });

  it('should not call new tick if current tick not finished', () => {
    appRef._runningTick = true;
    window.tickOff = true;

    decorateTick(
      (appRef as any),
      ngZone,
      pubSubService,
      router
    );

    appRef.tick();

    expect(baseMethod).not.toHaveBeenCalled();
    expect(ngZone.runOutsideAngular).toHaveBeenCalled();
  });

  it('should not decorate tick method if login dialog opened', () => {
    pubSubService.subscribe.and.callFake((subscriber, method, callBack ) => {
      if (method === pubSubApi.OPEN_LOGIN_DIALOG) {
        callBack();
      }

      if (method === pubSubApi.VANILLA_SCOPE_CHANGE) {
        callBack(true);
      }
    });

    decorateTick(
      (appRef as any),
      ngZone,
      pubSubService,
      router
    );

    appRef.tick();

    expect(baseMethod).toHaveBeenCalled();
    expect(ngZone.runOutsideAngular).not.toHaveBeenCalled();
  });

  it('should decorate tick method if login dialog opened and closed', () => {
    pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((subscriber, method, callBack ) => {
      if (method === pubSubApi.OPEN_LOGIN_DIALOG) {
        callBack();
      }

      if (method === pubSubApi.LOGIN_DIALOG_CLOSED) {
        callBack();
      }

      if (method === pubSubApi.VANILLA_SCOPE_CHANGE) {
        callBack(false);
      }
    });

    decorateTick(
      (appRef as any),
      ngZone,
      pubSubService,
      router
    );

    appRef.tick();

    expect(ngZone.runOutsideAngular).toHaveBeenCalled();
  });
});
