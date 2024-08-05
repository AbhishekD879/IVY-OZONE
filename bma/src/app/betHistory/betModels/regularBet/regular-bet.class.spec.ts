import { fakeAsync, tick } from '@angular/core/testing';
import { cashoutConstants } from 'app/betHistory/constants/cashout.constant';
import { RegularBet } from './regular-bet.class';

describe('RegularBetModel', () => {
  let model: RegularBet;

  let bet,
      betModelService,
      currency,
      currencySymbol,
      cashOutMapIndex,
      betHistoryMainService,
      localeService,
      cashOutErrorMessage;
  const part = [{
    startTime: new Date().toISOString(),
    outcome: [{
      name: 'Wimbeldon To Win',
      event: {
        startTime: new Date().toISOString(),
      },
      market: {},
      result: {
        value: 1
      },
      eventCategory: {
        id: 16
      }
    }],
    price: [{
      priceNum: '1',
      priceDen: '2'
    }]
  }];
  beforeEach(() => {
    bet = {
      id: 1234,
      betType: {
        code: 'qwertyui'
      },
      leg: [{
        legType: {
          code: 'qwertyui'
        },
        part: part
      }],
      stake: {
        stakePerLine: 1
      },
      cashoutValue: 10,
      partialCashoutAvailable: 'Y',
      source: 'f'
    };
    betModelService = {
      getBetTimeString: jasmine.createSpy(),
      createOutcomeName: jasmine.createSpy().and.returnValue(part)
    };
    currency = {};
    currencySymbol = '$';
    cashOutMapIndex = {
      create: jasmine.createSpy(),
    };
    betHistoryMainService = {
      getSortCode: jasmine.createSpy('getSortCode').and.returnValue('Forecast'),
      getBetStatus: jasmine.createSpy(),
      getBetReturnsValue: jasmine.createSpy().and.returnValue({}),
    };
    cashOutErrorMessage = {
      getErrorMessage: jasmine.createSpy(),
    };
    localeService = {
      getString: jasmine.createSpy('getString')
    };

    model = new RegularBet(
      bet,
      betModelService,
      currency,
      currencySymbol,
      cashOutMapIndex,
      betHistoryMainService,
      localeService,
      cashOutErrorMessage,
      cashoutConstants
    );
  });

  it('constructor should set cashout properties', () => {
    expect(model.errorDictionary).toBeDefined();
    expect(model.panelMsg).toBeDefined();
    expect(model.attemptPanelMsg).toBeDefined();
    expect(model.isCashOutUnavailable).toBeFalsy();
    expect(model.isPartialCashOutAvailable).toBeTruthy();
    expect(model.isConfirmed).toBeFalsy();
    expect(model.isPartialActive).toBeFalsy();
    expect(model.isCashOutedBetSuccess).toBeFalsy();
    expect(model.isCashOutBetError).toBeFalsy();
    expect(model.isDisable).toBeFalsy();
    expect(model.isConfirmInProgress).toBeFalsy();
    expect(model.inProgress).toBeFalsy();
    expect(model.isPriceDecrease).toBeFalsy();
  });

  it('handleError', () => {
    model.handleError('price changed', 10, 'decrease');
    expect(model.attemptPanelMsg).toEqual({
      type: 'error',
      msg: 'price changed'
    });
    model.handleError('price changed', 10, 'defaultType');
    expect(model.attemptPanelMsg).toEqual({
      type: 'error',
      msg: 'price changed'
    });
    expect(model.isDisable).toBeTruthy();
    expect(model.inProgress).toBeFalsy();
    expect(model.isCashOutBetError).toBeTruthy();
  });

  it('handleSuccess', fakeAsync(() => {
    model.handleSuccess();
    expect(model.attemptPanelMsg).toEqual({
      type: undefined,
      msg: undefined
    });
    expect(model.isCashOutedBetSuccess).toBeTruthy();
    tick(cashoutConstants.displaySuccess + 100);

    expect(model.totalStatus).toEqual('cashed out');
  }));

  describe('Partial Cashout', () => {
    it('should be available', () => {
      bet.partialCashoutAvailable = 'Y';

      model = new RegularBet(
        bet,
        betModelService,
        currency,
        currencySymbol,
        cashOutMapIndex,
        betHistoryMainService,
        localeService,
        cashOutErrorMessage,
        cashoutConstants
      );

      expect(model.isPartialCashOutAvailable).toBeTruthy();
    });

    it('should not be available', () => {
      bet.partialCashoutAvailable = 'N';

      model = new RegularBet(
        bet,
        betModelService,
        currency,
        currencySymbol,
        cashOutMapIndex,
        betHistoryMainService,
        localeService,
        cashOutErrorMessage,
        cashoutConstants
      );

      expect(model.isPartialCashOutAvailable).toBeFalsy();
    });
  });

  it('setCashoutSuccessState should set cashout success state properties', () => {
    model.cashoutSuccessMessage = '';
    model.setCashoutSuccessState('Cash Out Success');
    expect(model.cashoutSuccessMessage).toEqual('Cash Out Success');
  });

  it('resetCashoutSuccessState should reset cashout success state properties', () => {
    model.cashoutSuccessMessage = 'Cash Out Success';
    model.resetCashoutSuccessState();
    expect(model.cashoutSuccessMessage).toEqual('');
  });

  describe('initializeParts', () => {
    it('should correctly initialize leg parts twice', () => {
      const legItem = {
        part: [
          {
            price: [
              {}
            ],
            outcome: [
              {
                event: {},
                market: {},
                result: {}
              }
            ],
            handicap: [
              {
                formatted: 'Y',
                value: '+1.00'
              }
            ]
          }
        ]
      } as any;
      model.initializeParts(legItem as any);
      expect(legItem.part[0].handicap).toEqual('+1.00');
      model.initializeParts(legItem as any);
      expect(legItem.part[0].handicap).toEqual('+1.00');
    });
    it('should correctly initialize leg parts in case if handicap null', () => {
      const legItem = {
        part: [
          {
            price: [
              {}
            ],
            outcome: [
              {
                event: {},
                market: {},
                result: {}
              }
            ],
            handicap: null
          }
        ]
      } as any;
      model.initializeParts(legItem as any);
      expect(legItem.part[0].handicap).toEqual('');
    });
  });

  describe('setBetProperties', () => {
    it('sortType should be empty', () => {
      bet.source = 'f';
      model.setBetProperties(bet);
      expect(model.sortType).toEqual('');
    });

    it('sortType should be Forecast', () => {
      bet.source = 'SF';
      model.setBetProperties(bet);
      expect(model.sortType).toEqual('Forecast');
    });
  });

  describe('setBybType', () => {
    it('should set bybType (five a side)', () => {
      bet.source = 'f';
      model['setBybType'](bet);
      expect(localeService.getString).toHaveBeenCalledWith('bethistory.bybHeader.fiveASide');
    });

    it('should set bybType', () => {
      bet.source = 'e';
      model['setBybType'](bet);
      expect(localeService.getString).toHaveBeenCalledWith('bethistory.bybHeader.byb');
    });

    it('should not set bybType', () => {
      localeService.getString.calls.reset();
      bet.source = '';
      model['setBybType'](bet);
      expect(localeService.getString).not.toHaveBeenCalled();
    });
  });
});
