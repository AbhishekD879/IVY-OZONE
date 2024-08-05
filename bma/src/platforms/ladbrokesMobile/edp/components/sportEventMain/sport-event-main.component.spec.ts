import { SportEventMainComponent } from '@ladbrokesMobile/edp/components/sportEventMain/sport-event-main.component';
import { of } from 'rxjs';

describe('LMSportEventMainComponent', () => {
  let component,
    deviceService,
    activatedRoute,
    visEventService,
    visDataHandler,
    pubSubService,
    cmsService,
    gtmService,
    localeService,
    commandService,
    nativeBridgeService,
    eventVideoStreamProviderService,
    coreTools,
    userService,
    windowRef,
    sportEventPageProviderService,
    sportEventMainProviderService,
    renderer,
    timeService,
    changeDetectorRef,
    eventId,
    scoreParserService,
    updateEventService,
    cashOutMapService,
    CashoutWsConnectorService,
    router,
    routingHelperService,
    sportConfig,
    storageService,
    sportsConfigService,
    sportEventHelperService;

  beforeEach(() => {
    eventId = '12345';
    deviceService = {
      getDeviceViewType: jasmine.createSpy('getDeviceViewType').and.returnValue({mobile: false}),
      isTabletOrigin: false
    };
    activatedRoute = {
      snapshot: {
        paramMap: {
          get: jasmine.createSpy('paramMap.get').and.returnValue('football')
        }
      },
      params: of({
        sport: 'football',
        id: eventId
      })
    };
    visEventService = {
      visListener: jasmine.createSpy('visListener'),
      checkPreMatchWidgetAvailability: jasmine.createSpy('checkPreMatchWidgetAvailability').and.returnValue(of({})),
      checkForEventsWithAvailableVisualization: jasmine.createSpy()
    };
    storageService = {
      set: jasmine.createSpy('storageService.set'),
      get: jasmine.createSpy('storageService.get').and.returnValue([{ eventId: 11},{eventId: 22}]),
    };
    visDataHandler = {};
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        STREAM_ERROR_CHANGE: 'STREAM_ERROR_CHANGE',
        HIDE_OPTA_SCOREBOARD: 'HIDE_OPTA_SCOREBOARD',
        SPORT_EDP_CLOSED: 'SPORT_EDP_CLOSED',
        UNSUBSCRIBE_LS_UPDATES_MS: 'UNSUBSCRIBE_LS_UPDATES_MS',
        CASHOUT_CTRL_STATUS: 'CASHOUT_CTRL_STATUS'
      }
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({})),
      getFeatureConfig: jasmine.createSpy('getFeatureConfig').and.returnValue(of({})),
      getToggleStatus: jasmine.createSpy('getToggleStatus').and.returnValue(of({})),
      getEDPMarkets: jasmine.createSpy('getEDPMarkets').and.returnValue(of({})),
      triggerSystemConfigUpdate: jasmine.createSpy('triggerSystemConfigUpdate')
    };
    gtmService = {};
    localeService = {
      getString: jasmine.createSpy('getString').and.callFake(key => key)
    };
    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve({})),
      API: {
        OPEN_CASHOUT_STREAM: 'OPEN_CASHOUT_STREAM',
        CLOSE_CASHOUT_STREAM: 'CLOSE_CASHOUT_STREAM',
        GET_CASH_OUT_BETS_ASYNC: 'GET_CASH_OUT_BETS_ASYNC',
        GET_PLACED_BETS_ASYNC: 'GET_PLACED_BETS_ASYNC',
        DS_GET_GAME: 'DS_GET_GAME',
        GET_BETS_FOR_EVENT_ASYNC: 'GET_BETS_FOR_EVENT_ASYNC'
      }
    };
    nativeBridgeService = {
      onEventDetailsStreamAvailable: jasmine.createSpy('onEventDetailsStreamAvailable'),
      footballEventPageLoaded: jasmine.createSpy('footballEventPageLoaded'),
      hasShowFootballAlerts: jasmine.createSpy('hasShowFootballAlerts'),
      showFootballAlerts: jasmine.createSpy('showFootballAlerts'),
      hideVideoStream: jasmine.createSpy('hideVideoStream')
    };
    eventVideoStreamProviderService = {
      playSuccessErrorListener: jasmine.createSpy('playSuccessErrorListener').and.returnValue(of({}))
    };
    coreTools = {};
    userService = {};
    windowRef = {
      nativeWindow: {
        addEventListener: jasmine.createSpy('addEventListener'),
        removeEventListener: jasmine.createSpy('removeEventListener'),
        setInterval: jasmine.createSpy('setInterval'),
        clearInterval: jasmine.createSpy('clearInterval')
      },
      document: {
        removeEventListener: jasmine.createSpy('removeEventListener')
      }
    };
    sportEventPageProviderService = {
      sportData: {
        next: jasmine.createSpy('sportData.next')
      }
    };
    sportEventMainProviderService = {
      checkOptaScoreboardAvailability: jasmine.createSpy('checkOptaScoreboardAvailability').and.returnValue(of({}))
    };
    renderer = {
      listen: jasmine.createSpy('listen')
    };
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern')
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      detach: jasmine.createSpy('detach'),
    };
    scoreParserService = {
      parseScores: jasmine.createSpy('parseScores'),
      getScoreType: jasmine.createSpy('getScoreType'),
    };
    sportsConfigService = {};
    updateEventService = {};
    cashOutMapService = {};
    CashoutWsConnectorService = {};

    router = {
      navigate: jasmine.createSpy('navigate')
    };

    routingHelperService = {
      formCompetitionUrl: jasmine.createSpy('formCompetitionUrl').and.returnValue('competition/url')
    };

    sportConfig = {
      extendMarketsCollections: jasmine.createSpy('extendMarketsCollections'),
      config: {
        request: {
          categoryId: '1'
        }
      },
      getCollectionsTabs: jasmine.createSpy('extendMarketsCollections'),
      subscribeEDPForUpdates: jasmine.createSpy('subscribeEDPForUpdates'),
      getById: jasmine.createSpy('getById').and.returnValue(of(null)),
      unSubscribeEDPForUpdates: jasmine.createSpy('unSubscribeEDPForUpdates')
    };

    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of(sportConfig))
    };

    component = new SportEventMainComponent(
      deviceService,
      activatedRoute,
      visEventService,
      visDataHandler,
      pubSubService,
      cmsService,
      gtmService,
      localeService,
      commandService,
      nativeBridgeService,
      eventVideoStreamProviderService,
      coreTools,
      userService,
      windowRef,
      sportEventPageProviderService,
      sportEventMainProviderService,
      renderer,
      timeService,
      changeDetectorRef,
      scoreParserService,
      sportsConfigService,
      updateEventService,
      cashOutMapService,
      CashoutWsConnectorService,
      router,
      routingHelperService,
      storageService,
      sportEventHelperService
    );

    component.sport = sportConfig;
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
    expect(component['scoreSports']).toEqual(['BADMINTON', 'FOOTBALL']);
  });

  describe('scoreboardsLoadOrder', () => {
    it('should have the load order of scoreboard properly defined per sport', () => {
      expect(component['scoreboardsLoadOrder']).toEqual({
        default: ['OPTA','BR', 'IMG', 'IMG_ARENA', 'FS', 'GP'],
        tennis: ['OPTA', 'FS~', 'GP']
      });
    });
  });

  it('@goToCompetition should form url and call navigate', () => {
    component.eventEntity = {
      categoryName: 'categoryName',
      typeName: 'typeName',
      className: 'className'
    };

    component.goToCompetition();

    expect(routingHelperService.formCompetitionUrl).toHaveBeenCalledWith({
      sport: 'categoryName',
      typeName: 'typeName',
      className: 'className'
    });

    expect(router.navigate).toHaveBeenCalledWith(['competition/url']);
  });

  it('@reloadComponent should set streamShown to false and hide "done" button', () => {
    component.streamShown = true;
    component.reloadComponent();
    expect(component.streamShown).toBe(false);
  });

  it('should return eventEntity for non MTA sports', ()=>{
    const eventEntity = {id: 1} as any;
    component.eventEntity = eventEntity;
    expect(component.getEventEntity()).toEqual(eventEntity);
  });
});
