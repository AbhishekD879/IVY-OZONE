import { fakeAsync, tick } from '@angular/core/testing';
import { of as observableOf } from 'rxjs';

import { PrivateMarketsTabComponent } from './private-markets-tab.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('PrivateMarketsTabComponent', () => {
  let component: PrivateMarketsTabComponent;
  let privateMarketsService;
  let pubSubService;
  let updateEventService;
  let events = [];

  beforeEach(() => {
    events = [{ markets: [{ outcomes: [ {}, { isDisplayed: false }, { isDisplayed: true } ]}] }];

    privateMarketsService = {
      unsubscribe: jasmine.createSpy('privateMarketsService.unsubscribe'),
      subscribe: jasmine.createSpy('privateMarketsService.subscribe'),
      markets: jasmine.createSpy('privateMarketsService.markets').and.returnValue(observableOf(events))
    };
    pubSubService = {
      subscribe: jasmine.createSpy('pubSubService.subscribe').and.callFake((a, eventName, cb) => {
        if (eventName !== pubSubService.API.RELOAD_COMPONENTS) {
          cb && cb(events);
        }
      }),
      unsubscribe: jasmine.createSpy('pubSubService.unsubscribe'),
      publish: jasmine.createSpy('pubSubService.publish'),
      API: pubSubApi
    };
    updateEventService = {};

    component = new PrivateMarketsTabComponent(privateMarketsService, pubSubService, updateEventService);
  });

  it('#constructor', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', fakeAsync(() => {
    component.ngOnInit();
    tick();
    expect(pubSubService.subscribe).toHaveBeenCalledWith('PrivateMarketsTabComponent', 'PRIVATE_MARKETS_TAB', jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith('PrivateMarketsTabComponent', 'LIVE_SERVE_MS_UPDATE', jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith('PrivateMarketsTabComponent',
      pubSubService.API.RELOAD_COMPONENTS,
      jasmine.any(Function)
    );
    expect(pubSubService.publish).not.toHaveBeenCalledWith('HIDE_PRIVATE_MARKETS_TAB');
    expect(privateMarketsService.subscribe).toHaveBeenCalledTimes(1);
    expect(privateMarketsService.markets).toHaveBeenCalledTimes(2);
  }));

  it('should handle reload components call destroy/init', fakeAsync(() => {
    pubSubService.subscribe.and.callFake((a, eventName, callback) => {
      if (eventName === pubSubService.API.RELOAD_COMPONENTS) {
        component.ngOnInit = jasmine.createSpy('ngOnInit');
        component.ngOnDestroy = jasmine.createSpy('ngOnDestroy');

        callback(events);

        expect(component.ngOnInit).toHaveBeenCalled();
        expect(component.ngOnDestroy).toHaveBeenCalled();
      }
    });

    component.ngOnInit();
    tick();
  }));

  describe('ngOnDestroy', () => {
    it('should unsubscribe from privateMarketsService and pubsub channels', () => {
      component.events = events;
      component.ngOnDestroy();

      expect(privateMarketsService.unsubscribe).toHaveBeenCalledWith(component.events);
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('PrivateMarketsTabComponent');
    });

    it('should unsubscribe from private markets and init subscriptions', fakeAsync(() => {
      component.ngOnInit();
      (component as any).loadEvents();
      spyOn(component['onInitSubscription'], 'unsubscribe').and.callThrough();
      spyOn(component['privateMarketsSubscription'], 'unsubscribe').and.callThrough();

      tick();

      component.ngOnDestroy();

      expect(component['onInitSubscription'].unsubscribe).toHaveBeenCalled();
      expect(component['privateMarketsSubscription'].unsubscribe).toHaveBeenCalled();
    }));
  });

  it('trackEventsByFn', () => {
    expect(component.trackEventsByFn(100)).toBe(100);
  });

  it('trackMarketsByFn', () => {
    expect(component.trackMarketsByFn(100)).toBe(100);
  });

  it('trackOutcomesByFn', () => {
    expect(component.trackOutcomesByFn(100)).toBe(100);
  });

  describe('loadEvents', () => {
    it('should load events from private markets service', fakeAsync(() => {
      privateMarketsService.markets.and.returnValue(observableOf(events));

      component['loadEvents']();
      tick();

      expect(component.events).toEqual(events);
      // should checkVisibleEvents and close provate markets tab when no more markets found
      expect(pubSubService.publish).not.toHaveBeenCalled();
    }));

    it('should check loaded events, if events are not displayed, should close private market tab', fakeAsync(() => {
      events[0].markets = [{ outcomes: [{ isDisplayed: false }] }];
      privateMarketsService.markets.and.returnValue(observableOf(events));

      component['loadEvents']();
      tick();

      expect(component.events).toEqual(events);
      // should checkVisibleEvents and close provate markets tab when no more markets found
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.HIDE_PRIVATE_MARKETS_TAB);
    }));

    it('should check loaded events, if no events, should close private market tab', fakeAsync(() => {
      privateMarketsService.markets.and.returnValue(observableOf([]));

      component['loadEvents']();
      tick();

      expect(component.events).toEqual([]);
      // should checkVisibleEvents and close provate markets tab when no more markets found
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.HIDE_PRIVATE_MARKETS_TAB);
    }));

    it('should unsubscribe from private markets subscription if it exists', () => {
      const privateMarketsSubscription = jasmine.createSpyObj('privateMarketsSubscription', ['unsubscribe']);

      (component as any).privateMarketsSubscription = privateMarketsSubscription;

      component['loadEvents']();

      expect(privateMarketsSubscription.unsubscribe).toHaveBeenCalled();
    });
  });
});
