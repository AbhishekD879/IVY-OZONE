import { MobileOddsBoostPageComponent } from './odds-boost-page.component';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';

describe('LadsMobileOddsBoostPageComponent', () => {
     
    let component: MobileOddsBoostPageComponent;
    let userService;
    let oddsBoostService;
    let cmsService;
    let localeService;
    let sessionStatusCallback;
    let domSanitizer;
    let pubSubService;
    let windowRefService;
    let changeDetector;
    let gtm;
    let timeservice;
  
    beforeEach(() => {
      pubSubService = {
        subscribe: jasmine.createSpy('subscribe').and.callFake((file, method, callback) => {
          if (method !== 'STORE_FREEBETS') {
            sessionStatusCallback = callback;
          }
        }),
        unsubscribe: jasmine.createSpy('unsubscribe'),
        publish: jasmine.createSpy('publish'),
        API: pubSubApi
      };
      userService = {
        status: true
      };
      oddsBoostService = {
        getOddsBoostTokens:jasmine.createSpy()
      };
      cmsService = {
        getOddsBoost: jasmine.createSpy()
      };
      localeService = {
        getString: jasmine.createSpy().and.returnValue('Odds Boost')
      };
      domSanitizer = {
        bypassSecurityTrustHtml: jasmine.createSpy()
      };

      gtm = {
        push: jasmine.createSpy('push') 
      };
      timeservice = {};
  
      
      component = new MobileOddsBoostPageComponent(
        pubSubService,
        userService,
        oddsBoostService,
        cmsService,
        localeService,
        domSanitizer,
        windowRefService,
        changeDetector,
        gtm,
        timeservice
      );
      spyOn(component, 'showSpinner').and.callThrough();
      spyOn(component, 'hideSpinner').and.callThrough();
    });
  
    it('available', () => {
        component.isDefaultPillOnLoad=false;
        component.isActive = false;
        spyOn(component, 'sendGTMData');
        component.available();
        expect(component.isActive).toBeTrue();
        expect(component.isDefaultPillOnLoad).toBeFalse();
        expect(component.sendGTMData).toHaveBeenCalledWith('available');
    });

    it('upcoming', () => {
        component.isDefaultPillOnLoad=false;
        component.isActive = true;
        spyOn(component, 'sendGTMData');
        component.upcoming();
        expect(component.isDefaultPillOnLoad).toBeFalse();
        expect(component.sendGTMData).toHaveBeenCalledWith('upcoming');
    });
  });



