import { BetLegItemComponent } from '@ladbrokesMobile/betHistory/components/betLegItem/bet-leg-item.component';

describe('LMBetLegItemComponent', () => {
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
  let modulesExtensionsStorageStub;
  let cmsService;
  let betTrackingService;
  let casinoMyBetsIntegratedService;
  let handleVarReasoningUpdatesService;
  let deviceService;
  let watchRulesService;
  let horseRacingService;
  let nativeBridge;
  let windowRef;
  let liveStreamService;
  let gtmService;
  let sessionStorageService;

  beforeEach(() => {
    cashOutServiceStub = {
      getEachWayTerms: jasmine.createSpy().and.returnValue('#YourCall getEachWayTerms')
    };
    betTrackingService= {
      isTrackingEnabled: jasmine.createSpy
    };
    raceOutcomeDetailsServiceStub = {
      getSilkStyleForPage: jasmine.createSpy(),
      isSilkAvailableForOutcome: jasmine.createSpy(),
      isUnnamedFavourite: jasmine.createSpy()
    };
    localeStub = {
      getString: jasmine.createSpy().and.returnValue('Build Your Bet')
    };
    fracToDecServiceStub = {
      getFormattedValue: jasmine.createSpy()
    };
    filtersServiceStub = {
      filterPlayerName: jasmine.createSpy(),
      filterAddScore: jasmine.createSpy()
    };
    editMyAccaService = {
      isLegSuspended: jasmine.createSpy('isLegSuspended'),
      isLegResulted: jasmine.createSpy('isLegResulted')
    };
    pubSubService = {
      subscribe: jasmine.createSpy().and.callFake((a, b, cb) => cb && cb()),
      unsubscribe: jasmine.createSpy(),
      API: {
        UPDATE_EMA_ODDS: 'UPDATE_EMA_ODDS',
        CASHOUT_LIVE_SCORE_EVENT_UPDATE: 'CASHOUT_LIVE_SCORE_EVENT_UPDATE',
        CASHOUT_LIVE_SCORE_UPDATE: 'CASHOUT_LIVE_SCORE_UPDATE'
      }
    };
    routerStub = {};
    routingHelperStub = {};
    modulesExtensionsStorageStub = {
      getList: () => {}
    } as any;
    deviceService = { isWrapper: true,isDesktop:true };

    footballUpdateExtendSpy = jasmine.createSpy();
    commentsService = {
      sportUpdateExtend: jasmine.createSpy(),
      footballUpdateExtend: footballUpdateExtendSpy,
      extendWithScoreType: jasmine.createSpy('extendWithScoreType')
    };
    eventService = {
      isUKorIRE: jasmine.createSpy()
    };

    cmsService = {
    };
    leg = {
      name: 'test name',
      startTime: '1542273861984',
      poolPart: [],
      legSort: '',
      part: [
        {
          outcomeId: '51',
          outcome: {},
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
    } as any;
    gtmService = {
      push: jasmine.createSpy('push')
    };

    sessionStorageService = {
      get: jasmine.createSpy('get')
    }

    component = new BetLegItemComponent(cashOutServiceStub, raceOutcomeDetailsServiceStub, localeStub, fracToDecServiceStub,
      pubSubService, filtersServiceStub, editMyAccaService, routerStub, routingHelperStub,
      modulesExtensionsStorageStub, commentsService, eventService, cmsService, betTrackingService, casinoMyBetsIntegratedService, handleVarReasoningUpdatesService, deviceService, watchRulesService, nativeBridge, windowRef, liveStreamService, horseRacingService, sessionStorageService, gtmService);
    component.bet = {
      eventSource: { totalStatus : 'lost' }
    } as any;
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component.leg = leg;

      spyOn(component as any, 'formatOdds');
      spyOn(component as any, 'getOutcomeName').and.returnValue([]);
      spyOn(component as any, 'parseEventMarketDescription');
      spyOn(component as any, 'getRuleFourDeduction');
    });

    it('should set ExcludedDrilldownTagNames', () => {
      // @ts-ignore
      component.bet.eventSource = {
        betType: 'SGL'
      };

      component.outcomeNames = ['unnamed favourite'];

      expect(component.getExcludedDrilldownTagNames()).toEqual('EVFLAG_MB,MKTFLAG_MB,MKTFLAG_EPR,EVFLAG_EPR');
    });

    it('should set no ExcludedDrilldownTagNames', () => {
      // @ts-ignore
      component.bet.eventSource = {
        betType: 'DBL'
      };

      component.outcomeNames = ['Eddie'];

      expect(component.getExcludedDrilldownTagNames()).toEqual('');
    });
  });
});
