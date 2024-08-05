import { of as observableOf, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { DesktopSportMatchesPageComponent } from './sport-matches-page.component';
import { SportMatchesPageComponent } from '@sb/components/sportMatchesPage/sport-matches-page.component';

describe('LadbrokesDesktopSportMatchesPageComponent', () => {
  let component: DesktopSportMatchesPageComponent;

  const tabName = 'TestTabName';
  const locationStub = {
    go: () => {},
    path: () => {},
  } as any;
  const routingStateStub = {
    setCurrentUrl: jasmine.createSpy()
  } as any;
  const routerStub = {
    events: { pipe: jasmine.createSpy().and.returnValue(observableOf(null)) }
  } as any;
  const matchesTabs = {
    sportConfig: {
      tabs: [{ subTabs: { subTabs: [{ onClick: jasmine.createSpy() }] } }]
    },
    config: {
      tier: 2,
      request: {
        categoryId: '16'
      }
    }
  };

  let getSportInstanceServiceStub;
  let activatedRouteStub;
  let windowRefService;
  let competitionFiltersService;
  let cmsService;
  const navigationService = {} as any;
  const updateEventService = {} as any;

  beforeEach(() => {
    getSportInstanceServiceStub = {
      getSport: () => observableOf(matchesTabs)
    };
    activatedRouteStub = {
      snapshot: {
        paramMap: { get: () => '' },
        params: { tab: tabName },
        parent: { data: {} },
        _routerState:{ url:'matches'},
        routeConfig: { data: { segment: 'sport' } }
      },
      children: {},
      parent: { snapshot: { url: [{ path: '' }] } },
    };
    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout')
      }
    };
    competitionFiltersService = {
      formTimeFilters: jasmine.createSpy('formTimeFilters').and.returnValue([]),
      formLeagueFilters: jasmine.createSpy('formLeagueFilters').and.returnValue([]),
      getSportEventFiltersAvailability: jasmine.createSpy('getSportEventFiltersAvailability').and.returnValue(observableOf(false))
    };
    cmsService = {
      getSportTabs: jasmine.createSpy('getSportTabs').and.returnValue(observableOf({tabs: []}))
    };

    component = new DesktopSportMatchesPageComponent(
      locationStub,
      getSportInstanceServiceStub,
      routingStateStub,
      activatedRouteStub,
      routerStub,
      navigationService,
      windowRefService,
      competitionFiltersService,
      updateEventService,
      cmsService);

    component['featuredModuleRef'] = {
      destroy: jasmine.createSpy()
    } as any;
    component['featuredModuleView'] = {
      parentInjector: {},
      createComponent: jasmine.createSpy().and.returnValue({
        instance: {
          sportId: 0,
          sportName: 'sportName'
        },
        destroy: jasmine.createSpy()
      })
    } as any;
  });

  describe('ngOnInit', () => {
    it(`should set 'sportName'`, () => {
      spyOn(component['route'].snapshot.paramMap, 'get').and.returnValue('Name1');

      component.ngOnInit();

      expect(component.sportName).toBe('Name1');
    });

    it(`'isFootball' should be Falthy if 'sportName' is Not 'football'`, () => {
      spyOn(component['route'].snapshot.paramMap, 'get').and.returnValue('Name1');

      component.ngOnInit();

      expect(component.isFootball).toBeFalsy();
    });

    it(`'isFootball' should be Truthy if 'sportName' is 'football'`, () => {
      spyOn(component['route'].snapshot.paramMap, 'get').and.returnValue('football');

      component.ngOnInit();

      expect(component.isFootball).toBeTruthy();
    });

    it(`should set 'tab' if activatedRoute has children`, () => {
      spyOn(component['route'], 'children' as any).and.returnValue([1] as any);
      spyOn(component['route'].snapshot.paramMap, 'get').and.returnValue('tabStub' as any);

      component.ngOnInit();

      expect(component.tab).toBeDefined();
    });

    it(`should Not set 'tab' if activatedRoute has Not children`, () => {
      spyOn(component, 'loadSport');
      component['route'] = {
        snapshot: {
          paramMap: { get: () => '' },
          params: { tab: tabName },
          parent: { data: {} }
        },
        children: undefined,
      } as any;

      component.ngOnInit();

      expect(component['route'].children).toBeUndefined();
      expect(component.tab).toBeUndefined();
    });

    it(`should show spinner`, () => {
      spyOn(component, 'showSpinner');

      component.ngOnInit();

      expect(component['showSpinner']).toHaveBeenCalled();
    });

    it(`should set 'sport'`, () => {
      component.sport = null;

      component.ngOnInit();

      expect(component.sport).toBeDefined();
    });

    it(`should set matchesTabs, switchers, indexPage`, () => {
      component.switchers = undefined;
      component.indexPage = undefined;

      component.ngOnInit();

      expect(component.switchers).toBeDefined();
      expect(component.indexPage).toBeDefined();
    });

    it(`should loadSport`, () => {
      spyOn(component as any, 'initializeSwitchers').and.returnValue([{ name: 'Name1' }]);
      component.indexPage = 0;


      component.ngOnInit();

      expect(component.tab).toEqual('Name1');
    });

    it(`should run addLocationChangeHandler`, () => {
      spyOn(component as any, 'addLocationChangeHandler');

      component.ngOnInit();

      expect(component['addLocationChangeHandler']).toHaveBeenCalled();
    });

    it(`should hide spinner`, () => {
      spyOn(component, 'hideSpinner');

      component.ngOnInit();

      expect(component['hideSpinner']).toHaveBeenCalled();
    });

    describe(`getSport' return error`, () => {
      beforeEach(() => {
        component.switchers = [];
      });

      it(`should hide spinner`, () => {
        spyOn(component['sportsConfigService'], 'getSport').and.returnValue(throwError('adads'));
        spyOn(component, 'hideSpinner');

        component.ngOnInit();

        expect(component['hideSpinner']).toHaveBeenCalled();
      });
    });


    it('should get competition filters3', (done: DoneFn) => {
      component.ngOnInit();
      done();
      expect(competitionFiltersService.formLeagueFilters).toHaveBeenCalledWith('matches', []);
      expect(competitionFiltersService.formTimeFilters).toHaveBeenCalledWith('matches', [], []);
      expect(competitionFiltersService.formLeagueFilters).toHaveBeenCalledBefore(competitionFiltersService.formTimeFilters);
      expect(component.competitionFilters).toEqual([]);
    });

    it('should get Sport Event Filters availability', () => {
      component.ngOnInit();

      expect(component.isSportEventFiltersEnabled).toBeFalsy();
      expect(competitionFiltersService.getSportEventFiltersAvailability).toHaveBeenCalled();
    });

    it('should call cms service getSportTabs', () => {
      component.ngOnInit();

      expect(cmsService.getSportTabs).toHaveBeenCalledWith('0');
      expect(component.categoryId).toEqual('16');
      expect(component.sportId).toEqual('0');
    });

    it('should call if case', fakeAsync(() => {
      component.ngOnInit();
      tick();
      component['selectTab'] = jasmine.createSpy();
      activatedRouteStub.snapshot.params.tab = 'allEvents';
      component.sportId ='18';
      component['addLocationChangeHandler']();
      expect(component['selectTab']).toHaveBeenCalledWith('allEvents');
    }));
  });

  describe('ngOnDestroy', () => {
    it(`should unsubscribe from 'locationChangeListener', 'sportsConfigSubscription', 'cmsConfigSubscription' if subscription`, () => {
      component.locationChangeListener = jasmine.createSpyObj(['unsubscribe']);
      component['sportsConfigSubscription'] = jasmine.createSpyObj(['unsubscribe']);
      component['cmsConfigSubscription'] = jasmine.createSpyObj(['unsubscribe']);

      component.ngOnDestroy();

      expect(component.locationChangeListener.unsubscribe).toHaveBeenCalled();
      expect(component['sportsConfigSubscription'].unsubscribe).toHaveBeenCalled();
      expect(component['cmsConfigSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });

  describe('loadSport', () => {
    const sportName = 'football';

    it(`should set component 'tab'`, () => {
      component['loadSport'](sportName);

      expect(component.tab).toEqual(sportName);
    });

    it(`should run super loadSport method`, () => {
      spyOn(SportMatchesPageComponent.prototype as any, 'loadSport');

      component['loadSport'](sportName);

      expect(SportMatchesPageComponent.prototype['loadSport']).toHaveBeenCalledWith(sportName);
    });
  });

  describe('@addLocationChangeHandler', () => {
    it('should select active tab if location was changed', fakeAsync(() => {
      component.ngOnInit();
      tick();
      component['selectTab'] = jasmine.createSpy();
      component['addLocationChangeHandler']();
      expect(component['selectTab']).toHaveBeenCalledWith(tabName);
    }));

    it('should NOT select active tab if location was changed when tab is already active', () => {
      component['selectTab'] = jasmine.createSpy();
      component.tab = tabName;
      component['addLocationChangeHandler']();
      expect(component['selectTab']).toHaveBeenCalledTimes(1);
    });
  });

  describe('selectTab', () => {
    beforeEach(() => {
      spyOn(component as any, 'getTabIndex').and.returnValue(1);
      spyOn(component as any, 'loadSport');
    });

    it('should set indexPage', () => {
      component['selectTab']('Name');

      expect(component.indexPage).toBe(1);
    });

    it('should load sport if switchers has it', () => {
      component.switchers = [{ name: 'text' }, { name: 'switcherName' }] as any;

      component['selectTab']('Name');

      expect(component['loadSport']).toHaveBeenCalledWith(component.switchers[1].name);
    });

    it('should Not load sport if switchers is Not defined', () => {
      component['selectTab']('Name');

      expect(component['loadSport']).not.toHaveBeenCalled();
    });

    it('should Not load sport if switchers do Not has item by index', () => {
      component.switchers = [{ name: 'text' }] as any;

      component['selectTab']('Name');

      expect(component['loadSport']).not.toHaveBeenCalled();
    });

    it('should Not load sport if selected switcher do Not has name', () => {
      component.switchers = [{ id: 1 }, { id: 2 }] as any;

      component['selectTab']('Name');

      expect(component['loadSport']).not.toHaveBeenCalled();
    });
  });

  describe('getTabIndex', () => {
    beforeEach(() => {
      component.switchers = [{ name: 'Name1' }, { name: 'Name2' }] as any;
    });

    it(`should find index of switcher`, () => {
      expect(component['getTabIndex']('Name2')).toBe(1);
    });

    it(`should return 0 if can Not find index of switcher`, () => {
      expect(component['getTabIndex']('Name3')).toBe(0);
    });
  });

  describe('#initializeSwitchers', () => {
    it('should return switchers', () => {
      const result = component['initializeSwitchers']('football');

      expect(result).toEqual([
        {
          id: 'tab-today',
          name: 'today',
          label: 'Today',
          url: `/sport/football/matches/today`,
          hidden: false,
          onClick: jasmine.any(Function)
        },
        {
          id: 'tab-tomorrow',
          name: 'tomorrow',
          label: 'Tomorrow',
          url: `/sport/football/matches/tomorrow`,
          hidden: false,
          onClick: jasmine.any(Function)
        },
        {
          id: 'tab-future',
          name: 'future',
          label: 'Future',
          url: `/sport/football/matches/future`,
          hidden: false,
          onClick: jasmine.any(Function)
        }
      ]);
    });
  });
});
