import { CashoutBet } from 'app/betHistory/betModels/cashoutBet/cashout-bet.class';

describe('CashoutBet', () => {
  let model,
    bet,
    betModelService,
    currency,
    currencySymbol,
    cashOutMapIndex,
    cashOutErrorMessage;

  beforeEach(() => {
    bet = {
      cashoutValue: '0.09'
    };
    betModelService = jasmine.createSpyObj('betModelServiceSpy', ['getBetTimeString', 'getPotentialPayout']);
    currency = {};
    currencySymbol = {};
    cashOutMapIndex = {};
    cashOutErrorMessage = jasmine.createSpyObj('cashOutErrorMessageSpy', ['getErrorMessage']);
  });

  describe('#constructor', () => {
    beforeEach(() => {
      model = new CashoutBet(bet, betModelService, currency, currencySymbol, cashOutMapIndex, cashOutErrorMessage);
    });

    it('should set cashout properties', () => {
      expect(model.errorDictionary).toEqual({ decrease: jasmine.any(Function), defaultType: jasmine.any(Function) });
      expect(model.partialCashOutPercentage).toEqual(100);
      expect(model.isCashOutUnavailable).toEqual(false);
      expect(model.isConfirmed).toEqual(false);
      expect(model.isPartialActive).toEqual(false);
      expect(model.isCashOutedBetSuccess).toEqual(false);
      expect(model.isCashOutBetError).toEqual(false);
      expect(model.isDisable).toEqual(false);
      expect(model.isConfirmInProgress).toEqual(false);
      expect(model.inProgress).toEqual(false);
      expect(model.isPriceDecrease).toEqual(false);
      expect(model.panelMsg).toEqual({ type: undefined, msg: undefined });
      expect(model.attemptPanelMsg).toEqual({ type: undefined, msg: undefined });
      expect(model.isPartialCashOutAvailable).toEqual(false);
    });

    it('should have errorDictionary.decrease method update bet object', () => {
      const betObj = {};
      model.errorDictionary.decrease(betObj, '12.345');
      expect(betObj).toEqual({
        cashoutValue: 12.345,
        isDisable: false,
        isPriceDecrease: true,
        isConfirmed: false
      });
    });
  });
});
