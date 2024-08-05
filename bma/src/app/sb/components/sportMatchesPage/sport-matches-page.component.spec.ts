import { of as observableOf, throwError,BehaviorSubject } from 'rxjs';

import { SportMatchesPageComponent } from '@sb/components/sportMatchesPage/sport-matches-page.component';

describe('SportMatchesPageComponent', () => {
  let component: SportMatchesPageComponent;

  const tabName = 'TestTabName';
  const matchesTabs = {
    sportConfig: {
      tabs: [{ subTabs: { subTabs: [{ onClick: jasmine.createSpy() }] } }]
    },
    config: { tier: 2 }
  };

  let activatedRouteStub;
  let getSportInstanceServiceStub;
  let locationStub;
  let routingStateStub;
  let router;
  let navigationService;
  let windowRefService;
  let competitionFiltersService;
  let cmsService;
  const updateEventService = {} as any;

  beforeEach(() => {
    locationStub = {
      go: jasmine.createSpy(),
      path: () => ''
    };
    routingStateStub = {
      setCurrentUrl: jasmine.createSpy()
    };
    getSportInstanceServiceStub = {
      getSport: jasmine.createSpy('getSport').and.returnValue(observableOf(matchesTabs))
    };
    router = {
      navigateByUrl: jasmine.createSpy()
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
    activatedRouteStub = {
      snapshot: {
        paramMap: { get: jasmine.createSpy() },
        params: { tab: tabName },
        parent: { data: {} },
        _routerState:{ url:'matches'},
        routeConfig: { data: { segment: 'sport' } }
      },
      children: {},
      parent: { snapshot: { url: [{ path: '' }] } },
    };
     navigationService = jasmine.createSpyObj('navigationService', ['emitChangeSource','routingStateService'])
     navigationService.routingStateService.segmentHistory = ['sport.display'];

    cmsService = {
      getSportTabs: jasmine.createSpy('getSportTabs').and.returnValue(observableOf({tabs: []}))
    };

    component = new SportMatchesPageComponent(
        locationStub,
        getSportInstanceServiceStub,
        routingStateStub,
        activatedRouteStub,
        router,
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
    component.SportMatchesTab = {
      ngOnInit: jasmine.createSpy('ngOnInit'),
      ngOnDestroy: jasmine.createSpy('ngOnDestroy')
    };
  });

  describe('ngOnInit', () => {
    describe('should define sportId', () => {
      it('as number 0', () => {
        component.sport = null;
        spyOn(component,'getCurrentTargetTab');
        component.ngOnInit();

        expect(component.sportId).toEqual('0');

        component.sport = {
          readonlyRequestConfig: undefined
        } as any;
        component.ngOnInit();

        expect(component.sportId).toEqual('0');

        component.sport = {
          readonlyRequestConfig: {
            categoryId: undefined
          }
        } as any;
        component.ngOnInit();

        expect(component.sportId).toEqual('0');
      });

      it('from RequestConfig', () => {
        getSportInstanceServiceStub.getSport.and.returnValue(observableOf(
          Object.assign({}, matchesTabs, { readonlyRequestConfig: { categoryId: '333' } })
        ));
        spyOn(component,'getCurrentTargetTab');
        component.ngOnInit();

        expect(component.sportId).toEqual('333');
      });

    });

    describe('#reloadPage', () => {
      it('should reload component', () => {
        component.showSpinner = jasmine.createSpy('showSpinner');
        component.reloadPage();

        expect(component.showSpinner).toHaveBeenCalled();
        expect(component.SportMatchesTab.ngOnInit).toHaveBeenCalled();
        expect(component.SportMatchesTab.ngOnDestroy).toHaveBeenCalled();
      });
    });

    it('should get competition filters', (done: DoneFn) => {
      spyOn(component,'getCurrentTargetTab');
      component.ngOnInit();
      done();
      expect(competitionFiltersService.formLeagueFilters).toHaveBeenCalledWith('matches', []);
      expect(competitionFiltersService.formTimeFilters).toHaveBeenCalledWith('matches', [], []);
      expect(competitionFiltersService.formLeagueFilters).toHaveBeenCalledBefore(competitionFiltersService.formTimeFilters);
      expect(component.competitionFilters).toEqual([]);
    });

    it('should get Sport Event Filters availability', () => {
      spyOn(component,'getCurrentTargetTab');
      component.ngOnInit();

      expect(component.isSportEventFiltersEnabled).toBeFalsy();
      expect(competitionFiltersService.getSportEventFiltersAvailability).toHaveBeenCalled();
    });

    it('should call cms service getSportTabs', () => {
      spyOn(component,'getCurrentTargetTab');
      component.ngOnInit();

      expect(cmsService.getSportTabs).toHaveBeenCalledWith('0');
      expect(component.sportId).toEqual('0');
    });

    describe(`getSport' return error`, () => {
      it(`should hide spinner`, () => {
        getSportInstanceServiceStub.getSport.and.returnValue(throwError('adads'));
        spyOn(component, 'hideSpinner');

        component.ngOnInit();

        expect(component['hideSpinner']).toHaveBeenCalled();
      });
    });
  });

  describe(`getCurrentTargetTab'`, () => {
    it(`shouldcall getCurrentTargetTab`, () => {
      activatedRouteStub.snapshot._routerState.url = 'golf_matches';
      component.changeTabName = {tabs: [{id: 'golf_matches'},{id: 'matches'} ]} as any;
      component.getCurrentTargetTab();

      expect(component.targetTab).toBeDefined();
    });
    
    it(`should call getCurrentTargetTab without tabs`, () => {
      activatedRouteStub.snapshot._routerState.url = 'golf_matches';
      component.getCurrentTargetTab();

      expect(component.targetTab).toBeUndefined();
    });


  });


  describe('handleCompetitionFilterOutput', () => {
    beforeEach(() => {
      component.timeFilter = null;
      component.leagueFilter = null;
    });

    it('should not update filter if no output', () => {
      component.handleCompetitionFilterOutput({} as any);

      expect(component.timeFilter).toBeNull();
      expect(component.leagueFilter).toBeNull();
    });

    it('should update time filter', () => {
      const timeFilter = { id: 1, name: '1h', type: 'TIME', value: 1, active: true } as any;

      component.timeFilter = timeFilter;

      component.handleCompetitionFilterOutput({ output: 'filterChange', value: { ...timeFilter, active: false } });

      expect(component.leagueFilter).toBeNull();
      expect(component.timeFilter).toEqual({ ...timeFilter, active: false });
    });

    it('should update league filter', () => {
      const leagueFilter = { id: 1, name: 'Super League', type: 'LEAGUE', value: [1, 2], active: true } as any;

      component.leagueFilter = leagueFilter;

      component.handleCompetitionFilterOutput({ output: 'filterChange', value: { ...leagueFilter, active: false } });

      expect(component.timeFilter).toBeNull();
      expect(component.leagueFilter).toEqual({ ...leagueFilter, active: false });
    });
  });

  describe('loadSport', () => {
    beforeEach(() => {
      component.sportName = 'sportName';
    });

    it(`should generate new 'olympics' sportPath if path segment is equal 'olympicsSport'`, () => {
      component['route'].snapshot.parent.data['segment'] = 'olympicsSport';

      component['loadSport']();

      expect(component['location'].go).toHaveBeenCalledWith('olympics/sportName');
    });

    it(`should generate new 'sport' sportPath if path segment is Not equal 'olympicsSport'`, () => {
      component['route'].snapshot.parent.data['segment'] = 'someStr';

      component['loadSport']();

      expect(component['location'].go).toHaveBeenCalledWith('sport/sportName');
    });

    it(`should generate 'newURL' with 'tabName' if it is defined`, () => {
      activatedRouteStub.snapshot.routeConfig.data.segment = 'olympicsSport';
      component['loadSport']('today');

      expect(component['location'].go).toHaveBeenCalledWith('sport/sportName/matches/today');
    });

    it(`should generate 'newURL' without 'tabName' if it is Not defined`, () => {
      component['loadSport']();

      expect(component['location'].go).toHaveBeenCalledWith('sport/sportName');
    });

    it(`should Not change path if current path is the same`, () => {
      component['location'].path = () => '/sport/sportName';

      component['loadSport']();

      expect(component['location'].go).not.toHaveBeenCalled();
    });

    it(`should 'setCurrentUrl' if current path is Not the same`, () => {
      component['location'].path = () => '/pathname';

      component['loadSport']();

      expect(component['routingState'].setCurrentUrl).toHaveBeenCalledWith('/pathname');
    });

    it(`should Not 'setCurrentUrl' if current path is the same`, () => {
      component['location'].path = () => '/sport/sportName';

      component['loadSport']();

      expect(component['routingState'].setCurrentUrl).not.toHaveBeenCalled();
    });

    it(`should call loadSport`, () => {
      activatedRouteStub.snapshot._routerState.url = 'golf_matches';
      component['loadSport']('today');

      expect(component['location'].go).toHaveBeenCalledWith('sport/sportName/golf_matches/today');
    });
  });

  describe(`updateLoadStatus`, () => {

    beforeEach(() => {
      navigationService.emitChangeSource = new BehaviorSubject(null);
      windowRefService.nativeWindow.setTimeout.and.callFake(cb => cb && cb());
      spyOn(component, 'hideSpinner');
    });

    it(`should update featuredEventsCount and not update isNotAllModulesLoaded`, () => {
      const output = {
        output: 'featuredEventsCount',
        value: 2
      };
      component.updateLoadStatus(0, output);

      expect(component.featuredEventsCount).toEqual(output.value);
      expect(component.isFeaturedLoaded).toBeTruthy();
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(component['modulesLoadStatus']).toEqual([]);
      expect(component.isNotAllModulesLoaded).toBeTruthy();
      expect(component.hideSpinner).not.toHaveBeenCalled();
    });

    it(`should update isNotAllModulesLoaded, not update featuredEventsCount, not call hideSpinner`, () => {
      const output = {
        output: 'isLoadedEvent',
        value: false
      };
      component.updateLoadStatus(0, output);

      expect(component.featuredEventsCount).toEqual(0);
      expect(component.isFeaturedLoaded).toBeFalsy();
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(component['modulesLoadStatus'][0]).toEqual(output.value);
      expect(component.isNotAllModulesLoaded).toBeTruthy();
      expect(component.hideSpinner).not.toHaveBeenCalled();
    });

    it(`should update isNotAllModulesLoaded and not update featuredEventsCount`, () => {
      const output = {
        output: 'isLoadedEvent',
        value: true
      };
      component.updateLoadStatus(undefined, output);

      expect(component.featuredEventsCount).toEqual(0);
      expect(component.isFeaturedLoaded).toBeTruthy();
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(component['modulesLoadStatus'][0]).toEqual(output.value);
      expect(component.isNotAllModulesLoaded).toBeFalsy();
      expect(component.hideSpinner).toHaveBeenCalled();
    });
    it(`set isFeaturedLoaded true when isloadedevent emit true and i=0`, () => {
      const output = {
        output: 'isLoadedEvent',
        value: true
      };
      component.updateLoadStatus(0, output);
      expect(component.isFeaturedLoaded).toBeTruthy();
    });
    it(`set isFeaturedLoaded false when isloadedevent emit true and i=1`, () => {
      const output = {
        output: 'isLoadedEvent',
        value: true
      };
      component.updateLoadStatus(1, output);
      expect(component.isFeaturedLoaded).toBeFalsy();
    });
    it(`set isFeaturedLoaded false when isloadedevent emit false and i=0`, () => {
      const output = {
        output: 'isLoadedEvent',
        value: false
      };
      component.updateLoadStatus(0, output);
      expect(component.isFeaturedLoaded).toBeFalsy();
      component.updateLoadStatus(1, output);
      expect(component.isFeaturedLoaded).toBeFalsy();
    });
    it(`should emit value to navigationservice`, () => {
      const output = {
        output: 'isLoadedEvent',
        value: true
      };
      component.updateLoadStatus(0, output);
      component.updateLoadStatus(1, output);
      expect(component.featuredEventsCount).toEqual(0);
      expect(component.isFeaturedLoaded).toBeTruthy();
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(component['modulesLoadStatus'][0]).toEqual(output.value);
      expect(component['modulesLoadStatus'][1]).toEqual(output.value);
      expect(component.isNotAllModulesLoaded).toBeFalsy();
      expect(component.hideSpinner).toHaveBeenCalled();
    });
    it(`if loadedMatch is doesnt include "sport.display"`,()=>{
      navigationService.routingStateService.segmentHistory = ['sport.others'];
      const output = {
        output: 'isLoadedEvent',
        value: true
      };
      component.updateLoadStatus(0, output);
      expect(component.isFeaturedLoaded).toBeTruthy();
      activatedRouteStub.snapshot._routerState.url = 'golf_matches';
      component.updateLoadStatus(0, output);
      expect(component.isFeaturedLoaded).toBeTruthy();
    });
  });

  describe(`@ngOnDestroy`, () => {
    it(`unsubscribe sportsConfigSubscription cmsConfigSubscription`, () => {
      component['sportsConfigSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component['cmsConfigSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;

      component.ngOnDestroy();
      expect(component['sportsConfigSubscription'].unsubscribe).toHaveBeenCalled();
      expect(component['cmsConfigSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });

  it('update displayFilters true', () => {
    component.displayFilters = false;
    
    component.updateFiltersDisplay(true);

    expect(component.displayFilters).toBeTrue();
  });

  it('update displayFilters false', () => {
    component.displayFilters = true;
    
    component.updateFiltersDisplay(false);

    expect(component.displayFilters).toBeFalse();
  });
});
