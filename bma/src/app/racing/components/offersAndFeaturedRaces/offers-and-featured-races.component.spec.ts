import { OffersAndFeaturedRacesComponent } from '@racing/components/offersAndFeaturedRaces/offers-and-featured-races.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { BehaviorSubject } from 'rxjs/internal/BehaviorSubject';

describe('OffersAndFeaturedRacesComponent', () => {
  let component: OffersAndFeaturedRacesComponent;
  let extraPlaceService, gtmService, routingHelperService, router, pubSubService, localeService, changeDetectorRef,seoDataService, vEPService;

  const events = [{
    id: 1,
    startTime: 2234567,
    drilldownTagNames: 'EVFLAG_EPR',
    markets: [{
      name: 'testMarket',
      drilldownTagNames: 'MKTFLAG_EPR',
      eachWayFactorNum: 1,
      eachWayFactorDen: 2,
      eachWayPlaces: 3,
      isEachWayAvailable: true
    }],
    originalName: 'testOriginalName'
  }, {
    id: 2,
    startTime: 1234567,
    drilldownTagNames: 'EVFLAG_FRT',
    markets: [{
      name: 'testMarket'
    }]
  }, {
    id: 3,
    markets: [{
      name: 'testMarket'
    }]
  }, {
    id: 4,
    drilldownTagNames: 'EVFLAG_FRT',
    raceStage: 'O',
    markets: [{
      name: 'testMarket'
    }]
  }, {
    id: 5,
    drilldownTagNames: 'EVFLAG_FRT',
    isResulted: 'true',
    markets: [{
      name: 'testMarket'
    }]
  }, {
    id: 6,
    drilldownTagNames: 'EVFLAG_FRT',
    isFinished: 'true',
    markets: [{
      name: 'testMarket'
    }]
  }, {
    id: 7,
    drilldownTagNames: 'EVFLAG_FRT',
    isFinished: 'true',
    markets: []
  }] as any;

  const groupedEvents = {
    itv: {
      title: 'test',
      name: 'test',
      svgId: '#itv',
      events: [{
        id: 2,
        link: 'link?origin=offers-and-features',
        startTime: 1234567,
        drilldownTagNames: 'EVFLAG_FRT',
        markets: [{
          name: 'testMarket'
        }]
      }]
    },
    epr: {
      title: 'test',
      name: 'test',
      svgId: '#extra-place',
      events: [{
        drilldownTagNames: 'EVFLAG_EPR',
        id: 1,
        link: 'link?origin=offers-and-features',
        odds: '1/2 the Odds 1-2-<b>3</b>',
        originalName: 'testOriginalName',
        startTime: 2234567,
        markets: [{
          name: 'testMarket',
          drilldownTagNames: 'MKTFLAG_EPR',
          eachWayFactorNum: 1,
          eachWayFactorDen: 2,
          eachWayPlaces: 3,
          isEachWayAvailable: true
        }]
      }]
    },
  } as any;

  const filterdEvents = [{
    id: 2,
    link: 'link?origin=offers-and-features',
    startTime: 1234567,
    drilldownTagNames: 'EVFLAG_FRT',
    markets: [{
      name: 'testMarket'
    }]
  }, {
    drilldownTagNames: 'EVFLAG_EPR',
    id: 1,
    link: 'link?origin=offers-and-features',
    odds: '1/2 the Odds 1-2-<b>3</b>',
    originalName: 'testOriginalName',
    startTime: 2234567,
    markets: [{
      name: 'testMarket',
      drilldownTagNames: 'MKTFLAG_EPR',
      eachWayFactorNum: 1,
      eachWayFactorDen: 2,
      eachWayPlaces: 3,
      isEachWayAvailable: true
    }]
  }] as any;

  beforeEach(() => {
    extraPlaceService = {
      gtmObject: {
        event: 'trackEvent',
        eventCategory: 'horse racing',
        eventAction: 'extra place',
        eventLabel: 'collapse'
      },
      subscribeForUpdates: jasmine.createSpy('subscribeForUpdates'),
      unSubscribeForUpdates: jasmine.createSpy('unSubscribeForUpdates'),
      sendGTM: jasmine.createSpy('sendGTM'),
      getEvents: jasmine.createSpy('getEvents').and.returnValue(Promise.resolve(filterdEvents)),
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    routingHelperService = {
      formEdpUrl: () => 'link'
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    localeService = {
      getString: () => 'test'
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => cb && cb('3')),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };
    seoDataService = {
      eventPageSeo: jasmine.createSpy('eventPageSeo')
    };
    vEPService = {
      bannerBeforeAccorditionHeader:  new BehaviorSubject<any>('bannerBeforeAccorditionHeader' as any),
      targetTab:  new BehaviorSubject<any>('targetTab' as any),
    };
    component = new OffersAndFeaturedRacesComponent(extraPlaceService, gtmService,
      routingHelperService, router, localeService, pubSubService, changeDetectorRef,seoDataService, vEPService);
  });

  describe('ngOnInit', () => {
    it('should get Racing Event onInit', () => {
      component.events = [...events];
      component.ngOnInit();
      expect(extraPlaceService.subscribeForUpdates).toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      expect(component.allEvents).toEqual(filterdEvents);
      expect(component.groupedEvents).toEqual(groupedEvents);
      expect(pubSubService.subscribe).toHaveBeenCalled();
    });

    it('should get Racing Event from response onInit', fakeAsync(() => {
      component.events = [];
      component.ngOnInit();
      tick();
      expect(extraPlaceService.getEvents).toHaveBeenCalled();
      expect(extraPlaceService.subscribeForUpdates).toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      expect(component.allEvents).toEqual(filterdEvents);
      expect(component.groupedEvents).toEqual(groupedEvents);
      expect(pubSubService.subscribe).toHaveBeenCalled();
    }));

    it('should get Racing Event from response onInit', fakeAsync(() => {
      extraPlaceService.getEvents = jasmine.createSpy('getEvents').and.returnValue(Promise.reject(null));
      component.events = [];
      component.ngOnInit();
      tick();
      expect(extraPlaceService.getEvents).toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      expect(component.allEvents).toEqual([]);
      expect(component.groupedEvents).toEqual({});
      expect(pubSubService.subscribe).toHaveBeenCalled();
    }));
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe from Subscriptions', () => {
      component.subscribedChannelsId = '123';
      component.ngOnDestroy();
      expect(extraPlaceService.unSubscribeForUpdates).toHaveBeenCalledWith('123');
      expect(pubSubService.unsubscribe).toHaveBeenCalled();
    });

    it('should unsubscribe from data load subscription', () => {
      component['loadDataSubscription'] = jasmine.createSpyObj('loadDataSubscription', ['unsubscribe']);
      component.subscribedChannelsId = '123';
      component.ngOnDestroy();
      expect(extraPlaceService.unSubscribeForUpdates).toHaveBeenCalledWith('123');
      expect(component['loadDataSubscription'].unsubscribe).toHaveBeenCalled();
      expect(pubSubService.unsubscribe).toHaveBeenCalled();
    });
  });

  describe('filterEvents', () => {
    it('should filter events', () => {
      const result = component['filterEvents'](events as any);
      expect(result).toEqual(result.slice(0, 2));
    });
  });

  describe('setGroupedEvents', () => {
    it('should set Grouped Racing Events', () => {
      const racingEvents = component['filterEvents'](events as any);
      component['setGroupedEvents']([...racingEvents] as any);
      expect(extraPlaceService.subscribeForUpdates).toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      expect(component.groupedEvents).toEqual(groupedEvents);
    });
  });

  describe('sendCollapseGTM', () => {
    it('sendCollapseGTM: should send GA on first collapse', () => {
      component['isFirstTimeCollapsed'] = false;
      component.sendCollapseGTM();

      expect(gtmService.push).toHaveBeenCalled();
      expect(component['isFirstTimeCollapsed']).toEqual(true);
    });

    it('sendCollapseGTM: should not send GA when it is not first collapse', () => {
      gtmService.push = jasmine.createSpy();
      component['isFirstTimeCollapsed'] = true;
      component.sendCollapseGTM();

      expect(gtmService.push).not.toHaveBeenCalled();
    });
  });

  describe('goToEvent', () => {
    beforeEach(() => {
      routingHelperService = {
        formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('link')
      };
      component = new OffersAndFeaturedRacesComponent(extraPlaceService, gtmService,
        routingHelperService, router, localeService, pubSubService, changeDetectorRef,seoDataService, vEPService);
    });
    it('should navigate to event', () => {
      spyOn(component as any, 'formEdpUrl').and.returnValue('url');
      component.goToEvent(events[0] as any);
      expect(extraPlaceService.sendGTM).toHaveBeenCalledWith(events[0].originalName);
      expect(router.navigateByUrl).toHaveBeenCalledWith('url');
      expect(seoDataService.eventPageSeo).toHaveBeenCalledWith(events[0],'url');
    });

    it('should navigate to event with offers and features in url', () => {
      spyOn(component as any, 'formEdpUrl').and.returnValue('url');
      component.isEventOverlay = true;
      component.sectionTitle = 'Uk / Ireland';
      component.goToEvent(events[0] as any);
      expect(pubSubService.publish).toHaveBeenCalled();
      expect(extraPlaceService.sendGTM).toHaveBeenCalledWith(events[0].originalName);
      expect(router.navigateByUrl).toHaveBeenCalledWith('url');
      expect(seoDataService.eventPageSeo).toHaveBeenCalledWith(events[0],'url');
    });
  });

  describe('formEdpUrl', () => {

    it('should create EDP url', () => {
      component.isEventOverlay = true;
      const result = component['formEdpUrl'](events[0] as any);
      expect(result).toEqual('link?origin=offers-and-features');
    });
  });

  describe('getOdds', () => {
    it('should get odds', () => {
      expect(component['getOdds'](events[0] as any)).toEqual('1/2 the Odds 1-2-<b>3</b>');
    });
  });

  describe('getPlaces', () => {
    it('should test getPlaces with correct places num', () => {
      expect(component['getPlaces']('3')).toEqual('1-2-');
    });

    it('should test getPlaces with incorrect places num', () => {
      expect(component['getPlaces']('test')).toEqual('');
    });
  });

  describe('isOddsAvailable', () => {
    it('should check if odds available - positive', () => {
      expect(component['isOddsAvailable'](events[0] as any)).toBeTruthy();
    });

    it('should check if odds available - negative', () => {
      expect(component['isOddsAvailable'](events[1] as any)).toBeFalsy();
    });
  });

  describe('trackById', () => {
    it('should test trackById eventId', () => {
      expect(component.trackById(5, events[0] as any)).toEqual('51');
    });

    it('should test trackById index', () => {
      expect(component.trackById(1, {} as any)).toEqual('1');
    });
  });

  describe('updateEvents', () => {
    it('should update events', () => {
      component.allEvents = events as any;
      component.groupedEvents = {
        itv: { events }
      } as any;
      expect(component.allEvents.length).toEqual(7);

      component['updateEvents'](3 as any);

      expect(component.allEvents.length).toEqual(6);
      expect(component.groupedEvents.itv.events.length).toEqual(6);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });
  });

  describe('#ngOnChanges', () => {
    it('should not set events', () => {
      component.events = [];
      component.ngOnChanges({} as any);
      expect(component.events.length).toBe(0);
    });
    it('should not set events, if events is null', () => {
      component.events = null;
      component.ngOnChanges({ events: {}} as any);
      expect(component.events).toBeNull();
    });
    it('should not set events, if events is []', () => {
      component.events = [];
      component.ngOnChanges({ events: {}} as any);
      expect(component.events.length).toBe(0);
    });
    it('should set events, if events is not null', () => {
      spyOn(component as any, 'filterEvents').and.returnValue([{id: 1}] as any);
      spyOn(component as any, 'setGroupedEvents');
      component.events = [{id: 1}] as any;
      component.ngOnChanges({ events: {}} as any);
      expect(component.allEvents.length).not.toBe(0);
    });
  });


  it('should check when banner above the accorition enabled',()=>
  {
    component.bannerBeforeAccorditionHeader='virtual';
    expect(component.isDisplayBanner('virtual')).toBeTruthy();
    expect(component.isDisplayBanner('nextRaces')).toBeFalsy();
    expect(component.isDisplayBanner(null)).toBeFalsy();
    component.bannerBeforeAccorditionHeader=undefined;
    expect(component.isDisplayBanner('virtual')).toBeFalsy();
    
  })

});
