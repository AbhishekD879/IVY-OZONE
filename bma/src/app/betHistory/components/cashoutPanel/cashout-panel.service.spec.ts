import { CashoutPanelService } from '@app/betHistory/components/cashoutPanel/cashout-panel.service';
import { CashoutBet } from '@app/betHistory/betModels/cashoutBet/cashout-bet.class';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('CashoutPanelService', () => {
  let service: CashoutPanelService,
    cashOutMapService,
    cashOutService,
    localeService,
    windowRef,
    toolsService,
    pubsub,
    editMyAccaService,
    storageService;

  let bet: any;

  beforeEach(() => {
    bet = {
      panelMsg: { msg: 'msg' },
      attemptPanelMsg: { msg: 'msg' },
      valueToCashout: 'valueToCashout',
      isPartialCashOutAvailable: true,
      isPartialActive: undefined,
      id: '159',
      resetCashoutSuccessState: jasmine.createSpy('resetCashoutSuccessState'),
      cashoutValue: 12.53,
      partialCashOutPercentage: 50
    };
    cashOutMapService = {
      createCashoutBetsMap: jasmine.createSpy(),
      cashoutBetsMap: {
        mapState: {
          isUserLogOut: undefined
        }
      }
    };
    cashOutService = {
      createCashoutBetsMap: jasmine.createSpy(),
      createFullCashOut: jasmine.createSpy().and.returnValue({
        makeCashOut: () => {}
      }),
      createPartialCashOut: jasmine.createSpy().and.returnValue({
        makeCashOut: () => {}
      })
    };
    localeService = jasmine.createSpyObj(['getString']);
    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get').and.returnValue([{"eventId":"11","betIds":[3]},{"eventId":"2","betIds":[4]}])
    };
    pubsub = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    localeService = {
      getString: jasmine.createSpy().and.returnValues('confirmCashOut', 'cashOutBetSuspended', 'partialCashout', 'cashout')
    };
    pubsub = {
      publish: jasmine.createSpy(),
      API: {
        UPDATE_CASHOUT_BET: 'UPDATE_CASHOUT_BET',
        CASHOUT_COUNTDOWN_TIMER: 'CASHOUT_COUNTDOWN_TIMER'
      }
    };
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
        clearTimeout: jasmine.createSpy('clearTimeout')
      }
    } as any;
    toolsService = jasmine.createSpyObj('toolsService', ['getOwnDeepProperty', 'roundDown']);
    editMyAccaService = {
      removeSavedAcca: jasmine.createSpy('removeSavedAcca')
    };

    service = new CashoutPanelService(
      cashOutMapService as any,
      cashOutService as any,
      localeService as any,
      windowRef as any,
      toolsService as any,
      pubsub as any,
      editMyAccaService as any,
      storageService as any
      );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('getButtonState', () => {
    describe('for success-related conditions', () => {
      beforeEach(() => {
        bet = {
          panelMsg: {type: 'success'},
          isCashOutUnavailable: false,
          isCashOutBetError: false,
          type: 'not-a-placedBetsWithoutCashoutPossibility'
        };
      });
      it('should return "success" if all are met', () => {
        expect(service.getButtonState(bet)).toEqual('success');
      });

      describe('if any is not met', () => {
        it('should return "base" (bet.panelMsg.type does not equal "success")', () => {
          bet.panelMsg.type = 'not-a-success';
          expect(service.getButtonState(bet)).toEqual('base');
        });
        it('should return "unavailable" (bet.isCashOutUnavailable is true)', () => {
          bet.isCashOutUnavailable = true;
          expect(service.getButtonState(bet)).toEqual('unavailable');
        });
        it('should return "error" (bet.isCashOutBetError is true)', () => {
          bet.isCashOutBetError = true;
          expect(service.getButtonState(bet)).toEqual('error');
        });
        it('should return "base" (bet.type is "placedBetsWithoutCashoutPossibility")', () => {
          bet.type = 'placedBetsWithoutCashoutPossibility';
          expect(service.getButtonState(bet)).toEqual('base');
        });

        it('isBetInProgress', () => {
          bet.panelMsg.type = '';
          bet.inProgress = true;
          expect(service.getButtonState(bet)).toEqual('progress');
        });

        it('isConfirmInProgress', () => {
          bet.panelMsg.type = '';
          bet.isConfirmInProgress = true;
          expect(service.getButtonState(bet)).toEqual('confirm');
        });

        it('isPartialActive', () => {
          bet.panelMsg.type = '';
          bet.isPartialActive = true;
          expect(service.getButtonState(bet)).toEqual('partial');
        });
      });
    });
  });

  it('getStateConfig', () => {
    const stateConfig = {
      error: {
        text: '',
        value: jasmine.any(Function)
      },
      success: {
        text: '',
        value: jasmine.any(Function)
      },
      progress: {
        text: '',
        value: jasmine.any(Function)
      },
      confirm: {
        text: 'confirmCashOut',
        value: jasmine.any(Function)
      },
      unavailable: {
        text: 'cashOutBetSuspended',
        value: jasmine.any(Function)
      },
      partial: {
        text: 'partialCashout',
        value: jasmine.any(Function)
      },
      base: {
        text: 'cashout',
        value: jasmine.any(Function)
      },
    };
    expect(service.getStateConfig(bet)).toEqual(stateConfig);
  });

  it('isPartialAvailable', () => {
    expect(service.isPartialAvailable(bet)).toEqual(true);
  });

  describe('getCashOutValueWithPartial', () => {
    beforeEach(() => {
      bet = {
        partialCashOutPercentage: 100,
        cashoutValue: '5.00'
      } as CashoutBet;
    });

    it('should return cashout value if percentage is 100', () => {
      expect(service['getCashOutValueWithPartial'](bet)).toEqual(bet.cashoutValue);
    });

    it('should return cashout value if percentage is not 100', () => {
      toolsService.roundDown.and.callFake(v => v);
      bet.partialCashOutPercentage = 50;
      expect(service['getCashOutValueWithPartial'](bet)).toEqual('2.50');
    });
  });

  describe('doCashOutParamsSetting', () => {
    beforeEach(() => {
      toolsService.roundDown.and.callFake(v => v);
      bet = {
        betId: '123',
        cashoutValue: '5.00',
        currency: 'GBP',
        partialCashOutPercentage: 100,
        isDisable: true,
        valueToCashout: null,
      } as CashoutBet;
    });

    it('should return cashout params for full cashout', () => {
      const result = service['doCashOutParamsSetting'](bet);

      expect(result.partialData).toEqual({
        partialCashOutAmount: null,
        partialCashOutPercentage: null
      });
      expect(result.reqData).toEqual({
        betId: bet.betId,
        cashOutAmount: bet.cashoutValue,
        currency: bet.currency
      });
      expect(result.isPartial).toBeFalsy();
      expect(bet.isDisable).toEqual(false);
      expect(bet.valueToCashout).toEqual('5.00');
    });

    it('should return cashout params for full cashout', () => {
      bet.partialCashOutPercentage = 0;
      const result = service['doCashOutParamsSetting'](bet);

      expect(result.isPartial).toBeFalsy(false);
      expect(bet.valueToCashout).toEqual('0.00');
    });

    it('should return cashout params for partial cashout', () => {
      bet.partialCashOutPercentage = 50;
      const result = service['doCashOutParamsSetting'](bet);

      expect(result.partialData).toEqual({
        partialCashOutAmount: 2.5,
        partialCashOutPercentage: bet.partialCashOutPercentage
      });
      expect(result.isPartial).toBeTruthy();
      expect(bet.isDisable).toEqual(false);
      expect(bet.valueToCashout).toEqual('2.50');
    });
  });

  describe('runStrategy', () => {
    const currentBet = {
        inProgress: false,
        event: [11],
        betId: 3
      },
      reqData = {},
      partialData = {},
      location = {};

    it('when partial cashout', () => {
      const isPartial = true;
      service['runStrategy']({currentBet, reqData, partialData, isPartial, location});

      expect(currentBet.inProgress).toEqual(true);
      expect(cashOutService.createPartialCashOut).toHaveBeenCalled();
    });

    it('when full cashout', () => {
      const isPartial = false;
      service['runStrategy']({currentBet, reqData, partialData, isPartial, location});

      expect(currentBet.inProgress).toEqual(true);
      expect(cashOutService.createFullCashOut).toHaveBeenCalled();
    });
  });

  describe('triggerCashOut', () => {
    const cashoutData =  {} as any,
      isPartial = true,
      reqData = {
        reqData: 'reqData'
      },
      partialData = {
        partialData: 'partialData'
      },
      location = 'location',
      currentBet = {
      isConfirmInProgress: true,
      isDisable: false
    } as any;

    beforeEach(() => {
      spyOn<any>(service, 'doCashOutParamsSetting').and.returnValue({partialData, reqData, isPartial});
      spyOn<any>(service, 'runStrategy');
      spyOn<any>(service, 'timeOutCashout');
    });

    it('should check full cashout or partial', () => {
      cashOutMapService.cashoutBetsMap.mapState.isUserLogOut = false;
      service['timer'] = 12;
      service['triggerCashOut'](cashoutData, location, currentBet);

      expect(currentBet.isConfirmInProgress).toEqual(false);
      expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalledWith(12);
      expect(currentBet.isDisable).toEqual(true);
      expect(service['runStrategy']).toHaveBeenCalledWith({currentBet, reqData, partialData, isPartial, location});
    });

    it('should timeout confirm cashout', () => {
      currentBet.isConfirmInProgress = false;
      service['triggerCashOut'](cashoutData, location, currentBet);

      expect(currentBet.isConfirmInProgress).toEqual(true);
      expect(windowRef.nativeWindow.clearTimeout).not.toHaveBeenCalled();
      expect(service['timeOutCashout']).toHaveBeenCalledWith(currentBet);
      expect(service['runStrategy']).not.toHaveBeenCalled();
    });

    it('shouldn\'t run strategy when user is LogOut', () => {
      cashOutMapService.cashoutBetsMap.mapState.isUserLogOut = true;

      expect(service['runStrategy']).not.toHaveBeenCalled();
      expect(service['timeOutCashout']).not.toHaveBeenCalled();
    });
  });

  describe('setPartialState', () => {
    let timeoutCbMap;

    beforeEach(() => {
      spyOn(service as any, 'cancelCashout').and.callThrough();
      timeoutCbMap = {};
      windowRef.nativeWindow.setTimeout.and.callFake((cb, time) => {
        if (timeoutCbMap[time]) {
          timeoutCbMap[time].push(cb);
        } else {
          timeoutCbMap[time] = [cb];
        }
      });
    });
    describe('when toggling on', () => {
      beforeEach(() => {
        service.setPartialState(bet, true);
      });
      describe('before starting animation', () => {
        it('should set bet animating property', () => {
          expect(bet.animating).toEqual(true);
        });
        it('should set partialCashOutPercentage to 0', () => {
          expect(bet.partialCashOutPercentage).toEqual(0);
        });
        it('should publish pubsub UPDATE_CASHOUT_BET', () => {
          expect(pubsub.publish).toHaveBeenCalledWith('UPDATE_CASHOUT_BET', bet);
          expect(pubsub.publish).toHaveBeenCalledBefore(windowRef.nativeWindow.setTimeout);
        });
        afterEach(() => {
          expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 500);
          expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledTimes(1);
        });
      });

      describe('after starting 1st animation phase and before 2nd phase', () => {
        beforeEach(() => {
          pubsub.publish.calls.reset();
          windowRef.nativeWindow.setTimeout.calls.reset();
          timeoutCbMap[500][0]();
        });
        it('should set partialCashOutPercentage to 50', () => {
          expect(bet.partialCashOutPercentage).toEqual(50);
        });
        it('should set bet animating property', () => {
          expect(bet.animating).toEqual(true);
        });
        it('should publish pubsub UPDATE_CASHOUT_BET', () => {
          expect(pubsub.publish).toHaveBeenCalledWith('UPDATE_CASHOUT_BET', bet);
          expect(pubsub.publish).toHaveBeenCalledBefore(windowRef.nativeWindow.setTimeout);
        });

        afterEach(() => {
          expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 500);
          expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledTimes(1);
        });
      });

      describe('after starting 2nd animation phase', () => {
        beforeEach(() => {
          timeoutCbMap[500][0]();
          pubsub.publish.calls.reset();
          windowRef.nativeWindow.setTimeout.calls.reset();
          timeoutCbMap[500][1]();
        });

        it('should unset bet animating property', () => {
          expect(bet.animating).toEqual(false);
        });
        it('should publish pubsub UPDATE_CASHOUT_BET', () => {
          expect(pubsub.publish).toHaveBeenCalledWith('UPDATE_CASHOUT_BET', bet);
        });

        afterEach(() => {
          expect(windowRef.nativeWindow.setTimeout).not.toHaveBeenCalled();
        });
      });

      afterEach(() => {
        expect(bet.isPartialActive).toEqual(true);
      });
    });

    describe('when toggling off', () => {
      beforeEach(() => {
        (service as any).timer = 16;
        service.setPartialState(bet, false);
      });

      it('should not call setTimeout', () => {
        expect(windowRef.nativeWindow.setTimeout).not.toHaveBeenCalled();
      });
      it('should not set bet animating property', () => {
        expect(bet.animating).not.toBeDefined();
      });
      it('should update bet partialCashOutPercentage to 100', () => {
        expect(bet.partialCashOutPercentage).toEqual(100);
      });
      it('should clear timeout', () => {
        expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalledWith(16);
      });

      describe('should call cancelCashout method', () => {
        beforeEach(() => {
          expect((service as any).cancelCashout).toHaveBeenCalledWith(bet);
        });

        it('should call pubsub methods', () => {
          expect(pubsub.publish).not.toHaveBeenCalledBefore((service as any).cancelCashout);
          expect(pubsub.publish.calls.allArgs()).toEqual([
            ['UPDATE_CASHOUT_BET', bet], ['CASHOUT_COUNTDOWN_TIMER', null]
          ]);
        });
        it('should update bet properties', () => {
          expect(bet.isDisable).toEqual(false);
          expect(bet.isConfirmInProgress).toEqual(false);
        });
      });

      afterEach(() => {
        expect(bet.isPartialActive).toEqual(false);
      });
    });
  });

  it('should timeOutCashout', () => {
    const betItem = {};
    service['timeOutCashout'](<any>betItem);
    expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalled();
  });

  describe('doCashOut', () => {
    it('reset cashout success state and removed saved acca state', () => {
      const betCopy = Object.assign(bet);
      betCopy.isPartialActive = true;
      service.doCashOut([], 'myBets', betCopy, 'full');
      expect(betCopy.gtmCashoutValue).toEqual(betCopy.cashoutValue);
      expect(editMyAccaService.removeSavedAcca).toHaveBeenCalledWith('159');
      expect(betCopy.resetCashoutSuccessState).toHaveBeenCalledWith();
    });
  });
});
