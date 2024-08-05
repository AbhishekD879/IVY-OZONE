import { of as observableOf, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { CashOutPageComponent } from '@app/betHistory/components/cashOutPage/cash-out-page.component';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IDateRangeErrors } from '@app/betHistory/models/date-range-errors.model';
import { CashOutBetsMap } from '@app/betHistory/betModels/cashOutBetsMap/cash-out-bets-map.class';

describe('CashOutPageComponent', () => {
  let component: CashOutPageComponent;
  let maintenanceServiceStub;
  let sessionServiceStub;
  let cashoutBetsStreamService;
  let deviceService;
  let infoDialogService;
  let localeServiceStub;
  let userServiceStub;
  let cashoutBetsMap;
  let cashOutMapServiceStub;
  let liveServConnectionServiceStub;
  let pubSubServiceStub;
  let betHistoryMainService;
  let pubsubReg;
  let datepickerValidatorService;
  let cashoutWsConnectorService;
  let betsLazyLoadingService;
  let casinoMyBetsIntegratedService;
  let sessionStorageService;
  let windowRef;

  beforeEach(() => {
    cashoutBetsMap = {
      userCurrency: 'EUR',
      userCurrencySymbol: 'EUR-sym',
      mapState: {}
    } as any;
    cashOutMapServiceStub = {
      cashoutBetsMap: cashoutBetsMap,
      createCashoutBetsMap: jasmine.createSpy()
    };

    betHistoryMainService = {
      extendCashoutBets: jasmine.createSpy('extendCashoutBets')
    };
    liveServConnectionServiceStub = {
      connect: jasmine.createSpy('connect').and.returnValue(observableOf({}))
    };

    pubsubReg = {};

    pubSubServiceStub = {
      subscribe: jasmine.createSpy().and.callFake((domain, channel, fn) => {
        if (Array.isArray(channel)) {
          channel.forEach((channelName: string) => pubsubReg[channelName] = fn);
          } else {
            pubsubReg[channel] = fn;
          }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy().and.callFake( (channel) => pubsubReg[channel] && pubsubReg[channel]() ),
      API: {
        CASHOUT_CTRL_STATUS: 'CASHOUT_CTRL_STATUS',
        EMA_UNSAVED_IN_WIDGET: 'EMA_UNSAVED_IN_WIDGET',
        RELOAD_COMPONENTS: 'RELOAD_COMPONENTS',
        LOAD_CASHOUT_BETS: 'LOAD_CASHOUT_BETS'
      }
    };

    maintenanceServiceStub = {
      siteServerHealthCheck: jasmine.createSpy('siteServerHealthCheck').and.returnValue(
        observableOf('No HealthCheck for non maintenance page')
      )
    };

    sessionServiceStub = {
      whenProxySession: jasmine.createSpy('whenProxySession').and.returnValue(
        new Promise<void>((resolve) => {
          resolve();
        })
      )
    };

    cashoutBetsStreamService = {
      getCashoutBets: jasmine.createSpy('getCashoutBets').and.returnValue(observableOf([])),
      closeBetsStream: jasmine.createSpy('closeBetsStream'),
      clearCashoutBetsObservable: jasmine.createSpy('clearCashoutBetsObservable')
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

    betsLazyLoadingService = {
      initialize: jasmine.createSpy('initialize'),
      setData: jasmine.createSpy('setData')
    };


    localeServiceStub = {
      getString: jasmine.createSpy('getString').and.returnValue('test-string')
    };

    deviceService = {
      isOnline: jasmine.createSpy('isOnline').and.returnValue(true)
    };

    infoDialogService = jasmine.createSpyObj('infoDialogService', ['openConnectionLostPopup']);

    userServiceStub = {
      status: true,
      currency: 'EUR',
      currencySymbol: 'EUR-sym',
      isInShopUser: jasmine.createSpy('isInShopUser').and.returnValue(false)
    };

    casinoMyBetsIntegratedService = {};

    sessionStorageService = {
      get: jasmine.createSpy('get').and.callFake(
        n => {
          if(n === 'firstBetTutorial') { return {firstBetAvailable:'true'}}
          else if(n === 'tutorialCompleted')  {return false}
          else if(n === 'betPlaced')  {return true}
          else if(n === 'buttonText')  {return true}
      }),
      set: jasmine.createSpy('set')
    }

    windowRef = {
      document: {
        getElementsByClassName: jasmine.createSpy('getElementsByClassName').and.returnValue([{
          classList: {
            contains: jasmine.createSpy().and.returnValue('display-none'),
            remove: jasmine.createSpy().and.returnValue('display-none')
          }
        }])
      }
    }

    component = new CashOutPageComponent(cashOutMapServiceStub, userServiceStub, maintenanceServiceStub,
      sessionServiceStub, liveServConnectionServiceStub, pubSubServiceStub, localeServiceStub,
      deviceService, infoDialogService, cashoutBetsStreamService, datepickerValidatorService, cashoutWsConnectorService,betsLazyLoadingService, betHistoryMainService, casinoMyBetsIntegratedService, sessionStorageService, windowRef);
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  it('should open info dialog when device is not online', fakeAsync(() => {
    deviceService.isOnline.and.returnValue(false);

    component.ngOnInit();
    tick();

    expect(infoDialogService.openConnectionLostPopup).toHaveBeenCalled();
    expect(maintenanceServiceStub.siteServerHealthCheck).not.toHaveBeenCalled();
    expect(localeServiceStub.getString).toHaveBeenCalled();
    expect(component.state.error).toBeTruthy();
  }));

  it(' display FirstBet getElementsByClassName empty', fakeAsync(() => {
    deviceService.isOnline.and.returnValue(false);
    windowRef.document.getElementsByClassName.and.returnValue([]);
    component.ngOnInit();
    tick();

    expect(infoDialogService.openConnectionLostPopup).toHaveBeenCalled();
    expect(maintenanceServiceStub.siteServerHealthCheck).not.toHaveBeenCalled();
  }));

  it('#ngOnInit should call stack of functions and subscribe', fakeAsync(() => {
    component['reload'] = jasmine.createSpy('reload');
    component.ngOnInit();
    tick();

    expect(cashoutBetsStreamService.clearCashoutBetsObservable).toHaveBeenCalled();
    expect(maintenanceServiceStub.siteServerHealthCheck).toHaveBeenCalled();
    expect(sessionServiceStub.whenProxySession).toHaveBeenCalled();
    expect(cashoutBetsStreamService.getCashoutBets).toHaveBeenCalled();

    expect(pubSubServiceStub.subscribe).toHaveBeenCalledWith(
      component.title,
      ['LOAD_CASHOUT_BETS', 'RELOAD_COMPONENTS'],
      jasmine.any(Function)
    );

    expect(pubSubServiceStub.subscribe).toHaveBeenCalledWith(
      component.title,
      'EDIT_MY_ACCA',
      jasmine.any(Function)
    );

    pubSubServiceStub.publish(`RELOAD_COMPONENTS`);
    pubSubServiceStub.publish('LOAD_CASHOUT_BETS');
    expect(component['reload']).toHaveBeenCalledTimes(2);
  }));

  it('#ngOnInit should not retrieve cashout bets for inShop user', fakeAsync(() => {
    userServiceStub.isInShopUser.and.returnValue(true);

    component.ngOnInit();
    tick();

    expect(maintenanceServiceStub.siteServerHealthCheck).toHaveBeenCalled();
    expect(sessionServiceStub.whenProxySession).toHaveBeenCalled();
    expect(cashoutBetsStreamService.getCashoutBets).not.toHaveBeenCalled();
    expect(cashOutMapServiceStub.createCashoutBetsMap).toHaveBeenCalledWith([], userServiceStub.currency,
      userServiceStub.currencySymbol);
  }));

  it('#ngOnInit should handle maintenanceService.siteServerHealthCheck error', fakeAsync(() => {
    const areaInput = 'cashout-page';
    maintenanceServiceStub.siteServerHealthCheck.and.returnValue(throwError('error'));
    component['errorHandler'] = jasmine.createSpy('errorHandler');
    component.area = areaInput;

    component.ngOnInit();
    tick();

    expect(component.title).toEqual(areaInput);
    expect(component['errorHandler']).toHaveBeenCalled();
  }));
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
    it('#ngDestroy should call pubSubServiceStub.unsubscribe and pubSubServiceStub.publish', fakeAsync(() => {
      component.ngOnInit();
      component['cashoutDataSubscription'] = null;

      tick();

      component.ngOnDestroy();

      expect(cashoutBetsStreamService.clearCashoutBetsObservable).toHaveBeenCalled();
      expect(pubSubServiceStub.publish).toHaveBeenCalledWith(
        'CASHOUT_CTRL_STATUS',
        { ctrlName: 'fullCashout', isDestroyed: true }
      );
      expect(pubSubServiceStub.publish).toHaveBeenCalledWith('EMA_UNSAVED_IN_WIDGET', false);
      expect(pubSubServiceStub.unsubscribe).toHaveBeenCalledWith(component.title);
      expect(cashoutBetsStreamService.closeBetsStream).toHaveBeenCalled();
      expect(component['betsStreamOpened']).toBeFalsy();
    }));

    it('should unsubscribe from cashout data subscription', fakeAsync(() => {
      component.ngOnInit();
      spyOn(component['cashoutDataSubscription'], 'unsubscribe').and.callThrough();

      tick();

      component['betsStreamOpened'] = false;
      component.ngOnDestroy();

      expect(component['cashoutDataSubscription'].unsubscribe).toHaveBeenCalled();
      expect(cashoutBetsStreamService.closeBetsStream).not.toHaveBeenCalled();
      expect(component['betsStreamOpened']).toBeFalsy();
    }));
  });

  it('#userStatus should return userService.status', () => {
    expect(component.userStatus).toEqual(userServiceStub.status);
  });

  it('#reload should call SessionService.whenProxySession, liveServService.reconnect', fakeAsync(() => {
    component['reloadComponent'] = jasmine.createSpy();
    component['reload']();
    tick();
    expect(sessionServiceStub.whenProxySession).toHaveBeenCalled();
    expect(liveServConnectionServiceStub.connect).toHaveBeenCalled();
  }));

  it('#reloadComponent should call #ngOnDestroy, #showSpinner, #ngOnInit', () => {
    spyOn(component, 'ngOnInit');
    spyOn(component, 'ngOnDestroy');
    spyOn(component, 'showSpinner');

    component['reloadComponent']();
    expect(component.ngOnDestroy).toHaveBeenCalled();
    expect(component.showSpinner).toHaveBeenCalled();
    expect(component.ngOnInit).toHaveBeenCalled();
  });
  it('#extendCashOutDataWithMap should call cashOutMapService.createCashoutBetsMap', () => {
    const bets: IBetDetail[] = [];
    component['extendCashOutDataWithMap'](bets);

    expect(cashOutMapServiceStub.createCashoutBetsMap).toHaveBeenCalledWith(bets, 'EUR', 'EUR-sym');
  });

  it('#errorHandler should call localeService.getString and show error', () => {
    spyOn(component, 'showError');
    component['errorHandler']();

    expect(localeServiceStub.getString).toHaveBeenCalledTimes(2);
  });

  describe('filterCashoutBets', () => {
    it('should return only bets with cashout available', () => {
      const betsArray = [
        {
          cashoutValue: '0.00'
        },
        {
          cashoutValue: '5.71'
        },
        {
          cashoutValue: 'CASHOUT_SELN_SUSPENDED'
        },
        {
          cashoutValue: 'CASHOUT_UNAVAILABLE'
        }
      ] as any;
      const result = component['filterCashoutBets'](betsArray);
      expect(result).toEqual(
        [
          {
            cashoutValue: '0.00'
          },
          {
            cashoutValue: '5.71'
          },
          {
            cashoutValue: 'CASHOUT_SELN_SUSPENDED'
          }
        ] as any);
    });
    it('should`t fail in case if no bets received', () => {
      expect(component['filterCashoutBets'](undefined)).toEqual([]);
    });
  });

  it('reloadSegment when EDIT_MY_ACCA', () => {
    pubSubServiceStub.subscribe.and.callFake((channel, method, fn) => {
      if (method === 'EDIT_MY_ACCA') {
        fn();
      }
    });
    spyOn<any>(component, 'reloadSegment');
    component.ngOnInit();

    expect(component['reloadSegment']).toHaveBeenCalled();
  });

  it('#processDateRangeData should be called', fakeAsync(() => {
    userServiceStub.isInShopUser.and.returnValue(false);
    spyOn(component, 'loadCashOutBetsData').and.callThrough();

    component.processDateRangeData({} as IDateRangeErrors);
    tick();

    expect(component.loadCashOutBetsData).toHaveBeenCalled();
  }));

  it('#processDateRangeData should be called - isDatePickerError - true', fakeAsync(() => {
    component.isDatePickerError = jasmine.createSpy().and.returnValue(true);
    spyOn(component, 'loadCashOutBetsData').and.callThrough();

    component.processDateRangeData({} as IDateRangeErrors);
    tick();

    expect(component.loadCashOutBetsData).not.toHaveBeenCalled();
  }));

  it('#addLazyLoadedBets should be called', fakeAsync(() => {
    const extendCashOutData = {} as CashOutBetsMap;
    component.data = {} as CashOutBetsMap;
    spyOn<any>(component, 'handleBetsData').and.callThrough();
    spyOn<any>(component, 'extendCashOutDataWithMap').and.returnValue(extendCashOutData);

    component['addLazyLoadedBets']();
    tick();

    expect(component.handleBetsData).toHaveBeenCalled();
    expect(component['extendCashOutDataWithMap']).toHaveBeenCalled();
    expect(component.data).toEqual({ ...component.data, ...extendCashOutData } as CashOutBetsMap);
  }));

  it('#isDatePickerError should be called', fakeAsync(() => {
    component.datePickerErrors = {
      startDateInFuture: false,
      endDateInFuture: false,
      moreThanOneYear: false,
      moreThanThreeMonthRange: false,
      moreThanFourYears: false,
      moreThanFourYearsRange: false,
      endDateLessStartDate: false,
      isValidstartDate: true,
      isValidendDate: true
    };
    datepickerValidatorService.isFourYearsDatePickerError.and.callThrough();

    component.isDatePickerError();
    tick();

    expect(component['datepickerValidatorService'].isFourYearsDatePickerError).toHaveBeenCalledWith(component.datePickerErrors);
  }));

  it('call back for nextCashoutBet', fakeAsync(() =>  {
    betsLazyLoadingService.initialize = jasmine.createSpy('initializeSpy').and.callFake(function initialize(options) {
      options.loadMoreCallBack();
    });
    component.loadCashOutBetsData();
    tick();
    
    expect(component['cashoutWsConnectorService'].nextCashoutBet).toHaveBeenCalled();
  }));

  it('should show default content when no bets available for first bet', fakeAsync(() => {
    component.isDatePickerError = jasmine.createSpy().and.returnValue(true);
    spyOn(component, 'loadCashOutBetsData').and.callThrough();
    
    betsLazyLoadingService.initialize = jasmine.createSpy('initializeSpy').and.callFake(function initialize(options) {
      options.loadMoreCallBack();
    });
    component.loadCashOutBetsData();
    spyOn<any>(component, 'handleBetsData').and.returnValue([{
      cashoutValue: '0.00'
    },
    {
      cashoutValue: '5.71'
    },
    {
      cashoutValue: 'CASHOUT_SELN_SUSPENDED'
    }] as any);
    tick();
    
    expect(component['cashoutWsConnectorService'].nextCashoutBet).toHaveBeenCalled();
  }))

});
