import { RacingTabsMainComponent } from '@racingModule/components/racingTabsMain/racing-tabs-main.component';
import { Subject } from 'rxjs';
import { ISportEvent } from '@core/models/sport-event.model';

describe('LMRacingTabsMainComponent', () => {
  let component: RacingTabsMainComponent;
  let route;
  let router;
  let templateService;
  let timeService;
  let routesDataSharingService;
  let horseRacingService;
  let greyhoundService;
  const navigationService = {} as any;
  let routingState, sessionStorageService;
  const routeParams = new Subject();
  const eventMock = { id: 0, markets: [{ outcomes: [] }], racingFormEvent: { raceType: 'race-0' } } as ISportEvent;

  beforeEach(() => {
    route = {
      params: routeParams,
      snapshot: {
        params: {}
      }
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    templateService = {};
    timeService = {
      incrementDateDay: jasmine.createSpy('incrementDateDay').and.returnValue(new Date()),
      getDayI18nValue: jasmine.createSpy('getDayI18nValue'),
      getMonthI18nValue: jasmine.createSpy('getMonthI18nValue'),
    };
    routesDataSharingService = {
      getRacingTabs: jasmine.createSpy('getRacingTabs'),
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
      isDisplayAndFilterCorrect: jasmine.createSpy('isDisplayAndFilterCorrect'),
    };
    greyhoundService = {};
    routingState = {
      getCurrentSegment: jasmine.createSpy('getCurrentSegment').and.returnValue('horseracingSegment')
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

    component['getDataSubscription'] = {
      unsubscribe: jasmine.createSpy()
    } as any;
  });

  it('#ngOnInit', () => {
    expect(component).toBeDefined();
  });

  it('getData', () => {
    const result = component['concatDataRequests'](horseRacingService);
    result.subscribe(([events, yourCallEvents]) => {
      expect(events).toEqual([eventMock]);
      expect(yourCallEvents).toEqual([]);
    });
  });
});
