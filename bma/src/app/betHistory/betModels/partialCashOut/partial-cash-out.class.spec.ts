import { PartialCashOut } from 'app/betHistory/betModels/partialCashOut/partial-cash-out.class';
import { of } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { IBetHistoryBet } from '@app/betHistory/models/bet-history.model';

describe('PartialCashOut', () => {
  let model,
    filtersService,
    localeService,
    cashOutMapService,
    gtm,
    cashOutDataProviderService,
    toolsService,
    cashOutErrorMessage,
    pubsub,
    awsService,
    clientUserAgentService,
    liveServConnectionService,
    deviceService;

  const betMock = {
    cashoutValue: {
      status: 'BET_SETTLED',
      amount: '1.00'
    }
  } as IBetHistoryBet;

  const cashoutBet = {
    bet: {
      potentialPayout: '2',
      partialCashout: {
        available: 'Y'
      },
      betTermsChange: [{
        potentialPayout: '2'
      }],
      cashoutValue: '2',
      stake: {
        amount: '2',
        stakePerLine: '2'
      }
    }
  };

  beforeEach(() => {
    liveServConnectionService = {
      isConnected: jasmine.createSpy('isConnected').and.returnValue(true)
    };
    deviceService = {
      parsedUA: { ua: 'someuserAgent'}
    };
    filtersService = {
      currencyPipe: {
        transform: jasmine.createSpy()
      }
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.callFake(x => x)
    };
    cashOutMapService = {};
    gtm = jasmine.createSpyObj('gtmSpy', ['push']);
    cashOutDataProviderService = {
      getBet: jasmine.createSpy().and.returnValue(of(null))
    };
    toolsService = {
      roundDown: jasmine.createSpy().and.returnValue(1)
    };
    cashOutErrorMessage = {
      getErrorMessage: jasmine.createSpy('getErrorMessage')
    };
    pubsub = {
      publish: jasmine.createSpy('publishSpy'),
      API: { UPDATE_CASHOUT_BET: 'UPDATE_CASHOUT_BET' }
    };
    awsService = jasmine.createSpyObj('awsServiceSpy', ['addAction']);
    clientUserAgentService = jasmine.createSpyObj('clientUserAgentServiceSpy', ['getId']);

    model = new PartialCashOut(filtersService, localeService, cashOutMapService,
      gtm, cashOutDataProviderService, toolsService, cashOutErrorMessage,
      pubsub, awsService, liveServConnectionService, clientUserAgentService, deviceService);
    model.bet = betMock;
    model.cashOutObj = {
      attemptPanelMsg: { type: '', msg: '' },
      panelMsg: {},
      setCashoutSuccessState: jasmine.createSpy('setCashoutSuccessState'),
      handleSuccess: jasmine.createSpy('handleSuccess'),
      setCashedOutState: jasmine.createSpy('setCashedOutState')
    };
  });

  describe('handleSuccess', () => {
    beforeEach(() => {
      cashOutDataProviderService.getBet.and.returnValue(of(null));
    });

    it('should call proper methods', () => {
      model.handleSuccess(cashoutBet);
      expect(model.cashOutObj.panelMsg).toEqual({} as any);
      expect(model.cashOutObj.setCashoutSuccessState).toHaveBeenCalledWith('bethistory.partialCashOutSuccess');
      expect(model.cashOutObj.isPartialActive).toBeFalsy();
      expect(model.cashOutObj.partialCashOutPercentage).toEqual(100);
    });

    it('should call proper methods for bet array', () => {
      model.handleSuccess({
        bet: [{
          potentialPayout: '2',
          partialCashout: {
            available: 'Y'
          },
          betTermsChange: [{
            potentialPayout: '2'
          }],
          cashoutValue: {
            amount: '2'
          },
          stake: {
            amount: '2',
            stakePerLine: '2'
          }
        }]
      });
      expect(model.cashOutObj.panelMsg).toEqual({} as any);
      expect(model.cashOutObj.setCashoutSuccessState).toHaveBeenCalledWith('bethistory.partialCashOutSuccess');
      expect(model.cashOutObj.isPartialActive).toBeFalsy();
      expect(model.cashOutObj.partialCashOutPercentage).toEqual(100);
    });

    it('should send GTM info and call getCashoutBet', () => {
      model.cashOutObj = <any>{
        betId: '123',
        setCashoutSuccessState: jasmine.createSpy('setCashoutSuccessState'),
        attemptPanelMsg: { type: '', msg: '' },
        panelMsg: {}
      };
      model.bet = <any>{
        cashoutValue: {
          status: 'BET',
          amount: '1.00',
        },
        isCashedOut: 'Y',
        isSettled: 'N'
      };
      model.handleSuccess(cashoutBet);

      expect(gtm.push).toHaveBeenCalledTimes(1);
    });

    describe('should update partial cashout availability', () => {
      it('if it is enabled in response', () => {
        model.handleSuccess(cashoutBet);

        expect(model.cashOutObj).toEqual(jasmine.objectContaining({
          isPartialCashOutAvailable: true,
          cashoutValue: '2',
          stake: '2',
          stakePerLine: '2'
        }));
      });

      it('if it is not enabled in response', () => {
        cashoutBet.bet.partialCashout.available = 'N';
        model.handleSuccess(cashoutBet);

        expect(model.cashOutObj).toEqual(jasmine.objectContaining({
          isPartialCashOutAvailable: false
        }));
      });

      it('should handle updatePartialCashOutBet when no amount in cashoutValue', () => {
        model.handleSuccess({
          bet: {
            potentialPayout: '2',
            partialCashout: {
              available: 'Y'
            },
            betTermsChange: [{
              potentialPayout: '2'
            }],
            cashoutValue: 'CASHOUT_SELN_SUSPENDED',
            stake: {
              amount: '2',
              stakePerLine: '2'
            }
          }
        });

        expect(model.cashOutObj).toEqual(jasmine.objectContaining({
          isConfirmed: false
        }));
      });

      it('in case when Bet was Fully cashed out, setCashedOutState should be called', () => {
        model.cashOutObj.setCashedOutState = jasmine.createSpy('cashOutObj.setCashedOutState');
        model.handleSuccess(null);

        expect(model.cashOutObj.setCashedOutState).toHaveBeenCalled();
      });
    });
  });

  it('isCashOutSuccessful', () => {
    model.cashOutObj = <any>{
      betId: '123',
      setCashoutSuccessState: jasmine.createSpy('setCashoutSuccessState'),
      attemptPanelMsg: { type: '', msg: '' },
      panelMsg: {}
    };
    model.bet = <any>{
      cashoutValue: {
        status: 'BET',
        amount: '1.00',
      },
      isCashedOut: 'Y',
      isSettled: 'N'
    };

    expect(model.isCashOutSuccessful()).toBeTruthy();
  });

  describe('checkPartialCashOutStatus', () => {
    it('should get error from getErrorMessage for bet worth nothing case', () => {
      model['checkPartialCashOutStatus']({
        cashoutStatus: 'cashoutStatus',
        cashoutValue: '0.00',

      } as any);
      expect(cashOutErrorMessage.getErrorMessage).toHaveBeenCalledWith(jasmine.anything());
    });
    it('should get error from getErrorMessage for suspended selection', () => {
      model['checkPartialCashOutStatus']({
        cashoutStatus: 'cashoutStatus',
        cashoutValue: 'CASHOUT_SELN_SUSPENDED',
      } as any);
      expect(cashOutErrorMessage.getErrorMessage).toHaveBeenCalledWith(jasmine.anything());
    });
    it('should NOT get error from getErrorMessage for available cashout', () => {
      model['checkPartialCashOutStatus']({
        cashoutStatus: 'cashoutStatus',
        cashoutValue: {
          amount: '1.0',
        }
      } as any);
      expect(cashOutErrorMessage.getErrorMessage).not.toHaveBeenCalled();
    });
  });

  it('clearErrorStateAfter', fakeAsync(() => {
    model.cashOutObj.isPartialActive = true;
    model.cashOutObj.isCashOutBetError = true;

    model.cashOutObj.attemptPanelMsg = {};
    model.cashOutObj.partialCashOutPercentage = 100;
    model['clearErrorStateAfter'](10);

    tick(10);

    expect(model.cashOutObj.isCashOutBetError).toBeFalsy();
    expect(model.cashOutObj.isPartialActive).toBeFalsy();
    expect(model.cashOutObj.partialCashOutPercentage).toEqual(100);
    expect(pubsub.publish).toHaveBeenCalledWith('UPDATE_CASHOUT_BET', model.cashOutObj);
  }));

  it('handleError', () => {
    model['clearErrorStateAfter'] = jasmine.createSpy();
    model['formAttemptPanelObj'] = jasmine.createSpy();
    model['sendGTMFailureCashout'] = jasmine.createSpy();
    model['updatePartialCashOutBet'] = jasmine.createSpy();
    model.awsCashOut = jasmine.createSpy();
    model['handleError']('test');

    expect(model.cashOutObj.isCashOutBetError).toBeTruthy();
    expect(model.clearErrorStateAfter).toHaveBeenCalledWith(5000);
    expect(model['formAttemptPanelObj']).toHaveBeenCalledWith('test', null);
    expect(model['sendGTMFailureCashout']).toHaveBeenCalledWith('partial');
    expect(model.awsCashOut).toHaveBeenCalledWith('PartialCashOut=>makeCashOut=>Error', 'error', {
      errorCode: undefined,
      errorDictionary: 'test'
    });
    expect(model['updatePartialCashOutBet']).toHaveBeenCalled();
  });

  describe('error handling should updatePartialCashoutBet for', () => {
    let bet;
    beforeEach(() => {
      bet = { bet: { betId: '123' } };
      spyOn(model, 'updatePartialCashOutBet');
      spyOn(model, 'handleError').and.callThrough();
    });
    it('cashOutDefault', () => {
      model.cashOutDefault(bet);
    });
    it('cashOutChanged', () => {
      model.cashOutChanged(bet);
    });

    afterEach(() => {
      expect(model.handleError).toHaveBeenCalledWith('bethistory.cashoutBet.cashoutAttemptErrors.DEFAULT', bet);
      expect(model.updatePartialCashOutBet).toHaveBeenCalledWith(bet);
    });
  });

  describe('#updatePartialCashOutBet', () => {
    it('should call updatePartialCashOutBet when no internet connection', () => {
      model['updatePartialCashOutBet']('FAILED_CASHOUT_REQUEST');

      expect(model.cashOutObj.betTermsChange).toBeUndefined();
    });
  });

  it('should handle change cashout', () => {
    model.cashOutChanged({}, {});
    expect(model.cashOutObj.isCashOutBetError).toBeTruthy();
  });
});
