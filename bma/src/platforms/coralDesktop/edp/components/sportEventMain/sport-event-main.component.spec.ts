import { of, BehaviorSubject } from 'rxjs';
import { DesktopSportEventMainComponent } from '@coralDesktop/edp/components/sportEventMain/sport-event-main.component';
import { ISportEvent } from '@core/models/sport-event.model';

describe('CDSportEventMainComponent', () => {
  let component: DesktopSportEventMainComponent,
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
    sportConfig,
    sportsConfigService,
    sportEventHelperService,
    changeDetectorRef,
    updateEventService,
    CashoutWsConnectorService,
    storageService,
    cashOutMapService;
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
    visDataHandlerService = {};
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        HIDE_OPTA_SCOREBOARD: 'HIDE_OPTA_SCOREBOARD'
      }
    };
    storageService = {};
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({})),
      getFeatureConfig: jasmine.createSpy('getFeatureConfig').and.returnValue(of({})),
      getEDPMarkets: jasmine.createSpy('getEDPMarkets').and.returnValue(of({})),
      triggerSystemConfigUpdate: jasmine.createSpy('triggerSystemConfigUpdate'),
      getToggleStatus: jasmine.createSpy('getToggleStatus').and.returnValue(of(true))
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
        setInterval: jasmine.createSpy(),
        clearInterval: jasmine.createSpy(),
        addEventListener: jasmine.createSpy(), // TODO: Reverted changes from BMA-37049.
        // Will be removed after new approach implementation.
        removeEventListener: jasmine.createSpy(), // TODO: Reverted changes from BMA-37049.
        // Will be removed after new approach implementation.
      },
      document: {
        addEventListener: jasmine.createSpy(),
        removeEventListener: jasmine.createSpy()
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
        listen: jasmine.createSpy('listen').and.returnValue(() => { })
      }
    };
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern')
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
      getSport: jasmine.createSpy('getSport').and.returnValue(of({})),
    };
    sportEventHelperService = {
      isOutrightEvent: jasmine.createSpy('isOutrightEvent').and.returnValue(true)
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      detach: jasmine.createSpy('detach'),
    };
    updateEventService = {};
    cashOutMapService = {};
    CashoutWsConnectorService = {};

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
      sportsConfigService,
      sportEventHelperService,
      changeDetectorRef,
      updateEventService,
      cashOutMapService,
      CashoutWsConnectorService,
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
        default: ['OPTA', 'BG', 'BR', 'IMG', 'IMG_ARENA', 'FS', 'GP'],
        tennis: ['IMG', 'OPTA', 'BG', 'FS~', 'GP']
      });
    });
  });

  it('isDesktopScoreboardAvailable should return true', () => {
    component.eventEntity = {
      comments: {
        teams: {}
      }
    } as ISportEvent;
    component.sportName = 'badminton';
    component.isFallbackScoreboards = true;

    const actualResult = component.isDesktopScoreboardAvailable();

    expect(actualResult).toBeTruthy();
  });

  it('isLiveStreamAvailable should return true', () => {
    component.eventEntity = {
      liveStreamAvailable: true
    } as ISportEvent;
    component.showMatchLive = false;
    spyOnProperty(component, 'isMatchLive').and.returnValue(false);

    const actualResult = component.isLiveStreamAvailable();

    expect(actualResult).toBeTruthy();
  });

  it('isOutrightEvent should return true', () => {
    const actualResult = component.isOutrightEvent({} as ISportEvent);

    expect(sportEventHelperService.isOutrightEvent).toHaveBeenCalledWith({});
    expect(actualResult).toBeTruthy();
  });

  it('should toggle showMatchLive property', () => {
    const event = {
      preventDefault: jasmine.createSpy('preventDefault')
    } as any;

    component.showMatchLive = false;
    component.toggleLive(event);

    expect(component.showMatchLive).toBeTruthy();
    expect(event.preventDefault).toHaveBeenCalled();
  });

  afterEach(() => {
    component = null;
  });
  it('changeMatchToggle', () => {
    component.changeMatch = false;
    component.changeMatchToggle();
    expect(component.changeMatch).toBeTruthy();
  });
  it('closeQuickSwitchPanel', () => {
    component.closeQuickSwitchPanel();
    expect(component.changeMatch).toBeFalsy();
  });
});
