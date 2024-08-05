import { fakeAsync, tick } from '@angular/core/testing';
import { of as observableOf } from 'rxjs';
import { MYBETS_AREAS } from '@app/betHistory/constants/bet-leg-item.constant';
import { MyBetsComponent } from './my-bets.component';
import { CASHOUT_SUSPENDED } from '@app/betHistory/components/cashOutMessaging/cash-out-message.constants';

describe('MyBetsComponent', () => {
  let component,
    locale,
    cashOutSectionService,
    pubsub,
    editMyAccaService,
    liveBetUpdateHandler,
    updCashoutBetHandler,
    betlegLoadedhandler,
    cashoutMapUpdateHandler,
    callbackHandler,
    betTrackingService,
    payoutUpdateHandler,
    partialCashoutSuccessHandler,
    handleScoreboardsStatsUpdatesService,
    cmsService,
    deviceService;

  const bet = { betId: '615079', cashoutValue: '2' } as any;
  const content = 'static block content';

  beforeEach(() => {
    editMyAccaService = {};
    locale = {
      getString: jasmine.createSpy().and.returnValue(''),
    };
    callbackHandler = (ctrlName: string, eventName: string, callback) => {
      if (eventName === 'UPDATE_CASHOUT_BET') {
        updCashoutBetHandler = callback;
      } else if (eventName.indexOf('CASH_OUT_MAP_UPDATED') > -1) {
        cashoutMapUpdateHandler = callback;
      } else if (eventName === 'LIVE_BET_UPDATE') {
        liveBetUpdateHandler = callback;
      }else if (eventName === 'BET_LEGS_LOADED') {
        betlegLoadedhandler = callback;
      }else if(eventName === 'PAYOUT_UPDATE'){
        payoutUpdateHandler = callback;
      }
    };
    betTrackingService = {
      isTrackingEnabled: jasmine.createSpy('isTrackingEnabled').and.returnValue(observableOf(true)),
      getStaticContent: jasmine.createSpy('getStaticContent').and.returnValue(observableOf(content)),
    };
    cashOutSectionService = {
      registerController: jasmine.createSpy(),
      generateBetsMap: jasmine.createSpy().and.returnValue('betsMap'),
      generateBetsArray: jasmine.createSpy().and.returnValue([]),
      cashOutSectionService: jasmine.createSpy(),
      emitMyBetsCounterEvent: jasmine.createSpy(),
      createTempDataForMyBets: jasmine.createSpy().and.returnValue('createTempDataForMyBets'),
      removeListeners: jasmine.createSpy(),
      removeErrorMessageWithTimeout: jasmine.createSpy(),
      updateBet: jasmine.createSpy(),
      isCashoutError: jasmine.createSpy('isCashoutError'),
      getCashoutError: jasmine.createSpy('getCashoutError'),
      matchCommentaryDataUpdate: jasmine.createSpy('matchCommentaryDataUpdate'),
      sendRequestForLastMatchFact: jasmine.createSpy('sendRequestForLastMatchFact').and.returnValue(['mFACTS1234']),
      removeHandlers: jasmine.createSpy('removeHandlers')
    };
    pubsub = {
      unsubscribe: jasmine.createSpy(),
      subscribe: jasmine.createSpy().and.callFake(callbackHandler),
      API: {
        UPDATE_CASHOUT_BET: 'UPDATE_CASHOUT_BET',
        CASH_OUT_MAP_UPDATED: 'CASH_OUT_MAP_UPDATED',
        MY_BETS_UPDATED: 'MY_BETS_UPDATED',
        LIVE_BET_UPDATE: 'LIVE_BET_UPDATE',
        UPDATE_MATCHCOMMENTARY_DATA: 'UPDATE_MATCHCOMMENTARY_DATA',
        BET_LEGS_LOADED: 'BET_LEGS_LOADED',
        PAYOUT_UPDATE: 'PAYOUT_UPDATE',
        PARTIAL_CASHOUT_SUCCESS: 'PARTIAL_CASHOUT_SUCCESS'
      }
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({ScoreboardsDataDisclaimer:{enabled: true, dataDisclaimer: 'Transmission delayed'}, CelebratingSuccess: {displayCashoutProfitIndicator: true}})),
    };
    handleScoreboardsStatsUpdatesService = {
      getStatisticsEventIds: jasmine.createSpy('getStatisticsEventIds').and.returnValue(observableOf('123456'))
    };
    deviceService = {
      isMobile: true
    }

    component = new MyBetsComponent(
      editMyAccaService,
      locale,
      cashOutSectionService,
      pubsub,
      betTrackingService,
      handleScoreboardsStatsUpdatesService,
      cmsService,
      deviceService
    );
    component.ctrlName = 'MyBetsController';
    component.cashoutBets = [{
      betId: '615079',
      cashoutValue: '2'
    }] as any;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('@ngOnInit', () => {
    it('should init data, update it', () => {
      component.ngOnInit();
      expect(cashOutSectionService.registerController).toHaveBeenCalledWith('MyBetsController');
      expect(cashOutSectionService.emitMyBetsCounterEvent).toHaveBeenCalledWith([]);
      liveBetUpdateHandler();
      expect(cashOutSectionService.removeErrorMessageWithTimeout).toHaveBeenCalledWith([], undefined);
      updCashoutBetHandler(bet);
      expect(cashOutSectionService.updateBet).toHaveBeenCalledWith(bet, []);
      expect(component.cashoutBets[0].cashoutValue).toEqual('2');
    });

    it('should not update cashout value', () => {
      bet.betId = '123456';
      component.ngOnInit();
      updCashoutBetHandler(bet);
      expect(cashOutSectionService.updateBet).toHaveBeenCalledWith(bet, []);
      expect(component.cashoutBets[0].cashoutValue).toEqual('2');
    });

    it('should update cashout map on CASH_OUT_MAP_UPDATED', () => {
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({}));
      component.ngOnInit();
      cashoutMapUpdateHandler();

      expect(cashOutSectionService.removeListeners).toHaveBeenCalledWith('MyBetsController');
      expect(cashOutSectionService.removeListeners).toHaveBeenCalledWith('MyBetsController');
      expect(cashOutSectionService.registerController).toHaveBeenCalled();
      expect(cashOutSectionService.createTempDataForMyBets).toHaveBeenCalled();
      expect(cashOutSectionService.generateBetsMap).toHaveBeenCalled();
    });

    it('should show opta disclaimer', fakeAsync(() => {
      component.eventId = '123456';
      cashOutSectionService.generateBetsArray.and.returnValue([
        {
          eventSource: {
            event: ['123456'],
            leg:[{}]
          }
        }
      ] as any);
      component.ngOnInit();

      tick();
      expect(handleScoreboardsStatsUpdatesService.getStatisticsEventIds).toHaveBeenCalled();
      expect(component.bets[0].optaDisclaimerAvailable).toBeTruthy();
    }));

    it('should not show opta disclaimer', fakeAsync(() => {
      component.eventId = '654321';
      cashOutSectionService.generateBetsArray.and.returnValue([
        {
          eventSource: {
            event: ['654321'],
            leg:[{}]
          }
        }
      ] as any);
      component.ngOnInit();

      tick();
      expect(handleScoreboardsStatsUpdatesService.getStatisticsEventIds).toHaveBeenCalled();
      expect(component.bets[0].optaDisclaimerAvailable).toBeFalsy();
    }));
    it('should call matchCommentaryUpdate',()=>{
      spyOn(component as any, 'matchCommentaryUpdate');
      pubsub.subscribe.and.callFake((cashoutbets, listeners, handler) => {
        if (listeners == 'BET_LEGS_LOADED') {
          handler('myBetsTab');
        }
      });
      component.ngOnInit();
      expect(component['matchCommentaryUpdate']).toHaveBeenCalled();
      expect(cashOutSectionService.sendRequestForLastMatchFact).toHaveBeenCalledWith(component.bets);
    });
    it('should call subscribe for lucky bonus',()=>{
      spyOn(component as any, 'matchCommentaryUpdate');
      pubsub.subscribe.and.callFake((cashoutbets, listeners, handler) => {
        if (listeners == 'LUCKY_BONUS') {
          handler('O/26382303/0000067');
        }
      });
      component.ngOnInit();
      expect(component['matchCommentaryUpdate']).toHaveBeenCalled();
    });
    it('should set displayProfitIndicator - true', () => {
      component.ngOnInit();
      expect(component.displayProfitIndicator).toBeTrue();
    });
  });
  describe('#cmsService getSystemConfig', () => {
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
    it('getSystemConfig with displaySportIcon as correct values', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({CelebratingSuccess: {displaySportIcon: ['edpmybets']}}));
      component.ngOnInit();
      expect(component.isSportIconEnabled).toBeTrue();
    });
  });

  describe('@ngOnChanges', () => {
    let changes;

    beforeEach(() => {
      changes = { betsMap: false } as any;
    });

    it('removeListeners & updateBets should not be called', () => {
      component.ngOnChanges(changes);
      expect(cashOutSectionService.removeListeners).not.toHaveBeenCalledWith('MyBetsController');
      expect(cashOutSectionService.emitMyBetsCounterEvent).not.toHaveBeenCalledWith([]);
      liveBetUpdateHandler();
      expect(cashOutSectionService.removeErrorMessageWithTimeout).not.toHaveBeenCalledWith([], undefined);
      updCashoutBetHandler(bet);
      expect(cashOutSectionService.updateBet).not.toHaveBeenCalledWith(bet, []);
    });

    it('removeListeners & updateBets should be called', () => {
      changes.betsMap = true;
      component.ngOnChanges(changes);
      expect(cashOutSectionService.removeListeners).toHaveBeenCalledWith('MyBetsController');
      expect(cashOutSectionService.emitMyBetsCounterEvent).toHaveBeenCalledWith([]);
      liveBetUpdateHandler();
      expect(cashOutSectionService.removeErrorMessageWithTimeout).toHaveBeenCalledWith([], undefined);
      updCashoutBetHandler(bet);
      expect(cashOutSectionService.updateBet).toHaveBeenCalledWith(bet, []);
    });
  });

  it('@ngOnDestroy should perform unsubscribe and unsync', () => {
    component['betTrackingEnabledSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component['getEventIdStatisticsSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component['channels'] = ['mFACTS123'];
    component.ngOnDestroy();

    expect(cashOutSectionService.removeListeners).toHaveBeenCalledWith('MyBetsController');
    expect(pubsub.unsubscribe).toHaveBeenCalled();
    expect(component['betTrackingEnabledSubscription'].unsubscribe).toHaveBeenCalled();
    expect(component['getEventIdStatisticsSubscription'].unsubscribe).toHaveBeenCalled();
    expect(cashOutSectionService.removeHandlers).toHaveBeenCalledWith(['mFACTS123']);
  });
  it('@ngOnDestroy should perform unsubscribe and unsync ', () => {
    component['betTrackingEnabledSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component['getEventIdStatisticsSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component['channels'] = null;
    component.ngOnDestroy();

    expect(cashOutSectionService.removeListeners).toHaveBeenCalledWith('MyBetsController');
    expect(pubsub.unsubscribe).toHaveBeenCalled();
    expect(component['betTrackingEnabledSubscription'].unsubscribe).toHaveBeenCalled();
    expect(component['getEventIdStatisticsSubscription'].unsubscribe).toHaveBeenCalled();
    expect(cashOutSectionService.removeHandlers).not.toHaveBeenCalledWith(['mFACTS123']);
  });

  it('@trackByBet should return joined string', () => {
    const index: number = 11;
    const betData: any = {
      eventSource: {
        betId: 12,
        receipt: 'receipt'
      }
    };
    expect(component.trackByBet(index, betData)).toEqual('1112receipt');
  });

  it('@registerEventListeners should register callbacks on server updates', () => {
    spyOn<any>(component, 'removeListeners');
    spyOn<any>(component, 'updateBets');
    spyOn<any>(component, 'updateCashoutBetValue');
    const updatedBet = {
      betId: 42,
      isCashOutedBetSuccess: true,
      cashoutValue: 'TEST', 
      isPartialCashOutAvailable: false, 
      isCashOutUnavailable: true,
      isEWCashoutSuspend: false
    } as any;
    const returnsResponse = {updatedReturns: [{returns: 0.09, betNo: '12345'}]};
    pubsub.subscribe.and.callFake((name, listeners, handler) => {
      if (listeners === 'LIVE_BET_UPDATE') {
        handler('sync_options');
      } else if(listeners === 'PAYOUT_UPDATE'){
        handler(returnsResponse);
      }else {
        handler(updatedBet);
      }
    });
    component.bets = [{ id:"934",eventSource: null},{id:'935', eventSource: {}},{ id:"931", eventSource: { potentialPayout: 0.09,
      betId: '12345', event: '123456', leg: [{ part: [{outcomeId: "555"}], eventEntity: { eventIsLive: true, comments:{home:{}} } }] } }
    ] as any;
    component.cashoutIds = [{ id: 4 }];
    component.placedBets = [{ id: 42, betId: 42 }] as any;
    component.betLocation = 'bet location';
    component['registerEventListeners']();

    expect(pubsub.subscribe).toHaveBeenCalledWith(component.ctrlName, 'LIVE_BET_UPDATE', jasmine.any(Function));
    expect(cashOutSectionService.removeErrorMessageWithTimeout).toHaveBeenCalledWith(component.bets, 'sync_options');

    expect(pubsub.subscribe).toHaveBeenCalledWith(
      component.ctrlName, ['CASH_OUT_MAP_UPDATED', 'MY_BETS_UPDATED'], jasmine.any(Function)
    );
    expect(component['removeListeners']).toHaveBeenCalled();
    expect(component['updateBets']).toHaveBeenCalled();
    expect(cashOutSectionService.createTempDataForMyBets).toHaveBeenCalledWith([{ id: 4 }],
      [{ id: 42, betId: 42, isCashOutedBetSuccess: true}]);
    expect(cashOutSectionService.generateBetsMap).toHaveBeenCalledWith('createTempDataForMyBets', 'bet location');

    expect(pubsub.subscribe).toHaveBeenCalledWith(component.ctrlName, 'UPDATE_CASHOUT_BET', jasmine.any(Function));
    expect(cashOutSectionService.updateBet).toHaveBeenCalledWith(updatedBet, component.bets);
    expect(component.placedBets[0].isCashOutedBetSuccess).toBeTruthy();
    expect(component['updateCashoutBetValue']).toHaveBeenCalledWith(updatedBet);
  });

  it('@registerEventListeners should register callbacks on server updates', () => {
    spyOn<any>(component, 'removeListeners');
    spyOn<any>(component, 'updateBets');
    spyOn<any>(component, 'updateCashoutBetValue');
    const updatedBet = {
      betId: 42,
      isCashOutedBetSuccess: true,
      cashoutValue: CASHOUT_SUSPENDED, 
      isPartialCashOutAvailable: false, 
      isCashOutUnavailable: true,
      isEWCashoutSuspend: true
    } as any;

    const returnsResponse = {updatedReturns: [{returns: 0.09, betNo: '12345'}]}; 
    pubsub.subscribe.and.callFake((name, listeners, handler) => {
      if (listeners === 'LIVE_BET_UPDATE') {
        handler('sync_options');
      } else if(listeners === 'PAYOUT_UPDATE'){
        handler(returnsResponse);
      }else {
        handler(updatedBet);
      }
    });
    component.bets = [{ id:"931", eventSource: { potentialPayout: 0.09,
      betId: '12345', event: '123456', leg: [{ part: [{outcomeId: "555"}], eventEntity: { eventIsLive: true, comments:{home:{}} } }] } }] as any;
    component.cashoutIds = [{ id: 4 }];
    component.placedBets = [{ id: 42, betId: 42 }] as any;
    component.betLocation = 'bet location';
    component['registerEventListeners']();

    expect(pubsub.subscribe).toHaveBeenCalledWith(component.ctrlName, 'LIVE_BET_UPDATE', jasmine.any(Function));
    expect(cashOutSectionService.removeErrorMessageWithTimeout).toHaveBeenCalledWith(component.bets, 'sync_options');

    expect(pubsub.subscribe).toHaveBeenCalledWith(
      component.ctrlName, ['CASH_OUT_MAP_UPDATED', 'MY_BETS_UPDATED'], jasmine.any(Function)
    );
    expect(component['removeListeners']).toHaveBeenCalled();
    expect(component['updateBets']).toHaveBeenCalled();
    expect(cashOutSectionService.createTempDataForMyBets).toHaveBeenCalledWith([{ id: 4 }],
      [{ id: 42, betId: 42, isCashOutedBetSuccess: true, cashoutValue: CASHOUT_SUSPENDED, isPartialCashOutAvailable: false, isCashOutUnavailable: true }]);
    expect(cashOutSectionService.generateBetsMap).toHaveBeenCalledWith('createTempDataForMyBets', 'bet location');

    expect(pubsub.subscribe).toHaveBeenCalledWith(component.ctrlName, 'UPDATE_CASHOUT_BET', jasmine.any(Function));
    expect(cashOutSectionService.updateBet).toHaveBeenCalledWith(updatedBet, component.bets);
    expect(component.placedBets[0].isCashOutedBetSuccess).toBeTruthy();
    expect(component['updateCashoutBetValue']).toHaveBeenCalledWith(updatedBet);
  });

  it('isCashoutError should call isCashoutError method of cashout section service', () => {
    component['isCashoutError']({} as any);
    expect(cashOutSectionService.isCashoutError).toHaveBeenCalled();
  });

  it('getCashoutError should call getCashoutError method of cashout section service', () => {
    component['getCashoutError']({} as any);
    expect(cashOutSectionService.getCashoutError).toHaveBeenCalled();
  });

  it('updateBets', () => {
    component.eventId = '234';
    const bets = <any>[
      {
        eventSource: {
          event: ['234', '255']
        }
      },
      {
        eventSource: {
          event: ['123', '355']
        }
      }
    ];
    component['cashOutSectionService'].generateBetsArray = () => bets;
    component['updateBets']();

    expect(component.bets.length).toEqual(1);
  });

  it('updateBets - BYB changes', () => {
    component.eventId = '234';
    component.raceCardEventIds = [+component.eventId];
    
    const bets = <any>[
      {
        eventSource: {
          event: ['234', '255']
        }
      },
      {
        eventSource: {
          event: ['123', '355']
        }
      }
    ];
    component['cashOutSectionService'].generateBetsArray = () => bets;
    component['updateBets']();

    expect(component.bets.length).toEqual(1);
  });

  describe('Init', () => {
    it('should get static block if feature toggle is on', fakeAsync(() => {
      const betsMapMock = {value:{ bybType: '5-A-SIDE'}};
      cashOutSectionService.generateBetsMap.and.returnValue(betsMapMock);
      component.betTrackingEnabled = true;

      component['init']();
      tick();

      expect(cashOutSectionService.generateBetsMap).toHaveBeenCalled();
      expect(betTrackingService.getStaticContent).toHaveBeenCalled();
      expect(betTrackingService.isTrackingEnabled).toHaveBeenCalled();
      expect(component.betsMap).toBeTruthy();
      expect(component.optaDisclaimer).toEqual(content);
      expect(component.betTrackingEnabled).toBeTruthy();
    }));

    it('shouldnt get static block if feature toggle is off', fakeAsync(() => {
      const betsMapMock = {value:{ bybType: '5-A-SIDE'}};
      cashOutSectionService.generateBetsMap.and.returnValue(betsMapMock);
      betTrackingService.isTrackingEnabled.and.returnValue(observableOf(false));

      component['init']();
      tick();

      expect(cashOutSectionService.generateBetsMap).toHaveBeenCalled();
      expect(betTrackingService.getStaticContent).not.toHaveBeenCalled();
      expect(betTrackingService.isTrackingEnabled).toHaveBeenCalled();
      expect(component.betsMap).toBeTruthy();
      expect(component.optaDisclaimer).toEqual(null);
      expect(component.betTrackingEnabled).toBeFalsy();
    }));
  });

  describe('#isShownDisclaimer', () => {
    it('isShownDisclaimer true', () => {
      component.dataDisclaimer = { enabled: true } as any;
      const bet = { eventSource: { leg: [{ eventEntity: { eventIsLive: true, comments: {home:{}} } }] } } as any;
      const result = component.isShownDisclaimer(bet);
      expect(result).toBe(true);
    })
    it('isShownDisclaimer false of cms ', () => {
      component.dataDisclaimer = { enabled: false } as any;
      const bet = { eventSource: { leg: [{ eventEntity: { eventIsLive: true, comments: {home:{}} } }] } } as any;
      const result = component.isShownDisclaimer(bet);
      expect(result).toBe(false);
    })
    it('isShownDisclaimer nolive', () => {
      component.dataDisclaimer = { enabled: true } as any;
      const bet = { eventSource: { leg: [{ eventEntity: { eventIsLive: false, comments: {home:{}} } }] } } as any;
      const result = component.isShownDisclaimer(bet);
      expect(result).toBe(false);
    })
    it('isShownDisclaimer comments null', () => {
      component.dataDisclaimer = { enabled: true } as any;
      const bet = { eventSource: { leg: [{ eventEntity: { eventIsLive: true, comments: null } }] } } as any;
      const result = component.isShownDisclaimer(bet);
      expect(result).toBe(false);
    })
  })
  describe('#matchCommentaryUpdate', () => {
    it('should subscribe when match-facts is avaialble and call matchCommentaryDataUpdate', () => {
      component.bets = [{ id: 1, eventSource: { leg: [{}] } }];
      const matchCmtryDataUpdate = { EventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      pubsub.subscribe.and.callFake((mybets, listeners, handler) => {
        if (listeners == 'UPDATE_MATCHCOMMENTARY_DATA') {
          handler(matchCmtryDataUpdate);
        }
      });
      component['matchCommentaryUpdate']();
      expect(pubsub.subscribe).toHaveBeenCalledWith(component['ctrlName'], 'UPDATE_MATCHCOMMENTARY_DATA', jasmine.any(Function));
      expect(cashOutSectionService.matchCommentaryDataUpdate).toHaveBeenCalledOnceWith(component.bets, matchCmtryDataUpdate, 'edp');
    });
    it('should call resetMatchCmtryData', () => {
      spyOn(component, 'resetMatchCmtryData');
      component['matchCommentaryUpdate']();
      expect(component['resetMatchCmtryData']).toHaveBeenCalledWith(component.bets);
    });
  });
  describe('resetMatchCmtryData', () => {
    it('should set isMatchCmtryDataAvailable false if legitem?.myBetsAreas,legitem?.myBetsAreas[MYBETS_AREAS.EDP]', () => {
      component.bets = [{
        id: 1,
        eventSource: {
          leg: [{
            myBetsAreas: {
              [MYBETS_AREAS.EDP]: {
                isMatchCmtryDataAvailable: true
              }
            }
          }]
        }
      }];
      component['resetMatchCmtryData'](component.bets);
      expect(component.bets[0].eventSource.leg[0].myBetsAreas).toBeDefined();
      expect(component.bets[0].eventSource.leg[0].myBetsAreas[MYBETS_AREAS.EDP]).toBeDefined();
      expect(component.bets[0].eventSource.leg[0].myBetsAreas[MYBETS_AREAS.EDP].isMatchCmtryDataAvailable).toBeFalse();
    });
    it('should not set isMatchCmtryDataAvailable false if eventSource is undefined', () => {
      component.bets = [{ id: 1 }];
      component['resetMatchCmtryData'](component.bets);
      expect(component.bets[0].eventSource).toBeUndefined();
    });
    it('should not set isMatchCmtryDataAvailable false if legitem?.myBetsAreas,legitem?.myBetsAreas[MYBETS_AREAS.EDP] undefined', () => {
      component.bets = [{ id: 1, eventSource: { leg: [{}] } }];
      component['resetMatchCmtryData'](component.bets);
      expect(component.bets[0].eventSource.leg[0].myBetsAreas).toBeUndefined();
    });
    it('should not set isMatchCmtryDataAvailable false if legitem?.myBetsAreas,legitem?.myBetsAreas[MYBETS_AREAS.EDP] undefined', () => {
      component.bets = [{
        id: 1, eventSource: {
          leg: [{
            myBetsAreas: {}
          }]
        }
      }];
      component['resetMatchCmtryData'](component.bets);
      expect(component.bets[0].eventSource.leg[0].myBetsAreas[MYBETS_AREAS.EDP]).toBeUndefined();
    });
    it('should not set isMatchCmtryDataAvailable false if null', () => {
      component.bets = [null];
      component['resetMatchCmtryData'](component.bets);
      expect(component.bets[0]).toBeNull();
    });
    it('should not set isMatchCmtryDataAvailable false if null', () => {
      component.bets = [{
        id: 1, eventSource: {
          leg: [null]
        }
      }];
      component['resetMatchCmtryData'](component.bets);
      expect(component.bets[0].eventSource.leg[0]).toBeNull();
    });
  });
  describe('#isDisplayBonus', () => {
    it('should call isDisplayBonus() and return true', () => {
      component['betReceipts'].add('O/26382303/0000067');
      const resp = component['isDisplayBonus']('O/26382303/0000067');
      expect(resp).toBeTrue();
    });
    it('should call isDisplayBonus() and return false', () => {
      component['betReceipts'].add('O/26382303/0000067');
      expect(component['betReceipts'].has('O/26382303/0000066')).toBeFalse();
    });
  });
});
