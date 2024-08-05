import { fakeAsync, tick } from '@angular/core/testing';
import { InspiredVirtualComponent } from './inspired-virtual.component';
import { ISportEvent } from '@core/models/sport-event.model';
import { BehaviorSubject } from 'rxjs/internal/BehaviorSubject';

describe('InspiredVirtualComponent', () => {
  let component: InspiredVirtualComponent,
    inspiredVirtualService,
    router,
    storage,
    virtualSharedService,
    vEPService;

  beforeEach(() => {
    inspiredVirtualService = {
      config: {
        slidesLimit: 5
      },
      getEvents: jasmine.createSpy().and.returnValue(Promise.resolve([])),
      setupEvents: jasmine.createSpy().and.returnValue([]),
      sendGTMOnFirstTimeCollapse: jasmine.createSpy(),
      sendGTMOnGoToLiveEvent: jasmine.createSpy(),
      virtualsGTMEventTracker: jasmine.createSpy(),
      getStartTime: jasmine.createSpy().and.returnValue('testStartTime'),
      destroyTimers: jasmine.createSpy()
    };

    router = {
      navigate: jasmine.createSpy(),
      navigateByUrl: jasmine.createSpy()
    };
    storage = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set'),
    };

    virtualSharedService = {
      formVirtualTypeUrl: () => {},
      formVirtualEventUrl: () => {}
    };

    vEPService = {
      bannerBeforeAccorditionHeader:  new BehaviorSubject<any>('bannerBeforeAccorditionHeader' as any),
      targetTab:  new BehaviorSubject<any>('targetTab' as any),
    };

    component = new InspiredVirtualComponent(inspiredVirtualService, router, storage, virtualSharedService, vEPService);
  });

  it('should create component instance', () => {
    component.eventsData = [{}];
    component.ngOnInit();

    expect(component).toBeTruthy();
    expect(component.carouselName).toEqual('inspired-virtual');
    expect(component.isFirstTimeCollapsed).toBeFalsy();
  });

  it('should test ngOnInit (setupEvents)', fakeAsync(() => {
    component.eventsData = [{}];
    storage.get.and.returnValue(true);
    component.ngOnInit();
    tick();
    expect(inspiredVirtualService.setupEvents).toHaveBeenCalled();
    expect(component.eventsArray).toEqual([] as any);
    expect(component.isExpanded).toBeTruthy();
  }));

  it('should redirect virtual sports when only next events is available', () => {
    component.eventsData = [{}];
    component.isVirtualHomePage = true;
    component.IsOnlyNextEventEnabled = true;
    component.ngOnInit();
    expect(router.navigate).toHaveBeenCalledWith(['virtual-sports/sports']);
  });

  it('should test ngOnInit (getEvents)', fakeAsync(() => {
    component.eventsData = [{ name: 'VRC' }];
    storage.get.and.returnValue(true);
    component.ngOnInit();
    tick();
    expect(inspiredVirtualService.getEvents).toHaveBeenCalled();
  }));

  it('should test trackById', () => {
    expect(component.trackById(1, { id : 1 } as any)).toEqual('11');
  });

  it('should test sendCollapseGTM positive', () => {
    component.sportName = 'horseracing';
    component.sendCollapseGTM();
    expect(inspiredVirtualService.sendGTMOnFirstTimeCollapse).toHaveBeenCalled();
    expect(component.isFirstTimeCollapsed).toBeTruthy();
  });

  it('should test sendCollapseGTM negative', () => {
    component.sportName = 'horseracing';
    component.isFirstTimeCollapsed = true;
    component.sendCollapseGTM();
    expect(inspiredVirtualService.sendGTMOnFirstTimeCollapse).not.toHaveBeenCalled();
    expect(component.isFirstTimeCollapsed).toBeTruthy();
  });

  describe('viewAllVirtual', () => {
    it('should test viewAllVirtual', () => {
      const event = { classId: '123'} as ISportEvent;
      component.viewAllVirtual(event);
      expect(router.navigateByUrl).toHaveBeenCalled();
    });

    it('should test viewAllVirtual when event is undefined', () => {
      const event = undefined;
      component.viewAllVirtual(event);
      expect(router.navigateByUrl).toHaveBeenCalledWith('virtual-sports/sports');
    });
  });

  it('should test getStartTime', () => {
    expect(component.getStartTime(111)).toEqual('testStartTime');
    expect(inspiredVirtualService.getStartTime).toHaveBeenCalledWith(111);
  });

  describe('goToLiveEvent', () => {

    it('should test goToLiveEvent when isVirtualHomePage is true', () => {
      const event = { classId: '123'} as ISportEvent;
      component.isVirtualHomePage = true;
      component.goToLiveEvent(event);
      expect(inspiredVirtualService.virtualsGTMEventTracker).toHaveBeenCalled();
      expect(router.navigateByUrl).toHaveBeenCalled();
    });

    it('should test goToLiveEvent', () => {
      const event = { classId: '123'} as ISportEvent;
      component.goToLiveEvent(event);
      expect(inspiredVirtualService.sendGTMOnGoToLiveEvent).toHaveBeenCalled();
      expect(router.navigateByUrl).toHaveBeenCalled();
    });

    it('should test goToLiveEvent when classId is undefined', () => {
      component.goToLiveEvent( undefined);
      expect(inspiredVirtualService.sendGTMOnGoToLiveEvent).toHaveBeenCalled();
      expect(router.navigateByUrl).toHaveBeenCalledWith('virtual-sports/sports');
    });
  });

  describe('ngOnDestroy', () => {
    it('should test ngOnDestroy', () => {
      component['loadDataSubscription'] = null;
      component.ngOnDestroy();

      expect(inspiredVirtualService.destroyTimers).toHaveBeenCalled();
    });

    it('should unsubscribe from data load subscription', () => {
      const loadDataSubscription = jasmine.createSpyObj('loadDataSubscription', ['unsubscribe']);

      component['loadDataSubscription'] = loadDataSubscription;
      component.ngOnDestroy();

      expect(loadDataSubscription.unsubscribe).toHaveBeenCalled();
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
