import { FullCashOut } from 'app/betHistory/betModels/fullCashOut/full-cash-out.class';
import { of } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { IBetHistoryBet } from '@app/betHistory/models/bet-history.model';

describe('FullCashOut', () => {
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
    cashoutBetsStreamService,
    liveServConnectionService,
    deviceService;


  const betMock = {
    cashoutValue: {
      status: 'BET_SETTLED',
      amount: '1.00'
    }
  } as IBetHistoryBet;

  beforeEach(() => {
    filtersService = {};
    liveServConnectionService = {
      isConnected: jasmine.createSpy('isConnected').and.returnValue(true)
    };
    deviceService = {
      parsedUA: { ua: 'someuserAgent'}
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.callFake(x => x)
    };
    cashOutMapService = {
      isEmptyObj: jasmine.createSpy(),
      cashoutBetsMap: {
        deleteBets: jasmine.createSpy(),
        mapState: {
          isSpinnerActive: false,
          isEmpty: false
        }
      }
    };
    gtm = jasmine.createSpyObj('gtmSpy', ['push']);
    cashOutDataProviderService = jasmine.createSpyObj('cashOutDataProviderServiceSpy', ['getBet']);
    toolsService = {};
    cashOutErrorMessage = {
      getErrorMessage: jasmine.createSpy('getErrorMessage')
    };
    pubsub = {
      publish: jasmine.createSpy('publishSpy'),
      API: {
        UPDATE_CASHOUT_BET: 'UPDATE_CASHOUT_BET',
        BETS_COUNTER_CASHOUT_BET: 'BETS_COUNTER_CASHOUT_BET'
      }
    };
    awsService = jasmine.createSpyObj('awsServiceSpy', ['addAction']);
    clientUserAgentService = jasmine.createSpyObj('clientUserAgentServiceSpy', ['getId']);
    cashoutBetsStreamService = {
      getCashoutBet: jasmine.createSpy('getCashoutBet').and.returnValue(of({})),
      updateCashedOutBet: jasmine.createSpy('updateCashedOutBet')
    };

    model = new FullCashOut(filtersService, localeService, cashOutMapService,
      gtm, cashOutDataProviderService, toolsService, cashOutErrorMessage,
      pubsub, awsService, liveServConnectionService, clientUserAgentService, deviceService, cashoutBetsStreamService);
    model.bet = betMock;

    model.cashOutObj = {
      handleError: jasmine.createSpy(),
      attemptPanelMsg: { type: '', msg: '' },
      setCashoutSuccessState: jasmine.createSpy('setCashoutSuccessState'),
      handleSuccess: jasmine.createSpy('handleSuccess'),
      setCashedOutState: jasmine.createSpy('setCashedOutState'),
      isDisable : false,
      isCashOutBetError :false
    };
  });

  describe('cashOutDefault', () => {
    let isCashOutBetError;
    let attemptPanelMsg;
    let isDisable;

    beforeEach(() => {
      cashOutDataProviderService.getBet.and.returnValue(of(null));
      model.cashOutObj.handleError.and.callFake(function() {
        isCashOutBetError = true;
        attemptPanelMsg = { type: 'type', msg: 'msg' };
        isDisable = true;
      });
    });

    it('should hide error message and reset cashout state after the timeout', fakeAsync(() => {
      model.cashOutDefault();
      expect(model.cashOutObj).toEqual(jasmine.objectContaining({
        isCashOutBetError: false,
        attemptPanelMsg: { type: '', msg: '' },
        isDisable: false
      }));

      tick(5000);
      expect(model.cashOutObj).toEqual(jasmine.objectContaining({
        isCashOutBetError: false,
        attemptPanelMsg: {},
        isDisable: false
      }));
      expect(pubsub.publish).toHaveBeenCalledWith('UPDATE_CASHOUT_BET', jasmine.any(Object));
      expect(pubsub.publish).toHaveBeenCalledTimes(2); // before and after message appears
    }));
  });

  describe('updateAfterError', () => {
    it('should get error from  getErrorMessage for bet worth nothing case', () => {
      model['updateAfterError']([{
        cashoutStatus: 'cashoutStatus',
        cashoutValue: '0.00'
      } as any]);
      expect(cashOutErrorMessage.getErrorMessage).toHaveBeenCalledWith(jasmine.anything());
    });
  });

  describe('handleSuccess', () => {
    it('should call proper methods', () => {
      model.handleSuccess();
      expect(model.cashOutObj.panelMsg).toEqual({
        type: 'success',
        msg: ''
      } as any);
      expect(model.cashOutObj.setCashoutSuccessState).toHaveBeenCalledWith('bethistory.fullCashOutSuccess');
      expect(model.cashOutObj.setCashedOutState).toHaveBeenCalled();
      expect(pubsub.publish).toHaveBeenCalledWith('UPDATE_CASHOUT_BET', jasmine.any(Object));
      expect(pubsub.publish).toHaveBeenCalledWith('BETS_COUNTER_CASHOUT_BET');
      expect(cashoutBetsStreamService.updateCashedOutBet).toHaveBeenCalled();
    });
  });

  it('handleError with errorCode', () => {
    model['resetErrorStateAfter'] = jasmine.createSpy();
    model['sendGTMFailureCashout'] = jasmine.createSpy();
    model['updateAfterError'] = jasmine.createSpy();
    model.awsCashOut = jasmine.createSpy('awsCashOut');
    model.errorCode = '123';
    model['handleError'](null, '10', 'error');

    expect(model.cashOutObj.handleError).toHaveBeenCalledWith('bethistory.cashoutBet.cashoutAttemptErrors.123', '10', 'error');
    expect(pubsub.publish).toHaveBeenCalledWith('UPDATE_CASHOUT_BET', model.cashOutObj);
    expect(model['resetErrorStateAfter']).toHaveBeenCalledWith(5000);
    expect(model['sendGTMFailureCashout']).toHaveBeenCalledWith('full');
    expect(model.awsCashOut).toHaveBeenCalledWith('FullCashOut=>makeCashOut=>Error', 'error', {
      errorCode: '123',
      errorDictionary: 'bethistory.cashoutBet.cashoutAttemptErrors.123'
    });
    expect(cashoutBetsStreamService.getCashoutBet).toHaveBeenCalledWith([model.cashOutObj.betId]);
    expect(model['updateAfterError']).toHaveBeenCalledWith({});
  });

  it('handleError with errorOpt', () => {
    model['resetErrorStateAfter'] = jasmine.createSpy();
    model['sendGTMFailureCashout'] = jasmine.createSpy();
    model['updateAfterError'] = jasmine.createSpy();
    model.awsCashOut = jasmine.createSpy('awsCashOut');
    model['handleError'](null, '10', 'error');

    expect(model.cashOutObj.handleError).toHaveBeenCalledWith('bethistory.cashoutBet.cashoutAttemptErrors.DEFAULT', '10', 'error');
    expect(pubsub.publish).toHaveBeenCalledWith('UPDATE_CASHOUT_BET', model.cashOutObj);
    expect(model['resetErrorStateAfter']).toHaveBeenCalledWith(5000);
    expect(model['sendGTMFailureCashout']).toHaveBeenCalledWith('full');
    expect(model.awsCashOut).toHaveBeenCalledWith('FullCashOut=>makeCashOut=>Error', 'error', {
      errorCode: null,
      errorDictionary: 'bethistory.cashoutBet.cashoutAttemptErrors.DEFAULT'
    });
    expect(cashoutBetsStreamService.getCashoutBet).toHaveBeenCalledWith([model.cashOutObj.betId]);
    expect(model['updateAfterError']).toHaveBeenCalledWith({});
  });
});
