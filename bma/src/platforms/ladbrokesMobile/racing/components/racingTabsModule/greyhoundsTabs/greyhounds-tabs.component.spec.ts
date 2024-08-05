import { of } from 'rxjs';

import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { LadbrokesGreyhoundsTabsComponent } from './greyhounds-tabs.component';

describe('LadbrokesGreyhoundsTabsComponent', () => {
  let component;
  let router;
  let filterService;
  let racingGaService;
  let routingHelperService;
  let eventService;
  let pubSubService;
  let cmsService, gtm, vEPService;

  beforeEach(() => {
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    filterService = {
      orderBy: jasmine.createSpy('orderBy'),
      date: jasmine.createSpy('date')
    };
    racingGaService = {
      trackModule: jasmine.createSpy('trackModule'),
      reset: jasmine.createSpy('reset')
    };
    routingHelperService = {
      formSportUrl: jasmine.createSpy('formSportUrl'),
      formEdpUrl: jasmine.createSpy('formEdpUrl')
    };
    eventService = {
      isAnyCashoutAvailable: jasmine.createSpy('isAnyCashoutAvailable')
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({}))
    };
    gtm = {
      push: jasmine.createSpy('push')
    };
    vEPService = {
      targetTab: {subscribe : (cb) => cb()},
      lastBannerEnabled: {subscribe : (cb) => cb()},
      accorditionNumber: {subscribe : (cb) => cb()},
    };

    component = new LadbrokesGreyhoundsTabsComponent(router, filterService, racingGaService, routingHelperService,
      eventService, pubSubService, cmsService, gtm, vEPService);
  });

  describe('ngOnInit', () => {
    it('should store cmsDataSubscription', () => {
      component.ngOnInit();

      expect(component['cmsDataSubscription']).toBeDefined();
    });
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe from cmsDataSubscription', () => {
      const cmsDataSubscription = jasmine.createSpyObj('cmsDataSubscription', ['unsubscribe']);

      component['cmsDataSubscription'] = cmsDataSubscription;
      component.ngOnDestroy();

      expect(cmsDataSubscription.unsubscribe).toHaveBeenCalled();
    });

    it('should unsubscribe from pubsub and connect events', () => {
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('greyhoundsTabsComponent');
      expect(racingGaService.reset).toHaveBeenCalled();
    });
  });

  describe('displayNextRaces', () => {
    it('should return false in case of error', () => {
      component['responseError'] = 'error' as any;
      expect(component.displayNextRaces).toBeFalsy();
    });
    it('should return false in case if tab is not today', () => {
      component['responseError'] = undefined as any;
      component['display'] = 'tomorrow' as any;
      expect(component.displayNextRaces).toBeFalsy();
    });
    it('should return false in case if feat is disabled', () => {
      component['responseError'] = undefined as any;
      component['display'] = 'tomorrow' as any;
      component['nextRacesComponentEnabled'] = false;
      expect(component.displayNextRaces).toBeFalsy();
    });
    it('should return false in case if no error and tab is today and feat is enabled', () => {
      component['responseError'] = undefined as any;
      component['display'] = 'today' as any;
      component['nextRacesComponentEnabled'] = true;
      expect(component.displayNextRaces).toBeTruthy();
    });
  });
});
