import { ReloadService } from './reload.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { fakeAsync, tick } from '@angular/core/testing';

describe('ReloadService', () => {
  let service: ReloadService;
  let device;
  let windowRef;
  let pubsub;
  let infoDialogService;
  let eventCallbacks;
  let storageService;

  beforeEach(() => {
    eventCallbacks = {};
    device = {
      isNativeAndroid: true,
      osVersion: '5.0.0',
      deviceType: 'Samsung S12',
      isOnline: jasmine.createSpy().and.returnValue(false),
      setOnline: jasmine.createSpy(),
      isDesktop: true
    };
    windowRef = {
      nativeWindow: {
        addEventListener: jasmine.createSpy().and.callFake((method: string, cb: void) => {
          eventCallbacks[method] = cb;
        }),
        navigator: {
          onLine: true
        },
        location: {
          reload: jasmine.createSpy(),
          href: 'coral/under-maintenance'
        },
        document: {
          URL: '/'
        },
        setInterval: jasmine.createSpy('setInterval').and.callFake((cb, interval) => {
          cb && cb();
        }),
      }
    };
    pubsub = {
      API: pubSubApi,
      publish: jasmine.createSpy()
    };
    infoDialogService = {
      openConnectionLostPopup: jasmine.createSpy('openConnectionLostPopup'),
      closeConnectionLostPopup: jasmine.createSpy('closeConnectionLostPopup')
    };
    storageService = {
      set: jasmine.createSpy('storageService.set'),
      get: jasmine.createSpy('storageService.get')
    };
    spyOn(console, 'warn');
    service = new ReloadService(device, windowRef, pubsub, infoDialogService, storageService);
  });

  describe('Reload', () => {
    it('constructor', () => {
      expect(service).toBeDefined();
      expect(windowRef.nativeWindow.addEventListener).toHaveBeenCalledWith('offline', jasmine.any(Function));
      expect(windowRef.nativeWindow.addEventListener).toHaveBeenCalledWith('online', jasmine.any(Function));
    });

    it('should not reload if reload disabled', fakeAsync(() => {
      service.reload();
      tick(1000);
      expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.RELOAD_COMPONENTS);
    }));
    it('should not call RELOAD_COMPONENTS pubsub if connectionLost is true and onLine is false', fakeAsync(() => {
      service['connectionLost'] = true;
      windowRef.nativeWindow.navigator.onLine = false;
      service.reload();
      tick(1000);
      expect(pubsub.publish).not.toHaveBeenCalledWith(pubsub.API.RELOAD_COMPONENTS);
    }));
    it('should not call RELOAD_COMPONENTS pubsub if connectionLost is true and onLine is true', fakeAsync(() => {
      service['connectionLost'] = true;
      windowRef.nativeWindow.navigator.onLine = true;
      service.reload();
      tick(1000);
      expect(pubsub.publish).not.toHaveBeenCalledWith(pubsub.API.RELOAD_COMPONENTS);
    }));
    describe('#init', () => {
      it('should call connectionLostLogic on interval', () => {
        service['connectionLostLogic'] = jasmine.createSpy('connectionLostLogic');
        service['init']();

        expect(windowRef.nativeWindow.setInterval).toHaveBeenCalledWith(jasmine.any(Function), 30000);
        expect(service['connectionLostLogic']).toHaveBeenCalled();
      });
    });
  });

  it('init - should handle app coming online', () => {
    windowRef.nativeWindow.addEventListener.and.callFake((method: string, cb: Function) => {
      if (method === 'online') {
        cb();
      }
    });
    service['init']();
    expect(service['connectionLost']).toBe(false);
    expect(infoDialogService.closeConnectionLostPopup).toHaveBeenCalled();
  });
  describe('init - network indicator handling', () => {
    it('init - should call openConnectionLostPopup when it is desktop', () => {
      windowRef.nativeWindow.addEventListener.and.callFake((method: string, cb: Function) => {
        if (method === 'online') {
          cb();
        }
      });
      spyOn(service as any, 'openConnectionLostPopupForDesktop');
      service['init']();
      // expect(service['openConnectionLostPopupForDesktop']).toHaveBeenCalled();
    });
    it('init - should handle app coming offline', () => {
      windowRef.nativeWindow.addEventListener.and.callFake((method: string, cb: Function) => {
        if (method === 'offline') {
          cb();
        }
      });
      service['connectionLostLogic'] = jasmine.createSpy('connectionLostLogic');
      service['init']();
      expect(service['connectionLost']).toBe(false);
      expect(service['connectionLostLogic']).toHaveBeenCalled();
    });
  });

  describe('#openConnectionLostPopupForDesktop', () => {
    it('should call openConnectionLostPopup if it is desktop', () => {
      device.isDesktop = true;
      service['openConnectionLostPopupForDesktop']();
      expect(infoDialogService.openConnectionLostPopup).toHaveBeenCalled();
    });
    it('should not call openConnectionLostPopup if it is desktop', () => {
      device.isDesktop = false;
      storageService.get.and.returnValue(true);
      service['openConnectionLostPopupForDesktop']();
      expect(infoDialogService.openConnectionLostPopup).not.toHaveBeenCalled();
    });
    it('should call openConnectionLostPopup if storageService returns false', () => {
      storageService.get.and.returnValue(false);
      service['openConnectionLostPopupForDesktop']();
      expect(infoDialogService.openConnectionLostPopup).toHaveBeenCalled();
    });
    it('should not call openConnectionLostPopup if storageService returns true', () => {
      device.isDesktop = false;
      storageService.get.and.returnValue(true);
      service['openConnectionLostPopupForDesktop']();
      expect(infoDialogService.openConnectionLostPopup).not.toHaveBeenCalled();
    });
  });
});
