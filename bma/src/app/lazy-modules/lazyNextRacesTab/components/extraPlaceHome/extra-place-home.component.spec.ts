import { ExtraPlaceHomeComponent } from '@lazy-modules/lazyNextRacesTab/components/extraPlaceHome/extra-place-home.component';

import { fakeAsync, tick } from '@angular/core/testing';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('#ExtraPlaceHome', () => {
  let component: ExtraPlaceHomeComponent,
    filterService,
    extraPlaceService,
    gtmService,
    routingHelperService,
    localeService,
    templateService,
    router,
    pubSubService,
    changeDetectorRef;

  beforeEach(() => {
    filterService = {
      distance: jasmine.createSpy('distance')
    };
    extraPlaceService = {
      getEvents: jasmine.createSpy('getEvents').and.returnValue(Promise.resolve(
        [{ id: 1 }, { id: 2 }, { id: 3, markets: [{}] }, { markets: [] }
      ])),
      subscribeForUpdates: jasmine.createSpy('subscribeForUpdates'),
      unSubscribeForUpdates: jasmine.createSpy('unSubscribeForUpdates')
    };

    gtmService = {
      push: jasmine.createSpy('push')
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl'),
    };
    localeService = {
      getString: jasmine.createSpy('getString')
    };
    templateService = {
      setCorrectPriceType: jasmine.createSpy('setCorrectPriceType')
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };

    component = new ExtraPlaceHomeComponent(
      filterService,
      extraPlaceService,
      gtmService,
      routingHelperService,
      localeService,
      router,
      templateService,
      pubSubService,
      changeDetectorRef
    );
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  describe('@ngOnInit', () => {
    it('should get events', fakeAsync(() => {
      component.limit = 10;
      component.ngOnInit();
      expect(extraPlaceService.getEvents).toHaveBeenCalledWith({ racingFormEvent: true });
      tick();
      expect(component.events).toBeDefined();
      expect(component.events.length).toBe(1);
      expect(pubSubService.subscribe).toHaveBeenCalledTimes(1);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    }));

    it('should filter events', fakeAsync(() => {
      component.events = [{ id: 1 }, { id: 2 }, { id: 3, markets: [{}] }] as any;
      component.limit = 1;
      pubSubService.subscribe.and.callFake((fileName, eventName, cb) => {
        if (eventName.includes('DELETE_EVENT_FROM_CACHE')) {
          cb(1);
        }
        if (eventName.includes('EXTRA_PLACE_RACE_OFF')) {
          cb(2);
        }
      });
      component.ngOnInit();
      tick();

      expect(component.events).toEqual([{ id: 3, markets: [{}] } as any]);
    }));
  });

  describe('@ngOnDestroy', () => {
    it('should unsubscribe from updates', () => {
      component['eventsSubscription'] = { unsubscribe: jasmine.createSpy('unsubscribe') } as any;
      component.ngOnDestroy();
      expect(extraPlaceService.unSubscribeForUpdates).toHaveBeenCalled();
      expect(pubSubService.unsubscribe).toHaveBeenCalled();
      expect(component['eventsSubscription'].unsubscribe).toHaveBeenCalledTimes(1);
    });

    it('should not unsubscribe if no subscription', () => {
      component['eventsSubscription'] = null;
      expect(() => component.ngOnDestroy()).not.toThrowError();
    });
  });

  describe('@parseGoing', () => {
    it('should parse going', () => {
      const race = {
        racingFormEvent: {
          going: 'some going'
        }
      };
      component.parseGoing(race as any);
      expect(localeService.getString).toHaveBeenCalledWith(`racing.racingFormEventGoing.${race.racingFormEvent.going}`);
    });

    it('should parse going with key not found', () => {
      localeService.getString.and.returnValue('KEY_NOT_FOUND');
      const race = {
        racingFormEvent: {
          going: 'some going'
        }
      };
      const result = component.parseGoing(race as any);
      expect(localeService.getString).toHaveBeenCalledWith(`racing.racingFormEventGoing.${race.racingFormEvent.going}`);
      expect(result).toEqual('');
    });
  });

  describe('@parseDistance', () => {
    it('should parse distance', () => {
      const race = {
        racingFormEvent: {
          distance: 'some distance'
        }
      };
      component.parseDistance(race as any);
      expect(filterService.distance).toHaveBeenCalledWith(race.racingFormEvent.distance);
    });
  });

  describe('@goToEvent', () => {
    it('should navigate and send gtm', () => {
      component['sendGTM'] = jasmine.createSpy();
      spyOn(component, 'formEdpUrl');
      component.goToEvent({} as any);
      expect(component['sendGTM']).toHaveBeenCalled();
      expect(component.formEdpUrl).toHaveBeenCalled();
      expect(router.navigateByUrl);
    });
  });

  describe('#showEchWayTerms', () => {
    it('#showEchWayTerms if market has eachWayPlaces', () => {
      const result = component.showEchWayTerms(({
        eachWayPlaces: true,
        eachWayFactorDen: '1',
        eachWayFactorNum: '7'
      } as any));

      expect(result).toEqual(true);
    });

    it('#showEchWayTerms does not have eachWayPlaces', () => {
      const result = component.showEchWayTerms(({
        eachWayPlaces: false,
        eachWayFactorDen: '',
        eachWayFactorNum: ''
      } as any));

      expect(result).toEqual(false);
    });
  });

  describe('@formEdpUrl', () => {
    it('should go to the sport event', () => {
      component.formEdpUrl({} as any);
      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith({});
    });
  });

  describe('@trackById', () => {
    it('should track by id', () => {
      const result = component.trackById(1, ({
        id: '12'
      }) as any);
      expect(result).toEqual('112');
    });

    it('should track by index', () => {
      const result = component.trackById(1, ({}) as any);
      expect(result).toEqual('1');
    });
  });

  describe('@sendGTM', () => {
    it('should send data', () => {
      component['sendGTM']();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'horse racing',
        eventAction: 'extra place race module',
        eventLabel: 'view event'
      });
    });
  });
});
