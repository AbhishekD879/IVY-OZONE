import { fakeAsync, tick } from '@angular/core/testing';

import { CashoutSectionService } from '@app/betHistory/services/cashOutSection/cash-out-section.service';
import { CashoutBet } from '@app/betHistory/betModels/cashoutBet/cashout-bet.class';
import { ICashOutData } from '@app/betHistory/models/cashout-section.model';
import { cashoutConstants } from '../../constants/cashout.constant';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { IMatchCmtryData } from '../../models/bet-history.model';
import { MYBETS_AREAS } from '@app/betHistory/constants/bet-leg-item.constant';
import { of } from 'rxjs';

describe('CashoutSectionService', () => {
  let service: CashoutSectionService;

  let cashOutMapService,
    userService,
    cashOutLiveServeUpdatesService,
    pubSubService,
    cashOutLiveUpdatesSubscribeService,
    betModelService,
    cashOutMapIndexService,
    betHistoryMainService,
    cashOutErrorMessage,
    localeService,
    windowRefService,
    handleVarReasoningUpdatesService,
    cmsService,
    betReceiptService,
    storageService;

  const part = {
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
  };

  beforeEach(() => {
    cashOutMapService = {
      cashoutBetsMap: {
        1000: {
          outcome: [],
          market: [],
          event: []
        },
        5000: {
          outcome: [],
          market: [],
          event: []
        },
      }
    };
    userService = {username: 'test'};
    cashOutLiveServeUpdatesService = {};
    cashOutLiveUpdatesSubscribeService = {
      addWatchForRegularBets: jasmine.createSpy('addWatchForRegularBets'),
      addWatchForPlacedEventsOnly: jasmine.createSpy('addWatchForPlacedEventsOnly'),
    };
    betModelService = {
      getBetTimeString: jasmine.createSpy('getBetTimeString'),
      createOutcomeName: jasmine.createSpy('createOutcomeName').and.returnValue([part]),
      getPotentialPayout: jasmine.createSpy('getPotentialPayout'),
    };
    cashOutMapIndexService = {
      create: jasmine.createSpy()
    };
    betHistoryMainService = {
      getSortCode: jasmine.createSpy(),
      getBetStatus: jasmine.createSpy(),
      getBetReturnsValue: jasmine.createSpy().and.returnValue(5),
    };
    cashOutErrorMessage = {
      getErrorMessage: jasmine.createSpy()
    };

    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('locale test string')
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    windowRefService = { nativeWindow: {
      clearInterval: jasmine.createSpy(),
      setTimeout: jasmine.createSpy('setTimeout')}
    };
    handleVarReasoningUpdatesService = {
      sendRequestForLastMatchFact: jasmine.createSpy('sendRequestForLastMatchFact'),
      removeHandlers: jasmine.createSpy('removeHandlers')
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        MybetsMatchCommentary: {
          enabled: true
        }
      }))
    };
    betReceiptService = {
      luckyAllWinnersBonus: jasmine.createSpy('luckyAllWinnersBonus').and.returnValue('£2.35'),
      isAllWinnerOnlyApplicable: jasmine.createSpy('isAllWinnerOnlyApplicable').and.returnValue(true)
    };
    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get')
    };

    service = new CashoutSectionService(
      cashOutMapService,
      userService,
      cashOutLiveServeUpdatesService,
      pubSubService,
      cashOutLiveUpdatesSubscribeService,
      betModelService,
      cashOutMapIndexService,
      betHistoryMainService,
      cashOutErrorMessage,
      localeService,
      windowRefService,
      handleVarReasoningUpdatesService,
      cmsService,
      storageService,
      betReceiptService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect(service['freeBetMsg']).toEqual('locale test string');
    expect(service['betTokenMsg']).toEqual('locale test string');
  });

  describe('removeCashoutItemWithTimeout', () => {
    let betsMap, options;

    beforeEach(() => {
      betsMap = {
        '123': {
          betId: 123,
          event: ['123'],
          market: [],
          outcome: []
        },
        'bar': {
          betId: 159,
          event: [],
          someBetDataBar: 'someBetDataBar'
        }
      } as any;

      options = {
        betId: '123'
      };
    });

    it('should remove cashout item', fakeAsync(() => {
      service.removeCashoutItemWithTimeout(betsMap, options).subscribe(() => {
        expect(betsMap).toEqual({
          'bar': {
            betId: 159,
            event: [],
            someBetDataBar: 'someBetDataBar',
          }
        } as any);
        expect(pubSubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS_UPDATES_MS', {
          event: ['123'],
          market: [],
          outcome: []
        });
      });
      tick(cashoutConstants.tooltipTime + 1);
    }));

    it('shouldn`t call UNSUBSCRIBE if ll items are matched for at lease one bet in the list', fakeAsync(() => {
      betsMap = {
        '123': {
          betId: 123,
          event: ['111'],
          market: ['MKT111'],
          outcome: ['OUTCOME111']
        },
        '222': {
          betId: 222,
          event: ['222', '111'],
          market: ['333', 'MKT111'],
          outcome: ['OUTCOME222', 'OUTCOME111']
        }
      } as any;
      service.removeCashoutItemWithTimeout(betsMap, options).subscribe(() => {
        expect(pubSubService.publish).not.toHaveBeenCalled();
      });
      tick(cashoutConstants.tooltipTime + 1);
    }));

    it('should call UNSUBSCRIBE only for items which are not duplicate in other bets', fakeAsync(() => {
      betsMap = {
        '123': {
          betId: 123,
          event: ['555', '111', '222', '333'],
          market: ['MKT555', 'MKT111', 'MKT222', 'MKT333'],
          outcome: ['OUTCOME555', 'OUTCOME111', 'OUTCOME222', 'OUTCOME333', 'qwerty']
        },
        '222': {
          betId: 222,
          event: ['222', '111'],
          market: ['333', 'MKT111'],
          outcome: ['OUTCOME222', 'OUTCOME111']
        },
        '333': {
          betId: 333,
          event: ['222', '141324123411'],
          market: ['MKT222', 'MKT13241234123411'],
          outcome: ['OUTCOME222', 'OUTCO234123412ME111']
        }
      } as any;
      service.removeCashoutItemWithTimeout(betsMap, options).subscribe(() => {
        expect(pubSubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS_UPDATES_MS', {
          event: ['555', '333'],
          market: ['MKT555', 'MKT333'],
          outcome: ['OUTCOME555', 'OUTCOME333', 'qwerty']
        });
      });
      tick(cashoutConstants.tooltipTime + 1);
    }));

    it('should not remove if bet not exists in map before removal', fakeAsync(() => {
      const betsMapCopy = Object.assign({}, betsMap);
      options.betId = '321';

      service.removeCashoutItemWithTimeout(betsMap, options).subscribe(() => {
        expect(betsMap).toEqual(betsMapCopy);
        expect(pubSubService.publish).not.toHaveBeenCalled();
      });
      tick(cashoutConstants.tooltipTime + 1);
    }));

    it('should remove if bet matches given status', fakeAsync(() => {
      betsMap['123'].cashoutStatus = 'BET_SETTLED';
      options.isRegularBets = true;
      const betsMapCopy = Object.assign({}, betsMap);

      service.removeCashoutItemWithTimeout(betsMap, options).subscribe(() => {
        expect(betsMap).not.toEqual(betsMapCopy);
        expect(betsMap['123']).toBeUndefined();
        expect(pubSubService.publish).toHaveBeenCalled();
      });

      tick(cashoutConstants.tooltipTime + 1);
    }));

    it('should remove if bet matches given status BET_CASHED_OUT', fakeAsync(() => {
      betsMap['123'].cashoutStatus = 'BET_CASHED_OUT';
      options.isRegularBets = true;
      const betsMapCopy = Object.assign({}, betsMap);

      service.removeCashoutItemWithTimeout(betsMap, options).subscribe(() => {
        expect(betsMap).not.toEqual(betsMapCopy);
        expect(betsMap['123']).toBeUndefined();
        expect(pubSubService.publish).toHaveBeenCalled();
      });

      tick(cashoutConstants.tooltipTime + 1);
    }));
  });

  describe('@updateBet', () => {
    const betItem = {
      betId: '123',
      cashoutValue: 23
    };

    it('should update cashout bet', () => {
      const bets = [{
        eventSource: {
          betId: '123',
          cashoutValue: 1
        },
        location: 'tst'
      }];
      service.updateBet(betItem as CashoutBet, bets as ICashOutData[]);

      expect(bets[0].eventSource.cashoutValue).toBe(23);
    });

    it('should Not update cashout bet', () => {
      const bets = [{
        eventSource: {
          betId: '456',
          cashoutValue: 1
        },
        location: 'tst'
      }];
      service.updateBet(betItem as CashoutBet, bets as ICashOutData[]);

      expect(bets[0].eventSource.cashoutValue).toBe(1);
    });
  });

  it('createDataForRegularBets', () => {
    const map = service.createDataForRegularBets([
      {
        id: '12345',
        betType: {
          code: 'a'
        },
        leg: [{
          legType: {
            code: 'a'
          },
          part: [part]
        }],
        stake: {
          value: 1
        }
      }
    ]);

    expect(map).toBeDefined();
  });

  it('registerController', () => {
    service.registerController(cashoutConstants.controllers.MY_BETS_CTRL);
    expect(pubSubService.publish).toHaveBeenCalledWith('CASHOUT_CTRL_STATUS', {
      ctrlName: cashoutConstants.controllers.MY_BETS_CTRL,
      isDestroyed: false
    });
    expect(service['liveServeSubscribers'].length).toBe(1);
  });

  describe('removeListeners', () => {
    it('removeListeners ', () => {
      service.registerController(cashoutConstants.controllers.MY_BETS_CTRL);
      service.registerController(cashoutConstants.controllers.REGULAR_BETS_CTRL);
      service.removeListeners(cashoutConstants.controllers.MY_BETS_CTRL);
      expect(pubSubService.publish).not.toHaveBeenCalledWith('UNSUBSCRIBE_LS_UPDATES_MS');
    });

    it('removeListeners UNSUBSCRIBE_LS_UPDATES_MS', () => {
      service.registerController(cashoutConstants.controllers.MY_BETS_CTRL);
      service.registerController(cashoutConstants.controllers.REGULAR_BETS_CTRL);
      service.removeListeners(cashoutConstants.controllers.MY_BETS_CTRL);
      service.removeListeners(cashoutConstants.controllers.REGULAR_BETS_CTRL);
      expect(pubSubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS_UPDATES_MS');
    });
  });

  describe('removeErrorMessageWithTimeout', () => {
    let bets: any;

    beforeEach(() => {
      bets = [{
        eventSource: {
          betId: 1,
          isCashOutUnavailable: false,
          isPartialCashOutAvailable: true,
          isCashOutBetError: true,
          type: ''
        }
      }];
    });

    it('should not change bet type if bet not matched with passed bets', fakeAsync(() => {
      const options = {
        betId: 2,
        prevCashoutStatus: ''
      };

      service.removeErrorMessageWithTimeout(bets, options);
      tick(5001);

      expect(bets[0].eventSource.isCashOutUnavailable).toBeFalsy();
      expect(bets[0].eventSource.isPartialCashOutAvailable).toBeTruthy();
      expect(bets[0].eventSource.type).toBeFalsy();
    }));

    it('should change bet type if there was previous cashout status and no change timer yet', fakeAsync(() => {
      const options = {
        betId: 1,
        prevCashoutStatus: 'Y'
      };

      service.removeErrorMessageWithTimeout(bets, options);

      expect(bets[0].eventSource.isCashOutUnavailable).toBeTruthy();
      expect(bets[0].eventSource.isPartialCashOutAvailable).toBeFalsy();
      expect(bets[0].eventSource.type).toEqual('placedBetsWithoutCashoutPossibility');
    }));

    it('should change bet type in timeout if there was no previous cashout status', fakeAsync(() => {
      const options = {
        betId: 1,
        prevCashoutStatus: ''
      };

      service.removeErrorMessageWithTimeout(bets, options);
      expect(bets[0].eventSource.type).toBeFalsy();
      tick(5001);

      expect(bets[0].eventSource.isCashOutUnavailable).toBeTruthy();
      expect(bets[0].eventSource.isPartialCashOutAvailable).toBeFalsy();
      expect(bets[0].eventSource.isCashOutBetError).toBeFalsy();
      expect(bets[0].eventSource.type).toEqual('placedBetsWithoutCashoutPossibility');
    }));

    it('should change bet type in timeout if there was previous cashout status and change timeout', fakeAsync(() => {
      const options = {
        betId: 1,
        prevCashoutStatus: 'Y'
      };

      service.sortNotFilered = 1;
      service.removeErrorMessageWithTimeout(bets, options);
      expect(bets[0].eventSource.type).toBeFalsy();
      tick(5001);

      expect(bets[0].eventSource.isCashOutUnavailable).toBeTruthy();
      expect(bets[0].eventSource.isPartialCashOutAvailable).toBeFalsy();
      expect(bets[0].eventSource.isCashOutBetError).toBeFalsy();
      expect(bets[0].eventSource.type).toEqual('placedBetsWithoutCashoutPossibility');
    }));
  });

  describe('createTempDataForMyBets', () => {
    it('not bets', () => {
      expect(service.createTempDataForMyBets(null, null)).toEqual({});
    });

    it('cashout bets', () => {
      cashOutMapService.cashoutBetsMap['2'] = {};

      const result = service.createTempDataForMyBets([
        { id: '1', isSettled: true },
        { id: '2', isSettled: false }
      ] as any, null);

      expect(result).toEqual({
        '2': cashOutMapService.cashoutBetsMap['2']
      });
    });

    it('placed bets', () => {
      cashOutMapService.cashoutBetsMap['1'] = {};
      service.getMyBetsIds = jasmine.createSpy('getMyBetsIds');

      const cashoutIds: any = [{ id: '1' }];

      const placedBets: any = [
        { betId: '1' },
        { betId: '2', cashoutValue: 'BET_CASHED_OUT' },
        { betId: '3', settled: 'Y' },
        { betId: '4', cashoutValue: '0.90' },
        { betId: '5', isCashOutUnavailable: true }
      ];

      const result = service.createTempDataForMyBets(cashoutIds, placedBets);

      expect(result).toEqual({
        '1': {},
        '4': jasmine.objectContaining({ betId: '4' }),
        '5': jasmine.objectContaining({ betId: '5', type: 'placedBetsWithoutCashoutPossibility' })
      } as any);

      expect(service.getMyBetsIds).toHaveBeenCalledTimes(1);
      expect(cashOutLiveUpdatesSubscribeService.addWatchForPlacedEventsOnly).toHaveBeenCalledTimes(1);
    });

    it('should skip not mapped bets', () => {
      const ids = <any>[
        {
          id: 1000,
          isSettled: false
        },
        {
          id: 5000,
          isSettled: false
        },
        {
          id: 10000,
          isSettled: false
        }
      ];
      const result = service.createTempDataForMyBets(ids, []);

      expect(result['1000']).toEqual(jasmine.any(Object));
      expect(result['5000']).toEqual(jasmine.any(Object));
      expect(result['10000']).toBeUndefined();
    });
  });

  describe('isCashoutError', () => {
    it('should return true for cashout unavaileble and cashout error case', () => {
      expect(service.isCashoutError({ isCashOutBetError: true, isCashOutUnavailable: false } as any)).toBeTruthy();
      expect(service.isCashoutError({ isCashOutBetError: false, isCashOutUnavailable: true } as any)).toBeTruthy();
      expect(service.isCashoutError({ isCashOutBetError: false, isCashOutUnavailable: false, hasFreeBet: true } as any)).toBeTruthy();
    });
    it('should return false for cashout unavaileble and cashout error case', () => {
      expect(service.isCashoutError({ isCashOutBetError: false, isCashOutUnavailable: false } as any)).toBeFalsy();
    });
  });

  describe('getCashoutError', () => {
    it('should attemptPanelMsg or panelMsg if exists', () => {
      expect(service.getCashoutError({ attemptPanelMsg: { msg: 'attemptPanelMsg' } } as any)).toEqual('attemptPanelMsg');
      expect(service.getCashoutError({ panelMsg: { msg: 'panelMsg' } } as any)).toEqual('panelMsg');
    });

    it('should return free bet notification', () => {
      expect(service.getCashoutError({ hasFreeBet: true, isCashOutUnavailable: false, } as any)).toEqual('locale test string');
    });

    it('should return empty value', () => {
      expect(service.getCashoutError({} as any)).toBeFalsy();
      expect(service.getCashoutError({ hasFreeBet: false } as any)).toBeFalsy();
      expect(service.getCashoutError({ hasFreeBet: true, isCashOutUnavailable: true } as any)).toBeFalsy();
    });
    it('should return bet token notification', () => {
       localeService.getString.and.returnValue('BETPACK');
        expect(service.getCashoutError({ tokenType: 'Bet Pack', isCashOutUnavailable: false } as any)).toEqual('locale test string');
        expect(service.getCashoutError({ tokenType: 'Bet Pack', isCashOutUnavailable: true } as any)).toBeFalsy();
      });
  });

  it('emitMyBetsCounterEvent', () => {
    const bets = [{}] as any;
    service.emitMyBetsCounterEvent(bets);
    expect(pubSubService.publish).toHaveBeenCalledWith('EVENT_MY_BETS_COUNTER', 1);
  });
  describe('#getLeaderBoardConfig', () => {
    it('should return false if 1stcondition is false', () => {
      const response = service.getLeaderBoardConfig(null);
      expect(response).toBe(null);
    });
    it('should return false if 2ndcondition is false', () => {
      const response = service.getLeaderBoardConfig({} as any);
      expect(response).toBeUndefined();
    });
    it('should return true if condition satifies', () => {
      const response = service.getLeaderBoardConfig({ myBetsSection: true} as any);
      expect(response).toBe(true);
    });
  });
  describe('#matchCommentaryDataUpdate', () => {
    it('should make isMatchCmtryDataAvailable true when var-data is availble if eventID is availble in array', () => {
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'Ba', playerName: 'Ab', varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      const bets = [{ eventSource: { event: ['12345'], leg: [{ myBetsAreas: { [MYBETS_AREAS.WIDGET]: { isMatchCmtryDataAvailable: true }},eventEntity: { id: 12345 }, part: [{ outcome: [{}] }] }] } }] as any;
      service['matchCommentaryDataUpdate'](bets,varDataUpdate,MYBETS_AREAS.WIDGET);
      expect(bets[0].eventSource.leg[0].matchCmtryDataUpdate).toBeDefined();
      expect(bets[0].eventSource.leg[0].matchCmtryDataUpdate.varIconData).toBeDefined();
      expect(bets[0].eventSource.leg[0].matchCmtryDataUpdate.teamName).toEqual('BA');
      expect(bets[0].eventSource.leg[0].matchCmtryDataUpdate.playerName).toEqual('AB');
      expect(bets[0].eventSource.leg[0].matchCmtryDataUpdate.varIconData.svgId).toEqual('Var_Goal');
      expect(bets[0].eventSource.leg[0].matchCmtryDataUpdate.varIconData.description).toEqual('Goal');
      expect(bets[0].eventSource.leg[0].myBetsAreas[MYBETS_AREAS.WIDGET].isMatchCmtryDataAvailable).toBeTrue();
    });
    it('should not make vardataAvailable undefined if eventID is not includes in array and in leg and do not assign data', () => {
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      const bets = [{ eventSource: { event: ['1234'], leg: [{ eventEntity: { id: 1234 } }] } }] as any;
      service['matchCommentaryDataUpdate'](bets,varDataUpdate);
      expect(bets[0].eventSource.leg[0].matchCmtryDataUpdate).toBeUndefined();
      expect(bets[0].eventSource.leg[0].myBetsAreas).toBeUndefined();
    });
    it('should call clearInterval if leg.varTimeInterval is defined and leg.isvardataAvailable', fakeAsync(() => {
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      const bets = [{ eventSource: { event: ['12345'], leg: [{ myBetsAreas: { [MYBETS_AREAS.WIDGET]: { isMatchCmtryDataAvailable: true }},eventEntity: { id: 12345 }, matchCmtryTimeInterval: 10 ,isVarDataAvailable: true}] } }] as any;
      service['matchCommentaryDataUpdate'](bets,varDataUpdate);
      expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalledWith(10);
    }));
    it('should not call clearInterval if leg.varTimeInterval is undefined ', fakeAsync(() => {
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      const bets = [{ eventSource: { event: ['12345'], leg: [{  myBetsAreas: { [MYBETS_AREAS.WIDGET]: { isMatchCmtryDataAvailable: true }},eventEntity: { id: 12345 }, varTimeInterval: 0,isVarDataAvailable:false}] } }] as any;
      service['matchCommentaryDataUpdate'](bets,varDataUpdate,MYBETS_AREAS.WIDGET);
      expect(windowRefService.nativeWindow.clearInterval).not.toHaveBeenCalled();
    }));
    it('should not call clearInterval if leg.varTimeInterval is undefined leg.myBetsAreas is undefined', fakeAsync(() => {
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      const bets = [{ eventSource: { event: ['12345'], leg: [{ eventEntity: { id: 12345 }, varTimeInterval: 0,isVarDataAvailable:false}] } }] as any;
      service['matchCommentaryDataUpdate'](bets,varDataUpdate,MYBETS_AREAS.WIDGET);
      expect(windowRefService.nativeWindow.clearInterval).not.toHaveBeenCalled();
    }));
    it('should not call clearInterval if leg.varTimeInterval is defined leg.myBetsAreas is undefined', fakeAsync(() => {
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      const bets = [{ eventSource: { event: ['12345'], leg: [{ eventEntity: { id: 12345 }, varTimeInterval: 1,isVarDataAvailable:false}] } }] as any;
      service['matchCommentaryDataUpdate'](bets,varDataUpdate,MYBETS_AREAS.WIDGET);
      expect(windowRefService.nativeWindow.clearInterval).not.toHaveBeenCalled();
    }));
    it('should not call clearInterval if leg.varTimeInterval is defined and leg.myBetsAreas[section] is undefined', fakeAsync(() => {
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      const bets = [{ eventSource: { event: ['12345'], leg: [{  myBetsAreas: { },eventEntity: { id: 12345 }, varTimeInterval: 1,isVarDataAvailable:false}] } }] as any;
      service['matchCommentaryDataUpdate'](bets,varDataUpdate,MYBETS_AREAS.WIDGET);
      expect(windowRefService.nativeWindow.clearInterval).not.toHaveBeenCalled();
    }));
    it('should not call clearInterval if leg.varTimeInterval is defined and leg.isvardataAvailable[section].isMatchCmtryDataAvailable is false', fakeAsync(() => {
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      const bets = [{ eventSource: { event: ['12345'], leg: [{  myBetsAreas: { [MYBETS_AREAS.WIDGET]: {isMatchCmtryDataAvailable:false }},eventEntity: { id: 12345 }, varTimeInterval: 1,isVarDataAvailable:false}] } }] as any;
      service['matchCommentaryDataUpdate'](bets,varDataUpdate,MYBETS_AREAS.WIDGET);
      expect(windowRefService.nativeWindow.clearInterval).not.toHaveBeenCalled();
    }));
    it('should not call clearInterval if leg.varTimeInterval is defined and leg.isvardataAvailable[section].isMatchCmtryDataAvailable is false', fakeAsync(() => {
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      const bets = [{ eventSource: { event: ['12345'], leg: [{ myBetsAreas: { [MYBETS_AREAS.WIDGET]: { isMatchCmtryDataAvailable: false } }, eventEntity: { id: null }, varTimeInterval: 1, isVarDataAvailable: false }] } }] as any;
      service['matchCommentaryDataUpdate'](bets, varDataUpdate, MYBETS_AREAS.WIDGET);
      expect(bets[0].eventSource.leg[0].matchCmtryDataUpdate).toBeUndefined();
    }));
    it('should not assign data to teamName and playerName for var data', fakeAsync(() => {
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: null, playerName: null, varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      const bets = [{ eventSource: { event: ['12345'], leg: [{ myBetsAreas: { [MYBETS_AREAS.WIDGET]: { isMatchCmtryDataAvailable: false } }, eventEntity: { id: 12345 }, varTimeInterval: 1, isVarDataAvailable: false }] } }] as any;
      service['matchCommentaryDataUpdate'](bets, varDataUpdate, MYBETS_AREAS.WIDGET);
      expect(bets[0].eventSource.leg[0].matchCmtryDataUpdate.teamName).toBeUndefined();
      expect(bets[0].eventSource.leg[0].matchCmtryDataUpdate.playerName).toBeUndefined();
    }));
    it('should not call clearInterval if leg is null', fakeAsync(() => {
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      const bets = [{ eventSource: { event: ['12345'], leg: [null] } }] as any;
      service['matchCommentaryDataUpdate'](bets,varDataUpdate,MYBETS_AREAS.WIDGET);
      expect(windowRefService.nativeWindow.clearInterval).not.toHaveBeenCalled();
    }));
    it('should not go in foreach if bets is null', fakeAsync(() => {
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      const bets = [null] as any;
      service['matchCommentaryDataUpdate'](bets,varDataUpdate,MYBETS_AREAS.WIDGET);
      expect(bets[0]).toBeNull();
    }));
    it('should call setTimeout', fakeAsync(() => {
      windowRefService.nativeWindow.setTimeout.and.callFake(fn => fn())
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      const bets = [{ myBetsAreas: { [MYBETS_AREAS.WIDGET]: { isMatchCmtryDataAvailable: true }}, eventSource: { event: ['12345'], leg: [{ eventEntity: { id: 12345 } }] } }] as any;
      service['matchCommentaryDataUpdate'](bets,varDataUpdate,MYBETS_AREAS.WIDGET);
      tick(60000);
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 60000);
      expect(bets[0].eventSource.leg[0].myBetsAreas[MYBETS_AREAS.WIDGET].isMatchCmtryDataAvailable).toBeFalse();
    }));
    it('should call not setTimeout if isMatchTime is true', fakeAsync(() => {
      windowRefService.nativeWindow.setTimeout.and.callFake(fn => fn())
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', matchfact: 'Half Time' };
      const bets = [{ myBetsAreas: { [MYBETS_AREAS.WIDGET]: { isMatchCmtryDataAvailable: true } }, eventSource: { event: ['12345'], leg: [{ eventEntity: { id: 12345 } }] } }] as any;
      service['matchCommentaryDataUpdate'](bets, varDataUpdate, MYBETS_AREAS.WIDGET);
      tick(60000);
      expect(windowRefService.nativeWindow.setTimeout).not.toHaveBeenCalledWith(jasmine.any(Function), 60000);
      expect(bets[0].eventSource.leg[0].myBetsAreas[MYBETS_AREAS.WIDGET].isMatchCmtryDataAvailable).toBeTrue();
    }));
    it('should call not setTimeout if isMatchTime is true if matchCmtryDataUpdate is null', fakeAsync(() => {
      windowRefService.nativeWindow.setTimeout.and.callFake(fn => fn())
      const varDataUpdate = null;
      const bets = [{ myBetsAreas: { [MYBETS_AREAS.WIDGET]: { isMatchCmtryDataAvailable: true } }, eventSource: { event: ['12345'], leg: [{ eventEntity: { id: 12345 } }] } }] as any;
      service['matchCommentaryDataUpdate'](bets, varDataUpdate, MYBETS_AREAS.WIDGET);
      tick(60000);
      expect(windowRefService.nativeWindow.setTimeout).not.toHaveBeenCalledWith(jasmine.any(Function), 60000);
    }));
    it('should not call clearInterval if leg is null', fakeAsync(() => {
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      const bets = [{ eventSource: { event: ['12345'], leg: [null] } }] as any;
      service['matchCommentaryDataUpdate'](bets,varDataUpdate,MYBETS_AREAS.WIDGET);
      expect(windowRefService.nativeWindow.clearInterval).not.toHaveBeenCalled();
    }));
    it('should make isMatchCmtryDataAvailable true when var-data is availble if eventID is availble in array', () => {
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'Ba', playerName: 'Ab', varIconData: null, feed: 'OPTA', matchfact: 'test' };
      const bets = [{ myBetsAreas: { [MYBETS_AREAS.WIDGET]: { isMatchCmtryDataAvailable: true } }, eventSource: { event: ['12345'], leg: [{ eventEntity: { id: 12345 }, part: [{ outcome: [{}] }] }] } }] as any;
      service['matchCommentaryDataUpdate'](bets, varDataUpdate, MYBETS_AREAS.WIDGET);
      expect(bets[0].eventSource.leg[0].matchCmtryDataUpdate).toBeDefined();
      spyOn<any>(service, 'getMatchfactsUpdate').and.callThrough();
      expect(bets[0].eventSource.leg[0].matchCmtryDataUpdate).toEqual({
        teamName: 'Ba',
        playerName: 'Ab',
        matchfact: "Test",
        playerOffName: null,
        playerOnName: null,
        clock: null,
        minutes: null
      } as any);
      expect(bets[0].eventSource.leg[0].myBetsAreas[MYBETS_AREAS.WIDGET].isMatchCmtryDataAvailable).toBeTrue();
    });
    it('should make isMatchCmtryDataAvailable true when var-data is availble if eventID is availble in array', () => {
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'Ba', playerName: 'Ab', varIconData: null, feed: 'OPTA1', matchfact: 'test' };
      const bets = [{ myBetsAreas: { [MYBETS_AREAS.WIDGET]: { isMatchCmtryDataAvailable: true } }, eventSource: { event: ['12345'], leg: [{ eventEntity: { id: 12345 }, part: [{ outcome: [{}] }] }] } }] as any;
      service['matchCommentaryDataUpdate'](bets, varDataUpdate, MYBETS_AREAS.WIDGET);
      expect(bets[0].eventSource.leg[0].matchCmtryDataUpdate).toBeDefined();
      expect(bets[0].eventSource.leg[0].matchCmtryDataUpdate).toEqual({
        teamName: 'Ba',
        matchfact: "Test",
        playerName: 'Ab',
        playerOffName: null,
        playerOnName: null,
        clock: null,
        minutes: null
      } as any);
      expect(bets[0].eventSource.leg[0].myBetsAreas[MYBETS_AREAS.WIDGET].isMatchCmtryDataAvailable).toBeTrue();
    });
    it('should make isMatchCmtryDataAvailable true when var-data is not availble if eventID is availble in array', () => {
      const varDataUpdate = { matchCmtryEventId: '12345', teamName: 'Ba', varIconData: null, feed: 'OPTA1', matchfact: 'test' };
      const bets = [{ myBetsAreas: {}, eventSource: { event: ['12345'], leg: [{ eventEntity: { id: 12345 }, part: [{ outcome: [{}] }] }] } }] as any;
      service['matchCommentaryDataUpdate'](bets, varDataUpdate, MYBETS_AREAS.WIDGET);
      expect(bets[0].eventSource.leg[0].matchCmtryDataUpdate).toBeDefined();
      expect(bets[0].eventSource.leg[0].matchCmtryDataUpdate).toEqual({
        teamName: 'Ba',
        matchfact: "Test",
        playerName: null,
        playerOffName: null,
        playerOnName: null,
        clock: null,
        minutes: null,
      } as any);
      expect(bets[0].eventSource.leg[0].myBetsAreas[MYBETS_AREAS.WIDGET].isMatchCmtryDataAvailable).toBeTrue();
    });
 });

  describe('#getMatchfactsUpdate ', () => {
    it('should return info with playerName', () => {
      const matchCmtryDataUpdate: IMatchCmtryData = {
        matchCmtryEventId: '12345',
        teamName: 'Test team',
        playerName: 'Test player',
        varIconData: { svgId: 'Test svg', description: 'Test desc' },
        matchfact: "Test_match_fact",
        feed: "Test feed"
      } as any;
      expect(service['getMatchfactsUpdate'](matchCmtryDataUpdate)).toEqual({
        teamName: 'Test Team',
        playerName: 'Test Player',
        matchfact: "Test Match Fact",
        playerOffName: null,
        playerOnName: null,
        clock: null,
        minutes: null
      } as any);
    });
    it('should return playerName if not exists', () => {
      const matchCmtryDataUpdate: IMatchCmtryData = {
        matchCmtryEventId: '12345',
        teamName: 'Test team',
        matchfact: "Test_match_fact",
        feed: "Test feed"
      } as any;
      expect(service['getMatchfactsUpdate'](matchCmtryDataUpdate)).toEqual({
        teamName: 'Test Team',
        playerName: null,
        matchfact: "Test Match Fact",
        playerOffName: null,
        playerOnName: null,
        clock: null,
        minutes: null
      } as any);
    });
    it('should return not playerName if not exists and playerOffName and playerOnName exists', () => {
      const matchCmtryDataUpdate: IMatchCmtryData = {
        matchCmtryEventId: '12345',
        teamName: 'Test team',
        matchfact: "Test_match_fact",
        playerOffName: 'A',
        playerOnName: 'B',
        feed: "Test feed"
      } as any;
      expect(service['getMatchfactsUpdate'](matchCmtryDataUpdate)).toEqual({
        teamName: 'Test Team',
        playerName: null,
        matchfact: "Test Match Fact",
        playerOffName: 'A',
        playerOnName: 'B',
        clock: null,
        minutes: null
      } as any);
    });
    it('should return object with clock', () => {
      const matchCmtryDataUpdate: IMatchCmtryData = {
        matchCmtryEventId: '12345',
        teamName: 'Test team',
        matchfact: "Test_match_fact",
        clock: '50:00',
        feed: "Test feed"
      } as any;
      expect(service['getMatchfactsUpdate'](matchCmtryDataUpdate)).toEqual({
        teamName: 'Test Team',
        playerName: null,
        matchfact: "Test Match Fact",
        clock: '50:00',
        playerOffName: null,
        playerOnName: null,
        minutes: null
      } as any);
    });
    it('should return object with minutes', () => {
      const matchCmtryDataUpdate: IMatchCmtryData = {
        matchCmtryEventId: '12345',
        teamName: 'Test team',
        matchfact: "Test_match_fact",
        feed: "Test feed",
        minutes: '4'
      } as any;
      expect(service['getMatchfactsUpdate'](matchCmtryDataUpdate)).toEqual({
        teamName: 'Test Team',
        playerName: null,
        matchfact: "Test Match Fact",
        clock: null,
        playerOffName: null,
        playerOnName: null,
        minutes: '+4 mins'
      } as any);
    });
    it('should return object with minutes', () => {
      const matchCmtryDataUpdate: IMatchCmtryData = {
        matchCmtryEventId: '12345',
        teamName: 'Test team',
        matchfact: "Test_match_fact",
        feed: "Test feed",
        minutes: '1'
      } as any;
      expect(service['getMatchfactsUpdate'](matchCmtryDataUpdate)).toEqual({
        teamName: 'Test Team',
        playerName: null,
        matchfact: "Test Match Fact",
        clock: null,
        playerOffName: null,
        playerOnName: null,
        minutes: '+1 min'
      } as any);
    });
    it('should return null', () => {
      const matchCmtryDataUpdate: IMatchCmtryData = {
        matchCmtryEventId: '12345',
        teamName: null,
        playerName: null,
        varIconData: { svgId: 'Test svg', description: 'Test desc' },
        matchfact: null,
        feed: "Test feed"
      } as any;
      expect(service['getMatchfactsUpdate'](matchCmtryDataUpdate)).toEqual({
        teamName: null,
        playerName: null,
        matchfact: '',
        playerOffName: null,
        playerOnName: null,
        clock: null,
        minutes: null,
      } as any);
    });
  });
  describe('#transformMatchFact', () => {
    it('should return the transformed Text of matchFact', () => {
      const transformedMatcfact = service['transformMatchFact']('GOAL');
      expect(transformedMatcfact).toEqual('Goal');
    });
    it('should return the transformed Text of matchFact for more than a word', () => {
      const transformedMatcfact = service['transformMatchFact']('GOAL kick');
      expect(transformedMatcfact).toEqual('Goal Kick');
    });
    it('should return the transformed Text of matchFact for more than a word', () => {
      const transformedMatcfact = service['transformMatchFact']('Goal KICK');
      expect(transformedMatcfact).toEqual('Goal Kick');
    });
    it('should return the transformed Text of matchFact for more than a word', () => {
      const transformedMatcfact = service['transformMatchFact'](null);
      expect(transformedMatcfact).toEqual('');
    });
  });
  describe('sendRequestForLastMatchFact', () => {
    it('should call handleVarReasoningUpdatesService.sendRequestForLastMatchFact if channels.length', () => {
      const bets = [{ eventSource: { settled: 'N', leg: [{ part: [{ outcome: [{ event: { isOff: 'Y', id: '12345' }, eventCategory: { id: '16' } }] }] }] } }] as any;
      service.sendRequestForLastMatchFact(bets);
      expect(handleVarReasoningUpdatesService.sendRequestForLastMatchFact).toHaveBeenCalledWith(['mFACTS12345'])
    });
    it('should not  call handleVarReasoningUpdatesService.sendRequestForLastMatchFact if event is null', () => {
      const bets = [{ eventSource: { settled: 'N', leg: [{ part: [{ outcome: [{ event: null, eventCategory: { id: '16' } }] }] }] } }] as any;
      service.sendRequestForLastMatchFact(bets);
      expect(handleVarReasoningUpdatesService.sendRequestForLastMatchFact).not.toHaveBeenCalledWith(['mFACTS12345'])
    });
    it('should not  call handleVarReasoningUpdatesService.sendRequestForLastMatchFact if event.id is null', () => {
      const bets = [{ eventSource: { settled: 'N', leg: [{ part: [{ outcome: [{ event: { id: null }, eventCategory: { id: '16' } }] }] }] } }] as any;
      service.sendRequestForLastMatchFact(bets);
      expect(handleVarReasoningUpdatesService.sendRequestForLastMatchFact).not.toHaveBeenCalledWith(['mFACTS12345'])
    });
    it('should not  call handleVarReasoningUpdatesService.sendRequestForLastMatchFact if eventCategory is null', () => {
      const bets = [{ eventSource: { settled: 'N', leg: [{ part: [{ outcome: [{ event: { id: null }, eventCategory: null }] }] }] } }] as any;
      service.sendRequestForLastMatchFact(bets);
      expect(handleVarReasoningUpdatesService.sendRequestForLastMatchFact).not.toHaveBeenCalledWith(['mFACTS12345'])
    });
    it('should not call handleVarReasoningUpdatesService.sendRequestForLastMatchFact if outcome is null', () => {
      const bets = [{ eventSource: { settled: 'N', leg: [{ part: [{ outcome: null }] }] } }] as any;
      service.sendRequestForLastMatchFact(bets);
      expect(handleVarReasoningUpdatesService.sendRequestForLastMatchFact).not.toHaveBeenCalledWith(['mFACTS12345'])
    });
    it('should not call handleVarReasoningUpdatesService.sendRequestForLastMatchFact if part is null', () => {
      const bets = [{ eventSource: { settled: 'N', leg: [{ part: null }] } }] as any;
      service.sendRequestForLastMatchFact(bets);
      expect(handleVarReasoningUpdatesService.sendRequestForLastMatchFact).not.toHaveBeenCalledWith(['mFACTS12345'])
    });
    it('should not call handleVarReasoningUpdatesService.sendRequestForLastMatchFact if bets are null', () => {
      const bets = null as any;
      service.sendRequestForLastMatchFact(bets);
      expect(handleVarReasoningUpdatesService.sendRequestForLastMatchFact).not.toHaveBeenCalledWith(['mFACTS12345'])
    });
    it('should not call handleVarReasoningUpdatesService.sendRequestForLastMatchFact if bet is null', () => {
      const bets = [null] as any;
      service.sendRequestForLastMatchFact(bets);
      expect(handleVarReasoningUpdatesService.sendRequestForLastMatchFact).not.toHaveBeenCalledWith(['mFACTS12345'])
    });
    it('should not call handleVarReasoningUpdatesService.sendRequestForLastMatchFact if eventSource is null', () => {
      const bets = [{ eventSource: null }] as any;
      service.sendRequestForLastMatchFact(bets);
      expect(handleVarReasoningUpdatesService.sendRequestForLastMatchFact).not.toHaveBeenCalledWith(['mFACTS12345'])
    });
    it('should not call handleVarReasoningUpdatesService.sendRequestForLastMatchFact if leg is null', () => {
      const bets = [{ eventSource: { settled: 'N', leg: null } }] as any;
      service.sendRequestForLastMatchFact(bets);
      expect(handleVarReasoningUpdatesService.sendRequestForLastMatchFact).not.toHaveBeenCalledWith(['mFACTS12345'])
    });
    it('should not call handleVarReasoningUpdatesService.sendRequestForLastMatchFact if leg is null', () => {
      const bets = [{ eventSource: { settled: 'N', leg: [null] } }] as any;
      service.sendRequestForLastMatchFact(bets);
      expect(handleVarReasoningUpdatesService.sendRequestForLastMatchFact).not.toHaveBeenCalledWith(['mFACTS12345'])
    });
  });
  describe('removeHandlers', () => {
    it('should call handleVarReasoningUpdatesService.removeHandlers', () => {
      const channels = ['mFACTS123'];
      service.removeHandlers(channels);
      expect(handleVarReasoningUpdatesService.removeHandlers).toHaveBeenCalledWith(channels);
    });
  });
  describe('#getInitialStake ', () => {
    it('getInitialStake, stake is read from bet terms change and should be equal to 1', () => {
      const betEventSource = { betTermsChange: [{ stake: { value: 1 }, reasonCode: 'ORIGINAL_VALUES' }] } as any;
      expect(service.getInitialStake(betEventSource)).toBe(1) ;
    });
    it('getInitialStake, stake is read from bet.stake object and should be equal to 1', () => {
      const betEventSource =  { stake: { value: 1 } }  as any;
      expect(service.getInitialStake(betEventSource)).toBe(1);
    });
    it('getInitialStake, stake is read from bet.stake and should be equal to 1', () => {
      const betEventSource =  { stake: 1 }  as any;
      expect(service.getInitialStake(betEventSource)).toBe(1);
    });
  });

it('setToolTipStatus should have 1 receiptViewsCounter pre exist', () => {
    storageService.get.and.returnValue({ 'receiptViewsCounter-test': 1 });
    const tooltipData = { 'receiptViewsCounter-test': 2 };
    service.setToolTipStatus();
    expect(storageService.set).toHaveBeenCalledOnceWith('tooltipsSeen', tooltipData);
  });
  it('setToolTipStatus should not have receiptViewsCounter', () => {
    storageService.get.and.returnValue();
    const tooltipData = { 'receiptViewsCounter-test': 1 };
    service.setToolTipStatus();
    expect(storageService.set).toHaveBeenCalledOnceWith('tooltipsSeen', tooltipData);
  });

  it('should call checkLuckyBonus()', () => {
    const bets = {
      eventSource:{
      betType:'L15',
      availableBonuses :{
        availableBonus:{
          multiplier:'2'
        }
      }}
    }
    const resp = service['checkLuckyBonus'](bets);
    expect(resp).toEqual('£2.35');
  });

  it('should call checkSPSelection()', () => {
    const bets = {
        eventSource:{betType:'L15',availableBonuses :{availableBonus:{multiplier:'2'}},
        leg: [{part: [{price: [{priceType: {code: "S"}}]}]}]}
    }
    expect(service['checkSPSelection'](bets)).toBe(true);
  });

  it('should call checkSPSelection()', () => {
    const bets = {
        eventSource:{betType:'L15',availableBonuses :{availableBonus:{multiplier:'2'}},
        leg: [{part: [{priceType: "S"}]}]}
    }
    expect(service['checkSPSelection'](bets)).toBe(true);
  });

  it('should call checkLuckyType()', () => {
    const bets = {
      eventSource:{
      betType:'L15',
      availableBonuses :{
        availableBonus:{
          multiplier:'2'
        }
      }}
    }
    expect(service['checkLuckyType'](bets)).toBe(true);
  });
});
