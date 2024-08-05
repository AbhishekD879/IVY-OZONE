import { of as observableOf, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { OpenBetsComponent } from '@app/betHistory/components/openBets/open-bets.component';
import { IBetHistoryBet } from '@app/betHistory/models/bet-history.model';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('OpenBetsComponent', () => {
  let cashoutBetsStreamService, sessionServiceStub,
    liveServConnectionServiceStub, pubSubServiceStub, localeServiceStub, maintenanceServiceStub, betHistoryMainServiceStub,
    userServiceStub, betsLazyLoadingServiceStub, editMyAccaService, dynamicComponentsService, cmsService, cashoutWsConnectorService, datepickerValidatorService, casinoMyBetsIntegratedService,sessionStorageService;

  let component: OpenBetsComponent;

  beforeEach(() => {
    sessionServiceStub = {
      whenProxySession: jasmine.createSpy('whenProxySession').and.returnValue(
        Promise.resolve()
      )
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({
        Connect: {
          inShopBets: true
        }
      }))
    } as any;

    liveServConnectionServiceStub = {
      connect: jasmine.createSpy('connect').and.returnValue(observableOf({}))
    };

    pubSubServiceStub = {
      cbMap: {},
      subscribe: jasmine.createSpy('subscribe').and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
        pubSubServiceStub.cbMap[channel] = channelFunction;
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publishSpy'),
      API: pubSubApi
    };

    localeServiceStub = {
      getString: jasmine.createSpy('getString').and.returnValue('Locale')
    };

    maintenanceServiceStub = {
      siteServerHealthCheck: jasmine.createSpy('siteServerHealthCheck').and.returnValue(observableOf('health status'))
    };

    betHistoryMainServiceStub = {
      getBetStatus: jasmine.createSpy('getBetStatus').and.returnValue('open'),
      getHistoryForYear: jasmine.createSpy('getHistoryForYear').and.returnValue(Promise.resolve({ bets: [{ id: '1' }] } as any)),
      getEditMyAccaHistory: jasmine.createSpy('getEditMyAccaHistory').and.returnValue(observableOf({ bets: [{ id: '2' }] } as any)),
      makeSafeCall: jasmine.createSpy('makeSafeCall').and.callFake(x => x),
      buildSwitchers: jasmine.createSpy('buildSwitchers').and.returnValue([{}]),
      getSwitcher: jasmine.createSpy('getSwitcher'),
      extendCashoutBets: jasmine.createSpy('extendCashoutBets'),
      showFirstBet: jasmine.createSpy('showFirstBet')
    };

    userServiceStub = {
      status: true,
      isInShopUser: jasmine.createSpy('isInShopUser').and.returnValue(false)
    };

    betsLazyLoadingServiceStub = {
      reset: jasmine.createSpy('reset'),
      initialize: jasmine.createSpy('initialize'),
      setData: jasmine.createSpy('setData')
    };

    cashoutWsConnectorService = {
      getDateObject: jasmine.createSpy('getDateObject').and.returnValue({
        startDate: '10/22/2021',
        endDate: '10/25/2021'
      }),
      dateChangeBet: jasmine.createSpy('dateChangeBet').and.returnValue(observableOf([
        { id: 1, betType: 'open' }
      ] as any)),
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
      canChangeRoute: jasmine.createSpy('canChangeRoute'),
    };

    cashoutBetsStreamService = {
      openBetsStream: jasmine.createSpy('openBetsStream').and.returnValue(observableOf([{ id: '3' }])),
      closeBetsStream: jasmine.createSpy('closeBetsStream')
    };

    casinoMyBetsIntegratedService = {};

    sessionStorageService = {
        get: jasmine.createSpy('get').and.callFake(
          n => {
            if(n === 'firstBetTutorial') { return {firstBetAvailable:'true'}} 
            else if(n === 'tutorialCompleted')  {return false}
            else {return true}
        }), 
      set: jasmine.createSpy('set')
    };

    component = new OpenBetsComponent(cmsService, pubSubServiceStub, cashoutBetsStreamService, sessionServiceStub,
      liveServConnectionServiceStub, localeServiceStub, maintenanceServiceStub, betHistoryMainServiceStub,
      userServiceStub, betsLazyLoadingServiceStub, editMyAccaService, cashoutWsConnectorService, datepickerValidatorService, casinoMyBetsIntegratedService,sessionStorageService);
    component.betTypes = [ { viewByFilters: 'bet' }] as any;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      spyOn(component, 'reloadComponent').and.stub();
      spyOn(component as any, 'reload').and.callThrough();
      spyOn(component, 'hideSpinner').and.callThrough();
      spyOn(component as any, 'loadData').and.callThrough();
      spyOn(component as any, 'initTypes').and.callThrough(); 
    });

    it('#ngOnInit should set initial values', fakeAsync(() => {
      component.bets = [{ id: 12345 ,potentialPayout: [{value: "0.09"}], stake: "0.03" }] as any;
      component.ngOnInit();
      expect(betsLazyLoadingServiceStub.reset).toHaveBeenCalled();
      expect(maintenanceServiceStub.siteServerHealthCheck).toHaveBeenCalled();
      expect(component['hideSpinner']).toHaveBeenCalled();
      expect(component['loadData']).toHaveBeenCalled();

      expect(pubSubServiceStub.subscribe).toHaveBeenCalledWith('OpenBets_0', 'EDIT_MY_ACCA', jasmine.any(Function));
      pubSubServiceStub.cbMap['EDIT_MY_ACCA']();
      expect(component['reloadComponent']).toHaveBeenCalledWith(true);

      expect(pubSubServiceStub.subscribe).toHaveBeenCalledWith('OPEN_INSHOP_BETS_COUNT', 'OPEN_INSHOP_BETS_COUNT', jasmine.any(Function));
      pubSubServiceStub.cbMap['OPEN_INSHOP_BETS_COUNT']();

      expect(pubSubServiceStub.subscribe).toHaveBeenCalledWith('OpenBets_0', ['RELOAD_OPEN_BETS'], jasmine.any(Function));
      pubSubServiceStub.cbMap['RELOAD_OPEN_BETS']();
      expect(component['reloadComponent']).toHaveBeenCalledWith();

      expect(pubSubServiceStub.subscribe).toHaveBeenCalledWith(
        'OpenBets_0',
        pubSubServiceStub.API.RELOAD_COMPONENTS,
        jasmine.any(Function)
      );
      pubSubServiceStub.cbMap['RELOAD_COMPONENTS']();
      expect(sessionServiceStub.whenProxySession).toHaveBeenCalled();
      tick();
      expect(component['reload']).toHaveBeenCalled();
    }));

    it(`should initTypes after buildSwitchers`, () => {
      component.ngOnInit();
      expect(component['betHistoryMainService'].buildSwitchers).toHaveBeenCalledBefore(component['initTypes'] as any);
    });

    it(`returns cashOutValue`, () => {
      betHistoryMainServiceStub.getEditMyAccaHistory.and.returnValue(observableOf({ bets: [{ id: '2',cashoutValue:2 }] } as any))
      component.ngOnInit();
      expect(component['betHistoryMainService'].buildSwitchers).toHaveBeenCalled();
    });

    it('#ngOnInit should not call BETS_COUNTER_OPEN_BETS after editing acca', fakeAsync(() => {
      expect(pubSubServiceStub.publish).not.toHaveBeenCalled();

      component['editMyAccaReload'] = true;
      component.ngOnInit();
      expect(pubSubServiceStub.publish).not.toHaveBeenCalledWith('BETS_COUNTER_OPEN_BETS');
    }));
    it('getSystemConfig as undefined', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf(undefined));
      component.ngOnInit();
      expect(component.isSportIconEnabled).not.toBeTrue();
    });
    it('getSystemConfig with CelebratingSuccess as undefined', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({CelebratingSuccess: undefined}));
      component.ngOnInit();
      expect(component.isSportIconEnabled).not.toBeTrue();
    });
    it('getSystemConfig with displaySportIcon as undefined', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({CelebratingSuccess: {displaySportIcon: undefined}}));
      component.ngOnInit();
      expect(component.isSportIconEnabled).not.toBeTrue();
    });
    it('getSystemConfig with displaySportIcon as undefined', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({CelebratingSuccess: {displaySportIcon: ['openbets']}}));
      component.ngOnInit();
      expect(component.isSportIconEnabled).toBeTrue();
    });
  });
  describe('#datepicker initSystemConfig', () => {
    it('initSystemConfig with true values', () => {
      datepickerValidatorService.initSystemConfig.and.returnValue(observableOf({minDate: '2019-04-26', maxDate: '2019-04-26'}));
      component.ngOnInit();
      expect(component.minDate).toBe('2019-04-26');
      expect(component.maxDate).toBe('2019-04-26');
    });
    it('initSystemConfig with undefined values', () => {
      datepickerValidatorService.initSystemConfig.and.returnValue(observableOf(undefined));
      component.ngOnInit();
      expect(component.minDate).not.toBeDefined();
      expect(component.maxDate).not.toBeDefined();
    });
  });

  describe('ngOnDestroy', () => {
    it('#ngOnDestroy should call pubsub.unsubscribe and betsLazyLoading.reset', () => {
      component['betsStreamOpened'] = true;
      component['ctrlName'] = 'test';
      component.ngOnDestroy();
      expect(pubSubServiceStub.publish).toHaveBeenCalledWith(pubSubServiceStub.API.EMA_UNSAVED_IN_WIDGET, false);
      expect(pubSubServiceStub.unsubscribe).toHaveBeenCalledWith(component['ctrlName']);
      expect(betsLazyLoadingServiceStub.reset).toHaveBeenCalled();
      expect(cashoutBetsStreamService.closeBetsStream).toHaveBeenCalled();
    });

    it('#ngOnDestroy should not close stream if already closed', () => {
      component['betsStreamOpened'] = false;
      component.ngOnDestroy();
      expect(cashoutBetsStreamService.closeBetsStream).not.toHaveBeenCalled();
    });

    it('#ngOnDestroy loadDataSub', () => {
      component['loadDataSub'] = <any>{
        unsubscribe: jasmine.createSpy('unsubscribe')
      };
      component['cmsSubscription'] = <any>{
        unsubscribe: jasmine.createSpy('unsubscribe')
      };
      component.ngOnDestroy();
      expect(component['loadDataSub'].unsubscribe).toHaveBeenCalled();
      expect(component['cmsSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });

  it('#userStatus should return userService.status', () => {
    expect(component['userStatus']).toEqual(true);
  });

  it('#setError should call #showError', () => {
    spyOn(component, 'showError');
    component.setError();
    expect(component.showError).toHaveBeenCalled();

    component.setError(true);
    expect(component.showError).toHaveBeenCalled();
  });

  it('#setError should NOT call #showError', () => {
    spyOn(component, 'showError');
    component.setError(false);
    expect(component.showError).not.toHaveBeenCalled();
  });

  it('#reload should call liveServConnectionService.reconnect', () => {
    component['reloadComponent'] = jasmine.createSpy();
    component['reload']();

    expect(liveServConnectionServiceStub.connect).toHaveBeenCalled();
    expect(component['reloadComponent']).toHaveBeenCalled();
  });

  describe('reloadComponent', () => {
    it('#reloadComponent should call isStreamFlowEnabled = false', () => {
      spyOn(component, 'ngOnDestroy');
      spyOn(component, 'showSpinner');
      spyOn(component, 'ngOnInit');

      component['reloadComponent'](true);
      expect(component.ngOnDestroy).toHaveBeenCalled();
      expect(component.showSpinner).toHaveBeenCalled();
      expect(component.ngOnInit).toHaveBeenCalled();
      expect(component['editMyAccaReload']).toBeFalsy();
    });
  });

  describe('changeFilter', () => {
    beforeEach(() => {
      component.betTypes = <any>[{
        viewByFilters: 'bet'
      }];
    });

    it('#changeFilter filter is in-shop', () => {
      component['changeFilter']('shopBet');
      expect(component.filter).toBe('shopBet');
      expect(component['isRetailBetAvailable']).toEqual(false);
    });

    it('#changeFilter should set filter and call #loadData', () => {
      component['loadData'] = jasmine.createSpy();
      component['changeFilter']('testFilter');
      expect(component['loadData']).toHaveBeenCalled();
      expect(component.filter).toEqual('testFilter');
      expect(component['isRetailBetAvailable']).toBeTruthy();
    });

    it('#changeFilter (isUnsavedInWidget open-bets-page)', () => {
      component.area = 'open-bets-page';
      component['editMyAccaService']['isUnsavedInWidget'] = () => true;
      component['editMyAccaService']['canChangeRoute'] = () => true;
      component['changeFilter']('digitalSportBet');
      expect(editMyAccaService.showEditCancelMessage).not.toHaveBeenCalled();
    });

    it('#changeFilter (isUnsavedInWidget)', () => {
      component['editMyAccaService']['isUnsavedInWidget'] = () => true;
      component['changeFilter']('digitalSportBet');
      expect(editMyAccaService.showEditCancelMessage).toHaveBeenCalled();
    });

    it('#changeFilter (isUnsaved open-bets-page)', () => {
      component.area = 'open-bets-page';
      component['editMyAccaService']['isUnsavedInWidget'] = () => false;
      component['editMyAccaService']['canChangeRoute'] = () => false;
      component['changeFilter']('digitalSportBet');
      expect(editMyAccaService.showEditCancelMessage).toHaveBeenCalled();
    });
  });

  it('addLazyLoadBets', () => {
    const lazyBets: IBetHistoryBet[] = [
      { id: 1, betType: 'open' },
      { id: 2, betType: 'open' }
    ] as any;

    component.bets = [];

    component['addLazyLoadedBets'](lazyBets);
    expect(component.bets.length).toEqual(2);
  });

  it('addLazyLoadBets without input args', () => {
    component.bets = [];

    component['addLazyLoadedBets']();
    expect(component.bets.length).toEqual(0);
  });

  it('#loadData should get bets', fakeAsync(() => {
    component['editMyAccaReload'] = false;
    component['loadData']('lotteryBet');
    expect(betsLazyLoadingServiceStub.reset).toHaveBeenCalled();
    expect(component.isLoading).toEqual(true);
    tick();
    expect(userServiceStub.isInShopUser).toHaveBeenCalled();
    expect(betHistoryMainServiceStub.getHistoryForYear).toHaveBeenCalledWith('lotteryBet', 'open');
    expect(betHistoryMainServiceStub.getEditMyAccaHistory).toHaveBeenCalledWith({ bets: [{ id: '1' }] });
    expect(betHistoryMainServiceStub.extendCashoutBets).toHaveBeenCalledWith([{ id: '2' }]);
    expect(betsLazyLoadingServiceStub.initialize).toHaveBeenCalled();
    expect(component.isLoading).toEqual(false);
    expect(pubSubServiceStub.publish).toHaveBeenCalledWith('BETS_COUNTER_OPEN_BETS', jasmine.anything());
    expect(component.bets).toEqual([{ id: '2' }] as any);
  }));

  it('#loadData should get bets from Cashout WS', fakeAsync(() => {
    component['filter'] = 'bet';
    component['loadData']('bet');
    tick();
    expect(cashoutBetsStreamService.openBetsStream).toHaveBeenCalled();
    expect((component as any).betsStreamOpened).toEqual(true);
    expect(betHistoryMainServiceStub.getEditMyAccaHistory).toHaveBeenCalledWith({ bets: [{ id: '3' }] });
    expect(betHistoryMainServiceStub.getHistoryForYear).not.toHaveBeenCalled();
    expect(betHistoryMainServiceStub.extendCashoutBets).toHaveBeenCalledWith([{ id: '2' }]);
    expect(betsLazyLoadingServiceStub.initialize).toHaveBeenCalled();
    expect(component['betsStreamOpened']).toBeTruthy();
  }));

  it('#loadData should not call BETS_COUNTER_OPEN_BETS after editing acca', fakeAsync(() => {
    component['editMyAccaReload'] = true;
    component['loadData']('lotteryBet');
    tick();
    expect(betsLazyLoadingServiceStub.reset).toHaveBeenCalled();
    expect(betsLazyLoadingServiceStub.initialize).toHaveBeenCalled();
    expect(betHistoryMainServiceStub.getEditMyAccaHistory).toHaveBeenCalled();
  }));

  it('#loadData should handle error', fakeAsync(() => {
    cashoutBetsStreamService.openBetsStream.and.returnValue(throwError('error'));
    spyOn(component, 'showError');

    component['loadData']('bet');
    tick();
    expect(localeServiceStub.getString.calls.allArgs())
       .toEqual([['app.betslipTabs.openbets'], ['app.loginToSeePageMessage', { page: 'locale' }]]);
    expect(component.showError).toHaveBeenCalled();
  }));

  it('#loadData should unsubscribe from previous request', () => {
    const unsubscribeSpy = jasmine.createSpy();
    component['loadDataSub'] = { unsubscribe: unsubscribeSpy } as any;

    component['loadData']('bet');

    expect(unsubscribeSpy).toHaveBeenCalledTimes(1);
  });
  it('#loadData should return [] for in-shop user', () => {
    (userServiceStub.isInShopUser as any).and.returnValue(true);

    component['loadData']('bet');
    expect(component.bets).toEqual([]);
  });

  it('call back for nextCashoutBet', fakeAsync(() =>  {
    betsLazyLoadingServiceStub.initialize = jasmine.createSpy('initializeSpy').and.callFake(function initialize(options) {
      options.loadMoreCallBack();
    });
    component['loadData']('bet');
    tick();
        
    expect(component['cashoutWsConnectorService'].nextCashoutBet).toHaveBeenCalled();
  }));

  it('#loadData should return [] for in-shop user (coverage case)', fakeAsync(() => {
    (userServiceStub.isInShopUser as any).and.returnValues(false, true);

    component['loadData']('bet');
    tick();
    expect(cashoutBetsStreamService.openBetsStream).not.toHaveBeenCalled();
    expect(betHistoryMainServiceStub.getHistoryForYear).not.toHaveBeenCalled();
    expect(betHistoryMainServiceStub.getEditMyAccaHistory).toHaveBeenCalledWith({ bets: [] });
    expect(betHistoryMainServiceStub.extendCashoutBets).toHaveBeenCalledWith([{ id: '2' }]);
    expect(betsLazyLoadingServiceStub.initialize).toHaveBeenCalled();
    expect(component.bets).toEqual([{ id: '2' }] as any);
  }));

  describe('initTypes', () => {
    it(`should define Types`, () => {
      const switcher = {
        onClick: () => {},
        viewByFilters: 'someView',
        name: 'someName'
      };
       betHistoryMainServiceStub.extendCashoutBets();
      (betHistoryMainServiceStub.getSwitcher as jasmine.Spy).and.returnValue(switcher);

      component['initTypes']();

      expect(component['TYPES'].every((type: string) => component[type] === switcher)).toBeTruthy();
    });
  });

  describe('dateChange', () => {
    it('#dateChangeBet to be called', () => {
      const startDate = new Date();
      const endDate = new Date();
      const dateChange = component.dateChange();
      dateChange.subscribe(bets => {
        expect(bets).toEqual({
          bets: [
            { id: 1, betType: 'open' }
          ]
        });
      });
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
    });
    it('if isDatePickerError', fakeAsync(() => {
      spyOn(component, 'dateChange');
      component.processDateRangeData(errorObject);
      expect(datepickerValidatorService.updateErrorsState).toHaveBeenCalledWith(
        undefined,
        errorObject,
        component.startDate,
        component.endDate);
        tick();
      expect(component['dateChange']).toHaveBeenCalled();
    }));

    it('if not isDatePickerError', () => {
      component['loadData'] = jasmine.createSpy('loadData');
      component.isDatePickerError = jasmine.createSpy().and.returnValue(true);
      component.processDateRangeData(errorObject);
      expect(component['loadData']).not.toHaveBeenCalled();
    });
  });
  describe('isDatePickerError', () => {
    it('#isDatePickerError to be Falsy', () => {
      expect(component['isDatePickerError']()).toBeFalsy();
    });
  });
});
