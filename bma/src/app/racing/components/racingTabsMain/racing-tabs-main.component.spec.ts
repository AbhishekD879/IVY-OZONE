import { RacingTabsMainComponent } from '@racing/components/racingTabsMain/racing-tabs-main.component';
import { of, throwError, BehaviorSubject } from 'rxjs';
import { ISportEvent } from '@core/models/sport-event.model';

describe('RacingTabsMainComponent', () => {
  let component: RacingTabsMainComponent;
  let route;
  let router;
  let templateService;
  let timeService;
  let routesDataSharingService;
  let horseRacingService;
  let greyhoundService;
  let sessionStorageService;
  const navigationService = {} as any;
  let routingState;
  const mockEvents = {
    groupedRacing: [
      {
        'flag': 'FR',
        'data': [
          {
            startTime: new Date().getTime() + (11 * 60 * 1000)
          }, {
            startTime: new Date().getTime() + (12 * 60 * 1000)
          }
        ]
      }, {
        'flag': 'ZA',
        'data': [
          {
            startTime: 1593009900000
          }, {
            startTime: 1593012000000
          }
        ]
      }
    ],
    events: [{
      markets: [{
        terms: ''
      }]
    }],
    selectedTab: 'featured'
  } as any;
  const eventMock = { id: 0, markets: [{ outcomes: [] }], racingFormEvent: { raceType: 'race-0' } } as ISportEvent;
  beforeEach(() => {
    route = {
      params: of({ display: 'specials' }),
      snapshot: {
        params: {}
      }
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    templateService = {
      genTerms: jasmine.createSpy('genTerms').and.returnValue('market terms')
    };
    timeService = {
      incrementDateDay: jasmine.createSpy('incrementDateDay').and.returnValue(new Date()),
      getDayI18nValue: jasmine.createSpy('getDayI18nValue').and.returnValue('sb.dayWednesday'),
      getMonthI18nValue: jasmine.createSpy('getMonthI18nValue'),
    };
    routesDataSharingService = {
      getRacingTabs: jasmine.createSpy('getRacingTabs'),
      updatedActiveTabId: jasmine.createSpy('updatedActiveTabId')
    };
    horseRacingService = {
      getConfig: jasmine.createSpy('getConfig').and.returnValue({}),
      getByTab: jasmine.createSpy('getByTab').and.returnValue(Promise.resolve([eventMock])),
      prepareYourCallSpecialsForFeaturedTab: jasmine.createSpy('prepareYourCallSpecialsForFeaturedTab'),
      getYourCallSpecials: jasmine.createSpy('getYourCallSpecials').and.returnValue(Promise.resolve([eventMock])),
      getGeneralConfig: jasmine.createSpy('getGeneralConfig').and.returnValue({
        config: {},
        order: {},
        filters: {}
      }),
      isDisplayAndFilterCorrect: jasmine.createSpy('isDisplayAndFilterCorrect').and.returnValue(false),
      config: {
        request: {
          categoryId: '21',
        }
      },
      sortRaceGroup: jasmine.createSpy('sortRaceGroup').and.returnValue(mockEvents)
    };
    greyhoundService = {
      getConfig: jasmine.createSpy('getConfig').and.returnValue({}),
      config: {
        request: {
          categoryId: '21',
        }
      },
    };
    routingState = {
      getCurrentSegment: jasmine.createSpy('getCurrentSegment').and.returnValue('horseracingSegment')
    };
    sessionStorageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get').and.returnValue(null)
    };
    navigationService.emitChangeSource = new BehaviorSubject(null);
    component = new RacingTabsMainComponent(
      route,
      router,
      templateService,
      timeService,
      routesDataSharingService,
      horseRacingService,
      greyhoundService,
      routingState,
      navigationService,
      sessionStorageService
    );
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component['processDataSuccess'] = jasmine.createSpy('processDataSuccess');
      component['processDataError'] = jasmine.createSpy('processDataError');
    });

    it('#ngOnInit', () => {
      component['concatDataRequests'] = jasmine.createSpy('concatDataRequests').and.returnValue(of([{}, {}]));
      component.ngOnInit();

      expect(component.display).toBe('specials');
      expect(component['processDataSuccess']).toHaveBeenCalledTimes(1);
    });

    it('#ngOnInit set future for display if isEventOverlay', () => {
      component['concatDataRequests'] = jasmine.createSpy('concatDataRequests').and.returnValue(of([{}, {}]));
      component.isEventOverlay = true;
      component.sportName = 'greyhound';
      greyhoundService.getConfig.and.returnValue(null);
      component.ngOnInit();

      expect(component.display).toBe('future');
      expect(component['processDataSuccess']).not.toHaveBeenCalled();
    });

    it('getData throws error', () => {
      route.params = of({ tab: 'featured' });
      const errorStub = 'getData error';
      component['concatDataRequests'] = jasmine.createSpy('concatDataRequests').and.returnValue(throwError(errorStub));

      component.ngOnInit();

      expect(component.display).toBe('featured');
      expect(component['processDataSuccess']).not.toHaveBeenCalled();
      expect(component['processDataError']).toHaveBeenCalledTimes(1);
      expect(component['processDataError']).toHaveBeenCalledWith(errorStub);
    });

    it('should not get data if no config', () => {
      spyOn(component as any, 'concatDataRequests');

      horseRacingService.getConfig.and.returnValue(null);
      component.ngOnInit();

      expect(horseRacingService.getConfig).toHaveBeenCalled();
      expect(component.applyingParams).not.toBeTruthy();
      expect(component['concatDataRequests']).not.toHaveBeenCalled();
    });

    it('should sort races if the racingName is horse racing', () => {
      route = {
        params: of({ display: 'featured' }),
        snapshot: {
          params: {}
        }
      } as any;

      horseRacingService = {
        getConfig: jasmine.createSpy('getConfig').and.returnValue({ name: 'horseracing', path: '' }),
        getByTab: jasmine.createSpy('getByTab').and.returnValue(Promise.resolve(mockEvents)),
        prepareYourCallSpecialsForFeaturedTab: jasmine.createSpy('prepareYourCallSpecialsForFeaturedTab').and.returnValue({}),
        getYourCallSpecials: jasmine.createSpy('getYourCallSpecials').and.returnValue(Promise.resolve({})),
        getGeneralConfig: jasmine.createSpy('getGeneralConfig').and.returnValue({
          config: {},
          order: {},
          filters: {}
        }),
        addFirstActiveEventProp: jasmine.createSpy('addFirstActiveEventProp'),
        isDisplayAndFilterCorrect: jasmine.createSpy('isDisplayAndFilterCorrect').and.returnValue(true),
        config: {
          request: {
            categoryId: '21',
          }
        },
        sortRaceGroup: jasmine.createSpy('sortRaceGroup').and.returnValue(mockEvents)
      };
      sessionStorageService = {
        set: jasmine.createSpy('set')
      };
      component = new RacingTabsMainComponent(
        route,
        router,
        templateService,
        timeService,
        routesDataSharingService,
        horseRacingService,
        greyhoundService,
        routingState,
        navigationService,
        sessionStorageService
      );
      component.ngOnInit();
      expect(component.racing).not.toBeNull();
    });

    it('should not sort races if the racing is not horse racing', () => {
      route = {
        params: of({ display: 'future' }),
        snapshot: {
          params: {}
        }
      } as any;

      horseRacingService = {
        getConfig: jasmine.createSpy('getConfig').and.returnValue({ name: 'horseracing', path: '' }),
        getByTab: jasmine.createSpy('getByTab').and.returnValue(Promise.resolve(mockEvents)),
        prepareYourCallSpecialsForFeaturedTab: jasmine.createSpy('prepareYourCallSpecialsForFeaturedTab').and.returnValue({}),
        getYourCallSpecials: jasmine.createSpy('getYourCallSpecials').and.returnValue(Promise.resolve({})),
        getGeneralConfig: jasmine.createSpy('getGeneralConfig').and.returnValue({
          config: {},
          order: {},
          filters: {}
        }),
        addFirstActiveEventProp: jasmine.createSpy('addFirstActiveEventProp'),
        isDisplayAndFilterCorrect: jasmine.createSpy('isDisplayAndFilterCorrect').and.returnValue(true),
        config: {
          request: {
            categoryId: '19',
          }
        },
        sortRaceGroup: jasmine.createSpy('sortRaceGroup').and.returnValue(mockEvents)
      };
      sessionStorageService = {
        set: jasmine.createSpy('set')
      };
      component = new RacingTabsMainComponent(
        route,
        router,
        templateService,
        timeService,
        routesDataSharingService,
        horseRacingService,
        greyhoundService,
        routingState,
        navigationService,
        sessionStorageService
      );
      component.ngOnInit();
      expect(horseRacingService.sortRaceGroup).not.toHaveBeenCalled();
    });
    it('should set display values as today', () => {
      component['route'].params = of({display: null, tab: null});
      component['routingState'].getCurrentSegment = jasmine.createSpy('getCurrentSegment').and.returnValue('greyhound');
      greyhoundService.config = {
        request: {
          categoryId: '21',
        }
      };
      component.ngOnInit();
      expect(component.display).toBe('today');
    });
    it('should set display values as featured', () => {
      component['route'].params = of({display: null, tab: null});
      component['routingState'].getCurrentSegment = jasmine.createSpy('getCurrentSegment').and.returnValue('horseracing');
      horseRacingService.config = {
        request: {
          categoryId: '21',
        }
      };
      component.ngOnInit();
      expect(component.display).toBe('featured');
    });
    it('should set display values as future', () => {
      component['route'].params = of({display: null, tab: null});
      component['routingState'].getCurrentSegment = jasmine.createSpy('getCurrentSegment').and.returnValue('greyhound');
      greyhoundService.config = {
        request: {
          categoryId: '19',
        }
      };
      component.isEventOverlay = true;
      component.sportName = 'greyhound';
      component['getData'] = jasmine.createSpy('getData');
      component.ngOnInit();
      expect(component.display).toBe('future');
    });
  });

  it('#ngOnDestroy should unsubscribe from route on destroy', () => {
    component['getDataSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;

    component['routeSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;

    component.ngOnDestroy();

    expect(component['getDataSubscription'].unsubscribe).toHaveBeenCalled();
    expect(component['routeSubscription'].unsubscribe).toHaveBeenCalled();
  });

  it('getData for featured', () => {
    component.display = 'featured';
    const result = component['concatDataRequests'](horseRacingService);
    result.subscribe(([events, yourCallEvents]) => {
      expect(events).toEqual([eventMock]);
      expect(yourCallEvents).toEqual([eventMock]);
    });
  });
  it('getData for not featured', () => {
    component.display = 'not-featured';
    const result = component['concatDataRequests'](horseRacingService);
    result.subscribe(([events, yourCallEvents]) => {
      expect(events).toEqual([eventMock]);
      expect(yourCallEvents).toEqual([]);
    });
  });

  describe('applyParams', () => {
    it(`should set route's filter to filter if that is defined`, () => {
      const filterStub = 'filter stub';
      component['route'].snapshot.params['display'] = undefined;
      component['route'].snapshot.params['filter'] = filterStub;

      component['applyParams']();

      expect(component['filter']).toEqual(filterStub);
    });

    it(`should set 'by-meeting' to filter if null returned from sessionStorage `, () => {
      component.isEventOverlay = true;
      component.display = 'future';
      component['applyParams']();

      expect(component['filter']).toEqual('by-meeting');
      expect(sessionStorageService.set).toHaveBeenCalled();
    });

    it(`should set 'by-meeting' to filter if route's filter is undefined`, () => {
      component['route'].snapshot.params['display'] = undefined;
      component['route'].snapshot.params['filter'] = undefined;

      component['applyParams']();

      expect(component['filter']).toEqual('by-meeting');
    });
  });

  describe(`updateLoadStatus`, () => {
    beforeEach(() => {
      navigationService.emitChangeSource = new BehaviorSubject(null);
      spyOn(component, 'hideSpinner');
    });
    it(`should update status when output is true`, () => {
      const output = true;
      component.updateLoadStatus(output);
      expect(component.hideSpinner).toHaveBeenCalled();
    });
    it(`should not update status when output is false`, () => {
      const output = false;
      component.updateLoadStatus(output);
      expect(component.hideSpinner).not.toHaveBeenCalled();
    });
  });

  it('processDataError should show error', () => {
    spyOn(console, 'warn');
    component.showError = jasmine.createSpy('showError');

    component['processDataError']('customError');

    expect(component.showError).toHaveBeenCalled();
    expect(console.warn).toHaveBeenCalledWith('customError');
    expect(component.state.error).toBeTruthy();
    expect(component.applyingParams).toBeFalsy();
  });

  it('processDataSuccess', () => {
    const events: any = {};
    const specials = [];

    component['processDataSuccess']([events, specials]);

    expect(horseRacingService.prepareYourCallSpecialsForFeaturedTab).toHaveBeenCalledWith(specials);
    expect(component.eventsData).toBe(events);
    expect(component.applyingParams).toBeFalsy();
    expect(component.responseError).toBeFalsy();
  });

  it('should navigate to specific path when called goto function', () => {
    component.goTo('path');
    expect(router.navigateByUrl).toHaveBeenCalled();
  });

  describe('check isFavorite', () => {
    it('should satisfy 1st condition and return true', () => {
      const outcomeEntity = {
        outcomeMeaningMinorCode: 2
      } as any;
      const response = component.isFavourite(outcomeEntity);
      expect(response).toBe(true);
    });
    it('should satisfy 2st condition and return true', () => {
      const outcomeEntity = {
        outcomeMeaningMinorCode: -1,
        name: 'unnamed favourite'
      } as any;
      const response = component.isFavourite(outcomeEntity);
      expect(response).toBe(true);
    });
    it('should satisfy 3st condition and return true', () => {
      const outcomeEntity = {
        outcomeMeaningMinorCode: -1,
        name: 'unnamed 2nd favourite'
      } as any;
      const response = component.isFavourite(outcomeEntity);
      expect(response).toBe(true);
    });
    it('should not satisfy condition and return false', () => {
      const outcomeEntity = {
        outcomeMeaningMinorCode: -2,
        name: 'unnamed 3rd favourite'
      } as any;
      const response = component.isFavourite(outcomeEntity);
      expect(response).toBe(false);
    });
  });
});
