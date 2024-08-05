
import { of as observableOf, throwError } from 'rxjs';
import { RacingSpecialsCarouselComponent } from '@racing/components/racingSpecialsCarousel/racing-specials-carousel.component';

describe('RacingSpecialsCarouselComponent', () => {

  let component: RacingSpecialsCarouselComponent;

  let cmsService;
  let racingSpecialsCarouselService;
  let pubSubService;

  const ids = ['3123', '2343'];
  const orderOutcomes = [{ displayOrder: 1 }, { displayOrder: 3 }, { displayOrder: 5 }] as any;
  const events = [{
    isFinished: 'true',
    isResulted: 'true',
    markets: [{
      outcomes: [{
        id: 3123
      }]
    }]
  }, {
    isResulted: 'true',
    isFinished: 'true',
    markets: [{
      outcomes: [{
        id: 2343
      }]
    }]
  }, {
    markets: [{
      outcomes: [{
        id: 1246
      }]
    }]
  }] as any;
  const filteredEvent = [{
    markets: [{
      outcomes: [{
        id: 1246
      }]
    }]
  }] as any;

  describe('DISABLED - RacingSpecialsCarouselComponent', () => {
    beforeEach(() => {
      cmsService = {
        getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({
          RacingSpecialsCarousel: { enable: false }
        }))
      };
      racingSpecialsCarouselService = {
        getEvents: jasmine.createSpy().and.returnValue(Promise.resolve(events))
      };
      pubSubService = {};

      component = new RacingSpecialsCarouselComponent(cmsService, racingSpecialsCarouselService, pubSubService);
    });

    it('ngOnInit - prevent load data if CMS config is disabled', () => {
      component.ngOnInit();
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      expect(racingSpecialsCarouselService.getEvents).not.toHaveBeenCalled();
    });
  });

  describe('ENABLED - RacingSpecialsCarouselComponent', () => {
    beforeEach(() => {
      cmsService = {
        getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({
          RacingSpecialsCarousel: { enable: true, label: 'CMS label' }
        }))
      };
      racingSpecialsCarouselService = {
        getEvents: jasmine.createSpy().and.returnValue(Promise.resolve(events)),
        orderEvents: jasmine.createSpy().and.returnValue(orderOutcomes),
        clearCache: jasmine.createSpy(),
        subscribeForUpdates: jasmine.createSpy().and.returnValue(ids),
        unSubscribeForUpdates: jasmine.createSpy()
      };
      pubSubService = {
        subscribe: jasmine.createSpy(),
        unsubscribe: jasmine.createSpy(),
        API: {
          DELETE_SELECTION_FROMCACHE: ''
        }
      };

      component = new RacingSpecialsCarouselComponent(cmsService, racingSpecialsCarouselService, pubSubService);
    });

    it('ngOnInit should work correct if cms call failed ', () => {
      component.eventId = 1223423;
      cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(throwError({} as any));
      spyOn(component['eventsLoaded'], 'emit');
      component.ngOnInit();
      expect(component['eventsLoaded'].emit).toHaveBeenCalled();
    });

    it('setOutcomesLength - should set outcome length', () => {
      const eventsData = [{
        markets: [{
          outcomes: [{
            id: 3123
          }]
        }]
      }, {
        markets: [{
          outcomes: [{
            id: 1246
          }]
        }]
      }] as any;
      component['setOutcomesLength'](eventsData);
      expect(component.outcomesLength).toBe(2);
      expect(component.isSingleSlide).toBe(false);
    });

    it('setOutcomesLength - should set outcome length if events is one', () => {
      component['setOutcomesLength'](filteredEvent);
      expect(component.outcomesLength).toBe(1);
      expect(component.isSingleSlide).toBe(true);
    });

    it('isFavourite - should check if outcome isFavourite - false', () => {
      const outcomes = { outcomeMeaningMinorCode: 0, name: 'outcome'} as any;
      expect(component['isFavourite'](outcomes)).toBe(false);
    });

    it('isFavourite - should check if outcome isFavourite - true', () => {
      const outcomes = { outcomeMeaningMinorCode: 1, name: 'unnamed favourite'} as any;
      expect(component['isFavourite'](outcomes)).toBe(true);
    });

    it('ngOnDestroy - should not call any functions if events are not exist', () => {
      component.items = [];
      component.ngOnDestroy();
      expect(racingSpecialsCarouselService.clearCache).not.toHaveBeenCalled();
      expect(racingSpecialsCarouselService.unSubscribeForUpdates).not.toHaveBeenCalled();
      expect(pubSubService.unsubscribe).not.toHaveBeenCalled();
    });

    it('ngOnDestroy - should unSubscribe on component destroy', () => {
      component.items = [{ id: 123456 }] as any;
      component['racingSpecialsCarouselSubscription'] = { unsubscribe: jasmine.createSpy() } as any;
      component.ngOnDestroy();
      expect(racingSpecialsCarouselService.clearCache).toHaveBeenCalled();
      expect(racingSpecialsCarouselService.unSubscribeForUpdates).toHaveBeenCalled();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('racingSpecialsCarouselComponent');
      expect(component['racingSpecialsCarouselSubscription'].unsubscribe).toHaveBeenCalledTimes(1);
    });

    it('trackById - should track event by index', () => {
      expect(component.trackById(2, {} as any)).toEqual('2');
    });

    it('trackById - should track event by id', () => {
      expect(component.trackById(1, { id: 72124 } as any)).toEqual('172124');
    });

    it('orderOutcomes - should order outcome by displayOrder', () => {
      const outcomes = [{ displayOrder: 3 }, { displayOrder: 5 }, { displayOrder: 1 }] as any;
      expect(component.orderEntity(outcomes)).toBe(orderOutcomes);
    });

    it('ngOnInit - should load component data', () => {
      component['initData'] = jasmine.createSpy();
      component.ngOnInit();
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      expect(component['initData']).toHaveBeenCalled();
      expect(component.label).toBe('CMS label');
    });

    it('initData - should init component data', () => {
      component.eventId = 1223423;
      component['initData']();
      expect(racingSpecialsCarouselService.getEvents).toHaveBeenCalledWith(1223423);
      expect(pubSubService.subscribe).toHaveBeenCalled();
    });

    it('initData - should init component data and set empty array for items if events were not found in response ', () => {
      component.eventId = 1223423;
      racingSpecialsCarouselService.getEvents.and.returnValue(Promise.resolve([]));
      component['initData']();
      expect(racingSpecialsCarouselService.getEvents).toHaveBeenCalledWith(1223423);
      expect(component['items']).toEqual([]);
      expect(pubSubService.subscribe).toHaveBeenCalled();
    });

    it('initData - should init component data and set empty array for items if there is some error ', () => {
      component.eventId = 1223423;
      racingSpecialsCarouselService.getEvents.and.returnValue(Promise.reject());
      component['initData']();
      expect(racingSpecialsCarouselService.getEvents).toHaveBeenCalledWith(1223423);
      expect(component['items']).toEqual([]);
      expect(pubSubService.subscribe).toHaveBeenCalled();
    });

    it('initData - should call connect and pubsub callbacks', () => {
      component.eventId = 1223423;
      racingSpecialsCarouselService.getEvents.and.returnValue(Promise.reject());
      pubSubService.subscribe.and.callFake((domain, channel, fn) => fn && fn());
      component['setOutcomesLength'] = jasmine.createSpy('setOutcomesLength');
      component['filterEvents'] = jasmine.createSpy('filterEvents').and.returnValue([]);

      component['initData']();

      expect(racingSpecialsCarouselService.getEvents).toHaveBeenCalledWith(1223423);
      expect(pubSubService.subscribe).toHaveBeenCalled();
      expect(component['items']).toEqual([]);
      expect(component['setOutcomesLength']).toHaveBeenCalledWith([]);
      expect(component['filterEvents']).toHaveBeenCalledWith([]);
    });
  });
});
