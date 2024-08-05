import { of as observableOf } from 'rxjs';
import { OpenBetsComponent } from '@ladbrokesMobile/betHistory/components/openBets/open-bets.component';

describe('OpenBetsComponent', () => {
  let component: OpenBetsComponent;
  let sessionServiceStub;
  let liveServConnectionServiceStub;
  let pubSubServiceStub;
  let localeServiceStub;
  let maintenanceServiceStub;
  let betHistoryMainServiceStub;
  let userServiceStub;
  let betsLazyLoadingServiceStub;
  let cashoutBetsStreamServiceStub;
  let editMyAccaService;
  let cmsService;
  let cashoutWsConnectorService;
  let datepickerValidatorService;
  let casinoMyBetsIntegratedService;
  let storageService;

  beforeEach(() => {
    sessionServiceStub = {
      whenProxySession: jasmine.createSpy().and.returnValue(
        Promise.resolve()
      )
    };

    liveServConnectionServiceStub = {
      connect: jasmine.createSpy().and.returnValue(observableOf({}))
    };

    pubSubServiceStub = {
      subscribe: jasmine.createSpy(),
      publish: jasmine.createSpy('publish'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        RELOAD_COMPONENTS: 'reload'
      }
    };

    localeServiceStub = {
      getString: jasmine.createSpy().and.returnValue('locale')
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({
        Connect: {
          inShopBets: true
        }
      }))
    } as any;

    maintenanceServiceStub = {
      siteServerHealthCheck: jasmine.createSpy().and.returnValue(observableOf('health status'))
    };

    betHistoryMainServiceStub = {
      getBetStatus: jasmine.createSpy().and.returnValue('open'),
      getHistoryForYear: jasmine.createSpy('getHistoryForYear').and.returnValue(observableOf({ bets: [{}] } as any)),
      getEditMyAccaHistory: jasmine.createSpy('getEditMyAccaHistory').and.returnValue(observableOf({ bets: [{}] } as any)),
      makeSafeCall: jasmine.createSpy().and.callFake(x => x),
      buildSwitchers: jasmine.createSpy().and.returnValue([{}]),
      getSwitcher: jasmine.createSpy(),
      extendCashoutBets: jasmine.createSpy('extendCashoutBets'),
      showFirstBet: jasmine.createSpy('showFirstBet')
    };

    userServiceStub = {
      status: true,
      isInShopUser: jasmine.createSpy().and.returnValue(false)
    };

    betsLazyLoadingServiceStub = {
      reset: jasmine.createSpy(),
      initialize: jasmine.createSpy()
    };

    cashoutBetsStreamServiceStub = {
      openBetsStream: jasmine.createSpy().and.returnValue(observableOf([])),
      closeBetsStream: jasmine.createSpy()
    };

    cashoutWsConnectorService = {
      getDateObject: jasmine.createSpy('getDateObject').and.returnValue({
        startDate: '10/22/2021',
        endDate: '10/25/2021'
      }),
      dateChangeBet: jasmine.createSpy('dateChangeBet').and.returnValue(observableOf([])),
      nextCashoutBet: jasmine.createSpy('nextCashoutBet').and.returnValue(observableOf([])),
      getInitialDateRanges: jasmine.createSpy('getInitialDateRanges').and.returnValue({
        startDate: '10/22/2021',
        endDate: '10/25/2021'
      }),
      getFormattedDateObject: jasmine.createSpy('getFormattedDateObject').and.returnValue({
        startDate: '10/22/2021',
        endDate: '10/25/2021'
      })
    };

    datepickerValidatorService = {
      getDefaultErrorsState: jasmine.createSpy('getDefaultErrorsState').and.returnValue({
        startDateInFuture: false,
        endDateInFuture: false,
        moreThanOneYear: false,
        moreThanThreeMonthRange: false,
        moreThanFourYears: false,
        moreThanFourYearsRange: false,
        endDateLessStartDate: false,
        isValidstartDate: true,
        isValidendDate: true
      }),
      updateErrorsState: jasmine.createSpy('updateErrorsState'),
      isFourYearsDatePickerError: jasmine.createSpy('isFourYearsDatePickerError').and.returnValue(false),
      initSystemConfig: jasmine.createSpy('initSystemConfig').and.returnValue(observableOf({minDate: '2019-04-26', maxDate: '2019-04-26'}))
    } as any;
    
    editMyAccaService = {
      isUnsavedInWidget: jasmine.createSpy('isUnsavedInWidget'),
      showEditCancelMessage: jasmine.createSpy('isUnsavedInWidget'),
    };

    casinoMyBetsIntegratedService = {};
    storageService = {
      get: jasmine.createSpy('get')
    };
    component = new OpenBetsComponent(
      cmsService,
      pubSubServiceStub,
      cashoutBetsStreamServiceStub,
      sessionServiceStub,
      liveServConnectionServiceStub,
      localeServiceStub,
      maintenanceServiceStub,
      betHistoryMainServiceStub,
      userServiceStub,
      betsLazyLoadingServiceStub,
      editMyAccaService,
      cashoutWsConnectorService,
      datepickerValidatorService,
      casinoMyBetsIntegratedService,
      storageService
    );
  });

  describe('ngOnInit', () => {
    it('should remove digitalSportBet tab', () => {
      storageService.get.and.returnValue('GB');
      component.ngOnInit();
      const digitalSportBet = component['betTypes'].filter((type) => type.viewByFilters === 'digitalSportBet');
      expect(component['betTypes']).toBeDefined();
      expect(digitalSportBet.length).toBe(0);
    });

    it('getTabsList shopBetHistory', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({
        Connect: {
          inShopBets: true
        }
      }));
      component.ngOnInit();
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      expect(component.betTypes).toBeDefined();
    });
  });
});
