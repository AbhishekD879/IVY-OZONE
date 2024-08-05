import { of as observableOf } from 'rxjs';
import { CashOutBetsComponent } from './cash-out-bets.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { ALERTS_GTM } from '@app/betHistory/constants/bet-leg-item.constant';

describe('CashOutBetsComponent', () => {
  let component: CashOutBetsComponent;

  let emaService,
    locale,
    cashOutSectionService,
    pubsub,
    windowRef,
    changeDetectorRef,
    betTrackingService,
    handleScoreboardsStatsUpdatesService,
    cmsService,
    betReuseService,
    storageService,
    user,
    device,
    nativeBridge,
    sessionService,
    gtmService;

  let callbackHandler,
    callbacks;
  const areaInput = 'cashout-area';
  const content = 'static block content';


  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy().and.returnValue(''),
    };
    callbackHandler = (ctrlName: string, eventName: string, callback) => {
      if (['LIVE_BET_UPDATE', 'SESSION_LOGOUT', 'BETSLIP_UPDATED', 'BET_EVENTENTITY_UPDATED'].includes(eventName)) {
        callback && callback({});
      } else if(eventName === 'UPDATE_CASHOUT_BET') {
        callback('bet');
      }else if(eventName === 'PAYOUT_UPDATE') {
        callback({updatedReturns: [{returns: 0.09, betNo: '12345'}]});
      } else if(eventName === 'LIVE_STREAM_BIR') {
        callback({legId:'555',flag:true,isUsedFromWidget:true});
        callback({legId:'555',flag:false,isUsedFromWidget:true});
        callback({legId:'555',flag:false,isUsedFromWidget:false});
      } else if(['SUCCESSFUL_LOGIN', 'HOME_BETSLIP'].includes(eventName)) {
        callback('cashout');
      }
    };
    betTrackingService = {
      isTrackingEnabled: jasmine.createSpy('isTrackingEnabled').and.returnValue(observableOf(true)),
      getStaticContent: jasmine.createSpy('getStaticContent').and.returnValue(observableOf(content)),
    };
    cashOutSectionService = {
      updateBet: jasmine.createSpy('updateBet'),
      registerController: jasmine.createSpy('registerController'),
      generateBetsMap: jasmine.createSpy('generateBetsMap').and.returnValue(observableOf({ bybType: '5-A-SIDE' })),
      generateBetsArray: jasmine.createSpy('generateBetsArray').and.returnValue([
        {
          eventSource: {
            event: ['123456'],
            leg: [{ part: [{ outcomeId: "666" }] }],
            eventEntity: {
              id: "123456", eventIsLive: true, comments: { home: {} }, categoryCode: 'football',
              eventSortCode: 'test', categoryId: '16', typeName: "league", categoryName: 'test categoryName'
            },
            betType: 'SGL',
            receipt: '0000/1234/12345',
            potentialPayout: 0.09,
            betId: '12345'
          }
        }
      ] as any),
      removeCashoutItemWithTimeout: jasmine.createSpy('removeCashoutItem').and.returnValue(observableOf({})),
      removeListeners: jasmine.createSpy(),
      isCashoutError: jasmine.createSpy('isCashoutError'),
      getCashoutError: jasmine.createSpy('getCashoutError'),
      matchCommentaryDataUpdate:jasmine.createSpy('getCashoutError'),
      sendRequestForLastMatchFact: jasmine.createSpy('sendRequestForLastMatchFact').and.returnValue(['mFACTS1234']),
      removeHandlers: jasmine.createSpy('removeHandlers'),
      setToolTipStatus: jasmine.createSpy('setToolTipStatus')
    };
    pubsub = {
      subscribe: jasmine.createSpy('subscribe').and.callFake(callbackHandler),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      detach: jasmine.createSpy('detach'),
    };
    emaService = {
      clearAccas: jasmine.createSpy('emaService.clearAccas')
    };
    windowRef = {
      nativeWindow: {
        setInterval: jasmine.createSpy('setInterval'),
        clearInterval: jasmine.createSpy('clearInterval'),
        setTimeout: jasmine.createSpy('setTimeout'),
        parent: {
          postMessage: jasmine.createSpy('postMessage')
        }
      },
      document: {
        removeEventListener: jasmine.createSpy('removeEventListener'),
        addEventListener: jasmine.createSpy('addEventListener')
      }
    };
    handleScoreboardsStatsUpdatesService = {
      getStatisticsEventIds: jasmine.createSpy('getStatisticsEventIds').and.returnValue(observableOf('123456'))
    };
    cmsService = {
        getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({ScoreboardsDataDisclaimer:{enabled: true, dataDisclaimer: 'Transmission delayed'}, winAlerts: {displayOnMyBets: ['android']}, CelebratingSuccess: {displayCashoutProfitIndicator: true}})),
        getFeatureConfig : jasmine.createSpy('getFeatureConfig ').and.returnValue(observableOf({
            visibleNotificationIconsFootball: {
              multiselectValue: ['android'],
              value: 'league'
            },
            displayOnMyBets: ['android']
        }))
    };
    betReuseService = {
      reuse: jasmine.createSpy('reuse')
    };
    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get')
    };
    nativeBridge = {
      onActivateWinAlerts: jasmine.createSpy(),
      hasOnEventAlertsClick: jasmine.createSpy().and.returnValue(true),
      onClearCache: jasmine.createSpy(),
      hasShowFootballAlerts: jasmine.createSpy().and.returnValue(true),
      getMobileOperatingSystem: jasmine.createSpy().and.returnValue('android'),
      winAlertsStatus: jasmine.createSpy(),
      multipleEventPageLoaded: jasmine.createSpy(),
      onEventAlertsClick: jasmine.createSpy(),
      showFootballAlerts: jasmine.createSpy(),
      pushNotificationsEnabled: true,
      disableWinAlertsStatus : jasmine.createSpy()
    };
    device = { isWrapper: true,isDesktop:true, isMobile:true };
    gtmService = { push: jasmine.createSpy() };
    sessionService = {
      whenSession: jasmine.createSpy().and.returnValue(Promise.resolve(true))
    };
    user = {
      set: jasmine.createSpy(),
      winAlertsToggled: true,
      username: 'test'
    };
    
    component = new CashOutBetsComponent(
      emaService,
      locale,
      cashOutSectionService,
      pubsub,
      windowRef,
      changeDetectorRef,
      betTrackingService,
      handleScoreboardsStatsUpdatesService,
      cmsService,
      betReuseService,
      storageService,
      user,
      nativeBridge,
      sessionService,
      device,
      gtmService
    );

    component.area = areaInput;
    component.bets = [{ eventSource: { potentialPayout: 0.09, betId: '12345', event: '123456', leg: [{legNo:'5',  removedLeg: false, part: [{outcomeId: "555"}], eventEntity: {  id: '123456', eventIsLive: true, comments:{home:{}}, categoryCode: 'football', 
    eventSortCode: 'test', categoryId: '16', typeName: "league", categoryName: 'test categoryName' } }],
    betType: 'SGL', receipt: '0000/1234/12345' } }] as any;
  });

  it('should set displayProfitIndicator - true', () => {
    expect(component.displayProfitIndicator).toBeTrue();
  });
  
  describe('ngOnInit', () => {
    beforeEach(() => {
      spyOn<any>(component, 'init');
    });

    it('should set ctrlName based on input "area" param', () => {
      component.ngOnInit();

      expect(component['ctrlName']).toEqual(`CashoutWidgetController-${areaInput}`);
      expect(component.winAlertsEnabled).toBeTrue();
    });

    it('should show opta disclaimer', fakeAsync(() => {
      pubsub.subscribe.and.callFake((cashoutbets, listeners, handler) => {
        if (listeners == 'BET_LEGS_LOADED') {
          handler("cashOutSection");
        }
      });
      component.ngOnInit();
      tick();

      expect(handleScoreboardsStatsUpdatesService.getStatisticsEventIds).toHaveBeenCalled();
      expect(cashOutSectionService.sendRequestForLastMatchFact).toHaveBeenCalledWith(component.bets);
      expect(component.bets[0].optaDisclaimerAvailable).toBeTruthy();
    }));

    it('should call lucky bonus subscription', fakeAsync(() => {
      pubsub.subscribe.and.callFake((cashoutbets, listeners, handler) => {
        if (listeners == 'LUCKY_BONUS') {
          handler("O/26382303/0000067");
        }
      });
      component.ngOnInit();
      tick();
    }));

    it('should not show opta disclaimer', fakeAsync(() => {
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({}))
      cashOutSectionService.generateBetsArray.and.returnValue([
        {
          eventSource: {
            event: ['111'],
            leg: [{ part: [{outcomeId: "666"}]}],
            eventEntity: { eventIsLive: true, comments:{home:{}} }
          },

        }
      ] as any);
      const newComponent = new CashOutBetsComponent(
        emaService,
        locale,
        cashOutSectionService,
        pubsub,
        windowRef,
        changeDetectorRef,
        betTrackingService,
        handleScoreboardsStatsUpdatesService,
        cmsService,
        betReuseService,
        storageService,
        user,
        nativeBridge,
        sessionService,
        device,
        gtmService
      );
      newComponent.bets = component.bets;
      newComponent.ngOnInit();
      tick();

      expect(handleScoreboardsStatsUpdatesService.getStatisticsEventIds).toHaveBeenCalled();
      expect(newComponent.bets[0].optaDisclaimerAvailable).toBeFalsy();
      expect(newComponent.bets[0].optaDisclaimerAvailable).toBeFalsy();
      expect(newComponent.winAlertsEnabled).toBeFalsy();
    }));

    it('should not call setAlertsConfig with bets as null', () => {
      spyOn<any>(component, 'setAlertsConfig');
      spyOn<any>(component, 'alertsListeners');
      component.bets = null;
      component.ngOnInit();

      expect(component['setAlertsConfig']).not.toHaveBeenCalled();
    });

    it('should not call setAlertsConfig with first bet as null', () => {
      spyOn<any>(component, 'setAlertsConfig');
      spyOn<any>(component, 'alertsListeners');
      component.bets = [null];
      component.ngOnInit();

      expect(component['setAlertsConfig']).not.toHaveBeenCalled();
    });

    it('should not call setAlertsConfig with first bet as null', () => {
      spyOn<any>(component, 'setAlertsConfig');
      spyOn<any>(component, 'alertsListeners');
      component.bets = [{eventSource: null}] as any;
      component.ngOnInit();

      expect(component['setAlertsConfig']).not.toHaveBeenCalled();
    });

    it('should call matchCommentaryUpdate',()=>{
      spyOn(component as any, 'matchCommentaryUpdate');
      component.ngOnInit();
      expect(component['matchCommentaryUpdate']).toHaveBeenCalled();
    });

    it('should set liveStreamOpened to false', () => {
      component.bets = [{ eventSource: { event: '123456', betId: '55',leg: [{  removedLeg: false,part: [{outcomeId: "666"}], eventEntity: { eventIsLive: true, comments:{home:{}} } }] } }] as any;
      component.ngOnInit();
    });
    
    it('should set liveStreamOpened to false where removedleg is true', () => {
      component.bets = [{ eventSource: {betId: '55', event: '123456', leg: [{legNo:'5', removedLeg: true, part: [{ outcomeId: "555" }], eventEntity: { eventIsLive: true, comments: { home: {} } }}] } }] as any;
      component.ngOnInit();
    });
    it('should set liveStreamOpened for widget', () => {
      component.isUsedFromWidget =true;
      component.bets = [{ eventSource: {betId: '55', event: '123456', leg: [{legNo:'5', removedLeg: true, part: [{ outcomeId: "555" }], eventEntity: { eventIsLive: true, comments: { home: {} } }}] } }] as any;
      component.ngOnInit();
    });

    it('bet as undefined', () => {
      component.bets = [undefined] as any;
      component.ngOnInit();
    });
    it('eventSource as undefined', () => {
      component.bets = [{ eventSource: undefined }] as any;
      component.ngOnInit();
    });
    describe('getSystemConfig - isSportIconEnabled', () => {
      it('getSystemConfig as undefined', () => {
        cmsService.getSystemConfig.and.returnValue(observableOf(undefined));

        const newComponent = new CashOutBetsComponent(
          emaService,
          locale,
          cashOutSectionService,
          pubsub,
          windowRef,
          changeDetectorRef,
          betTrackingService,
          handleScoreboardsStatsUpdatesService,
          cmsService,
          betReuseService,
          storageService,
          user,
          nativeBridge,
          sessionService,
          device,
          gtmService
        );

        expect(newComponent.isSportIconEnabled).not.toBeTrue();
      });
      it('getSystemConfig with CelebratingSuccess as undefined', () => {
        cmsService.getSystemConfig.and.returnValue(observableOf({ CelebratingSuccess: undefined }));

        const newComponent = new CashOutBetsComponent(
          emaService,
          locale,
          cashOutSectionService,
          pubsub,
          windowRef,
          changeDetectorRef,
          betTrackingService,
          handleScoreboardsStatsUpdatesService,
          cmsService,
          betReuseService,
          storageService,
          user,
          nativeBridge,
          sessionService,
          device,
          gtmService
        );

        expect(newComponent.isSportIconEnabled).not.toBeTrue();
      });
      it('getSystemConfig with displaySportIcon as undefined', () => {
        cmsService.getSystemConfig.and.returnValue(observableOf({ CelebratingSuccess: { displaySportIcon: undefined } }));

        const newComponent = new CashOutBetsComponent(
          emaService,
          locale,
          cashOutSectionService,
          pubsub,
          windowRef,
          changeDetectorRef,
          betTrackingService,
          handleScoreboardsStatsUpdatesService,
          cmsService,
          betReuseService,
          storageService,
          user,
          nativeBridge,
          sessionService,
          device,
          gtmService
        );

        expect(newComponent.isSportIconEnabled).not.toBeTrue();
      });
      it('getSystemConfig with isSportIconEnabled as true', () => {
        cmsService.getSystemConfig.and.returnValue(observableOf({ CelebratingSuccess: { displaySportIcon: ['cashoutbets'] } }));

        const newComponent = new CashOutBetsComponent(
          emaService,
          locale,
          cashOutSectionService,
          pubsub,
          windowRef,
          changeDetectorRef,
          betTrackingService,
          handleScoreboardsStatsUpdatesService,
          cmsService,
          betReuseService,
          storageService,
          user,
          nativeBridge,
          sessionService,
          device,
          gtmService
        );

        expect(newComponent.isSportIconEnabled).toBeTrue();
      });
    });
  });

  describe('ngOnChanges', () => {
    beforeEach(() => {
      spyOn<any>(component, 'init');
    });
    it('should call init method', () => {
      const changes: any = {
        betsMap: false,
        data: true
      };
      component.ngOnChanges(changes);
      expect(component['init']).toHaveBeenCalledTimes(1);
    });
    it('should not call init method', () => {
      const changes: any = {
        betsMap: false,
        data: null
      };
      component.ngOnChanges(changes);
      expect(component['init']).not.toHaveBeenCalledTimes(1);
    });
  });

  describe('Init', () => {
    it('should get static block if feature toggle is on', fakeAsync(() => {
      const betsMapMock = {value:{ bybType: '5-A-SIDE'}};
      cashOutSectionService.generateBetsMap.and.returnValue(betsMapMock);
      component.betTrackingEnabled = true;
      component.area = 'cashout-page';
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
      component.area = 'cashout-page';
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

  it('should clear listeners on destroy', () => {
    component['betTrackingEnabledSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component['channels'] = ['mFACTS123'];
    component['ctrlName'] = `CashoutWidgetController-${areaInput}`;
    component.ngOnDestroy();

    expect(cashOutSectionService.removeListeners).toHaveBeenCalledWith(`CashoutWidgetController-${areaInput}`);
    expect(pubsub.unsubscribe).toHaveBeenCalledWith(`CashoutWidgetController-${areaInput}`);
    expect(emaService.clearAccas).toHaveBeenCalled();
    expect(component['betTrackingEnabledSubscription'].unsubscribe).toHaveBeenCalled();
    expect(cashOutSectionService.removeHandlers).toHaveBeenCalledWith(['mFACTS123']);
  });
  it('should clear listeners on destroy not call cashOutSectionService.removeHandlers ', () => {
    component['betTrackingEnabledSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component['channels'] = null;
    component['ctrlName'] = `CashoutWidgetController-${areaInput}`;
    component.ngOnDestroy();

    expect(cashOutSectionService.removeListeners).toHaveBeenCalledWith(`CashoutWidgetController-${areaInput}`);
    expect(pubsub.unsubscribe).toHaveBeenCalledWith(`CashoutWidgetController-${areaInput}`);
    expect(emaService.clearAccas).toHaveBeenCalled();
    expect(component['betTrackingEnabledSubscription'].unsubscribe).toHaveBeenCalled();
    expect(cashOutSectionService.removeHandlers).not.toHaveBeenCalledWith(['mFACTS123']);
  });

  describe('@registerEventListeners', () => {
    beforeEach(() => {
      callbacks = {};
      spyOn<any>(component, 'updateBets');
      pubsub.subscribe.and.callFake((subscriber, key, fn) => {
        callbacks[key] = fn;
      });
    });

    it('should call removeCashoutItem and updateBets methods on event "LIVE_BET_UPDATE"', () => {
      component['registerEventListeners']();

      callbacks['LIVE_BET_UPDATE']();
      spyOn<any>(component, 'updateOptaDisclaimer');
      expect(cashOutSectionService.removeCashoutItemWithTimeout).toHaveBeenCalled();
      expect(component['updateBets']).toHaveBeenCalled();
    });

    it(`should updateBet, with isMyBetsInCasino as true and cashoutMsg as success`, () => {
      component['registerEventListeners']();
      const bet = {cashoutSuccessMessage: 'cashOutSuccessful'};
      component.isMyBetsInCasino = true;
      callbacks[pubsub.API.UPDATE_CASHOUT_BET](bet);
      spyOn<any>(component, 'updateOptaDisclaimer');
      expect(cashOutSectionService.updateBet).toHaveBeenCalled();
      expect(cashOutSectionService.updateBet).toHaveBeenCalledBefore(changeDetectorRef.detectChanges);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(windowRef.nativeWindow.parent.postMessage).toHaveBeenCalled();
    });

    it(`should updateBet, with isMyBetsInCasino false and cashoutMsg as success`, () => {
      component['registerEventListeners']();
      const bet = {cashoutSuccessMessage: 'cashOutSuccessful'};
      component.isMyBetsInCasino = false;
      callbacks[pubsub.API.UPDATE_CASHOUT_BET](bet);
      spyOn<any>(component, 'updateOptaDisclaimer');
      expect(cashOutSectionService.updateBet).toHaveBeenCalled();
      expect(cashOutSectionService.updateBet).toHaveBeenCalledBefore(changeDetectorRef.detectChanges);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(windowRef.nativeWindow.parent.postMessage).not.toHaveBeenCalled();
    });

    it(`should updateBet, with isMyBetsInCasino true and cashoutMsg as undefined`, () => {
      component['registerEventListeners']();
      const bet = {cashoutSuccessMessage: undefined};
      component.isMyBetsInCasino = true;
      callbacks[pubsub.API.UPDATE_CASHOUT_BET](bet);
      spyOn<any>(component, 'updateOptaDisclaimer');
      expect(cashOutSectionService.updateBet).toHaveBeenCalled();
      expect(cashOutSectionService.updateBet).toHaveBeenCalledBefore(changeDetectorRef.detectChanges);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(windowRef.nativeWindow.parent.postMessage).not.toHaveBeenCalled();
    });

    it(`should update the potential payout value on receiving PAYOUT_UPDATE`, () => {
      component.bets = [{eventSource: { betId: "12345", potentialPayout : 2.5 }},{eventSource: {betId: "1234", potentialPayout : 2.8 }}] as any;
      component['registerEventListeners']();
       const returnsResponse = {updatedReturns: [{returns: 0.09, betNo: '12345'}]};
       callbacks[pubsub.API.PAYOUT_UPDATE](returnsResponse);
       const findBet = component.bets.find((bet) =>{ return bet.eventSource.betId === '12345' });
       expect(findBet.eventSource.potentialPayout).toEqual(returnsResponse.updatedReturns[0].returns);
    });

    it(`should not update the potential payout value on receiving PAYOUT_UPDATE and eventSource is null`, () => {
      component.bets = [{},{}] as any;
      component['registerEventListeners']();
       const returnsResponse = {updatedReturns: [{returns: 0.09, betNo: '12345'}]};
       callbacks[pubsub.API.PAYOUT_UPDATE](returnsResponse);
       expect(component.bets.length).toEqual(2);
    });

    it(`should not update the potential payout value on receiving PAYOUT_UPDATE and betId is null`, () => {
      component.bets = [{eventSource: { }},{eventSource: { }}] as any;
      component['registerEventListeners']();
       const returnsResponse = {updatedReturns: [{returns: 0.09, betNo: '12345'}]};
       callbacks[pubsub.API.PAYOUT_UPDATE](returnsResponse);
       expect(component.bets.length).toEqual(2);
    });
    it(`should not update the potential payout value on receiving PAYOUT_UPDATE and returns are zero`,  fakeAsync(() => {
      component.bets = [{eventSource: { betId: "12345", potentialPayout : 2.5 }},{eventSource: {betId: "123", potentialPayout : 2.8 }}] as any;
      component['registerEventListeners']();
       const returnsResponse = {updatedReturns: [{returns: 0, betNo: '12345'}]};
       callbacks[pubsub.API.PAYOUT_UPDATE](returnsResponse);
       tick();
       const findBet = component.bets.find((bet) =>bet.eventSource.betId === returnsResponse.updatedReturns[0].betNo);
       expect(findBet.eventSource.potentialPayout).toEqual('N/A');
    }));
    it(`should not update the potential payout value on receiving PAYOUT_UPDATE and returns are positive`, fakeAsync(() => {
      component.bets = [{eventSource: { betId: "12345", potentialPayout : 2.5 }},{eventSource: {betId: "123", potentialPayout : 2.8 }}] as any;
      component['registerEventListeners']();
       const returnsResponse = {updatedReturns: [{returns: 2, betNo: '12345'}]};
       callbacks[pubsub.API.PAYOUT_UPDATE](returnsResponse);
       tick();
       const findBet = component.bets.find((bet) =>bet.eventSource.betId === returnsResponse.updatedReturns[0].betNo);
       expect(findBet.eventSource.potentialPayout).toEqual(2);
    }));
  });

  it('isCashoutError should call isCashoutError method of cashout section service', () => {
    component['isCashoutError']({} as any);
    expect(cashOutSectionService.isCashoutError).toHaveBeenCalled();
  });

  it('getCashoutError should call getCashoutError method of cashout section service', () => {
    component['getCashoutError']({} as any);
    expect(cashOutSectionService.getCashoutError).toHaveBeenCalled();
  });

  it('#updateOptaDisclaimer update true condition', () => {
    component.bets = [{ eventSource: {event:['123456']} }] as any;
    component['updateOptaDisclaimer']();
    expect(component.bets[0].optaDisclaimerAvailable).toBe(true);
  });

  it('#updateOptaDisclaimer update false condition', () => {
    component.bets = [{ eventSource: {event:['123456567']} }] as any;
    component['updateOptaDisclaimer']();
    expect(component.bets[0].optaDisclaimerAvailable).toBe(undefined);
  });

  describe('#isShownDisclaimer', () => {
    it('isShownDisclaimer true', () => {
      component.dataDisclaimer = { enabled: true } as any;
      const bet = { eventSource: { leg: [{ eventEntity: { eventIsLive: true, comments:{home:{}} } }] } } as any;
      const result = component.isShownDisclaimer(bet);
      expect(result).toBe(true);
    })
    it('isShownDisclaimer false of cms ', () => {
      component.dataDisclaimer = { enabled: false } as any;
      const bet = { eventSource: { leg: [{ eventEntity: { eventIsLive: true, comments:null } }] } } as any;
      const result = component.isShownDisclaimer(bet);
      expect(result).toBe(false);
    })
    it('isShownDisclaimer nolive', () => {
      component.dataDisclaimer = { enabled: true } as any;
      const bet = { eventSource: { leg: [{ eventEntity: { eventIsLive: false, comments:{} } }] } } as any;
      const result = component.isShownDisclaimer(bet);
      expect(result).toBe(false);
    })
    it('isShownDisclaimer comments null', () => {
      component.dataDisclaimer = { enabled: true } as any;
      const bet = { eventSource: { leg: [{ eventEntity: { eventIsLive: true, comments:null } }] } } as any;
      const result = component.isShownDisclaimer(bet);
      expect(result).toBe(false);
    })
  })
  describe('#matchCommentaryUpdate', () => {
    it('should subscribe when var-data is available and matchCommentaryDataUpdate', () => {
      const varDataUpdate = { varEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      component.bets = [{ eventSource: { event: ['12345'], leg: [{ eventEntity: { id: 12345 }, part: [{ outcome: [{}] }] }] } }] as any;
      pubsub.subscribe.and.callFake((cashoutbets, listeners, handler) => {
        if (listeners == 'UPDATE_MATCHCOMMENTARY_DATA') {
          handler(varDataUpdate);
        }
      });
      component['matchCommentaryUpdate']();
      expect(pubsub.subscribe).toHaveBeenCalledWith(component['ctrlName'], 'UPDATE_MATCHCOMMENTARY_DATA', jasmine.any(Function));
      expect(cashOutSectionService.matchCommentaryDataUpdate).toHaveBeenCalledOnceWith(component.bets,varDataUpdate);
    });
 });
 describe('#reuseBets', () => {
   it('should call reuse service and add bets to bet slip', fakeAsync(() => {
    betReuseService.reuse.and.returnValue(Promise.resolve());
     const bet = {
       eventSource: {
          betId: 8237238,
          leg: [{
            status: "open",
            removedLeg: false,
            part: [{
              outcomeId: 123132
            }]
          }]
       }
     } as any;
     component.reuseBets(bet);
     expect(component.reuseBets).toBeTruthy();
     tick();
   }));
 });

  describe('#alertsListeners', () => {
    it('alertsListeners', fakeAsync(() => {
      callbackHandler = (ctrlName: string, eventName: string, callback) => {
        if(['HOME_BETSLIP'].includes(eventName)) {
          callback();
        }
      };
      pubsub.subscribe.and.callFake(callbackHandler);

      component.ngOnInit();
      tick();
      expect(pubsub.subscribe).toHaveBeenCalledWith(
        component['ctrlName'], pubSubApi.HOME_BETSLIP, jasmine.any(Function)
      );
    }));

    it('alertsListeners', fakeAsync(() => {
      component.lazyLoadedBets = [{id: 1}, {id: 2}] as any;
      component.selectCashoutTab = jasmine.createSpy();
      component['sessionStateDefined'] = true;

      component.ngOnInit();
      tick();

      expect(component.selectCashoutTab).toHaveBeenCalledTimes(6);
      expect(pubsub.subscribe).toHaveBeenCalledWith(
        component['ctrlName'], pubsub.API.SUCCESSFUL_LOGIN, jasmine.any(Function)
      );
      expect(sessionService.whenSession).toHaveBeenCalled();
      expect(pubsub.subscribe).toHaveBeenCalledWith(
        component['ctrlName'], pubsub.API.SESSION_LOGOUT, jasmine.any(Function)
      );
      expect(pubsub.subscribe).toHaveBeenCalledWith(
        component['ctrlName'], pubSubApi.HOME_BETSLIP, jasmine.any(Function)
      );
      expect(pubsub.subscribe).toHaveBeenCalledWith(
        component['ctrlName'], pubSubApi.BET_EVENTENTITY_UPDATED, jasmine.any(Function)
      );
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
    }));

    it('ngOnInit (whenSession error #1)', fakeAsync(() => {
      sessionService.whenSession.and.returnValue(Promise.reject());
      component.selectCashoutTab = jasmine.createSpy();

      component.ngOnInit();
      tick();
      expect(component.selectCashoutTab['calls'].count()).toBe(4);
    }));

    it('ngOnInit (whenSession error #2)', fakeAsync(() => {
      sessionService.whenSession.and.returnValue(Promise.reject('error msg'));
      component.selectCashoutTab = jasmine.createSpy();

      component.ngOnInit();
      tick();
      expect(component.selectCashoutTab['calls'].count()).toBe(4);
    }));
  });

  describe('setAlertsConfig', () => {
    it('should NOT call multipleEventPageLoaded - bet not found', () => {
      const bets = [{eventSource: {betId: 'test'}}] as any;

      component['setAlertsConfig'](bets);
      expect(nativeBridge['multipleEventPageLoaded']).not.toHaveBeenCalled();
    });

    it('should hasOnEventAlertsClick - false, hasShowFootballAlerts - true', () => {
      nativeBridge.hasOnEventAlertsClick.and.returnValue(false);
      const bets = [{eventSource: {betId: 'test'}}] as any;

      component['setAlertsConfig'](bets);
      expect(nativeBridge['multipleEventPageLoaded']).not.toHaveBeenCalled();
    });

    it('should call multipleEventPageLoaded with football category name', () => {
      component.bets.push({ eventSource: { betId: '551', event: 'test123', leg: [{ part: [{outcomeId: "555"}], eventEntity: {  id: 'test123', eventIsLive: true, comments:{home:{}}, categoryCode: 'football', 
      eventSortCode: 'test', categoryId: '16', typeName: "league", categoryName: 'test categoryName' } }],
      betType: 'SGL', receipt: '0000/1234/123456' } } as any);

      component['setAlertsConfig'](component.bets);
      expect(nativeBridge['multipleEventPageLoaded']).toHaveBeenCalledWith(['123456', 'test123'], 'test categoryname');
    });

    it('should not call multipleEventPageLoaded with MOTOR_SPORTS as outright categoryCode', () => {
      component.bets= [{ eventSource: { betId: '551', event: 'test123', leg: [{ part: [{outcomeId: "555"}], eventEntity: {  id: 'test123', eventIsLive: true, comments:{home:{}}, categoryCode: 'MOTOR_SPORTS', 
      eventSortCode: 'test', categoryId: '16', typeName: "league", categoryName: 'test categoryName' } }],
      betType: 'SGL', receipt: '0000/1234/123456' } }] as any;

      component['setAlertsConfig'](component.bets);
      expect(nativeBridge['multipleEventPageLoaded']).not.toHaveBeenCalledWith(['123456', 'test123'], 'test categoryname');
    });


    it('should call setAlertsConfig - no allowedLeaguesList ', () => {
      cmsService.getFeatureConfig.and.returnValue(observableOf({
          visibleNotificationIcons: {
            multiselectValue: ['android'],
            value: ['android']
        },
        displayOnMyBets: ['android']
      }));
      component.bets.push({ eventSource: { betId: '551', event: 'test123', leg: [{ part: [{outcomeId: "555"}], eventEntity: {  id: 'test123', eventIsLive: true, comments:{home:{}}, categoryCode: 'football', 
      eventSortCode: 'test', categoryId: '16', typeName: "league", categoryName: 'test categoryName' } }],
      betType: 'SGL', receipt: '0000/1234/123456' } } as any);

      component['setAlertsConfig'](component.bets);
      expect(nativeBridge.multipleEventPageLoaded).not.toHaveBeenCalled();
    });

    it('should NOT do football Alerts Visible if no configuration in CMS', () => {
      spyOn<any>(component, 'setFootballAlerts').and.callThrough();
      cmsService.getFeatureConfig.and.returnValue(observableOf({
        visibleNotificationIcons: {
          multiselectValue: ['test'],
          value: 'test'
      },
      displayOnMyBets: ['test']
      }));

      component['setAlertsConfig'](component.bets);
      expect(component['setFootballAlerts']).not.toHaveBeenCalled();
    });

    it('should NOT do football Alerts Visible if no configuration in CMS', () => {
      cmsService.getFeatureConfig.and.returnValue(observableOf({
          visibleNotificationIcons: { }
      }));

      component['setAlertsConfig'](component.bets);
      expect(cmsService.getFeatureConfig).toHaveBeenCalled();
    });

    it('should get visible notification icons from sport types', () => {
      cmsService.getFeatureConfig.and.returnValue(observableOf({
          visibleNotificationIcons: {
            multiselectValue: ['android'],
            value: 'league'
        }
      }));

      component['setAlertsConfig'](component.bets);
      expect(cmsService.getFeatureConfig).toHaveBeenCalled();
    });
  });

  describe('handleFootballAlerts', () => {
    it('handleFootballAlerts - with matching eventid', () => {
      component['deviceMatchAlerts'] = [{eventId: "123456"}] as any;
      const data = {detail: [{eventId: "123456", isEnabled: true}]} as any;

      component['handleFootballAlerts'](data);
      expect(component['deviceMatchAlerts'][0].isEnabled).toBeTrue();
      expect(component['bets'][0].footballBellActive).toBeTrue();
    });

    it('handleFootballAlerts - without matching eventid', () => {
      component['deviceMatchAlerts'] = [{eventId: "123456"}] as any;
      const data = {detail: [{eventId: "3", isEnabled: true}]} as any;

      component['handleFootballAlerts'](data);
      expect(component['bets'][0].footballBellActive).toBeFalsy();
    });
  });

  describe('GTM', () => {
    it('onFootballBellClick', () => {
      spyOn<any>(component, 'sendGTMMatchAlertClick').and.callThrough();
      const data = component.bets[0];
      const event = data.eventSource.leg[0].eventEntity;

      component['onFootballBellClick'](data);

      expect(nativeBridge['onEventAlertsClick']).toHaveBeenCalledWith(event.id.toString(),
      event.categoryName.toLocaleLowerCase(),
      event.categoryId,
      event.drilldownTagNames,
      ALERTS_GTM.CASHOUT);
      expect(nativeBridge['showFootballAlerts']).toHaveBeenCalled();
      expect(component['sendGTMMatchAlertClick']).toHaveBeenCalledWith(data);
    });

    it('handleAlertInfoClick', () => {
      spyOn<any>(component, 'sendGTMAlerts').and.callThrough();
      const bet = component.bets[0];
      const gtmData = {
        'component.ActionEvent': ALERTS_GTM.CLICK,
        'component.PositionEvent': ALERTS_GTM.NA,
        'component.EventDetails': ALERTS_GTM.WIN_ALERT_ICON
      };

      component['handleAlertInfoClick'](bet);

      expect(component['sendGTMAlerts']).toHaveBeenCalledWith(gtmData, bet);
    });

    it('sendGTMWinAlertToggle - enabled - false', () => {
      spyOn<any>(component, 'sendGTMAlerts').and.callThrough();
      const bet = component.bets[0];
      const gtmData = {
        'component.ActionEvent': ALERTS_GTM.TOGGLE_OFF,
        'component.PositionEvent': ALERTS_GTM.CASHOUT,
        'component.EventDetails': ALERTS_GTM.WIN_ALERT
      };

      component['sendGTMWinAlertToggle'](false, bet);

      expect(component['sendGTMAlerts']).toHaveBeenCalledWith(gtmData, bet);
    });
  });

  describe('handleWinAlerts', () => {
    it('handleWinAlerts', () => {
      const data = {detail: ["0000/1234/12345"]} as any;
      
      component['handleWinAlerts'](data);

      expect(component['deviceWinAlerts']).toEqual(data.detail);
      expect(component['bets'][0].winAlertsActive).toBeTrue();
    });

    it('handleWinAlerts - data - undefined', () => {
      component['deviceWinAlerts'] = ['dummy'];
      
      component['handleWinAlerts']();

      expect(component['bets'][0].winAlertsActive).toBeFalsy();
    });
  });

  describe('toggleWinAlerts', () => {
    it('toggleWinAlerts - winAlertsToggled - true', () => {
      const bet = component.bets[0];
      
      component['toggleWinAlerts'](bet, true);

      expect(user['set']).not.toHaveBeenCalled();
    });
    it('toggleWinAlerts - winAlertsToggled - false', () => {
      user.winAlertsToggled = false;
      const bet = component.bets[0];
      
      component['toggleWinAlerts'](bet, true);

      expect(user['set']).toHaveBeenCalledWith({ winAlertsToggled: true });
    });
  });

  describe('setWinAlertsBets', () => {
    it('setWinAlertsBets - winAlertsReceiptId - value', () => {
      component['winAlertsReceiptId'] = '000/123/1234';
      const bet = component.bets[0];
      const receipt = bet.eventSource.receipt;
      
      component['setWinAlertsBets'](bet, true);

      expect(component['winAlertsReceiptId']).not.toEqual(receipt);
    });
    it('setWinAlertsBets - value - false', () => {
      const bet = component.bets[0];
      const receipt = bet.eventSource.receipt;
      component['winAlertsReceiptId'] = '000/123/1234';
      component['winAlertsBets'] = ['1', receipt, '2'];
      component['deviceWinAlerts'] = ['1', receipt, '3'];
      
      component['setWinAlertsBets'](bet, false);

      expect(component['winAlertsBets']).toEqual(['1', '2']);
      expect(component['deviceWinAlerts']).toEqual(['1', '3']);
    });
  });

  it('setToggleSwitchId', () => {
    const bet = component.bets[0];
    
    const toggleSwitch = component['setToggleSwitchId'](bet);

    expect(toggleSwitch).toEqual('toggle-switch-regularbets-12345');
  });

  describe('#showWinAlertsTooltip', () => {
    it('showWinAlertsTooltip should be true', () => {
      user.winAlertsToggled = false;
      const result = component.showWinAlertsTooltip();
      expect(result).toBeTruthy();
    });
    it('showWinAlertsTooltip should be false', () => {
      storageService.get.and.returnValue({ 'receiptViewsCounter-test': 2 });
      const result = component.showWinAlertsTooltip();
      expect(result).toBeFalsy();
    });
  });

  describe('#selectCashoutTab', () => {
    it('selectCashoutTab - name - test', () => {
      component.winAlertsEnabled = true;
      component['winAlertsBets'] = ['1'];
      component['winAlertsReceiptId'] = '1';
      component['mode'] = component.MODES.cashout;

      user.winAlertsToggled = false;
      component.selectCashoutTab('test');
      expect(component['mode']).toBe('test');
      expect(component['winAlertsBets'].length).toEqual(0);
      expect(component['winAlertsReceiptId']).toBeFalsy();
      expect(nativeBridge['onActivateWinAlerts']).toHaveBeenCalledWith('1', ['1']);
    });
  });
  
  describe('#updateBets', () => {
    it('updateBets - isFirstLoad - false', () => {
      component['isFirstLoad'] = false;

      component['updateBets']();
      expect(nativeBridge['winAlertsStatus']).not.toHaveBeenCalled();
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
