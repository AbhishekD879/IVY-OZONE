import { NativeBridgeBootstrapperService } from './native-bridge-bootstrapper.service';
import { fakeAsync, tick } from '@angular/core/testing';
import { NavigationEnd, RouterEvent } from '@angular/router';
import { Subject } from 'rxjs';

describe('NativeBridgeBootstrapperService', () => {
  let service: NativeBridgeBootstrapperService;
  let bridge;
  let nativeBridgeAdapterMock;
  let portalNativeEventNotifierMock;
  let vanillaNativeAppServiceMock;
  let routerMock;
  beforeEach(() => {
    bridge = {
      onCookieBannerClosed: jasmine.createSpy()
    };
    nativeBridgeAdapterMock = {
      attachNativeMessageReceiver: jasmine.createSpy()
    };
    portalNativeEventNotifierMock = {
      attachNativeMessageNotifier: jasmine.createSpy()
    };
    vanillaNativeAppServiceMock = {
      sendToNative: jasmine.createSpy(),
      isNativeWrapper: true,
    };
    routerMock = {
      events: new Subject<RouterEvent>(),
    };
    service = new NativeBridgeBootstrapperService(
      bridge,
      nativeBridgeAdapterMock,
      portalNativeEventNotifierMock,
      vanillaNativeAppServiceMock,
      routerMock
    );
  });

  describe('init', () => {

    it('is called', () => {
      service.init = jasmine.createSpy();
      service.init();
      expect(service.init).toHaveBeenCalled();
    });

    it('calls attachNativeMessageNotifier and attachNativeMessageReceiver', () => {
      service.init();
      expect(nativeBridgeAdapterMock.attachNativeMessageReceiver).toHaveBeenCalled();
      expect(portalNativeEventNotifierMock.attachNativeMessageNotifier).toHaveBeenCalled();
    });

    it('emits native event named "AFTER_INITIAL_NAVIGATION" on first navigation and calls onCookieBannerClosed', fakeAsync(() => {
      service.init();
      routerMock.events.next(new NavigationEnd(1, '/', '/'));
      tick();
      expect(vanillaNativeAppServiceMock.sendToNative).toHaveBeenCalledWith({ eventName: 'AFTER_INITIAL_NAVIGATION' });
      expect(bridge.onCookieBannerClosed).toHaveBeenCalled();
    }));

  });
});
