import { fakeAsync, tick } from '@angular/core/testing';
import { of, of as observableOf, throwError } from 'rxjs';

import { CashOutCore } from 'app/betHistory/betModels/cashOutCore/cash-out-core.class';
import { IBetHistoryBet, ICashoutError } from '@app/betHistory/models/bet-history.model';
import { ICashoutBet } from '@app/betHistory/models/bet-history-bet.model';

class Test extends CashOutCore {
  isCashOutSuccessful(): boolean {
    return true;
  }

  handleSuccess(res): void {
  }

  cashOutChanged(res): void {
  }

  cashOutDefault(errorOpt: any): void {
  }
}

describe('CashOutCore', () => {
  let model: CashOutCore;

  let
    filterService,
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

  beforeEach(() => {
    filterService = {};
    liveServConnectionService = {
      isConnected: jasmine.createSpy('isConnected').and.returnValue(true)
    };
    deviceService = {
      parsedUA: { ua: 'someuserAgent'}
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.callFake(x => x)
    };
    cashOutMapService = {};
    gtm = {
      push: jasmine.createSpy('push')
    };
    cashOutDataProviderService = {
      makeReadBetRequest: jasmine.createSpy('makeReadBetRequest').and.returnValue(observableOf({})),
      makeCashOutRequest: jasmine.createSpy('makeCashOutRequest').and.returnValue(of({ partialCashOutAmount: 2.22}))
    };
    toolsService = {};
    cashOutErrorMessage = {};
    pubsub = {
      publish: jasmine.createSpy('publish'),
      publishSync: jasmine.createSpy('publishSync'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        CASHOUT_COUNTDOWN_TIMER: 'CASHOUT_COUNTDOWN_TIMER'
      }
    };
    awsService = {
      addAction: jasmine.createSpy('addAction')
    };
    clientUserAgentService = {
      getId: jasmine.createSpy('getId')
    };

    model = new Test(
      filterService,
      localeService,
      cashOutMapService,
      gtm,
      cashOutDataProviderService,
      toolsService,
      cashOutErrorMessage,
      pubsub,
      awsService,
      liveServConnectionService,
      clientUserAgentService,
      deviceService
    );

    model.bet = betMock;
  });

  it('constructor', () => {
    expect(model).toBeTruthy();
    expect(model.errorDictionary).toEqual('bethistory.cashoutBet.cashoutAttemptErrors');
  });

  describe('#getPotentialPayout', () =>  {
    it('should call getPotentialPayout with betTermsChange without potentialPayout value property', () => {
      const result = model['getPotentialPayout']({ betTermsChange: [{
        potentialPayout: '0.1'
      }]} as any);

      expect(result).toEqual('0.1');
    });

    it('should call getPotentialPayout betTermsChange potentialPayout value property', () => {
      const result = model['getPotentialPayout']({
        betTermsChange: [{
          potentialPayout: {
            value: '0.1'
          }
        }]
      } as any);

      expect(result).toEqual('0.1');
    });

    it('should call getPotentialPayout with potentialPayout', () => {
      const result = model['getPotentialPayout']({
        betTermsChange: [{
          potentialPayout: ''
        }],
        potentialPayout: '0.1'
      } as any);

      expect(result).toEqual('0.1');
    });

    it('should call getPotentialPayout without betTermsChange', () => {
      const result = model['getPotentialPayout']({
        potentialPayout: '0.1'
      } as any);

      expect(result).toEqual('0.1');
    });
  });

  describe('@cashOutPending', () => {
    let pendingBetRes;

    beforeEach(() => {
      pendingBetRes = { betError: { cashoutDelay: 3, cashoutBetDelayId: '123' } };
      model['makeReadBet'] = jasmine.createSpy('makeReadBet');
    });

    it('should emit CASHOUT_COUNTDOWN_TIMER', () => {
      model['cashOutPending'](pendingBetRes);

      expect(pubsub.publishSync).toHaveBeenCalledWith('CASHOUT_COUNTDOWN_TIMER', 3);
    });

    it('should execute makeReadBet after the delay', fakeAsync(() => {
      pendingBetRes.betError.cashoutDelay = 0.001;
      model['cashOutPending'](pendingBetRes);

      tick(2);

      expect(model['makeReadBet']).toHaveBeenCalled();
    }));

    it('should update response id', () => {
      model['cashOutPending'](pendingBetRes);

      expect(model.responseId).toBe(pendingBetRes.betError.cashoutBetDelayId);
    });
  });

  describe('getErrorMsgFromDictionary', () => {
    it('should return exact error from errors dictionary if provided error code', () => {
      model.errorCode = 'ERROR_CODE';
      expect(model['getErrorMsgFromDictionary']()).toEqual('bethistory.cashoutBet.cashoutAttemptErrors.ERROR_CODE');
    });
    it('should return default error from errors dictionary if no error code', () => {
      model.errorCode = '';
      expect(model['getErrorMsgFromDictionary']()).toEqual('bethistory.cashoutBet.cashoutAttemptErrors.DEFAULT');
    });

    it('should return default error from errors dictionary if KEY_NOT_FOUND', () => {
      model.errorCode = 'ERROR_NOT_MAPPED';
      localeService.getString.and.returnValue('KEY_NOT_FOUND');

      model['getErrorMsgFromDictionary']();

      expect(localeService.getString).toHaveBeenCalledWith('bethistory.cashoutBet.cashoutAttemptErrors.DEFAULT');
    });
  });

  it('#sendGTMSuccessCashout should send gtm data', () => {
    model.cashOutObj = {
      panelMsg: {},
      gtmCashoutValue: '5.5'
    } as any;
    model['sendGTMSuccessCashout'](model.cashoutConstants.cashOutType.PARTIAL);

    expect(gtm.push).toHaveBeenCalledWith('trackEvent', {
      eventLabel: 'success',
      successMessage: 'bethistory.partialcashoutsuccess',
      eventCategory: 'cash out',
      eventAction: 'attempt',
      location: undefined,
      cashOutOffer: 5.5,
      oddsBoost: 'no',
      cashOutType: 'partial'
    });
    expect(localeService.getString).toHaveBeenCalledWith('bethistory.partialCashOutSuccess');

    model['sendGTMSuccessCashout'](model.cashoutConstants.cashOutType.FULL);
    expect(localeService.getString).toHaveBeenCalledWith('bethistory.fullCashOutSuccess');
  });

  describe('updateCashOutObjPayout', () => {
    it('should change cashOutObj payload values', () => {
      const mockPayout = {
        bonus: 'bonus',
        refunds: 'refunds',
        winnings: '11.3',
        potential: '20.00',
        legType: ''
      };
      model.cashOutObj = {
        cashoutValue: '5',
        potentialPayout: '10.3',
        bonus: '',
        refund: ''
      } as ICashoutBet;
      model.bet = {
        payout: [mockPayout]
      } as IBetHistoryBet;
      model['updateCashOutObjPayout']();

      expect(model.cashOutObj.cashoutValue).toEqual(mockPayout.winnings);
      expect(model.cashOutObj.potentialPayout).toEqual(mockPayout.potential);
      expect(model.cashOutObj.bonus).toEqual(mockPayout.bonus);
      expect(model.cashOutObj.refund).toEqual(mockPayout.refunds);
    });

    it('should not change cashOutObj payload values when payload values are undefined', () => {
      const mockCashOutObj = {
        cashoutValue: '5',
        potentialPayout: '10.3',
        bonus: 'bonus',
        refund: 'refund'
      } as ICashoutBet;
      model.cashOutObj = mockCashOutObj;
      model.bet = {
        payout: [{} as any]
      } as IBetHistoryBet;
      model['updateCashOutObjPayout']();

      expect(model.cashOutObj.cashoutValue).toEqual(mockCashOutObj.cashoutValue);
      expect(model.cashOutObj.potentialPayout).toEqual(mockCashOutObj.potentialPayout);
      expect(model.cashOutObj.bonus).toEqual(mockCashOutObj.bonus);
      expect(model.cashOutObj.refund).toEqual(mockCashOutObj.refund);
    });

    it('should not change cashOutObj payload values when bet payload is undefined', () => {
      const mockCashOutObj = {
        cashoutValue: '5',
        potentialPayout: '10.3',
        bonus: 'bonus',
        refund: 'refund'
      } as ICashoutBet;
      model.cashOutObj = mockCashOutObj;
      model.bet = {
        payout: undefined
      } as IBetHistoryBet;
      model['updateCashOutObjPayout']();

      expect(model.cashOutObj.cashoutValue).toEqual(mockCashOutObj.cashoutValue);
      expect(model.cashOutObj.potentialPayout).toEqual(mockCashOutObj.potentialPayout);
      expect(model.cashOutObj.bonus).toEqual(mockCashOutObj.bonus);
      expect(model.cashOutObj.refund).toEqual(mockCashOutObj.refund);
    });
  });

  describe('getErrorCode', () => {
    it('should return error code in case it received in subErrorCode property', () => {
      const errorCode = model['getErrorCode']({
        betError: {
          subErrorCode: 'SOME_ERROR_CODE'
        }
      } as any);
      expect(errorCode).toEqual('SOME_ERROR_CODE');
      expect(model.errorCode).toEqual('SOME_ERROR_CODE');
    });
    it('should return error code in case it received in cashoutValue property', () => {
      const errorCode = model['getErrorCode']({
        bet: [
          {
            cashoutValue: {
              amount: 'SOME_ERROR_CODE_2'
            }
          }
        ]
      } as any);
      expect(errorCode).toEqual('SOME_ERROR_CODE_2');
      expect(model.errorCode).toEqual('SOME_ERROR_CODE_2');
    });
    it('should return null in case cashoutValue is number', () => {
      const errorCode = model['getErrorCode']({
        bet: [
          {
            cashoutValue: {
              amount: '5.12'
            }
          }
        ]
      } as any);
      expect(errorCode).toEqual(null);
      expect(model.errorCode).toEqual(null);
    });
    it('should return null if there is no error code', () => {
      const errorCode = model['getErrorCode'](null);
      expect(errorCode).toEqual(null);
      expect(model.errorCode).toEqual(null);
    });
  });
  describe('makeReadBet', () => {
    it('should makeReadBet Request',  fakeAsync(() => {
      cashOutDataProviderService.makeReadBetRequest.and.returnValue(observableOf({
        bet: [{
          cashoutValue: {
            amount: 'SOME_ERROR_CODE_2'
          }
        }]
      } as any));
      model.responseId = '1';
      model.reqData = {};
      model['makeReadBet']();
      tick();
      expect(cashOutDataProviderService.makeReadBetRequest).toHaveBeenCalledWith('1', {});
    }));
  });
  describe('cashOutRequestHandler', () => {
    it('should set isCashOutBetError property to true', () => {
      model['cashOutObj'] = {} as any;

      model['cashOutRequestHandler']({
        bet: [{
          cashoutValue: {
            amount: 'SOME_ERROR_CODE_2'
          }
        }]
      } as any);
      expect(model['cashOutObj'].isCashOutBetError).toBeTruthy();
    });
    it('should`t set isCashOutBetError property to true if there is no error', () => {
      model['cashOutObj'] = {} as any;

      model['cashOutRequestHandler']({
        bet: [{
          cashoutValue: {
            amount: '5.12'
          }
        }]
      } as any);
      expect(model['cashOutObj'].isCashOutBetError).toBeFalsy();
    });
    it('should call cashOutDefault if there is no error code', () => {
      model['cashOutObj'] = {} as any;

      spyOn(model, 'isCashOutSuccessful').and.returnValue(false);
      spyOn(model, 'cashOutDefault');

      model['cashOutRequestHandler']({
        bet: undefined
      } as any);
      expect(model.cashOutDefault).toHaveBeenCalledWith(null);
    });
  });

  describe('readBetRequestHandler', () => {
    it('should set isCashOutBetError property to true', () => {
      model['cashOutObj'] = {} as any;
      spyOn(model, 'isCashOutSuccessful').and.returnValue(false);
      model['readBetRequestHandler']({
        bet: [{
          cashoutValue: {
            amount: 'SOME_ERROR_CODE_2'
          }
        }]
      } as any);
      expect(model['cashOutObj'].isCashOutBetError).toBeTruthy();
    });
    it('should`t set isCashOutBetError property to true if there is no error', () => {
      model['cashOutObj'] = {} as any;

      spyOn(model, 'isCashOutSuccessful').and.returnValue(false);
      model['readBetRequestHandler']({
        bet: [{
          cashoutValue: {
            amount: '5.12'
          }
        }]
      } as any);
      expect(model['cashOutObj'].isCashOutBetError).toBeFalsy();
    });
  });

  it('awsCashOut', () => {
    const actionName = 'name',
      error = {errorCode: 'code', errorDictionary: 'description'} as ICashoutError;
      status = 'error';
    model['awsCashOut'](actionName, status, error);
    expect(awsService.addAction).toHaveBeenCalledWith(actionName, jasmine.objectContaining({
      liveServConnectionStatus: 'active',
      userAgent: 'someuserAgent',
      cashoutStatus: 'BET_SETTLED',
      cashoutValue: '1.00',
      errorCode: error.errorCode,
      errorDictionary: error.errorDictionary
    }));
  });

  it('awsCashOut when cashoutValue is string', () => {
    const actionName = 'name',
      error = {errorCode: 'code', errorDictionary: 'description'} as ICashoutError;
    status = 'error';
    model.bet = { cashoutValue: '1.00' } as IBetHistoryBet;

    model['awsCashOut'](actionName, status, error);
    expect(awsService.addAction).toHaveBeenCalledWith(actionName, jasmine.objectContaining({
      liveServConnectionStatus: 'active',
      userAgent: 'someuserAgent',
      cashoutStatus: null,
      cashoutValue: '1.00',
      errorCode: error.errorCode,
      errorDictionary: error.errorDictionary
    }));
  });

  it('awsCashOut when no bet', () => {
    const actionName = 'name',
      error = {errorCode: 'code', errorDictionary: 'description'} as ICashoutError;
    status = 'error';
    model.bet = undefined;
    model.id = '123';

    model['awsCashOut'](actionName, status, error);
    expect(awsService.addAction).toHaveBeenCalledWith(actionName, jasmine.objectContaining({
      liveServConnectionStatus: 'active',
      userAgent: 'someuserAgent',
      errorCode: error.errorCode,
      errorDictionary: error.errorDictionary,
      betId: '123'
    }));
  });

  it('awsCashOut should not pass error', () => {
    const actionName = 'name';
    status = 'success';
    model.bet = { cashoutValue: '1.00' } as IBetHistoryBet;

    model['awsCashOut'](actionName, status);
    expect(awsService.addAction).toHaveBeenCalledWith(actionName, jasmine.objectContaining({
      liveServConnectionStatus: 'active',
      userAgent: 'someuserAgent',
      cashoutStatus: null,
      cashoutValue: '1.00',
      errorCode: undefined,
      errorDictionary: undefined
    }));
  });

  it('should makeCashOut', () => {
    const reqDataMock = {partialCashOutAmount: '2.22'};
    const currentBetMock = {
      betId: 'betIdMock'
    } as any;
    const locationMock = 'locationMock';

    model.makeCashOut(reqDataMock, currentBetMock, locationMock);

    expect(model.id).toEqual(currentBetMock.betId);
    expect(model.reqData).toEqual(reqDataMock);
    expect(model.cashOutObj).toEqual(currentBetMock);
    expect(model.cashoutDelay).toEqual(0);
    expect(model.withCashoutDelay).toEqual(false);
  });

  it('should makeCashOut error scenario', () => {
    cashOutDataProviderService.makeCashOutRequest = jasmine.createSpy('makeCashOutRequest').and.returnValue(throwError({}));
    const reqDataMock = {partialCashOutAmount: '2.22'};
    const currentBetMock = {
      betId: 'betIdMock',
      betType: 'TRX'
    } as any;
    const locationMock = 'locationMock';

    spyOn(model, 'cashOutDefault');

    model.makeCashOut(reqDataMock, currentBetMock, locationMock);
    expect(model.cashOutDefault).toHaveBeenCalled();
  });

  it('should makeCashOut when there is no partialCashout amount', () => {
    cashOutDataProviderService.makeCashOutRequest = jasmine.createSpy('makeCashOutRequest').and.returnValue(of({}));
    const reqDataMock = null;
    const currentBetMock = {
      betId: 'betIdMock'
    } as any;
    const locationMock = 'locationMock';

    spyOn(model, 'cashOutDefault');

    model.makeCashOut(reqDataMock, currentBetMock, locationMock);
    expect(pubsub.publish).not.toHaveBeenCalled();
  });

  it('should makeCashOut when betType is SGL and not call publish', () => {
    cashOutDataProviderService.makeCashOutRequest = jasmine.createSpy('makeCashOutRequest').and.returnValue(of({}));
    const reqDataMock = null;
    const currentBetMock = {
      betId: 'betIdMock',
      betType: 'SGL'
    } as any;
    const locationMock = 'locationMock';
    model.makeCashOut(reqDataMock, currentBetMock, locationMock);
    expect(pubsub.publish).not.toHaveBeenCalled();
  });
  it('should call getCashOutGtmObject', () => {
    model.betLocation = '';
    model.cashOutObj = {
      gtmCashoutValue: 1,
      partialCashOutPercentage: 20,
      betType: 'L15',
      availableBonuses: {
        availableBonus: []
      }
    } as any;
    spyOn<any>(model, 'getPartialCashoutOffer').and.returnValue(1);
    const resp = model['getCashOutGtmObject']('Partial');
    expect(resp.cashOutType).toEqual('Partial');
  });
  it('should call getCashOutGtmObject with isCashoutBetBoosted yes', () => {
    model.betLocation = '';
    model.cashOutObj = {
      gtmCashoutValue: 1,
      partialCashOutPercentage: 20,
      betType: 'L15',
      availableBonuses: {
        availableBonus: []
      }
    } as any;
    spyOn<any>(model, 'isCashoutBetBoosted').and.returnValue('yes');
    spyOn<any>(model, 'getPartialCashoutOffer').and.returnValue(1);
    const resp = model['getCashOutGtmObject']('Partial');
    expect(resp.cashOutType).toEqual('Partial');
  });

  describe('isFilteredError', () => {
    let updateObj;
    beforeEach(() => {
      updateObj = {};
    });
    describe('should return true', () => {
      it('if updateObj.cashoutStatus contains one of the cashout status constants', () => {
        updateObj.cashoutStatus = 'SELN_SUSP ';
        updateObj.cashoutValue = 123;
      });
      it('if updateObj.cashoutValue contains one of the cashout value constants', () => {
        updateObj.cashoutStatus = undefined;
        updateObj.cashoutValue = 'CASHOUT_SELN_SUSPENDED';
      });
      it('if updateObj.cashoutValue.amount contains one of the cashout value constants', () => {
        updateObj.cashoutStatus = '';
        updateObj.cashoutValue = 'CASHOUT_SELN_SUSPENDED';
      });
      afterEach(() => {
        expect((model as any).isFilteredError(updateObj)).toEqual(true);
      });
    });

    describe('should return false', () => {
      it('if updateObj.cashoutStatus and updateObj.cashoutValue does not contain any of the cashout constants', () => {
        updateObj.cashoutStatus = 'status';
        updateObj.cashoutValue = 123;
      });
      it('if updateObj.cashoutStatus is undefined and updateObj.cashoutValue does not contain any of the cashout constants', () => {
        updateObj.cashoutStatus = undefined;
        updateObj.cashoutValue = 123;
      });
      it('if updateObj.cashoutStatus is undefined and updateObj.cashoutValue.amount does not contain any of the cashout constants', () => {
        updateObj.cashoutStatus = undefined;
        updateObj.cashoutValue = { amount: 123 };
      });
      afterEach(() => {
        expect((model as any).isFilteredError(updateObj)).toEqual(false);
      });
    });
  });
});
