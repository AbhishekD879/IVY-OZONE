import { of as observableOf, of, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { RegularBetsComponent } from '@app/betHistory/components/regularBets/regular-bets.component';
import { cashoutConstants } from '../../constants/cashout.constant';
import { contestBets, initialBets, regularBets } from './regular-bets.mock';
import environment from '@environment/oxygenEnvConfig';
import { NavigationEnd } from '@angular/router';
import { ALERTS_GTM } from '@app/betHistory/constants/bet-leg-item.constant';

describe('RegularBetsComponent', () => {
  let component: RegularBetsComponent,
    locale,
    cashOutSectionService,
    pubsub,
    emaService,
    callbackHandler,
    windowRef,
    betTrackingService,
    changeDetectorRef,
    handleScoreboardsStatsUpdatesService,
    betFinderHelperService,
    cmsService,
    betReuseService,
    storageService,
    user,
    device,
    nativeBridge,
    sessionService,
    gtmService,
    currencyPipe,
    timeService,
    betHistoryMainService,
    sessionStorageService,
    router, location;

  const content = 'static block content';
  const areaInput = 'open-bets-page';
  

  beforeEach(() => {
    callbackHandler = (ctrlName: string, eventName: string, callback) => {
      if (['LIVE_BET_UPDATE', 'SESSION_LOGOUT', 'BETSLIP_UPDATED', 'BET_EVENTENTITY_UPDATED'].includes(eventName)) {
        callback && callback({});
      } else if(eventName === 'UPDATE_CASHOUT_BET') {
        callback('bet');
      } else if(eventName === 'LIVE_STREAM_BIR') {
        callback({legId:'555',flag:true,isUsedFromWidget:true});
        callback({legId:'555',flag:false,isUsedFromWidget:true});
        callback({legId:'555',flag:false,isUsedFromWidget:false});
      } else if(['SUCCESSFUL_LOGIN', 'HOME_BETSLIP'].includes(eventName)) {
        callback('cashout');
      } else if(eventName === 'PAYOUT_UPDATE') {
        callback({updatedReturns : [{betNo:'12345', returns: 2}]});
      }
    };

    emaService = {
      clearAccas: jasmine.createSpy('emaService.clearAccas')
    };
    locale = {
      getString: jasmine.createSpy().and.callFake(x=>{
        if(x === 'bethistory.noOpenBetsToday'){
          return 'No open bets placed today.';
        }
        else{
          return 'No Open bets In specified time range';
        }
      }),
    };
    cashOutSectionService = {
      updateBet: jasmine.createSpy(),
      createDataForRegularBets: jasmine.createSpy(),
      getLeaderBoardConfig: jasmine.createSpy('getLeaderBoardConfig'),
      generateBetsMap: jasmine.createSpy('generateBetsMap').and.returnValue({'123': { potentialPayout: "N/A"}, '12345': {potentialPayout: "N/A"}}),
      generateBetsArray: jasmine.createSpy().and.returnValue(
        [
          {
            eventSource: {
              event: ['123456'],
              leg: [{ part: [{ outcome: [{}] }] }],
              eventEntity: { id: "123456", eventIsLive: true, comments:{home:{}}, categoryCode: 'football', 
                eventSortCode: 'test', categoryId: '16', typeName: "league", categoryName: 'test categoryName' }, 
              betType: 'SGL',
              receipt: '0000/1234/12345',
              betId: '55'
            }
          }
          ] as any),
      removeListeners: jasmine.createSpy(),
      registerController: jasmine.createSpy(),
      removeCashoutItemWithTimeout: jasmine.createSpy().and.returnValue(observableOf()),
      isCashoutError: jasmine.createSpy('isCashoutError'),
      getCashoutError: jasmine.createSpy('getCashoutError'),
      matchCommentaryDataUpdate: jasmine.createSpy('matchCommentaryDataUpdate'),
      sendRequestForLastMatchFact: jasmine.createSpy('sendRequestForLastMatchFact').and.returnValue(['mFACTS1234']),
      removeHandlers: jasmine.createSpy('removeHandlers'),
      setToolTipStatus: jasmine.createSpy('setToolTipStatus'),
      getInitialStake:jasmine.createSpy('getInitialStake')
    };
    windowRef = {
      nativeWindow: {
        setInterval: jasmine.createSpy().and.callFake((callback) => {
          callback && callback();
        }),
        clearInterval: jasmine.createSpy(),
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
    changeDetectorRef = {
      detectChanges: jasmine.createSpy(),
      detach: jasmine.createSpy()
    };
    pubsub = {
      subscribe: jasmine.createSpy('subscribe').and.callFake(callbackHandler),
      API: pubSubApi,
      unsubscribe: jasmine.createSpy(),
      publish: jasmine.createSpy('publish')
    };
    betTrackingService = {
      isTrackingEnabled: jasmine.createSpy('isTrackingEnabled').and.returnValue(observableOf(true)),
      getStaticContent: jasmine.createSpy('getStaticContent').and.returnValue(observableOf(content)),
    };
    handleScoreboardsStatsUpdatesService = {
      getStatisticsEventIds: jasmine.createSpy('getStatisticsEventIds').and.returnValue(observableOf('123456'))
    };
    cmsService = {
      getFeatureConfig:jasmine.createSpy('getFeatureConfig').and.returnValue(observableOf({
        visibleNotificationIconsFootball: {
          multiselectValue: ['android'],
          value: 'league'
        },
        displayOnMyBets: ['android']
    })),
      isBogFromCms: jasmine.createSpy('isBogFromCms').and.returnValue(of(true)),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({ScoreboardsDataDisclaimer:{enabled: true, dataDisclaimer: 'Transmission delayed'}, winAlerts: {displayOnMyBets: ['android']}, CelebratingSuccess: {displayCashoutProfitIndicator: true}}))
    };
    betFinderHelperService = {
      getContestIdsForFiveASideBets: jasmine.createSpy('getContestIdsForFiveASideBets').and.returnValue(observableOf([
        {
          betId: '2379097305',
          contestId: '60eb075772149d6475386619'
        },
        {
          betId: '2379096729',
          contestId: 'NA'
        }
      ]))
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

    currencyPipe = {
      transform: jasmine.createSpy().and.callFake((value, currencySymbol) => `${value}${currencySymbol}`)
    };
    betHistoryMainService = {
      getCelebrationBanner: jasmine.createSpy('getCelebrationBanner').and.returnValue({})
    };
    
    timeService = {
      getLocalDateFromString: jasmine.createSpy().and.returnValue('2019-03-04T16:30:45.000Z')
    };

    sessionStorageService = {
      get: jasmine.createSpy('get'),
      remove: jasmine.createSpy('remove')
    }
    
    router = {
      events: of(new NavigationEnd(1, '/', '/')),
    };

    location = {
      path: jasmine.createSpy().and.returnValue('')
    };

    component = new RegularBetsComponent(
      emaService,
      locale,
      cashOutSectionService,
      windowRef,
      changeDetectorRef,
      pubsub,
      betTrackingService,
      handleScoreboardsStatsUpdatesService,
      cmsService,
      betFinderHelperService,
      sessionStorageService,
      router,
      location,
      betReuseService,
      storageService,
      user,
      device,
      nativeBridge,
      sessionService,
      gtmService,
      currencyPipe,
      timeService,
      betHistoryMainService
    );
    component.bets = [{ eventSource: { betId: '55', event: '123456', leg: [{ legNo:5,part: [{outcomeId: "555"}], eventEntity: {  id: '123456', eventIsLive: true, comments:{home:{}}, categoryCode: 'football', 
    eventSortCode: 'test', categoryId: '16', typeName: "league", categoryName: 'test categoryName' } }],
    betType: 'SGL', receipt: '0000/1234/12345' } }] as any;
  });

  it('should set displayProfitIndicator - true', () => {
    expect(component.displayProfitIndicator).toBeTrue();
  });

  describe('ngOnInit', () => {
    it('should ini bets map', fakeAsync(() => {
      spyOn<any>(component, 'setActiveEvent');
      pubsub.subscribe.and.callFake((cashoutbets, listeners, handler) => {
        if (listeners == 'BET_LEGS_LOADED') {
          handler('openBets');
        }
      });
      location.path.and.returnValue('/bet-history');
      component.ngOnInit();
      tick();

      expect(cashOutSectionService.generateBetsMap).toHaveBeenCalled();
      expect(cashOutSectionService.sendRequestForLastMatchFact).toHaveBeenCalledWith(component.bets);
      expect(component.betsMap).toBeTruthy();
    }));

    it('should subscribe lucky bonus', fakeAsync(() => {
      spyOn<any>(component, 'setActiveEvent');
      pubsub.subscribe.and.callFake((cashoutbets, listeners, handler) => {
        if (listeners == 'LUCKY_BONUS') {
          handler('O/26382303/0000067');
        }
      });
      component.ngOnInit();
      tick();
    }));

    it('should not sync with cashout update flow on settled tab', () => {
      component.isBetHistoryTab = true;
      spyOn<any>(component, 'setActiveEvent');
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({}));
      component.ngOnInit();

      expect(pubsub.subscribe).not.toHaveBeenCalledWith(jasmine.any(String), 'LIVE_BET_UPDATE', jasmine.any(Function));
    });

    it('should create componnet and winAlertsEnabled - false', fakeAsync(() => {
      cashOutSectionService.generateBetsArray.and.returnValue([
        {
          eventSource: {
            event: ['111'],
            leg: [{ part: [{outcomeId: "666"}]}],
            eventEntity: { eventIsLive: true, comments:{home:{}} }
          },

        }
      ] as any);
      
      cmsService.getSystemConfig.and.returnValue(observableOf({winAlerts: {displayOnMyBets: ['android']}}))
      const newComponent = new RegularBetsComponent(
        emaService,
        locale,
        cashOutSectionService,
        windowRef,
        changeDetectorRef,
        pubsub,
        betTrackingService,
        handleScoreboardsStatsUpdatesService,
        cmsService,
        betFinderHelperService,
        sessionStorageService,
        router,
        location,
        betReuseService,
        storageService,
        user,
        device,
        nativeBridge,
        sessionService,
        gtmService,
        currencyPipe,
        timeService,
        betHistoryMainService

      );
      newComponent.bets = component.bets;
      tick();

      expect(newComponent.winAlertsEnabled).toBeTrue();
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

    it('should sync with cashout update flow extending passed params', () => {
      spyOn<any>(component, 'setActiveEvent');
      component.isBetHistoryTab = false;
      component.ngOnInit();

      expect(pubsub.subscribe).toHaveBeenCalledWith(jasmine.any(String), 'LIVE_BET_UPDATE', jasmine.any(Function));
      expect(cashOutSectionService.removeCashoutItemWithTimeout).toHaveBeenCalled();
      const args = cashOutSectionService.removeCashoutItemWithTimeout.calls.argsFor(0);
      expect(args[0]).toEqual(jasmine.any(Object));
      expect(args[1]).toEqual(jasmine.any(Object));
      expect(args[1].isRegularBets).toBeTruthy();
    });

    it('should show opta disclaimer', fakeAsync(() => {
      spyOn<any>(component, 'setActiveEvent');
      cashOutSectionService.generateBetsArray.and.returnValue([
        {
          eventSource: {
            event: ['123456'],
            leg: [{ part: [{ outcome: [{}] }] }]
          }
        }
      ] as any);
      component.ngOnInit();

      tick();
      expect(handleScoreboardsStatsUpdatesService.getStatisticsEventIds).toHaveBeenCalled();
      expect(component.bets[0].optaDisclaimerAvailable).toBeTruthy();
    }));
    describe('liveStreamOpened ',() => {
      it('should set liveStreamOpened to false', () => {
        component.bets = [{ eventSource: { event: '123456',betId:55, leg: [{ removedLeg: false,legNo:5, part: [{outcomeId: "666"}], eventEntity: { eventIsLive: true, comments:{home:{}} } }] } }] as any;
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
      it('should set liveStreamOpened for widget', () => {
        component.isUsedFromWidget =true;
       // component.bets = [{ eventSource: {betId: '12345', event: '123456', leg: [{legNo:'5', removedLeg: true, part: [{ outcomeId: "555" }], eventEntity: { eventIsLive: true, comments: { home: {} } }}] } }] as any;
        component.ngOnInit();
      });
    });

    it('should not show opta disclaimer', fakeAsync(() => {
      spyOn<any>(component, 'setActiveEvent');
      cashOutSectionService.generateBetsArray.and.returnValue([
        {
          eventSource: {
            event: ['654321'],
            leg: [{ part: [{ outcome: [{}] }] }]
          }
        }
      ] as any);
      component.ngOnInit();

      tick();
      expect(handleScoreboardsStatsUpdatesService.getStatisticsEventIds).toHaveBeenCalled();
      expect(component.bets[0].optaDisclaimerAvailable).toBeFalsy();
    }));

    describe('Should check isBogEnabled', () => {
      it('should check isBogEnabled when  isBogFromCms() = true', () => {
        component.ngOnInit();
        expect(component.isBogEnabledFromCms).toBe(true);
      });
      it('should check isBogEnabled when isBogFromCms() = false', () => {
        cmsService.isBogFromCms = jasmine.createSpy('isBogFromCms').and.returnValue(of(false));
        component.ngOnInit();

        expect(component.isBogEnabledFromCms).toBe(false);
      });
    });

    it('should add the contest ids to the five aside bets ', fakeAsync(() => {
      spyOn<any>(component, 'setActiveEvent');
      environment.brand = 'ladbrokes';
      cashOutSectionService.generateBetsArray.and.returnValue( initialBets as any);
      component.ngOnInit();

      tick();
      expect(betFinderHelperService.getContestIdsForFiveASideBets).toHaveBeenCalled();
      expect(component.bets).toEqual(contestBets as any);
      expect(component.loadingContestIds).toBe(false);
    }));

    it('should add the contest ids to the five aside bets if brand is not ladbrokes ', fakeAsync(() => {
      spyOn<any>(component, 'setActiveEvent');
      environment.brand = 'bma';
      cashOutSectionService.generateBetsArray.and.returnValue( initialBets as any);
      component.ngOnInit();

      tick();
      expect(component.bets).toEqual(contestBets as any);
      expect(component.loadingContestIds).toBe(false);
    }));


    it('should not add the contest ids to the five aside bets if there is a error', fakeAsync(() => {
      spyOn<any>(component, 'setActiveEvent');
      spyOn<any>(console, 'error');
      environment.brand = 'ladbrokes';
      component.bets = undefined;
      cashOutSectionService.generateBetsArray.and.returnValue( initialBets as any);
      betFinderHelperService.getContestIdsForFiveASideBets.and.returnValue(throwError('error'));
      component.ngOnInit();

      tick();
      expect(betFinderHelperService.getContestIdsForFiveASideBets).toHaveBeenCalled();
      expect(console.error).toHaveBeenCalled();
      expect(component.loadingContestIds).toBe(false);
    }));
    it('should call matchCommentaryUpdate',()=>{
      spyOn(component as any, 'matchCommentaryUpdate');
      component.ngOnInit();
      expect(component['matchCommentaryUpdate']).toHaveBeenCalled();
    });
  });

  describe('isLdipBetTag', () =>{
    it('should return value if LDIP tag is available', () =>{
      const bet = { eventSource: { betTags:{ betTag: [{tagName: 'LDIP'}]} }};
      const result = component.isLdipBetTag(bet);
      expect(result).toBeTruthy();
    });
    it('should return value if LDIP tag is not available', () =>{
      const bet = { eventSource: {}};
      const result = component.isLdipBetTag(bet);
      expect(result).toBeFalsy();
    });
    it('should return value if eventSource tag is not available', () =>{
      const bet = {};
      const result = component.isLdipBetTag(bet);
      expect(result).toBeFalsy();
    });
  });

  describe('Init', () => {
    it('should get static block if feature toggle is on', fakeAsync(() => {
      spyOn(component as any, 'setActiveEvent');
      const betsMapMock = {value:{ bybType: '5-A-SIDE'}};
      cashOutSectionService.generateBetsMap.and.returnValue(betsMapMock);
      component.betTrackingEnabled = true;
      component.area = 'open-bets-page';
      component.isUsedFromWidget = true;
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
      spyOn(component as any, 'setActiveEvent');
      const betsMapMock = {value:{ bybType: '5-A-SIDE'}};
      cashOutSectionService.generateBetsMap.and.returnValue(betsMapMock);
      betTrackingService.isTrackingEnabled.and.returnValue(observableOf(false));
      component.area = 'open-bets-page';
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

  it('cashout updateBet', () => {
    component.area = areaInput;
    spyOn(component as any, 'setActiveEvent');
    component.ngOnInit();

    expect(cashOutSectionService.updateBet).toHaveBeenCalledTimes(1);
    expect(cashOutSectionService.updateBet).toHaveBeenCalledWith('bet', [
      ({
        eventSource: ({
          event: ['123456'], leg:
            [({
              part: [(
                { outcome: [{}] })]
            })],
          eventEntity: ({
            id: '123456', eventIsLive: true, comments: (
              { home: ({}) }),
            categoryCode: 'football', eventSortCode: 'test', categoryId: '16', typeName: 'league',
            categoryName: 'test categoryName'
          }), betType: 'SGL', receipt: '0000/1234/12345', betId: '55'
        }),
        optaDisclaimerAvailable: true,
        footballAlertsVisible: false
      })
    ] as any);

    expect(changeDetectorRef.detectChanges).toHaveBeenCalledTimes(3);

    expect(cashOutSectionService.registerController).toHaveBeenCalledTimes(1);
    expect(cashOutSectionService.registerController).toHaveBeenCalledWith(`${cashoutConstants.controllers.REGULAR_BETS_CTRL}-${areaInput}`);

    expect(cashOutSectionService.createDataForRegularBets).toHaveBeenCalledTimes(1);
    expect(cashOutSectionService.generateBetsArray).toHaveBeenCalled();
  });

  it(`should updateBet when UPDATE_CASHOUT_BET and define detectListener, with isMyBetsInCasino as true and cashoutMsg as success`, () => {
    spyOn<any>(component, 'setActiveEvent');
    delete component['detectListener'];
    const callbacks = {};
    pubsub.subscribe.and.callFake((subscriber, key, fn) => {
      callbacks[key] = fn;
    });
    windowRef.nativeWindow.setInterval.and.returnValue(123);
    component.ngOnInit();
    const bet = {cashoutSuccessMessage: 'cashOutSuccessful'};
    component.isMyBetsInCasino = true;
    callbacks[pubsub.API.UPDATE_CASHOUT_BET](bet);

    expect(cashOutSectionService.updateBet).toHaveBeenCalled();
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    expect(windowRef.nativeWindow.parent.postMessage).toHaveBeenCalled();
    expect(component['detectListener']).toEqual(123);
  });

  it(`should updateBet when UPDATE_CASHOUT_BET and define detectListener, with isMyBetsInCasino as false and cashoutMsg as success`, () => {
    spyOn<any>(component, 'setActiveEvent');
    delete component['detectListener'];
    const callbacks = {};
    pubsub.subscribe.and.callFake((subscriber, key, fn) => {
      callbacks[key] = fn;
    });
    windowRef.nativeWindow.setInterval.and.returnValue(123);
    component.ngOnInit();
    const bet = {cashoutSuccessMessage: 'cashOutSuccessful'};
    component.isMyBetsInCasino = false;
    callbacks[pubsub.API.UPDATE_CASHOUT_BET](bet);

    expect(cashOutSectionService.updateBet).toHaveBeenCalled();
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    expect(windowRef.nativeWindow.parent.postMessage).not.toHaveBeenCalled();
    expect(component['detectListener']).toEqual(123);
  });

  it(`should updateBet when UPDATE_CASHOUT_BET and define detectListener, with isMyBetsInCasino as true and cashoutMsg as undefined`, () => {
    spyOn<any>(component, 'setActiveEvent');
    delete component['detectListener'];
    const callbacks = {};
    pubsub.subscribe.and.callFake((subscriber, key, fn) => {
      callbacks[key] = fn;
    });
    windowRef.nativeWindow.setInterval.and.returnValue(123);
    component.ngOnInit();
    const bet = {cashoutSuccessMessage: undefined};
    component.isMyBetsInCasino = true;
    callbacks[pubsub.API.UPDATE_CASHOUT_BET](bet);

    expect(cashOutSectionService.updateBet).toHaveBeenCalled();
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    expect(windowRef.nativeWindow.parent.postMessage).not.toHaveBeenCalled();
    expect(component['detectListener']).toEqual(123);
  });

  it(`should updateBet when PAYOUT_UPDATE received and update the potentialPayout accordingly`, () => {
    const spyObj = spyOn<any>(component, 'updateBets');
    const callbacks = {};
    pubsub.subscribe.and.callFake((subscriber, key, fn) => {
      callbacks[key] = fn;
    });
    component.ngOnInit();
    const bet = {updatedReturns : [{betNo:'12345', returns: 2}]};
    callbacks[pubsub.API.PAYOUT_UPDATE](bet);

    expect(spyObj).toHaveBeenCalled();
  });

  it(`should updateBet when PAYOUT_UPDATE received and update the potentialPayout accordingly when return is zero`, () => {
    const spyObj = spyOn<any>(component, 'updateBets');
    const callbacks = {};
    pubsub.subscribe.and.callFake((subscriber, key, fn) => {
      callbacks[key] = fn;
    });
    component.ngOnInit();
    const bet = {updatedReturns : [{betNo:'12345', returns: 0}]};
    callbacks[pubsub.API.PAYOUT_UPDATE](bet);

    expect(spyObj).toHaveBeenCalled();
  });

  it(`should detectListener on 100ms`, () => {
    spyOn<any>(component, 'setActiveEvent');
    component.ngOnInit();

    expect(windowRef.nativeWindow.setInterval).toHaveBeenCalledWith(jasmine.any(Function), 100);
  });
  describe('CongratsBanner', () => {
    let bet;
    beforeEach(() => {
      component.celebration = {
        displayCelebrationBanner: true,
        duration: 240000000000,
        winningMessage: 'You have won {amount}!!',
        cashoutMessage: 'You have cashedout {amount}!!'
      };
      bet = {
        eventSource: {
          totalReturns: '6.00',
          stake: '5.00',
          settledAt: '2019-03-04 11:00:45',
          currencySymbol: '£',
          potentialPayout: '6.00',
          totalStatus: 'cashed out'
        }
      };
      component.isBetHistoryTab = true;
    });
    it('isCongratsBannerShown with bet', () => {
      cashOutSectionService.getInitialStake.and.returnValue(bet.eventSource);
      expect(component.isCongratsBannerShown(bet)).toBeFalse();
      expect(cashOutSectionService.getInitialStake).toHaveBeenCalled();
    });
    it('isCongratsBannerShown with totalStatus as son', () => {
      cashOutSectionService.getInitialStake.and.returnValue(bet.eventSource);
      bet.eventSource.totalStatus = 'won';
      expect(component.isCongratsBannerShown(bet)).toBeFalse();
    });
    it('isCongratsBannerShown with celebration as null', () => {
      cashOutSectionService.getInitialStake.and.returnValue(bet.eventSource);
      component.celebration = null;
      expect(component.isCongratsBannerShown(bet)).toBe(undefined);
    });
    it('getReturnValue', () => {
      expect(component.getReturnValue(bet)).toBe('You have won 6.00£!!');
    });
    it('getReturnValue with celebration as null', () => {
      component.celebration = null;
      expect(component.getReturnValue(bet)).toBe(undefined);
    });
    it('getCashoutReturnValue', () => {
      expect(component.getCashoutReturnValue(bet)).toBe('You have cashedout 6.00£!!');
    });
    it('getCashoutReturnValue', () => {
      component.celebration = null;
      expect(component.getCashoutReturnValue(bet)).toBe(undefined);
    });
  });
  it('ngOnDestroy', () => {
    spyOn<any>(component, 'setActiveEvent');
    component.area = areaInput;
    environment.brand = 'ladbrokes';
    component.ngOnInit();
    component['betTrackingEnabledSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component['getEventIdStatisticsSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component['fiveASideVoidHandlingSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component['channels'] = ['mFACTS123'];
    component.ngOnDestroy();

    expect(component['betTrackingEnabledSubscription'].unsubscribe).toHaveBeenCalled();
    expect(component['getEventIdStatisticsSubscription'].unsubscribe).toHaveBeenCalled();
    expect(component['fiveASideVoidHandlingSubscription'].unsubscribe).toHaveBeenCalled();
    expect(environment.brand).toBe('ladbrokes');

    expect(pubsub.unsubscribe).toHaveBeenCalledTimes(1);
    expect(pubsub.unsubscribe).toHaveBeenCalledWith(`${cashoutConstants.controllers.REGULAR_BETS_CTRL}-${areaInput}`);

    expect(cashOutSectionService.removeListeners).toHaveBeenCalledTimes(1);
    expect(emaService.clearAccas).toHaveBeenCalled();
    expect(cmsService.getFeatureConfig).toHaveBeenCalled();
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

  it('should call needed methods in constructor', () => {
    spyOn(component as any, 'setActiveEvent');
    spyOn<any>(component, 'init');
    component.betsMap = { '12345': { potentialPayout : "N/A"}} as any;
    component.ngOnChanges({ regularBets: true } as any);
    component.bets = [{ eventSource: { event: '654321', leg: [{ part: [{outcomeId: "555"}], eventEntity: { eventIsLive: true, comments:{home:{}} } }] } }] as any;
    component.ngOnInit();

    expect(component['init']).toHaveBeenCalledTimes(1);
  });

  it('should call needed methods in constructor', () => {
    spyOn(component as any, 'setActiveEvent');
    spyOn<any>(component, 'init');
    component.betsMap = { '12345': { potentialPayout : "N/A"}} as any;
    component.bets = [{ eventSource: { event: '654321', leg: [{ part: [{outcomeId: "555"}], eventEntity: { eventIsLive: true, comments:{home:{}} } }] } }] as any;
    component.ngOnInit();
    component.initialized = true;
    component.ngOnChanges({ regularBets: true } as any);

    expect(component['init']).toHaveBeenCalledTimes(2);
  });

  it('should call ngOnChanges with start date and end date same ', () => {
    component.initialized = false;
    component.isBetHistoryTab = false;
    const currentDate = new Date(new Date().toDateString());
    component.ngOnChanges({  startDate: {currentValue : {value:currentDate}}, endDate: {currentValue : {value:currentDate}}} as any);
    expect(component['noBetsMessage']).toBe('No open bets placed today.');
  });

  it('should call ngOnChanges with start date change', () => {
    component.initialized = false;
    component.isBetHistoryTab = false;
    const currentDate = new Date(new Date().toDateString());
    component.ngOnChanges({  startDate: {currentValue : {value:new Date(Date.now() - ( 3600 * 1000 * 24))}}, endDate: {currentValue : {value:currentDate}}} as any);
    expect(component['noBetsMessage']).toBe('No open bets placed within the last 2 days.');
  });

  it('should call ngOnChanges with start date change with leap year', () => {
    component.initialized = false;
    component.isBetHistoryTab = true;
    const currentDate = new Date(new Date().toDateString());
    component.ngOnChanges({  startDate: {currentValue : {value:new Date('December 20, 2020')}}, endDate: {currentValue : {value:currentDate}}} as any);
    expect(component['noBetsMessage']).toBe('No Open bets In specified time range');
  });


  it('should call ngOnChanges with end date change with leap year', () => {
    component.initialized = false;
    component.isBetHistoryTab = false;
    component.ngOnChanges({  startDate: {currentValue : {value:new Date('December 20, 2023')}}, endDate: {currentValue : {value:new Date('December 20, 2024')}}} as any);
    expect(component['noBetsMessage']).toBe('No Open bets In specified time range');
  });
  
  it('should return cashout value', () => {
    let bet = { cashoutValue: '10' } as any;
    expect(component.getCashedOutValue(bet)).toEqual('10');
    bet = { cashoutValue: 'test', potentialPayout: '12' };
    expect(component.getCashedOutValue(bet)).toEqual('12');
  });

  it('isCashoutError should call isCashoutError method of cashout section service', () => {
    component['isCashoutError']({} as any, true, true);
    expect(cashOutSectionService.isCashoutError).toHaveBeenCalled();
  });

  it('getCashoutError should call getCashoutError method of cashout section service', () => {
    component['getCashoutError']({} as any);
    expect(cashOutSectionService.getCashoutError).toHaveBeenCalled();
  });

  describe('Test showBogForBetFromPriceType', () => {
    beforeEach(() => {
      component.bets = [
        {
          eventSource: {
            event: ['654321'],
            leg: [
              {
                name: 'test name',
                startTime: '1542273861984',
                poolPart: [],
                legSort: '',
                legNo:5,
                betId:55,
                part: [
                  {
                    outcomeId: '51',
                    outcome: [{
                      eventCategory: {
                        id: '1'
                      }
                    }],
                    priceNum: 3,
                    priceDen: 6,
                    price: [
                      {
                        priceType: {
                          code: ''
                        }
                      },
                      {
                        priceType: {
                          code: ''
                        }
                      }
                    ]
                  } as any
                ],
                status: 'won',
                removing: false,
                removedLeg: false,
                resultedBeforeRemoval: true
              } as any
            ]
          }
        }
      ] as any;
    });

    it('should call showBogForBetFromPriceType() and return isBog=false if priceType.codes is "" ', () => {
      expect(component.showBogForBetFromPriceType(component.bets[0])).toBe(false);
    });

    it('should call showBogForBetFromPriceType() and return isBog=false if priceType is "null" ', () => {
      component.bets[0].eventSource.leg[0].part[0].price[0].priceType = null;
      expect(component.showBogForBetFromPriceType(component.bets[0])).toBe(false);
    });

    it('should call showBogForBetFromPriceType() and return isBog=false if priceType.codes is "null" ', () => {
      component.bets[0].eventSource.leg[0].part[0].price[0].priceType.code = null;
      expect(component.showBogForBetFromPriceType(component.bets[0])).toBe(false);
    });

    it('should call showBogForBetFromPriceType() and return isBog=true if priceType.codes is "GP" ', () => {
      component.bets[0].eventSource.leg[0].part[0].price[0].priceType.code = 'GP';
      expect(component.showBogForBetFromPriceType(component.bets[0])).toBe(true);
    });

    it('should call showBogForBetFromPriceType() and return isBog=false if priceType.codes is "S" ', () => {
      component.bets[0].eventSource.leg[0].part[0].price[0].priceType.code = 'S';
      expect(component.showBogForBetFromPriceType(component.bets[0])).toBe(false);
    });

  });

  describe('Test bogReturnValue', () => {
    it('#bogReturnValue should return bogReturn value', () => {
      const livePriceWinnings = [{
        value: '1.00'
      }];
      const winnings = [{
        value: '10.00'
      }];
      expect(component.bogReturnValue(winnings, livePriceWinnings)).toBe(9.00);
    });

    it('#bogReturnValue should return bogReturn value', () => {
      const livePriceWinnings = undefined;
      const winnings = undefined;
      expect(component.bogReturnValue(winnings, livePriceWinnings)).toBe(0);
    });
  });

  describe('Test showBog', () => {
    const bet = { eventSource: {hasFreeBet: false }} as any;
    it('showBog() should return false, when BOG Not enabled from CMS', ()=> {
      component.isBogEnabledFromCms = false;
      expect(component.showBog(bet)).toBe(false);
    });

    it('showBog() should return false, when its Not BOG from price type', ()=> {
      component.isBogEnabledFromCms = true;
      spyOn(component, 'showBogForBetFromPriceType').and.returnValue(false);
      expect(component.showBog(bet)).toBe(false);
    });

    it('showBog() should return false, when BOG extra earnings is less than zero', ()=> {
      component.isBogEnabledFromCms = true;
      spyOn(component, 'showBogForBetFromPriceType').and.returnValue(true);
      spyOn(component, 'bogReturnValue').and.returnValue(0);
      expect(component.showBog(bet)).toBe(false);
    });

    it('showBog() should return false, when its a Free bet', ()=> {
      component.isBogEnabledFromCms = true;
      bet.eventSource.hasFreeBet = true;
      spyOn(component, 'showBogForBetFromPriceType').and.returnValue(true);
      spyOn(component, 'bogReturnValue').and.returnValue(10);
      expect(component.showBog(bet)).toBe(false);
    });

    it('showBog() should return true, when its BOG and satisfies all conditions', ()=> {
      component.isBogEnabledFromCms = true;
      bet.eventSource.hasFreeBet = false;
      spyOn(component, 'showBogForBetFromPriceType').and.returnValue(true);
      spyOn(component, 'bogReturnValue').and.returnValue(10);
      expect(component.showBog(bet)).toBe(true);
    });
  });
  describe('#setFiveASideVoidHandling', () => {
    it('should not set Five A Side VoidHandling, if both conditions does not satisfy', () => {
      const config = {};
      cmsService.getFeatureConfig.and.returnValue(observableOf(config));
      environment.brand = 'ladbrokes';
      component['setFiveASideVoidHandling']();
      expect(component['fiveASideVoidHandling']).toBeUndefined();
      expect(component['goToFiveASide']).toBeUndefined();
    });
    it('should not set Five A Side VoidHandling, if only one condition satisfy', () => {
      const config = {
          enabled: false
      };
      cmsService.getFeatureConfig.and.returnValue(observableOf(config));
      environment.brand = 'ladbrokes';
      component['setFiveASideVoidHandling']();
      expect(component['fiveASideVoidHandling']).toBeUndefined();
    });
    it('should set set Five A Side VoidHandling, if both condition satisfy(length > 100)', () => {
      cmsService.getFeatureConfig.and.returnValue(observableOf(regularBets.config));
      environment.brand = 'ladbrokes';
      component['setFiveASideVoidHandling']();
      expect(component['goToFiveASide']).toBe(`${regularBets.config.gotoFiveASideText}`);
    });
    it('should set setFiveASideVoidHandling, if both condition satisfy(length < 150)', () => {
      cmsService.getFeatureConfig.and.returnValue(observableOf(regularBets.config1));
      environment.brand = 'ladbrokes';
      component['setFiveASideVoidHandling']();
      expect(component['fiveASideVoidHandling']).toBe(regularBets.config1.infoText);
      expect(component['goToFiveASide']).toBe(`${regularBets.config1.gotoFiveASideText}`);
    });
    it('should set setFiveASideVoidHandling, if both condition satisfy(length > 100)', () => {
      cmsService.getFeatureConfig.and.returnValue(observableOf(regularBets.config2));
      environment.brand = 'ladbrokes';
      component['setFiveASideVoidHandling']();
      expect(component['fiveASideVoidHandling']).toBe(`${regularBets.config2.infoText.substring(0,150)}...`);
      expect(component['goToFiveASide']).toBe(`${regularBets.config2.gotoFiveASideText.substring(0,50)}...`);
    });
  });

  describe('#setActiveEvent', () => {
    it('should not set Five A Side VoidHandling, case1', () => {
      component.bets = [{ eventSource: null }] as any;
      component['setActiveEvent']();
      expect(component.bets[0].hasActiveEvent).toBeUndefined();
    });
    it('should not set Five A Side VoidHandling, case2', () => {
      component.bets = [{ eventSource: {event:[], leg: [] } }] as any;
      component['setActiveEvent']();
      expect(component.bets[0].hasActiveEvent).toBeUndefined();
    });
    it('should not set Five A Side VoidHandling, case3', () => {
      component.bets = [{ eventSource: {event:[], leg: [{ part: [] }] } }] as any;
      component['setActiveEvent']();
      expect(component.bets[0].hasActiveEvent).toBeUndefined();
    });
    it('should not set Five A Side VoidHandling, case4', () => {
      component.bets = [{ eventSource: {event: ['123456'], leg: [{ part: [{ outcome: [] }] }] } }] as any;
      component['setActiveEvent']();
      expect(component.bets[0].hasActiveEvent).toBeUndefined();
    });

    it('should not set Five A Side VoidHandling, case5', () => {
      component.bets = [{ eventSource: {event:[], leg: [{ part: [{ outcome: [{}] }] }] } }] as any;
      component['setActiveEvent']();
      expect(component.bets[0].hasActiveEvent).toBeUndefined();
    });
    it('should not set Five A Side VoidHandling, case6', () => {
      component.bets = [regularBets.eventStartTime] as any;
      component['setActiveEvent']();
      expect(component.bets[0].hasActiveEvent).toBeUndefined();
    });
    it('should set Five A Side VoidHandling, case7', () => {
      component.bets = [regularBets.eventStartTime2] as any;
      component['setActiveEvent']();
      expect(component.bets[0].hasActiveEvent).toBe(true);
    });
    it('should be check with event id with getEventIdStatisticsSubscription true', () => {
      component.bets = [{ eventSource: {event:['123456'], leg: [{ part: [{ outcome: [{}] }] }] } }] as any;
      component['setActiveEvent']();
      expect(component.bets[0].optaDisclaimerAvailable).toBe(true);
    });

    it('should be check with event id with getEventIdStatisticsSubscription undefined', () => {
      component.bets = [{ eventSource: {event:['12345678'], leg: [{ part: [{ outcome: [{}] }] }] } }] as any;
      component['setActiveEvent']();
      expect(component.bets[0].optaDisclaimerAvailable).toBeUndefined();
    });
  });
  it('createDateAsUTC', () => {
    const result = component.createDateAsUTC(new Date('2020-12-07 19:30:00'));
    expect(result).toEqual(result);
  });

  describe('#isShownDisclaimer', () => {
    it('isShownDisclaimer true', () => {
      component.isBetHistoryTab = false;
      component.dataDisclaimer = { enabled: true } as any;
      const bet = { eventSource: { leg: [{ eventEntity: { eventIsLive: true, comments: {home:{}} } }] } } as any;
      const result = component.isShownDisclaimer(bet);
      expect(result).toBe(true);
    })
    it('isShownDisclaimer bet cms false', () => {
      component.isBetHistoryTab = true;
      component.dataDisclaimer = { enabled: false } as any;
      const bet = { eventSource: { leg: [{ eventEntity: { eventIsLive: true, comments: {home:{}} } }] } } as any;
      const result = component.isShownDisclaimer(bet);
      expect(result).toBe(false);
    })
    it('isShownDisclaimer bet history true', () => {
      component.isBetHistoryTab = true;
      component.dataDisclaimer = { enabled: true } as any;
      const bet = { eventSource: { leg: [{ eventEntity: { eventIsLive: true, comments: {home:{}} } }] } } as any;
      const result = component.isShownDisclaimer(bet);
      expect(result).toBe(false);
    })
    it('isShownDisclaimer bet nolive false', () => {
      component.isBetHistoryTab = false;
      component.dataDisclaimer = { enabled: true } as any;
      const bet = { eventSource: { leg: [{ eventEntity: { eventIsLive: false,comments: {home:{}} } }] } } as any;
      const result = component.isShownDisclaimer(bet);
      expect(result).toBe(false);
    })
    it('isShownDisclaimer bet comments false', () => {
      component.isBetHistoryTab = false;
      component.dataDisclaimer = { enabled: true } as any;
      const bet = { eventSource: { leg: [{ eventEntity: { eventIsLive: true,comments: null } }] } } as any;
      const result = component.isShownDisclaimer(bet);
      expect(result).toBe(false);
    })
  })
  describe('#matchCommentaryUpdate', () => {
    it('should subscribe when var-data is avaialble and call matchCommentaryDataUpdate', () => {
      const varDataUpdate = { varEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } };
      component.bets = [{ eventSource: { event: ['12345'], leg: [{ eventEntity: { id: 12345 }, part: [{ outcome: [{}] }] }] } }] as any;
      pubsub.subscribe.and.callFake((cashoutbets, listeners, handler) => {
        if (listeners == 'UPDATE_MATCHCOMMENTARY_DATA') {
          handler(varDataUpdate);
        }
      });
      component['matchCommentaryUpdate']();
      expect(pubsub.subscribe).toHaveBeenCalledWith(component['ctrlName'], 'UPDATE_MATCHCOMMENTARY_DATA', jasmine.any(Function));
      expect(cashOutSectionService.matchCommentaryDataUpdate).toHaveBeenCalledOnceWith(component.bets, varDataUpdate);
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
    it('should call reuse service and add bets to bet slip', fakeAsync(() => {
     component['origin'] = 'Open Bets';
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

  describe("#checkIfAnyEventActive", () => {
    it('should return true if event not confirmed', () => {
      const bet = {
        eventSource: {
          leg: [{
            part: [{
              outcome: [{
                result: {
                  confirmed: 'N'
                }
              }]
            }],
            status: 'open'
          }]
        }
      } as any;
      const res = component.checkIfAnyEventActive(bet);
      expect(res).toEqual(true);
    });
    it('should return false if event confirmed', () => {
      const bet = {
        eventSource: {
          leg: [{
            part: [{
              outcome: [{
                result: {
                  confirmed: 'Y'
                }
              }]
            }],
            status: 'open'
          }]
        }
      } as any;
      const res = component.checkIfAnyEventActive(bet);
      expect(res).toEqual(false);
    });
  });

  describe("#checkIfAnyEventDisplayed", () => {
    it('should return true if event not confirmed', () => {
      const bet = {
        eventSource: {
          leg: [{
            part: [{
              outcome: [{
                result: {
                  confirmed: 'N'
                }
              }]
            }],
            status: 'open'
          }],
          events: {}
        }
      } as any;
      const res = component.checkIfAnyEventDisplayed(bet);
      expect(res).toEqual(true);
    });
    it('should return true if event confirmed and displayed SGL', () => {
      const bet = {
        eventSource: {
          betType: 'SGL',
          leg: [{
            part: [{
              outcome: [{
                result: {
                  confirmed: 'N'
                }
              }]
            }],
            status: 'open'
          }],
          events: {12345 : {displayed: "Y"}},
          markets: {12345 : {displayed: "Y"}},
          outcomes: {12345 : {displayed: "Y"}}
        }
      } as any;
      const res = component.checkIfAnyEventDisplayed(bet);
      expect(res).toEqual(true);
    });
    it('should return true if event confirmed and displayed MUL', () => {
      const bet = {
        eventSource: {
          betType: 'MUL',
          leg: [{
            part: [{
              outcome: [{
                result: {
                  confirmed: 'N'
                }
              }]
            }],
            status: 'open'
          }],
          events: {12345 : {displayed: "Y"}},
          markets: {12345 : {displayed: "Y"}},
          outcomes: {12345 : {displayed: "Y"}}
        }
      } as any;
      const res = component.checkIfAnyEventDisplayed(bet);
      expect(res).toEqual(true);
    });
    it('should return false if event confirmed and not displayed SGL', () => {
      const bet = {
        eventSource: {
          betType: 'SGL',
          leg: [{
            part: [{
              outcome: [{
                result: {
                  confirmed: 'N'
                }
              }]
            }],
            status: 'open'
          }],
          events: {12345 : {displayed: "N"}},
          markets: {12345 : {displayed: "N"}},
          outcomes: {12345 : {displayed: "N"}}
        }
      } as any;
      const res = component.checkIfAnyEventDisplayed(bet);
      expect(res).toEqual(false);
    });
    it('should return false if event confirmed and not displayed MUL', () => {
      const bet = {
        eventSource: {
          betType: 'MUL',
          leg: [{
            part: [{
              outcome: [{
                result: {
                  confirmed: 'N'
                }
              }]
            }],
            status: 'open'
          }],
          events: {12345 : {displayed: "N"}},
          markets: {12345 : {displayed: "N"}},
          outcomes: {12345 : {displayed: "N"}}
        }
      } as any;
      const res = component.checkIfAnyEventDisplayed(bet);
      expect(res).toEqual(false);
    });
  });
  
  describe('#alertsListeners', () => {
    it('alertsListeners - HOME_BETSLIP', fakeAsync(() => {
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
    it('alertsListeners - subscriptions', fakeAsync(() => {
      component.lazyLoadedBets = [{id: 1}, {id: 2}] as any;
      component.selectOpenBetsTab = jasmine.createSpy();
      component['sessionStateDefined'] = true;
      component.ngOnInit();
      tick();
      expect(component.selectOpenBetsTab).toHaveBeenCalledTimes(6);
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
      component.selectOpenBetsTab = jasmine.createSpy();
      component.ngOnInit();
      tick();
      expect(component.selectOpenBetsTab['calls'].count()).toBe(4);
    }));
    it('ngOnInit (whenSession error #2)', fakeAsync(() => {
      sessionService.whenSession.and.returnValue(Promise.reject('error msg'));
      component.selectOpenBetsTab = jasmine.createSpy();
      component.ngOnInit();
      tick();
      expect(component.selectOpenBetsTab['calls'].count()).toBe(4);
    }));
  });
  describe('setAlertsConfig', () => {
    it('should hasOnEventAlertsClick - false, hasShowFootballAlerts - true', () => {
      nativeBridge.hasOnEventAlertsClick.and.returnValue(false);
      const bets = [{eventSource: {betId: 'test'}}] as any;

      component['setAlertsConfig'](bets);
      expect(nativeBridge['multipleEventPageLoaded']).not.toHaveBeenCalled();
    });
    it('should NOT call multipleEventPageLoaded - bet not found', () => {
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

    it('should NOT do football Alerts Visible if no valid configuration in CMS', () => {
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

    it('handleFootballAlerts - without eventEntity', () => {
      component.bets = [{ eventSource: { betId: '55', event: '123456', leg: [{ part: [{outcomeId: "555"}], backupEventEntity: {  id: '123456', eventIsLive: true, comments:{home:{}}, categoryCode: 'football', 
      eventSortCode: 'test', categoryId: '16', typeName: "league", categoryName: 'test categoryName' } }],
      betType: 'SGL', receipt: '0000/1234/12345' } }] as any;
      component['deviceMatchAlerts'] = [{eventId: "123456"}] as any;
      const data = {detail: [{eventId: "123456", isEnabled: true}]} as any;
      component['handleFootballAlerts'](data);
      expect(component['bets'][0].footballBellActive).toBeTrue();
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
      ALERTS_GTM.OPEN_BETS);
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
        'component.PositionEvent': ALERTS_GTM.OPEN_BETS,
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
    expect(toggleSwitch).toEqual('toggle-switch-regularbets-55');
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

  describe('#selectOpenBetsTab', () => {
    it('selectOpenBetsTab - name - test', () => {
      component.winAlertsEnabled = true;
      component['winAlertsBets'] = ['1'];
      component['winAlertsReceiptId'] = '1';
      component['mode'] = component.MODES.openbets;

      user.winAlertsToggled = false;
      component.selectOpenBetsTab('test');
      expect(component['mode']).toBe('test');
      expect(component['winAlertsBets'].length).toEqual(0);
      expect(component['winAlertsReceiptId']).toBeFalsy();
      expect(nativeBridge['onActivateWinAlerts']).toHaveBeenCalledWith('1', ['1']);
    });

    it('selectOpenBetsTab - name - test', () => {
      component.winAlertsEnabled = false;

      component.selectOpenBetsTab('test');

      expect(nativeBridge['onActivateWinAlerts']).not.toHaveBeenCalled();
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