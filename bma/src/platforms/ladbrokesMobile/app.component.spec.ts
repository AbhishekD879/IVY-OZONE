import { async } from '@angular/core/testing';
import { RootComponent } from './app.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { of } from 'rxjs';
import { NavigationEnd, NavigationStart } from '@angular/router';

describe('LMAppComponent', () => {
  let component: RootComponent;
  let casinoPlatformLoaderService;
  let appRef;
  let ngZone;
  let pubSubService;
  let router;
  let cmsService;
  let userService;

  beforeEach(async(() => {
    router = {
      events: {
        subscribe: jasmine.createSpy('subscribe')
      }
    };

    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      API: pubSubApi
    };
    casinoPlatformLoaderService = {
      loadCasinoPlatformModule: jasmine.createSpy('',null)
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        GamingEnabled: {
          enabledGamingOverlay: true
        }
      }))
    };
    userService = {
      logout: jasmine.createSpy(),
      login: jasmine.createSpy(),
      set: jasmine.createSpy(),
      initProxyAuth: jasmine.createSpy(),
      resolveProxyAuth: jasmine.createSpy(),
      rejectProxyAuth: jasmine.createSpy(),
      isInShopUser: jasmine.createSpy().and.returnValue(false),
      proxyPromiseResolved: jasmine.createSpy().and.returnValue(true),
      username: 'username'
    };
    appRef = {};
    ngZone = {};

    component = new RootComponent(
      appRef,
      ngZone,
      pubSubService,
      router,
      cmsService
    );
  }));

  it('should call loadCasinoPlatformModule when disabled in CMS', () => {
    cmsService.getSystemConfig.and.returnValue(of({ GamingEnabled: { enabledGamingOverlay: false } }));
    component.ngAfterViewInit();
    expect(casinoPlatformLoaderService.loadCasinoPlatformModule).not.toHaveBeenCalled();
  });

  describe('ngOnInit', () => {
    it('should call checkHomeUrl with NavigationStart  n true', () => {
      router.url = '/home/featured';
      const eventStart = new NavigationStart(0, '');
      router.events.subscribe.and.callFake((fn) => fn(eventStart));
      component.ngOnInit();
      expect(component.isHomePage).toBeTruthy();
    });
    it('should call checkHomeUrl with NavigationEnd n true', () => {
      router.url = '/home/featured';
      const eventStart = new NavigationEnd(0, '', '');
      router.events.subscribe.and.callFake((fn) => fn(eventStart));
      component.ngOnInit();
      expect(component.isHomePage).toBeTruthy();
    });
    it('should call checkHomeUrl n false', () => {
      router.url = '/sports/football';
      component.ngOnInit();
      expect(component.isHomePage).toBeFalsy();
    });
    it('should call checkHomeUrl n true', () => {
      router.url = '/q=1';
      component.ngOnInit();
      expect(component.isHomePage).toBeFalsy();
    });
  });
});
