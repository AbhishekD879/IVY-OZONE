import { of as observableOf, throwError,BehaviorSubject } from 'rxjs';
import { SportTabsPageComponent } from '@sb/components/sportTabsPage/sport-tabs-page.component';
import { fakeAsync, tick } from '@angular/core/testing';

describe('AppSportTabsPageComponent', () => {
  let component: SportTabsPageComponent;

  let
    activatedRoute,
    getSportInstanceService,
    tier = 1,
    router,
    slpSpinnerStateService,
    navigationService,
    changeDetectorRef,
    windowRefService,
    cmsService;
  const updateService = {} as any;

  const urlObj = {
    path: 'olympics'
  };

  beforeEach(() => {
    activatedRoute = {
      snapshot: {
        paramMap: {
          get: jasmine.createSpy().and.returnValue('boxing')
        },
        url: [urlObj]
      },
      params: observableOf({ display: 'foo1' })
    } as any;
    getSportInstanceService = {
      getSport: jasmine.createSpy('getSport').and.callFake(() => observableOf(({
        readonlyRequestConfig: {
          categoryId: '129'
        },
        config: {
          tier: tier
        },
        sportConfig: {
          config: {
            request: {
              aggregatedMarkets1: []
            }
          }
        }
      } as any)))
    } as any;
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    } as any;
    slpSpinnerStateService = {
      handleSpinnerState: jasmine.createSpy('handleSpinnerState')
    } as any;
    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake((fn) => { fn(); })
      }
    } as any;
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    navigationService = jasmine.createSpyObj('navigationService', ['emitChangeSource']);
    navigationService.emitChangeSource = new BehaviorSubject(null);

    cmsService = {
      getSportTabs: jasmine.createSpy('getSportTabs').and.returnValue(observableOf({tabs: []}))
    };

    component = new SportTabsPageComponent(activatedRoute, getSportInstanceService,
      router, slpSpinnerStateService, windowRefService, navigationService, changeDetectorRef, updateService, cmsService);
    component.displayTab = {
      name: 'matches'
    } as any;
    spyOn(component, 'showSpinner');
    spyOn(component, 'hideSpinner');
    component.ngOnInit();
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  describe('@ngOnInit', () => {
    beforeEach(() => {
      component.ngOnInit();
    });

    it(`LAZY_COMPONENTS should be defined`, () => {
      expect(component['LAZY_COMPONENTS']).toEqual(['live', 'competitions']);
    });
    it(`should navigate if display is neither live nor competitions`, () => {
      component.displayTab.name = 'test';
      component.ngOnInit();
      navigationService.emitChangeSource.next = new BehaviorSubject(true);
    });
    it(`should not navigate if display is live`, () => {
      component.displayTab.name = 'live';
      component.ngOnInit();
      navigationService.emitChangeSource.next = new BehaviorSubject(null);
    });
    it(`should not navigate if display is null`, () => {
      component.displayTab.name = 'null';
      component.ngOnInit();
      navigationService.emitChangeSource.next = new BehaviorSubject(null);
    });
    it(`should not navigate if display is competitions`, () => {
      component.displayTab.name = 'competitions';
      component.ngOnInit();
      navigationService.emitChangeSource.next = new BehaviorSubject(null);
    });
    it(`should define isLazyComponentLoading`, () => {
      component.isLazyComponentLoading = undefined;
      component.displayTab.name = 'live';

      component.ngOnInit();

      expect(component.isLazyComponentLoading).toBeTruthy();
    });

    it('should get sport and display params from route', () => {
      expect(activatedRoute.snapshot.paramMap.get).toHaveBeenCalledWith('sport');
      expect(activatedRoute.snapshot.paramMap.get).toHaveBeenCalledTimes(2);
    });

    it('should subscribe on params and update if changed', () => {
      activatedRoute.params.subscribe(() => {
        expect(component.display).toBe('matches');
      });
    });

    it('should init spinner', () => {
      expect(component.showSpinner).toHaveBeenCalled();
    });

    it('error case', () => {
      component['showError'] = jasmine.createSpy();
      getSportInstanceService.getSport = jasmine.createSpy().and.returnValue(throwError('error'));
      component.ngOnInit();
      expect(component['showError']).toHaveBeenCalled();
    });

    it('get and assign sport service instance, hide spinner, reloadinitiated false', () => {
      component.reloadInitiated = false;
      expect(getSportInstanceService.getSport).toHaveBeenCalledWith('boxing');
      component.ngOnInit();
      getSportInstanceService.getSport('boxing').subscribe(() => {
        expect(changeDetectorRef.detectChanges).not.toHaveBeenCalled();
        expect(component.hideSpinner).toHaveBeenCalled();
      });
    });
    it('get and assign sport service instance, hide spinner, reloadinitiated true', () => {
      component.reloadInitiated = true;
      expect(getSportInstanceService.getSport).toHaveBeenCalledWith('boxing');
      component.ngOnInit();
      getSportInstanceService.getSport('boxing').subscribe(() => {
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
        expect(component.hideSpinner).toHaveBeenCalled();
      });
    });

    it('should call cms service getSportTabs', () => {
      component.ngOnInit();

      expect(cmsService.getSportTabs).toHaveBeenCalledWith('129');
      expect(component.sportId).toEqual('129');
      expect(component.isTierOneOrTwoSport).toEqual(true);
    });
  });

  describe('ngOnInit', () => {
    describe('checkDisplayingLazyComponent', () => {
      beforeEach(() => {
        spyOn(component as any, 'checkDisplayingLazyComponent');
      });

      it(`should checkDisplayingLazyComponent`, () => {
        component.ngOnInit();

        expect(<any>component['checkDisplayingLazyComponent']).toHaveBeenCalledTimes(1);
      });


      it(`should checkDisplayingLazyComponent if change route`, () => {
        component['displayTab'] = undefined;
        component.display = 'live';

        component.ngOnInit();

        expect(<any>component['checkDisplayingLazyComponent']).toHaveBeenCalledTimes(2);
      });

      it('should checkDisplayingLazyComponent once if display params match', () => {
        component['displayTab'] = undefined;
        activatedRoute.snapshot.paramMap.get = jasmine.createSpy('paramMap.get').and.returnValue('foo1');

        component.ngOnInit();

        expect(<any>component['checkDisplayingLazyComponent']).toHaveBeenCalledTimes(1);
      });
    });
  });

  describe('ngOnchanges', () => {
    it('should set displayTab', () => {
      const changes: any = {
        displayTab: {
          currentValue: {name: 'coupons'}
        }
      };
      component.ngOnChanges(changes);
      expect(component.displayTab.name).toBe('coupons');
    });
  });

  it('should unsubscribe from route OnDestroy', () => {
    component['routeChangeListener'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component.ngOnDestroy();

    expect(component['routeChangeListener'].unsubscribe).toHaveBeenCalled();
  });

  describe('@isFootball should return active tab name', () => {
    it('', () => {
      component.sportName = 'football';

      expect(component.showSportTab('coupons', true)).toBe('coupons');
    });

    it('', () => {
      expect(component.showSportTab('coupons', false)).toBe('coupons');
    });

    it('', () => {
      expect(component.showSportTab('coupons', true)).toBe('');
    });
  });

  it('should create component and init properties', fakeAsync(() => {
    tick();
    expect(component).toBeTruthy();
    expect(component.sportName).toEqual('boxing');
    expect(component.display).toEqual('matches');
    expect(component.isTierOneOrTwoSport).toEqual(true);
    expect(component.sportId).toEqual('129' as any);
  }));

  it('should set proper isTierOneOrTwoSport for tier 2 sports', fakeAsync(() => {
    tier = 2;
    component.ngOnInit();
    tick();
    expect(component.isTierOneOrTwoSport).toEqual(true);
  }));

  it('should set proper isTierOneOrTwoSport for tier 3 sports', fakeAsync(() => {
    tier = 3;
    component.ngOnInit();
    tick();
    expect(component.isTierOneOrTwoSport).toEqual(false);
  }));

  describe('navigateToSportLandingPage', () => {
    it('shouldn`t navigate other URL for tier 1 and two', () => {
      component.isTierOneOrTwoSport = true;
      router.navigateByUrl = jasmine.createSpy();
      component['navigateToSportLandingPage']();
      expect(router.navigateByUrl).not.toHaveBeenCalled();
    });
    it('should navigate to proper URL for non olympics', () => {
      urlObj.path = 'sport';
      component.isTierOneOrTwoSport = false;
      router.navigateByUrl = jasmine.createSpy('navigateByUrl');
      component['navigateToSportLandingPage']();
      expect(router.navigateByUrl).toHaveBeenCalledWith('sport/boxing');
    });
    it('should navigate to proper URL for olympics', () => {
      urlObj.path = 'olympics';
      component.isTierOneOrTwoSport = false;
      router.navigateByUrl = jasmine.createSpy('navigateByUrl');
      component['navigateToSportLandingPage']();
      expect(router.navigateByUrl).toHaveBeenCalledWith('olympics/boxing');
    });
  });

  describe('#featuredSpinnerStatus', () => {
    it('should control featured spinner when loaded', () => {
      const status = {
        value: false
      };

      component.featuredSpinnerStatus(status);

      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(component['featuredSpinner']).toEqual(false);
    });

    it('should control featured spinner when loading', () => {
      const status = {
        value: true
      };

      component.featuredSpinnerStatus(status);

      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(component['featuredSpinner']).toEqual(true);
    });
  });

  describe(`updateLoadStatus`, () => {
    it(`should update status when output is isLoadedEvent and value is true`, () => {
      const output = { output: 'isLoadedEvent', value: true };
      component.updateLoadStatus(output);
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(component.hideSpinner).toHaveBeenCalled();
    });

    it(`should not update status when output is isLoadedEvent and value is false`, () => {
      const output = { output: 'isLoadedEvent', value: false };
      component.updateLoadStatus(output);
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
    });
    it(`should not update status when output is not isLoadedEvent and value is true`, () => {
      const output = { output: 'someEvent', value: true };
      component.updateLoadStatus(output);
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
    });
    it(`should not update status when output is not isLoadedEvent and value is false`, () => {
      const output = { output: 'someEvent', value: false };
      component.updateLoadStatus(output);
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
    });
  });

  describe('#receiveSpinnerStatus', () => {
    it('should control matches spinner when loaded', () => {
      const status = true;

      component.receiveSpinnerStatus(status);

      expect(component['isLoaded']).toEqual(true);
    });

    it('should control matches spinner when loading', () => {
      const status = false;

      component.receiveSpinnerStatus(status);

      expect(component['isLoaded']).toEqual(false);
    });
  });

  describe('#hideMatches', () => {
    it('should set true "showMatchesSection" if matches has events', () => {
      const isEvents = true;
      component.hideMatches(isEvents);

      expect(component['showMatchesSection']).toEqual(true);
    });

    it('should set false "showMatchesSection" if matches has no events', () => {
      const isEvents = false;
      component.hideMatches(isEvents);

      expect(component['showMatchesSection']).toEqual(false);
    });
  });

  describe('#handleMatchesLoadingStatus', () => {
    it('should control matches and featured spinner when loaded', () => {
      component.receiveSpinnerStatus(true);
      component.featuredSpinnerStatus({ value: true });
      component['handleMatchesLoadingStatus']();

      expect(slpSpinnerStateService.handleSpinnerState).toHaveBeenCalled();
    });

    it('should control matches , outrights, and featured spinner when loaded', () => {
      component.display = 'outrights';
      component.featuredSpinnerStatus({ value: true });
      component['handleMatchesLoadingStatus']();

      expect(slpSpinnerStateService.handleSpinnerState).toHaveBeenCalled();
    });
  });

  describe('checkDisplayingLazyComponent', () => {
    describe('isLazyComponentLoading should be Truthy if display equal', () => {
      afterEach(() => {
        expect(component.isLazyComponentLoading).toBeTruthy();
      });
      it(`isLazyComponentLoading should be true if display equal 'live'`, () => {
        component.display = 'live';
        component['checkDisplayingLazyComponent']();
      });

      it(`isLazyComponentLoading should be true if display equal 'competitions'`, () => {
        component.display = 'competitions';
        component['checkDisplayingLazyComponent']();
      });
    });

    it(`isLazyComponentLoading should be Falthy if display not equal Lazy component`, () => {
      component.display = 'matches';
      component['checkDisplayingLazyComponent']();

      expect(component.isLazyComponentLoading).toBeFalsy();
    });
  });

  describe('initLazyHandler', () => {
    it(`should set isLazyComponentLoading  as Falsy`, () => {
      component.isLazyComponentLoading = true;

      component.initLazyHandler();

      expect(component.isLazyComponentLoading).toBeFalsy();
    });
    it(`should emit true when display is live`, () => {
      component.isLazyComponentLoading = true;
      component.display = 'live';
      component.initLazyHandler();
      navigationService.emitChangeSource.next = new BehaviorSubject(true);
      expect(component.isLazyComponentLoading).toBeFalsy();
    });
  });
});
