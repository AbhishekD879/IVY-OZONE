import { LadbrokesBetHistoryPageComponent } from '@ladbrokesMobile/betHistory/components/betHistoryPage/bet-history-page.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { of } from 'rxjs';

describe('LadbrokesBetHistoryPageComponent', () => {
  let component: LadbrokesBetHistoryPageComponent;

  let pubSubService, liveServConnectionService,
    userService, timeService, betsLazyLoadingService, localeService, datepickerValidatorService,
    maintenanceService, resolveService, sessionService, route, betHistoryMainService, dynamicComponentsService,
    cmsService, windowRef, casinoMyBetsIntegratedService: any, vanillaApiService;

  beforeEach(() => {
    liveServConnectionService = {
      connect: jasmine.createSpy('connect').and.returnValue(of({}))
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(of({
        Connect: {
          inShopBets: true
        }
      }))
    } as any;

    userService = {};

    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('2019-04-26 00:00:00')
    } as any;

    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('Lorem')
    } as any;

    datepickerValidatorService = {
      getDefaultErrorsState: jasmine.createSpy('getDefaultErrorsState').and.returnValue(false),
      isDatePickerError: jasmine.createSpy('isDatePickerError').and.returnValue(false),
      updateErrorsState: jasmine.createSpy('updateErrorsState')
    } as any;

    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    } as any;

    maintenanceService = {
      siteServerHealthCheck: jasmine.createSpy('siteServerHealthCheck').and.returnValue(of({}))
    } as any;

    resolveService = {
      reset: jasmine.createSpy('reset'),
      set: jasmine.createSpy('set').and.returnValue(Promise.resolve({})),
      get: jasmine.createSpy('get').and.returnValue({})
    };

    sessionService = {
      whenProxySession: jasmine.createSpy('whenProxySession').and.returnValue(Promise.resolve())
    };

    route = {
      snapshot: {
        params: {}
      }
    };

    betHistoryMainService = {
      makeSafeCall: jasmine.createSpy('makeSafeCall').and.callFake(x => x),
      getSummaryTotals: jasmine.createSpy('getSummaryTotals').and.returnValue({}),
      getHistoryForTimePeriod: jasmine.createSpy('getHistoryForTimePeriod'),
      showFirstBet: jasmine.createSpy('showFirstBet')
    };

    betsLazyLoadingService = {
      reset: jasmine.createSpy('reset'),
      initialize: jasmine.createSpy('initialize')
    };

    windowRef = {
      document: { dispatchEvent: jasmine.createSpy('dispatchEvent'),
      getElementsByClassName : jasmine.createSpy().and.returnValue([   {classList: {
        add: jasmine.createSpy('add'),
        remove: jasmine.createSpy('remove')}
      }]) }
    };

    casinoMyBetsIntegratedService = {};

    component = new LadbrokesBetHistoryPageComponent(
      cmsService,
      pubSubService,
      betHistoryMainService,
      timeService,
      sessionService,
      liveServConnectionService,
      datepickerValidatorService,
      localeService,
      resolveService,
      maintenanceService,
      route,
      userService,
      betsLazyLoadingService,
      windowRef,
      casinoMyBetsIntegratedService
    );

    component.dateObject = {
      startDate: '',
      endDate: ''
    } as any;
  });

  describe('#createFilters', () => {
    it('should remove digitalSportBet tab', () => {
      component['createFilters']();
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      const digitalSportBet = component['betTypes'].filter((type) => type.viewByFilters === 'digitalSportBet');
      expect(component['betTypes']).toBeDefined();
      expect(digitalSportBet.length).toBe(0);
    });

    it('getTabsList shopBetHistory', () => {
      cmsService.getSystemConfig.and.returnValue(of({
        Connect: {
          inShopBets: true
        }
      }));
      component['createFilters']();
      expect(component.betTypes.length).toEqual(4);
    });
  });
});
