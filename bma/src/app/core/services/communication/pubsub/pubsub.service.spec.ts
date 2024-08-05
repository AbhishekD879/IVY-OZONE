import { PubSubService } from './pubsub.service';
import { pubSubApi } from './pubsub-api.constant';
import { fakeAsync, tick } from '@angular/core/testing';

describe('PubSubService', () => {
  let service: PubSubService;
  let ngZone;

  beforeEach(() => {
    ngZone = {
      runOutsideAngular: jasmine.createSpy('runOutsideAngular').and.callFake((fn) => fn())
    };
    service = new PubSubService(ngZone);
  });

  it('API', () => {
    expect(service.API).toBeDefined();
    expect(service.API).toEqual(pubSubApi);
  });

  describe('subscribe, publish, publishSync', () => {
    it('proper call back to be executed only', fakeAsync(() => {
      const callback = jasmine.createSpy().and.returnValue(() => {});
      service.subscribe('loginDialogService', pubSubApi.OPEN_LOGIN_DIALOG, callback);
      service.publish(pubSubApi.OPEN_LOGIN_DIALOG);
      tick();
      expect(callback).toHaveBeenCalledTimes(1);
    }));

    it('proper call back to be executed only', fakeAsync(() => {
      const callback = jasmine.createSpy().and.returnValue(() => {});
      const callback2 = jasmine.createSpy().and.returnValue(() => {});
      service.subscribe('loginDialogService', pubSubApi.OPEN_LOGIN_DIALOG, callback);
      service.subscribe('loginDialogService', pubSubApi.APP_IS_LOADED, callback);
      service.publish(pubSubApi.OPEN_LOGIN_DIALOG);
      tick();
      expect(callback).toHaveBeenCalledTimes(1);
      expect(callback2).not.toHaveBeenCalled();
    }));

    it('proper call back with params', fakeAsync(() => {
      const callback = jasmine.createSpy().and.returnValue(() => {});
      service.subscribe('loginDialogService', pubSubApi.OPEN_LOGIN_DIALOG, callback);
      service.publish(pubSubApi.OPEN_LOGIN_DIALOG, { test: 'pubsub' });
      tick();
      expect(callback).toHaveBeenCalledTimes(1);
      expect(callback).toHaveBeenCalledWith({ test: 'pubsub' });
    }));

    it('proper call back with params and not async', () => {
      const callback = jasmine.createSpy().and.returnValue(() => {});
      service.subscribe('loginDialogService', pubSubApi.OPEN_LOGIN_DIALOG, callback);
      service.publish(pubSubApi.OPEN_LOGIN_DIALOG, { test: 'pubsub' }, false);
      expect(callback).toHaveBeenCalledTimes(1);
      expect(callback).toHaveBeenCalledWith({ test: 'pubsub' });
    });

    it('proper call back with params and not async', () => {
      const callback = jasmine.createSpy().and.returnValue(() => {});
      service.subscribe('loginDialogService', pubSubApi.OPEN_LOGIN_DIALOG, callback);
      service.publishSync(pubSubApi.OPEN_LOGIN_DIALOG, { test: 'pubsub' });
      expect(callback).toHaveBeenCalledTimes(1);
      expect(callback).toHaveBeenCalledWith({ test: 'pubsub' });
    });
  });

  describe('subscribe, publish, unsubscribe', () => {
    it('proper call back to be executed only', fakeAsync(() => {
      const callback = jasmine.createSpy().and.returnValue(() => {});
      service.subscribe('loginDialogService', pubSubApi.OPEN_LOGIN_DIALOG, callback);
      service.publish(pubSubApi.OPEN_LOGIN_DIALOG);
      tick();
      expect(callback).toHaveBeenCalledTimes(1);
      service.unsubscribe('loginDialogService');
      service.publish(pubSubApi.OPEN_LOGIN_DIALOG);
      tick();
      expect(callback).toHaveBeenCalledTimes(1);
    }));
  });

});
