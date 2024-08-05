import { fakeAsync, tick } from '@angular/core/testing';
import { QuickSwitchPanelComponent } from './quick-switch-panel.component';
import { Subject, of } from 'rxjs';

describe('QuickSwitchPanelComponent', () => {
  let component: QuickSwitchPanelComponent;
  let WindowRefService;
  let ElementRef;
  let DomToolsService;
  let CurrentMatchesService;
  let DeviceService;
  let FiltersService;
  let ChangeDetectorRef;
  let GtmService;
  let ActivatedRoute;
  let RendererService;
  let PubSubService;
  let sportConfig;
  beforeEach(() => {
    sportConfig = {
      data: {
        events: [{ name: 'eventName' }],
        type: {
          id: 'typeId',
          name: 'typeName',
          classId: 'classId'
        }
      }
    }

    DeviceService = {
      getDeviceViewType: jasmine.createSpy('getDeviceViewType').and.returnValue('deviceViewType'),
      isTablet: false,
      isMobile: true,
      isLadbrokes: true,
      isIosWrapper: true,
      isWrapper: true
    };
    DomToolsService = {
      getHeight: jasmine.createSpy().and.returnValue(1000),
      getOffset: jasmine.createSpy().and.returnValue({ top: 20 }),
      getWidth: jasmine.createSpy().and.returnValue('100%'),
      css: jasmine.createSpy('css'),
      getScrollTopPosition: jasmine.createSpy('getScrollTopPosition'),
      getPageScrollTop: jasmine.createSpy('getPageScrollTop').and.returnValue(200)
    };
    FiltersService = {
      orderBy: jasmine.createSpy('orderBy').and.callFake(data => data)
    };
    RendererService = {
      renderer: {
        addClass: jasmine.createSpy('addClass'),
        removeClass: jasmine.createSpy('removeClass')
      }
    };
    WindowRefService = {
      nativeWindow: {
        setInterval: jasmine.createSpy('setInterval'),
        clearInterval: jasmine.createSpy('clearInterval')
      },
      document: {
        querySelector: jasmine.createSpy('querySelector')
      }
    };
    GtmService = {
      push: jasmine.createSpy('push')
    };

    ActivatedRoute = {
      params: of({})
    };
    CurrentMatchesService = {
      subscribeForUpdates: jasmine.createSpy('subscribeForUpdates'),
      unSubscribeForUpdates: jasmine.createSpy('unSubscribeForUpdates'),
      getEventsByTypeWithMarketCounts: jasmine.createSpy('getEventsByTypeWithMarketCounts')
    };
    ElementRef = {
      querySelector: (section) => {
        return section;
      },
      nativeElement: {}
    };
    ChangeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    PubSubService = {
      publish: jasmine.createSpy('publish'),
      API: 'QUICK_SWITCHER_ACTIVE'
    };
    component = new QuickSwitchPanelComponent(
      WindowRefService,
      ElementRef,
      DomToolsService,
      CurrentMatchesService,
      DeviceService,
      FiltersService,
      ChangeDetectorRef,
      GtmService,
      ActivatedRoute,
      RendererService,
      PubSubService
    );
    component['element'] = {
      querySelector: jasmine.createSpy().and.returnValue({}),
      getBoundingClientRect: jasmine.createSpy().and.returnValue({
        left: 20
      })
    } as any;
    ActivatedRoute.params = new Subject();
    component.sport = {
      arrangeEventsBySection: jasmine.createSpy('arrangeEventsBySection').and.returnValue([{
        groupedByDate: [{events: [{categoryCode: 'FOOTBALL'}], title: 'today'}]
      }]),
      sportConfig: { config: {request: {categoryId: '16'}}}
    } as any;
    spyOn(component.closeQuickSwitchPanel, 'emit');
  });

  describe('@ngOnInit', () => {
    it('should call relocate function', () => {
      spyOn(component, 'relocate');

      WindowRefService.nativeWindow.setInterval.and.callFake(cb => cb());
      CurrentMatchesService.getEventsByTypeWithMarketCounts = jasmine.createSpy('getEventsByTypeWithMarketCounts').and.returnValue(Promise.resolve([]));
      component.ngOnInit();

      expect(WindowRefService.nativeWindow.setInterval).toHaveBeenCalledTimes(1);
      expect(component.relocate).toHaveBeenCalled();
    });

    it('should add quick-switch-scroll-overlay class to homeBody on mobile', () => {
      component.isMobile = true;
      const homeBody = document.createElement('div');
      WindowRefService.document.querySelector.and.returnValue(homeBody);
      CurrentMatchesService.getEventsByTypeWithMarketCounts = jasmine.createSpy('getEventsByTypeWithMarketCounts').and.returnValue(Promise.resolve([]));
      component.ngOnInit();
      //expect(component.homeBody).toBe(filter);
      expect(RendererService.renderer.addClass).toHaveBeenCalledWith(homeBody, 'quick-switch-scroll-overlay');
    });

    it('should not add quick-switch-scroll-overlay class to homeBody when not on mobile', () => {
      component.isMobile = false;
      const homeBody = document.createElement('div');
      WindowRefService.document.querySelector.and.returnValue(homeBody);
      CurrentMatchesService.getEventsByTypeWithMarketCounts = jasmine.createSpy('getEventsByTypeWithMarketCounts').and.returnValue(Promise.resolve([]));
      component.ngOnInit();
      expect(RendererService.renderer.addClass).not.toHaveBeenCalled();
    });
  });
  describe('@ngDestroy', () => {
    it('should call PubSubService.publish if isMobile is true', () => {
      component.ngOnDestroy();
      expect(PubSubService.publish).toHaveBeenCalledWith(
        PubSubService.API.QUICK_SWITCHER_ACTIVE,
        false
      );
    });

    it('should call closeMenu', () => {
      spyOn(component, 'closeMenu');
      component.interval = setInterval(() => { }, 1000);
      component.ngOnDestroy();
      expect(component.closeMenu).toHaveBeenCalled();
    });

    it('should unsubscribe from getDataSubscription if it exists', () => {
      const unsubscribeSpy = jasmine.createSpy('unsubscribe');
      component['getDataSubscription'] = { unsubscribe: unsubscribeSpy } as any;
      component.ngOnDestroy();
      expect(unsubscribeSpy).toHaveBeenCalled();
    });

    it('should not throw an error when unsubscribing from null getDataSubscription', () => {
      component['getDataSubscription'] = null;

      expect(() => component.ngOnDestroy()).not.toThrow();
    });

    it('should unsubscribe from routeParamsListener if it exists', () => {
      const unsubscribeSpy = jasmine.createSpy('unsubscribe');
      component['routeParamsListener'] = { unsubscribe: unsubscribeSpy } as any;

      component.ngOnDestroy();

      expect(unsubscribeSpy).toHaveBeenCalled();
    });

    it('should not throw an error when unsubscribing from null routeParamsListener', () => {
      component['routeParamsListener'] = null;

      expect(() => component.ngOnDestroy()).not.toThrow();
    });

    it('should remove the "quick-switch-scroll-overlay" class from homeBody if isMobile is true and homeBody exists', () => {
      component.isMobile = true;
      component.homeBody = document.createElement('div');

      component.ngOnDestroy();

      expect(RendererService.renderer.removeClass).toHaveBeenCalledWith(
        component.homeBody,
        'quick-switch-scroll-overlay'
      );
    });

    it('should not remove the class from homeBody if isMobile is false', () => {
      component.isMobile = false;
      component.homeBody = document.createElement('div');

      component.ngOnDestroy();

      expect(RendererService.renderer.removeClass).not.toHaveBeenCalled();
    });

    it('should not remove the class from homeBody if homeBody is null', () => {
      component.isMobile = true;
      component.homeBody = null;

      component.ngOnDestroy();

      expect(RendererService.renderer.removeClass).not.toHaveBeenCalled();
    });
  });
  describe('#closeMenu', () => {
    it('should emit closeQuickSwitchPanel event', () => {
      component.closeMenu();
      expect(component.closeQuickSwitchPanel.emit).toHaveBeenCalled();
    });

    it('should call gaTracking when fromClick is true', () => {
      const fromClick = true;
      component.closeMenu(fromClick);
      component['gaTracking']('info', 'track1', 'name');
    });

    it('should remove the "quick-switch-scroll-overlay" class from homeBody if it exists and isMobile is true', () => {
      component.isMobile = true;
      component.homeBody = document.createElement('div');
      component.closeMenu();
    });

    it('should emit closeQuickSwitchPanel event', () => {
      component.closeMenu();
      expect(component.closeQuickSwitchPanel.emit).toHaveBeenCalled();
    });

    it('should remove the "quick-switch-scroll-overlay" class from homeBody if it exists and isMobile is true', () => {
      component.isMobile = true;
      component.homeBody = document.createElement('div');
      component.closeMenu();
      expect(RendererService.renderer.removeClass).toHaveBeenCalledWith(
        component.homeBody,
        'quick-switch-scroll-overlay'
      );
    });

    it('should not remove the class from homeBody if isMobile is false', () => {
      component.isMobile = false;
      component.homeBody = document.createElement('div');
      component.closeMenu();
      expect(RendererService.renderer.removeClass).not.toHaveBeenCalled();
    });

    it('should not remove the class from homeBody if isMobile is false', () => {
      component.isMobile = false;
      component.homeBody = document.createElement('div');
      component.closeMenu();
      expect(RendererService.renderer.removeClass).not.toHaveBeenCalled();
    });

    it('should not remove the class from homeBody if homeBody is null', () => {
      component.isMobile = true;
      component.homeBody = null;
      component.closeMenu();
      expect(RendererService.renderer.removeClass).not.toHaveBeenCalled();
    });
  });
  describe('#selectTab', () => {
    it('should update activeTab with the provided id and name', () => {
      const tab = { id: 'tab-today', name: 'today' };
      component['selectTab']({ id: tab.id, tab: tab });
      expect(component.activeTab.id).toEqual(tab.id);
      expect(component.activeTab.name).toEqual(tab.name);
    });
    it('should update activeTab with tomorrow', () => {
      component.tomorrowEvents =  [{events: [{categoryCode: 'FOOTBALL'}], title: 'tomorrow'}] as any;
      component.filteredQuickSwitchEvents = [];
      const tab = { id: 'tab-tomorrow', name: 'tomorrow' };
      component['selectTab']({ id: tab.id, tab: tab });
      expect(component.activeTab.id).toEqual(tab.id);
      expect(component.activeTab.name).toEqual(tab.name);
      expect(component.filteredQuickSwitchEvents).toEqual(component.tomorrowEvents);
    });
    it('should update activeTab with future', () => {
      component.futureEvents =  [{events: [{categoryCode: 'FOOTBALL'}], title: 'future'}] as any;
      component.filteredQuickSwitchEvents = [];
      const tab = { id: 'tab-future', name: 'future' };
      component['selectTab']({ id: tab.id, tab: tab });
      expect(component.activeTab.id).toEqual(tab.id);
      expect(component.activeTab.name).toEqual(tab.name);
      expect(component.filteredQuickSwitchEvents).toEqual(component.futureEvents);
    });
  });
  describe('#loadCompetitionsData', () => {
    it('should load and arrange competition data and set isLoaded to true for today events', fakeAsync(() => {
      CurrentMatchesService.getEventsByTypeWithMarketCounts = jasmine.createSpy('getEventsByTypeWithMarketCounts').and.returnValue(Promise.resolve([]));
      const fakeEvents ={groupedByDate: [{events: [{categoryCode: 'FOOTBALL'}], title: 'today'}]};
      spyOn(component, 'groupEvents').and.callThrough();
      component.loadCompetitionsData();
      tick();
      expect(component.eventsByCategory).toEqual(fakeEvents as any);
      expect(component.sport.arrangeEventsBySection).toHaveBeenCalled();
      expect(CurrentMatchesService.unSubscribeForUpdates).toHaveBeenCalled(); 
      expect(CurrentMatchesService.subscribeForUpdates).toHaveBeenCalled();
      expect(component.isLoaded).toEqual(true);
      expect(component.groupEvents).toHaveBeenCalled();
      expect(component.todayEvents).toEqual(fakeEvents.groupedByDate as any);
      expect(ChangeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('should load and arrange competition data and set isLoaded to true for tomorrow events', fakeAsync(() => {
      CurrentMatchesService.getEventsByTypeWithMarketCounts = jasmine.createSpy('getEventsByTypeWithMarketCounts').and.returnValue(Promise.resolve([]));
      component.sport.arrangeEventsBySection = jasmine.createSpy('arrangeEventsBySection').and.returnValue([{
        groupedByDate: [{events: [{categoryCode: 'FOOTBALL'}], title: 'tomorrow'}]
      }]);
      const fakeEvents ={groupedByDate: [{events: [{categoryCode: 'FOOTBALL'}], title: 'tomorrow'}]};
      spyOn(component, 'groupEvents').and.callThrough();
      component.loadCompetitionsData();
      tick();
      expect(component.eventsByCategory).toEqual(fakeEvents as any);
      expect(component.sport.arrangeEventsBySection).toHaveBeenCalled();
      expect(CurrentMatchesService.unSubscribeForUpdates).toHaveBeenCalled(); 
      expect(CurrentMatchesService.subscribeForUpdates).toHaveBeenCalled();
      expect(component.isLoaded).toEqual(true);
      expect(component.groupEvents).toHaveBeenCalled();
      expect(component.tomorrowEvents).toEqual(fakeEvents.groupedByDate as any);
      expect(ChangeDetectorRef.detectChanges).toHaveBeenCalled();
    }));
    it('should load and arrange competition data and set isLoaded to true for future events', fakeAsync(() => {
      CurrentMatchesService.getEventsByTypeWithMarketCounts = jasmine.createSpy('getEventsByTypeWithMarketCounts').and.returnValue(Promise.resolve([]));
      component.sport.arrangeEventsBySection = jasmine.createSpy('arrangeEventsBySection').and.returnValue([{
          groupedByDate: [{events: [{categoryCode: 'FOOTBALL'}], title: 'future'}]
        }]);
      const fakeEvents ={groupedByDate: [{events: [{categoryCode: 'FOOTBALL'}], title: 'future'}]};
      spyOn(component, 'groupEvents').and.callThrough();
      component.loadCompetitionsData();
      tick();
      expect(component.eventsByCategory).toEqual(fakeEvents as any);
      expect(component.sport.arrangeEventsBySection).toHaveBeenCalled();
      expect(CurrentMatchesService.unSubscribeForUpdates).toHaveBeenCalled(); 
      expect(CurrentMatchesService.subscribeForUpdates).toHaveBeenCalled();
      expect(component.isLoaded).toEqual(true);
      expect(component.groupEvents).toHaveBeenCalled();
      expect(component.futureEvents).toEqual(fakeEvents.groupedByDate as any);
      expect(ChangeDetectorRef.detectChanges).toHaveBeenCalled();
    }));
    it('when event data is not available', fakeAsync(() => {
      CurrentMatchesService.getEventsByTypeWithMarketCounts = jasmine.createSpy('getEventsByTypeWithMarketCounts').and.returnValue(Promise.resolve([]));
      component.sport.arrangeEventsBySection = jasmine.createSpy('arrangeEventsBySection').and.returnValue([{
          groupedByDate: null
        }]);;
      spyOn(component, 'groupEvents').and.callThrough();
      component.loadCompetitionsData();
      tick();
      expect(component.isLoaded).toBeFalse();
      expect(component.groupEvents).toHaveBeenCalled();
      expect(component.filteredQuickSwitchEvents).toEqual([]);
    }));
  });
  describe('#initLazyHandler', () => {
    it('should set isLazyComponentLoaded to true', () => {
      component.isLazyComponentLoaded = false;
      component.initLazyHandler();
      expect(component.isLazyComponentLoaded).toBe(true);
    });

    it('should set isChildComponentLoaded to true', () => {
      component.isChildComponentLoaded = false;
      component.initLazyHandler();
      expect(component.isChildComponentLoaded).toBe(true);
    });

    it('should set both isLazyComponentLoaded and isChildComponentLoaded to true', () => {
      component.isLazyComponentLoaded = false;
      component.isChildComponentLoaded = false;
      component.initLazyHandler();
      expect(component.isLazyComponentLoaded).toBe(true);
      expect(component.isChildComponentLoaded).toBe(true);
    });

    it('should not change properties if they are already true', () => {
      component.isLazyComponentLoaded = true;
      component.isChildComponentLoaded = true;
      component.initLazyHandler();
      expect(component.isLazyComponentLoaded).toBe(true);
      expect(component.isChildComponentLoaded).toBe(true);
    });
  });
  describe('#relocate', () => {
    it('should return early when isMobileOrigin is true and isTablet is false', () => {
      DeviceService.isMobileOrigin = true;
      DeviceService.isTablet = false;
      const isLazyComponentLoadedBefore = component.isLazyComponentLoaded;
      const isChildComponentLoadedBefore = component.isChildComponentLoaded;
      component.relocate();
      expect(component.isLazyComponentLoaded).toBe(isLazyComponentLoadedBefore);
      expect(component.isChildComponentLoaded).toBe(isChildComponentLoadedBefore);
    });

    it('should set dashboardHeight to DASHBOARD_MIN_HEIGHT when getHeight returns falsy and isLadbrokes is truthy', () => {
      component.isLadbrokes = true;
      DomToolsService.getHeight = 0;
      spyOn(DomToolsService, 'getHeight').and.returnValue(0);
      component.relocate();
      expect(component.sticky).toBeFalse();
    });

    it('should set dashboardHeight to DASHBOARD_MIN_HEIGHT_CORAL when getHeight returns falsy and isLadbrokes is falsy', () => {
      component.isLadbrokes = false;
      DomToolsService.getHeight = 0;
      spyOn(DomToolsService, 'getHeight').and.returnValue(0);
      component.relocate();
      expect(component.sticky).toBeFalse();
    });

    it('should set dashboardOffset to zero', () => {
      DomToolsService.getOffset = 0;
      spyOn(DomToolsService, 'getOffset').and.returnValue(0);
      component.relocate();
      expect(component.sticky).toBeTrue();
    });

    it('should set dashboardBottom to TABLET_BOTTOM_MENU_HEIGHT when isMobile and isDesktop falsy', () => {
      DeviceService.isMobile = false;
      DeviceService.isDesktop = false;
      DomToolsService.getHeight = 0;
      spyOn(DomToolsService, 'getHeight').and.returnValue(0);
      component.relocate();
      expect(component.sticky).toBeFalse();
    });

    it('should should call relocate method when element is sticky', () => {
      component.isLadbrokes = true
      const container = {
        querySelector: ''
      }
      component.relocate();
      expect(DomToolsService.css).toHaveBeenCalled();
    });

    it('should return early when dashboard is falsy', () => {
      const container = document.createElement('div');
      const dashboard = null;
      const closeMenu = document.createElement('div');
      const overlay = document.createElement('div');
      component.element = container;
      spyOn(container, 'querySelector').and.returnValues(dashboard, closeMenu, overlay);
      component.relocate();
    });

    it('should should call relocate method when element is not sticky', () => {
      component['windowRefService'].nativeWindow.pageYOffset = 2000;
      component.relocate();
      expect(DomToolsService.css).not.toHaveBeenCalled();
    });

    it('should apply style to overlay if overlay exists', () => {
      const overlay = document.createElement('div');
      spyOn(document, 'querySelector').and.returnValue(overlay);
      component.relocate();
      expect(DomToolsService.css).toHaveBeenCalled();
    });
  });

  it('should perform GA tracking', () => {
    const data = {
      'event': 'Event.Tracking',
      'component.CategoryEvent': 'event switcher',
      'component.LabelEvent': 'events',
      'component.ActionEvent': 'click',
      'component.PositionEvent': 'track',
      'component.LocationEvent': 'edp',
      'component.EventDetails': 'name'
    }
    component['gaTracking']('click', 'track', 'name');
    expect(GtmService.push).toHaveBeenCalledWith('Event.Tracking', data as any);
  });
});
