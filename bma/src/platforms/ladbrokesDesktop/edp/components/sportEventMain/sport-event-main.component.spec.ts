import { DesktopSportEventMainComponent } from '@ladbrokesDesktop/edp/components/sportEventMain/sport-event-main.component';
import { of, BehaviorSubject } from 'rxjs';

describe('LDesktopSportEventMainComponent', () => {
  let component;
  let deviceService;
  let activatedRoute;
  let visEventService;
  let visDataHandlerService;
  let pubSubService;
  let cmsService;
  let gtmService;
  let localeService;
  let commandService;
  let nativeBridgeService;
  let eventVideoStreamProviderService;
  let coreToolsService;
  let userService;
  let windowRefService;
  let sportEventPageProviderService;
  let sportEventMainProviderService;
  let rendererService;
  let timeService;
  let scoreParserService;
  let sportEventHelperService;
  let changeDetectorRef;
  let updateEventService;
  let cashOutMapService;
  let CashoutWsConnectorService;
  let router;
  let routingHelperService;
  let sportConfig;
  let storageService;
  let sportsConfigService;

  const menuItemMock = {
    categoryId: 10
  };
  const deviceViewType = {
    mobile: false,
    desktop: true,
    tablet: false
  };
  beforeEach(() => {
    deviceService = { getDeviceViewType: jasmine.createSpy('getDeviceViewType').and.returnValue(deviceViewType) };
    activatedRoute = {
      snapshot: {
        paramMap: {
          get: jasmine.createSpy('paramMap.get').and.returnValue('football')
        }
      },
      params: of({
        sport: 'football',
        id: '12345'
      })
    };
    visEventService = {
      visListener: jasmine.createSpy('visListener'),
      checkPreMatchWidgetAvailability: jasmine.createSpy('checkPreMatchWidgetAvailability').and.returnValue(of({})),
      checkForEventsWithAvailableVisualization: jasmine.createSpy()
    };
    storageService = {};
    visDataHandlerService = {};
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      API: {
        HIDE_OPTA_SCOREBOARD: 'HIDE_OPTA_SCOREBOARD'
      },
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({})),
      getEDPMarkets: jasmine.createSpy('getEDPMarkets').and.returnValue(of({})),
      triggerSystemConfigUpdate: jasmine.createSpy('triggerSystemConfigUpdate'),
      getToggleStatus: jasmine.createSpy('getToggleStatus').and.returnValue(of(true)),
      getFeatureConfig: jasmine.createSpy('getFeatureConfig').and.returnValue(of({})),
      getMenuItems: jasmine.createSpy('getMenuItems').and.returnValue(of([menuItemMock])),
    };
    gtmService = {};
    localeService = {};
    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve({})),
      API: {
        GET_CASH_OUT_BETS_ASYNC: 'GET_CASH_OUT_BETS_ASYNC',
        GET_PLACED_BETS_ASYNC: 'GET_PLACED_BETS_ASYNC',
        DS_GET_GAME: 'DS_GET_GAME'
      }
    };
    nativeBridgeService = {
      onEventDetailsStreamAvailable: jasmine.createSpy('onEventDetailsStreamAvailable'),
      eventPageLoaded: jasmine.createSpy('eventPageLoaded'),
      hasOnEventAlertsClick: jasmine.createSpy('hasOnEventAlertsClick'),
      onEventAlertsClick: jasmine.createSpy('onEventAlertsClick'),
      footballEventPageLoaded: jasmine.createSpy('footballEventPageLoaded'), // TODO: Reverted changes from BMA-37049.
      // Will be removed after new approach implementation.
      hasShowFootballAlerts: jasmine.createSpy('hasShowFootballAlerts'), // TODO: Reverted changes from BMA-37049.
      // Will be removed after new approach implementation.
      showFootballAlerts: jasmine.createSpy('showFootballAlerts') // TODO: Reverted changes from BMA-37049.
      // Will be removed after new approach implementation.
    };
    eventVideoStreamProviderService = {
      playSuccessErrorListener: jasmine.createSpy('playSuccessErrorListener').and.returnValue(of({}))
    };
    coreToolsService = {};
    userService = {};
    windowRefService = {
      nativeWindow: {
        setInterval: jasmine.createSpy('setInterval'),
        clearInterval: jasmine.createSpy('clearInterval'),
        addEventListener: jasmine.createSpy('addEventListener'), // TODO: Reverted changes from BMA-37049.
        // Will be removed after new approach implementation.
        removeEventListener: jasmine.createSpy('removeEventListener'), // TODO: Reverted changes from BMA-37049.
        // Will be removed after new approach implementation.
      },
      document: {
        addEventListener: jasmine.createSpy(),
        removeEventListener: jasmine.createSpy(),
      }
    };
    sportEventPageProviderService = {
      sportData: new BehaviorSubject<any>(null)
    };
    sportEventMainProviderService = {
      checkOptaScoreboardAvailability: jasmine.createSpy('checkOptaScoreboardAvailability').and.returnValue(of({}))
    };
    rendererService = {
      renderer: {
        listen: jasmine.createSpy('listen').and.returnValue(() => {})
      }
    };
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern')
    };
    scoreParserService = {
      getScoreType: jasmine.createSpy('getScoreType')
    };
    sportEventHelperService = {};
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      detach: jasmine.createSpy('detach'),
    };
    updateEventService = {};

    cashOutMapService = {};

    CashoutWsConnectorService = {};

    router = {
      navigate: jasmine.createSpy('navigate')
    };

    routingHelperService = {
      formCompetitionUrl: jasmine.createSpy('formCompetitionUrl').and.returnValue('competition/url')
    };

    scoreParserService = {
      getScoreType: jasmine.createSpy('getScoreType')
    };

    sportConfig = {
      extendMarketsCollections: jasmine.createSpy('extendMarketsCollections'),
      config: {
        request: {
          categoryId: '1'
        }
      },
      getScoreboardConfig: jasmine.createSpy('getScoreboardConfig'),
      getCollectionsTabs: jasmine.createSpy('extendMarketsCollections'),
      subscribeEDPForUpdates: jasmine.createSpy('subscribeEDPForUpdates'),
      unSubscribeEDPForUpdates: jasmine.createSpy('unSubscribeEDPForUpdates'),
      getById: jasmine.createSpy('getById').and.returnValue(of({
        event: [{ startTime: '2019-01-02T22:04:00', categoryId: '16', name: 'Ashleigh Barty* v Saisai Zheng' }]
      }))
    };

    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of(sportConfig))
    };

    component = new DesktopSportEventMainComponent(
      deviceService,
      activatedRoute,
      visEventService,
      visDataHandlerService,
      pubSubService,
      cmsService,
      gtmService,
      localeService,
      commandService,
      nativeBridgeService,
      eventVideoStreamProviderService,
      coreToolsService,
      userService,
      windowRefService,
      sportEventPageProviderService,
      sportEventMainProviderService,
      rendererService,
      timeService,
      scoreParserService,
      sportEventHelperService,
      changeDetectorRef,
      updateEventService,
      cashOutMapService,
      CashoutWsConnectorService,
      sportsConfigService,
      router,
      routingHelperService,
      storageService
    );

    component.sport = sportConfig;
  });

  it('should create DesktopSportEventMainComponent instance', () => {
    expect(component).toBeTruthy();
  });

  it('sport should be olympics', () => {
    sportConfig.extension = 'olympics';
    component.init();
    expect(component.isOlympics).toBeTruthy();
  });

  describe('scoreboardsLoadOrder', () => {
    it('should have the load order of scoreboard properly defined per sport', () => {
      expect(component['scoreboardsLoadOrder']).toEqual({
        default: ['OPTA', 'BR', 'IMG', 'IMG_ARENA', 'FS', 'GP'],
        tennis: ['OPTA', 'FS~', 'GP']
      });
    });
  });
});
