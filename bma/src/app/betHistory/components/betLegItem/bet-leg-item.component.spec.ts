import environment from '@environment/oxygenEnvConfig';
import { BetLegItemComponent } from './bet-leg-item.component';
import { IBetHistoryLeg, IBetHistoryPart } from '@app/betHistory/models/bet-history.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { horseracingConfig } from '@core/services/racing/config/horseracing.config';
import { of } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

describe('BetLegItemComponent', () => {
  let component: BetLegItemComponent;

  let leg;
  let commentsService, eventService;
  let footballUpdateExtendSpy;
  let cashOutServiceStub;
  let raceOutcomeDetailsServiceStub;
  let localeStub;
  let fracToDecServiceStub;
  let filtersServiceStub;
  let editMyAccaService;
  let pubSubService;
  let routerStub;
  let routingHelperStub;
  let cmsService;
  let betTrackingService;
  let sportsConfigHelperService;
  let casinoMyBetsIntegratedService;
  let handleVarReasoningUpdatesService;  
  let deviceService;
  let watchRulesService;
  let nativeBridge;
  let windowRef;
  let liveStreamService;
  let horseRacingService;
  const HORSE_RACING_CATEGORY_ID = environment.HORSE_RACING_CATEGORY_ID;
  const isLastBet = true;
  let gtmService;
  let cmsObservableResult;
  let sessionStorageService;

  beforeEach(() => {
    cashOutServiceStub = {
      getEachWayTerms: jasmine.createSpy().and.returnValue('#YourCall getEachWayTerms')
    };
    betTrackingService= {
      isTrackingEnabled: jasmine.createSpy('isTrackingEnabled'),
      checkIsBuildYourBet: jasmine.createSpy('checkIsBuildYourBet')
    };
    raceOutcomeDetailsServiceStub = {
      getSilkStyleForPage: jasmine.createSpy('getSilkStyleForPage'),
      isSilkAvailableForOutcome: jasmine.createSpy('isSilkAvailableForOutcome'),
      isUnnamedFavourite: jasmine.createSpy('isUnnamedFavourite'),
      isNumberNeeded: jasmine.createSpy('isNumberNeeded'),
    };
    localeStub = {
      getString: jasmine.createSpy().and.returnValue('Build Your Bet')
    };
    fracToDecServiceStub = {
      getFormattedValue: jasmine.createSpy('getFormattedValue')
    };
    filtersServiceStub = {
      filterPlayerName: jasmine.createSpy('filterPlayerName'),
      filterAddScore: jasmine.createSpy('filterAddScore')
    };
    editMyAccaService = {
      isLegSuspended: jasmine.createSpy('isLegSuspended'),
      isLegResulted: jasmine.createSpy('isLegResulted')
    };
    handleVarReasoningUpdatesService ={
      unsubscribeForMatchCmtryUpdates: jasmine.createSpy('unsubscribeForMatchCmtryUpdates'),
      subscribeForMatchCmtryUpdates:  jasmine.createSpy('subscribeForMatchCmtryUpdates')
    }
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy().and.callFake((a, b, cb) => cb && cb()),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        UPDATE_EMA_ODDS: 'UPDATE_EMA_ODDS',
        CASHOUT_LIVE_SCORE_EVENT_UPDATE: 'CASHOUT_LIVE_SCORE_EVENT_UPDATE',
        CASHOUT_LIVE_SCORE_UPDATE: 'CASHOUT_LIVE_SCORE_UPDATE',
        UPDATE_ITEM_HEIGHT: 'UPDATE_ITEM_HEIGHT',
        BET_LEGS_LOADED:'BET_LEGS_LOADED',
        EVENT_STARTED:'EVENT_STARTED',
        IS_LIVE: 'IS_LIVE',
        EVENT_FINSHED:'EVENT_FINSHED',
        TWO_UP_UPDATE:'TWO_UP_UPDATE'
      }
    };
    deviceService = { isWrapper: true,isDesktop:true };
    routerStub = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    routingHelperStub = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('url')
    };
    footballUpdateExtendSpy = jasmine.createSpy('footballUpdateExtendSpy');
    commentsService = {
      sportUpdateExtend: jasmine.createSpy('sportUpdateExtend'),
      footballUpdateExtend: footballUpdateExtendSpy,
      extendWithScoreType: jasmine.createSpy('extendWithScoreType')
    };
    eventService = {
      isUKorIRE: jasmine.createSpy('isUKorIRE')
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({ 
		MybetsMatchCommentary: {
          enabled: true
        },
        ExternalUrls: {
          'DeadHeat_Info': 'DEAD_HEAT_URL'
        },
		HorseRacingBIR: {
          streamEnabled: true },
      TwoUpSignposting: {isTwoUpSettlementEnabled: true}
    })),
      getItemSvg: jasmine.createSpy('getItemSvg').and.returnValue(of({
        svg: 'svg',
        svgId: 'svgId'
      })),
      getFeatureConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of(cmsObservableResult))
    };
    cmsObservableResult = {
      insightsDrillDownTags: ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA']
    };
    watchRulesService = {
      isInactiveUser: jasmine.createSpy('isInactiveUser')
    };
    nativeBridge = {
      hideVideoStream: jasmine.createSpy('hideVideoStream'),
      eventPageLoaded: jasmine.createSpy('eventPageLoaded'),
      hasOnEventAlertsClick: jasmine.createSpy('hasOnEventAlertsClick').and.returnValue(true),
      playerStatus: true,
      onEventAlertsClick: jasmine.createSpy('onEventAlertsClick'),
      getMobileOperatingSystem: jasmine.createSpy().and.returnValue('ios'),
      handleNativeVideoPlaceholder: jasmine.createSpy('handleNativeVideoPlaceholder'),
      handleNativeVideoPlayer: jasmine.createSpy('handleNativeVideoPlayer'),
      hideVideoPlaceholder: jasmine.createSpy('hideVideoPlaceholder')
    };
    windowRef = {
      document: {
        addEventListener: () => {},
      }
    };
    liveStreamService = {
      isLiveStreamAvailable: jasmine.createSpy('isLiveStreamAvailable').and.returnValue(() => {})
    };
    horseRacingService = {
      isRacingSpecials: jasmine.createSpy('isRacingSpecials').and.returnValue(false)
    };
    leg = {
      name: 'test name',
      startTime: '1542273861984',
      poolPart: [],
      legSort: '',
      eventEntity: {
        eventStatusCode: 'S'
      },
      part: [
        {
          outcomeId: '51',
          outcome: [{
            name: 'xyz',
            runnerNumber: 1,
            eventCategory: {
              id: '1'
            },event: {
              id: "240790191",
              name: "14:55 Ayr",
              startTime: "2023-07-10 14:55:00",
              raceNumber: "",
              venue:"",
              isOff: "N"
          }
          ,eventType: {
            name:'abc'
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
          ],
          marketId: '1',
        } as any
      ],
      status: 'won',
      removing: false,
      removedLeg: false,
      resultedBeforeRemoval: true,
      isLiveStreamOpened: true
    } as any;
    origin ='openbets';
    gtmService = {
      push: jasmine.createSpy('push')
    };

    sportsConfigHelperService = {
      getSportPathByCategoryId: jasmine.createSpy('getSportPathByCategoryId').and.returnValue(of('horsePath'))
    };

    casinoMyBetsIntegratedService = {
      confirmationPopUpClick: jasmine.createSpy('confirmationPopUpClick'),
      goToSportsCTABtnClick: jasmine.createSpy('goToSportsCTABtnClick')
    };

    sessionStorageService = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set')
    }

    component = new BetLegItemComponent(cashOutServiceStub, raceOutcomeDetailsServiceStub, localeStub, fracToDecServiceStub,
      pubSubService, filtersServiceStub, editMyAccaService, routerStub, routingHelperStub,
      commentsService, eventService, sportsConfigHelperService, cmsService, betTrackingService, casinoMyBetsIntegratedService, handleVarReasoningUpdatesService, deviceService, watchRulesService, nativeBridge, windowRef, liveStreamService, horseRacingService,sessionStorageService, gtmService);
    component.bet = {
      eventSource: { totalStatus : 'lost' }
    } as any;
    component.streamControl = {
      externalControl: true,
      playLiveSim: jasmine.createSpy('playLiveSim'),
      playStream: jasmine.createSpy('playStream'),
      hideStream: jasmine.createSpy('hideStream'),
    };
    component.leg = { part: [{outcomeId: 12345, "outcome": [{ eventType: {
      name:'abc'
    },"event": {
      "id": "240790191",
      "name": "14:55 Ayr",
      "startTime": "2023-07-10 14:55:00",
      "raceNumber": "",
      "venue": "",
      "isOff": "N"
  },}]}], isLiveStreamOpened: false } as any;
  component.leg.part[0].outcome =[ {
    flags: ['2UP'],
    result:{
      value:"W",
      confirmed:"Y"
    }
  }] as any;
    component.isHRLiveEnabled = true;
    component['config'] = horseracingConfig;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  it('replayStream', () => {
    component.leg.eventEntity = {
      typeName:'UK',
      rawIsOffCode: '-',
      drilldownTagNames: 'EVFLAG_PVM'
    } as any;
    component.leg.part[0].outcome[0].eventType={name:'abc'};
    component.isUsedFromWidget =false;
    component.isReplayVideo=true;
    component['deviceService'].isWrapper = false;
    component['deviceService'].isDesktop = true;

    component.replayStream({ preventDefault: () => { } } as any);
  });
  it('replayStream from widget', () => {
    component.leg.eventEntity = {
      typeName:'UK',
      rawIsOffCode: '-',
      drilldownTagNames: 'EVFLAG_PVM'
    } as any;
    component.leg.part[0].outcome[0].eventType={name:'abc'};
    component.isUsedFromWidget =true;
    component.isReplayVideo=true;
    component['deviceService'].isDesktop = false;
    component['deviceService'].isWrapper = true;
    component.replayStream({ preventDefault: () => { } } as any);
  });
  it('getStreamByType called from widget ', () => {    
    component.isUsedFromWidget =true;
    expect(component.getStreamByType()).toBe(false);
  });
  it('getStreamByType called  ', () => {    
    component.leg.isWidgetLiveStreamOpened = false;
    component.isUsedFromWidget =false;
    expect(component.getStreamByType()).toBe(false);
  });

  it('playStream on wrapper', () => {
    component.leg.isLiveStreamOpened = true;
    component.leg.eventEntity = {
      'rawIsOffCode': '-'
    } as any;
    component.playStream({ preventDefault: () => { } } as any);

    expect(component.streamControl.playLiveSim).toHaveBeenCalledWith(false);
    expect(nativeBridge.hideVideoStream).toHaveBeenCalled();
    expect(pubSubService.subscribe).toHaveBeenCalled();
  });

  it('playStream not on wrapper', () => {
    component.leg.eventEntity = {
      typeName:'UK',
      rawIsOffCode: '-',
      drilldownTagNames: 'EVFLAG_PVM'
    } as any;
    component['deviceService'].isWrapper = false;
    component.playStream({ preventDefault: () => { } } as any);

    expect(component.streamControl.playLiveSim).toHaveBeenCalledWith(false);
    expect(nativeBridge.hideVideoStream).not.toHaveBeenCalled();
    expect(pubSubService.subscribe).toHaveBeenCalled();
  });

  it('isHRLiveLabelEnabled ', () => {
    component.leg.eventEntity = {
      categoryCode: 'HORSE_RACING'
    } as any;
    expect(component.isHRLiveLabelEnabled()).toEqual(true);
  });

  it('isHRbuttonEnabled', () => {
    component.leg.eventEntity = {
      categoryCode: 'HORSE_RACING',
      isFinished: false,
      isBetSettled: false
    } as any;
    component.isHRLiveEnabled = true;
    component.isMyBetsWidget = true;
    expect(component.isHRbuttonEnabled()).toEqual(true);
  });

  it('transitionSpinner', () => {
    component.spinner = {loading: true};
    component.transitionSpinner();
    expect(component.spinner.loading).toBeFalsy();
  });

  it('onVideoStreamEvent when user is inactive', () => {
    const error = { output: 'playStreamError', value: 'inactiveError' };
    component.leg = { isDisplayed: true, isLiveStreamOpened: true  } as any;
    watchRulesService.isInactiveUser.and.returnValue(true);
    component.onVideoStreamEvent(error);
    expect(component.leg.isLiveStreamOpened).toBeTruthy();
  });

  it('onVideoStreamEvent', () => {
    const error = { output: 'playStreamError', value: 'error' };
    component.leg = { isDisplayed: true, isLiveStreamOpened: true } as any;
    watchRulesService.isInactiveUser.and.returnValue(false);
    component.onVideoStreamEvent(error);
    expect(component.leg.isLiveStreamOpened).toBeFalsy();
  });

  it('#HorseRacingBIR cms config as null', () => {
    component.leg.eventEntity = {
      id: 555,
      name: 'Leg event',
      markets: [],
      categoryCode: 'HORSE_RACING',
      isFinished: 'false'
    } as any;
    cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of(null));
    component.ngOnInit();
    expect(component.isHRLiveEnabled).not.toBeTruthy();
  });

  it('#HorseRacingBIR cms config with streamEnabled as null', () => {
    component.leg.eventEntity = {
      id: 555,
      name: 'Leg event',
      markets: [],
      categoryCode: 'HORSE_RACING',
      isFinished: 'false'
    } as any;
    component.event = { categoryId: '1' } as any;
    cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of({HorseRacingBIR: {}}));
    const config = {
      insightsDrillDownTags: ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA']
    };
    cmsService.getFeatureConfig.and.returnValue(of(config));
    component.ngOnInit();
    expect(component.isHRLiveEnabled).not.toBeTruthy();
  });

  it('#HorseRacingBIR cms config', () => {
    component.leg.eventEntity = {
      id: 555,
      name: 'Leg event',
      markets: [],
      categoryCode: 'HORSE_RACING',
      isFinished: 'false',
      drilldownTagNames: ['EVFLAG_PVM']
    } as any;
    component.event = { categoryId: '1' } as any;
    component.leg.isLiveStreamOpened = true;
    cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of({HorseRacingBIR: {streamEnabled: true}}));
    component.ngOnInit();
    expect(component.isHRLiveEnabled).toBeTruthy();
  });

  it('IS_LIVE subscription', () => {
    component.leg.eventEntity = {
      id: 555,
      name: 'Leg event',
      markets: [],
      categoryCode: 'HORSE_RACING',
      isFinished: 'false'
    } as any;
    component.playStream = jasmine.createSpy('playStream');
    component.leg.isLiveStreamOpened = true;
    component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
      if (ch === pubSubService.API.IS_LIVE) {
        fn('555');
      }
    });
    component.ngOnInit();
    expect(component.playStream).toHaveBeenCalled();
  });  
  
  it('#Betsharing for sports regular bets with multiples', () => {
    spyOn(component as any,'getRunnerNumberAndStallNumber').and.returnValue({runnerNumber: 'test runner',
      stallNumber: 'test stall'});
    component.isMultiples = true;
    component.eventMarketDescription = 'test desc';
    component.displayBogPrice = true;
    component.startingOddsCaption = '5/3';
    component.leg = leg;
    component.leg.cashoutId = '12';
    component.leg.part[0].outcome = '1245' as any;
    component.leg.eventEntity.categoryId = HORSE_RACING_CATEGORY_ID;
    component.event = { categoryId: '1' } as any;
    component.outcomeNames = ['test outcomes'];
    component.eventEntity.id = 123;
    component.settingDataInSession();
    expect(component.sessionData['123-12-1245'].outcomeNames).toEqual([ 'test outcomes (test runner)' ]);
  });

  it('#Betsharing for sports regular bets without multiples', () => {
    sessionStorageService.get.and.returnValue([{'123':{}}]);
    component.isMultiples = false;
    component.outcomeNames = ['test outcomes'];
    component.eventMarketDescription = 'test desc';
    component.displayBogPrice = false;
    component.takenOddsCaption = '2/3';
    component.leg = leg;
    component.leg.cashoutId = '12';
    component.leg.part[0].outcome[0].id= '1235';
    component.leg.eventEntity.categoryId = HORSE_RACING_CATEGORY_ID;
    component.event = { categoryId: '1' } as any;
    component.eventEntity.id = 123;
    component.settingDataInSession();
    expect(component.sessionData['123-12-1235'].outcomeNames).toEqual([ 'test outcomes' ]);
  });

  describe('@HostListener onClick', () => {
    beforeEach(() => {
      component.goToEvent = jasmine.createSpy('goToEvent');
      component.bet = { eventSource: { isAccaEdit: undefined } } as any;
      component.leg = { eventEntity: { isDisplayed: true, isLiveStreamOpened: false } } as any;
      component.tooltipShown = false;
    });

    it('should navigate to event if all conditions are met', () => {
      component.onClick();
      expect(component.goToEvent).toHaveBeenCalled();
    });

    describe('should not navigate to event', () => {
      it('when bet.eventSource.isAccaEdit is true', () => {
        component.bet.eventSource.isAccaEdit = true;
      });
      it('when leg.eventEntity is unavailable', () => {
        component.leg.eventEntity = null;
      });
      it('when leg.eventEntity.isDisplayed is falsy', () => {
        component.leg.eventEntity.isDisplayed = false;
      });
      it('when leg.eventEntity.isDisplayed is falsy', () => {
        component.tooltipShown = true;
      });

      afterEach(() => {
        component.onClick();
        expect(component.goToEvent).not.toHaveBeenCalled();
      });
    });
  });

  describe('ngOnInit', () => {
    const eventEntity = {
      id: 555,
      name: 'Leg event',
      markets: [],
      categoryCode: 'HORSE_RACING',
      isFinished: 'false',
      drilldownTagNames:['EVFLAG_PVA']
    } as any;

    beforeEach(() => {
      component.leg = leg;
      component.leg.part[0].outcome =[ {
        flags: ['2UP'],
        result:{
          value:"W",
          confirmed:"Y"
        }
      }] as any;
      component.isLastBet = true;

      component['filtersService']['isGreyhoundsEvent'] = jasmine.createSpy().and.returnValue(false);
      spyOn(component as any, 'formatOdds');
      spyOn(component as any, 'getOutcomeName').and.returnValue([]);
      spyOn(component as any, 'parseEventMarketDescription');
      spyOn(component as any, 'getRuleFourDeduction');
    });

    it('source as 5-A-Side', () => {
      component.bet.eventSource.source = 'f';
      component.leg.eventEntity = eventEntity;
      component.ngOnInit();
      expect(component.sportIconSvgId).toBe('5-a-side');
    });
    it('getItemSvg with missing config', () => {
      cmsService.getItemSvg.and.returnValue(of({}));
      component.leg.eventEntity = eventEntity;
      component.ngOnInit();
      expect(component.sportIconSvgId).toBe('icon-generic');
    });
    it('should set isFCTC to true', () => {
      component.leg.legSort = { code: 'CF' } as any;
      component.ngOnInit();
      expect(component.isFCTC).toEqual(true);
      expect(component.excludedDrilldownTagNames).toEqual('EVFLAG_MB,MKTFLAG_MB,EVFLAG_PB,MKTFLAG_PB');
    });

    it('should set isFCTC to false', () => {
      component.leg.legSort = 'MC';
      component.ngOnInit();
      expect(component.isFCTC).toEqual(false);
    });

    it('should set shouldShowFiveASideIcon to true', () => {
      component.bet.eventSource = { source: 'f' } as any;
      component.ngOnInit();
      expect(component.shouldShowFiveASideIcon).toEqual(true);
    });

    it('should set shouldShowFiveASideIcon to false', () => {
      component.bet.eventSource = { source: 'M' } as any;
      component.ngOnInit();
      expect(component.shouldShowFiveASideIcon).toEqual(false);
    });

    it('should set shouldShowFiveASideIcon to false', () => {
      component.ngOnInit();
      expect(component.shouldShowFiveASideIcon).toEqual(false);
    });

    it('should set isLDMarket', () => {
      component.bet.eventSource = { betTags: {betTag : [{tagName : 'LDIP'}]} } as any;
      component.ngOnInit();
      expect(component.isLDMarket).toEqual(true);
    });

    it('should set isUKorIRE to true', () => {
      eventService.isUKorIRE.and.returnValue(true);
      component.leg.eventEntity = {
        categoryId: 16,
        markets: []
      } as any;
      component.ngOnInit();
      expect(eventService.isUKorIRE).toHaveBeenCalledWith({ categoryId: 16,  markets: [] });
      expect(component.isUKorIRE).toEqual(true);
    });

    it('should set isUKorIRE to false', () => {
      component.leg.eventEntity = null;
      component.ngOnInit();
      expect(eventService.isUKorIRE).not.toHaveBeenCalled();
      expect(component.isUKorIRE).toEqual(false);
    });

    it('should call stack of private methods', () => {
      component.ngOnInit();

      expect(component['formatOdds']).toHaveBeenCalledWith(leg);
      expect(component['getOutcomeName']).toHaveBeenCalledWith(leg);
      expect(component['parseEventMarketDescription']).toHaveBeenCalled();
      expect(component['getRuleFourDeduction']).toHaveBeenCalledWith(leg);
      expect(pubSubService.subscribe).toHaveBeenCalled();
    });

    it(`should define 'event'`, () => {
      component.leg.eventEntity = eventEntity;

      component.ngOnInit();

      expect(component.event).toEqual(eventEntity);
    });

    it(`should call 'init' if 'event' is defined`, () => {
      spyOn(component as any, 'init');
      component.leg.eventEntity = eventEntity;

      component.ngOnInit();

      expect(component['init']).toHaveBeenCalled();
    });

    it(`should Not call 'init' if 'event' is Not defined`, () => {
      spyOn(component as any, 'init');
      component.leg.eventEntity = null;

      component.ngOnInit();

      expect(component['init']).not.toHaveBeenCalled();
    });

    it(`should call checkForBogOddsAndResetOddsCaptions`, () => {
      spyOn(component as any, 'checkForBogOddsAndResetOddsCaptions');
      component.leg.eventEntity = eventEntity;

      component.ngOnInit();

      expect(component['checkForBogOddsAndResetOddsCaptions']).toHaveBeenCalled();
    });

    it(`if bet is settled than BOG enabled is checked from CMS`, () => {
      component.leg.eventEntity = eventEntity;
      (<any>component.bet) = {eventSource: {settled: 'Y'}};
      cmsService.isBogFromCms = jasmine.createSpy().and.returnValue(of(true));

      component.ngOnInit();

      expect(cmsService['isBogFromCms']).toHaveBeenCalled();
    });

    it('publish each stake height', fakeAsync(() => {
      pubSubService.publish.and.callThrough();
      component.bet = { eventSource: { isAccaEdit: undefined, numLegs: 1 }, location: 'openBets' } as any;
      component.leg.status = 'won';
      component.leg.legNo = '1';
      component.leg.eventEntity = eventEntity;
      component.isLastBet = isLastBet; 
      component.ngOnInit();
      tick();        
      expect(pubSubService.publish).toHaveBeenCalledWith('UPDATE_ITEM_HEIGHT');
      expect(pubSubService.publish).toHaveBeenCalledWith('BET_LEGS_LOADED', 'openBets');
    }));
    it('should not publish BET_LEGS_LOADED', fakeAsync(() => {
      component.leg.status = 'won';
      component.leg.eventEntity = eventEntity;
      component.leg.legNo = '1';
      component.isLastBet = isLastBet;
      pubSubService.publish.and.callThrough();
      component.bet = { eventSource: { numLegs: null } } as any;
      component.ngOnInit();
      tick();
      expect(pubSubService.publish).not.toHaveBeenCalledWith('BET_LEGS_LOADED', 'openBets');
    }));

    describe('isMultiples', () => {
      beforeEach(() => {
        component.leg.part[0].outcome = [{
          flags: ['2UP'],
          result: {
            value: "W",
            confirmed: "Y"
          }
        }] as any;
        spyOn(component as any, 'init');
      });

      it(`should be Truthy if outcomeNames.length === 1`, () => {
        component.ngOnInit();

        expect(component.isMultiples).toBeFalsy();
      });

      it(`should be Truthy if outcomeNames.length === 1`, () => {
        (component['getOutcomeName'] as jasmine.Spy).and.returnValue([1]);

        component.ngOnInit();

        expect(component.isMultiples).toBeFalsy();
      });

      it(`should be Truthy if outcomeNames.length > 1`, () => {
        (component['getOutcomeName'] as jasmine.Spy).and.returnValue([1, 2, 3]);

        component.ngOnInit();

        expect(component.isMultiples).toBeTruthy();
      });

    });

    it('should set showRemovedLabel and statusName', () => {
      component.ngOnInit();
      expect(component.showRemovedLabel).toBeFalsy();
      expect(component.statusName).toEqual('won');
      expect(component.isRemovingState).toEqual(false);
    });
    it('should call subscribeMatchCommentary',()=>{
      spyOn(component as any, 'subscribeMatchCommentary');
      component.leg.eventEntity = eventEntity;
      component.ngOnInit();
      expect(component['subscribeMatchCommentary']).toHaveBeenCalledWith(eventEntity,component.leg);
    });  
  });

  it('#ngOnDestroy should call pubSubService.unsubscribe', () => {
    const controllerIdentifier = 'BetLegItemComponent123';
    component['controllerIdentifier'] = controllerIdentifier;
    component.leg = {
      ...leg,
      legSort: '',
      eventEntity: { id: 32, name: 'event name',categoryCode:'FOOTBALL',isStarted: true, eventIsLive: true,isResulted:false}
    } as any;
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith(controllerIdentifier);
  });
  it('#ngOnDestroy should call pubSubService.unsubscribe', () => {
    component.leg = {
      ...leg,
      legSort: '',
      eventEntity: { id: 32, name: 'event name',categoryCode:'FOOTBALL',isStarted: true, eventIsLive: true,isResulted:false}
    } as any;
    component['subscriptiontoMatchCmtryEnabled'] = true;
    component.ngOnDestroy();
    expect(handleVarReasoningUpdatesService.unsubscribeForMatchCmtryUpdates).toHaveBeenCalledWith('32');
  });


  describe('#goToEvent', () => {
    beforeEach(() => {
      component.event = <any>{};
      component.isEnhanced = false;
      component.isVirtuals = false;
      component.sportPath = 'racing';
    });

    describe('should return empty string', () => {
      it('if sportpath is empty', () => {
        component.sportPath = '';
      });
      it('if isEnhanced', () => {
        component.isEnhanced = true;
      });
      it('if isVirtuals', () => {
        component.isVirtuals = true;
      });
      afterEach(() => {
        expect(component.goToEvent()).toEqual('');
      });
    });

    it('should retunn url string if no preventing conditions are met', () => {
      expect(component.goToEvent()).toEqual('url');
    });

    it('#goToEvent if could not get sportType', () => {
      component.event = <any>{};
      component.sportPath = 'racing';
      component.goToEvent();
      expect(component.goToEvent()).toEqual('url');
    });

    it(`should return if Not sportPath and isEnhanced equal false`, () => {
      component.sportPath = undefined;
      component.isEnhanced = false;

      expect(component.goToEvent()).toEqual('');
    });

    describe('categoryName', () => {
      beforeEach(() => {
        routingHelperStub.formEdpUrl.and.callFake(url => url);
        component.isEnhanced = false;
        component.sportPath = 'text';
      });

      it(`should define as sportPath if event.categoryName is Falthy`, () => {
        expect(component.goToEvent()).toEqual(jasmine.objectContaining({ categoryName: 'text' }));
      });

      it(`should not change`, () => {
        const categoryName = 'some category';
        component.event.categoryName = categoryName;

        expect(component.goToEvent()).toEqual(jasmine.objectContaining({ categoryName }));
      });

      it('has isMyBetsInCasino as true and showLeavingCasinoDialog as false', () => {
        component.isMyBetsInCasino = true;
        component.showLeavingCasinoDialog = false;
        component.goToEvent();
        expect(component['casinoMyBetsIntegratedService'].goToSportsCTABtnClick).toHaveBeenCalled();  
      });
    });
  });

  it('#ngOnChanges should not set showRemovedLabel, showRemovedLabel, isRemovingState', () => {
    component.showRemovedLabel = false;
    component.statusName = 'won';
    component.ngOnChanges({} as any);
    expect(component.showRemovedLabel).toBeFalsy();
    expect(component.statusName).toEqual('won');
    expect(component.isRemovingState).toBeFalsy(false);
  });

  it('#ngOnChanges should set showRemovedLabel and showRemovedLabel', () => {
    component.leg = {
      status: 'lost',
      removing: true,
      eventEntity: null
    } as any;
    component.ngOnChanges({
      leg:  { currentValue: component.leg }
    } as any);
    expect(component.showRemovedLabel).toBeTruthy();
    expect(component.statusName).toEqual('lost');
  });
  describe('getStatusName', () => {
    it('#statusIconName should return icon name for singles', () => {
      component.leg = leg;
      component.leg.status = 'won';
      expect(component.getStatusName).toEqual('won');
      component.leg.status = 'suspended';
      localeStub.getString = () => 'suspended';
      expect(component.getStatusName).toEqual('suspended');
      localeStub.getString = () => 'void';
      component.leg.status = 'void';
      expect(component.getStatusName).toEqual('void');
    });
    it('#statusIconName should return icon name for multiples', () => {
      component.leg = leg;
      component.isMultiples = true;
      component.bet.eventSource.totalStatus = 'won';
      component.leg.status = 'won';
      expect(component.getStatusName).toEqual('won');
      component.bet.eventSource.totalStatus = 'won';
      component.leg.status = 'lost';
      expect(component.getStatusName).toEqual('won');
      component.bet.eventSource.totalStatus = 'test';
      component.leg.status = 'test';
      expect(component.getStatusName).toEqual('');
      component.bet.eventSource.totalStatus = 'lost';
      component.leg.status = 'lost';
    });
  });
  
  it('#isESPCheck should return true', () => {
    const betType = {
      eventSource: {
        sortType: ''
      }
    };
    const marketName = 'Win or Each Way';
    const market = [{
      drilldownTagNames: 'MKTFLAG_EPR',
      templateMarketName: 'Win or Each Way'
    }];
    component.isESPCheck(betType,market, marketName);
    expect( component.isESPCheck(betType,market, marketName)).toBeTruthy();
  });

  it('#isESPCheck should return true for forecast markets', () => {
    const betType = {
      eventSource: {
        sortType: 'Forecast'
      }
    };
    const marketName = 'Win or Each Way';
    const market = [{
      drilldownTagNames: 'MKTFLAG_EPR',
      templateMarketName: 'Win or Each Way'
    }];
    component.isESPCheck(betType,market, marketName);
    expect( component.isESPCheck(betType,market, marketName)).toBeFalsy();
  });

  it('#isESPCheck should return true without sorttype ', () => {
    const betType = {
      eventSource: {
        type: 'Forecast'
      }
    };
    const marketName = 'Win or Each Way';
    const market = [{
      drilldownTagNames: 'MKTFLAG_EPR',
      templateMarketName: 'Win or Each Way'
    }];
    component.isESPCheck(betType,market, marketName);
    expect( component.isESPCheck(betType,market, marketName)).toBeTruthy();
  });

  it('#isESPCheck should return true without sorttype when there is extraplace offered event', () => {
    const betType = {
      eventSource: {
        type: 'Forecast'
      }
    };
    const marketName = 'Win or Each Way';
    const market = [{
      drilldownTagNames: 'MKTFLAG_EPR',
      templateMarketName: ''
    }];
    component.extraPlaceOfferedEvent = {} as any;
    const result = component.isESPCheck(betType,market, marketName);
    expect( result ).toBe(false);
  });

  it('#isESPCheck should return true without sorttype when market is outright ', () => {
    const betType = {
      eventSource: {
        stype: 'Forecast'
      }
    };
    const marketName = 'Outright';
    const market = [{
      drilldownTagNames: 'MKTFLAG_EPR',
      templateMarketName: 'Outright'
    }];
    const result = component.isESPCheck(betType,market, marketName);
    expect( result ).toBe(true);
  });

  it('#isESPCheck should return true for tricast markets', () => {
    const betType = {
      eventSource: {
        sortType: 'Tricast'
      }
    };
    const marketName = 'Win or Each Way';
    const market = [{
      drilldownTagNames: 'MKTFLAG_EPR',
      templateMarketName: 'Win or Each Way'
    }];
    component.isESPCheck(betType,market, marketName);
    expect( component.isESPCheck(betType,market, marketName)).toBeFalsy();
  });

  it('#isESPCheck should return false', () => {
    const betType = {
      eventSource: {
        sortType: ''
      }
    };
    const marketName = 'Win only';
    const market = [{
      drilldownTagNames: 'MKTFLAG_EPR',
      templateMarketName: 'Win or Each Way'
    }];
    component.isESPCheck(betType,market, marketName);
    expect( component.isESPCheck(betType, market, marketName)).toBeFalsy();
  });

  it('#isESPCheck should check outright market return true', () => {
    const betType = {
      eventSource: {
        sortType: ''
      }
    };
    const marketName = 'Outright';
    const market = [{
      drilldownTagNames: 'MKTFLAG_EPR',
      templateMarketName: 'Outright'
    }];
    component.isESPCheck(betType,market, marketName);
    expect( component.isESPCheck(betType,market, marketName)).toBeTruthy();
  });

  it('#eventEntity should return correct event', () => {
    const backupEventEntity = {
      id: 123,
      name: 'Backup event'
    };

    const eventEntity = {
      id: 8,
      name: 'Leg event'
    } as any;

    leg.eventEntity = null;

    component.leg = leg;
    expect(component.eventEntity).toBeFalsy();

    component.leg.noEventFromSS = false;
    component.leg.backupEventEntity = backupEventEntity as any;
    expect(component.eventEntity).toBeFalsy();

    component.leg.noEventFromSS = true;
    expect(component.eventEntity).toEqual(backupEventEntity as any);

    component.leg.eventEntity = eventEntity;
    expect(component.eventEntity).toEqual(eventEntity);
  });

  it('#winLosIndicator should return correct indicator or call #getWinLosIndicator', () => {
    component['getWinLosIndicator'] = jasmine.createSpy().and.returnValue('getWinLosIndicatorValue');

    component.leg = leg;
    component.leg.status = 'open';
    expect(component.winLosIndicator).toBeFalsy();

    component.leg.eventEntity = {
      categoryCode: 'FOOTBALL',
      comments: {}
    } as any;
    component.eventMarketDescription = 'Match Result';

    expect(component.winLosIndicator).toEqual('getWinLosIndicatorValue');
    expect(component['getWinLosIndicator']).toHaveBeenCalledWith(component.leg);

    component.eventMarketDescription = 'Match Betting';
    expect(component.winLosIndicator).toEqual('getWinLosIndicatorValue');
    expect(component['getWinLosIndicator']).toHaveBeenCalledWith(component.leg);
  });

  it('#trackByOutcomeName should return concatenated value', () => {
    expect(component.trackByOutcomeName(321, 'test-string')).toEqual('321_test-string');
  });

  it('#showSilk should return showSilk status', () => {
    expect(component.showSilk(leg)).toBeFalsy();

    leg.eventEntity = { categoryId: HORSE_RACING_CATEGORY_ID } as any;
    expect(component.showSilk(leg)).toBe(true);
  });

  it('#getSilkStyle should call RaceOutcomeDetailsService.getSilkStyleForPage', () => {
    const allSilkyNames = ['name1', 'name2'];
    const eventEntity: ISportEvent = { id: 32, name: 'event name' } as any;
    leg.allSilkNames = allSilkyNames;
    leg.eventEntity = eventEntity;

    component.getSilkStyle(leg, 0);
    expect(raceOutcomeDetailsServiceStub.getSilkStyleForPage).toHaveBeenCalledWith('51', eventEntity, allSilkyNames, true);
  });

  it('#getSilkStyle should call RaceOutcomeDetailsService.getSilkStyleForPage with outcome', () => {
    const allSilkyNames = ['name1', 'name2'];
    const eventEntity: ISportEvent = { id: 32, name: 'event name' } as any;
    leg.allSilkNames = allSilkyNames;
    leg.eventEntity = eventEntity;
    leg.part[0].outcomeId = undefined;
    leg.part[0].outcome = '51';

    component.getSilkStyle(leg);
    expect(raceOutcomeDetailsServiceStub.getSilkStyleForPage).toHaveBeenCalledWith('51', eventEntity, allSilkyNames, true);
  });

  it('#isSilkAvailable should call RaceOutcomeDetailsService.isSilkAvailableForOutcome', () => {
    const eventEntity: ISportEvent = { id: 32, name: 'event name' } as any;
    leg.eventEntity = eventEntity;
    component.isSilkAvailable(leg, 0);
    expect(raceOutcomeDetailsServiceStub.isSilkAvailableForOutcome).toHaveBeenCalledWith('51', eventEntity);
  });

  it('#isSilkAvailable should call RaceOutcomeDetailsService.isSilkAvailableForOutcome with outcome', () => {
    const eventEntity: ISportEvent = { id: 32, name: 'event name' } as any;
    leg.eventEntity = eventEntity;
    leg.part[0].outcomeId = undefined;
    leg.part[0].outcome = '51';

    component.isSilkAvailable(leg);
    expect(raceOutcomeDetailsServiceStub.isSilkAvailableForOutcome).toHaveBeenCalledWith('51', eventEntity);
  });

  describe('#isGenericSilk should check whether default silk image should be shown', () => {
    const index = 0,
      eventEntity: ISportEvent = { id: 32, name: 'event name' } as any;

    beforeEach(() => {
      leg.eventEntity = eventEntity;
      component.bet = {eventSource: {leg: [leg]}, location: 'location'} as any;
      spyOn(component, 'isSilkAvailable').and.returnValue(false);
      (raceOutcomeDetailsServiceStub as any).isUnnamedFavourite.and.returnValue(false);
    });

    it('should return false when not isUnnamedFavourite but silks are not available', () => {
      expect(component.isGenericSilk(leg, index)).toEqual(true);
      expect(raceOutcomeDetailsServiceStub.isUnnamedFavourite).toHaveBeenCalledWith('51', eventEntity);
    });

    it('should return true when isUnnamedFavourite', () => {
      (raceOutcomeDetailsServiceStub as any).isUnnamedFavourite.and.returnValue(true);
      expect(component.isGenericSilk(leg, index)).toEqual(true);
      expect(component.isSilkAvailable).toHaveBeenCalledWith(leg, index);
    });

    it('should return true when isUnnamedFavourite calls with outcome', () => {
      (raceOutcomeDetailsServiceStub as any).isUnnamedFavourite.and.returnValue(true);
      leg.part[0].outcomeId = undefined;
      leg.part[0].outcome = '51';
      const result = component.isGenericSilk(leg);

      expect(result).toEqual(true);
      expect(component.isSilkAvailable).toHaveBeenCalledWith(leg, index);
    });

    it('should return false when not isUnnamedFavourite but silks are available', () => {
      (component as any).isSilkAvailable.and.returnValue(true);
      expect(component.isGenericSilk(leg, index)).toEqual(false);
    });

    it('should return false when it is isUnnamedFavourite and silks are available', () => {
      (raceOutcomeDetailsServiceStub as any).isUnnamedFavourite.and.returnValue(true);
      (component as any).isSilkAvailable.and.returnValue(true);
      expect(component.isGenericSilk(leg, index)).toEqual(false);
    });

    afterEach(() => {
      expect(raceOutcomeDetailsServiceStub.isUnnamedFavourite).toHaveBeenCalledWith('51', eventEntity);
    });
  });

  describe('getClasses', () => {
    beforeEach(() => {
      component.bet = {
        eventSource: {
          isAccaEdit: true
        }
      } as any;

      component.leg = {
        eventEntity: {}
      } as any;
      component.isEnhanced = false;
      component.isVirtuals = false;
    });
    it('classes should be "lost removed"', () => {
      expect(component.getClasses({ status: 'lost', removedLeg: [{}] } as any)).toEqual('lost removed');
    });

    it('classes should be "won arrowed-item"', () => {
      component.bet.eventSource.settled = 'N';
      component.sportPath = 'Football';
      expect(component.getClasses({ status: 'suspended' } as any)).toContain('suspended');
    });

    it('classes should be "won arrowed-item"', () => {
      component.bet.eventSource.settled = 'Y';
      component.sportPath = 'Football';
      expect(component.getClasses({ status: 'suspended' } as any)).not.toContain('suspended');
    });

    it('classes should be "void is-acca-remove"', () => {
      component.bet.eventSource.settled = 'Y';
      component.bet.eventSource.totalStatus = '';
      component.sportPath = 'Football';
      expect(component.getClasses({ status: 'void' } as any)).not.toContain('void is-acca-remove');
    });

    it('classes should be "void-item"', () => {
      component.bet.eventSource.settled = 'Y';
      component.bet.eventSource.totalStatus = 'void';
      component.sportPath = 'Football';
      expect(component.getClasses({ status: 'void' } as any)).not.toContain('void-item');
    });

    it('classes should be "won arrowed-item"', () => {
      component.leg.eventEntity.isDisplayed = true;
      component.bet.eventSource.isAccaEdit = false;
      component.sportPath = 'Football';
      expect(component.getClasses({ status: 'won' } as any)).toEqual('won arrowed-item');
    });

    it(`classes should not set "arrowed-item" if isAccaEdit is equal true`, () => {
      component.leg.eventEntity.isDisplayed = true;
      component.bet.eventSource.isAccaEdit = true;
      component.sportPath = 'Football';

      expect(component.getClasses({ status: 'won' } as any)).not.toContain('arrowed-item');
    });

    describe('classes should not set "arrowed-item" class', () => {
      beforeEach(() => {
        component.leg.eventEntity.isDisplayed = true;
        component.bet.eventSource.isAccaEdit = false;
        component.sportPath = 'Football';
      });

      it('on Enhanced Multiples', () => {
        component.isEnhanced = true;
        expect(component.getClasses({ status: 'won' } as any)).toEqual('won');
      });

      it('on Virtual Sports', () => {
        component.isVirtuals = true;
        expect(component.getClasses({ status: 'won' } as any)).toEqual('won is-virtual');
      });
    });

    it('classes should not set "arrowed-item" class', () => {
      component.leg.eventEntity.isDisplayed = true;
      component.bet.eventSource.isAccaEdit = false;
      component.sportPath = undefined;
      expect(component.getClasses({ status: 'won' } as any)).toEqual('won');
    });

    it('classes should not set "arrowed-item" class and set "byb-list"', () => {
      component.leg.eventEntity.isDisplayed = true;
      component.bet.eventSource.isAccaEdit = false;
      component.sportPath = 'sport-path';
      component.isBuildYourBet = true;
      expect(component.getClasses({ status: 'open' } as any)).toEqual('open byb-list');
    });

    it('classes should be "open removed is-acca-undo"', () => {
      component.leg.removing = true;
      expect(component.getClasses({ status: 'open', removing: true, removedLeg: false } as any)).toEqual('open removed is-acca-undo');
    });

    it('classes should be "open is-acca-remove"', () => {
      component.leg.removing = false;
      expect(component.getClasses({ status: 'open', removing: false } as any)).toEqual('open is-acca-remove');
    });

    it('classes should be "open is-virtual"', () => {
      component.bet.eventSource.isAccaEdit = false;
      component.isVirtuals = true;
      expect(component.getClasses({ status: 'open' } as any)).toEqual('open is-virtual');
    });

    it('should not crash if leg.eventEntity is missing', () => {
      delete component.leg.eventEntity;
      component.bet.eventSource.isAccaEdit = false;
      expect(component.getClasses({ status: 'open' } as any)).toEqual('open');
    });
  });

  describe('init', () => {
    beforeEach(() => {
      component.event = { categoryId: '1' } as any;
      spyOn(component, 'showSilk');
      spyOn(component as any, 'setSportConfig');
      component.outcomeNames = jasmine.createSpyObj('outcomeNames', ['some']);
    });

    describe('isEnhanced should be Falsy if', () => {
      it(`if typeName is Not equal 'Enhanced Multiples'`, () => {
        component.event.typeName = 'typeName';
      });
      it(`isEnhanced should be Falsy if event is not defined`, () => {
        component.event = null;
      });
      afterEach(() => {
        component['init']();
        expect(component.isEnhanced).toBeFalsy();
      });
    });
    it(`isEnhanced should be Truthy if typeName equal 'Enhanced Multiples'`, () => {
      component.event.typeName = 'Enhanced Multiples';
      component['init']();
      expect(component.isEnhanced).toBeTruthy();
    });

    describe('isVirtuals should be Falsy if', () => {
      it('if categoryCode is Not equal VIRTUAL', () => {
        component.event.categoryCode = 'categoryCode';
      });
      it('isVirtuals should be Falsy if event is not defined', () => {
        component.event = null;
      });
      afterEach(() => {
        component['init']();
        expect(component.isVirtuals).toBeFalsy();
      });
    });
    it('isVirtuals should be Truthy if categoryCode equal VIRTUAL', () => {
      component.event.categoryCode = 'VIRTUAL';
      component['init']();
      expect(component.isVirtuals).toBeTruthy();
    });

    it(`should define shouldShowSilk`, () => {
      component.shouldShowSilk = undefined;
      (component['showSilk'] as jasmine.Spy).and.returnValue(true);
      component['init']();
      expect(component['showSilk']).toHaveBeenCalledWith(component.leg);
      expect(component.shouldShowSilk).toBeTruthy();
    });

    describe('silkSpace', () => {
      beforeEach(() => {
        spyOn(component, 'isGenericSilk' as any).and.callFake((elemLeg, i) => elemLeg.part[i].hasGenericSilk);
        spyOn(component, 'isSilkAvailable' as any).and.callFake((elemLeg, i) => elemLeg.part[i].hasSilkAvailable);
        component.outcomeNames = ['someName', 'name'];
        (component['showSilk'] as jasmine.Spy).and.returnValue(false);
      });
      describe('should be false', () => {
        it(`should be false if isMultiple equal false`, () => {
          component.isMultiples = false;
        });

        it(`should be false if isMultiple equal false and shouldShowSilk equal false`, () => {
          component.isMultiples = false;
        });

        it(`should be false if isMultiple equal true and have not GenericSilk or SilkAvailable`, () => {
          component.isMultiples = true;
          component.leg = { part: [{ hasGenericSilk: false }, { hasSilkAvailable: false }] } as any;
        });

        it(`should be false if isMultiple equal false and have not GenericSilk or SilkAvailable and shouldShowSilk equal true`, () => {
          component.isMultiples = false;
          (component['showSilk'] as jasmine.Spy).and.returnValue(true);
          component.leg = { part: [{ hasGenericSilk: false }, { hasSilkAvailable: false }] } as any;
        });

        it(`should be false if isMultiple equal false and have not GenericSilk or SilkAvailable`, () => {
          component.isMultiples = false;
          component.leg = { part: [{ hasGenericSilk: false }, { hasSilkAvailable: false }] } as any;
        });

        it(`should be false if isMultiple equal true and have not GenericSilk or SilkAvailable and shouldShowSilk equal true`, () => {
          component.isMultiples = true;
          (component['showSilk'] as jasmine.Spy).and.returnValue(true);
          component.leg = { part: [{ hasGenericSilk: false }, { hasSilkAvailable: false }] } as any;
        });

        it(`should be false if isMultiple equal true and have not GenericSilk or SilkAvailable and shouldShowSilk equal false`, () => {
          component.isMultiples = true;
          component.leg = { part: [{ hasGenericSilk: false }, { hasSilkAvailable: false }] } as any;
        });

        afterEach(() => {
          component['init']();
          expect(component.silkSpace).toBeFalsy();
        });
      });

      describe('should be Truthy if isMultiples and shouldShowSilk and some of outcomeNames', () => {
        beforeEach(() => {
          component.isMultiples = true;
          (component['showSilk'] as jasmine.Spy).and.returnValue(true);
          component.outcomeNames.some = jasmine.createSpy('some').and.returnValue(true);
        });

        it(`and isGenericSilk`, () => {
          component.leg = { part: [{ hasGenericSilk: false }, { hasGenericSilk: true }] } as any;
        });

        it(`and isSilkAvailable`, () => {
          component.leg = { part: [{ hasSilkAvailable: false }, { hasSilkAvailable: true }] } as any;
        });

        afterEach(() => {
          component.shouldShowSilk  = true;
          component['init']();

          expect(component.silkSpace).toBeTruthy();
        });
      });
    });
  });

  describe('resetOddsCaption', () => {
    beforeEach(() => {
      component.event = { categoryId: '1' }as any;
      component['fracToDecService'].getFormattedValue = (num, den) => `${num}/${den}`;

      (<any>component.leg) = {part: [{priceNum: 4, priceDen: 8, price: [{priceStartingNum: 8, priceStartingDen: 9}]}]};
      cmsService.isBogFromCms = jasmine.createSpy().and.returnValue(of(true));
    });

    it(`odds captions were reset properly - plain and bog-prev`, () => {
      component.displayBogPrice = true;
      component.resetOddsCaptions();

      expect(component.takenOddsCaption).toBe('4/8');
      expect(component.startingOddsCaption).toBe('8/9');
    });

    it(`startingOddsCaption were not reset if bog is not enabled`, () => {
      component.displayBogPrice = false;
      component.resetOddsCaptions();

      expect(component.takenOddsCaption).toBe('4/8');
      expect(component.startingOddsCaption).toBeFalsy();
    });

    it(`startingOddsCaption were not reset if they are equal to taken`, () => {
      (<any>component.leg) = {part: [{priceNum: 4, priceDen: 8, price: [{priceStartingNum: 4, priceStartingDen: 8}]}]};
      component.displayBogPrice = true;
      component.resetOddsCaptions();

      expect(component.takenOddsCaption).toBe('4/8');
      expect(component.startingOddsCaption).toBeFalsy();
    });

    it(`startingOddsCaption were not reset if they are no prices`, () => {
      (<any>component.leg) = {part: [{priceNum: undefined, priceDen: undefined, price: [{priceStartingNum: '', priceStartingDen: null}]}]};
      component.displayBogPrice = true;
      component.resetOddsCaptions();

      expect(component.startingOddsCaption).toBeFalsy();
    });
  });

  describe('setSportConfig', () => {
    beforeEach(() => {
      component.event = { categoryId: '1' }as any;
    });

    it(`should define 'sportType'`, () => {
      component['setSportConfig']();

      expect(component.sportPath).toEqual('horsePath');
      expect(sportsConfigHelperService.getSportPathByCategoryId).toHaveBeenCalled();
    });

    it(`should define 'sportType'`, () => {
      component.sportPath = 'racing';
      component['setSportConfig']();

      expect(sportsConfigHelperService.getSportPathByCategoryId).not.toHaveBeenCalled();
    });
  });

  describe('formatOdds', () => {
    it(`should return SP price (priceTypeCodes = 'SP,')`, () => {
      component['formatOdds']({
        part: [{ priceNum: 1, priceDen: 2 }],
        eventEntity: {
          markets: [{ priceTypeCodes: 'SP,' }]
        }
      } as any);
      expect(localeStub.getString).toHaveBeenCalledWith('bethistory.SP');
    });

    it(`should return SP price (no price num/den)`, () => {
      component['formatOdds']({
        part: [{ priceNum: 0, priceDen: 0 }],
      } as any);
      expect(localeStub.getString).toHaveBeenCalledWith('bethistory.SP');
    });

    it(`should return SP price (priceType = 'S')`, () => {
      component['formatOdds']({
        part: [{
          priceNum: 1, priceDen: 2,
          price: [{
            priceType: { code: 'S' }
          }]
        }],
      } as any);
      expect(localeStub.getString).toHaveBeenCalledWith('bethistory.SP');
    });

    it(`should return decimal price`, () => {
      component['formatOdds']({
        part: [{ priceNum: 1, priceDen: 2 }],
      } as any);
      expect(fracToDecServiceStub.getFormattedValue).toHaveBeenCalledWith(1, 2);
    });

    it(`should return decimal price if on market level priceType equal 'SP' but on leg level it's 'L'`, () => {
      component['formatOdds']({
        part: [{ priceNum: 1, priceDen: 2, price: [{
            priceType: { code: 'L' }
          }]  }],
        eventEntity: {
          markets: [{ priceTypeCodes: 'SP,' }]
        }
      } as any);
      expect(fracToDecServiceStub.getFormattedValue).toHaveBeenCalledWith(1, 2);
    });
  });

  it('#fracToDec should call FracToDecService.getFormattedValue', () => {
    const priceNum: number = 3,
      priceDen: number = 7;

    component['fracToDec'](priceNum, priceDen);
    expect(fracToDecServiceStub.getFormattedValue).toHaveBeenCalledWith(priceNum, priceDen);
  });
  describe('#getHandicapOutcomeName call', () => {
    beforeEach(() => {
      localeStub = {
        getString: jasmine.createSpy().and.callFake(() => 'HL')
      } as any;
      component = new BetLegItemComponent(cashOutServiceStub, raceOutcomeDetailsServiceStub, localeStub, fracToDecServiceStub,
        pubSubService, filtersServiceStub, editMyAccaService, routerStub, routingHelperStub,
        commentsService, eventService, sportsConfigHelperService, cmsService, betTrackingService, casinoMyBetsIntegratedService, handleVarReasoningUpdatesService, deviceService, watchRulesService, nativeBridge, windowRef, liveStreamService, horseRacingService, sessionStorageService, gtmService);
    })
    it('#getOutcomeName should call #getHandicapOutcomeName', () => {
      component['getHandicapOutcomeName'] = jasmine.createSpy();

      component['getOutcomeName'](leg);
      expect(component['getHandicapOutcomeName']).toHaveBeenCalledWith(leg);
    });

    it('#getHandicapOutcomeName should calculate outcome name with handicap value', () => {
      const part: IBetHistoryPart[] = [
        {
          description: 'description1',
          handicap: 'Handicap1',
          outcome: [{ market: { marketSort: { code: 'MR' } } }]
        },
        {
          description: 'description2',
          handicap: '9',
          outcome: [{ market: { marketSort: { code: 'HL' } } }]
        }
      ] as any;

      leg.part = part;

      const expectResult = ['description1 (Handicap1)', 'description2 (9)'];

      expect(component['getHandicapOutcomeName'](leg)).toEqual(expectResult);
    });

    it('#getHandicapOutcomeName should calculate outcome name with handicap value & over/under goal', () => {
      const part: IBetHistoryPart[] = [
        {
          description: 'description1',
          handicap: 'Handicap1',
          outcome: [{ market: { marketSort: { code: 'HL' } } }]
        }
      ] as any;

      leg.part = part;

      const expectResult = ['description1 (Handicap1)'];

      expect(component['getHandicapOutcomeName'](leg)).toEqual(expectResult);
      const part2: IBetHistoryPart[] = [
        {
          description: 'description1',
          handicap: '0.5',
          outcome: [{ market: { marketSort: { code: 'AH' } } }]
        }
      ] as any;

      leg.part = part2;

      const expectResult2 = ['description1 (+0.5)']; 
      expect(component['getHandicapOutcomeName'](leg)).toEqual(expectResult2);
      const part3: IBetHistoryPart[] = [
        {
          description: 'description1',
          handicap: undefined,
          outcome: [{ market: { marketSort: { code: 'AH' } } }]
        }
      ] as any;

      leg.part = part3;

      const expectResult3 = ['description1']; 
      expect(component['getHandicapOutcomeName'](leg)).toEqual(expectResult3);
    });

    it('#getHandicapOutcomeName should calculate outcome name with handicap -ve & +ve ', () => {
      const part: IBetHistoryPart[] = [
        {
          description: 'description1',
          handicap: '-0.5',
          outcome: [{ market: { marketSort: { code: 'AH' } } }]
        }
      ] as any;
      leg.part = part;
      const expectResult1 = ['description1 (-0.5)'];

      const part0: IBetHistoryPart[] = [
        {
          description: 'description1',
          handicap: -0.5,
          outcome: [{ market: { marketSort: { code: 'AH' } } }]
        }
      ] as any;
      leg.part = part0;
      const expectRes1 = ['description1'];

      expect(component['getHandicapOutcomeName'](leg)).toEqual(expectRes1);

      part[0].handicap = '+1.0';
      leg.part = part;
      const expectResult2 = ['description1 (+1.0)'];
      expect(component['getHandicapOutcomeName'](leg)).toEqual(expectResult2);

      part[0].handicap = '1.0';
      leg.part = part;
      const expectResult3 = ['description1 (+1.0)'];
      expect(component['getHandicapOutcomeName'](leg)).toEqual(expectResult3);

    });

    it('#getHandicapOutcomeName should calculate outcome name with handicap & no outcome ', () => {
      const part: IBetHistoryPart[] = [
        {
          description: 'description1',
          handicap: '0.5',
        }
      ] as any;
      leg.part = part;
      const expectResult = ['description1 (0.5)'];

      expect(component['getHandicapOutcomeName'](leg)).toEqual(['description1 (0.5)']);
      const part1: IBetHistoryPart[] = [
        {
          description: 'description1',
          handicap: '0.5',
        }
      ] as any;
      part1[0].outcome = [{ market: '' }] as any;
      leg.part = part1;
      expect(component['getHandicapOutcomeName'](leg)).toEqual(expectResult);
      const part3: IBetHistoryPart[] = [
        {
          description: 'description1',
          handicap: '0.5',
        }
      ] as any;
      part3[0].outcome = [{ market: { marketSort: '' } }] as any;
      leg.part = part3;
      expect(component['getHandicapOutcomeName'](leg)).toEqual(['description1 (+0.5)']);
      const part2: IBetHistoryPart[] = [
        {
          description: 'description1',
          handicap: '+0.9',
          outcome: [{ market: { marketSort: { code: 'AH' } } }]
        }
      ] as any;
      leg.part = part2;
      expect(component['getHandicapOutcomeName'](leg)).toEqual(['description1 (+0.9)']);
    });
    it('#calcDeductionForGP should Calculate deduction value for GP price type', () => {
      const part: IBetHistoryPart = {
        deduction: [
          {
            priceType: 'L',
            value: '78'
          }
        ],
        price: [
          {
            priceStartingNum: '3',
            priceStartingDen: '41',
            priceNum: 31,
            priceDen: 57
          }
        ]
      } as any;

      expect(component['calcDeductionForGP'](part)).toEqual('78');
      part.deduction[0].priceType='S';
      part.price[0]={};
      expect(component['calcDeductionForGP'](part)).toEqual('78');
    });
  })
  it('#getRuleFourDeduction should Calculate Rule 4 deduction value and return number', () => {

    const part0: IBetHistoryPart[] = [
      {}
    ] as any;

    const part1: IBetHistoryPart[] = [{
      deduction: [
        {
          priceType: 'L',
          value: '78'
        }
      ]
    }] as any;

    const part2: IBetHistoryPart[] = [{
      deduction: [
        {
          priceType: 'L',
          value: '32'
        },
        {
          priceType: 'L',
          value: '78'
        }
      ]
    }] as any;

    const part3: IBetHistoryPart[] = [{
      deduction: [
        {
          priceType: 'L',
          value: '32'
        },
        {
          priceType: 'L',
          value: '78'
        },
        {
          priceType: 'L',
          value: '83'
        }
      ]
    }] as any;

    leg.part = part0;
    expect(component['getRuleFourDeduction'](leg)).toEqual(0);

    leg.part = part1;
    expect(component['getRuleFourDeduction'](leg)).toEqual(78);

    component['calcDeductionForGP'] = jasmine.createSpy().and.returnValue(121);
    leg.part = part2;
    expect(component['getRuleFourDeduction'](leg)).toEqual(121);
    expect(component['calcDeductionForGP']).toHaveBeenCalledWith(part2[0]);

    leg.part = part3;

    expect(component['getRuleFourDeduction'](leg)).toEqual(0);
  });

  it('#getDeadHeatInfo: should return whether deadheat condition exist or not ', () => {
    const part = [{
      deduction: [{
       type: 'deadheat', value: '0.5'
      }],
      outcome: [{ name: 'test',
        event: {name: 'event name'},
        eventCategory: {id: '22'}
      }]
    }] as any;
    leg.part = part; 
    component.estimatedReturns = '1';
    component.bet.eventSource.settled = 'Y';   
    component['getDeadHeatInfo'](leg);
    expect(component['getDeadHeatInfo'](leg)).toEqual(true);
  });
  it('#getDeadHeatInfo#1: should return whether deadheat condition exist or not ', () => {
    const part = [{
      deduction: [{
       type: 'deadheat', value: '0.5'
      }],
      outcome: [{ name: 'test',
        event: {name: 'event name'},
        eventCategory: {id: '22'}
      }]
    }] as any;
    leg.part = part; 
    component.bet.eventSource.settled = 'Y'; 
    component.estimatedReturns = '0';   
    component['getDeadHeatInfo'](leg);
    expect(component['getDeadHeatInfo'](leg)).toEqual(false);
  });
  it('#getDeadHeatInfo#2: should return whether deadheat condition exist or not ', () => {
    const part = [{
      deduction: [{
       type: 'deadheat', value: '0.5'
      }],
      outcome: [{ name: 'test',
        event: {name: 'event name'},
        eventCategory: {id: '22'}
      }]
    }] as any;
    leg.part = part;   
    component['getDeadHeatInfo'](leg);
    expect(component['getDeadHeatInfo'](leg)).toEqual(true);
  });
  it('#getDeadHeatInfo#3: should return whether deadheat condition exist or not ', () => {
    
    const part = [{
      deadHeatWinDeductions: "0.1"
    }] as any;
    leg.part = part; 
    component.showDHmessage = true; 
    leg = {...leg, eventEntity:{name: 'Test', categoryId: "16", markets:[{outcomes:[{name:"Test-outcome"}]}]}} ;
    component['getDeadHeatInfo'](leg);
    expect(component['getDeadHeatInfo'](leg)).toEqual(true);
  });
  it('#getDeadHeatInfo#4: should return whether deadheat condition exist or not ', () => {
    const part = [{
      deadHeatEachWayDeductions: "0.1"
    }] as any;
    leg.part = part; 
    leg = {...leg, eventEntity:{name: 'Test', categoryId: "16", markets:[{outcomes:[{name:"Test-outcome"}]}]}} ;
    component.showDHmessage = true;  
    component['getDeadHeatInfo'](leg);
    expect(component['getDeadHeatInfo'](leg)).toEqual(true);
  });
  it('#isDeadHeatApplicable#1: should return whether deadheat condition exist or not ', () => {
    component.bet.eventSource.totalStatus = 'won';
    component.bet.eventSource.leg = [{}, {}] as any;
    component.leg = {isBetSettled: true} as any;    
    component['isDeadHeatApplicable'](component.leg);
    expect(component['isDeadHeatApplicable'](component.leg)).toEqual(true);
  });
  it('#isDeadHeatApplicable#2: should return whether deadheat condition exist or not ', () => {
    component.bet.eventSource.totalStatus = 'cashed out';
    component.bet.eventSource.leg = [{}, {}] as any;
    component.leg = {isBetSettled: true} as any;    
    component['isDeadHeatApplicable'](component.leg);
    expect(component['isDeadHeatApplicable'](component.leg)).toEqual(false);
  });
  it('#isDeadHeatApplicable#3: should return whether deadheat condition exist or not ', () => {
    component.bet.eventSource.totalStatus = 'cashed out';
    component.bet.eventSource.leg = [{}, {}] as any;
    component.leg = {isBetSettled: false} as any;    
    component['isDeadHeatApplicable'](component.leg);
    expect(component['isDeadHeatApplicable'](component.leg)).toEqual(true);
  });
  it('#isDeadHeatApplicable#4: should return whether deadheat condition exist or not ', () => {
    component.bet.eventSource.totalStatus = 'cashed out';
    component.bet.eventSource.leg = [{}] as any;
    component.leg = {isBetSettled: true} as any;    
    component['isDeadHeatApplicable'](component.leg);
    expect(component['isDeadHeatApplicable'](component.leg)).toEqual(false);
  });
  it('#isDeadHeatApplicable#5: should return whether deadheat condition exist or not ', () => {
    component.bet.eventSource.totalStatus = 'won';
    component.bet.eventSource.leg = [{}] as any;
    component.leg = {isBetSettled: true} as any;    
    component['isDeadHeatApplicable'](component.leg);
    expect(component['isDeadHeatApplicable'](component.leg)).toEqual(true);
  });
  it('#isDeadHeatApplicable#6: should return whether deadheat condition exist or not ', () => {
    component.bet.eventSource.totalStatus = 'won';
    component.bet.eventSource.leg = [{}] as any;
    component.leg = {isBetSettled: false} as any;    
    component['isDeadHeatApplicable'](component.leg);
    expect(component['isDeadHeatApplicable'](component.leg)).toEqual(false);
  });
  it('#isDeadHeatApplicable#7: should return whether deadheat condition exist or not ', () => {
    component.bet.eventSource.totalStatus = 'cashed out';
    component.bet.eventSource.leg = [{}, {}] as any;
    component.leg = {isBetSettled: true} as any;  
    component.editAccaHistory = true  
    component['isDeadHeatApplicable'](component.leg);
    expect(component['isDeadHeatApplicable'](component.leg)).toEqual(true);
  });

  it('#isDeadHeatApplicable#8: should return whether deadheat condition exist or not ', () => {
    component.bet.eventSource.totalStatus = 'cashed out';
    component.bet.eventSource.leg = [{}, {}] as any;
    component.leg = {removedLeg: true} as any;  
    component.editAccaHistory = true;  
    component['isDeadHeatApplicable'](component.leg);
    expect(component['isDeadHeatApplicable'](component.leg)).toEqual(false);
  });

  it('#prepareGAData: GA for dead heat condition load and click #1', () => {
    const part = [{
      outcome: [{ name: 'outcome test',
        event: {name: 'event name'},
        eventCategory: {id: '22'}
      }]
    }] as any;
    leg.part = part; 
    component.deadHeatURL = 'DEAD_HEAT_URL';
    spyOn<any>(component, 'storeDeadHeatGAInfo'); 
     const event: any = { stopPropagation: jasmine.createSpy() };    
    component['prepareGAData'](true, leg, event);
    expect(component['storeDeadHeatGAInfo']).toHaveBeenCalledWith( 
        {eventTracking: 'Event.Tracking', 
        positionEvent: 'event name - outcome test', 
        sportID: '22', 
        ActionEvent: 'click',
        EventDetails: 'more info link',
        URLClicked: 'DEAD_HEAT_URL'});
  });
  it('#prepareGAData: GA for dead heat condition load and click #2', () => {
    const part = [{
      outcome: [{ name: 'outcome test',
        event: {name: 'event name'},
        eventCategory: {id: '22'}
      }]
    }] as any;
    leg.part = part; 
    spyOn<any>(component, 'storeDeadHeatGAInfo');   
    component['prepareGAData'](false, leg);
    expect(component['storeDeadHeatGAInfo']).toHaveBeenCalledWith( 
    {eventTracking: 'contentView', 
        positionEvent: 'event name - outcome test', 
        sportID: '22', 
        ActionEvent: 'load',
        EventDetails: 'dead heat info message',
        URLClicked: 'not applicable'});
  });

  describe('getWinLosIndicator', () => {
    it('should calculate win indicator', () => {
      const eventEntity: ISportEvent = {
        comments: {
          teams: {
            away: {
              name: 'Win',
              score: '0'
            },
            home: {
              name: 'Lose',
              score: 0
            }
          }
        }
      } as any;

      const part: IBetHistoryPart[] = [
        {
          description: 'Draw'
        }
      ] as any;

      leg.eventEntity = eventEntity;
      leg.part = part;

      expect(component['getWinLosIndicator'](leg)).toEqual('winning');

      leg.eventEntity.comments.teams.away.score = 2;
      expect(component['getWinLosIndicator'](leg)).toEqual('losing');

      leg.part[0].description = 'Win';
      expect(component['getWinLosIndicator'](leg)).toEqual('winning');

      leg.eventEntity.comments.teams.away.score = '0';
      expect(component['getWinLosIndicator'](leg)).toEqual('losing');
    });

    it('should not return any indicator if score of against team is not defined', () => {
      const eventEntity: ISportEvent = {
        comments: {
          teams: {
            away: {
              name: 'Win',
              score: 1
            },
            home: {
              name: 'Lose',
              score: null
            }
          }
        }
      } as any;

      const part: IBetHistoryPart[] = [
        {
          description: 'Win'
        }
      ] as any;

      leg.eventEntity = eventEntity;
      leg.part = part;

      expect(component['getWinLosIndicator'](leg)).toBeFalsy();

      leg.eventEntity.comments.teams.away.score = '';
      leg.eventEntity.comments.teams.home.score = 0;

      expect(component['getWinLosIndicator'](leg)).toBeFalsy();
    });
  });

  it('#parseEventMarketDescription should get market description', () => {
    const part0: IBetHistoryPart[] = [
      {
        eventMarketDesc: 'Build Your Bet test1'
      },
      {
        eventMarketDesc: 'Build Your Bet test2',
      }
    ] as any;

    component.leg = leg;
    component.leg.part = part0;
    expect(component['parseEventMarketDescription']()).toEqual('Build Your Bet');

    const part1: IBetHistoryPart[] = [
      {
        eventMarketDesc: 'Build Your Bet test1'
      }
    ] as any;

    const part2: IBetHistoryPart[] = [
      {
        eventMarketDesc: '#YourCall test1'
      }
    ] as any;

    const part3: IBetHistoryPart[] = [] as any;

    cashOutServiceStub.getEachWayTerms.and.returnValue('Build Your Bet getEachWayTerms');
    localeStub.getString.and.returnValue('Bet Builder');
    component.leg.part = part1;
    component.legType = 'TestLegType';

    expect(component['parseEventMarketDescription']()).toEqual('BET BUILDER getEachWayTerms');
    expect(cashOutServiceStub.getEachWayTerms).toHaveBeenCalledWith(part1[0], 'TestLegType');

    component.leg.part = part1;
    component.legType = 'TestLegType';

    expect(component['parseEventMarketDescription']()).toEqual('BET BUILDER getEachWayTerms');
    expect(cashOutServiceStub.getEachWayTerms).toHaveBeenCalledWith(part1[0], 'TestLegType');

    component.leg.part = part2;
    component.legType = 'TestLegType';

    expect(component['parseEventMarketDescription']()).toEqual('Build Your Bet getEachWayTerms');
    expect(cashOutServiceStub.getEachWayTerms).toHaveBeenCalledWith(part2[0], 'TestLegType');

    component.leg.part = part3;
    component.legType = 'TestLegType';

    expect(component['parseEventMarketDescription']()).toEqual('Build Your Bet getEachWayTerms');
    expect(cashOutServiceStub.getEachWayTerms).toHaveBeenCalledWith(part3[0], 'TestLegType');
  });

  it('#parseEventMarketDescription should return 5-A-Side', () => {
    localeStub.getString = jasmine.createSpy('getString').and.returnValue('5-A-Side');
    component.bet.eventSource.source = 'f';

    const result = component['parseEventMarketDescription']();

    expect(result).toEqual('5-A-Side');
  });

  it('should check if isLegSuspended', () => {
    component.isLegSuspended({} as any);
    expect(editMyAccaService.isLegSuspended).toHaveBeenCalled();
  });

  describe('getRemovingState', () => {
    it('should return true when leg is in removing state and bet not suspended', () => {
      component.leg = {
        removing: true,
        status: 'open'
      } as any;
      expect(component.getRemovingState).toBeTruthy();
    });
    it('should return false when leg is in removing state and bet is suspended', () => {
      component.leg = {
        removing: true,
        status: 'suspended'
      } as any;
      expect(component.getRemovingState).toBeFalsy();
    });
    it('should return false when leg is in not in removing state', () => {
      component.leg = {
        removing: false,
        status: 'open'
      } as any;
      expect(component.getRemovingState).toBeFalsy();
    });
  });

  describe('showRemovedLabel', () => {
    it('should showRemovedLabel', () => {
      component.leg = { removing: false, removedLeg: false } as any;
      component.isRemovingState = false;
      expect(component.getShowRemovedLabelValue).toBeFalsy();
    });

    it('should showRemovedLabel(removing)', () => {
      component.leg = { removing: true } as any;
      component.isRemovingState = true;
      expect(component.getShowRemovedLabelValue).toBeTruthy();
    });

    it('should showRemovedLabel(removed)', () => {
      component.leg = { removedLeg: true } as any;
      component.isRemovingState = false;
      expect(component.getShowRemovedLabelValue).toBeTruthy();
    });

    it('should showRemovedLabel(removed resultedBeforeRemoval)', () => {
      component.leg = { removedLeg: true, resultedBeforeRemoval: true } as any;
      component.isRemovingState = false;
      expect(component.getShowRemovedLabelValue).toBeFalsy();
    });
  });

  describe('BMA-40873. Live Score Updates', () => {
    beforeEach(() => {
      component['filtersService']['isGreyhoundsEvent'] = jasmine.createSpy().and.returnValue(false);
      spyOn<any>(component, 'formatOdds');
      spyOn<any>(component, 'getOutcomeName').and.returnValue([]);
      spyOn<any>(component, 'parseEventMarketDescription');
      spyOn<any>(component, 'getRuleFourDeduction');
    });

    it('should subscribe on live score updates', () => {
      component['pubSubService'].subscribe = jasmine.createSpy();
      component.leg = {
        ...leg,
        eventEntity: {
          id: 555,
          categoryCode: 'football',
          comments: {},
          markets: []
        }
      } as any;
      component.leg.part[0].outcome =[ {
        flags: ['2UP'],
        result:{
          value:"W",
          confirmed:"Y"
        }
      }] as any;
      component.ngOnInit();

      expect(component['pubSubService'].subscribe).toHaveBeenCalledTimes(7);
    });

    describe('CASHOUT_LIVE_SCORE_EVENT_UPDATE subscription', () => {
      let update;

      beforeEach(() => {
        update = {
          id: 555,
          payload: {
            scores: {}
          }
        } as any;

        component.leg = {
          ...leg,
          eventEntity: {
            id: 555,
            comments: {},
            markets: []
          }
        } as any;
        component.leg.part[0].outcome = [{
          flags: ['2UP'],
          result: {
            value: "W",
            confirmed: "Y"
          }
        }] as any;

        component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
          if (ch === pubSubService.API.CASHOUT_LIVE_SCORE_EVENT_UPDATE) {
            fn(update);
          }
        });
      });

      it('should update scores', () => {
        component.ngOnInit();

        expect(commentsService.sportUpdateExtend).toHaveBeenCalledWith(component.leg.eventEntity.comments, update.payload.scores);
      });

      it('should not update scores if not the same event', () => {
        update.id = 1000;
        component.ngOnInit();

        expect(commentsService.sportUpdateExtend).not.toHaveBeenCalled();
      });

      it('should not update scores if no update data', () => {
        update = null;
        component.ngOnInit();

        expect(commentsService.sportUpdateExtend).not.toHaveBeenCalled();
      });

      it('should not update scores if no payload for update', () => {
        update.payload = null;
        component.ngOnInit();

        expect(commentsService.sportUpdateExtend).not.toHaveBeenCalled();
      });

      it('should not update scores if no scores for update', () => {
        update.payload.scores = null;
        component.ngOnInit();

        expect(commentsService.sportUpdateExtend).not.toHaveBeenCalled();
      });

      it('should not update scores if event has for scores', () => {
        component.leg.eventEntity.comments = null;
        component.ngOnInit();

        expect(commentsService.sportUpdateExtend).not.toHaveBeenCalled();
      });
    });

    describe('CASHOUT_LIVE_SCORE_UPDATE subscription', () => {
      let update;

      beforeEach(() => {
        update = {
          id: 555,
          payload: {
            scores: {}
          }
        } as any;

        component.leg = {
          ...leg,
          legSort: '',
          eventEntity: {
            id: 555,
            categoryCode: 'football',
            comments: {},
            markets: []
          }
        } as any;
        component.leg.part[0].outcome = [{
          flags: ['2UP'],
          result: {
            value: "W",
            confirmed: "Y"
          }
        }] as any;
        component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
          if (ch === pubSubService.API.CASHOUT_LIVE_SCORE_UPDATE) {
            fn(update);
          }
        });
      });

      it('should update scores', () => {
        component.ngOnInit();

        expect(footballUpdateExtendSpy).toHaveBeenCalledWith(component.leg.eventEntity.comments, update.payload);
      });

      it('should not update scores if not the same event', () => {
        update.id = 1000;
        component.ngOnInit();

        expect(footballUpdateExtendSpy).not.toHaveBeenCalled();
      });

      it('should not update scores if no update data', () => {
        update = null;
        component.ngOnInit();

        expect(footballUpdateExtendSpy).not.toHaveBeenCalled();
      });

      it('should not update scores if no payload data', () => {
        update.payload = null;
        component.ngOnInit();

        expect(footballUpdateExtendSpy).not.toHaveBeenCalled();
      });

      it('should not update scores if event has for scores', () => {
        component.leg.eventEntity.comments = null;
        component.ngOnInit();

        expect(footballUpdateExtendSpy).not.toHaveBeenCalled();
      });

      it('should not update scores if event has for scores', () => {
        component.leg.eventEntity.comments = null;
        component.ngOnInit();

        expect(footballUpdateExtendSpy).not.toHaveBeenCalled();
      });

      it('should not update scores if unknown sport to update', () => {
        component['commentsService']['footballUpdateExtend'] = undefined;
        component.ngOnInit();

        expect(footballUpdateExtendSpy).not.toHaveBeenCalled();
      });
    });
    describe('EVENT_STARTED subscription', () => {
      let update;
      beforeEach(() => {
        update = {
          id: '555',
          payload: {
            scores: {}
          }
        } as any;
        component.leg = {
          ...leg,
          legSort: '',
          eventEntity: {
            id: 555,
            categoryCode: 'football',
            comments: {},
            markets: [],
            isStarted: true,
            eventIsLive: true,
            isResulted: false
          }
        } as any;
        component.leg.part[0].outcome = [{
          flags: ['2UP'],
          result: {
            value: "W",
            confirmed: "Y"
          }
        }] as any;
        component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
          if (ch === pubSubService.API.EVENT_STARTED) {
            fn(update.id);
          }
        });
      });
      it('should call subscribeMatchCommentary', () => {
        spyOn(component as any, 'subscribeMatchCommentary');
        const eventEntity = component.leg.eventEntity;
        component.ngOnInit();
        expect(eventEntity.isStarted).toBeTrue();
        expect(eventEntity.eventIsLive).toBeTrue();
        expect(eventEntity.isResulted).toBeFalse();
        expect(component['subscribeMatchCommentary']).toHaveBeenCalledWith(eventEntity, component.leg);
        expect(component['subscribeMatchCommentary']).toHaveBeenCalledTimes(2);
      });
      
      it('should not update scores if not the same event', () => {
        spyOn(component as any, 'subscribeMatchCommentary');
        const eventEntity = component.leg.eventEntity;
        update = { id: '10', payload: {   scores: {} }} as any;
        component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
          if (ch === pubSubService.API.EVENT_STARTED) {
            fn(update.id);
          }
        }); 
        component.ngOnInit();
        expect(component['subscribeMatchCommentary']).toHaveBeenCalledOnceWith(eventEntity, component.leg);
      });
    });
    describe('EVENT_FINSHED subscription', () => {
      let update;
      beforeEach(() => {
        update = '555' as any;
              component.leg = {
          ...leg,
          legSort: '',
          eventEntity: {
            id: 555,
            categoryCode: 'football',
            comments: {},
            markets: []
          }
        } as any;
        component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
          if (ch === pubSubService.API.EVENT_FINSHED) {
            fn(update.id);
          }
        });
        component.leg.part[0].outcome[0].event.isOff ='Y';
        component.leg.part[0].outcome[0].event.flags ='AVD';

      });
     
      it('should not update scores if not the same event', () => {
        spyOn(component as any, 'subscribeMatchCommentary');
        spyOn(component as any, 'getTwoUpSuccessFlag');
        const eventEntity = component.leg.eventEntity;
        component.leg.part[0].outcome [0]= {
          flags: ['2UP'],
            result: {
              value: "N",
              confirmed: "-"
            }
          } as any;
        component.leg.part[0].outcome[0].event = {
          "id": "240790191",
          "name": "17:55 Chepstow",
          "startTime": "2023-07-10 17:55:00",
          "raceNumber": "",
          "venue": "",
          "isOff": "N",
      } as any;
      
        update ='240790191' as any;
        component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
          if (ch === pubSubService.API.EVENT_FINSHED) {
            fn(update);
          }
        }); 
        component.ngOnInit();
        component.leg.part[0].outcome[0].event.isOff ='Y';
        component.leg.part[0].outcome[0].event.flags ='AVD';
        expect(component.getTwoUpSuccessFlag).toHaveBeenCalled();  
      });
    });

    describe('EVENT_FINSHED subscription', () => {
      let update;
      beforeEach(() => {
        update = '555' as any;
              component.leg = {
          ...leg,
          legSort: '',
          eventEntity: {
            id: 555,
            categoryCode: 'football',
            comments: {},
            markets: []
          }
        } as any;
        component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
          if (ch === pubSubService.API.EVENT_FINSHED) {
            fn(update.id);
          }
        });
        component.leg.part[0].outcome[0].event.isOff ='Y';
        component.leg.part[0].outcome[0].event.flags ='AVD';

      });
     
      it('should not update scores if not the same event', () => {
        spyOn(component as any, 'subscribeMatchCommentary');
        spyOn(component as any, 'getTwoUpSuccessFlag');
        const eventEntity = component.leg.eventEntity;
        component.leg.part[0].outcome [0]= {
          flags: ['2UP'],
            result: {
              value: "N",
              confirmed: "-"
            }
          } as any;
        component.leg.part[0].outcome[0].event = {
          "id": "240790191",
          "name": "17:55 Chepstow",
          "startTime": "2023-07-10 17:55:00",
          "raceNumber": "",
          "venue": "",
          "isOff": "N",
      } as any;
      
        update ='240790191' as any;
        component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
          if (ch === pubSubService.API.EVENT_FINSHED) {
            fn(update);
          }
        }); 
        component.ngOnInit();
        component.leg.part[0].outcome[0].event.isOff ='Y';
        component.leg.part[0].outcome[0].event.flags ='AVD';
        expect(component.getTwoUpSuccessFlag).toHaveBeenCalled();  
      });
    });
    describe('Two up update subscription', () => {
      let update;
      beforeEach(() => {
        update={selectionId:555,twoUpSettled:false} as any;
              component.leg = {
          ...leg,
          legSort: '',
          eventEntity: {
            id: 555,
            categoryCode: 'football',
            comments: {},
            markets: []
          }
        } as any;
        component.leg.part[0].outcome [0]= {
          id:555,
          flags: ['2UP'],
            result: {
              value: "N",
              confirmed: "-"
            }
          } as any;
        component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
          if (ch === pubSubService.API.TWO_UP_UPDATE) {
            fn(update.selectionId);
          }
         });
         spyOn(component as any, 'getTwoUpSuccessFlag');
      });
     
      it('gery two up signpost should display ', () => {
        component.leg.part[0].outcome [0]= {
          id:555,
          flags: ['2UP'],
            result: {
              value: "V",
              confirmed: "Y"
            }
          } as any;
        component.leg.part[0].outcome[0].event = {
          "id": "240790191",
          "name": "17:55 Chepstow",
          "startTime": "2023-07-10 17:55:00",
          "raceNumber": "",
          "venue": "",
          "isOff": "N",
      } as any;
      
      update={selectionId:555,twoUpSettled:false} as any;
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
          if (ch === pubSubService.API.TWO_UP_UPDATE) {
            fn(update);
          }
        }); 
        component.ngOnInit();
        expect(component.getTwoUpSuccessFlag).toHaveBeenCalled();  
      });

      it('green two up signpost should display ', () => {
        component.leg.part[0].outcome [0]= {
          id:555,
          flags: ['2UP'],
            result: {
              value: "V",
              confirmed: "Y"
            }
          } as any;
        component.leg.part[0].outcome[0].event = {
          "id": "240790191",
          "name": "17:55 Chepstow",
          "startTime": "2023-07-10 17:55:00",
          "raceNumber": "",
          "venue": "",
          "isOff": "N",
      } as any;
      
      update={selectionId:555,twoUpSettled:true} as any;
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
          if (ch === pubSubService.API.TWO_UP_UPDATE) {
            fn(update);
          }
        }); 
        component.ngOnInit();
        expect(component.getTwoUpSuccessFlag).toHaveBeenCalled();  
      });
    });
     });

  describe('formatStartingOdds', () => {
    it('should return empty string if no data', () => {
      expect(component['formatStartingOdds']({} as IBetHistoryLeg)).toBe('');
    });

    it('should return number if price is present and market is not SP', () => {
      const leg1 = {
        eventEntity: {
          markets: [{
            priceTypeCodes: 'not SP'
          }]
        },
        part: [{
          price: [{
            priceStartingNum: 1,
            priceStartingDen: 2
          }]
        }]
      };

      component['fracToDec'] = jasmine.createSpy('fracToDec').and.callFake(
        (num: number, den: number) =>  (1 + (num / den)).toFixed(2)
      );

      expect(component['formatStartingOdds'](leg1 as any)).toBe('1.50');
    });

    it('should return empty string in case if SP event despite price info absence', () => {
      const leg1 = {
        eventEntity: {
          markets: [{
            priceTypeCodes: 'SP'
          }]
        }
      };

      expect(component['formatStartingOdds'](leg1 as any)).toBe('');
    });
  });

  describe('confirmationDialogClick', () => {
    it('confirmationDialogClick, with event data', () => {
      const event = {
        output: 'userAction',
        value: {
          checkboxValue: true, 
          btnClicked: 'no thanks'
        }
      };
      component.confirmationDialogClick(event);
      expect(component['casinoMyBetsIntegratedService'].confirmationPopUpClick).toHaveBeenCalled();  
    });
  });
  describe('#subscribeMatchCommentary',()=>{
    it('should subscribe to handlevarresoning updates if sport is football and liveEvent ',()=>{
      component.leg = {
        isBetSettled:false,
        ...leg,
        legSort: '',
        eventEntity: { id: 32, name: 'event name',categoryCode:'FOOTBALL',isStarted: true, eventIsLive: true,isResulted:false}
      } as any;
       const eventEntity = { id: 32, name: 'event name',categoryCode:'FOOTBALL',isStarted: true, eventIsLive: true,isResulted:false} as ISportEvent;
       component['subscribeMatchCommentary'](eventEntity,component.leg);
       expect(component.leg).toBeDefined();
       expect(handleVarReasoningUpdatesService.subscribeForMatchCmtryUpdates).toHaveBeenCalledWith('32');
    });
    it('should subscribe to handlevarresoning updates if sport is not football and liveEvent ',()=>{
      component.leg = {
        isBetSettled:true,
        ...leg,
        legSort: '',
        eventEntity: { id: 32, name: 'event name',categoryCode:'cricket',isStarted: true, eventIsLive: true,isResulted:false}
      } as any;
      const eventEntity = { id: 32, name: 'event name',categoryCode:'FOOTBALL',isStarted: true, eventIsLive: true,isResulted:false} as ISportEvent;
      component['subscribeMatchCommentary'](eventEntity,component.leg);
      expect(handleVarReasoningUpdatesService.subscribeForMatchCmtryUpdates).not.toHaveBeenCalledWith('32');
    });
    it('should not subscribe to handlevarresoning updates if sport is not football and not liveEvent ',()=>{
      component.leg = {
        isBetSettled:true,
        ...leg,
        legSort: '',
        eventEntity: { id: 32, name: 'event name',categoryCode:'cricket',isStarted: false, eventIsLive: false,isResulted:false}
      } as any;
      const eventEntity = { id: 32, name: 'event name',categoryCode:'FOOTBALL',isStarted: true, eventIsLive: true,isResulted:false} as ISportEvent;
      component['subscribeMatchCommentary'](eventEntity,component.leg);
      expect(handleVarReasoningUpdatesService.subscribeForMatchCmtryUpdates).not.toHaveBeenCalledWith('32');
    });
    it('should not subscribe to handlevarresoning updates if sport is football and not liveEvent ',()=>{
      component.leg = {
        isBetSettled:true,
        ...leg,
        legSort: '',
        eventEntity: { id: 32, name: 'event name',categoryCode:'cricket',isStarted: false, eventIsLive: false,isResulted:false}
      } as any;
      const eventEntity = { id: 32, name: 'event name',categoryCode:'FOOTBALL',isStarted: true, eventIsLive: true,isResulted:false} as ISportEvent;
      component['subscribeMatchCommentary'](eventEntity,component.leg);
      expect(handleVarReasoningUpdatesService.subscribeForMatchCmtryUpdates).not.toHaveBeenCalledWith('32');
    });
  });

  describe('#appendDrillDownTagNames', () => {
    it('should return true for appendDrillDownTagName', () => {
      localeStub.getString.and.returnValue('Match Result');
      const returnValue = component.appendDrillDownTagNames({categoryId: '16'}, {eventMarketDesc: 'Match Result'});
      expect(returnValue).toEqual('Match Result,');
    });

    it('should return empty string  for appendDrillDownTagName', () => {
      localeStub.getString.and.returnValue('Match Result');
      const returnValue = component.appendDrillDownTagNames({categoryId: '21'}, {eventMarketDesc: 'Match Result'});
      expect(returnValue).toEqual('');
    });

    it('should return empty string  for appendDrillDownTagName', () => {
      localeStub.getString.and.returnValue('Both Teams to Score');
      const returnValue = component.appendDrillDownTagNames({categoryId: '16'}, {eventMarketDesc: 'Match Result'});
      expect(returnValue).toEqual('');
    });
  });
  describe('Check for antepost or racing specials', () => {
    it('isNotAntepostOrSpecials', () => {
      spyOn(component, 'isAntepostMarket').and.returnValue(false);
      expect(component.isNotAntepostOrSpecials()).toBeTruthy();
    });
    it('isAntepostMarket', () => {
      component.leg.eventEntity = {
        markets: [{
          isAntepost: 'true'
        }]
      } as any;
      expect(component.isAntepostMarket()).toBeTruthy();
  
      component.leg.eventEntity.markets[0].isAntepost = null;
      expect(component.isAntepostMarket()).toBeFalsy();

      component.leg.eventEntity.markets[0] = null;
      expect(component.isAntepostMarket()).toBeFalsy();

      component.leg.eventEntity = null;
      expect(component.isAntepostMarket()).toBeFalsy();
    });
  })
  describe('#isRunnerNumber', () => {
    it('should return true', () => {
      component.leg.eventEntity = {
        categoryCode: 'HORSE_RACING',
        isFinished: false,
        isBetSettled: false,
        racingFormEvent: {
          horses: [{horseName: 'xyz', nonRunner: 'false'}]
        },
        markets: [{outcomes: [{outcomeMeaningMinorCode: 0, name: 'xyz'}]}]
      } as any;
      component.isNumberNeeded = jasmine.createSpy('isNumberNeeded').and.returnValue(true);
      spyOn(component as any, 'isFavourite').and.callThrough();
      spyOn(component as any, 'isNonRunner').and.callThrough();
      component.isRunnerNumber(component.leg.eventEntity.markets[0].outcomes[0]);
      expect(component.isRunnerNumber(component.leg.eventEntity.markets[0].outcomes[0])).toBe(true);
    });
    it('isFavourite - true with outcome name as null', () => {
      const outcome = {outcomeMeaningMinorCode: 0} as any;
      expect(component.isFavourite(outcome)).toBe(false);
    });
    it('isNonRunner - false when racingFormEvent is null', () => {
      const eventEntity = {
        categoryCode: 'HORSE_RACING',
        markets: [{outcomes: [{outcomeMeaningMinorCode: 0, name: 'xyz'}]}]
      } as any;
      const outcome = {outcomeMeaningMinorCode: 0, name: 'xyz'} as any;
      expect(component.isNonRunner(eventEntity, outcome)).toBe(false);
    });
  });
  describe('#getRunnerNumberAndStallNumber', () => {
    it('should return runner number', () => {
      component.isNumberNeeded = jasmine.createSpy('isNumberNeeded').and.returnValue(true);
      leg.eventEntity = {
        markets: [
          {
            id: '1',
            outcomes: [{id: '51', name: 'xyz', runnerNumber: '1', racingFormOutcome: {draw: '2'}}]
          }
        ]
      } as any;
      component.leg = {
        eventEntity: {}
      } as any;
      expect(component.getRunnerNumberAndStallNumber(leg, 'xyz')).toEqual({runnerNumber: '1', stallNumber: '2'});
      leg.eventEntity.markets[0].outcomes[0].racingFormOutcome = null;
      expect(component.getRunnerNumberAndStallNumber(leg, 'xyz')).toEqual({runnerNumber: '1', stallNumber: undefined});
    });
    it('should return runner number and stall number as null - leg as null', () => {
      const betLeg = null;
      expect(component.getRunnerNumberAndStallNumber(betLeg, 'xyz')).toBe(null);
    });
    it('should return runner number and stall number as null - part as null', () => {
      const betLeg = {part: null} as any;
      expect(component.getRunnerNumberAndStallNumber(betLeg, 'xyz')).toBe(null);
    });
    it('should return runner number and stall number as null - legPart as null', () => {
      const betLeg = {part: [null]} as any;
      expect(component.getRunnerNumberAndStallNumber(betLeg, 'xyz')).toBe(null);
    });
    it('should return runner number and stall number as null - eventEntity as null', () => {
      const betLeg = {part: [{outcomeId: '1'}], eventEntity: null} as any;
      expect(component.getRunnerNumberAndStallNumber(betLeg, 'xyz')).toBe(null);
    });
    it('should return runner number and stall number as null - markets as null', () => {
      const betLeg = {part: [{outcome: '1'}], eventEntity: {markets: null}} as any;
      expect(component.getRunnerNumberAndStallNumber(betLeg, 'xyz')).toBe(null);
    });
    it('should return runner number and stall number as null - market as null', () => {
      const betLeg = {part: [{outcome: '1', marketId: '1'}], eventEntity: {markets: [null]}} as any;
      expect(component.getRunnerNumberAndStallNumber(betLeg, 'xyz')).toBe(null);
    });
    it('should return runner number and stall number as null - outcomes as null', () => {
      const betLeg = {part: [{outcome: '1', marketId: '1'}], eventEntity: {markets: [{id: '1', outcomes: null}]}} as any;
      expect(component.getRunnerNumberAndStallNumber(betLeg, 'xyz')).toBe(null);
    });
  });

  describe('#is2UpMarketSuspended', () => {
    it('should return true when event is Active and 2up market is suspended', () => {
      leg.eventEntity.markets = [
        { name: '2Up - Instant Win', id: '1', marketStatusCode: 'S' }
      ];
      leg.eventEntity.eventStatusCode = 'A';
      leg.part[0].eventMarketDesc = '2Up - Instant Win';
      expect(component.is2upMarketSuspended(leg)).toBeTrue();
      expect(component.statusName).toBe('');
    });
    it('should return false when both event and 2up market is Active', () => {
      leg.eventEntity.markets = [
        { name: '2Up - Instant Win', id: '1', marketStatusCode: 'A' }
      ];
      leg.eventEntity.eventStatusCode = 'A';
      leg.part[0].eventMarketDesc = '2Up - Instant Win';
      component.leg = leg;
      expect(component.is2upMarketSuspended(leg)).toBeFalse();
      expect(component.statusName).toBe('won');
    });
    it('#when is2upMarketSuspended is called from ngOnChanges should return true', () => {
      component.showRemovedLabel = false;
      component.statusName = 'won';
      leg.eventEntity.markets = [
        { name: '2Up - Instant Win', id: '1', marketStatusCode: 'S' }
      ];
      leg.eventEntity.eventStatusCode = 'A';
      leg.part[0].eventMarketDesc = '2Up - Instant Win';
      component.ngOnChanges({
        leg:  { currentValue: leg } as any
      });
      expect(component.statusName).toBe('');
    });
    it('getClasses should be "won arrowed-item" and is2upMarketSuspended should return true', () => {
      component.bet.eventSource.settled = 'N';
      component.sportPath = 'Football';
      leg.eventEntity.markets = [
        { name: '2Up - Instant Win', id: '1', marketStatusCode: 'S',priceTypeCodes:'S' }
      ];
      leg.eventEntity.eventStatusCode = 'A';
      leg.part[0].eventMarketDesc = '2Up - Instant Win';
      expect(component.getClasses(leg as any)).toContain('open');
    });
    it('getClasses should be "won arrowed-item" and is2upMarketSuspended should return true', () => {
      leg.eventEntity.markets = [
        { name: '2Up - Instant Win', id: '1', marketStatusCode: 'S',priceTypeCodes: 'S' }
      ];
      leg.eventEntity.eventStatusCode = 'A';
      leg.part[0].eventMarketDesc = '2Up - Instant Win';
      component.leg = leg;
      component.leg.part[0].outcome = [{
        flags: ['2UP'],
        result: {
          value: "W",
          confirmed: "Y"
        }
      }] as any;
      component.ngOnInit();
      expect(component.statusName).toBe('');
    });

    it('getTwoUpSuccessFlag', () => {
      component.leg = {
        ...leg,
        eventEntity: {
          id: 555,
          categoryCode: 'football',
          comments: {},
          markets: []
        }
      } as any;
      component.winLosIndicator="winning";
      component.getShowRemovedLabelValue = true;
      component.getRemovingState = true;
      component.getStatusName = 'won';
      leg.part[0].outcome =[ {
        flags: ['2UP'],
        result:{
          value:"W",
          confirmed:"Y"
        }
      }] as any;
      component.leg = leg;
      component.isTwoUpSettlmentSignpostDisplay = true;
      expect(component.getTwoUpSuccessFlag(leg)).toBe(1);
      leg.part[0].outcome[0] = {
        result:{
          value:"W",
          confirmed:"Y"
        }
      } as any;
      component.leg = leg;
      expect(component.getTwoUpSuccessFlag(leg)).toBe(0);
      leg.part[0].outcome[0] = {
        result:{
          value:"W",
          confirmed:"Y"
        }
      } as any;
      component.leg = leg;
      expect(component.getTwoUpSuccessFlag(leg)).toBe(0);
      leg.part[0].outcome[0] = {
        result:{
          value:"L",
          confirmed:"Y"
        }
      } as any;
      component.leg = leg;
      expect(component.getTwoUpSuccessFlag(leg)).toBe(0);

      leg.part[0].outcome[0] = {
        result:{
          value:"V",
          confirmed:"Y"
        }
      } as any;
      component.leg = leg;
      expect(component.getTwoUpSuccessFlag(leg)).toBe(0);
    
      component.leg = leg;
      leg.part[0].outcome[0] = {
        result:{
          value:"-",
          confirmed:"N"
        }
      } as any;
      expect(component.getTwoUpSuccessFlag(leg)).toBe(-1);
      leg.part[0].outcome =[ {
        result:{
          value:"W",
          confirmed:"Y"
        }
      }] as any;
      component.leg = leg;
      expect(component.getTwoUpSuccessFlag(leg)).toBe(0);
      leg.part[0].outcome[0] = {
        result:{
          value:"W",
          confirmed:"Y"
        }
      } as any;      component.leg = leg;
      expect(component.getTwoUpSuccessFlag(leg)).toBe(0);
    });
  })
  
  describe('showWatchAndInsights', () => {
    it('EVFLAG_PVM', () => {
      component['isUKorIRE'] = true;
      component.leg.eventEntity = {
        drilldownTagNames:['EVFLAG_PVM'],
        categoryId: HORSE_RACING_CATEGORY_ID
      } as any;
      component.drillDownTags = ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'];     
      expect(component.showWatchAndInsights()).toBeTruthy();
    });

    it('EVFLAG_PVA', () => {
      component['isUKorIRE'] = true;
      component.leg.eventEntity = {
        drilldownTagNames:['EVFLAG_PVA'],
        categoryId: HORSE_RACING_CATEGORY_ID
      } as any;
      component.drillDownTags = ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'];     
      expect(component.showWatchAndInsights()).toBeTruthy();
    });
  })

  describe('#setGtmData', () => {  
    it('storing GA object', () => {
      component.leg.eventEntity = {
        typeName: 'UK'
      } as any;
      component['tabName'] = 'open bets';
      component.setGtmData('test');
      expect(component['gtmService'].push).toHaveBeenCalled();
    });
  });

  describe('Play stream with GA tracking', () => {
    it('playStream on wrapper with watch & Insights', () => {
      component.leg.part[0].outcome[0].eventType={name:'abc'};
      component['isUKorIRE'] = true;
      component.leg.eventEntity = {
        drilldownTagNames:['EVFLAG_PVA'],
        categoryId: HORSE_RACING_CATEGORY_ID
      } as any;
      component.eventEntity = {
        drilldownTagNames:['EVFLAG_PVA']
      } as any;
      component.leg.is_off = false;
      component.leg.isLiveStreamOpened = false;      
      component.drillDownTags = ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'];         
      const setGtmDataSpy = spyOn(component as any, 'setGtmData');      
      component.playStream({ preventDefault: () => { } } as any);
      expect(setGtmDataSpy).toHaveBeenCalled();
    });
  
    it('playStream on wrapper with watch: is_off', () => {
      component['isUKorIRE'] = true;
      component.leg.eventEntity = {
        drilldownTagNames:['EVFLAG_PVA'],
        categoryId: HORSE_RACING_CATEGORY_ID
      } as any;
      component.eventEntity = {
        drilldownTagNames:['EVFLAG_PVA']
      } as any;
      component.leg.is_off = true;
      component.leg.isLiveStreamOpened = false;      
      component.drillDownTags = ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'];         
      const setGtmDataSpy = spyOn(component as any, 'setGtmData');      
      component.playStream({ preventDefault: () => { } } as any);
      expect(setGtmDataSpy).toHaveBeenCalled();
    });

    it('playStream on wrapper with watch: rawIsOffCode', () => {
      component['isUKorIRE'] = true;
      component.leg.eventEntity = {
        drilldownTagNames:['EVFLAG_PVA'],
        categoryId: HORSE_RACING_CATEGORY_ID,
        rawIsOffCode: 'Y'
      } as any;
      component.eventEntity = {
        drilldownTagNames:['EVFLAG_PVA']
      } as any;
      component.leg.is_off = false;
      component.leg.isLiveStreamOpened = false;      
      component.drillDownTags = ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'];         
      const setGtmDataSpy = spyOn(component as any, 'setGtmData');      
      component.playStream({ preventDefault: () => { } } as any);
      expect(setGtmDataSpy).toHaveBeenCalled();
    });
  });

  it('#Betsharing for sports regular bets with multiples when leg and event entity is false', () => {
    spyOn(component as any,'getRunnerNumberAndStallNumber').and.returnValue({runnerNumber: 'test runner',
      stallNumber: 'test stall'});
    component.isMultiples = true;
    component.eventMarketDescription = 'test desc';
    component.displayBogPrice = true;
    component.startingOddsCaption = '5/3';
    component.leg = null;
    component.event = { categoryId: '1' } as any;
    component.outcomeNames = ['test outcomes'];
    component.settingDataInSession();
  });
  describe('isWatchReplayAvailable', () => {
    it('replayavailable', () => {
      component.leg.isBetSettled=true;           
      component.leg.part[0].outcome[0].event = {
        "id": "240790174",
        "name": "17:55 Chepstow",
        "startTime": "2023-07-10 17:55:00",
        "raceNumber": "",
        "venue": "",
        "isOff": "Y","flags":'AVD',
        "categoryId":21
    },
    component.leg.eventEntity = {
      categoryCode: 'HORSE_RACING'
    } as any;
      expect(component.isWatchReplayAvailable()).toEqual(true);
    });
    it('vod not available', () => {
      component.leg.isBetSettled=true;
      component.leg.part[0].outcome[0].event = {
        "id": "240790174",
        "name": "17:55 Chepstow",
        "startTime": "2023-07-10 17:55:00",
        "raceNumber": "",
        "venue": "",
        "isOff": "N",  "categoryId":21

    },
    component.leg.eventEntity = {
      categoryCode: 'HORSE_RACING'
    } as any;
      expect(component.isWatchReplayAvailable()).toEqual(false);
    });
    it('vod not available', () => {
      component.leg.isBetSettled=false; 
      component.leg.part[0].outcome[0].event = {
        "id": "240790174",
        "name": "17:55 Chepstow",
        "startTime": "2023-07-10 17:55:00",
        "raceNumber": "",
        "venue": "",
        "isOff": "N","flags":'AVD',
        "categoryId":21
    },
      component.leg.eventEntity = {
        categoryCode: 'FOOTBALL',  
      } as any;
      expect(component.isWatchReplayAvailable()).toEqual(false);
    });
    });
    
});
