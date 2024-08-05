import { fakeAsync } from '@angular/core/testing';
import { ToteSliderComponent } from '@app/tote/components/toteSlider/tote-slider.component';
import { IToteEvent } from '@app/tote/models/tote-event.model';
import * as _ from 'underscore';
import { of } from 'rxjs';
import { BehaviorSubject } from 'rxjs/internal/BehaviorSubject';

describe('ToteSliderComponent', () => {
  let component: ToteSliderComponent;
  let events: IToteEvent[];
  let gtmService;
  let toteService;
  let router;
  let locale;
  let storage;
  let buildUtilityService;
  let vEPService;

  beforeEach(() => {
    events = [
      { id: 1, typeName: 'Dundalk', name: 'Race 1', startTime: 234567, externalKeys: { OBEvLinkNonTote: 124457 } },
      { id: 2, typeName: 'Dundalk', name: 'Race 2', startTime: 345678, externalKeys: { OBEvLinkNonTote: 124456 } },
      { id: 3, typeName: 'Flemington TH', name: 'Race 1', startTime: 123456, localTime: '11:40' },
      { id: 4, typeName: 'Vaal (SA)', name: 'Race 1', startTime: 123456, isResulted: true },
    ] as any;

    gtmService = jasmine.createSpyObj('gtm', [ 'push' ]);
    toteService = {
      getEventById: jasmine.createSpy('getEventById').and.callFake(() => of({
        isResulted: false
      })),
      filterToteGroup: jasmine.createSpy('filterToteGroup'),
      getToteLink: jasmine.createSpy('getToteLink').and.returnValue(of('foo')),
      getRawToteEvents: jasmine.createSpy('getRawToteEvents').and.returnValue(of(events))
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };

    locale = {
      getString: jasmine.createSpy('locale.getString')
    } as any;

    storage = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set'),
    };

    buildUtilityService = {
      getLocalTime: jasmine.createSpy('buildUtilityService.getLoocalTime')
    };

    vEPService = {
      bannerBeforeAccorditionHeader:  new BehaviorSubject<any>('bannerBeforeAccorditionHeader' as any),
      targetTab:  new BehaviorSubject<any>('targetTab' as any),
    }

    component = new ToteSliderComponent(toteService, gtmService, router, locale, storage, buildUtilityService,vEPService);
  });

  describe('@parseTypeName', () => {
    it('should return parsed value', () => {
      expect(component.parseTypeName('Dundalk')).toEqual('Dunda');
      expect(component.parseTypeName('Chelmsford City')).toEqual('Chelm');
      expect(component.parseTypeName('Vaal (SA)')).toEqual('Vaal');
      expect(component.parseTypeName('Sale TH')).toEqual('Sale');
      expect(component.parseTypeName('Sale TH ')).toEqual('Sale');
      expect(component.parseTypeName('Turf Paradise')).toEqual('TurfP');
      expect(component.parseTypeName('Tur Paradise')).toEqual('TurPa');
      expect(component.parseTypeName('Tu Paradise')).toEqual('TuPar');
      expect(component.parseTypeName('T Paradise')).toEqual('TPara');
    });
  });

  describe('@sortEvents', () => {
    it('should sort events', () => {
      const result = component.sortEvents(events);
      expect(_.pluck(result, 'id')).toEqual([4, 3, 1, 2]);
    });
  });

  describe('@prepareData', () => {
    beforeEach(() => {
      spyOn(component, 'filterLinkedToteEvents').and.returnValue(events);
      spyOn(component, 'parseTypeName').and.callThrough();
    });

    it('should not sort events and parse names', () => {
      component.prepareData(events);
      expect(component['filterLinkedToteEvents']).toHaveBeenCalled();
      expect(component.parseTypeName).toHaveBeenCalledTimes(4);
    });

    it('should sort events and parse names', () => {
      toteService.filterToteGroup.and.returnValue(events);
      const sorted = component.prepareData(events, true);
      expect(sorted[0].id).toBe(1);
    });
  });

  describe('@ngOnChanges', () => {
    it('should sort events and parse names when eventsData were changed', () => {
      spyOn(component, 'filterLinkedToteEvents').and.returnValue(events);
      spyOn(component, 'parseTypeName').and.callThrough();
      const changes = {
        eventsData: {
          currentValue: events,
          previousValue: []
        }
      } as any;

      component.ngOnChanges(changes);
      expect(component['filterLinkedToteEvents']).toHaveBeenCalled();
      expect(component.parseTypeName).toHaveBeenCalledTimes(4);
    });

    it('should not sort events and parse names when eventsData not changed', () => {
      spyOn(component, 'filterLinkedToteEvents').and.returnValue(events);
      spyOn(component, 'parseTypeName').and.callThrough();
      const changes = {} as any;

      component.ngOnChanges(changes);
      expect(component['filterLinkedToteEvents']).not.toHaveBeenCalled();
      expect(component.parseTypeName).not.toHaveBeenCalled();
    });
  });

  describe('filterLinkedToteEvents', () => {
    it('should filter out not linked tote events', () => {
      const result = component['filterLinkedToteEvents'](events);
      expect(result).toEqual([
        { id: 1, typeName: 'Dundalk', name: 'Race 1', startTime: 234567, externalKeys: { OBEvLinkNonTote: 124457 } },
        { id: 2, typeName: 'Dundalk', name: 'Race 2', startTime: 345678, externalKeys: { OBEvLinkNonTote: 124456 } }
      ] as any);
    });

    it('behave correct when undefined passed', () => {
      const result = component['filterLinkedToteEvents'](undefined);
      expect(result).toEqual([] as any);
    });
  });

  describe('@clickEvent', () => {

    it('should track', () => {
      spyOn(component, 'trackEvent');
      component.clickEvent({} as any);

      expect(component.trackEvent).toHaveBeenCalledWith({} as any);
    });

    it('should start redirection', () => {
      component.clickEvent({id: '54321', externalKeys: {OBEvLinkNonTote: '12345'}} as any);

      expect(toteService.getToteLink).toHaveBeenCalledWith('12345', '54321', false);
    });

    it('should start redirection (non-linked tote)', () => {
      component.clickEvent({id: '54321'} as any);

      expect(toteService.getToteLink).toHaveBeenCalledWith(undefined, '54321', false);
    });

    it('should redirect if passed event contains enough data', fakeAsync(() => {
      component.clickEvent({id: '54321', externalKeys: {OBEvLinkNonTote: '12345'}} as any);

      expect(toteService.getToteLink).toHaveBeenCalled();
      expect(router.navigate).toHaveBeenCalled();
    }));

    it('should skip redirect if something went wrong', fakeAsync(() => {
      toteService.getToteLink.and.returnValue(of(''));
      component.clickEvent({id: '54321', externalKeys: {OBEvLinkNonTote: '12345'}} as any);

      expect(toteService.getToteLink).toHaveBeenCalled();
      expect(router.navigate).not.toHaveBeenCalled();
    }));

    it('should unsubscribe from previious event loader', () => {
      const loadEventSubscription = jasmine.createSpyObj('loadEventSubscription', ['unsubscribe']);

      component['loadEventSubscription'] = loadEventSubscription;
      toteService.getToteLink.and.returnValue(of(''));
      component.clickEvent({id: '54321', externalKeys: {OBEvLinkNonTote: '12345'}} as any);

      expect(loadEventSubscription.unsubscribe).toHaveBeenCalled();
      expect(component['loadEventSubscription']).not.toEqual(loadEventSubscription);
    });
  });

  describe('ngOnInit', () => {
    it('should store load data subscription', () => {
      component.prepareData = jasmine.createSpy('prepareData').and.returnValue([]);
      component.eventsData = [{ id: 123 }] as any;
      component.ngOnInit();
      expect(component['storage'].set).toHaveBeenCalled();
      expect(component.eventsData).toEqual([]);
    });

    it('should get events from storage', () => {
      component['checkStoredTime'] = jasmine.createSpy('checkStoredTime').and.returnValue(false);
      component['storage'].get = jasmine.createSpy('storage.get').and.returnValue({data: [], time: 1234321});
      spyOn(component as any, 'filterEventsData');
      component.ngOnInit();
      expect(component.eventsData).toEqual([] as any);
    });

    it('should be expanded', () => {
      storage.get.and.returnValue(true);
      component.ngOnInit();
      expect(component.isExpanded).toBeTruthy();
    });

    it('should get data from ss-request if featured is down', () => {
      component.prepareData = jasmine.createSpy('prepareData').and.returnValue([]);
      component.eventsData = [{ name: 'ITC' }] as any;
      component.ngOnInit();
      expect(toteService.getRawToteEvents).toHaveBeenCalled();
      toteService.getRawToteEvents(1).subscribe(() => {
        expect(component['storage'].set).toHaveBeenCalled();
        expect(component.eventsData).toEqual([]);
      });
    });
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe from event loader', () => {
      const loadEventSubscription = jasmine.createSpyObj('loadEventSubscription', ['unsubscribe']);

      component['loadEventSubscription'] = loadEventSubscription;
      component.ngOnDestroy();

      expect(loadEventSubscription.unsubscribe).toHaveBeenCalled();
    });

    it('should unsubscribe from data loader', () => {
      const loadDataSubscription = jasmine.createSpyObj('loadDataSubscription', ['unsubscribe']);

      component['loadDataSubscription'] = loadDataSubscription;
      component.ngOnDestroy();

      expect(loadDataSubscription.unsubscribe).toHaveBeenCalled();
    });
  });

  it('trackById', () => {
    expect(component.trackById(0, { id: 1 } as any)).toBe(1);
  });

  it('checkStoredTime returns true', () => {
    const time1 = 10000;
    const time2 = 395000;
    expect(component['checkStoredTime'](time1, time2)).toBe(true);
  });

  it('checkStoredTime returns false', () => {
    const time1 = 10000;
    const time2 = 170000;
    expect(component['checkStoredTime'](time1, time2)).toBe(false);
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
