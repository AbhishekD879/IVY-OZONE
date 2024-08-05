import { fakeAsync, tick } from '@angular/core/testing';
import { GreyhoundsTabsComponent } from '@racing/components/racingTabsModule/greyhoundsTabs/greyhounds-tabs.component';
import { of } from 'rxjs';


describe('GreyhoundsTabsComponent', () => {
  let component: GreyhoundsTabsComponent;
  let router, filterService, racingGaService, routingHelperService, eventService, pubSubService, cmsService, vEPService;
  let widgetSpyObj, gtm;


  beforeEach(() => {
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl'),
      url: 'url1'
    };
    filterService = {
      orderBy: jasmine.createSpy(),
      date: jasmine.createSpy()
    };
    racingGaService = {
      trackModule: jasmine.createSpy(),
      reset: jasmine.createSpy()
    };
    routingHelperService = {
      formSportUrl: jasmine.createSpy('formSportUrl').and.returnValue(of('url')),
      formEdpUrl: jasmine.createSpy()
    };
    eventService = {
      isAnyCashoutAvailable: jasmine.createSpy()
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe')
        .and.callFake((a: string, b: string[] | string, fn: Function) => {
          if (b === 'SHOW_WIDGET') {
            fn(widgetSpyObj);
            return;
          }
          fn();
        }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        RELOAD_GREYHOUNDS_TABS: 'RELOAD_GREYHOUNDS_TABS',
        SHOW_WIDGET: 'SHOW_WIDGET',
        RELOAD_COMPONENTS: 'RELOAD_COMPONENTS'
      }
    };
    cmsService = {};
    gtm = {
      push: jasmine.createSpy('push')
    };
    vEPService = {
      targetTab: {subscribe : (cb) => cb()},
      lastBannerEnabled: {subscribe : (cb) => cb()},
      accorditionNumber: {subscribe : (cb) => cb()},
    };

    component = new GreyhoundsTabsComponent(router, filterService, racingGaService, routingHelperService,
      eventService, pubSubService, cmsService, gtm, vEPService);
    component.viewByFilters = 'by-time';
    component.filteredTypeNames = [{
      name: 'A Type',
      isExpanded: true
    }, {
      name: 'B Type',
      isExpanded: false
    }] as any;
  });

  it('should create GreyhoundsTabsComponent instance', () => {
    expect(component).toBeTruthy();
  });

  it('should get data if filter async was changed', () => {
    component.filterInitData = jasmine.createSpy();
    component.ngOnChanges({
      viewByFilters: 'by-meeting'
    } as any);

    expect(component.filterInitData).toHaveBeenCalled();
  });

  it('ngOnInit', () => {
    component.display = 'today';
    component.filter = 'by-meeting';
    component.sportName = 'greyhound';
    component.handleFutureTabLoaded = jasmine.createSpy();
    component.ngOnInit();

    expect(component.isDailyRacingModule).toEqual(true);
    expect(component.handleFutureTabLoaded).toHaveBeenCalled();
    expect(pubSubService.subscribe).toHaveBeenCalledWith('greyhoundsTabsComponent', 'SHOW_WIDGET', jasmine.any(Function));
    component.switchers.forEach(switcher => {
      switcher.onClick();
    });

    expect(routingHelperService.formSportUrl).toHaveBeenCalledTimes(2);
  });

  it('ngOnInit passing widgetSpyObj', () => {
      widgetSpyObj = {
        name: 'next-races',
        data: ['random-data']
      };
      // case with correct widget object
      component.nextRacesWidgetVisible = false;
      component.handleFutureTabLoaded = jasmine.createSpy();
      component.ngOnInit();
      expect(component.nextRacesWidgetVisible).toBeTruthy();
      expect(component.handleFutureTabLoaded).toHaveBeenCalled();
      widgetSpyObj = {
        name: 'not-next-races',
        data: ['random-data']
      };
      // case without widget data
      component.nextRacesWidgetVisible = false;
      component.ngOnInit();
      expect(component.nextRacesWidgetVisible).toBeFalsy();

      widgetSpyObj = {
        name: 'next-races',
        data: []
      };
      // case without widget data
      component.nextRacesWidgetVisible = false;
      component.ngOnInit();
      expect(component.nextRacesWidgetVisible).toBeFalsy();
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('greyhoundsTabsComponent');
    expect(racingGaService.reset).toHaveBeenCalled();
  });

  describe('@filterInitData', () => {
    it('it should filter racing data', () => {
      component.display = 'lorem';
      component.racing = {
        classesTypeNames: {
          default: [{
            name: 'B Type'
          }, {
            name: 'A Type'
          }]
        },
        events: [{ id: 1, typeName: 'A Type' }, { id: 2, typeName: 'A Type' }, { id: 3, typeName: 'B Type' }, { id: 4, typeName: 'C Type' }]
      } as any;
      component.eventsOrder = ['startTime', 'name'];
      component.filterInitData();
      expect(filterService.orderBy).toHaveBeenCalledWith(component.racing.events, component.eventsOrder);
      expect(component.filteredTypeNames).toEqual([{
        name: 'A Type'
      }, {
        name: 'B Type'
      }]);
      expect(component.orderedEventsByTypeNames).toEqual([[{
        id: 1,
        typeName: 'A Type'
      }, {
        id: 2,
        typeName: 'A Type'
      }], [{
        id: 3,
        typeName: 'B Type'
      }]] as any);
    });

    it(' if todayTommorow', () => {
      component.display = 'today';
      component.filterInitData();
      expect(filterService.orderBy).not.toHaveBeenCalled();
    });

    it(' if no racing', () => {
      component.racing = undefined;
      component.filterInitData();
      expect(filterService.orderBy).not.toHaveBeenCalled();
    });
  });

  describe('handleFeaturedLoaded', () => {
    it('should set handleFeaturedLoaded prop to true', () => {
      expect(component.featuredLoaded).toBeFalsy();
      component.handleFeaturedLoaded();
      expect(component.featuredLoaded).toBeTruthy();
    });
  });

  describe('#handleFutureTabLoaded', () => {
    it('should set handleFeaturedLoaded prop to true', () => {
      component.handleFeaturedLoaded = jasmine.createSpy();
      component.display = 'future';
      component.racing  = { events:  [{
        name: 'B Type'
      }, {
        name: 'A Type'
      }]} as any;
      component.handleFutureTabLoaded();
      expect(component.handleFeaturedLoaded).toHaveBeenCalled();
    });
    it('should set handleFeaturedLoaded prop to true  no data available', () => {
      component.handleFeaturedLoaded = jasmine.createSpy();
      component.display = 'future';
      component.racing  = { events:  []} as any;
      component.handleFutureTabLoaded();
      expect(component.featuredLoaded).toBeTrue();
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

    it('should return false in case if no error and tab is today', () => {
      component['responseError'] = undefined as any;
      component['display'] = 'today' as any;
      expect(component.displayNextRaces).toBeTruthy();
    });
  });

  describe('handleNextRacesLoaded', () => {
    it('should set nextRacesLoaded property to true', () => {
      component['nextRacesLoaded'] = false;
      component.handleNextRacesLoaded();
      expect(component['nextRacesLoaded']).toBeTruthy();
    });
  });

  it('@reloadComponent should reload component', () => {
    component.reloadComponent();
    expect(component.pubSubService.unsubscribe).toHaveBeenCalledWith('greyhoundsTabsComponent');
    expect(component.pubSubService.subscribe).toHaveBeenCalled();
   });

  describe('#goToFilter', () => {
    beforeEach(() => {
      component.racingPath = 'racingPath';
      component.display = 'display';
    });
    it('should call goToFilter', fakeAsync(() => {
      component.goToFilter('filter');
      tick(100);

      expect(router.navigateByUrl).toHaveBeenCalledWith('url');
      expect(routingHelperService.formSportUrl).toHaveBeenCalledWith('racingPath', 'display/filter');
    }));

    it('should call goToFilter when url equal with router.url', fakeAsync(() => {
      routingHelperService.formSportUrl.and.returnValue(of('url1'));
      component.goToFilter('filter');
      tick(1000);

      expect(router.navigateByUrl).not.toHaveBeenCalled();
      expect(routingHelperService.formSportUrl).toHaveBeenCalledWith('racingPath', 'display/filter');
    }));
    it('should call goToFilter', fakeAsync(() => {
      component.isEventOverlay = true;
      component.goToFilter('filter');
      tick(100);

      expect(gtm.push).toHaveBeenCalled();
    }));
  });

  it('@isTodayTomorrow', () => {
    component.display = 'today';
    expect(component.isTodayTomorrow).toBe(true);

    component.display = 'tomorrow';
    expect(component.isTodayTomorrow).toBe(true);

    component.display = 'lorem';
    expect(component.isTodayTomorrow).toBe(false);
  });
});
