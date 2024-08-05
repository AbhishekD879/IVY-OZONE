import { EMPTY, Observable, of, Subject, throwError } from 'rxjs';
import { SportEventMainComponent } from '@edp/components/sportEventMain/sport-event-main.component';
import { fakeAsync, tick } from '@angular/core/testing';
import * as _ from 'underscore';
import { SCOREBOARDS_LOAD_ORDER } from '@edp/components/sportEventMain/sport-event-main.constant';
import { BETRADAREVENTMAPPING, IMG_ARENA_EVENT_BYMAPPING } from './mock/sport-bymapping';
import { ALERTS_GTM } from '@app/betHistory/constants/bet-leg-item.constant';
import environment from '@environment/oxygenEnvConfig';

describe('AppSportEventMainComponent', () => {
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
    rendererService,
    timeService,
    changeDetectorRef,
    updateEventService,
    cashOutMapService,
    CashoutWsConnectorService,
    scoreParserService,
    successfulLoginHandler,
    emaHandler,
    sportConfig,
    storageService,
    sportsConfigService,
    sportEventHelperService;

  const menuItemMock = {
    categoryId: 10
  };

  const deviceViewType = {
    mobile: true,
    desktop: false,
    tablet: false
  };
  beforeEach(() => {
    scoreParserService = {
      parseScores: jasmine.createSpy('parseScores'),
      getScoreType: jasmine.createSpy('getScoreType'),
    };
    deviceService = {getDeviceViewType: jasmine.createSpy('getDeviceViewType').and.returnValue(deviceViewType) };
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
    storageService = {
      set: jasmine.createSpy('storageService.set'),
      get: jasmine.createSpy('storageService.get').and.returnValue([{"eventId":"11","betIds":[3]},{"eventId":"2","betIds":[4]}]),
    };
    visEventService = {
      visListener: jasmine.createSpy('visListener'),
      checkPreMatchWidgetAvailability: jasmine.createSpy('checkPreMatchWidgetAvailability').and.returnValue(of({})),
      checkForEventsWithAvailableVisualization: jasmine.createSpy()
    };
    visDataHandler = {
      init: jasmine.createSpy('init').and.returnValue(of({}))
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((name, listeners, handler) => {
        if (listeners === 'SUCCESSFUL_LOGIN') {
          successfulLoginHandler = handler;
        } else if (listeners === 'EDIT_MY_ACCA') {
          emaHandler = handler;
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        PIN_TOP_BAR: 'PIN_TOP_BAR',
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN',
        SPORT_EDP_CLOSED: 'SPORT_EDP_CLOSED',
        HIDE_OPTA_SCOREBOARD: 'HIDE_OPTA_SCOREBOARD',
        SYSTEM_CONFIG_UPDATED: 'SYSTEM_CONFIG_UPDATED',
        EMA_OPEN_CANCEL_DIALOG: 'EMA_OPEN_CANCEL_DIALOG',
        EMA_UNSAVED_ON_EDP: 'EMA_UNSAVED_ON_EDP',
        IS_NATIVE_VIDEO_STICKED: 'IS_NATIVE_VIDEO_STICKED',
        CASH_OUT_BET_PROCESSED: 'CASH_OUT_BET_PROCESSED',
        UNSUBSCRIBE_LS_UPDATES_MS: 'UNSUBSCRIBE_LS_UPDATES_MS',
        MY_BETS_UPDATED: 'MY_BETS_UPDATED',
        CASHOUT_CTRL_STATUS: 'CASHOUT_CTRL_STATUS',
        EDIT_MY_ACCA: 'EDIT_MY_ACCA',
        LIVE_MARKET_FOR_EDP: 'LIVE_MARKET_FOR_EDP',
        EVENT_MY_BETS_COUNTER: 'EVENT_MY_BETS_COUNTER',
        AUTOSEO_DATA_UPDATED: 'AUTOSEO_DATA_UPDATED',
        MY_BET_PLACED: 'MY_BET_PLACED',
      }
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({})),
      getFeatureConfig: jasmine.createSpy('getFeatureConfig').and.returnValue(of({})),
      getEDPMarkets: jasmine.createSpy('getEDPMarkets').and.returnValue(of({})),
      triggerSystemConfigUpdate: jasmine.createSpy('triggerSystemConfigUpdate'),
      getMenuItems: jasmine.createSpy('getMenuItems').and.returnValue(of([menuItemMock])),
      getToggleStatus: jasmine.createSpy().and.returnValue(of(true)),
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
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
      playerStatus: true,
      onEventDetailsStreamAvailable: jasmine.createSpy('onEventDetailsStreamAvailable'),
      eventPageLoaded: jasmine.createSpy('eventPageLoaded'),
      hasOnEventAlertsClick: jasmine.createSpy('hasOnEventAlertsClick'),
      onEventAlertsClick: jasmine.createSpy('onEventAlertsClick'),
      footballEventPageLoaded: jasmine.createSpy('footballEventPageLoaded'), // TODO: Reverted changes from BMA-37049.
                                                                             // Will be removed after new approach implementation.
      hasShowFootballAlerts: jasmine.createSpy('hasShowFootballAlerts'), // TODO: Reverted changes from BMA-37049.
                                                                         // Will be removed after new approach implementation.
      showFootballAlerts: jasmine.createSpy('showFootballAlerts'), // TODO: Reverted changes from BMA-37049.
                                                                        // Will be removed after new approach implementation.
      hideVideoStream: jasmine.createSpy('hideVideoStream'),
      getMobileOperatingSystem: jasmine.createSpy('getMobileOperatingSystem'),
      handleNativeVideoPlaceholder: jasmine.createSpy('handleNativeVideoPlaceholder'),
      handleNativeVideoPlayer: jasmine.createSpy('handleNativeVideoPlayer'),
      hideVideoPlaceholder: jasmine.createSpy('hideVideoPlaceholder')
    };
    eventVideoStreamProviderService = {
      playSuccessErrorListener: new Subject<boolean>(),
      playListener: new Subject<boolean>(),
      getStreamBetCmsConfig: jasmine.createSpy('getStreamBetCmsConfig').and.returnValue(of({})),
      isStreamBetAvailable: jasmine.createSpy('isStreamBetAvailable')
    };
    coreTools = {
      hasOwnDeepProperty: jasmine.createSpy('hasOwnDeepProperty')
    };
    userService = {
      status: false,
      currency: 'USD',
      currencySymbol: '$'
    };
    windowRef = {
      nativeWindow: {
        addEventListener: jasmine.createSpy('addEventListener'), // TODO: Reverted changes from BMA-37049.
                                                                 // Will be removed after new approach implementation.
        removeEventListener: jasmine.createSpy('removeEventListener') // TODO: Reverted changes from BMA-37049.
                                                                      // Will be removed after new approach implementation.
      },
      document: {
        removeEventListener: jasmine.createSpy('removeEventListener'),
        addEventListener: jasmine.createSpy('addEventListener')
      }
    };
    sportEventPageProviderService = {
      sportData: {
        next: jasmine.createSpy('sportData.next')
      }
    };
    sportEventMainProviderService = {
      checkOptaScoreboardAvailability: jasmine.createSpy('checkOptaScoreboardAvailability').and.returnValue(of({})),
      checkBetradarAvailability: jasmine.createSpy('checkBetradarAvailability').and.returnValue(of({})),
      checkImgArenaScoreboardAvailability: jasmine.createSpy('checkImgArenaScoreboardAvailability').and.returnValue(of({}))
    };
    rendererService = {
      renderer: {
        listen: jasmine.createSpy('listen')
      }
    };
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern')
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      detach: jasmine.createSpy('detach'),
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
      updateCollectionsWithLiveMarket: jasmine.createSpy('updateCollectionsWithLiveMarket').and.returnValue(false),
      subscribeEDPForUpdates: jasmine.createSpy('subscribeEDPForUpdates'),
      unSubscribeEDPForUpdates: jasmine.createSpy('unSubscribeEDPForUpdates'),
      getById: jasmine.createSpy('getById').and.returnValue(of({
        event: [{ startTime: '2019-01-02T22:04:00', categoryId: '16', name: 'Ashleigh Barty* v Saisai Zheng' }]
      })),
      sportConfig: {
        specialsTypeIds: []
      }
    };
    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of(sportConfig))
    };
    updateEventService = {};
    cashOutMapService = {
      createCashoutBetsMap: jasmine.createSpy('createCashoutBetsMap')
    };
    CashoutWsConnectorService = {
      getConnection: jasmine.createSpy('getConnection'),
      dateChangeBet: jasmine.createSpy('dateChangeBet')
    };
    sportEventHelperService = {
      isSpecialEvent: jasmine.createSpy('isSpecialEvent').and.returnValue(false),
      isOutrightEvent: jasmine.createSpy('isOutrightEvent').and.returnValue(false)
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
      rendererService,
      timeService,
      changeDetectorRef,
      scoreParserService,
      sportsConfigService,
      updateEventService,
      cashOutMapService,
      CashoutWsConnectorService,
      storageService,
      sportEventHelperService
    );
    component.sysConfig = {} as any;
    component.sport = sportConfig;
  });

  describe('constructor', () => {
    it('should initialize properties', () => {
      expect(component.streamShown).toEqual(false);
      expect(component.sportName).toEqual('');
      expect(component.eventId).toEqual('');
      expect(component.isEnhanceMultiples).toEqual(false);
      expect(component.isOutRight).toEqual(false);
      expect(component.isSpecialEvent).toEqual(false);
      expect(component.isScoreboardVis).toEqual(true);
      expect(component.showMatchLive).toEqual(true);
      expect(component.showScoreboard).toEqual(false);
      expect(component.optaScoreboardAvailable).toEqual(false);
      expect(component.bgScoreboardConfig).toEqual({ available: false });
      expect(component.brScoreboardConfig).toEqual({ available: false });
      expect(component.eventsWithVisualizationParams).toEqual([]);
      expect(component.footballAlertsVisible).toEqual(false);
      expect(component.footballBellActive).toEqual(false);
      expect(component.favouritesVisible).toEqual(undefined);
      expect(component.isEnhancedMultiplesEnabled).toEqual(false);
      expect((component as any).eventStartDatePattern).toEqual('EEEE, d-MMM-yy. HH:mm');
      expect((component as any).scoreboardsLoadOrder).toEqual(SCOREBOARDS_LOAD_ORDER);
      expect((component as any).scoreSports).toEqual(['BADMINTON']);
      expect((component as any).scoreboardsLoaders).toEqual({
        PM: jasmine.any(Function), OPTA: jasmine.any(Function), IMG: jasmine.any(Function), IMG_ARENA: jasmine.any(Function),
        FS: jasmine.any(Function), BG: jasmine.any(Function),   BR: jasmine.any(Function),
        GP: jasmine.any(Function)
      });
      expect((component as any).isIMGScoreboardAvailable).toEqual(false);
      expect((component as any).isOptaScoreboardChecked).toEqual(false);
      expect((component as any).betsStreamOpened).toEqual(false);
      expect((component as any).tagName).toEqual('sportEventMain');
    });
  });

  describe('@init', () => {
    it('should set EDP_MARKETS from CMS', () => {
      const EDP_MARKETS = [{
        id: '5d2e1703c9e77c0001eaa754',
        lastItem: false,
        marketId: null,
        name: 'All Markets'
      }];
      cmsService.getEDPMarkets = jasmine.createSpy().and.returnValue(of(EDP_MARKETS));
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of({ScoreboardsDataDisclaimer:{enabled: false, dataDisclaimer: ''}}))
      component['init']()
        .subscribe(() => {
          expect(component.EDP_MARKETS).toEqual(EDP_MARKETS);
        });
    });
    it('no getSystemConfig', () => {
      const EDP_MARKETS = [{
        id: '5d2e1703c9e77c0001eaa754',
        lastItem: false,
        marketId: null,
        name: 'All Markets'
      }];
      cmsService.getEDPMarkets = jasmine.createSpy().and.returnValue(of(EDP_MARKETS));
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of({}))
      component['init']()
        .subscribe(() => {
          expect(component.EDP_MARKETS).toEqual(EDP_MARKETS);
        });
    });
    it('should set EDP_MARKETS if CMS error', () => {
      cmsService.getEDPMarkets = jasmine.createSpy().and.returnValue(throwError(null));
      component['init']()
        .subscribe(() => {}, () => {
          expect(component.EDP_MARKETS).toEqual([]);
        });
    });
  });

  describe('ngOnchanges', () => {
    it('should set isQuickSwitchPanelActive', () => {
      const changes: any = {
        isQuickSwitchPanelActive: {
          currentValue: { name: 'test' as any }
        }
      };
      component.ngOnChanges(changes);
      expect(component.isQuickSwitchPanelActive).toEqual(changes.isQuickSwitchPanelActive.currentValue);
    });
  });

  describe('@ngOnInit', () => {
    beforeEach(() => {
      component.sport.getById.and.returnValue(of({
        event: [{
          startTime: '2019-01-02T22:04:00',
          categoryId: '16',
          name: 'Ashleigh Barty* v Saisai Zheng',
          liveStreamAvailable: true,
          classId: '123',
          typeId: '124',
          id: '12345'
        }]
      }));
    });

    it('should init eventVideoStreamSubscriber', fakeAsync(() => {
      expect(component.streamShown).toEqual(false);

      component.ngOnInit();
      tick();
      eventVideoStreamProviderService.playSuccessErrorListener.next(true);
      expect(component.streamShown).toEqual(true);
    }));

    it('should init messageListener', fakeAsync(() => {
      rendererService.renderer.listen.and.callFake((dom, message, eventFn) => {
        eventFn && eventFn('click');
      });
      component.ngOnInit();
      tick();

      expect(visEventService.visListener).toHaveBeenCalledWith('click');
    }));

    

    it('do not Subscribe for liveServe PUSH updates', fakeAsync(() => {
      component.sport.getById.and.returnValue(of({
        event: []
      }));

      component.ngOnInit();
      tick();

      expect(component.sport.subscribeEDPForUpdates).not.toHaveBeenCalledWith();
    }));

    it('should parse activatedRoute.snapshot', () => {
      (activatedRoute.snapshot.paramMap.get as jasmine.Spy).and.callFake((paramName: string) => paramName);
      component.ngOnInit();
      expect(component.sportName).toBe('sport');
      expect(component.eventId).toBe('id');
      expect(component.showMatchLive).toBe(true);

      (activatedRoute.snapshot.paramMap.get as jasmine.Spy).and.returnValue('watch-live');
      component.ngOnInit();
      expect(component.showMatchLive).toBe(false);
    });

    it('should not call excludedFanzoneMarkets', () => {
      component.isFootball = false;
      spyOn(component, 'excludedFanzoneMarkets');

      component.ngOnInit();

      expect(component.excludedFanzoneMarkets).not.toHaveBeenCalled();
    });

    it('should call excludedFanzoneMarkets', fakeAsync(() => {
      component.isFootball = true;
      spyOn(component, 'excludedFanzoneMarkets');

      component.ngOnInit();

      tick();
      expect(component.excludedFanzoneMarkets).toHaveBeenCalled();
    })); 

    it('should subscribe to hide scoreboard component on custom event', fakeAsync(() => {
      component.ngOnInit();
      tick();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('sportEventMain',
        pubSubService.API.HIDE_OPTA_SCOREBOARD,
        jasmine.any(Function));
    }));

    it('should remove "*" from event name', fakeAsync(() => {
      component.ngOnInit();
      tick();
      expect(component.eventEntity.name).toEqual('Ashleigh Barty v Saisai Zheng');
    }));

    it('ngOnInit should throw error', fakeAsync(() => {
      component.init = jasmine.createSpy('init').and.returnValue(throwError('error'));
      component.ngOnInit();
      tick();

      expect(component.state.error).toBeTruthy();
    }));

    it('EMA_UNSAVED_ON_EDP', fakeAsync(() => {
      pubSubService.subscribe.and.callFake((file, method, cb) => {
        if (method === 'EMA_UNSAVED_ON_EDP') {
          cb(true);
        }
      });

      component.ngOnInit();
      tick();
      expect(component['editMyAccaUnsavedOnEdp']).toEqual(true);
    }));

    it('should call onEventDetailsStreamAvailable', fakeAsync(() => {
      component['deviceService'].isWrapper = true;
      component.ngOnInit();
      tick();
      expect(component.streamShown).toEqual(true);
      expect(nativeBridgeService.onEventDetailsStreamAvailable).toHaveBeenCalledWith({
        categoryId: 16,
        classId: 123,
        typeId: 124,
        eventId: 12345
      });
    }));

    it('should not call onEventDetailsStreamAvailable when liveStreamAvailable not available', fakeAsync(() => {
      component.sport.getById.and.returnValue(of({
        event: [{
          startTime: '2019-01-02T22:04:00',
          categoryId: '16',
          name: 'Ashleigh Barty* v Saisai Zheng',
          liveStreamAvailable: false,
          classId: '123',
          typeId: '124',
          id: '12345'
        }]
      }));
      component.deviceService.isWrapper = true;
      component.ngOnInit();
      tick();
      expect(component.streamShown).toEqual(true);
      expect(nativeBridgeService.onEventDetailsStreamAvailable).not.toHaveBeenCalled();
    }));

    it('should check isOutRight', fakeAsync(() => {
      component.sport.getById.and.returnValue(of({
        event: [{
          name: 'name',
          startTime: '2019-01-02T22:04:00',
          categoryId: '16',
          categoryCode: 'GOLF',
          eventSortCode: 'TR01'
        }]
      }));
      component.ngOnInit();
      tick();
      expect(component.isOutRight).toEqual(true);
    }));

    it('should check SCOREBOARD_VISIBILITY', fakeAsync(() => {
      const placedBets = [ { id: 4, settled: 'Y', cashoutStatus: 'BET_CASHED_OUT', type: '', leg: [ {'part':[{eventId: "11"}]}] }];
      const betsData = { placedBets: placedBets, cashoutIds: [], bets: [] };
      commandService.executeAsync.and.callFake(key => {
        if (key === 'GET_BETS_FOR_EVENT_ASYNC') {
          return Promise.resolve(betsData);
        }

        return Promise.resolve({});
      });

      component.eventEntity = {
        id: '12345'
      };
      component.handleFootballAlerts({
        detail: {
          isEnabled: true,
          settingValue: true
        }
      });
      pubSubService.subscribe.and.callFake((name, channel, fn) => {
        fn && fn({
          detail: {
            isEnabled: true,
            settingValue: true,
          },
          bets: [ { id: 4, settled: 'Y', cashoutStatus: 'BET_CASHED_OUT', type: '', leg: [ {'part':[{eventId: "11"}]}] }]
        });
      });
      component.ngOnInit();
      tick();
      expect(component.isScoreboardVis).toEqual({detail : { isEnabled: true, settingValue: true }, bets: [ { id: 4, settled: 'Y', cashoutStatus: 'BET_CASHED_OUT', type: '', leg: [ {'part':[{eventId: "11"}]}] }]});
      expect(component.showScoreboard).toEqual({detail : { isEnabled: true, settingValue: true }, bets: [ { id: 4, settled: 'Y', cashoutStatus: 'BET_CASHED_OUT', type: '', leg: [ {'part':[{eventId: "11"}]}] }]});
    }));

    describe('check LIVE_MARKET_FOR_EDP', () => {
      beforeEach(() => {
        pubSubService.subscribe.and.callFake((name, channel, fn) => {
          if (channel === 'LIVE_MARKET_FOR_EDP') {
            fn && fn(true);
          }
        });
      });

      it('should check LIVE_MARKET_FOR_EDP result false', fakeAsync(() => {
        component.ngOnInit();
        tick();
        expect(component.sport.getCollectionsTabs).toHaveBeenCalledTimes(1);
        expect(sportEventPageProviderService.sportData.next).toHaveBeenCalledTimes(1);
      }));

      it('should check LIVE_MARKET_FOR_EDP result true', fakeAsync(() => {
        component.sport.updateCollectionsWithLiveMarket.and.returnValue(true);
        component.ngOnInit();
        tick();
        expect(component.sport.getCollectionsTabs).toHaveBeenCalledTimes(2);
        expect(sportEventPageProviderService.sportData.next).toHaveBeenCalledTimes(2);
      }));
    });

    it('should set startTime to NativeBridge', fakeAsync(() => {
      expect(nativeBridgeService.eventStartTime).toEqual(undefined);

      component.sport.getById.and.returnValue(of({
        event: [{
          name: 'name',
          startTime: '2019-01-02T22:04:00',
          categoryId: '16',
          categoryCode: 'GOLF',
          categoryName: 'Football',
          eventSortCode: 'TR01'
        }]
      }));

      component.ngOnInit();
      tick();
      expect(nativeBridgeService.eventStartTime).toEqual('2019-01-02T22:04:00');
    }));

    describe('on HIDE_OPTA_SCOREBOARD event', () => {
      let pubSubCbMap = {};
      beforeEach(fakeAsync(() => {
        component.sportName = 'football';
        spyOn(component as any, 'prepareEventVisualization');
        spyOn(component as any, 'getSportScoreboardsLoadOrder').and.callThrough();
        pubSubCbMap = {};
        pubSubService.subscribe.and.callFake((name, channel, fn) => pubSubCbMap[channel] = fn);

        component.ngOnInit();
        tick();
        component['prepareEventVisualization'].calls.reset();
        component['getSportScoreboardsLoadOrder'].calls.reset();
        component['optaScoreboardAvailable'] = true;
      }));

      describe('should prepare Event Visualization/Scoreboards with OPTA excluded from loaders if it is available', () => {
        it('for live event', () => {
          component.eventEntity = { eventIsLive: true };
          pubSubCbMap['HIDE_OPTA_SCOREBOARD']();
          expect(component['prepareEventVisualization']).toHaveBeenCalledWith(['BG','BR','IMG', 'IMG_ARENA', 'FS', 'GP']);
        });
        it('for pre-match event', () => {
          component.eventEntity = { eventIsLive: false };
          pubSubCbMap['HIDE_OPTA_SCOREBOARD']();
          expect(component['prepareEventVisualization']).toHaveBeenCalledWith(['PM']);
        });
        afterEach(() => {
          expect(component['getSportScoreboardsLoadOrder']).toHaveBeenCalled();
        });
      });

      it('should do nothing if OPTA is already hidden', () => {
        component['optaScoreboardAvailable'] = false;

        pubSubCbMap['HIDE_OPTA_SCOREBOARD']();
        expect(component['prepareEventVisualization']).not.toHaveBeenCalled();
        expect(component['getSportScoreboardsLoadOrder']).not.toHaveBeenCalled();
      });

      afterEach(() => {
        expect(component['optaScoreboardAvailable']).toEqual(false);
      });
    });

    it('should start preparation of Event Visualization/Scoreboards', fakeAsync(() => {
      spyOn(component as any, 'prepareEventVisualization');
      component.ngOnInit();
      tick();
      expect(component['prepareEventVisualization']).toHaveBeenCalledWith();
    }));

    it('should subscribe on "CASH_OUT_BET_PROCESSED" pubsub event', fakeAsync(() => {
      component.ngOnInit();
      tick();
      expect(pubSubService.subscribe.calls.allArgs()).toContain(['sportEventMain', 'CASH_OUT_BET_PROCESSED', jasmine.any(Function)]);
    }));

    describe('IS_NATIVE_VIDEO_STICKED subscription', () => {
      describe('for Wrapper', () => {
        beforeEach(() => {
          nativeBridgeService.isWrapper = true;
        });
        it('should subscribe on "IS_NATIVE_VIDEO_STICKED" pubsub event', () => {
          component.ngOnInit();
          expect(pubSubService.subscribe).toHaveBeenCalledWith('sportEventMain',
            'IS_NATIVE_VIDEO_STICKED', jasmine.any(Function));
        });
        it('when IS_NATIVE_VIDEO_STICKED event received', () => {
          const pubsubMap = {};
          (component as any).nativeVideoPlayerPlaceholder = { className: 'native-video-player-placeholder'};
          pubSubService.subscribe.and.callFake((name, subscription, fn) => { pubsubMap[subscription] = fn; });
          component.ngOnInit();
          pubsubMap['IS_NATIVE_VIDEO_STICKED'](true);
          expect(nativeBridgeService.handleNativeVideoPlaceholder)
            .toHaveBeenCalledWith(true, { className: 'native-video-player-placeholder'});
          expect(pubSubService.publish).toHaveBeenCalledWith('PIN_TOP_BAR', true);
        });
      });
      it('should not subscribe to "IS_NATIVE_VIDEO_STICKED" pubsub event for non-wrapper', () => {
        nativeBridgeService.isWrapper = false;
        component.ngOnInit();
        expect(pubSubService.subscribe).not.toHaveBeenCalledWith('sportEventMain', 'IS_NATIVE_VIDEO_STICKED', jasmine.any(Function));
      });
    });

    it('should update cashoutIds, cashoutBets and placedBets on "CASH_OUT_BET_PROCESSED" pubsub event', fakeAsync(() => {
      const pubSubCbMap = {
        CASH_OUT_BET_PROCESSED: jasmine.createSpy('CASH_OUT_BET_PROCESSED')
      };
      pubSubService.subscribe.and.callFake((name, method, fn) => { pubSubCbMap[method] = fn; });
      component.ngOnInit();
      tick();
      component.eventId = '12345';
      component.cashoutIds = [{ id: 'i1' }, { id: 'i2' }, { id: 'i3' }];
      component.placedBets = [{ betId: 'i1', id: '1', leg: ['1'] }, { betId: 'i2', id: '2', leg: ['2'] }];
      component.cashoutBets = [{ betId: 'i2', id: '2', leg: ['2'] }, { betId: 'i3', id: '3', leg: ['3'] }];
      pubSubCbMap['CASH_OUT_BET_PROCESSED']('i2');
      expect(component.cashoutIds).toEqual([{ id: 'i1' }, { id: 'i3' }]);
      expect(component.placedBets).toEqual([{ betId: 'i1', id: '1', leg: ['1'] }, { betId: 'i2', id: '2', leg: ['2'], type: 'placedBetsWithoutCashoutPossibility' }]);
      expect(component.cashoutBets).toEqual([{ betId: 'i2', id: '2', leg: ['2'], type: 'placedBetsWithoutCashoutPossibility' }, { betId: 'i3', id: '3', leg: ['3'] }]);
    }));

    it('should update cashoutIds, cashoutBets and placedBets on "CASH_OUT_BET_PROCESSED" showSingposting true', fakeAsync(() => {
      const pubSubCbMap = {
        CASH_OUT_BET_PROCESSED: jasmine.createSpy('CASH_OUT_BET_PROCESSED')
      };
      pubSubService.subscribe.and.callFake((name, method, fn) => { pubSubCbMap[method] = fn; });
      component.ngOnInit();
      tick();
      component.eventId = '11';
      component.cashoutIds = [{ id: 'i1'}, { id: 'i2' }, { id: 'i3' }];
      component.placedBets = [{ id: 11, settled: 'N', cashoutStatus: 'BET_CASHED_IN', type: '', leg: [1,3,4,11] },
      { id: 6, settled: 'N', cashoutStatus: 'BET_CASHED_IN', type: '', leg: [1,3,4,7] }];
      component.cashoutBets = [{ betId: 'i2', id: '2', leg: ['2'] }, { betId: 'i3', id: '3', leg: ['3'] }];
      pubSubCbMap['CASH_OUT_BET_PROCESSED']('i2');
      expect(component.cashoutIds).toEqual([{ id: 'i1' }, { id: 'i3' }]);
      expect(component.cashoutBets).toEqual([{ betId: 'i2', id: '2', leg: ['2'], type: 'placedBetsWithoutCashoutPossibility' }, { betId: 'i3', id: '3', leg: ['3'] }]);
    }));

    it('should set eventStartDate to correct date format', fakeAsync(() => {
      component.eventEntity = { startTime: '2019-01-02T22:04:00' };
      timeService.formatByPattern.and.returnValue('Wednesday, 2-Jan-19. 22:04');
      const date = new Date(component.eventEntity.startTime);
      component.ngOnInit();
      tick();
      expect(timeService.formatByPattern).toHaveBeenCalledWith(date, 'EEEE, d-MMM-yy. HH:mm', null, null, 'en-US');
      expect(component.eventStartDate).toEqual('Wednesday, 2-Jan-19. 22:04');
    }));

    it('should close connection if there is no event', fakeAsync(() => {
      component.sport.getById.and.returnValue(of({
        event: undefined
      }));
      component['betsStreamOpened'] = true;
      component.ngOnInit();
      tick();
      expect(commandService.executeAsync).toHaveBeenCalledWith(commandService.API.CLOSE_CASHOUT_STREAM);
    }));

    it('should handle SUCCESSFUL_LOGIN event', fakeAsync(() => {
      const callbacks = {};

      pubSubService.subscribe.and.callFake((subscriber, keys, fn) => {
        if (_.isArray(keys)) {
          _.each(keys, key => {
            callbacks[key] = fn;
          });
        } else {
          callbacks[keys] = fn;
        }
      });
      userService.status = false;
      component.ngOnInit();
      tick();

      expect(component['isLoggedIn']).toBeFalsy();

      userService.status = true;
      callbacks['SUCCESSFUL_LOGIN']();

      expect(nativeBridgeService.hideVideoStream).toHaveBeenCalled();

      tick(1001);
      expect(component.state.loading).toBeFalsy();
    }));

    describe('getCashOutData', () => {
      let cashoutBets;
      let placedBets;
      let betsData;

      beforeEach(() => {
        component.isLoggedIn = true;
        cashoutBets = [{ id: 2, cashoutValue: '1.00' }];
        placedBets = [{ id: 1 }];
        betsData = { placedBets: placedBets, cashoutIds: [] };

        commandService.executeAsync.and.callFake(key => {
          if (key === 'GET_CASH_OUT_BETS_ASYNC') {
            return Promise.resolve(cashoutBets);
          } else if (key === 'GET_PLACED_BETS_ASYNC') {
            return Promise.resolve(placedBets);
          } else if (key === 'GET_BETS_FOR_EVENT_ASYNC') {
            return Promise.resolve(betsData);
          }

          return Promise.resolve({});
        });
      });

      it('should set "My bets" tab as available if there are placedBets returned', fakeAsync(() => {
        component.ngOnInit();
        tick();

        expect(component['betsStreamOpened']).toBeTruthy();
        expect(commandService.executeAsync).toHaveBeenCalledWith(commandService.API.OPEN_CASHOUT_STREAM);
        expect(component.placedBets).toEqual(betsData.placedBets);
        expect(component.cashoutIds).toEqual([]);
        expect(component.myBetsCounter).toEqual(1);
        expect(component.myBets).toEqual('sb.myBets (1)');
        expect(component.myBetsAvailable).toBeTruthy();
      }));

      it('should set "My bets" tab as available if there are no placedBets returned but are cashout ids', fakeAsync(() => {
        betsData = {
          placedBets: [],
          cashoutIds: [cashoutBets[0].id]
        };

        component.ngOnInit();
        tick();

        expect(component['betsStreamOpened']).toBeTruthy();
        expect(commandService.executeAsync).toHaveBeenCalledWith(commandService.API.OPEN_CASHOUT_STREAM);
        expect(component.placedBets).toEqual([]);
        expect(component.cashoutIds).toEqual([cashoutBets[0].id]);
        expect(component.myBetsCounter).toEqual(0);
        expect(component.myBets).toEqual('sb.myBets');
        expect(component.myBetsAvailable).toBeTruthy();
      }));

      it(`should filter placedBets`, fakeAsync(() => {
        betsData = {
          placedBets: [
            { id: 11 },
            { id: 2, settled: 'Y' },
            { id: 3, cashoutStatus: 'BET_CASHED_OUT' },
            { id: 4, settled: 'Y', cashoutStatus: 'BET_CASHED_OUT' }
          ],
          cashoutIds: []
        };

        component.ngOnInit();
        tick();

        expect(component.placedBets).toEqual([{ id: 11 }]);
      }));

      it('should set "My bets" tab as unavailable if there are no placedBets or cashoutIds returned', fakeAsync(() => {
        betsData = {
          placedBets: [],
          cashoutIds: []
        };

        component['betsStreamOpened'] = true;
        component.ngOnInit();
        tick();

        expect(component['betsStreamOpened']).toBeFalsy();
        expect(commandService.executeAsync).toHaveBeenCalledWith(commandService.API.CLOSE_CASHOUT_STREAM);
        expect(component.myBetsAvailable).toBeFalsy();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      }));

      it('should not attempt to update My bets tab data if user is not logged in', fakeAsync(() => {
        component.isLoggedIn = false;
        component.ngOnInit();
        tick();
        expect(commandService.executeAsync.calls.allArgs()).toEqual([ ['DS_GET_GAME', ['football', '1'], [] ] ]);
        expect(cmsService.getEDPMarkets).toHaveBeenCalled();
        expect(cmsService.getSystemConfig).toHaveBeenCalledWith();
        expect(cmsService.getFeatureConfig).toHaveBeenCalledWith('ScoreboardsSports', false, true);
      }));
    });

    it(`should show New User Tabs if ScoreboardsSports is true for this sport`, fakeAsync(() => {
      activatedRoute.snapshot.paramMap.get.and.returnValue('tennis');
      cmsService.getFeatureConfig.and.returnValue(of({ 16: true } ));

      component.ngOnInit();
      tick();

      expect(component.showNewUserTabs).toBeTruthy();
    }));

    it(`should Not show New User Tabs if ScoreboardsSports is Not true for this sport`, fakeAsync(() => {
      activatedRoute.snapshot.paramMap.get.and.returnValue('tennis');
      cmsService.getFeatureConfig.and.returnValue(of({ 16: false,ScoreboardsDataDisclaimer:{enabled: true, dataDisclaimer:'test'} }));

      component.ngOnInit();
      tick();

      expect(component.showNewUserTabs).toBeTruthy();
    }));

    it(`should Not show New User Tabs if Not ScoreboardsSports for this sport`, fakeAsync(() => {
      activatedRoute.snapshot.paramMap.get.and.returnValue('tennis');
      cmsService.getSystemConfig.and.returnValue(of({}));

      component.ngOnInit();
      tick();

      expect(component.showNewUserTabs).toBeTruthy();
    }));

    describe('fallbackScoreboardType', () => {
      it('should be set from getScoreType', fakeAsync(() => {
        scoreParserService.getScoreType.and.returnValue('foo');

        component.ngOnInit();
        tick();

        expect(scoreParserService.getScoreType).toHaveBeenCalledWith('16');
        expect(component.fallbackScoreboardType).toEqual('foo');
      }));
    });


    it('ngOnInit-storage Service ShowSignposting to Be True', () => {
      storageService = {
        set: jasmine.createSpy('storageService.set'),
        get: jasmine.createSpy('storageService.get').and.returnValue([{"eventId":"11","betIds":[3]},{"eventId":"2","betIds":[4]}]),
      };
      activatedRoute.snapshot.paramMap.get.and.returnValue(11);
      component.ngOnInit();
      expect(component['showSignPosting']).toEqual(true);  
    }); 


    it('should show new tabs if sport is football ', fakeAsync(() => {
      activatedRoute.snapshot.paramMap.get.and.returnValue('football');
      cmsService.getSystemConfig.and.returnValue(of({}));

      component.ngOnInit();
      tick();

      expect(component.showNewUserTabs).toBeTruthy();
    }));

    it('should throw error if eventEntity is not defined', () => {
      timeService.formatByPattern.and.callFake(() => component.eventEntity = null);
      expect(fakeAsync(() => {
        component.ngOnInit();
        tick();
      })).toThrowError();
    });
    it('should call eventAutoSeoData', fakeAsync(() => {
      spyOn(component, 'eventAutoSeoData').and.callThrough();
      component.ngOnInit();
      tick();
      expect(component.eventAutoSeoData).toHaveBeenCalled();
    })); 
  });

  describe('ngAfterViewInit', () => {
    let changes, getChangesSpy;
    beforeEach(() => {
      changes = new Subject();
      getChangesSpy = jasmine.createSpy('get changes').and.returnValue(changes);
      component.nativeVideoPlayerPlaceholderRef = {};
      Object.defineProperty(component.nativeVideoPlayerPlaceholderRef, 'changes', { get: getChangesSpy });
    });
    it('should do nothing for non-wrapper', () => {
      nativeBridgeService.isWrapper = false;
      component.ngAfterViewInit();
      expect(getChangesSpy).not.toHaveBeenCalled();
    });
    describe('for wrapper should subscribe on ViewChildren changes and', () => {
      let refs;
      const oldEl = Symbol('oldEl') as any, newEl = Symbol('newEl') as any;
      beforeEach(() => {
        refs = { first: { nativeElement: newEl } };
        nativeBridgeService.isWrapper = true;
        (component as any).nativeVideoPlayerPlaceholder = oldEl;
        component.ngAfterViewInit();
      });
      it('update nativeVideoPlayerPlaceholder reference and call handleNativeVideoPlayer asynchronously', fakeAsync(() => {
        changes.next(refs);
        expect((component as any).nativeVideoPlayerPlaceholder).toEqual(oldEl);
        expect(nativeBridgeService.handleNativeVideoPlayer).not.toHaveBeenCalled();
        tick();
        expect((component as any).nativeVideoPlayerPlaceholder).toEqual(newEl);
        expect(nativeBridgeService.handleNativeVideoPlayer).toHaveBeenCalledWith(newEl);
      }));
      describe('not update nativeVideoPlayerPlaceholder reference and not call handleNativeVideoPlayer', () => {
        it('if no refs provided', () => {
          refs = null;
        });
        it('if refs does not have first item', () => {
          refs.first = null;
        });
        it('if refs first item does not have nativeElement', () => {
          refs.first.nativeElement = null;
        });
        it('if refs first item nativeElement is the same as nativeVideoPlayerPlaceholder', () => {
          refs.first.nativeElement = oldEl;
        });
        afterEach(fakeAsync(() => {
          changes.next(refs);
          tick();
          expect((component as any).nativeVideoPlayerPlaceholder).toEqual(oldEl);
          expect(nativeBridgeService.handleNativeVideoPlayer).not.toHaveBeenCalled();
        }));
      });
      afterEach(() => {
        expect(getChangesSpy).toHaveBeenCalled();
      });
    });
  });

  describe('#getIsEnhancedMultiplesEnabled', () => {
    it('isEnhancedMultiplesEnabled true', () => {
      component['getIsEnhancedMultiplesEnabled']().subscribe((value) => {
        expect(value).toBeTruthy();
      });
      expect(cmsService.getToggleStatus).toHaveBeenCalledWith('EnhancedMultiples');
    });

    it('isEnhancedMultiplesEnabled false', () => {
      cmsService.getToggleStatus = jasmine.createSpy().and.returnValue(of(false));
      component['getIsEnhancedMultiplesEnabled']().subscribe((value) => {
        expect(value).toBeFalsy();
      });
      expect(cmsService.getToggleStatus).toHaveBeenCalledWith('EnhancedMultiples');
    });
  });

  describe('@isEventTitleBarAvailable', () => {
    beforeEach(() => {
      component.isIMGScoreboardAvailable = false;
      component.isOptaScoreboardChecked = true;
    });

    it('event title bar should be available if opta checked and not available and bgScoreboard is not available', () => {
      component.optaScoreboardAvailable = false;
      component.bgScoreboardConfig = {
        available: false
      };
      expect(component.isEventTitleBarAvailable()).toBeTruthy();
    });

    it('event title bar should not be available if opta checked and not available but bgScoreboard is available', () => {
      component.optaScoreboardAvailable = false;
      component.bgScoreboardConfig = {
        available: true
      };
      expect(component.isEventTitleBarAvailable()).toBeFalsy();
    });

    it('event title bar should not be available if opta available', () => {
      component.optaScoreboardAvailable = true;
      component.bgScoreboardConfig = {
        available: false
      };
      expect(component.isEventTitleBarAvailable()).toBeFalsy();
    });

    it('event title bar should be available if IMG available', () => {
      component.isIMGScoreboardAvailable = true;
      expect(component.isEventTitleBarAvailable()).toBeTruthy();
    });
  });

  describe('isLoadedHandler', () => {
    it(`should set 'isScoreLoaded' property`, () => {
      component.isLoadedHandler(true);

      expect(component.isScoreLoaded).toBeTruthy();
    });
  });

  describe('isLoading', () => {
    describe('should return True if data loaded and', () => {
      it(` optaScoreboardAvailable`, () => {
        component.optaScoreboardAvailable = true;
        component.isScoreLoaded = false;
        component.isOptaScoreboardChecked = true;
      });

      it(`gpScoreboardAvailable`, () => {
        component.gpScoreboardAvailable = true;
        component.isScoreLoaded = false;
        component.isOptaScoreboardChecked = true;
      });

      it(`does Not gpScoreboardAvailable`, () => {
        component.gpScoreboardAvailable = false;
        component.isOptaScoreboardChecked = false;
      });

      it(`does Not gpScoreboardAvailable`, () => {
        component.optaScoreboardAvailable = false;
        component.isOptaScoreboardChecked = false;
      });

      afterEach(() => {
        expect(component.isLoading()).toBeTruthy();
      });
    });

    describe('should return False if', () => {
      describe('optaScoreboardAvailable', () => {
        it(`optaScoreboardAvailable`, () => {
          component.optaScoreboardAvailable = true;
          component.isScoreLoaded = true;
          component.isOptaScoreboardChecked = false;
        });

        it(`isOptaScoreboardChecked equal false`, () => {
          component.optaScoreboardAvailable = true;
          component.isScoreLoaded = false;
          component.isOptaScoreboardChecked = false;
        });

        it(`isScoreLoaded equal true`, () => {
          component.optaScoreboardAvailable = true;
          component.isScoreLoaded = true;
          component.isOptaScoreboardChecked = false;
        });

        it(`equal False and isOptaScoreboardChecked`, () => {
          component.gpScoreboardAvailable = false;
          component.isOptaScoreboardChecked = true;
        });
      });

      describe('gpScoreboardAvailable', () => {
        it(`gpScoreboardAvailable`, () => {
          component.gpScoreboardAvailable = true;
          component.isScoreLoaded = true;
          component.isOptaScoreboardChecked = false;
        });

        it(`gpScoreboardAvailable equal false`, () => {
          component.gpScoreboardAvailable = true;
          component.isScoreLoaded = false;
          component.isOptaScoreboardChecked = false;
        });

        it(`gpScoreboardAvailable equal true`, () => {
          component.gpScoreboardAvailable = true;
          component.isScoreLoaded = true;
          component.isOptaScoreboardChecked = false;
        });

        it(`equal False and gpScoreboardAvailable`, () => {
          component.gpScoreboardAvailable = false;
          component.isOptaScoreboardChecked = true;
        });
      });
      afterEach(() => {
        expect(component.isLoading()).toBeFalsy();
      });
    });
  });

  describe('@isMarketsTabAvailable', () => {

    describe('show New User Tabs', () => {
      beforeEach(() => {
        component.showNewUserTabs = true;
      });

      it(`should return True if 'isLoggedIn' and 'myBetsAvailable are equal true`, () => {
        component.isLoggedIn = true;
        component.myBetsAvailable = true;

        expect(component.isMarketsTabAvailable()).toBeTruthy();
      });

      it(`should return False if 'isLoggedIn' is equal false`, () => {
        component.isLoggedIn = false;
        component.myBetsAvailable = true;

        expect(component.isMarketsTabAvailable()).toBeFalsy();
      });

      it(`should return False if 'myBetsAvailable' is equal false`, () => {
        component.isLoggedIn = true;
        component.myBetsAvailable = false;

        expect(component.isMarketsTabAvailable()).toBeFalsy();
      });      
    });

    describe('do Not show New User Tabs', () => {
      beforeEach(() => {
        component.showNewUserTabs = false;
      });

      it(`should return True if 'isLoggedIn' and 'myBetsAvailable are true and 'liveStreamAvailable' is false`, () => {
        component['eventEntity'] = { liveStreamAvailable: false };
        component.isLoggedIn = true;
        component.myBetsAvailable = true;

        expect(component.isMarketsTabAvailable()).toBeTruthy();
      });

      it(`should return False if 'isLoggedIn' and 'liveStreamAvailable' is equal false`, () => {
        component['eventEntity'] = { liveStreamAvailable: false };
        component.isLoggedIn = false;
        component.myBetsAvailable = true;

        expect(component.isMarketsTabAvailable()).toBeFalsy();
      });

      it(`should return False if 'myBetsAvailable' and 'liveStreamAvailable' is equal false`, () => {
        component['eventEntity'] = { liveStreamAvailable: false };
        component.isLoggedIn = true;
        component.myBetsAvailable = false;

        expect(component.isMarketsTabAvailable()).toBeFalsy();
      });
    });
  });

  describe('@isEventTitleBarAvailable', () => {

    it('eventTitleBar should be available', () => {
      component.isOptaScoreboardChecked = true;
      component.optaScoreboardAvailable = false;
      component.bgScoreboardConfig.available = false;
      expect(component.isEventTitleBarAvailable()).toBeTruthy();
    });

    it('eventTitleBar shouldn`t be available', () => {
      component.isLoggedIn = false;
      component.myBetsAvailable = true;
      component.liveStreamAvailable = true;
      expect(component.isEventTitleBarAvailable()).toBeFalsy();
    });
  });

  describe('@onFootballBellClick', () => {
    it('call function click on notification bell icon', () => { 
      component.eventEntity = {categoryId: '16'}
      component.eventId = '12345';
      component.sportName = 'horseracing';
      component.eventData = {
          event: [
          {
            drilldownTagNames: 'EVFLAG_FE,EVFLAG_PVM,EVFLAG_NE,EVFLAG_BL,'
          }
        ]
      };
      component.onFootballBellClick();

      expect(component.nativeBridgeService.onEventAlertsClick)
        .toHaveBeenCalledWith(
          component.eventId,
          component.sportName,
          component.sport.config.request.categoryId,
          component.eventData.event[0].drilldownTagNames,
          ALERTS_GTM.EVENT_SCREEN);

      // TODO: Reverted changes from BMA-37049. Will be removed after new approach implementation.
      expect(component.nativeBridgeService.showFootballAlerts).toHaveBeenCalled();
      // TODO END
    }); 
  });

  describe('ngOnDestroy', () => {
    beforeEach(() => {
      component.ngOnInit();
    });

    it('@ngOnDestroy', () => {
      component.sport.unSubscribeEDPForUpdates = jasmine.createSpy('unSubscribeEDPForUpdates');
      component.eventEntity = { startTime: '2019-01-02T22:04:00' };
      component['messageListener'] = jasmine.createSpy('messageListener');
      component['myBetsRef'] = { destroy: jasmine.createSpy('destroy') };
      component.ngOnDestroy();
      expect(component.sport.unSubscribeEDPForUpdates).toHaveBeenCalledTimes(1);
      expect(pubSubService.unsubscribe).toHaveBeenCalledTimes(1);
      expect(pubSubService.publish).toHaveBeenCalledWith('SPORT_EDP_CLOSED');
      expect(sportEventPageProviderService.sportData.next).toHaveBeenCalledTimes(1);
      expect(windowRef.document.removeEventListener).toHaveBeenCalledTimes(2);

      // TODO: Reverted changes from BMA-37049. Will be removed after new approach implementation.
      expect(windowRef.nativeWindow.removeEventListener).toHaveBeenCalledTimes(1);
      // TODO END

      expect(component['messageListener']).toHaveBeenCalledTimes(1);
      expect(component['myBetsRef'].destroy).toHaveBeenCalledTimes(1);
    });

    it('should emit connect and pubsub events', () => {
      component.ngOnDestroy();

      expect(pubSubService.publish).toHaveBeenCalledWith('CASHOUT_CTRL_STATUS', {
        ctrlName: 'eventCashoutAndPlacedBets',
        isDestroyed: true
      });
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('sportEventMain');
    });

    it('should window event listeners', () => {
      component.ngOnDestroy();

      expect(windowRef.document.removeEventListener).toHaveBeenCalledWith('CURRENT_WATCH_LIVE_STATE_CHANGED',
        jasmine.any(Function));
      expect(windowRef.document.removeEventListener).toHaveBeenCalledWith('eventAlertsEnabled',
        jasmine.any(Function));

      // TODO: Reverted changes from BMA-37049. Will be removed after new approach implementation.
      expect(windowRef.nativeWindow.removeEventListener).toHaveBeenCalledWith('CURRENT_FOOTBALL_ALERTS_STATE_CHANGED',
        jasmine.any(Function));
      // TODO END
    });

    it('should close cashout stream on destroy', () => {
      component['betsStreamOpened'] = true;
      component['initDataSubscription'] = null;
      component.ngOnDestroy();

      expect(commandService.executeAsync).toHaveBeenCalledWith(commandService.API.CLOSE_CASHOUT_STREAM);
      expect(component['betsStreamOpened']).toBeFalsy();

    });

    it('should unsubscribe on initData subscription on destroy', () => {
      spyOn(component['initDataSubscription'], 'unsubscribe').and.callThrough();

      component.ngOnDestroy();

      expect(component.initDataSubscription.unsubscribe).toHaveBeenCalled();
    });
  });

  describe('@ngOnDestroy eventVideoStreamSubscriber', () => {
    beforeEach(() => {
      component.sport.getById.and.returnValue(of({
        event: [{ startTime: '2019-01-02T22:04:00', categoryId: '16', liveStreamAvailable: true, name: 'Ashleigh Barty* v Saisai Zheng' }]
      }));
      component.eventEntity = { startTime: '2019-01-02T22:04:00', categoryId: '16' };
    });

    it('@ngOnDestroy unsubscribe from eventVideoStreamSubscriber', fakeAsync(() => {
      component.ngOnInit();
      tick();
      spyOn(component.eventVideoStreamSubscriber, 'unsubscribe');

      component.ngOnDestroy();
      expect(component.eventVideoStreamSubscriber.unsubscribe).toHaveBeenCalled();
    }));
  });

  describe('SUCCESSFUL_LOGIN connect', () => {
    beforeEach(() => {
      component.sport.getById.and.returnValue(of({
        event: [{ startTime: '2019-01-02T22:04:00', categoryId: '16', liveStreamAvailable: true, name: 'Ashleigh Barty* v Saisai Zheng' }]
      }));
    });

    it('should listen to view type change ', fakeAsync(() => {
      component.ngOnInit();
      tick();

      successfulLoginHandler();

      expect(component.streamShown).toBeFalsy();
      expect(component.isLoggedIn).toBeFalsy();
      expect(nativeBridgeService.hideVideoStream).toHaveBeenCalled();
    }));

    it('should listen to view type change, isStreamBetAvailable is true', fakeAsync(() => {
      eventVideoStreamProviderService.isStreamBetAvailable.and.returnValue(true);
      component.ngOnInit();
      tick();

      successfulLoginHandler();

      expect(component.streamShown).toBeFalsy();
      expect(component.isLoggedIn).toBeFalsy();
      expect(nativeBridgeService.hideVideoStream).toHaveBeenCalled();
    }));
  });

  describe('@playStream', () => {
    beforeEach(() => {
      component.sport.getById.and.returnValue(of({
        event: [{ startTime: '2019-01-02T22:04:00', categoryId: '16', liveStreamAvailable: true, name: 'Ashleigh Barty* v Saisai Zheng' }]
      }));
    });

    it('should toggle Video Stream Area', fakeAsync(() => {
      const event = {
        preventDefault: jasmine.createSpy('preventDefault')
      };

      (component as any).nativeVideoPlayerPlaceholder = Symbol('element') as any;
      component.ngOnInit();
      tick();
      spyOn(eventVideoStreamProviderService.playListener, 'next');

      component.playStream(event);

      expect(component.streamShown).toBeTruthy();
      expect(event.preventDefault).toHaveBeenCalled();
      expect(eventVideoStreamProviderService.playListener.next).toHaveBeenCalled();
      component['deviceService'].isWrapper = true;
      component.playStream(event);
      expect(nativeBridgeService.handleNativeVideoPlaceholder).toHaveBeenCalledWith(false, (component as any).nativeVideoPlayerPlaceholder);
    }));
  });

  describe('@onPlayLiveStreamError', () => {
    it('should onPlayLiveStreamError', () => {
      component.onPlayLiveStreamError();

      expect(component.streamShown).toBeFalsy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('@prepareEventVisualization', () => {
    beforeEach(() => {
      spyOn<any>(component, 'loadVisualization').and.callThrough();
    });

    describe('when eventEntity.eventIsLive', () => {
      beforeEach(() => {
        component.eventEntity = { eventIsLive: true };
      });

      describe('should set isOptaScoreboardChecked to true', () => {
        beforeEach(() => {
          component.isOptaScoreboardChecked = false;
        });

        it('if visualisztion is switched off in CMS', () => {
          spyOn(component, 'visualizationCmsGuard').and.returnValue(EMPTY);
          component['prepareEventVisualization']();
        });

        it('if visualisztion is not switched off in CMS', () => {
          component['prepareEventVisualization']();
        });

        afterEach(() => {
          expect(component.isOptaScoreboardChecked).toBeTruthy();
        });
      });

      describe('it should load configured visualization', () => {
        it('with default load order (football)', () => {
          component.sportName = 'football';
          component['prepareEventVisualization']();
          expect(component['loadVisualization']).toHaveBeenCalledWith(SCOREBOARDS_LOAD_ORDER.default);
        });

        it('with specific load order (tennis)', () => {
          component.sportName = 'tennis';
          component['prepareEventVisualization']();
          expect(component['loadVisualization']).toHaveBeenCalledWith(SCOREBOARDS_LOAD_ORDER.tennis);
        });

        it('with load order with come items being excluded (football without OPTA and IMG)', () => {
          component.sportName = 'football';
          component['prepareEventVisualization'](['OPTA', 'IMG', 'BG']);
          expect(component['loadVisualization']).toHaveBeenCalledWith(['OPTA', 'IMG', 'BG']);
        });
      });
    });

    describe('when not eventEntity.eventIsLive', () => {
      beforeEach(() => {
        component.eventEntity = { eventIsLive: false };
      });

      it('it should try loading OPTA, then PreMatch', () => {
        component.sportName = 'tennis';
        component['prepareEventVisualization']();
        expect(component['loadVisualization']).toHaveBeenCalledWith(['OPTA', 'PM']);
      });
    });

    describe('should check whether visualisation/scoreboards is disabled in CMS for current sport', () => {
      beforeEach(() => {
        component.eventEntity = { categoryId: '16' };
      });

      it('and not call the loaders if scoreboards/visualization is disabled for current sport', () => {
        cmsService.getSystemConfig.and.returnValue(of({ VisualisationDisabledCategory: { 16: true } }));
        component['prepareEventVisualization'](['IMG', 'BG']);
        expect(component['loadVisualization']).not.toHaveBeenCalled();
      });

      describe('and call the configured loaders if visualization disabling config', () => {
        beforeEach(() => {
          component['imgLoader'] = jasmine.createSpy('imgLoader').and.returnValue(EMPTY);
          component['betGeniusLoader'] = jasmine.createSpy('betGeniusLoader').and.callFake(config => of(config));
        });

        it('is not applied for current sport', () => {
          cmsService.getSystemConfig.and.returnValue(of({ VisualisationDisabledCategory: { 16: false } }));
        });
        it('is not defined for current sport', () => {
          cmsService.getSystemConfig.and.returnValue(of({ VisualisationDisabledCategory: { 18: true } }));
        });
        it('is not defined', () => {
          cmsService.getSystemConfig.and.returnValue(of({ }));
        });
        it('is not available', () => {
          cmsService.getSystemConfig.and.returnValue(of(null));
        });
        afterEach(() => {
          component['prepareEventVisualization'](['IMG', 'BG']);
          expect(component['loadVisualization']).toHaveBeenCalledWith(['IMG', 'BG']);
          expect(component['imgLoader']).toHaveBeenCalledTimes(1);
          expect(component['betGeniusLoader']).not.toHaveBeenCalled();
        });
      });

      afterEach(() => {
        expect(cmsService.getSystemConfig).toHaveBeenCalled();
      });
    });
  });

  describe('@getSportScoreboardsLoadOrder', () => {
    describe('for live event', () => {
      beforeEach(() => {
        component.eventEntity = { eventIsLive: true };
      });
      it('should return specific list of scoreboard ids if there is mapping for current sport', () => {
        component.sportName = 'tennis';
        expect(component['getSportScoreboardsLoadOrder']()).toEqual(SCOREBOARDS_LOAD_ORDER.tennis);
      });
      it('should return default list of scoreboard ids if there is no specific mapping for current sport', () => {
        component.sportName = 'football';
        expect(component['getSportScoreboardsLoadOrder']()).toEqual(SCOREBOARDS_LOAD_ORDER.default);
      });
    });

    it('for pre-match event should return fixed list of ids', () => {
      component.eventEntity = { eventIsLive: false };
      expect(component['getSportScoreboardsLoadOrder']()).toEqual(['OPTA', 'PM']);
    });
  });

  describe('scoreboardsLoadOrder', () => {
    it('should have the load order of scoreboard properly defined per sport', () => {
      expect(component['scoreboardsLoadOrder']).toEqual(SCOREBOARDS_LOAD_ORDER);
    });
  });

  it('ngOnDestoy', () => {
    component.ngOnDestroy();

    expect(pubSubService.publish).toHaveBeenCalledTimes(3);
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('sportEventMain');
  });

  describe('@loadVisualization', () => {
    beforeEach(() => {
      component.sport = {
        getScoreboardConfig: jasmine.createSpy().and.returnValue({ type: 'mockConfig' })
      };

      component['preMatchLoader'] = jasmine.createSpy('preMatchLoader').and.callFake(config => of(config));
      component['optaLoader'] = jasmine.createSpy('optaLoader').and.callFake(config => of(config));
      component['imgLoader'] = jasmine.createSpy('imgLoader').and.callFake(config => of(config));
      component['imgArenaLoader'] = jasmine.createSpy('imgArenaLoader').and.callFake(config => of(config));
      component['fallbackScoreboardLoader'] = jasmine.createSpy('fallbackScoreboardLoader').and.callFake(config => of(config));
      component['betGeniusLoader'] = jasmine.createSpy('betGeniusLoader').and.callFake(config => of(config));
      component['betRadarLoader'] = jasmine.createSpy('betRadarLoader').and.callFake(config => of(config));
      component['grandParadeLoader'] = jasmine.createSpy('grandParadeLoader').and.callFake(config => of(config));
    });

    it('should return an observable', done => {
      const result = component['loadVisualization']([]);
      expect(result).toEqual(jasmine.any(Observable));
      result.subscribe(data => {
        expect(component.sport.getScoreboardConfig).toHaveBeenCalled();
        expect(data).toEqual({ type: 'mockConfig' });
        done();
      });
    });

    it('should use {} if sport.getScoreboardConfig does not return a proper value', done => {
      component.sport.getScoreboardConfig.and.returnValue(null);
      component['loadVisualization']().subscribe(data => {
        expect(component.sport.getScoreboardConfig).toHaveBeenCalled();
        expect(data).toEqual({});
        done();
      });
    });

    it('should return observable of config data if no loaders list is provided', done => {
      component['loadVisualization']().subscribe(data => {
        expect(data).toEqual({ type: 'mockConfig' });
        done();
      });
      expect(component['preMatchLoader']).not.toHaveBeenCalled();
      expect(component['imgLoader']).not.toHaveBeenCalled();
      expect(component['imgArenaLoader']).not.toHaveBeenCalled();
      expect(component['fallbackScoreboardLoader']).not.toHaveBeenCalled();
      expect(component['grandParadeLoader']).not.toHaveBeenCalled();
      expect(component['optaLoader']).not.toHaveBeenCalled();
      expect(component['betGeniusLoader']).not.toHaveBeenCalled();
      expect(component['betRadarLoader']).not.toHaveBeenCalled();
    });

    it('should build observable chain based on provided loaders order', () => {
      component['loadVisualization'](['IMG','IMG_ARENA','FS', 'UNKNOWN_ID', 'GP~', 'OPTA']).subscribe();
      expect(component['preMatchLoader']).not.toHaveBeenCalled();
      expect(component['imgLoader']).toHaveBeenCalledWith({ type: 'mockConfig' });
      expect(component['imgArenaLoader']).toHaveBeenCalledWith({ type: 'mockConfig' });
      expect(component['fallbackScoreboardLoader']).toHaveBeenCalledWith({ type: 'mockConfig' });
      expect(component['grandParadeLoader']).toHaveBeenCalledWith({ type: 'mockConfig' });
      expect(component['optaLoader']).toHaveBeenCalledWith({ type: 'mockConfig' });
      expect(component['betGeniusLoader']).not.toHaveBeenCalled();
      expect(component['betRadarLoader']).not.toHaveBeenCalled();
    });

    describe('when loader observable returns EMPTY', () => {
      beforeEach(() => {
        component['grandParadeLoader'].and.returnValue(EMPTY);
        component['preMatchLoader'].and.returnValue(EMPTY);
      });

      it('should interrupt search sequence if loader id does not end with ~', () => {
        component['fallbackScoreboardLoader'].and.returnValue(EMPTY);
        component['loadVisualization'](['IMG', 'FS', 'BG', 'BR', 'GP', 'OPTA']).subscribe();
        expect(component['betGeniusLoader']).not.toHaveBeenCalled();
        expect(component['betRadarLoader']).not.toHaveBeenCalled();
        expect(component['grandParadeLoader']).not.toHaveBeenCalled();
      });

      it('should continue further search sequence if loader id ends with ~', () => {
        component['loadVisualization'](['IMG', 'FS~', 'BG', 'BR', 'GP', 'OPTA']).subscribe();
        expect(component['betGeniusLoader']).toHaveBeenCalledWith({ type: 'mockConfig' });
        expect(component['betRadarLoader']).toHaveBeenCalledWith({ type: 'mockConfig' });
        expect(component['grandParadeLoader']).toHaveBeenCalledWith({ type: 'mockConfig' });
      });

      it('should interrupt search sequence on success event if further loaders end with ~', () => {
        component['loadVisualization'](['FS~', 'IMG', 'PM', 'GP~', 'BG~', 'BR~', 'OPTA']).subscribe();
        expect(component['preMatchLoader']).toHaveBeenCalledWith({ type: 'mockConfig' });
        expect(component['grandParadeLoader']).not.toHaveBeenCalled();
        expect(component['betGeniusLoader']).not.toHaveBeenCalled();
        expect(component['betRadarLoader']).not.toHaveBeenCalled();
      });

      afterEach(() => {
        expect(component['imgLoader']).toHaveBeenCalledWith({ type: 'mockConfig' });
        expect(component['fallbackScoreboardLoader']).toHaveBeenCalledWith({ type: 'mockConfig' });
        expect(component['optaLoader']).not.toHaveBeenCalled();
      });
    });
  });

  describe('@updateCashoutBets', () => {
    it('should update bet type of each element in list if its betId is equal to provided value', () => {
      const mockList = [ { betId: 'i1' }, { betId: 'i2' }, { betId: 'i3' } ];
      component['updateCashoutBets'](mockList, 'i2');
      expect(mockList).toEqual([
        { betId: 'i1' },
        { betId: 'i2', type: 'placedBetsWithoutCashoutPossibility' },
        { betId: 'i3' }
      ] as any);
    });

    it('should not fail if provided list is undefined', done => {
      component['updateCashoutBets'](undefined, 'i2');
      done();
    });

    it('should not fail if provided list is null', (done) => {
      component['updateCashoutBets'](null, 'i2');
      done();
    });
  });

  describe('scoreboard loaders', () => {
    let mockConfig;

    beforeEach(() => {
      mockConfig = { type: 'mockConfig', config: {} };
      component.eventEntity = { eventIsLive: true, categoryId: '16', id: '123456' } as any;
    });

    describe('@preMatchLoader', () => {
      it('should return observable', () => {
        expect(component['preMatchLoader'](mockConfig)).toEqual(jasmine.any(Observable));
      });

      describe('should make call to visEventService.checkPreMatchWidgetAvailability', () => {
        describe('and on success', () => {
          beforeEach(() => {
            component.eventId = '123456';
            visEventService.checkPreMatchWidgetAvailability.and.returnValue(of(true));
          });

          it('should return EMPTY and set params for PreMatchWidget', () => {
            const nextSpy = jasmine.createSpy('next'),
              completeSpy = jasmine.createSpy('complete');
            component['preMatchLoader'](mockConfig).subscribe(nextSpy, null, completeSpy);
            expect(nextSpy).not.toHaveBeenCalled();
            expect(completeSpy).toHaveBeenCalled();

            expect(component.preMatchWidgetAvailable).toEqual(true);
          });
        });
        describe('and on failure', () => {
          beforeEach(() => {
            component.eventId = '123456';
            visEventService.checkPreMatchWidgetAvailability.and.returnValue(throwError(null));
          });

          it('should return observable of provided config', () => {
            const nextSpy = jasmine.createSpy('next');
            component['preMatchLoader'](mockConfig).subscribe(nextSpy);
            expect(nextSpy).toHaveBeenCalledWith(mockConfig);
            expect(component.preMatchWidgetAvailable).toEqual(undefined);
          });
        });
        afterEach(() => {
          expect(visEventService.checkPreMatchWidgetAvailability).toHaveBeenCalledWith('123456');
        });
      });
    });

    describe('@fallbackScoreboardLoader', () => {
      beforeEach(() => {
        component.sysConfig = { FallbackScoreboard: { enabled: true, Simple: '16', SetsGamesPoints: '34' } };
        component.eventEntity = { originalName: 'Original Name', startTime: '2019-01-02T22:04:00', categoryId: '16' };
      });

      it('should return observable', () => {
        const observable = component['fallbackScoreboardLoader'](mockConfig);
        expect(observable).toEqual(jasmine.any(Observable));
        observable.subscribe(data => expect(data).toEqual(mockConfig));
      });

      describe('should set isFallbackScoreboards to', () => {
        let returnedValue;
        it('true if scoreParserService.parseScores could parse the event name', () => {
          returnedValue = { value: 'not-a-false' };
        });

        it('false if scoreParserService.parseScores did not parse the event name', () => {
          returnedValue = null;
        });

        afterEach(() => {
          scoreParserService.parseScores.and.returnValue(returnedValue);
          component['fallbackScoreboardLoader'](mockConfig);
          expect(component.isFallbackScoreboards).toEqual(!!returnedValue);
          expect(scoreParserService.parseScores).toHaveBeenCalledWith('Original Name', 'Simple');
        });
      });

      describe('should not enable fallback scoreboards', () => {
        it('if sysConfig does not exist', () => {
          component.sysConfig = null;
        });
        it('if FallbackScoreboard is not defined in sysConfig', () => {
          component.sysConfig = {};
        });
        it('if FallbackScoreboard is not enabled in sysConfig', () => {
          component.sysConfig = { FallbackScoreboard: { enabled: false } };
        });

        afterEach(() => {
          component['fallbackScoreboardLoader']({ type: 'mockConfig' });
          expect(component.fallbackScoreboardType).toBeUndefined();
        });
      });

      describe('if FallbackScoreboard is enabled in sysConfig', () => {
        it('fallbackScoreboardType should be set according to sport category matched with system config entries', () => {
          component['fallbackScoreboardLoader']({ type: 'mockConfig' });
          expect(component.fallbackScoreboardType).toEqual('Simple');
          component.eventEntity.categoryId = '34';
          component['fallbackScoreboardLoader']({ type: 'mockConfig' });
          expect(component.fallbackScoreboardType).toEqual('SetsGamesPoints');
        });

        it('fallbackScoreboardType should be left as undefined if event categoryId is not matched with system config', () => {
          component.eventEntity.categoryId = '14';
          component['fallbackScoreboardLoader']({ type: 'mockConfig' });
          expect(component.fallbackScoreboardType).toBeUndefined();
        });
      });
    });

    it('should return observable of config if no fallback comments teams', fakeAsync(() => {
      component.sysConfig = null;
      component.eventEntity = { comments: { teams: null } };
      scoreParserService.parseScores.and.returnValue(false);

      component['fallbackScoreboardLoader'](mockConfig).subscribe((data) => {
        expect(data).toEqual(mockConfig);
      });
      tick();
    }));

    it('should return observable of config if no fallback scoreboards', fakeAsync(() => {
      component.sysConfig = null;
      component.eventEntity = { comments: null };
      scoreParserService.parseScores.and.returnValue(false);

      component['fallbackScoreboardLoader'](mockConfig).subscribe((data) => {
        expect(data).toEqual(mockConfig);
      });
      tick();
    }));

    it('should return EMPTY if fallback scoreboards', () => {
      component.sysConfig = null;
      component.eventEntity = { comments: { teams: {} } };

      const result = component['fallbackScoreboardLoader'](mockConfig);
      expect(result).toEqual(EMPTY);
    });

    describe('@imgLoader', () => {
      it('should return observable', () => {
        expect(component['imgLoader'](mockConfig)).toEqual(jasmine.any(Observable));
      });

      describe('should make call to get visualization params', () => {
        describe('and if response contains applicable data', () => {
          beforeEach(() => {
            visDataHandler.init.and.returnValue(of({ eventsWithVisualizationParams: [{ data: 'params' }] }));
          });

          it('should return EMPTY and set params for IMG visualization', () => {
            const nextSpy = jasmine.createSpy('next'),
              completeSpy = jasmine.createSpy('complete');
            component['imgLoader'](mockConfig).subscribe(nextSpy, null, completeSpy);
            expect(nextSpy).not.toHaveBeenCalled();
            expect(completeSpy).toHaveBeenCalled();

            expect(component['isIMGScoreboardAvailable']).toEqual(true);
            expect(component.eventsWithVisualizationParams).toEqual([{ data: 'params' }]);
          });
        });

        describe('should return observable of provided config and set default values for IMG visualization', () => {
          it('if response data contains empty array', () => {
            visDataHandler.init.and.returnValue(of({ eventsWithVisualizationParams: [] }));
          });

          it('if response does not have eventsWithVisualizationParams property', () => {
            visDataHandler.init.and.returnValue(of({ }));
          });

          it('if response is empty', () => {
            visDataHandler.init.and.returnValue(of(null));
          });

          it('if error occurred', () => {
            visDataHandler.init.and.returnValue(throwError(null));
          });

          afterEach(() => {
            const nextSpy = jasmine.createSpy('next');
            component['imgLoader'](mockConfig).subscribe(nextSpy);
            expect(nextSpy).toHaveBeenCalledWith(mockConfig);

            expect(component['isIMGScoreboardAvailable']).toEqual(false);
            expect(component.eventsWithVisualizationParams).toEqual([]);
          });
        });

        afterEach(() => {
          expect(visDataHandler.init).toHaveBeenCalledWith(component.eventEntity);
        });
      });
    });

    describe('@optaLoader', () => {
      it('should return observable', () => {
        expect(component['optaLoader'](mockConfig)).toEqual(jasmine.any(Observable));
      });

      describe('should make call to checkOptaScoreboardAvailability', () => {
        describe('and if response is resolved succesfully', () => {
          it('should return EMPTY and set params for OPTA scoreboard', () => {
            const nextSpy = jasmine.createSpy('next'),
              completeSpy = jasmine.createSpy('complete');
            component['optaLoader'](mockConfig).subscribe(nextSpy, null, completeSpy);
            expect(nextSpy).not.toHaveBeenCalled();
            expect(completeSpy).toHaveBeenCalled();

            expect(component['isOptaScoreboardChecked']).toEqual(true);
            expect(component.optaScoreboardAvailable).toEqual(true);
            expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
          });
        });

        describe('and if error occurred', () => {
          beforeEach(() => {
            sportEventMainProviderService.checkOptaScoreboardAvailability.and.returnValue(throwError({}));
          });

          it('should return observable of provided config and set default values for OPTA scoreboard', () => {
            const nextSpy = jasmine.createSpy('next');
            component['optaLoader'](mockConfig).subscribe(nextSpy);
            expect(nextSpy).toHaveBeenCalledWith(mockConfig);

            expect(component.optaScoreboardAvailable).toEqual(false);
          });
        });

        afterEach(() => {
          expect(sportEventMainProviderService.checkOptaScoreboardAvailability).toHaveBeenCalledWith(component.eventEntity);
        });
      });
    });

    describe('@betGeniusLoader', () => {
      it('should return observable', () => {
        expect(component['betGeniusLoader'](mockConfig)).toEqual(jasmine.any(Observable));
      });

      describe('should check scorboardConfig.type', () => {
        describe('and if it is equal "betGenius"', () => {
          beforeEach(() => {
            mockConfig.type = 'betGenius';
            mockConfig.config.type = 'betGeniusConfig';
          });

          describe('should make call to CmsService.getMenuItems', () => {
            describe('and if response is resolved successfully', () => {
              beforeEach(() => {
                cmsService.getMenuItems.and.returnValue(of([
                  { categoryId: 34, showScoreboard: false },
                  { categoryId: 16, showScoreboard: true }
                ]));
              });
              it('should return EMPTY, pick config by categoryId and set params for BG scoreboard', () => {
                const nextSpy = jasmine.createSpy('next'),
                  completeSpy = jasmine.createSpy('complete');
                component['betGeniusLoader'](mockConfig).subscribe(nextSpy, null, completeSpy);
                expect(nextSpy).not.toHaveBeenCalled();
                expect(completeSpy).toHaveBeenCalled();

                expect(component.bgScoreboardConfig).toEqual({
                  available: true,
                  eventId: '123456'
                });
              });

              it('should return scoreboard config if BG is disabled in CMS', () => {
                const nextSpy = jasmine.createSpy('next'),
                  completeSpy = jasmine.createSpy('complete');

                cmsService.getMenuItems.and.returnValue(of([
                  { categoryId: 34, showScoreboard: false },
                  { categoryId: 16, showScoreboard: false }
                ]));
                component['betGeniusLoader'](mockConfig).subscribe(nextSpy, null, completeSpy);

                expect(nextSpy).toHaveBeenCalledWith(mockConfig);
                expect(completeSpy).toHaveBeenCalled();
                expect(component.bgScoreboardConfig).toEqual({
                  available: false,
                  eventId: '123456'
                });
              });
            });

            describe('should return observable of provided config and set default values for BG scoreboard', () => {
              it('if error occurred', () => {
                cmsService.getMenuItems.and.returnValue(throwError(null));
              });

              it('if returned CMS config items does not contain current categoryId', () => {
                cmsService.getMenuItems.and.returnValue(of([
                  { categoryId: 34, showScoreboard: false },
                  { categoryId: 19, showScoreboard: true }
                ]));
              });

              afterEach(() => {
                const nextSpy = jasmine.createSpy('next');
                component['betGeniusLoader'](mockConfig).subscribe(nextSpy);
                expect(nextSpy).toHaveBeenCalledWith(mockConfig);
                expect(component.bgScoreboardConfig).toEqual({ available: false });
              });
            });

            afterEach(() => {
              expect(cmsService.getMenuItems).toHaveBeenCalledWith();
            });
          });
        });

        describe('and if it is not equal "betGenius"', () => {
          it('should return observable of provided config leaving other properties untouched', () => {
            const oldBgScoreboardConfig = component.bgScoreboardConfig;
            const nextSpy = jasmine.createSpy('next');
            component['betGeniusLoader'](mockConfig).subscribe(nextSpy);
            expect(nextSpy).toHaveBeenCalledWith(mockConfig);
            expect(component.bgScoreboardConfig).toBe(oldBgScoreboardConfig);
            expect(component.bgScoreboardConfig).toEqual({ available: false });
          });
        });
      });
    });

  describe('@imgArenaLoader', () => {
    it('should return observable', () => {
      expect(component['imgArenaLoader'](mockConfig)).toEqual(jasmine.any(Observable));
    });
    describe('should make call to checkImgArenaScoreboardAvailability', () => {
      beforeEach(() => {
        sportEventMainProviderService.checkImgArenaScoreboardAvailability.and.returnValue(of(IMG_ARENA_EVENT_BYMAPPING));
      });
      describe('if response is resolved succesfully', () => {
        it('should return EMPTY and set img event id scoreboard details', () => {
          const nextSpy = jasmine.createSpy('next'),
            completeSpy = jasmine.createSpy('complete');
          component['imgArenaLoader'](mockConfig).subscribe(nextSpy, null, completeSpy);
          expect(nextSpy).not.toHaveBeenCalled();
          expect(completeSpy).toHaveBeenCalled();
          expect(component.imgFrontRowArena.available).toEqual(true);
          expect(component.imgEventDetails).toEqual("487:2:1:1");
        });
      });
      describe('and if error occurred', () => {
        beforeEach(() => {
          sportEventMainProviderService.checkImgArenaScoreboardAvailability.and.returnValue(throwError({}));
        });
        it('should return observable of provided config and set default values for IMG ARENA scoreboard', () => {
          component['imgArenaLoader'](mockConfig).subscribe();
          expect(component.imgFrontRowArena.available).toEqual(false);
        });
      });
      afterEach(() => {
        expect(sportEventMainProviderService.checkImgArenaScoreboardAvailability).toHaveBeenCalledWith(component.eventEntity);
      });
    });
  });

    describe('@betRadarLoader', () => {
      it('should return observable', () => {
        expect(component['betRadarLoader'](mockConfig)).toEqual(jasmine.any(Observable));
      });

      describe('should make call to checkBetradarAvailability', () => {
        beforeEach(() => {
            component.eventEntity = { id : '123456'};
            sportEventMainProviderService.checkBetradarAvailability.and.returnValue(of(BETRADAREVENTMAPPING));
        });
        describe('and if response is resolved succesfully', () => {
          it('should return EMPTY and set  betradar match id scoreboard', () => {
            const nextSpy = jasmine.createSpy('next'),
              completeSpy = jasmine.createSpy('complete');
            component['betRadarLoader'](mockConfig).subscribe(nextSpy, null, completeSpy);
            expect(nextSpy).not.toHaveBeenCalled();
            expect(completeSpy).toHaveBeenCalled();
            expect(component.brScoreboardConfig.available).toEqual(true);
            expect(component.brScoreboardConfig.eventId).toEqual('123456');
            expect(component.betRadarMatchId).toEqual(22537897);
          });
        });

        describe('and if error occurred', () => {
          beforeEach(() => {
            sportEventMainProviderService.checkBetradarAvailability.and.returnValue(throwError({}));
          });

          it('should return observable of provided config and set default values for BETRADAR scoreboard', () => {
            component['betRadarLoader'](mockConfig).subscribe();
            expect(component.brScoreboardConfig.available).toEqual(false);
          });
        });

        afterEach(() => {
          expect(sportEventMainProviderService.checkBetradarAvailability).toHaveBeenCalledWith(component.eventEntity);
        });
      });
    });

    describe('@grandParadeLoader', () => {
      beforeEach(() => {
        component.sysConfig.Scoreboard = { config: 'data-set-1' };
      });

      it('should always return observable of provided config', () => {
        const observable = component['grandParadeLoader'](mockConfig);
        const nextSpy = jasmine.createSpy('next');

        expect(observable).toEqual(jasmine.any(Observable));
        observable.subscribe(nextSpy);
        expect(nextSpy).toHaveBeenCalledWith(mockConfig);
      });

      describe('it should call @checkGrandParadeAvailability', () => {
        beforeEach(() => {
          component.isSpecialEvent = false;
          component.eventsWithVisualizationParams = [];
          coreTools.hasOwnDeepProperty.and.returnValue(true);
          component.sysConfig.Scoreboard = { showScoreboard: 'Yes' };
        });

        it('without any arguments', () => {
          component['checkGrandParadeAvailability'] = jasmine.createSpy('checkGrandParadeAvailability');
          component['grandParadeLoader'](mockConfig).subscribe();
          expect(component['checkGrandParadeAvailability']).toHaveBeenCalled();
        });

        describe('and set gpScoreboardAvailable property', () => {
          describe('to true', () => {
            it('when event is not special, live visualization is unavailable (empty) and scoreboards are enabled in CMS', () => {});
            it('when event is not special, live visualization is unavailable (no data) and scoreboards are enabled in CMS', () => {
              component.eventsWithVisualizationParams = null;
              component['checkGrandParadeAvailability']();
              expect(component.gpScoreboardAvailable).toEqual(true);
            });

            afterEach(() => {
              component['checkGrandParadeAvailability']();
              expect(component.gpScoreboardAvailable).toEqual(true);
            });
          });

          describe('to false', () => {
            it('when event is special', () => {
              component.isSpecialEvent = true;
            });
            it('when live visualization is unavailable', () => {
              component.eventsWithVisualizationParams = [{ params: 'params' }];
            });
            it('when CMS config does not have corresponding property', () => {
              coreTools.hasOwnDeepProperty.and.returnValue(false);
            });
            it('when scoreboards are disabled in CMS', () => {
              component.sysConfig.Scoreboard = { showScoreboard: 'No' };
            });

            afterEach(() => {
              component['checkGrandParadeAvailability']();
              expect(component.gpScoreboardAvailable).toEqual(false);
            });
          });
        });

        describe('and make cmsService.getMenuItems call', () => {
          it('if gpScoreboardAvailable is true', () => {
            component['checkGrandParadeAvailability']();
          });
          it('if called with forceUrlUpdate=true', () => {
            component.isSpecialEvent = true;
            component['checkGrandParadeAvailability'](true);
            expect(component.gpScoreboardAvailable).toEqual(false); // prove the condition
          });

          describe('on resolution of which scoreboardUrl should be updated', () => {
            beforeEach(() => {
              component.sysConfig.Scoreboard = { scoreboardUrl: 'sysconfig-url', showScoreboard: 'Yes' };
            });
            it('with scoreboardUrl for current categoryId if it is available and enabled in received config', () => {
              cmsService.getMenuItems.and.returnValue(of([
                { categoryId: 19, showScoreboard: true, scoreBoardUrl: 'greyhounds-url' },
                { categoryId: 16, showScoreboard: true, scoreBoardUrl: 'football-url' }
              ]));
              component['checkGrandParadeAvailability']();
              expect(component.scoreboardUrl).toEqual('football-url');
            });

            describe('with system config URL if it is defined', () => {
              it('when CMS MenuItems data does not contain item matched with current categoryId', () => {
                cmsService.getMenuItems.and.returnValue(of([
                  { categoryId: 19, showScoreboard: true, scoreBoardUrl: 'greyhounds-url' },
                  { categoryId: 34, showScoreboard: true, scoreBoardUrl: 'tennis-url' }
                ]));
              });
              it('when matched with current categoryId MenuItem does not have scoreBoardUrl', () => {
                cmsService.getMenuItems.and.returnValue(of([
                  { categoryId: 19, showScoreboard: true, scoreBoardUrl: 'greyhounds-url' },
                  { categoryId: 16, showScoreboard: true }
                ]));
              });
              it('when scoreboards are disabled for current categoryId', () => {
                cmsService.getMenuItems.and.returnValue(of([
                  { categoryId: 19, showScoreboard: true, scoreBoardUrl: 'greyhounds-url' },
                  { categoryId: 16, showScoreboard: false, scoreBoardUrl: 'football-url' }
                ]));
              });
              afterEach(() => {
                component['checkGrandParadeAvailability']();
                expect(component.scoreboardUrl).toEqual('sysconfig-url');
              });
            });

            describe('with empty string when the scoreboard URL form CMS is not available', () => {
              it('and scoreboardUrl is not defined in sysConfig.Scoreboard section', () => {
                component.sysConfig.Scoreboard = { showScoreboard: 'Yes' };
              });
              it('and sysConfig does not have Scoreboard section', () => {
                component.sysConfig = { };
                coreTools.hasOwnDeepProperty.and.returnValue(false);
              });
              it('and sysConfig is not available', () => {
                component.sysConfig = null;
                coreTools.hasOwnDeepProperty.and.returnValue(false);
              });
              afterEach(() => {
                component['checkGrandParadeAvailability'](true);
                expect(component.scoreboardUrl).toEqual('');
              });
            });
          });
          afterEach(() => {
            expect(coreTools.hasOwnDeepProperty).toHaveBeenCalledWith(component.sysConfig, 'Scoreboard.showScoreboard');
            expect(cmsService.getMenuItems).toHaveBeenCalledWith();
          });
        });
      });

      describe('it should subscribe to SYSTEM_CONFIG_UPDATED pubsub event and on it', () => {
        let pubSubCb;

        beforeEach(() => {
          component['checkGrandParadeAvailability'] = jasmine.createSpy('checkGrandParadeAvailability');
          pubSubService.subscribe.and.callFake((name, channel, fn) => { pubSubCb = fn; });
          component['grandParadeLoader'](mockConfig).subscribe();
          component['checkGrandParadeAvailability'].calls.reset();
        });

        it('should do nothing if config is not updated', () => {
          const oldConfig = component.sysConfig;
          pubSubCb({ Scoreboard: { config: 'data-set-1' } });
          expect(component['checkGrandParadeAvailability']).not.toHaveBeenCalled();
          expect(component.sysConfig).toEqual({ Scoreboard: { config: 'data-set-1' } });
          expect(component.sysConfig).toBe(oldConfig);
        });

        it('should update sysConfig and call @checkGrandParadeAvailability with forceUrlUpdate=true if config is updated', () => {
          pubSubCb({ Scoreboard: { config: 'data-set-2' } });
          expect(component['checkGrandParadeAvailability']).toHaveBeenCalledWith(true);
          expect(component.sysConfig).toEqual({ Scoreboard: { config: 'data-set-2' } });
        });

        afterEach(() => {
          expect(pubSubService.subscribe).toHaveBeenCalledWith('sportEventMain', 'SYSTEM_CONFIG_UPDATED', jasmine.any(Function));
        });
      });
    });
  });

  describe('closeCashoutStream', () => {
    it('should unsubscribe from cashout data subscription', () => {
      component['cashoutDataSubscription'] = jasmine.createSpyObj('cashoutDataSubscription', ['unsubscribe']);

      component['closeCashoutStream']();

      expect(component['cashoutDataSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });

  describe('EDIT_MY_ACCA', () => {

    it('should switch to markets tab when my-bets edited (myBets)', fakeAsync(() => {
      const placedBets = [];
      component.eventEntity = <any>{ id: 2 };
      component.ngOnInit();
      tick();
      spyOn(component, 'setActiveUserTab').and.callThrough();

      commandService.executeAsync.and.callFake(key => {
        return Promise.resolve({ placedBets: placedBets, cashoutIds: <any>[] });
      });

      component.activeUserTab = 'myBets';
      emaHandler();
      tick();
      expect(component.activeUserTab).toEqual('markets');
      expect(component.setActiveUserTab).toHaveBeenCalled();
    }));

    it('should switch to markets tab when my-bets edited (markets)', fakeAsync(() => {
      const placedBets = [];
      component.eventEntity = <any>{ id: 2 };
      component.ngOnInit();
      tick();
      spyOn(component, 'setActiveUserTab');

      commandService.executeAsync.and.callFake(key => {
        return Promise.resolve({ placedBets: placedBets, cashoutIds: <any>[] });
      });

      component.activeUserTab = 'markets';
      emaHandler();
      tick();
      expect(component.setActiveUserTab).not.toHaveBeenCalled();
    }));
  });

  describe('init', () => {
    const deviceViewType = {
      mobile: true,
      desktop: false,
      tablet: false
    };
    it('should init with old data', () => {
      const eventMock = {
        drilldownTagNames: 'EVFLAG_FE,EVFLAG_PVM,EVFLAG_NE,EVFLAG_BL,',
        displayed: 'Y'
      };

      component.eventData = {
        event: [eventMock]
      };

      component.sport.getById.and.returnValue(of({
        collection: [],
        event: []
      }));
      component.deviceService = { getDeviceViewType: jasmine.createSpy('getDeviceViewType').and.returnValue(deviceViewType), isTabletOrigin: false};
      component['catId'] = '6';
      environment.brand = 'bma';

      component.init()
        .subscribe(() => {
          expect(eventMock.displayed).toEqual('N');
        });
    });

    it('should init without old data event', () => {
      const emptyEventDataMock = {
        event: []
      };

      component.eventData = emptyEventDataMock;

      component.sport.getById.and.returnValue(of({
        collection: [],
        event: []
      }));

      component.deviceService = { getDeviceViewType: jasmine.createSpy('getDeviceViewType').and.returnValue(deviceViewType), isTabletOrigin: false};
      component['catId'] = '39';
      environment.brand = 'ladbrokes';
      component.init()
        .subscribe(() => {
          expect(component.eventData).toEqual(emptyEventDataMock);
        });
    });

    it('should init data for MTA sport', () => {
      const emptyEventDataMock = {
        event: []
      };

      component.eventData = emptyEventDataMock;

      component.sport.getById.and.returnValue(of({
        collection: [],
        event: []
      }));

      component.deviceService = { getDeviceViewType: jasmine.createSpy('getDeviceViewType').and.returnValue(deviceViewType), isTabletOrigin: false};
      component['catId'] = '6';
      environment.brand = 'bma';
      component.init()
        .subscribe(() => {
          expect(component.eventData).toEqual(emptyEventDataMock);
        });
        component.deviceService = { getDeviceViewType: jasmine.createSpy('getDeviceViewType').and.returnValue({desktop: true})};
        component['catId'] = '39';
        environment.brand = 'bma';
      component.init()
      .subscribe(() => {
        expect(component.eventData).toEqual(emptyEventDataMock);
      });
    });
  });

  describe('checkFootballAlerts', () => {
    beforeEach(() => {
      nativeBridgeService.hasOnEventAlertsClick.and.returnValue(true);
      nativeBridgeService.getMobileOperatingSystem.and.returnValue('android');
      component.sportName = 'football';
      component.isOutright = false;
      component.eventEntity = { typeName: 'league'};
    });

    it('should NOT do football Alerts Visible if no configuration in CMS', () => {
      cmsService.getFeatureConfig.and.returnValue(of({
          visibleNotificationIcons: { }
      }));

      component.isFootball = true;

      component.checkFootballAlerts();
      expect(cmsService.getFeatureConfig).toHaveBeenCalled();
      expect(component.footballAlertsVisible).toBeFalsy();
    });

    it('should get visible notification icons from sport types', () => {
      cmsService.getFeatureConfig.and.returnValue(of({
          visibleNotificationIcons: {
            multiselectValue: ['android'],
            value: 'league'
        }
      }));

      component.isFootball = true;

      component.checkFootballAlerts();
      expect(cmsService.getFeatureConfig).toHaveBeenCalled();
      expect(component.footballAlertsVisible).toBeTruthy();
    });

    it('should set footballAlertsVisible (isOSPermitted = true, isFootball = false)', () => {
      nativeBridgeService.hasOnEventAlertsClick.and.returnValue(true);
      cmsService.getFeatureConfig.and.returnValue(of({
        NativeConfig: {
          visibleNotificationIconsFootball: {
            multiselectValue: ['android'],
            value: []
          }
        }
      }));

      component.sportName = 'football';
      component.isOutright = false;
      component.isFootball = false;

      component.checkFootballAlerts();
      expect(component.footballAlertsVisible).toBeFalsy();
    });

    it('should not set footballAlertsVisible', () => {
      nativeBridgeService.hasOnEventAlertsClick.and.returnValue(true);
      cmsService.getFeatureConfig.and.returnValue(of({}));
      component.sportName = 'football';
      component.isOutright = false;

      component.checkFootballAlerts();

      expect(component.footballAlertsVisible).toBeFalsy();
    });
  });

  describe('setActiveUserTab', () => {
    it('should open cancel EMA popup', () => {
      component.editMyAccaUnsavedOnEdp = true;
      component.setActiveUserTab('');
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.EMA_OPEN_CANCEL_DIALOG);
    });

    it('shoud set active tab and push GTM event', () => {
      component.eventEntity = {};
      component.editMyAccaUnsavedOnEdp = false;
      component.setActiveUserTab('myBets');
      expect(component.activeUserTab).toBe('myBets');
      expect(gtmService.push).toHaveBeenCalledTimes(1);
    });
  });

  it('setActiveUserTab: should open cancel edit acca popup', () => {
    component['editMyAccaUnsavedOnEdp'] = true;
    component['setActiveUserTab']('someTab');
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.EMA_OPEN_CANCEL_DIALOG);
  });

  describe('#handleFootballAlerts', () => {
    it('handleFootballAlerts isEnabled = true', () => {
      component.handleFootballAlerts({
        detail: {
          isEnabled: true
        }
      });

      expect(component.footballBellActive).toEqual(true);
    });

    it('handleFootballAlerts isEnabled = false', () => {
      component.handleFootballAlerts({
        detail: {
          isEnabled: false,
          settingValue: false
        }
      });

      expect(component.footballBellActive).toEqual(false);
    });
  });

  it('#trackMyBetsTabSwitch', () => {
    component.eventEntity = {
      id: '12345'
    };
    component['trackMyBetsTabSwitch']();

    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
      eventCategory: 'content',
      eventAction: 'click',
      eventLabel: `event page - my bets (undefined)`,
      eventID: '12345',
      location: 'event page'
    });
  });

  it('#setStreamShowFlag', () => {
    component['setStreamShowFlag']({
      detail: {
        settingValue: true
      }
    });

    expect(component.streamShown).toEqual(true);
  });

  describe('hasMarketSPFlag', () => {
    it('should return true', () => {
      component.eventEntity = { markets: [{ drilldownTagNames: 'MKTFLAG_SP' }] };
      expect(component.hasMarketSPFlag()).toBeTruthy();
    });

    it('should return true', () => {
      component.eventEntity = {};
      expect(component.hasMarketSPFlag()).toBeFalsy();
    });
  });

  describe('showWatchLiveWidget', () => {
    let isMatchLiveSpy;
    beforeEach(() => {
      component.eventEntity = {};
      isMatchLiveSpy = spyOnProperty(component, 'isMatchLive');
    });

    describe('when isButtons is true', () => {
      beforeEach(() => {
        component.eventEntity.liveStreamAvailable = true;
        isMatchLiveSpy.and.returnValue(true);
      });
      it('should return true when isMatchLive and liveStreamAvailable are both true', () => {
        expect(component.showWatchLiveWidget(true)).toEqual(true);
      });

      describe('should return false', () => {
        it('when isMatchLive is false', () => {
          isMatchLiveSpy.and.returnValue(false);
        });
        it('when liveStreamAvailable is false', () => {
          component.eventEntity.liveStreamAvailable = false;
        });
        afterEach(() => {
          expect(component.showWatchLiveWidget(true)).toEqual(false);
        });
      });
    });

    describe('when isButtons is false', () => {
      beforeEach(() => {
        component.eventEntity.liveStreamAvailable = false;
        isMatchLiveSpy.and.returnValue(false);
      });
      it('should return false when isMatchLive and liveStreamAvailable are both false', () => {
        expect(component.showWatchLiveWidget(false)).toEqual(false);
      });

      describe('should return true', () => {
        it('when isMatchLive is true', () => {
          isMatchLiveSpy.and.returnValue(true);
        });
        it('when liveStreamAvailable is true', () => {
          component.eventEntity.liveStreamAvailable = true;
        });
        afterEach(() => {
          expect(component.showWatchLiveWidget(false)).toEqual(true);
        });
      });
    });
    afterEach(() => {
      expect(isMatchLiveSpy).toHaveBeenCalled();
    });
  });

  describe('isMatchLive getter', () => {
    beforeEach(() => {
      component.preMatchWidgetAvailable = false;
      component.bgScoreboardConfig = null;
      component.eventsWithVisualizationParams = null;
      component.isScoreboardVis = component.gpScoreboardAvailable = false;
      component.optaScoreboardAvailable = false;
    });

    describe('should return false', () => {
      it('if no scoreboards/visualizations are available', () => {});
      it('if no scoreboards/visualizations are available (coverage case)', () => {
        component.bgScoreboardConfig = {};
        component.eventsWithVisualizationParams = [];
        component.isScoreboardVis = true;
      });
      it('if no scoreboards/visualizations are available (coverage case)', () => {
        component.bgScoreboardConfig = { available: false};
        component.gpScoreboardAvailable = true;
      });
      afterEach(() => {
        expect(component.isMatchLive).toEqual(false);
      });
    });

    describe('should return true', () => {
      it('when preMatchWidgetAvailable is true', () => {
        component.preMatchWidgetAvailable = true;
      });
      it('when bgScoreboardConfig.available is true', () => {
        component.bgScoreboardConfig = { available: true };
      });
      it('when eventsWithVisualizationParams is not empty', () => {
        component.eventsWithVisualizationParams = [{ } as any];
      });
      it('when isScoreboardVis and gpScoreboardAvailable are true', () => {
        component.isScoreboardVis = component.gpScoreboardAvailable = true;
      });
      it('when optaScoreboardAvailable is true', () => {
        component.optaScoreboardAvailable = true;
      });
      afterEach(() => {
        expect(component.isMatchLive).toEqual(true);
      });
    });
  });

  describe('subscribeForEventBetsUpdates', () => {
    beforeEach(() => {
      pubSubService.subscribe.and.callFake((p1, p2, cb) => {
        p2 === 'MY_BET_PLACED' && cb();
      });
    });

    it('should set active tab', () => {
      const placedbets = {bets: [
        { id: 4, settled: 'Y', cashoutStatus: 'BET_CASHED_OUT', type: '', leg: [ {'part':[{eventId: "11"}]}] }
      ] };
      component.activeUserTab = 'markets';
      pubSubService.subscribe.and.callFake((p1, p2, cb) => p2 === 'MY_BET_PLACED' && cb(placedbets));
      component.subscribeForEventBetsUpdates();
      expect(component.activeUserTab).toBe('markets');
    });

    it('should not set active tab', () => {
      const placedbets = {bets: [
        { id: 4, settled: 'Y', cashoutStatus: 'BET_CASHED_OUT', type: '', leg: [ {'part':[{eventId: "11"}]}] }
      ] };
      pubSubService.subscribe.and.callFake((p1, p2, cb) => p2 === 'MY_BET_PLACED' && cb(placedbets));
      component.subscribeForEventBetsUpdates();
      expect(component.activeUserTab).toBeUndefined();
    });

    it('bet placed from betslip when quick bet is true', () => {
      const placedbetsQ = {isquickbet: true, id: 1, bets: [{id: '1', leg: ['1'] }]};      
      pubSubService.subscribe.and.callFake((p1, p2, cb) => p2 === 'MY_BET_PLACED' && cb(placedbetsQ));
      const placedBets = [{ id: '1' }];
      const betsData = [{ betId: 'i2', id: '2', leg: ['2'] }];
      commandService.executeAsync.and.callFake(key => {
        if (key === 'GET_PLACED_BETS_ASYNC') {
          return Promise.resolve(betsData);
        }
        return Promise.resolve({});
      });
      component.subscribeForEventBetsUpdates();
      expect(component.activeUserTab).toBeUndefined();
    });
    
  });

  describe('#openCashoutStream', () => {
    it('no data from cash out stream', fakeAsync(() => {
      commandService.executeAsync = jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve(null));
      component['openCashoutStream']();

      tick();

      expect(component.betsStreamOpened).toBeTruthy();
      expect(cashOutMapService.createCashoutBetsMap).not.toHaveBeenCalled();
    }));

    it('data from cash out stream received', fakeAsync(() => {
      const data = [];
      commandService.executeAsync = jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve(data));
      component['openCashoutStream']();

      tick();

      expect(component.betsStreamOpened).toBeTruthy();
      expect(cashOutMapService.createCashoutBetsMap).toHaveBeenCalledWith(
        data,
        userService.currency,
        userService.currencySymbol
      );
    }));
  });
  describe('isShownDisclaimer', () => {
    it('#isShownDisclaimer condition1 true', () => {
      component.dataDisclaimer = {enabled : true} as any;
      component.eventEntity = {eventIsLive : true, comments:{teams : {home:{}}}} as any;
      component.isOutRight = false;
      component.isFallbackScoreboards = true;
      component.optaScoreboardAvailable = true;
     const result =  component.isShownDisclaimer();
      expect(result).toBe(true);
    });
    it('#isShownDisclaimer condition2 false', () => {
      component.dataDisclaimer = {enabled : true} as any;
      component.eventEntity = {eventIsLive : true, comments: null} as any;
      component.isOutRight = false;
      component.bgScoreboardConfig = {available : false} as any;
      component.brScoreboardConfig = {available : false} as any;
      component.isFallbackScoreboards = false;
      component.optaScoreboardAvailable = false;
     const result =  component.isShownDisclaimer();
      expect(result).toBe(false);
    });
  });
  describe('eventAutoSeoData', () => {
    it('should assign data to autoSeoData Object and publish data', () => {
      component.eventEntity = { name: 'teamA v teamB', typeName: 'World Cup', categoryName: 'football' };
      component.eventAutoSeoData();
      expect(component.autoSeoData).toBeDefined();
      expect(component.autoSeoData.name).toEqual(component.eventEntity.name);
      expect(component.autoSeoData.typeName).toEqual(component.eventEntity.typeName);
      expect(component.autoSeoData.categoryName).toEqual(component.eventEntity.categoryName);
      expect(pubSubService.publish).toHaveBeenCalledWith('AUTOSEO_DATA_UPDATED', jasmine.any(Object));
    });
  });
  describe('excludedFanzoneMarkets', () => {
    it('should call getExcludedDrilldownTagNameMarkets', () => {
      component.eventData = {
        event: [ { markets: [ { drilldownTagNames: 'MKTFLAG_FZ,' } ] } ],
        collection: []
      };
      spyOn(component as any, 'getExcludedDrilldownTagNameMarkets');

      component.excludedFanzoneMarkets();

      expect(component['getExcludedDrilldownTagNameMarkets']).toHaveBeenCalledTimes(1);
    });

    it('should not call getExcludedDrilldownTagNameMarkets as evenData is an empty object', () => {
      component.eventData = {};

      spyOn(component as any, 'getExcludedDrilldownTagNameMarkets');

      component.excludedFanzoneMarkets();

      expect(component['getExcludedDrilldownTagNameMarkets']).not.toHaveBeenCalled();
    });

    it('should call getExcludedDrilldownTagNameMarkets 2 times as collection data is having 2 markets', () => {
      component.eventData = {
        event: [],
        collection: [ { markets: [] }, { markets: [] } ]
      };

      spyOn(component as any, 'getExcludedDrilldownTagNameMarkets');

      component.excludedFanzoneMarkets();

      expect(component['getExcludedDrilldownTagNameMarkets']).toHaveBeenCalledTimes(2);
    });

    it('should not call getExcludedDrilldownTagNameMarkets for collection data is not having markets', () => {
      component.eventData = {
        event: [],
        collection: []
      };

      spyOn(component as any, 'getExcludedDrilldownTagNameMarkets');

      component.excludedFanzoneMarkets();

      expect(component['getExcludedDrilldownTagNameMarkets']).not.toHaveBeenCalled();
    });
  });

  it('getExcludedDrilldownTagNameMarkets', () => {
    const markets = [
      { id: '1', drilldownTagNames: 'MKTFLAG_FZ,' },
      { id: '2' }
    ];
    expect(component['getExcludedDrilldownTagNameMarkets'](markets)).toEqual([ {id: '2'} ]);
  });

  describe('should call updateCashoutData', () => {
    it('should call updateCashoutData', () => {
      component.placedBets = [];
      expect(component['updateCashoutData']()).toBeUndefined();
    });
  });
  describe("updateCashoutData", ()=>{
    it('should call updateCashoutData when isTempBetsAvailable length zero', () => {
      component.placedBets = <any>[{ betId: 'i1', leg: [{sportsLeg: {legPart: [{outcomeRef: {eventId: "12345"}}]}}] }, { betId: 'i2', leg: [{sportsLeg: {legPart: [{outcomeRef: {eventId: "54321"}}]}}] }];
      component.cashoutBets = null;
      component.tempBets = null;
      expect(component.updateCashoutData()).toBeUndefined();
    });

    it(`Should call updatecashout data for Local storage`, () => {
      component.placedBets = <any>[{ betId: 'i1', leg: [{sportsLeg: {legPart: [{outcomeRef: {eventId: "12345"}}]}}] }, { betId: 'i2', leg: [{sportsLeg: {legPart: [{outcomeRef: {eventId: "54321"}}]}}] }];
      storageService = {
        set: jasmine.createSpy('storageService.set'),
        get: jasmine.createSpy('storageService.get').and.returnValue([{"eventId":"11","betIds":[3]},{"eventId":"2","betIds":[4]}]),
      };
      component.eventId = 11;
      component['placedBets'] = [
        { id: 11, settled: 'N', cashoutStatus: 'BET_CASHED_IN', type: '', leg: [1,3,4,11] }
      ] as any;
      component.updateCashoutData();
      expect(component['showSignPosting']).toEqual(false);  
    });

    it('should call updateCashoutData when isTempBetsAvailable length > zero', () => {
      component.placedBets = <any>[{ betId: 'i1', leg: [{sportsLeg: {legPart: [{outcomeRef: {eventId: "12345"}}]}}] }, { betId: 'i2', leg: [{sportsLeg: {legPart: [{outcomeRef: {eventId: "54321"}}]}}] }];
      component.cashoutBets = null;
      component.tempBets = [{ betId: 'i2', id: '2', leg: ['2'] }, { betId: 'i3', id: '3', leg: ['3'] }];
      CashoutWsConnectorService.getConnection.and.returnValue(false);
      component.updateCashoutData();
      expect(CashoutWsConnectorService.getConnection).toHaveBeenCalled();
    });
    it('should call updateCashoutData when connection true', () => {
      component.placedBets = <any>[{ betId: 'i1', leg: [{sportsLeg: {legPart: [{outcomeRef: {eventId: "12345"}}]}}] }, { betId: 'i2', leg: [{sportsLeg: {legPart: [{outcomeRef: {eventId: "54321"}}]}}] }];
      component.cashoutBets = null;
      component.tempBets = [{ betId: 'i2', id: '2', leg: ['2'] }, { betId: 'i3', id: '3', leg: ['3'] }];
      CashoutWsConnectorService.getConnection.and.returnValue(true);
      CashoutWsConnectorService.dateChangeBet.and.returnValue(of(component.tempBets));
      component.updateCashoutData();
      expect(component.cashoutBets).toEqual(component.tempBets);
    });
  })
  describe('isLuckyDipMarket', () => {
    it('isLuckyDipMarket if luckyDip market available ', () => {

      const mockEvent = {
        "id": "3331136",
        "name": "TEST",
        "eventStatusCode": "A",
        "isActive": "true",
        "isDisplayed": "true",
        "displayOrder": "0",
        "siteChannels": "P,Q,C,I,M,",
        "eventSortCode": "TNMT",
        "startTime": "2023-02-28T18:43:00Z",
        "rawIsOffCode": "-",
        "classId": "195",
        "typeId": "3545",
        "sportId": "18",
        "liveServChannels": "sEVENT0003331136,",
        "liveServChildrenChannels": "SEVENT0003331136,",
        "categoryId": "18",
        "categoryCode": "GOLF",
        "categoryName": "Golf",
        "categoryDisplayOrder": "-377",
        "className": "Golf All Golf",
        "classDisplayOrder": "0",
        "classSortCode": "ST",
        "classFlagCodes": "SP,",
        "typeName": "Golf Day test",
        "typeDisplayOrder": "-100",
        "isOpenEvent": "true",
        "isNext2DayEvent": "true",
        "isNext1WeekEvent": "true",
        "isAvailable": "true",
        "cashoutAvail": "N",
        "markets": [
            {
                    "id": "48980432",
                    "eventId": "3331136",
                    "templateMarketId": "1597587",
                    "templateMarketName": "Lucky Dip",
                    "marketMeaningMajorCode": "N",
                    "marketMeaningMinorCode": "CW",
                    "name": "Lucky Dip",
                    "isLpAvailable": "true",
                    "betInRunIndex": "1",
                    "displayOrder": "0",
                    "marketStatusCode": "A",
                    "isActive": "true",
                    "isDisplayed": "true",
                    "siteChannels": "P,Q,C,I,M,",
                    "liveServChannels": "sEVMKT0048980432,",
                    "liveServChildrenChannels": "SEVMKT0048980432,",
                    "priceTypeCodes": "LP,",
                    "drilldownTagNames": "MKTFLAG_LD,",
                    "isAvailable": "true",
                    "maxAccumulators": "25",
                    "minAccumulators": "1",
                    "cashoutAvail": "N",
                    "termsWithBet": "N",
                    "children": [
                        {
                            "outcome": {
                                "id": "213900109",
                                "marketId": "48980432",
                                "name": "Player A",
                                "outcomeMeaningMajorCode": "CW",
                                "displayOrder": "0",
                                "outcomeStatusCode": "A",
                                "isActive": "true",
                                "isDisplayed": "true",
                                "siteChannels": "P,Q,C,I,M,",
                                "liveServChannels": "sSELCN0213900109,",
                                "liveServChildrenChannels": "SSELCN0213900109,",
                                "isAvailable": "true",
                                "cashoutAvail": "N",
                                "children": [
                                    {
                                        "price": {
                                            "id": "1",
                                            "priceType": "LP",
                                            "priceNum": "125",
                                            "priceDen": "1",
                                            "priceDec": "126.00",
                                            "isActive": "true",
                                            "displayOrder": "1"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            
              ]
    };
      component.events = mockEvent;
      component.sysConfig.LuckyDip = {enabled : true}
      component.isLuckyDipMarket(mockEvent)
      expect(component.isLuckyDipMarket(mockEvent)).toBeTruthy();
    });

    it('isLuckyDipMarket if luckyDip market not available ', () => {

      const mockEvent = {
        "id": "3331136",
        "name": "TEST",
        "eventStatusCode": "A",
        "isActive": "true",
        "isDisplayed": "true",
        "displayOrder": "0",
        "siteChannels": "P,Q,C,I,M,",
        "eventSortCode": "MTCH",
        "startTime": "2023-02-28T18:43:00Z",
        "rawIsOffCode": "-",
        "classId": "195",
        "typeId": "3545",
        "sportId": "18",
        "liveServChannels": "sEVENT0003331136,",
        "liveServChildrenChannels": "SEVENT0003331136,",
        "categoryId": "18",
        "categoryCode": "GOLF",
        "categoryName": "Golf",
        "categoryDisplayOrder": "-377",
        "className": "Golf All Golf",
        "classDisplayOrder": "0",
        "classSortCode": "ST",
        "classFlagCodes": "SP,",
        "typeName": "Golf Day test",
        "typeDisplayOrder": "-100",
        "isOpenEvent": "true",
        "isNext2DayEvent": "true",
        "isNext1WeekEvent": "true",
        "isAvailable": "true",
        "cashoutAvail": "N",
        "markets": [
            {
                    "id": "48980432",
                    "eventId": "3331136",
                    "templateMarketId": "1597587",
                    "templateMarketName": "Lucky Dip",
                    "marketMeaningMajorCode": "N",
                    "marketMeaningMinorCode": "CW",
                    "name": "Lucky Dip",
                    "isLpAvailable": "true",
                    "betInRunIndex": "1",
                    "displayOrder": "0",
                    "marketStatusCode": "A",
                    "isActive": "true",
                    "isDisplayed": "true",
                    "siteChannels": "P,Q,C,I,M,",
                    "liveServChannels": "sEVMKT0048980432,",
                    "liveServChildrenChannels": "SEVMKT0048980432,",
                    "priceTypeCodes": "LP,",
                    "drilldownTagNames": "MKT,",
                    "isAvailable": "true",
                    "maxAccumulators": "25",
                    "minAccumulators": "1",
                    "cashoutAvail": "N",
                    "termsWithBet": "N",
                    "children": [
                        {
                            "outcome": {
                                "id": "213900109",
                                "marketId": "48980432",
                                "name": "Player A",
                                "outcomeMeaningMajorCode": "CW",
                                "displayOrder": "0",
                                "outcomeStatusCode": "A",
                                "isActive": "true",
                                "isDisplayed": "true",
                                "siteChannels": "P,Q,C,I,M,",
                                "liveServChannels": "sSELCN0213900109,",
                                "liveServChildrenChannels": "SSELCN0213900109,",
                                "isAvailable": "true",
                                "cashoutAvail": "N",
                                "children": [
                                    {
                                        "price": {
                                            "id": "1",
                                            "priceType": "LP",
                                            "priceNum": "125",
                                            "priceDen": "1",
                                            "priceDec": "126.00",
                                            "isActive": "true",
                                            "displayOrder": "1"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            
              ]
    };
     component.sysConfig.LuckyDip = {enabled : false}
      component.isLuckyDipMarket(mockEvent)
      expect(component.isLuckyDipMarket(mockEvent)).toBeFalsy();
    });

    it('isLuckyDipMarket if luckyDip market is available but sys config is false ', () => {

      const mockEvent = {
        "id": "3331136",
        "name": "TEST",
        "eventStatusCode": "A",
        "isActive": "true",
        "isDisplayed": "true",
        "displayOrder": "0",
        "siteChannels": "P,Q,C,I,M,",
        "eventSortCode": "MTCH",
        "startTime": "2023-02-28T18:43:00Z",
        "rawIsOffCode": "-",
        "classId": "195",
        "typeId": "3545",
        "sportId": "18",
        "liveServChannels": "sEVENT0003331136,",
        "liveServChildrenChannels": "SEVENT0003331136,",
        "categoryId": "18",
        "categoryCode": "GOLF",
        "categoryName": "Golf",
        "categoryDisplayOrder": "-377",
        "className": "Golf All Golf",
        "classDisplayOrder": "0",
        "classSortCode": "ST",
        "classFlagCodes": "SP,",
        "typeName": "Golf Day test",
        "typeDisplayOrder": "-100",
        "isOpenEvent": "true",
        "isNext2DayEvent": "true",
        "isNext1WeekEvent": "true",
        "isAvailable": "true",
        "cashoutAvail": "N",
        "markets": [
            {
                    "id": "48980432",
                    "eventId": "3331136",
                    "templateMarketId": "1597587",
                    "templateMarketName": "Lucky Dip",
                    "marketMeaningMajorCode": "N",
                    "marketMeaningMinorCode": "CW",
                    "name": "Lucky Dip",
                    "isLpAvailable": "true",
                    "betInRunIndex": "1",
                    "displayOrder": "0",
                    "marketStatusCode": "A",
                    "isActive": "true",
                    "isDisplayed": "true",
                    "siteChannels": "P,Q,C,I,M,",
                    "liveServChannels": "sEVMKT0048980432,",
                    "liveServChildrenChannels": "SEVMKT0048980432,",
                    "priceTypeCodes": "LP,",
                    "drilldownTagNames": "MKTFLAG_LD",
                    "isAvailable": "true",
                    "maxAccumulators": "25",
                    "minAccumulators": "1",
                    "cashoutAvail": "N",
                    "termsWithBet": "N",
                    "children": [
                        {
                            "outcome": {
                                "id": "213900109",
                                "marketId": "48980432",
                                "name": "Player A",
                                "outcomeMeaningMajorCode": "CW",
                                "displayOrder": "0",
                                "outcomeStatusCode": "A",
                                "isActive": "true",
                                "isDisplayed": "true",
                                "siteChannels": "P,Q,C,I,M,",
                                "liveServChannels": "sSELCN0213900109,",
                                "liveServChildrenChannels": "SSELCN0213900109,",
                                "isAvailable": "true",
                                "cashoutAvail": "N",
                                "children": [
                                    {
                                        "price": {
                                            "id": "1",
                                            "priceType": "LP",
                                            "priceNum": "125",
                                            "priceDen": "1",
                                            "priceDec": "126.00",
                                            "isActive": "true",
                                            "displayOrder": "1"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            
              ]
    };
     component.sysConfig.LuckyDip = {enabled : false}
      component.isLuckyDipMarket(mockEvent)
      expect(component.isLuckyDipMarket(mockEvent)).toBeFalsy();
    });
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
  it('quickSwitchEnabled', () => {
    cmsService.getFeatureConfig = jasmine.createSpy('getFeatureConfig').and.returnValue(of({ isQuickSwitchEnabled: true }));
    component.quickSwitchEnabledSports = ['football'];
    component.sportName = 'football';
    component.isOutRight = false;
    component.isSpecialEvent = false;
    component.quickSwitchEnabled();
    expect(component.isQuickSwitchEnabled).toBeTrue();
  });
  it('handleQuickSwitchEvent', () => {
    component.handleQuickSwitchEvent({ output: 'closeQuickSwitchPanel' } as any);
    expect(component.changeMatch).toBeFalse();
  });
});
