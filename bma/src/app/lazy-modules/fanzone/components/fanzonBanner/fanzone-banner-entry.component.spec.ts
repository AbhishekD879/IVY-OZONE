import { of } from 'rxjs';

import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { FanzoneBannerComponent } from '@app/lazy-modules/fanzone/components/fanzonBanner/fanzone-banner-entry.component';
import { FANZONECONFIG, SITECORE_PROMOTION, SITECORE_PROMOTION_EMPTY_TEASER } from '@ladbrokesDesktop/bma/components/home/mockdata/home.component.mock';
import { fakeAsync, tick } from '@angular/core/testing';
import { Router } from '@angular/router';

describe('FanzoneBannerComponent', () => {
  let component: FanzoneBannerComponent;
  let cms;
  let dynamicComponentLoader;
  let pubSubService;
  let userService;
  let vanillaApiService;
  let fanzoneHelperService;
  let gtmService;
  let router;
  let cdRef;
  let fanzoneStorageService;
  let device;

  beforeEach(() => {
    cms = {
      getFanzoneRouteName: jasmine.createSpy('getFanzoneRouteName').and.returnValue('now-next')
    };
    dynamicComponentLoader = {};
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy().and.callFake((p1, p2, cb) => {
        cb({ data: [1] });
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
    };
    userService = {
      username: 'abc'
    };
    vanillaApiService = {
      get: jasmine.createSpy('get').and.returnValue(of(SITECORE_PROMOTION))
    };
    fanzoneHelperService = {
      selectedFanzone: FANZONECONFIG,
      getSelectedFzUpdate  : jasmine.createSpy().and.returnValue(of(FANZONECONFIG))
    }
    gtmService = {
      push: jasmine.createSpy('push')
    };
    router = {url: 'test'};
    cdRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    fanzoneStorageService = {
      set: jasmine.createSpy('fanzoneStorageService.set'),
      get: jasmine.createSpy('fanzoneStorageService.get').and.returnValue({teamId:'ARS', teamName: 'Arsenal FC'})
    };
    device = {
      isIos: false,
      isAndroid: false,
      isMobile: true,
      isTablet: false
    };
    createComponent();
  });

  function createComponent() {
    component = new FanzoneBannerComponent(router as Router, cms, dynamicComponentLoader, pubSubService, userService, vanillaApiService, fanzoneHelperService, gtmService,fanzoneStorageService, cdRef,device);
  }

  it('set fanzone enabled as true when home page on login', fakeAsync(() => {
    pubSubService.subscribe.and.callFake((a, b, cb) => {
      component.checkIfFanzoneEnabled = jasmine.createSpy('');
      if (Array.isArray(b) && (b[0] === 'SESSION_LOGIN')) {
        cb();
        expect(component.checkIfFanzoneEnabled).toHaveBeenCalled();
      }
    });
    component.ngOnInit();
    tick();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      component.channelName, [pubSubService.API.SESSION_LOGIN], jasmine.any(Function)
    );
  }));

  it('set fanzone enabled as true when home page', fakeAsync(() => {
    router.url = '/';
    device.isMobile = false;
    fanzoneStorageService.get.and.returnValue({teamId:'FZ001', teamName: 'My own team'});
    component = new FanzoneBannerComponent(router as Router, cms, dynamicComponentLoader, pubSubService, userService, vanillaApiService, fanzoneHelperService, gtmService,fanzoneStorageService, cdRef,device);
    component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
      .and.callFake((filename: string, eventName: string, callback: Function) => {
        if (eventName === 'FANZONE_DATA') {
          callback(FANZONECONFIG);
          device.isMobile = false;
          expect(component.fanzoneBannerImage).toEqual('abc');
        }
      });
    component.ngOnInit();

    expect(component.isFanzoneEnabled).toBe(true);
  }));

  it('set fanzone enabled as true when home page for rgy user', fakeAsync(() => {
    router.url = '/';
    device.isMobile = false;
    userService.bonusSuppression = true;
    fanzoneStorageService.get.and.returnValue({teamId:'FZ001', teamName: 'My own team'});
    cms = {
      getFanzoneRouteName: jasmine.createSpy('getFanzoneRouteName').and.returnValue('games')
    };
    component = new FanzoneBannerComponent(router as Router, cms, dynamicComponentLoader, pubSubService, userService, vanillaApiService, fanzoneHelperService, gtmService,fanzoneStorageService, cdRef,device);
    component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
      .and.callFake((filename: string, eventName: string, callback: Function) => {
        if (eventName === 'FANZONE_DATA') {
          callback(FANZONECONFIG);
          device.isMobile = false;
          expect(component.fanzoneRoutingUrl).toContain('/games');
          expect(component.fanzoneBannerImage).toEqual('abc');
        }
      });
    component.ngOnInit();

    expect(component.isFanzoneEnabled).toBe(true);
  }));

  it('set fanzone enabled as true when home page url as "/home/featured"', fakeAsync(() => {
    router.url = '/home/featured';
    component = new FanzoneBannerComponent(router as Router, cms, dynamicComponentLoader, pubSubService, userService, vanillaApiService, fanzoneHelperService, gtmService,fanzoneStorageService, cdRef,device);
    component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
      .and.callFake((filename: string, eventName: string, callback: Function) => {
        if (eventName === 'FANZONE_DATA') {
          callback(FANZONECONFIG);
        }
      });
    component.ngOnInit();

    expect(component.isFanzoneEnabled).toBe(true);
  }));

  it('set fanzone enabled as true when football page', fakeAsync(() => {
    router.url = '/sport/football/matches';
    component = new FanzoneBannerComponent(router as Router, cms, dynamicComponentLoader, pubSubService, userService, vanillaApiService, fanzoneHelperService, gtmService,fanzoneStorageService, cdRef,device);
    component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
      .and.callFake((filename: string, eventName: string, callback: Function) => {
        if (eventName === 'FANZONE_DATA') {
          callback(FANZONECONFIG);
        }
      });
    component.ngOnInit();

    expect(component.isFanzoneEnabled).toBe(true);
  }));

  it('set fanzone enabled as false when not football or home page', fakeAsync(() => {
    router.url = 'test';
    component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
      .and.callFake((filename: string, eventName: string, callback: Function) => {
        if (eventName === 'FANZONE_DATA') {
          callback(FANZONECONFIG);


        }
      });
    component.ngOnInit();

    expect(component.isFanzoneEnabled).toBe(false);
  }));

  it('set fanzone enabled as false when no fanzone storage data', fakeAsync(() => {
    router.url = '/sport/football/matches';
    fanzoneStorageService.get = jasmine.createSpy().and.returnValue(null);
    component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
      .and.callFake((filename: string, eventName: string, callback: Function) => {
        if (eventName === 'FANZONE_DATA') {
          callback(FANZONECONFIG);
          expect(component.fanzoneBannerImage).toEqual('abc');

        }
      });
    component.ngOnInit();

    expect(component.isFanzoneEnabled).toBe(false);
  }));

    it('set fanzone enabled as false when no fanzone storage data', fakeAsync(() => {
    router.url = '/sport/football';
    fanzoneStorageService.get = jasmine.createSpy().and.returnValue(null);
    component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
      .and.callFake((filename: string, eventName: string, callback: Function) => {
        if (eventName === 'FANZONE_DATA') {
          callback(FANZONECONFIG);
          expect(component.fanzoneBannerImage).toEqual('abc');

        }
      });
    component.ngOnInit();

    expect(component.isFanzoneEnabled).toBe(false);
  }));

  it('sitecore fanzone should be empty if response is not empty but no teasers data ', () => {
    FANZONECONFIG.launchBannerUrl = 'xyz';
    router.url = '/sport/football/matches';
    vanillaApiService.get = jasmine.createSpy('get').and.returnValue(of(SITECORE_PROMOTION_EMPTY_TEASER))
    component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
      .and.callFake((filename: string, eventName: string, callback: Function) => {
        if (eventName === 'SESSION_LOGIN') {
          callback();
        }
      });

    component.ngOnInit();
  });

  it('iMInClicked', () => {
    component.iMInClicked('fanzone');
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', { event: 'trackEvent', eventAction: 'entry banner', eventCategory: 'fanzone', eventLabel: 'click', eventDetails: 'fanzone' });
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('fanzoneHome');
  });
});
