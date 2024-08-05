import { cashoutConstants } from 'app/betHistory/constants/cashout.constant';
import { RegularBetBase } from './regular-bet-base.class';
import { fakeAsync, tick } from '@angular/core/testing';

describe('RegularBetBase', () => {
  let model: RegularBetBase;

  let bet,
    betModelService,
    currency,
    currencySymbol,
    cashOutMapIndex,
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
        stakePerLine: 1,
        tokenValue: '0.00'
      },
      cashoutValue: 10,
      partialCashoutAvailable: 'Y'
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
    cashOutErrorMessage = {
      getErrorMessage: jasmine.createSpy(),
    };

    model = new RegularBetBase(
      bet,
      betModelService,
      currency,
      currencySymbol,
      cashOutMapIndex,
      cashOutErrorMessage
    );
    model['setCashoutProperties'](bet as any);
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
    expect(model.hasFreeBet).toBeFalsy();
  });

  describe('isCashedOut', () => {
    it('should return true if cashoutStatus is not BET_SETTLED', () => {
      model.cashoutStatus = 'SOME_STATUS';
      expect(model.isCashedOut).toBeFalsy();
    });
    it('should return true if cashoutStatus is BET_SETTLED', () => {
      model.cashoutStatus = 'BET_SETTLED';
      expect(model.isCashedOut).toBeTruthy();
    });
  });

  describe('constructor should', () => {
    it('set hasFreeBet to false (no stake and tokenValue)', () => {
      bet.stake = undefined;
      bet.tokenValue = undefined;

      model = new RegularBetBase(
        bet,
        betModelService,
        currency,
        currencySymbol,
        cashOutMapIndex,
        cashOutErrorMessage
      );

      expect(model.hasFreeBet).toBeFalsy();
    });

    it('set hasFreeBet to true (stake.tokenValue > 0 and tokenValue)', () => {
      bet.stake = {
        tokenValue: '2.00'
      };

      model = new RegularBetBase(
        bet,
        betModelService,
        currency,
        currencySymbol,
        cashOutMapIndex,
        cashOutErrorMessage
      );

      expect(model.hasFreeBet).toBeTruthy();
    });

    it('set hasFreeBet to true (no stake and bet.tokenValue > 0)', () => {
      bet.stake = undefined;
      bet.tokenValue = '2.00';

      model = new RegularBetBase(
        bet,
        betModelService,
        currency,
        currencySymbol,
        cashOutMapIndex,
        cashOutErrorMessage
      );

      expect(model.hasFreeBet).toBeTruthy();
    });

    it('set hasFreeBet to false (no stake and bet.tokenValue == 0)', () => {
      bet.stake = undefined;
      bet.tokenValue = '0.00';

      model = new RegularBetBase(
        bet,
        betModelService,
        currency,
        currencySymbol,
        cashOutMapIndex,
        cashOutErrorMessage
      );

      expect(model.hasFreeBet).toBeFalsy();
    });
  });

  it('handleError', () => {
    model.handleError('price changed', 10, 'decrease');
    expect(model.attemptPanelMsg).toEqual({
      type: 'error',
      msg: 'price changed'
    });
    model.handleError('price changed', 10, undefined);
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

      model = new RegularBetBase(
        bet,
        betModelService,
        currency,
        currencySymbol,
        cashOutMapIndex,
        cashOutErrorMessage
      );
      model['setCashoutProperties'](bet as any);

      expect(model.isPartialCashOutAvailable).toBeTruthy();
    });

    it('should not be available', () => {
      bet.partialCashoutAvailable = 'N';

      model = new RegularBetBase(
        bet,
        betModelService,
        currency,
        currencySymbol,
        cashOutMapIndex,
        cashOutErrorMessage
      );
      model['setCashoutProperties'](bet as any);

      expect(model.isPartialCashOutAvailable).toBeFalsy();
    });
  });

  describe('isCashoutSuspendedState', () => {
    it('should return true for suspended case', () => {
      model.isCashOutUnavailable = true;
      model.panelMsg = {
        type: 'suspended'
      };
      expect(model.isCashoutSuspendedState).toBeTruthy();
    });

    it('should return false if unavailable but not suspended', () => {
      model.isCashOutUnavailable = true;
      model.panelMsg = {
        type: 'error'
      };
      expect(model.isCashoutSuspendedState).toBeFalsy();
      model.panelMsg = undefined;
      expect(model.isCashoutSuspendedState).toBeFalsy();
    });
  });

  describe('resetCashoutSuspendedState', () => {
    it('should reset cashout suspended state', () => {
      model.isCashOutUnavailable = true;
      model.panelMsg = {
        type: 'suspended'
      };
      expect(model.isCashoutSuspendedState).toBeTruthy();
      model.resetCashoutSuspendedState();
      expect(model.isCashoutSuspendedState).toBeFalsy();
    });
  });

  it('setCashedOutState should set betIsFullyCashedOut property to true', () => {
    expect(model.betIsFullyCashedOut).toBeFalsy();
    model.setCashedOutState();
    expect(model.betIsFullyCashedOut).toBeTruthy();
  });
});
