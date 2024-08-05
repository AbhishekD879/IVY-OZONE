import { BetHistoryPageComponent } from '@app/betHistory/components/betHistoryPage/bet-history-page.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { of, throwError, Subject } from 'rxjs';

describe('BetHistoryPageComponent', () => {
  let component: BetHistoryPageComponent;

  let pubSubService, liveServConnectionService,
    userService, timeService, betsLazyLoadingService, localeService, datepickerValidatorService,
    maintenanceService, resolveService, sessionService, route, loginHandler, betHistoryMainService,
    dynamicComponentsService, cmsService, windowRef, ezNavVanillaService: any;

  beforeEach(() => {
    liveServConnectionService = {
      connect: jasmine.createSpy('connect').and.returnValue(of({}))
    };

    userService = {
      status: true
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(of({
        Connect: {
          inShopBets: true
        },
        CelebratingSuccess: {
          cashoutMessage: "YOU HAVE CASHED OUT: {amount}!!",
          celebrationBannerURL: "{6C768A64-74F8-46FE-A380-9DE3E51C2EBA}",
          celebrationMessage: "CONGRATS!",
          displayCelebrationBanner: true,
          duration: 48,
          winningMessage: "YOU HAVE WON: {amount}!!",
          displaySportIcon: ["openbets", "settledbets", "cashoutbets", "betreceipt", "edpmybets"]
        }
      }))
    } as any;

    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('2019-04-26 00:00:00')
    } as any;

    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('Lorem')
    } as any;

    datepickerValidatorService = {
      getDefaultErrorsState: jasmine.createSpy('getDefaultErrorsState').and.returnValue(false),
      isDatePickerError: jasmine.createSpy('isDatePickerError').and.returnValue(false),
      updateErrorsState: jasmine.createSpy('updateErrorsState'),
      initSystemConfig: jasmine.createSpy('initSystemConfig').and.returnValue(of({minDate: '2019-04-26', maxDate: '2019-04-26'}))
    } as any;

    pubSubService = {
      cbMap: {},
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy('subscribe').and.callFake((subscriber, method, handler) => {
        if (method === 'SESSION_LOGIN') {
          loginHandler = handler;
        } else {
          pubSubService.cbMap[method] = handler;
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    } as any;

    maintenanceService = {
      siteServerHealthCheck: jasmine.createSpy('siteServerHealthCheck').and.returnValue(of({}))
    } as any;

    resolveService = {
      reset: jasmine.createSpy('reset'),
      set: jasmine.createSpy('set').and.returnValue(of({})),
      get: jasmine.createSpy('get').and.returnValue({})
    };

    sessionService = {
      whenProxySession: jasmine.createSpy('whenProxySession').and.returnValue(of({}))
    };

    route = {
      snapshot: {
        params: {}
      }
    };

    betHistoryMainService = {
      makeSafeCall: jasmine.createSpy('makeSafeCall').and.callFake(x => x),
      getSummaryTotals: jasmine.createSpy('getSummaryTotals').and.returnValue({}),
      getHistoryForTimePeriod: jasmine.createSpy('getHistoryForTimePeriod').and.returnValue(of([])),
      showFirstBet: jasmine.createSpy('showFirstBet').and.returnValue(of([]))
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
      }])
    }
    };

    ezNavVanillaService = {};

    component = new BetHistoryPageComponent(
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
      ezNavVanillaService
    );

    component.dateObject = {
      startDate: '',
      endDate: ''
    } as any;
  });

  it('#ngOnInit should init the component', () => {
    component.ngOnInit();
    expect(localeService.getString).toHaveBeenCalledWith('app.loginToSeePageMessage', {
      page: 'lorem'
    });
    expect(component.errorMsg).toBe('Lorem');
    expect(component.contactUsMsg).toBe('Lorem');
    expect(component.regularType).toBeTruthy();
    expect(component.betTypes.length).toBe(3);
    expect(datepickerValidatorService.getDefaultErrorsState).toHaveBeenCalled();

    maintenanceService.siteServerHealthCheck().subscribe(() => {
      expect(component.isLoading).toBe(false);
      expect(resolveService.set).toHaveBeenCalled();
    });
    (pubSubService.subscribe as jasmine.Spy).and.callFake((...args) => args[2]());
    expect(pubSubService.subscribe).toHaveBeenCalledWith('SETTLED_INSHOP_BETS_COUNT',
      'SETTLED_INSHOP_BETS_COUNT', jasmine.any(Function));
      pubSubService.cbMap['SETTLED_INSHOP_BETS_COUNT']();
  });
  
  it('#loginHandler', () => {
    component['assignListeners']();
    loginHandler();
    expect(localeService.getString).toHaveBeenCalled();
  });

  it('#memorizeSummaryState should set isExpanded state for summary', () => {
    component.memorizeSummaryState(true);
    expect(component.isExpandedSummary).toBe(true);
  });

  it('should test initial time range - 29 days', () => {
    timeService.oneDayInMiliseconds = 86400000;
    component['dateInit']();
    const startTime = new Date(component['startDate'].value).getTime();
    const endTime = new Date(component['endDate'].value).getTime();
    const daysCount = ((endTime - startTime) / timeService.oneDayInMiliseconds);
    expect(Math.floor(daysCount)).toEqual(29);
  });

  it('#createFilters should create data for switchers on the page', () => {
    component['changeFilter'] = jasmine.createSpy().and.returnValue('changefilter');
    component['createFilters']();

    expect(component.regularType.viewByFilters).toBe('bet');
    expect(component.regularType.onClick('bet')).toEqual('changefilter');
    expect(component.lottoType.name).toBe('Lorem');
    expect(component.lottoType.onClick('bet')).toEqual('changefilter');
    expect(component.poolType.refs).toBe('pool');
    expect(component.poolType.onClick('bet')).toEqual('changefilter');
    expect(component.betTypes.length).toBe(3);
    expect(component.filter).toBe('bet');
    expect(component.summarySelected).toBe('sb');
  });

  it('#calling showFirstBet without first bet should return', () => {
    windowRef.document = {
      getElementsByClassName: jasmine.createSpy().and.callFake(param => {
        if (param === 'firstBet') {
          return [];
        }
      }),
      body: {
        appendChild: jasmine.createSpy('appendChild'),
        classList: {
          add: jasmine.createSpy('add'),
          remove: jasmine.createSpy('remove')
        }
      }
    };
    component.ngOnInit();
    expect(windowRef.document.body.classList.add).not.toHaveBeenCalledWith('display-none');
    expect(windowRef.document.body.classList.remove).not.toHaveBeenCalledWith('display-none');
  })
  describe('#datepicker initSystemConfig', () => {
    it('initSystemConfig with true values', () => {
      datepickerValidatorService.initSystemConfig.and.returnValue(of({minDate: '2019-04-26', maxDate: '2019-04-26'}));
      component.ngOnInit();
      expect(component.minDate).toBe('2019-04-26');
      expect(component.maxDate).toBe('2019-04-26');
    });
    it('initSystemConfig with undefined values', () => {
      datepickerValidatorService.initSystemConfig.and.returnValue(of(undefined));
      component.ngOnInit();
      expect(component.minDate).not.toBeDefined();
      expect(component.maxDate).not.toBeDefined();
    });
  });
  describe('#cmsService getSystemConfig', () => {
    it('getSystemConfig as undefined', () => {
      cmsService.getSystemConfig.and.returnValue(of(undefined));
      component.ngOnInit();
      expect(component.isSportIconEnabled).not.toBeTrue();
    });
    it('getSystemConfig with CelebratingSuccess as undefined', () => {
      cmsService.getSystemConfig.and.returnValue(of({CelebratingSuccess: undefined}));
      component.ngOnInit();
      expect(component.isSportIconEnabled).not.toBeTrue();
    });
    it('getSystemConfig with displaySportIcon as undefined', () => {
      cmsService.getSystemConfig.and.returnValue(of({CelebratingSuccess: {displaySportIcon: undefined}}));
      component.ngOnInit();
      expect(component.isSportIconEnabled).not.toBeTrue();
    });
    it('getSystemConfig with displaySportIcon as undefined', () => {
      cmsService.getSystemConfig.and.returnValue(of({CelebratingSuccess: {displaySportIcon: ['settledbets']}}));
      component.ngOnInit();
      expect(component.isSportIconEnabled).toBeTrue();
    });
  });
  describe('#changeFilter', () => {
    beforeEach(() => {
      component.betTypes = [{
        viewByFilters: 'bet',
        refs: 'sb'
      }, {
        viewByFilters: 'digitalSportBet'
      }] as any;
    });

    it('if filter is in-shop', () => {
      component['changeFilter']('shopBet');
      expect(component.filter).toBe('shopBet');
      expect(component.isRetailBetAvailable).toEqual(false);
    });

    it('if digitalSportBet', () => {
      component['changeFilter']('digitalSportBet');

      expect(component.filter).toBe('digitalSportBet');
      expect(component.showDatepicker).toBe(false);
      expect(component.isRetailBetAvailable).toEqual(true);
    });

    it('if not digitalSportBet but dateError', () => {
      (datepickerValidatorService.isDatePickerError as jasmine.Spy).and.returnValue(true);
      component['changeFilter']('bet');

      expect(component.filter).toBe('bet');
      expect(component.showDatepicker).toBe(true);
      expect(component.isRetailBetAvailable).toEqual(true);
    });

    it('if not digitalSportBet and not dateError', () => {
      component.startDate = { value: '' } as any;
      component.endDate = { value: '' } as any;
      component['changeFilter']('bet');

      expect(betsLazyLoadingService.reset).toHaveBeenCalled();
      expect(component.summarySelected).toBe('sb');
      expect(component.filter).toBe('bet');
      expect(component.showDatepicker).toBe(true);
      expect(component.isRetailBetAvailable).toBe(true);
    });
  });

  describe('processDateRangeData function', () => {
    let errorObject;

    beforeEach(() => {
      const startDate = new Date();
      const endDate = new Date();
      errorObject = {
        startDateInFuture: false,
        endDateInFuture: false,
        moreThanOneYear: false,
        moreThanThreeMonthRange: false,
        endDateLessStartDate: false,
        isValidstartDate: true,
        isValidendDate: true
      };

      component.startDate = { value: startDate };
      component.endDate = { value: endDate };
      component['loadData'] = jasmine.createSpy('loadData');
    });

    it('should call updateErrorsState with params', () => {
      component.filter='bet';
      component.processDateRangeData(errorObject);

      expect(datepickerValidatorService.updateErrorsState).toHaveBeenCalledWith(
        undefined,
        errorObject,
        component.startDate,
        component.endDate);
      expect(component['windowRef'].document.dispatchEvent).not.toHaveBeenCalled();
      expect(component['loadData']).toHaveBeenCalled();
    });

    it('if isDatePickerError', () => {
      component.isDatePickerError = jasmine.createSpy().and.returnValue(true);
      component.processDateRangeData(errorObject);
      expect(component['windowRef'].document.dispatchEvent).not.toHaveBeenCalled();
      expect(component['loadData']).not.toHaveBeenCalled();
    });

    it('if filter is shopBet event should be dispatched', () => {
      component.filter = 'shopBet';
      component.processDateRangeData(errorObject);
      expect(datepickerValidatorService.updateErrorsState).toHaveBeenCalledWith(
        undefined,
        errorObject,
        component.startDate,
        component.endDate);
      expect(component['windowRef'].document.dispatchEvent).toHaveBeenCalled();
    });
  });

  describe('reloadComponent', () => {
    beforeEach(() => {
      spyOn(component as any, 'getDateObject').and.returnValue({ startDate: '', endDate: '' });
    });

    it(`should call through ngDestroy, ngOnInit`, () => {
      component['reloadComponent']();

      expect(component.loadFailed).toBe(false);
      expect(betsLazyLoadingService.reset).toHaveBeenCalled();
      expect(component.state.loading).toBe(false);
      expect(maintenanceService.siteServerHealthCheck).toHaveBeenCalled();
    });
  });

  describe('reload', () => {
    it('should connect to LS and call reloadSegment method', () => {
      const connection = new Subject();
      spyOn(component as any, 'reloadComponent');
      liveServConnectionService.connect.and.returnValue(connection);
      component.reload();
      expect(liveServConnectionService.connect).toHaveBeenCalled();
      expect(component['reloadComponent']).not.toHaveBeenCalled();
      connection.next({});
      expect(component['reloadComponent']).toHaveBeenCalled();
    });
  });

  describe('loadData', () => {
    beforeEach(() => {
      component['getDateObject'] = jasmine.createSpy('getDateObject');
      component['addLazyLoadedBets'] = jasmine.createSpy('addLazyLoadedBets');
      component['hideSpinner'] = jasmine.createSpy('hideSpinner');
      component['filterBetHistory'] = jasmine.createSpy('filterBetHistory');
      component.setError = jasmine.createSpy('setErr');
    });

    it('should load data, succesfull betsLazyLoading initialize', () => {
      (resolveService.set as jasmine.Spy).and.callFake(() => of({}));
      component['loadData']();
      expect(component.isLoading).toBe(false);
      expect(betsLazyLoadingService.reset).toHaveBeenCalled();
      expect(betsLazyLoadingService.initialize).toHaveBeenCalled();
      expect(betHistoryMainService.makeSafeCall).toHaveBeenCalled();
      expect(sessionService.whenProxySession).toHaveBeenCalled();
      expect(component['hideSpinner']).toHaveBeenCalled();
      expect(component['filterBetHistory']).toHaveBeenCalled();
      expect(component.setError).not.toHaveBeenCalled();
    });

    it('betsLazyLoading initialize error', () => {
      (resolveService.set as jasmine.Spy).and.returnValue(throwError(''));
      component['loadData']();
      expect(component.setError).toHaveBeenCalledWith(true);
    });

  });

  it('#getSelectedSwitcher should get selected tab', () => {
    component.betTypes = [{
      viewByFilters: 'bet',
      refs: 'sb'
    }, {
      viewByFilters: 'digitalSportBet'
    }] as any;

    expect(component['getSelectedSwitcher']('bet')).toEqual({
      viewByFilters: 'bet',
      refs: 'sb'
    } as any);
  });

  it('#getSummarySwitcherRefs should get refs props from array of objects', () => {
    component.betTypes = [{
      refs: 'sb'
    }, {
      refs: 'lotto'
    }] as any;

    expect(component['getSummarySwitcherRefs']()).toEqual(['sb', 'lotto'] as any);
  });

  it('#assignListeners', () => {
    (pubSubService.subscribe as jasmine.Spy).and.callFake((...args) => args[2]());
    component.ngOnInit = jasmine.createSpy('ngOnInit');  // to prevent circular calls
    component['ctrlName'] = 'BetHistoryComponent';
    component.startDate = { value: '' } as any;
    component.endDate = { value: '' } as any;

    component['assignListeners']();

    expect(pubSubService.subscribe).toHaveBeenCalledWith('BetHistoryComponent',
      pubSubService.API.RELOAD_COMPONENTS, jasmine.any(Function));
    expect(sessionService.whenProxySession).toHaveBeenCalled();
    expect(datepickerValidatorService.updateErrorsState).toHaveBeenCalled();
  });

  describe('#addLazyLoadedBets', () => {
    it('should set bets to the component with parameters', () => {
      component.bets = [{ id: 1 }] as any;
      const lazyLoadedBets = [{ id: 2 }] as any;
      component['filterBetHistory'] = jasmine.createSpy().and.returnValue(lazyLoadedBets);
      component['addLazyLoadedBets'](lazyLoadedBets);
      expect(component['filterBetHistory']).toHaveBeenCalledWith(lazyLoadedBets);
      expect(component.bets.length).toBe(2);
    });
    it('should set bets to the component without parameters', () => {
      const bet = { id: 1 };
      component.bets = [bet] as any;
      component['filterBetHistory'] = jasmine.createSpy().and.returnValue([]);
      component['addLazyLoadedBets']();
      expect(component['filterBetHistory']).toHaveBeenCalledWith([]);
      expect(component.bets.length).toBe(1);
    });
  });

  it('#userStatus should return userService.status', () => {
    expect(component.userStatus).toEqual(true);
  });

  it('#isBetsTab should return filter !== digitalSportBet value', () => {
    component.filter = '';
    expect(component.isBetsTab).toEqual(true);
  });

  it('#setError should call showError, false case', () => {
    component.showError = jasmine.createSpy('showError');
    component.setError(false);
    expect(component.showError).not.toHaveBeenCalled();
  });

  it('#setError should call showError, true case', () => {
    component.loadFailed = false;
    component.showError = jasmine.createSpy('showError');
    component.setError();
    expect(component.loadFailed).toEqual(true);
    expect(component.showError).toHaveBeenCalled();
  });

  it('filterBetHistory, negative case', () => {
    component.filter = 'notbet';
    component['betHistoryMainService'].getBetStatus = jasmine.createSpy().and.returnValue(false);
    expect(component['filterBetHistory']([])).toEqual([]);
  });

  it('filterBetHistory, positive case', () => {
    component.filter = 'bet';
    component['betHistoryMainService'].getBetStatus = jasmine.createSpy().and.returnValue(component['filteredBetsStatus']);
    component['filterBetHistory'](['bet1', 'bet2']);
    expect(component['betHistoryMainService'].getBetStatus).toHaveBeenCalledTimes(2);
  });

  describe('ngOnDestroy', () => {
    it('#ngOnDestroy cmsSubscription', () => {
      component['cmsSubscription'] = <any>{
        unsubscribe: jasmine.createSpy('unsubscribe')
      };
      component.ngOnDestroy();
      expect(component['cmsSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });
});
