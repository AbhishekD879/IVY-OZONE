import { of as observableOf, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { RacingEventComponent } from './racing-event.component';

import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';

import { eventMock, EDP_MARKETS } from './racing-event.component.mock';
import { horseracingConfig } from '@core/services/racing/config/horseracing.config';
import { UK_TOTE_CONFIG } from '@uktote/constants/uk-tote-config.contant';
import { FORECAST_CONFIG } from '@lazy-modules/forecastTricast/constants/forecast-tricast-config.contant';
import { IPerformGroupConfig } from '@lazy-modules/eventVideoStream/models/video-stream.model';
import { ALERTS_GTM } from '@app/betHistory/constants/bet-leg-item.constant';
import environment from '@environment/oxygenEnvConfig';

describe('RacingEventComponent', () => {
  let component: RacingEventComponent;
  let pubSubService;
  let windowRef;
  let timeService;
  let nativeBridgeService;
  let ukToteService;
  let lpAvailabilityService;
  let deviceService;
  let gtmService;
  let streamTrackingService;
  let dialogService;
  let filterService;
  let localeService;
  let horseracing;
  let routingHelperService;
  let cmsService;
  let tools;
  let sbFilters;
  let location;
  let router;
  let changeDetectorRef;
  let sortByOptionsService;
  let cmsObservableResult;
  let route;
  let watchRulesService;
  let seoDataService;
  let elementRef;
  let racingGaService;
  let pubSubResp: string;
  const placedBets = [
    { id: 11 },
    { id: 2, settled: 'Y' },
    { id: 3, cashoutStatus: 'BET_CASHED_OUT' },
    { id: 4, settled: 'Y', cashoutStatus: 'BET_CASHED_OUT' }
  ],
  betsData = { placedBets: placedBets, cashoutIds: [] };
  const mockString = 'seeAll';
  let raceDataMock;
  const HORSE_RACING_CATEGORY_ID = environment.HORSE_RACING_CATEGORY_ID;

  beforeEach(() => {
    raceDataMock = [
      {
        id: 123,
        markets: [
          {
            id: '12345',
            outcomes: []
          }
        ],
        categoryId: 9337,
        typeId: 2031
      }
    ];
    pubSubResp = 'price';
    seoDataService = {
      eventPageSeo: jasmine.createSpy('eventPageSeo')
    };
    route = {
      snapshot: {
        queryParams: {},
        params: {
          market: 'Win Only'
        }
      }
    };
    pubSubService = {
      API: {
        PIN_TOP_BAR: 'PIN_TOP_BAR',
        CLOSE_SORT_BY: 'CLOSE_SORT_BY',
        SORT_BY_OPTION: 'SORT_BY_OPTION',
        LIVE_MARKET_FOR_EDP: 'LIVE_MARKET_FOR_EDP',
        IS_NATIVE_VIDEO_STICKED: 'IS_NATIVE_VIDEO_STICKED',
        HAS_MARKET_DESCRIPTION: 'HAS_MARKET_DESCRIPTION',
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN',
        BET_PLACED: 'BET_PLACED', 
        EDIT_MY_ACCA: 'EDIT_MY_ACCA',
        EMA_UNSAVED_ON_EDP: 'EMA_UNSAVED_ON_EDP',
        CASH_OUT_BET_PROCESSED: 'CASH_OUT_BET_PROCESSED',
        MY_BETS_UPDATED: 'MY_BETS_UPDATED',
        SUSPEND_IHR_EVENT_OR_MRKT: 'SUSPEND_IHR_EVENT_OR_MRKT',
        EXTRA_PLACE_RACE_OFF: 'EXTRA_PLACE_RACE_OFF',
        IS_WEB_VIDEO_STICKED: 'IS_WEB_VIDEO_STICKED'
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
        if (channel === 'HAS_MARKET_DESCRIPTION') {
          channelFunction(true);
        } else if (channel === 'CASH_OUT_BET_PROCESSED'){
          channelFunction(1);
        } else if (channel === 'BET_PLACED'){
          channelFunction({bets: null});
        } else if (channel === pubSubService.API.SUSPEND_IHR_EVENT_OR_MRKT) {
          channelFunction('555', {fcMktAvailable: 'N', tcMktAvailable: 'N', originalName: 'Win or Each Way'});
        } else if (channel === 'IS_WEB_VIDEO_STICKED') {
          channelFunction('1px');
        }else {
          channelFunction(pubSubResp);
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish')
    };
    windowRef = {
      nativeWindow: {
        setInterval: jasmine.createSpy().and.callFake((fn, timer) => fn && fn()),
        clearInterval: jasmine.createSpy(),
        document: {
          querySelector: jasmine.createSpy().and.returnValue({
            style: {},
            offsetHeight: 123
          }),
          getElementById: jasmine.createSpy().and.returnValue({
            offsetWidth: 123
          }),
          addEventListener: jasmine.createSpy(),
          removeEventListener: jasmine.createSpy()
        },
        scrollTo: jasmine.createSpy(),
        requestAnimationFrame: jasmine.createSpy('requestAnimationFrame'),
        getComputedStyle: jasmine.createSpy().and.returnValue({top: '20px'}),
        NativeBridge: {
          displayInLandscapeMode: jasmine.createSpy()
        }
      }
    };
    changeDetectorRef = {
      detach: jasmine.createSpy(),
      detectChanges: jasmine.createSpy()
    };
    timeService = {
      getCurrentTime: jasmine.createSpy('getCurrentTime'),
      minutesToMiliseconds: jasmine.createSpy('minutesToMiliseconds'),
      formatByPattern: jasmine.createSpy().and.returnValue('2018-10-30'),
      isActiveRangeForCustomTime: jasmine.createSpy('isActiveRangeForCustomTime').and.returnValue(true)
    };
    nativeBridgeService = {
      hideVideoStream: jasmine.createSpy('hideVideoStream'),
      eventPageLoaded: jasmine.createSpy('eventPageLoaded'),
      hasOnEventAlertsClick: jasmine.createSpy('hasOnEventAlertsClick').and.returnValue(true),
      playerStatus: false,
      onEventAlertsClick: jasmine.createSpy('onEventAlertsClick'),
      getMobileOperatingSystem: jasmine.createSpy().and.returnValue('ios'),
      handleNativeVideoPlaceholder: jasmine.createSpy('handleNativeVideoPlaceholder'),
      handleNativeVideoPlayer: jasmine.createSpy('handleNativeVideoPlayer'),
      hideVideoPlaceholder: jasmine.createSpy('hideVideoPlaceholder'),
      displayInLandscapeMode: jasmine.createSpy('displayInLandscapeMode')
    };
    ukToteService = {
      getTotePoolEventIds: jasmine.createSpy('getTotePoolEventIds').and.returnValue(['1', '2', '3']),
      getPoolsForEvent: jasmine.createSpy('getPoolsForEvent').and.returnValue(observableOf([
        { type: 'UWIN' },
        { type: 'UPLC' },
        { type: 'UPLC' }
      ]))
    };
    lpAvailabilityService = {
      check: jasmine.createSpy('check')
    };
    deviceService = {
      isTablet: true,
      isDesktop: true,
      isWrapper: true,
      isTabletLandscape: false
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    streamTrackingService = {
      checkIdForDuplicates: jasmine.createSpy('checkIdForDuplicates').and.returnValue(false),
      addIdToTrackedList: jasmine.createSpy('addIdToTrackedList')
    };
    dialogService = {
      openDialog: jasmine.createSpy('openDialog')
    };
    filterService = {
      distance: jasmine.createSpy('distance').and.returnValue('test distance'),
      orderBy: jasmine.createSpy('orderBy').and.returnValue(eventMock.markets),
      date: jasmine.createSpy('date').and.returnValue('2018-10-30')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('test_string')
    };
    horseracing = {
      getEvent: jasmine.createSpy('getEvent').and.returnValue(Promise.resolve(['poolEventEntity'])),
      isRacingSpecials: jasmine.createSpy('isRacingSpecials'),
      getSortingFromCms: jasmine.createSpy('getSortingFromCms').and.returnValue({}),
      isToteForecastTricasMarket: jasmine.createSpy('isToteForecastTricasMarket').and.returnValue(true)
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('url'),
      formResultedEdpUrl: jasmine.createSpy('formResultedEdpUrl')
    };
    cmsService = {
      getRacingEDPMarkets: jasmine.createSpy('getRacingEDPMarkets').and.returnValue(observableOf(EDP_MARKETS)),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.callFake((preventCache, isPromise) => {
        if (isPromise) {
          return {
            then(callback) {
              callback({
                NativeConfig: {
                  visibleNotificationIconsHorseracing: {
                    multiselectValue: {
                      '0': 'ios',
                      '1': 'android'
                    },
                    value: 'ChepstowTN'
                  }
                }
              });
            }
          };
        } else {
          return observableOf(cmsObservableResult);
        }
      }),
      getFeatureConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf(cmsObservableResult))
    };

    cmsObservableResult = {
      SortOptions: {
        enabled: true
      },
      RacingEDPMarketsDescription: {
        enabled: false
      },
      TotePools: {
        Enable_UK_Totepools: true
      },
      performGroup: {},
      quantumLeapTimeRange: {
        startTime: '10:20am',
        endTime: '11:10pm'
      },
      enabled: true,
      title: 'welcome'
    };
    tools = {
      getDaySuffix: jasmine.createSpy('getDaySuffix').and.returnValue('th')
    };
    sbFilters = {
      orderOutcomeEntities: jasmine.createSpy('orderOutcomeEntities').and.returnValue(eventMock.markets[0].outcomes),
      orderOutcomesByName: jasmine.createSpy('orderOutcomeEntities')
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl'),
      events: {
        subscribe: jasmine.createSpy('events')
      },
      url: 'test'
    };
    location = {
      replaceState: jasmine.createSpy(),
      go: jasmine.createSpy(),
      path: jasmine.createSpy().and.returnValue('/path/racing-specials')
    };
    sortByOptionsService = {
      get: jasmine.createSpy('get').and.returnValue('Price'),
      set: jasmine.createSpy('set'),
    };

    watchRulesService = {
      shouldShowCSBIframe: jasmine.createSpy('shouldShowCSBIframe'),
      isInactiveUser: jasmine.createSpy('isInactiveUser')
    };

    elementRef = {
      nativeElement: {
        querySelector: jasmine.createSpy().and.returnValue(null)
      }
    } as any;

    racingGaService = {
      trackEvent: jasmine.createSpy('trckEvent'),
      updateGATracking: jasmine.createSpy('updateGATracking'),
      toggleShowOptionsGATracking: jasmine.createSpy('toggleShowOptionsGATracking')
    };


    createComponent();

    component.eventEntity = Object.assign({}, eventMock);
    component.sportName = 'horseracing';
    component.selectedTypeName = 'selectedTypeName_string';
    component['config'] = horseracingConfig;
    component.racingTypeNames = ['racingTypeNames_string', 'racingTypeNames_string2'];
    component.racingInMeeting = [component.eventEntity];
    component.presimStopTrackInterval = 100;
    component.filter = 'filter_string';
    component.eventId = 11;
    component.images = 'images_string';
    component.onExpand = jasmine.any(Function) as any;
    component.streamControl = {
      externalControl: true,
      playLiveSim: jasmine.createSpy('playLiveSim'),
      playStream: jasmine.createSpy('playStream'),
      hideStream: jasmine.createSpy('hideStream'),
    };
    component.nativeVideoPlayerPlaceholderRef = { nativeElement: { className: 'native-video-player-placeholder'} };
    component['cashoutIds'] = <any>[{ id: 'i1' }, { id: 'i2' }];
    component['placedBets'] = <any>[{ betId: 'i1' }, { betId: 'i2' }];
    component['isLoggedIn'] = true;
  });

  function createComponent() {
    component = new RacingEventComponent(
      windowRef,
      timeService,
      pubSubService,
      nativeBridgeService,
      ukToteService,
      lpAvailabilityService,
      deviceService,
      gtmService,
      streamTrackingService,
      dialogService,
      filterService,
      localeService,
      horseracing,
      routingHelperService,
      cmsService,
      tools,
      sbFilters,
      router,
      location,
      changeDetectorRef,
      sortByOptionsService,
      route,
      watchRulesService,
      seoDataService,
      elementRef,
      racingGaService
    );
    (component['_raceData'] as any) = raceDataMock;
  }

  it('ngOnInit no event entity', () => {
    component.eventEntity = undefined;
    component.ngOnInit();
    expect(component.isWrapper).toBe(false);
    expect(cmsService.getSystemConfig).not.toHaveBeenCalled();
    expect(component.racingPostSummary).toBe(undefined);
    expect(component.isActiveRangeForQuantumLeap).toBe(true);
  });

  it('ngOnInit with event entity', fakeAsync(() => {
    spyOn(component, 'filterDate');
    spyOn(component, 'modifyMarkets');
    spyOn(component, 'isAntepostMarket');
    spyOn(component, 'showRibbonEventName');
    spyOn(component, 'goToSeo');
    component['syncToApplySorting'] = jasmine.createSpy();
    component['addForecastTricastTabs'] = jasmine.createSpy();
    component['addTotePoolTab'] = jasmine.createSpy();
    component['getBIRMarkets'] = jasmine.createSpy();
    component['initializeBreadcrumbs'] = jasmine.createSpy('initializeBreadcrumbs');
    component['isHR'] = true;
    route.snapshot.params.market = undefined;

    component.ngOnInit();

    tick(1000);
    expect(component.selectedMarket).toEqual('Win Only');
    expect(component['hasMarketType']).toBe(false);
    expect(component.racingTypeNames).toEqual(['racingTypeNames_string', 'racingTypeNames_string2']);
    expect(component['filterDate']).toHaveBeenCalledWith(component.eventEntity.startTime);
    expect(component.expandedSummary).toEqual([]);
    expect(component.eventEntity.filteredTime).toBe(undefined);
    expect(component.outcomeInfo).toBeTruthy();
    expect(component['getBIRMarkets']).toHaveBeenCalled();
    expect(component.racingPostSummary).toBe('test overview ... ');
    expect(component.eventEntity.racingFormEvent.overview).toEqual('test overview');
    expect(component.eventEntity.racingFormEvent.distance).toEqual('test distance');
    expect(component.sortBy).toEqual('Price');
  }));

    it('ngOnInit with event entity', fakeAsync(() => {
      spyOn(component, 'filterDate');
      spyOn(component, 'modifyMarkets');
      spyOn(component, 'isAntepostMarket');
      spyOn(component, 'showRibbonEventName');
      spyOn(component, 'goToSeo');
      component['syncToApplySorting'] = jasmine.createSpy();
      component['addForecastTricastTabs'] = jasmine.createSpy();
      component['addTotePoolTab'] = jasmine.createSpy();
      component['initializeBreadcrumbs'] = jasmine.createSpy('initializeBreadcrumbs');

      component.ngOnInit();

      tick(1000);

      expect(component.selectedMarket).toEqual('Win Only');
      expect(component.racingTypeNames).toEqual(['racingTypeNames_string', 'racingTypeNames_string2']);
      expect(component['filterDate']).toHaveBeenCalledWith(component.eventEntity.startTime);
      expect(component.expandedSummary).toEqual([]);
      expect(component.eventEntity.filteredTime).toBe(undefined);
      expect(component.outcomeInfo).toBeTruthy();
      expect(component.racingPostSummary).toBe('test overview ... ');
      expect(component.eventEntity.racingFormEvent.overview).toEqual('test overview');
      expect(component.eventEntity.racingFormEvent.distance).toEqual('test distance');
      expect(component.sortBy).toEqual('Price');

      expect(component.filter).toBe('showVideoStream');

      expect(sortByOptionsService.get).toHaveBeenCalled();
      expect(component.goToSeo).toHaveBeenCalled();
      expect(filterService.orderBy).toHaveBeenCalledWith(jasmine.any(Object), ['customOrder', 'displayOrder', 'name']);
      expect(filterService.distance).toHaveBeenCalledWith('test distance');
      expect(cmsService.getSystemConfig).toHaveBeenCalled();

      expect(component.sortOptionsEnabled).toBeTruthy();
      expect(component.performConfig).toEqual({} as IPerformGroupConfig);
      expect(timeService.isActiveRangeForCustomTime).toHaveBeenCalled();
      expect(component.isActiveRangeForQuantumLeap).toEqual(true);
      expect(component.eventEntity.categoryCode).toBe('HORSE_RACING');
      expect(component.isAntepostMarket).toHaveBeenCalled();
      expect(component['syncToApplySorting']).toHaveBeenCalled();
      expect(component['addForecastTricastTabs']).toHaveBeenCalled();
      expect(ukToteService.getTotePoolEventIds).toHaveBeenCalledWith(component.eventEntity);
      expect(component.pools.length).toEqual(3);
      expect(horseracing.getEvent).toHaveBeenCalledWith('1');
      expect(component.poolEventEntity).toEqual(jasmine.any(String));
      expect(component['addTotePoolTab']).toHaveBeenCalled();
      expect(component['initializeBreadcrumbs']).toHaveBeenCalled();
      expect(horseracing.isRacingSpecials).toHaveBeenCalled();
      expect(nativeBridgeService.eventPageLoaded).toHaveBeenCalledWith(component.eventId.toString(), component.sportName);
      expect(component['document'].addEventListener).toHaveBeenCalledWith('eventAlertsEnabled', jasmine.any(Function));
      expect(component.showRibbonEventName).toHaveBeenCalled();
      expect(component.isWrapper).toBe(true);
      expect(component.isMarketAntepost).toBeFalsy();
      expect(component.showQuantumLeap).toBeTruthy();

      const config = {
        showFullScreen: true,
        fullScreenDrillDownTags: ['EVFLAG_PVM', 'EVFLAG_PVA'],
        insightsDrillDownTags: ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'],
      };
      cmsService.getFeatureConfig.and.returnValue(observableOf(config));
      deviceService.isWrapper = false;
      component.ngOnInit();

      tick(1000);

      expect(component.isWrapper).toBe(false);
      expect(component.isFullScreenConfig).toEqual(true);
    }));

    it(`should addDeleteMarketListener`, () => {
      spyOn(component,'updateFloatingMsgTop');
      component.ngOnInit();
      expect(component.updateFloatingMsgTop).toHaveBeenCalled();
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith('RacingEventComponent', pubSubService.API.DELETE_MARKET_FROM_CACHE, jasmine.any(Function));
    });

  describe('ngOnInit with event entity for QuantumLeap', () => {
    it('should isActiveRangeForQuantumLeap = true when sportName = greyhound', fakeAsync(() => {
      component.sportName = 'greyhound';
      component.ngOnInit();
      tick();
    }));
    it('should isActiveRangeForQuantumLeap = true when isUKorIRE = false', fakeAsync(() => {
      component.eventEntity.isUKorIRE = false;
      component.ngOnInit();
      tick();
      expect(component['hasMarketType']).toBe(true);
      expect(component.showQuantumLeap).toBeFalsy();
    }));
    it('should isActiveRangeForQuantumLeap = true when quantumLeapTimeRange = {}', fakeAsync(() => {
      cmsObservableResult.quantumLeapTimeRange = {};

      component.ngOnInit();
      tick();
    }));
    it('should isActiveRangeForQuantumLeap = true when quantumLeapTimeRange = { startTime: 10:20am }', fakeAsync(() => {
      cmsObservableResult.quantumLeapTimeRange = { startTime: '10:20am' };

      component.ngOnInit();
      tick();
    }));
    it('should isActiveRangeForQuantumLeap = true when quantumLeapTimeRange = { endTime: 11:10pm }', fakeAsync(() => {
      cmsObservableResult.quantumLeapTimeRange = { endTime: '11:10pm' };

      component.ngOnInit();
      tick();
    }));
    afterEach(() => {
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      expect(timeService.isActiveRangeForCustomTime).not.toHaveBeenCalled();
      expect(component.isActiveRangeForQuantumLeap).toEqual(true);
    });
  });

  describe('addDeleteMarketListener', () => {
    beforeEach(() => {
      spyOn(component as any, 'removeTab');
      component.eventEntity.sortedMarkets = [{ id: '1' }, { id: '2', markets: [{ id: '3' }, { id: '4' }] }] as any;
    });

    it(`should addDeleteMarketListener`, () => {
      component.addDeleteMarketListener();

      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith('RacingEventComponent', pubSubService.API.DELETE_MARKET_FROM_CACHE, jasmine.any(Function));
    });

    it(`should find market index`, () => {
      pubSubResp = '2';
      component.addDeleteMarketListener();

      expect(component.removeTab).toHaveBeenCalledWith(undefined, 1);
    });

    it(`index should equal -1`, () => {
      pubSubResp = '21';
      component.addDeleteMarketListener();

      expect(component.removeTab).not.toHaveBeenCalled();
    });

    it(`should remove daughter market`, () => {
      pubSubResp = '4';
      component.addDeleteMarketListener();

      const daughterIndex = component.eventEntity.sortedMarkets[1].markets.findIndex(mkt => mkt.id === pubSubResp);

      expect(daughterIndex).toEqual(-1);
      expect(component.removeTab).not.toHaveBeenCalled();
    });
  });

  describe('removeTab', () => {
    beforeEach(() => {
      component.eventEntity.sortedMarkets = [
        { id: '7', label: 'lbl' },
        { id: '1', label: 'Win or E/W' },
        { id: '2', label: component.tricastLabel },
        { id: '3', label: component.forecastLabel },
        {
          id: '4',
          label: 'label',
          markets: [{ id: '5' }, { id: '6' }]
        }
      ] as any;
      component['setMarketTabs']();
      component.selectedMarket = 'lbl';
    });

    it(`should return if not find index`, () => {
      spyOn(component.eventEntity.sortedMarkets, 'splice');

      component.removeTab(undefined, -1);

      expect(component.eventEntity.sortedMarkets.splice).not.toHaveBeenCalled();
    });

    it(`should return if label and index are Not Integer`, () => {
      spyOn(component.eventEntity.sortedMarkets, 'splice');

      component.removeTab('str', undefined);

      expect(component.eventEntity.sortedMarkets.splice).not.toHaveBeenCalled();
    });

    it(`should work without label`, () => {
      component.selectedMarket = 'label';

      component.removeTab(undefined, 4);

      expect(component.selectedMarket).toEqual(component.forecastLabel);
    });

    it(`should remove tricast and forecast tabs if WinOrEWCase and activate first tab`, () => {
      component.selectedMarket = component.tricastLabel;

      component.removeTab(component.winOrEWLabel);

      const sortedMarket = component.eventEntity.sortedMarkets
        .some(el => el.label === component.tricastLabel || el.label === component.forecastLabel);
      const marketTab = component.marketsTabs
        .some(el => el.name === component.tricastLabel || el.name === component.forecastLabel);

      expect(sortedMarket).toBeFalsy();
      expect(marketTab).toBeFalsy();
      expect(component.selectedMarket).toEqual('lbl');
    });

    it(`should not change tab if active tab is not WinOrEWCase`, () => {
      component.removeTab(component.winOrEWLabel);

      expect(component.selectedMarket).toEqual('lbl');
    });

    it(`should not remove tricast and forecast tabs if Not WinOrEWCase `, () => {
      component.removeTab('label');

      expect(component.selectedMarket).toEqual('lbl');
    });

    it(`should remove tab`, () => {
      component.removeTab('label');

      expect(component.eventEntity.sortedMarkets.find(el => el.label === 'label')).toBeUndefined();
      expect(component.marketsTabs.find(el => el.name === 'label')).toBeUndefined();
    });

    it(`should Not change tab if no markets left`, () => {
      component.eventEntity.sortedMarkets = [{ id: '7', label: 'lbl' }] as any;

      component.removeTab('lbl');

      expect(component.selectedMarket).toEqual('lbl');
    });

    it(`should activate last tab `, () => {
      component.selectedMarket = 'label';

      component.removeTab('label');

      expect(component.selectedMarket).toEqual(component.forecastLabel);
    });

    it(`should activate next tab`, () => {
      component.selectedMarket = component.tricastLabel;

      component.removeTab(component.tricastLabel);

      expect(component.selectedMarket).toEqual(component.forecastLabel);
    });
  });

  describe('', () => {
    beforeEach(() => {
      component.eventEntity.categoryCode = 'GRAYHOUNDS';
    });
    it('ngOnInit with event entity not for bma', fakeAsync(() => {
      component.ngOnInit();
      component.sortBy= 'Price';
      tick(1000);
      expect(component.sortBy).toEqual('Price');
      expect(filterService.distance).not.toHaveBeenCalled();
    }));
  });

  describe('RacingEventComponent, parse distance, when no yards was in DF data', () => {
    beforeEach(() => {
      component.eventEntity.categoryCode = 'HORSE_RACING';
      component.eventEntity.racingFormEvent.distance = undefined;
    });
    it('ngOnInit with event entity not for bma', fakeAsync(() => {
      component.ngOnInit();
      tick(1000);
      expect(filterService.distance).not.toHaveBeenCalled();
    }));

    it('ngOnInit to filter virtual event', fakeAsync(() => {
      component.eventEntity.categoryId = '39';
      component.ngOnInit();
      tick(1000);
      expect(filterService.distance).not.toHaveBeenCalled();
    }));
  });

  describe('goToSeo', () => {
    it('should create seo ', () => {
      routingHelperService.formEdpUrl.and.returnValue('url');
      component.goToSeo(({id: '1'} as any));
      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith({ id: '1' });
      expect(seoDataService.eventPageSeo).toHaveBeenCalledWith({ id: '1' },'url');
    });
  });

  describe('isShowMedia', () => {
    it('should set isShowMedia to false if it is isAntepost market', () => {
      component.sportName = 'greyhound';
      component.isRacingSpecialsCondition = false;
      component.eventEntity = {
        isUKorIRE: true,
        liveStreamAvailable: true,
        markets: [{ isAntepost: 'true' }]
      } as any;

      expect(component['isShowMedia']).toBe(false);
    });

    it('should set isShowMedia to false if it is isRacingSpecialsCondition', () => {
      component.sportName = 'greyhound';
      component.isRacingSpecialsCondition = true;
      component.eventEntity = {
        isUKorIRE: false,
        liveStreamAvailable: false,
        markets: [{ isAntepost: 'false' }]
      } as any;

      expect(component['isShowMedia']).toBe(false);
    });

    it('should set isShowMedia to false if it is liveStreamAvailable = false', () => {
      component.sportName = 'greyhound';
      component.isRacingSpecialsCondition = false;
      component.eventEntity = {
        isUKorIRE: true,
        liveStreamAvailable: false,
        markets: [{ isAntepost: 'false' }]
      } as any;

      expect(component['isShowMedia']).toBe(false);
    });

    it('should set isShowMedia to true if it is isUKorIRE and not greyhound', () => {
      component.sportName = 'racing';
      component.isRacingSpecialsCondition = false;
      component.eventEntity = {
        isUKorIRE: true,
        liveStreamAvailable: false,
        markets: [{ isAntepost: 'false' }]
      } as any;

      expect(component['isShowMedia']).toBe(true);
    });

    it('should set isShowMedia to true if it is liveStreamAvailable = true', () => {
      component.sportName = 'greyhound';
      component.isRacingSpecialsCondition = false;
      component.eventEntity = {
        isUKorIRE: true,
        liveStreamAvailable: true,
        markets: [{ isAntepost: 'false' }]
      } as any;

      expect(component['isShowMedia']).toBe(true);
    });
  });

  describe('Wrapper Notifications handling', () => {
    it('should set alertsVisible to true', () => {
      component.ngOnInit();

      expect(component.alertsVisible).toBe(false);
    });

    it('should call onEventAlertsClick', () => {
      component.eventId = 11;
      component.sportName = 'horseracing';
      component.onBellClick();

      expect(nativeBridgeService.onEventAlertsClick)
        .toHaveBeenCalledWith(component.eventId.toString(), component.sportName, component.eventEntity.categoryId, 'test', ALERTS_GTM.EVENT_SCREEN);
    });
  });

  describe('ngOnInit racingSpecials', () => {
    it('if it is racing Specials page', () => {
      spyOn(component, 'filterDate');
      component.eventEntity.startTime = '12';
      horseracing.isRacingSpecials.and.returnValue(true);
      component.ngOnInit();

      expect(component.filterDate).toHaveBeenCalledWith('12', true);
    });

    it('if it is nor racing Specials page', () => {
      spyOn(component, 'filterDate');
      horseracing.isRacingSpecials.and.returnValue(false);
      component.ngOnInit();

      expect(component.filterDate).not.toHaveBeenCalledWith('12', true);
    });

    it('should set isGreyhound property', () => {
      component.eventEntity.categoryCode = 'GreyHoundEdp';
      component.ngOnInit();

      expect(component.isGreyhoundEdp).toEqual(true);
    });

    it('should set hideSilk property greyhound specials', fakeAsync(() => {
      horseracing.isRacingSpecials.and.returnValue(true);
      component.eventEntity.categoryCode = 'greyhound';
      component.ngOnInit();
      tick(1000);
      expect(component.hideSilk).toEqual(true);
    }));

    it('should set isFutureMeetingsOverlay greyhound categoryid', fakeAsync(() => {
      horseracing.isRacingSpecials.and.returnValue(true);
      component.eventEntity.categoryId = '19';
      component.ngOnInit();
      tick(1000);
      expect(component.isFutureMeetingsOverlay).toEqual(true);
    }));

    it('should set hideSilk property not greyhound specials', fakeAsync(() => {
      horseracing.isRacingSpecials.and.returnValue(true);
      component.eventEntity.categoryCode = 'HORSE_RACING';
      component.ngOnInit();
      tick(1000);
      expect(component.hideSilk).toEqual(false);
    }));

    it('should set hideSilk property greyhound not specials', fakeAsync(() => {
      horseracing.isRacingSpecials.and.returnValue(false);
      component.eventEntity.categoryCode = 'greyhound';
      component.ngOnInit();
      tick(1000);
      expect(component.hideSilk).toEqual(false);
    }));

    it('should set hideSilk property not greyhound not specials', fakeAsync(() => {
      horseracing.isRacingSpecials.and.returnValue(false);
      component.eventEntity.categoryCode = 'HORSE_RACING';
      component.ngOnInit();
      tick(1000);
      expect(component.hideSilk).toEqual(false);
    }));

    it('should set eventEntity rawIsOffCode from racingInMeeting event', () => {
      component.eventId = 1;
      component.racingInMeeting = [
        { rawIsOffCode: 'Y', id: 10 },
        { rawIsOffCode: 'N', id: component.eventId }
      ] as any[];
      component.ngOnInit();
      expect(component.eventEntity.rawIsOffCode).toEqual('N');
    });
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe from listeners', () => {
      component['routeEventsListener'] = null;
      component['ukToteDataSubscription'] = undefined;
      component['secondaryMarketsSubscription'] = undefined;
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('RacingEventComponent');
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('racingEvent');
      expect(windowRef.nativeWindow.clearInterval).toHaveBeenCalled();
    });

    it('should unsubscribe from route events listener', () => {
      component['routeEventsListener'] = {
        unsubscribe: jasmine.createSpy('routeEventsListener')
      } as any;
      component['ukToteDataSubscription'] = {
        unsubscribe: jasmine.createSpy()
      } as any;
      component['secondaryMarketsSubscription'] = {
        unsubscribe: jasmine.createSpy()
      } as any;
      component.ngOnDestroy();
      expect(component['routeEventsListener'].unsubscribe).toHaveBeenCalled();
      expect(component['ukToteDataSubscription'].unsubscribe).toHaveBeenCalled();
      expect(component['secondaryMarketsSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });

  describe('@update location', () => {
    beforeEach(() => {
      routingHelperService.formResultedEdpUrl.and.returnValue('edpUrl');
    });

    it('should update the browser with proper URL when "replace" argument is falsy', () => {
      component.updateLocation('path');
      expect(location.go).toHaveBeenCalledWith('url/path', '');
    });

    it('should update url with query param', () => {
      component['route'].snapshot.queryParams.origin = 'next-race';
      component.updateLocation('path');

      expect(location.go).toHaveBeenCalledWith('url/path', 'origin=next-race');
    });

    it('should replace the browser with proper URL when "replace" argument is true', () => {
      component.updateLocation('path', true);
      expect(location.replaceState).toHaveBeenCalledWith('url/path', '');
    });

    it('should not add trailing slash to EDP URL if subpath is null', () => {
      component.updateLocation(null);
      expect(location.go).toHaveBeenCalledWith('url', '');
    });

    it('should not add trailing slash to EDP URL if subpath is null', () => {
      component['route'].snapshot.queryParams.origin = 'next-race';
      component.updateLocation(null);
      expect(location.go).toHaveBeenCalledWith('url', 'origin=next-race');
    });
  });

  describe('getBIRMarkets', () => {
    beforeEach(() => {
      spyOn(component,'modifyMarkets').and.callThrough();
      component['eventEntity'] = { drilldownTagNames: 'test,EVFLAG_IHR',
        markets: [{
        id: '275108045',
        name: 'Win Only',
        outcomes: [{
          runnerNumber: '15',
          racingFormOutcome: {
            weight: 'Pounds, 8  '
          },
          isValidRunnerNumber: false
        }]
      }]} as any;
      component['isHR'] = true;
    });
    it('getBIRMarkets with cms config as null', () => {
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf(null));
      component['getBIRMarkets']();
      expect(component['BIRMarketsEnabled']).toBeFalsy();
      expect(component.modifyMarkets).toHaveBeenCalled();
    });
    it('getBIRMarkets with actual values', () => {
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({HorseRacingBIR: {marketsEnabled: ['Win or Each Way']}}));
      component['getBIRMarkets']();
      expect(component['BIRMarketsEnabled']).toEqual(['Win or Each Way']);
      expect(component.modifyMarkets).toHaveBeenCalled();
    });
    it('getBIRMarkets with HorseRacingBIR as null', () => {
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({HorseRacingBIR: null}));
      component['getBIRMarkets']();
      expect(component['BIRMarketsEnabled']).toBeFalsy();
      expect(component.modifyMarkets).toHaveBeenCalled();
    });
  });

  it('selectFallbackMarket', () => {
    component['selectFallbackMarket']({ label: 'Market1', path: 'market1' } as IMarket);

    expect(component.selectedMarket).toBe('Market1');
    expect(component.selectedMarketPath).toBe('market1');
    expect(component.selectedMarketTypePath).toBeNull();
  });
  it('handleRacingMybetsUpdates', () => {
    component['handleRacingMybetsUpdates']({output: 'tabUpdated', value: 'myBets'});
    expect(component.activeUserTab).toBe('myBets');
  });
  describe('isBirMarketEnabled', () => {
    it('BIRMarketsEnabled', () => {
      component['BIRMarketsEnabled'] = ['Win or Each Way'];
      expect(component['isBirMarketEnabled']('Win or Each Way')).toBeTruthy();
    });
    it('isBirMarketEnabled with null input', () => {
      component['BIRMarketsEnabled'] = ['Win or Each Way'];
      expect(component['isBirMarketEnabled']()).toBeFalsy();
    });
    it('isBirMarketEnabled with BIRMarketsEnabled as null', () => {
      component['BIRMarketsEnabled'] = null;
      expect(component['isBirMarketEnabled']()).toBeFalsy();
    });
  });
  describe('isBIRSignpostAvailable', () => {
    it('isBIRSignpostAvailable with drilldownTagNames as null', () => {
      component['isHR'] = true;
      expect(component['isBIRSignpostAvailable']({drilldownTagNames: null} as any)).toBeFalsy();
    });
  });
  describe('direct navigation', () => {
    const sortedMarkets = [
      { label: 'Market0', path: 'market0' },
      { label: 'Market1', path: 'market1' },
      { label: 'Market2', path: 'market2' },
      { label: 'Totepool', path: 'totepool' }
    ] as IMarket[];

    let totePoolLabel, winOrEachWayLabel;

    beforeEach(() => {
      spyOn(component, 'updateLocation');
      ['getMarketByPath', 'getMarketByLabel', 'selectFallbackMarket', 'addTotePoolTab', 'getTotePoolTypeByPath'].forEach(method => {
        const bind = component[method].bind(component);
        component[method] = jasmine.createSpy(method).and.callFake(bind);
      });
      totePoolLabel = 'Totepool';
      winOrEachWayLabel = 'Market1';
      localeService.getString.and.callFake(s => ({ 'uktote.totepool': totePoolLabel, 'sb.winOrEachWay': winOrEachWayLabel })[s]);
      component.eventEntity.sortedMarkets = sortedMarkets;
    });

    describe('to non-totepool market tab', () => {
      it('should ignore the market type subpath and replace the browser location only with market subpath', () => {
        component.selectedMarketPath = 'market2';
        component.selectedMarketTypePath = 'marketType2';
        component.ngOnInit();
        expect(component.selectedMarketTypePath).toEqual(null);
      });

      it('should select the proper tab when valid market subpath is provided', () => {
        component.selectedMarketPath = 'market2';
        component.ngOnInit();

        expect(component['getMarketByPath']).toHaveBeenCalledWith(sortedMarkets, 'market2');
        expect(component['getMarketByLabel']).not.toHaveBeenCalled();
        expect(component['selectFallbackMarket']).toHaveBeenCalledWith({ label: 'Market2', path: 'market2' } as IMarket);
        expect(component.selectedMarket).toEqual('Market2');
      });

      it('should select the default tab when nonexistent market subpath is provided', () => {
        component.selectedMarketPath = 'market4';
        component.ngOnInit();

        expect(component['getMarketByPath']).toHaveBeenCalledWith(sortedMarkets, 'market4');
        expect(component['getMarketByLabel']).toHaveBeenCalledWith(sortedMarkets, 'Market1');
        expect(component['selectFallbackMarket']).toHaveBeenCalledWith({ label: 'Market1', path: 'market1' } as IMarket);
        expect(component.selectedMarket).toEqual('Market1');
      });

      it('should select the first tab when nonexistent market subpath is provided and default tab is also unavailable', () => {
        component.selectedMarketPath = 'market4';
        winOrEachWayLabel = 'Market5';
        component.ngOnInit();

        expect(component['getMarketByPath']).toHaveBeenCalledWith(sortedMarkets, 'market4');
        expect(component['getMarketByLabel']).toHaveBeenCalledWith(sortedMarkets, 'Market5');
        expect(component['selectFallbackMarket']).toHaveBeenCalledWith({ label: 'Market0', path: 'market0' } as IMarket);
        expect(component.selectedMarket).toEqual('Market0');
      });
    });

    describe('to totepool market tab', () => {
      const pools = [
        { type: 'UEXA' },
        { type: 'UTRI' },
        { type: 'USW' }
      ];

      beforeEach(() => {
        ukToteService.getPoolsForEvent.and.returnValue(observableOf(pools));
        component.selectedMarketPath = 'totepool';
      });

      describe('when totepool is enabled and pools are available', () => {
        describe('should not change the browser location within this component', () => {
          it('on successful navigation', () => {
            component.selectedMarketTypePath = 'trifecta';
          });

          it('on failed navigation', (() => {
            component.selectedMarketTypePath = 'placepoo';
          }));

          afterEach(fakeAsync(() => {
            component.ngOnInit();
            tick(100);
            expect(component.updateLocation).not.toHaveBeenCalled();
          }));
        });

        it('should return the proper pooltype switcher tab id when valid pooltype subpath is provided', fakeAsync(() => {
          component.selectedMarketTypePath = 'trifecta';
          component.ngOnInit();
          tick(100);
          expect(component['getTotePoolTypeByPath']).toHaveBeenCalledWith(UK_TOTE_CONFIG.poolTypesMap, 'trifecta');
          expect(component.selectedMarket).toEqual('Totepool');
          expect(component.selectedMarketType).toEqual('UTRI');
        }));

        describe('should return null as pooltype switcher tab id', () => {
          it('when nonexistent pooltype subpath is provided', () => {
            component.selectedMarketTypePath = 'placepoo';
          });

          it('when provided pooltype subpath is not present in event pools', () => {
            component.selectedMarketTypePath = 'quadpot';
          });

          it('when provided pooltype subpath is not supported', () => {
            component.selectedMarketTypePath = 'swinger';
          });

          afterEach(fakeAsync(() => {
            component.ngOnInit();
            tick(100);
            expect(component.selectedMarket).toEqual('Totepool');
            expect(component.selectedMarketType).toEqual(null);
          }));
        });
      });

      describe('it should switch to default market', () => {
        it('when UK totepool is disabled in CMS and event.isUKorIRE is true', () => {
          cmsObservableResult = { TotePools: { Enable_UK_Totepools: false } };
          component.eventEntity.isUKorIRE = true;
        });
        it('when Int totepool is disabled in CMS and event.isUKorIRE is false', () => {
          cmsObservableResult = { InternationalTotePool: { Enable_International_Totepools: false } };
          component.eventEntity.isUKorIRE = false;
        });
        it('when poolEventIds are empty', () => {
          ukToteService.getTotePoolEventIds.and.returnValue(observableOf([]));
        });
        it('when there are no pools for event', () => {
          ukToteService.getPoolsForEvent.and.returnValue(observableOf([]));
        });
        afterEach(fakeAsync(() => {
          component.ngOnInit();
          tick(100);

          expect(component['getMarketByLabel']).toHaveBeenCalledWith(sortedMarkets, 'Market1');
          expect(component['selectFallbackMarket']).toHaveBeenCalledWith({ label: 'Market1', path: 'market1' } as any);
        }));
      });
    });

    describe('market description enabled', () => {
      const sortMarkets = [
        { label: 'Market0', path: 'market0' },
        { label: 'Market1', path: 'market1' },
        { label: 'Market2', path: 'market2' },
        { label: 'Totepool', path: 'totepool' }
      ] as IMarket[];
      beforeEach(() => {
        cmsObservableResult.RacingEDPMarketsDescription.enabled = true;
      });
      it('should call cms service to fetch racing edp markets if market description is enabled', () => {
        horseracing.getSortingFromCms = jasmine.createSpy('getSortingFromCms').and.returnValue(sortMarkets);
        component.ngOnInit();
        expect(cmsService.getRacingEDPMarkets).toHaveBeenCalled();
      });
    });
  });

  it('stopPropagation', () => {
    const testFn = {
      stopPropagation: jasmine.createSpy()
    };

    component.stopPropagation(testFn);
    expect(testFn.stopPropagation).toHaveBeenCalled();
  });

  it('trackByIndex', () => {
    expect(component.trackByIndex(123)).toBe(123);
  });

  it('trackById', () => {
    expect(component.trackById(null, { id: 123 })).toBe(123);
  });

  it('summaryMoreLess', () => {
    component.showLess = true;
    component.eventEntity.racingFormEvent.overview = 'test_string, test_string, test_string, test_string,' +
      'test_string, test_string, test_string, test_string, test_string, test_string, test_string, test_string,';
    component.summaryMoreLess();

    expect(component.showLess).toBeFalsy();
    expect(component.racingPostSummary.length).toBe(154);

    component.summaryMoreLess();
    expect(component.showLess).toBeTruthy();
    expect(component.racingPostSummary.length).toBe(104);
  });

  it('displayMarketPanel', () => {
    const market = component.eventEntity.markets[0];
    component.selectedMarket = 'test_string';
    component.isGroupedMarket = jasmine.createSpy('isGroupedMarket');

    market.isTopFinish = true;
    market.collapseMarket = false;
    expect(component.displayMarketPanel(market)).toBeTruthy();

    market.isTopFinish = false;
    market.insuranceMarkets = true;
    expect(component.displayMarketPanel(market)).toBeTruthy();

    market.insuranceMarkets = false;
    market.isOther = true;
    expect(component.displayMarketPanel(market)).toBeTruthy();

    market.isOther = false;
    market.isWO = true;
    expect(component.displayMarketPanel(market)).toBeTruthy();

    market.collapseMarket = true;
    expect(component.displayMarketPanel(market)).toBeFalsy();
    expect(localeService.getString).toHaveBeenCalledTimes(25);

    const areEmptyOutcomes: any = {};
    areEmptyOutcomes.outcomes = [] as any;
    areEmptyOutcomes.label = 'test';
    expect(component.displayMarketPanel(areEmptyOutcomes)).toBeFalsy();
    expect(component.isGroupedMarket).toHaveBeenCalledTimes(4);

    market.label = 'test';
    market.isTopFinish = true;
    market.collapseMarket = false;
    component.isRacingSpecialsCondition = false;
    expect(component.displayMarketPanel(market)).toBeTruthy();

    component.isRacingSpecialsCondition = true;
    market.label = 'To Finish';
    expect(component.displayMarketPanel(market)).toBeTruthy();
  });

  describe('displayMarketHeader', () => {
    it('main logic', () => {
      const market = component.eventEntity.markets[0];
      component.selectedMarket = 'test_string';
      market.isTopFinish = false;
      market.insuranceMarkets = false;
      market.isWO = false;
      market.isOther = false;
      market.name = 'test_name';

      expect(component.displayMarketHeader(market)).toBe('');

      market.isTopFinish = true;
      expect(component.displayMarketHeader(market)).toBe('test_name');

      market.isTopFinish = false;
      market.insuranceMarkets = true;
      expect(component.displayMarketHeader(market)).toBe('test_name');

      market.insuranceMarkets = false;
      market.isWO = true;
      expect(component.displayMarketHeader(market)).toBe('test_name');

      market.isWO = false;
      market.isOther = true;
      expect(component.displayMarketHeader(market)).toBe('test_name');

      market.isOther = false;
      market.isAntepost = 'true';
      expect(component.displayMarketHeader(market)).toBe('test_name');

      horseracing.isRacingSpecials.and.returnValue(true);
      market.templateMarketName = 'test_market_template';
      expect(component.displayMarketHeader(market)).toBe('test_name');

      market.isAntepost = 'false';
      expect(localeService.getString).toHaveBeenCalledTimes(42);
    });

    it('if it is win or each way market', () => {
      horseracing.isRacingSpecials.and.returnValue(true);
      const market = component.eventEntity.markets[0];
      component.selectedMarket = 'test_string';
      market.isTopFinish = false;
      market.insuranceMarkets = false;
      market.isWO = false;
      market.isOther = false;
      market.templateMarketName = 'Win or Each Way';
      market.name = 'Win or Each Way';
      const actualResult = component.displayMarketHeader(market);

      expect(horseracing.isRacingSpecials).toHaveBeenCalled();
      expect(actualResult).toBe('');
    });
  });

  it('change', () => {
    spyOn(component, 'updateLocation');
    spyOn(component, 'track');
    component.eventEntity.markets[0].collapseMarket = true;
    component.sortOptionsEnabled = true;
    component.sortBy = 'PRICE';
    component.isRaceCard = false;

    expect(component.eventEntity.markets[0].collapseMarket).toBeTruthy();
    component.change({ label: 'test_label', path: 'test_path' } as IMarket);

    expect(component.selectedMarket).toBe('test_label');
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.CLOSE_SORT_BY);
    expect(component.updateLocation).toHaveBeenCalledWith('test_path');
    expect(component.track).toHaveBeenCalledWith('test_label');
    expect(component.eventEntity.markets[0].collapseMarket).toBeFalsy();
    expect(component.isForecastTricast).toEqual(false);
  });

  it('change', () => {
    spyOn(component, 'updateLocation');
    spyOn(component, 'track');
    component.eventEntity.markets[0].collapseMarket = true;
    component.sortOptionsEnabled = true;
    component.sortBy = 'PRICE';
    component.isRaceCard = true;

    expect(component.eventEntity.markets[0].collapseMarket).toBeTruthy();
    component.change({ label: 'test_label', path: 'test_path' } as IMarket);

    expect(component.selectedMarket).toBe('test_label');
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.CLOSE_SORT_BY);
    expect(component.eventEntity.markets[0].collapseMarket).toBeFalsy();
    expect(component.isForecastTricast).toEqual(false);
  });

  it('playStream on wrapper', () => {
    component.filter = 'showVideoStream';
    component.isWrapper = true;
    spyOn<any>(component, 'handleNativeVideoPlayer').and.callThrough();

    component.playStream({ preventDefault: () => { } } as any);

    expect(component.preloadStream).toBeTruthy();
    expect(component.streamControl.playLiveSim).toHaveBeenCalledWith(false);
    expect(nativeBridgeService.hideVideoStream).toHaveBeenCalled();
    expect(pubSubService.subscribe).toHaveBeenCalled();
    expect(component['handleNativeVideoPlayer']).toHaveBeenCalled();
    expect(component['isVideoHandled']).toBeTrue();
  });

  it('should not call handleNativeVideoPlayer', () => {
    component['isVideoHandled'] = true;
    spyOn<any>(component, 'handleNativeVideoPlayer');

    component.playStream({ preventDefault: () => { } } as any);

    expect(component['handleNativeVideoPlayer']).not.toHaveBeenCalled();
    expect(component['isVideoHandled']).toBeTrue();
  });

  it('playStream not on wrapper', () => {
    component.filter = 'showVideoStream';
    component.isWrapper = false;

    component.playStream({ preventDefault: () => { } } as any);

    expect(component.preloadStream).toBeTruthy();
    expect(component.streamControl.playLiveSim).toHaveBeenCalledWith(false);
    expect(nativeBridgeService.hideVideoStream).not.toHaveBeenCalled();
    expect(pubSubService.subscribe).toHaveBeenCalled();
  });

  it('playLiveSim', () => {
    const event = component.eventEntity;

    component.playLiveSim({ preventDefault: () => { } } as any);

    expect(streamTrackingService.checkIdForDuplicates).toHaveBeenCalledWith(event.id, 'preSim');
    expect(timeService.getCurrentTime).toHaveBeenCalled();
    expect(component.filter).toBe('showLiveSim');
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
      eventCategory: 'streaming',
      eventAction: 'click',
      eventLabel: 'watch pre sim',
      sportID: event.categoryId,
      typeID: event.typeId,
      eventID: event.id
    });
    expect(streamTrackingService.addIdToTrackedList).toHaveBeenCalledWith(event.id, 'preSim');
    expect(component.streamControl.hideStream).toHaveBeenCalled();
    expect(component.streamControl.playLiveSim).toHaveBeenCalledWith(true);
  });

  describe('track', () => {
    it('track (uk)', () => {
      component.track('test_string');
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'uk tote',
        eventAction: 'entry',
        eventLabel: 'main tab'
      });
    });

    it('track (international)', () => {
      component.eventEntity.isUKorIRE = false;
      component.track('test_string');
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'international tote',
        eventAction: 'entry',
        eventLabel: 'main tab'
      });
    });
  });

  describe('#setMarketsInfo', () => {
    it('setMarketsInfo', () => {
      component.expandedSummary = [];
      component['setMarketsInfo']({ outcomes: [
        { name: 'unnamed favourite', isFavourite: true }, { name: '', isFavourite: false}
      ] } as any, 0);

      expect(component.expandedSummary[0].length).toEqual(1);
    });
  });

  it('modifyMarkets', () => {
    component['isValidRunnerNumber'] = jasmine.createSpy().and.returnValue(true);

    const event = component.eventEntity;
    const outcome = event.markets[0].outcomes[0];

    expect(outcome.isValidRunnerNumber).toBeFalsy();

    component.modifyMarkets(event, 'greyhound');

    expect(outcome.isValidRunnerNumber).toBeTruthy();
    expect(component['isValidRunnerNumber']).toHaveBeenCalledWith(outcome.runnerNumber);
    expect(event.silksAvailable).toBeTruthy();
  });

  it('modifyMarkets with termsBeforeMarketAvailable', () => {
    const event = component.eventEntity;
    event.markets[0].isEachWayAvailable = false;
    event.markets[0].isGpAvailable = undefined;
    event.markets[0].drilldownTagNames = '';
    event.markets[0].cashoutAvail = 'N';
    event.markets[0].viewType = 'NotHandicaps';
    event.uiClass = undefined;

    component.modifyMarkets(event, 'horseracing');

    expect(component.termsBeforeMarketAvailable).toEqual({275108045: undefined});
  });

  it('modifyMarkets with termsBeforeMarketAvailable', () => {
    const event = component.eventEntity;

    event.markets[0].isEachWayAvailable = true;

    component.modifyMarkets(event, 'horseracing');

    expect(component.termsBeforeMarketAvailable).toEqual({275108045: true});
  });

  it('modifyMarkets with termsBeforeMarketAvailable', () => {
    const event = component.eventEntity;
    event.markets[0].isGpAvailable = true;

    component.modifyMarkets(event, 'horseracing');

    expect(component.termsBeforeMarketAvailable).toEqual({275108045: true});
  });

  it('modifyMarkets with termsBeforeMarketAvailable', () => {
    const event = component.eventEntity;
    event.markets[0].drilldownTagNames = 'EVFLAG_MB';

    component.modifyMarkets(event, 'horseracing');

    expect(component.termsBeforeMarketAvailable).toEqual({275108045: true});
  });

  it('isAntepostMarket', () => {
    component.eventEntity.markets[0].isAntepost = 'true';
    expect(component.isAntepostMarket()).toBeTruthy();

    component.eventEntity.markets[0].isAntepost = null;
    expect(component.isAntepostMarket()).toBeFalsy();
  });

  describe('#formEdpUrl', () => {
    it('should formEdpUrl with origin', () => {
      component.origin = 'next-races';
      routingHelperService.formResultedEdpUrl.and.returnValue('edpUrl?origin=next-races');
      const result = component.formEdpUrl(component.eventEntity);
      expect(routingHelperService.formResultedEdpUrl).toHaveBeenCalledWith(component.eventEntity, '?origin=next-races');

      expect(result).toContain('?origin');
    });

    it('should formEdpUrl without origin', () => {
      const result = component.formEdpUrl(component.eventEntity);
      expect(routingHelperService.formResultedEdpUrl).toHaveBeenCalledWith(component.eventEntity, '');

      expect(result).not.toContain('?origin');
    });
  });

  it('goToEdpUrl', () => {
    spyOn(component, 'formEdpUrl');
    component.goToEdpUrl(component.eventEntity);
    expect(component.formEdpUrl).toHaveBeenCalled();
    expect(router.navigateByUrl).toHaveBeenCalled();
  });


  it('isLpAvailable', () => {
    component.isLpAvailable(null);
    expect(lpAvailabilityService.check).toHaveBeenCalledWith(null);
  });

  it('isLpAvailable', () => {
    component.isLpAvailable(null);
    expect(lpAvailabilityService.check).toHaveBeenCalledWith(null);
  });


  it('setOutcomeFavourite', () => {
    let outcome = {
      isFavourite: null,
      name: 'Unnamed Favourite',
      outcomeMeaningMinorCode: 0
    };

    component.setOutcomeFavourite(outcome as IOutcome);
    expect(outcome.isFavourite).toBeTruthy();

    outcome = {
      isFavourite: null,
      name: 'Unnamed 2nd Favourite',
      outcomeMeaningMinorCode: 0
    };

    component.setOutcomeFavourite(outcome as IOutcome);
    expect(outcome.isFavourite).toBeTruthy();

    outcome = {
      isFavourite: null,
      name: null,
      outcomeMeaningMinorCode: 1
    };

    component.setOutcomeFavourite(outcome as IOutcome);
    expect(outcome.isFavourite).toBeTruthy();
  });

  it('showMeetingsList', () => {
    component.showMeetings = false;
    component.showMeetingsList();

    expect(component.showMeetings).toBeTruthy();
    expect(windowRef.nativeWindow.scrollTo).toHaveBeenCalledWith(0, 0);
  });

  it('showMeetingsList for greyhounds ', () => {
    component.showMeetings = false;
    component.sportName = 'greyhounds';
    component.showMeetingsList();

    expect(component.showMeetings).toBeTruthy();
    expect(windowRef.nativeWindow.scrollTo).toHaveBeenCalledWith(0, 0);
  });

  it('isGroupedRaceMarket', () => {
    const name = 'To Finish Second';
    component.eventEntity.markets[0].name = name;
    expect(component.isGroupedRaceMarket(component.eventEntity.markets[0])).toBe(name);
  });

  it('going', () => {
    expect(component.going).toBe('test_string');
    expect(localeService.getString['calls'].argsFor(0)).toEqual(['racing.racingFormEventGoing.G']);
  });
  it('raceType', () => {
    component.eventEntity.racingFormEvent.raceType = 'type';
    expect(component.raceType).toBe('test_string');
    expect(localeService.getString['calls'].argsFor(0)).toEqual(['racing.raceType.type']);
  });

  it('isGroupedMarket', () => {
    component.selectedMarket = 'To Finish';
    expect(component.isGroupedMarket()).toBeTruthy();

    component.selectedMarket = 'Top Finish';
    expect(component.isGroupedMarket()).toBeTruthy();

    component.selectedMarket = 'Place Insurance';
    expect(component.isGroupedMarket()).toBeTruthy();

    component.selectedMarket = 'To be falsy';
    expect(component.isGroupedMarket()).toBeFalsy();
  });

  it('formatAntepostTerms', () => {
    expect(component.formatAntepostTerms('antepost odds places 123, 1,2,3')).toBe('antepost Odds Places 123, 1,2,<strong>3</strong>');
  });

  it('showTab', () => {
    expect(component.showTab({} as any, { drilldownTagNames: 'EVFLAG_AP,321' } as any)).toBeFalsy();
    expect(component.showTab({ drilldownTagNames: 'EVFLAG_AP,123' } as any, { drilldownTagNames: 'EVFLAG_AP,321' } as any)).toBeTruthy();
    expect(component.showTab({} as any, {} as any)).toBeTruthy();
  });

  it('onPlayLiveStreamError', () => {
    const error = { value: 'error' };
    createComponent();
    component.isWrapper = false;
    component.filter = 'test_string';

    component.onPlayLiveStreamError(error);
    expect(component.filter).toBe('test_string');

    createComponent();
    watchRulesService.isInactiveUser.and.returnValue(false);
    component.isWrapper = true;

    component.onPlayLiveStreamError(error);
    expect(component.filter).toBe('hideStream');
  });

  it('onPlayLiveStreamError: should not hide stream if user get inactive qualification error', () => {
    const error = { value: 'inactiveError' };
    createComponent();
    component.filter = 'test_string';
    watchRulesService.isInactiveUser.and.returnValue(true);
    component.isWrapper = true;

    component.onPlayLiveStreamError(error);
    expect(component.filter).toBe('test_string');
  });

  it('applySortBy', () => {
    spyOn(component, 'setOutcomeFavourite');
    component.sortBy = null;
    component.expandedSummary = [];
    component['applySortBy']('PRICE');

    expect(component.sortBy).toBe('PRICE');
    expect(sbFilters.orderOutcomeEntities).toHaveBeenCalledWith(jasmine.any(Object), true, true, true, false, false, true);
    expect(component.expandedSummary).toEqual([[false]]);
    expect(component.setOutcomeFavourite).toHaveBeenCalledWith(jasmine.any(Object));

    component['applySortBy']('RACECARD');
    expect(component.sortBy).toBe('RACECARD');
    expect(sbFilters.orderOutcomeEntities).toHaveBeenCalledWith(jasmine.any(Object), true, true, true, false, false, true);
  });

  describe('syncToApplySorting', () => {
    const unSortedMarkets = [{
      isLpAvailable: 'true',
      outcomes: [{
        runnerNumber: 3,
        name: 'aname',
        prices: []
      }, {
        runnerNumber: 7,
        name: 'zname',
        prices: []
      }, {
        runnerNumber: undefined,
        name: 'bname',
        prices: []
      }]
    }];

    const sortedByName = [{
      runnerNumber: 3,
      name: 'aname',
      prices: [],
      isFavourite: false
    }, {
      runnerNumber: undefined,
      name: 'bname',
      prices: [],
      isFavourite: false
    }, {
      runnerNumber: 7,
      name: 'zname',
      prices: []
    }];

    beforeEach(() => {
      component['applySortBy'] = jasmine.createSpy();
      component['updateGATracking'] = jasmine.createSpy();
      component.sortOptionsEnabled = true;
    });

    it('should apply sorting on init and subscription', () => {
      component.sortBy = 'price';
      component['syncToApplySorting']();

      expect(pubSubService.subscribe).toHaveBeenCalledWith('RacingEventComponent', pubSubService.API.SORT_BY_OPTION, jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith('racingEvent', pubSubService.API.LIVE_MARKET_FOR_EDP, jasmine.any(Function));
      expect(component['applySortBy']).toHaveBeenCalledWith('price');
    });

    it('should apply sorting by name', () => {
      sbFilters.orderOutcomesByName = jasmine.createSpy().and.returnValue(sortedByName);
      component.expandedSummary = [];
      component.sortBy = 'Name';
      component.eventEntity.markets = unSortedMarkets as any;
      component['syncToApplySorting']();

      expect(component.eventEntity.markets[0].outcomes as any).toEqual(sortedByName);
    });

    it('should apply sorting by price', () => {
      component.expandedSummary = [];
      component.sortBy = 'Price';
      component.eventEntity.markets = unSortedMarkets as any;
      component.applySortBy = jasmine.createSpy('applySortBy');
      component['syncToApplySorting']();
      expect(component.applySortBy).toHaveBeenCalledWith('Price');
    });
    it('#Should call updateGATracking and applySortBy', () => {
      component.isGreyhoundEdp = true;
      component.sortBy = 'price';
      component['syncToApplySorting']();
      expect(component.applySortBy).toHaveBeenCalledWith('price');
    });
  });

  describe('filterDate', () => {
    let result;

    beforeEach(() => {
      result = component.filterDate('2018-10-30');
    });

    it('should format day number', () => {
      expect(timeService.formatByPattern['calls'].argsFor(0)).toEqual(['2018-10-30', 'd', null, true]);
    });

    it('should get day suffix', () => {
      expect(tools.getDaySuffix).toHaveBeenCalledWith('20181030');
    });

    it('should format day name', () => {
      expect(timeService.formatByPattern['calls'].argsFor(1)).toEqual(['2018-10-30', 'EEEE', null, true]);
    });

    it('should format mounth name', () => {
      expect(timeService.formatByPattern['calls'].argsFor(2)).toEqual(['2018-10-30', 'MMMM', null, true]);
    });

    it('should return formatted date', () => {
      expect(result).toBe('2018-10-30 2018-10-30th 2018-10-30');
    });
  });

  it('filterDate with year', () => {
    const result = component.filterDate('2018-10-30', true);

    expect(result).toBe('2018-10-30 2018-10-30th 2018-10-30 2018');
  });

  it('isValidRunnerNumber', () => {
    expect(component['isValidRunnerNumber']('10')).toBeFalsy();
    expect(component['isValidRunnerNumber'](0)).toBeFalsy();
    expect(component['isValidRunnerNumber']('4')).toBeTruthy();
  });

  it('addTotePoolTab', () => {
    component.toteLabel = 'Totepool';
    component['addTotePoolTab']();
    const markets = component.eventEntity.sortedMarkets;

    expect(markets[markets.length - 1].label).toEqual('Totepool');
  });

  describe('addForecastTricastTabs', () => {
    it('should add forecast tricast markets', () => {
      const markets = component.eventEntity.sortedMarkets;
      component.eventEntity.markets = [{
          templateMarketName: 'Win or Each Way',
          outcomes: [
            {id: '944140636', isFavourite: false, displayOrder: 5},
            {id: '944140637', isFavourite: false, displayOrder: 3},
            {id: '944140638', isFavourite: true, displayOrder: 1},
            {id: '944140638', isFavourite: false, displayOrder: 6},
            {id: '944140638', isFavourite: false, displayOrder: 7},
          ],
          ncastTypeCodes: 'CF, CT'
        }] as any;
      const config = {
        forecastTricastRacing: {
          enabled: true
        },
        order: { EVENTS_ORDER : {}}
      };
      component.selectedMarketPath = FORECAST_CONFIG.tricastMarketPath;
      component['addForecastTricastTabs'](config);

      expect(component.forecastTricastMarket.templateMarketName).toEqual('Win or Each Way');
      expect(component.forecastTricastMarket.outcomes[0].id).toEqual('944140637');
      expect(component.forecastTricastMarket.outcomes[1].id).toEqual('944140636');
      expect(component.forecastTricastMarket.outcomes.length).toEqual(4);
      expect(markets[1].label).toEqual('Forecast');
      expect(markets[2].label).toEqual('Tricast');
      expect(component.selectedMarket).toEqual(component.tricastLabel);

      component.selectedMarketPath = 'test';
      component['addForecastTricastTabs'](config);
      expect(component.selectedMarket).toBeDefined();
      expect(component.selectedMarket).toEqual(component.tricastLabel);

      component.selectedMarketPath = FORECAST_CONFIG.forecastMarketPath;
      component['addForecastTricastTabs'](config);
      expect(component.selectedMarket).toEqual(component.forecastLabel);
    });

    it('should not add forecast tricast markets when cms toggle is not enabled', () => {
      component.eventEntity.sortedMarkets.splice(1, component.eventEntity.sortedMarkets.length - 1);
      const markets = component.eventEntity.sortedMarkets;
      const config = {
        forecastTricastRacing: {
          enabled: false
        }
      };
      component['addForecastTricastTabs'](config);

      expect(markets.length).toEqual(1);
    });

    it('should not add forecast tricast markets when there are no enough selections', () => {
      const markets = component.eventEntity.sortedMarkets;
      component.eventEntity.markets = [{
        templateMarketName: 'Win or Each Way',
        outcomes: [
          {id: '944140636', isFavourite: false, displayOrder: 5},
        ],
        ncastTypeCodes: 'CF, CT'
      }] as any;
      const config = {
        forecastTricastRacing: {
          enabled: true
        }
      };
      component['addForecastTricastTabs'](config);

      expect(markets.length).toEqual(1);
    });
  });

  describe('sortOptionsEnabledFn', () => {
    it('general flow', () => {
      component.sortOptionsEnabled = false;
      component.selectedMarket = 'Test Tab';
      component.toteLabel = 'Totepool';
      const market = component.eventEntity.markets[0];
      expect(component.sortOptionsEnabledFn(true, false, market)).toBeFalsy();

      component.sortOptionsEnabled = true;
      expect(component.sortOptionsEnabledFn(true)).toBeTruthy();
      expect(component.sortOptionsEnabledFn(true, false, market)).toBeTruthy();

      market.outcomes[0].prices = [];
      expect(component.sortOptionsEnabledFn(true, false, market)).toBeFalsy();

      expect(component.sortOptionsEnabledFn(false)).toBeFalsy();

      component.selectedMarket = 'Totepool';
      expect(component.sortOptionsEnabledFn(true)).toBeFalsy();
    });

    it('should not show sort option when there are no prices and no market in params', () => {
      component.selectedMarket = 'Top Finish';
      component.eventEntity.sortedMarkets = [
        {name: 'Top Finish', markets: [{id: '14213044'}]}, {name: 'More Markets'}
      ] as any;
      const market = undefined;

      expect(component.sortOptionsEnabledFn(false, true, market)).toBeFalsy();
    });

    it('should show sort option when there are prices and and no market in params', () => {
      component.sortOptionsEnabled = true;
      component.selectedMarket = 'Top Finish';
      component.eventEntity.sortedMarkets = [
        {name: 'Top Finish', markets: [{id: '14213044', outcomes: [
              {prices: [{id: '1'}, {id: '2'}], isLpAvailable: true}
         ], isLpAvailable: true}]},
        {name: 'More Markets'}
      ] as any;
      const market = undefined;

      expect(component.sortOptionsEnabledFn(true, true, market)).toBeTruthy();
    });

    it('should be truthy if selectedMarket is not defined', () => {
      component.sortOptionsEnabled = true;
      component.selectedMarket = undefined;
      component.toteLabel = 'Tote';
      component.eventEntity.sortedMarkets = [
        {name: 'Win or Each Way', label: 'Win or E/W'},
        {label: 'Forecast', path: 'forecast'},
        {label: 'Totepool', path: 'totepool'}
      ] as any;

      expect(component.sortOptionsEnabledFn(true, true)).toBeTruthy();
    });

    it('should be truthy if selected market do not have markets', () => {
      component.sortOptionsEnabled = true;
      component.selectedMarket = 'Win or Each Way';
      component.toteLabel = 'Tote';
      component.eventEntity.sortedMarkets = [
        {name: 'Win or Each Way', label: 'Win or E/W'},
        {label: 'Forecast', path: 'forecast'},
        {label: 'Totepool', path: 'totepool'}
      ] as any;

      expect(component.sortOptionsEnabledFn(true, true)).toBeTruthy();
    });

    it('should be falsy if prices are not appropriate prices to sort', () => {
      component.sortOptionsEnabled = true;
      component.selectedMarket = 'Win Only';
      component.eventEntity.sortedMarkets = [
        {name: 'Win or Each Way', label: 'Win or E/W'},
        {label: 'Forecast', path: 'forecast'},
        {label: 'Totepool', path: 'totepool'},
        {name: 'Win Only', label: 'Win Only', outcomes: [{prices: []}, {prices: []}]},
      ] as any;

      expect(component.sortOptionsEnabledFn(true, true)).toBeFalsy();
    });

    it('should be truthy if there are appropriate prices to sort', () => {
      component.sortOptionsEnabled = true;
      component.selectedMarket = 'Win Only';
      component.eventEntity.sortedMarkets = [
        {name: 'Win or Each Way', label: 'Win or E/W'},
        {label: 'Forecast', path: 'forecast'},
        {label: 'Totepool', path: 'totepool'},
        {name: 'Win Only', label: 'Win Only', isLpAvailable: true,
          outcomes: [{prices: [{priceDen: 12, priceNum: 4}]}]},
      ] as any;

      expect(component.sortOptionsEnabledFn(true, true)).toBeTruthy();
    });
  });

  describe('initialize breadcrumbs', () => {
    const breadcrumbsItems = [{
      name: 'test_string',
      targetUri: '/horse-racing/featured'
    }, {
      name: 'ChepstowTN'
    }];

    it('should initialize meeting breadcrumbs if sportName is horseracing', () => {
      component.origin = null;
      component.sportName = 'horseracing';
      component['initializeBreadcrumbs']();
      expect(component.breadcrumbsItems).toEqual(breadcrumbsItems);
    });

    it('should initialize breadcrumbs for next races', () => {
      component.origin = 'next races origin';
      component.sportName = 'horseracing';
      component['initializeBreadcrumbs']();
      expect(component.breadcrumbsItems[1].name).toEqual('test_string');
    });

    it('should initialize breadcrumbs for offers and features', () => {
      component.origin = 'offers-and-featured';
      component.sportName = 'horseracing';
      component['initializeBreadcrumbs']();
      expect(component.breadcrumbsItems[1].name).toEqual('Offers and Featured');
    });

    it('should initialize next races breadcrumbs if sportName is greyhound', () => {
      breadcrumbsItems[0].targetUri = '/greyhound-racing/today';
      component.origin = null;
      component.sportName = 'greyhound';
      component['initializeBreadcrumbs']();
      expect(component.breadcrumbsItems).toEqual(breadcrumbsItems);
    });

    it('should initialize next races breadcrumbs', () => {
      breadcrumbsItems[1].name = 'test_string';
      component.origin = 'next races origin';
      component.sportName = 'greyhound';
      component['initializeBreadcrumbs']();
      expect(component.breadcrumbsItems).toEqual(breadcrumbsItems);
    });

    it('should initialize next races breadcrumbs', () => {
      breadcrumbsItems[1].name = 'test_string';
      component.origin = 'next races origin';
      component.sportName = 'greyhound';
      component['initializeBreadcrumbs']();
      expect(component.breadcrumbsItems).toEqual(breadcrumbsItems);
    });

    it('should initialize next races breadcrumbs if there are no origin and eventEntity', () => {
      breadcrumbsItems[1].name = undefined;
      component.origin = undefined;
      component.eventEntity = undefined;
      component.sportName = 'greyhound';
      component['initializeBreadcrumbs']();
      expect(component.breadcrumbsItems).toEqual(breadcrumbsItems);
    });
  });

  describe('initialize breadcrumbs', () => {
    it('should get active events', () => {
      component.racingsMap = {
        test: [{
          isResulted: false
        }]
      };

      component.selectEvent('test');

      expect(filterService.orderBy).toHaveBeenCalledWith([{ isResulted: false }], ['startTime']);
      expect(routingHelperService.formEdpUrl).toHaveBeenCalled();
      expect(router.navigateByUrl).toHaveBeenCalledWith('url');
    });
    it('should not get active events', () => {
      component.racingsMap = {
        test: [{
          isResulted: true,
          isStarted: true,
          isLiveNowEvent: false
        }]
      };

      component.selectEvent('test');
      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith(component.racingsMap.test[0]);
    });
  });
  describe('selectEvent', () => {
    it('activeEvents should be sorted by time', () => {
      component.racingsMap = {
        test: [{
          isResulted: false
        }]
      };

      component.selectEvent('test');
      expect(filterService.orderBy).toHaveBeenCalledWith([{ isResulted: false }], ['startTime']);
      expect(routingHelperService.formEdpUrl).toHaveBeenCalled();
      expect(router.navigateByUrl).toHaveBeenCalledWith('url');
    });
    it('activeEvents should not be sorted by time', () => {
      component.racingsMap = {
        test: [{
          isResulted: true,
          isStarted: true,
          isLiveNowEvent: false
        }]
      };

      component.selectEvent('test');
      expect(filterService.orderBy).toHaveBeenCalledWith([], ['startTime']);
      expect(routingHelperService.formEdpUrl).toHaveBeenCalled();
      expect(router.navigateByUrl).toHaveBeenCalledWith('url');
    });
  });
  describe('showRibbonEventName',  () => {
    it('isRibbonEventName should be false', () => {
      component.racingInMeeting = [
        { name: 'name' },
        { name: 'name' }
      ] as any[];
      component.showRibbonEventName();

      expect(component.isRibbonEventName).toBeFalsy();
    });
    it('isRibbonEventName should be true', () => {
      component.racingInMeeting = [
        { name: 'name01' },
        { name: 'name02' }
      ] as any[];
      component.showRibbonEventName();

      expect(component.isRibbonEventName).toBeTruthy();
    });
    it('isRibbonEventName will not be updated', () => {
      component.racingInMeeting = [] as any;
      component.showRibbonEventName();

      expect(component.isRibbonEventName).toBeFalsy();
    });
  });
  describe('ngOnChanges',  () => {
    it('showRibbonEventName will not be called',  () => {
      const changes: any = {};
      spyOn(component, 'showRibbonEventName');
      component.ngOnChanges(changes);

      expect(component.showRibbonEventName).not.toHaveBeenCalled();
    });
    it('showRibbonEventName will be called',  () => {
      const changes: any = {
        racingInMeeting: {
          currentValue: [
            { categoryName: 'Horse Racing' }
          ]
        }
      };
      spyOn(component, 'showRibbonEventName');
      component.ngOnChanges(changes);

      expect(component.showRibbonEventName).toHaveBeenCalledTimes(1);
    });
  });


  it('shoul dcheck isNextRaceEvent information to show right breadcrumb and build EDP URL', () => {
    const startedEventMock: any = {...eventMock};
    startedEventMock.isStarted = 'true';

    component.origin = 'next-races';
    component.eventEntity = startedEventMock;

    const isNextRaceEvent = component['isNextRaceEvent']();
    expect(isNextRaceEvent).toBeFalsy();
  });

  it('shoul dcheck isNextRaceEvent information to show right breadcrumb and build EDP URL', () => {
    component.origin = 'next-races';
    component.eventEntity = eventMock;

    const isNextRaceEvent = component['isNextRaceEvent']();
    expect(isNextRaceEvent).toBeTruthy();
  });

  it('checkIsForecastTricast', () => {
    component['checkIsForecastTricast']('forecast');
    expect(component.isForecastTricast).toBeTruthy();

    component['checkIsForecastTricast']('tricast');
    expect(component.isForecastTricast).toBeTruthy();

    component['checkIsForecastTricast']('win-or-each-way');
    expect(component.isForecastTricast).toBeFalsy();
  });

  describe('@setMarketTabs',  () => {
    beforeEach(() => {
      component.eventEntity = {
        sortedMarkets: [{
          label: 'Win or E/W',
          path: 'Win or E/W'
        }, {
          label: 'Tricast',
          path: 'tricast'
        }]
      } as any;
    });
    it('it should create marketsTabs',  () => {
      component['setMarketTabs']();

      expect(component.marketsTabs).toEqual([{
        onClick: jasmine.any(Function),
        name: 'Win or E/W',
        viewByFilters: 'Win or E/W'
      }, {
        onClick: jasmine.any(Function),
        name: 'Tricast',
        viewByFilters: 'Tricast'
      }]);
    });

    it('it should check onClick Function',  () => {
      component['setMarketTabs']();

      component.marketsTabs[0].onClick(component.eventEntity.sortedMarkets[0]);

      expect(component.selectedMarket).toEqual('Win or E/W');
      expect(component.selectedMarketType).toEqual(null);
      expect(component.isForecastTricast).toEqual(false);
      expect(pubSubService.publish).toHaveBeenCalledTimes(2);
    });

    it('it should sort if marketDescription is enabled (Case: hasMarketType(true))',  () => {
      const sortMarkets = [{
        label: 'Win or E/W',
        path: 'Win or E/W'
      }, {
        label: 'Tricast',
        path: 'tricast'
      }] as IMarket[];
      horseracing.getSortingFromCms = jasmine.createSpy('getSortingFromCms').and.returnValue(sortMarkets);
      component.isMarketDescriptionAvailable = true;
      component['hasMarketType'] = true;
      component['setMarketTabs']();
      expect(component.selectedMarket).toBeUndefined();
      expect(component.marketsTabs).toEqual([{
        onClick: jasmine.any(Function),
        name: 'Win or E/W',
        viewByFilters: 'Win or E/W'
      }, {
        onClick: jasmine.any(Function),
        name: 'Tricast',
        viewByFilters: 'Tricast'
      }]);
    });
    it('it should sort if marketDescription is enabled (Case: hasMarketType(false))',  () => {
      const sortMarkets = [{
        label: 'Win or E/W',
        path: 'Win or E/W'
      }, {
        label: 'Tricast',
        path: 'tricast'
      }] as IMarket[];
      horseracing.getSortingFromCms = jasmine.createSpy('getSortingFromCms').and.returnValue(sortMarkets);
      component.isMarketDescriptionAvailable = true;
      component['hasMarketType'] = false;
      component['isRaceCard'] = false;
      component['setMarketTabs']();
      expect(component.selectedMarket).toBe(sortMarkets[0].label);
      expect(component.marketsTabs).toEqual([{
        onClick: jasmine.any(Function),
        name: 'Win or E/W',
        viewByFilters: 'Win or E/W'
      }, {
        onClick: jasmine.any(Function),
        name: 'Tricast',
        viewByFilters: 'Tricast'
      }]);
    });
  });
  describe('native video placeholder flow', () => {
    describe('for wrapper', () => {
      let animationFrameCb;

      beforeEach(() => {
        nativeBridgeService.isWrapper = true;
        windowRef.nativeWindow.requestAnimationFrame.and.callFake(cb => animationFrameCb = cb);
      });
      it('should call nativePlayerSticky', () => {
        spyOn<any>(component, 'nativePlayerSticky');
        component.ngOnInit();
        expect(component['nativePlayerSticky']).toHaveBeenCalled();
      });
      it('should create IS_NATIVE_VIDEO_STICKED subscription', () => {
        component['nativePlayerSticky']();
        expect(pubSubService.subscribe).toHaveBeenCalledWith('RacingEventComponent', 'IS_NATIVE_VIDEO_STICKED', jasmine.any(Function));
      });
      describe('should call handleNativeVideoPlayer with delay', () => {
        it('when nativeVideoPlayerPlaceholder element exists', () => {
          component['handleNativeVideoPlayer']();
          animationFrameCb();
          expect(nativeBridgeService.handleNativeVideoPlayer).toHaveBeenCalledWith({ className: 'native-video-player-placeholder' });
        });
        it('when nativeVideoPlayerPlaceholder element does not exist', () => {
          component.nativeVideoPlayerPlaceholderRef = undefined;
          component['handleNativeVideoPlayer']();
          animationFrameCb();
          expect(nativeBridgeService.handleNativeVideoPlayer).toHaveBeenCalledWith(undefined);
        });
      });
      describe('when IS_NATIVE_VIDEO_STICKED event received', () => {
        const pubsubMap = {};
        beforeEach(() => {
          pubSubService.subscribe.and.callFake((name, subscription, fn) => { pubsubMap[subscription] = fn; });
        });
        it('should publish PIN_TOP_BAR event', () => {
          component.filter = 'hideStream';
          component['nativePlayerSticky']();
          pubsubMap['IS_NATIVE_VIDEO_STICKED'](true);
          expect(pubSubService.publish).toHaveBeenCalledWith('PIN_TOP_BAR', true);
          expect(component.filter).toBe('showVideoStream');
        });
        describe('should call handleNativeVideoPlaceholder', () => {
          it('when nativeVideoPlayerPlaceholder element exists', () => {
            component['nativePlayerSticky']();
            pubsubMap['IS_NATIVE_VIDEO_STICKED'](true);
            expect(nativeBridgeService.handleNativeVideoPlaceholder).toHaveBeenCalledWith(true,
              { className: 'native-video-player-placeholder' });
          });
          it('when nativeVideoPlayerPlaceholder element does not exist', () => {
            component.nativeVideoPlayerPlaceholderRef = undefined;
            component['nativePlayerSticky']();
            pubsubMap['IS_NATIVE_VIDEO_STICKED'](true);
            expect(nativeBridgeService.handleNativeVideoPlaceholder).toHaveBeenCalledWith(true, undefined);
          });
          it('should call updateFloatingMsgTop with', () => {
            component.updateFloatingMsgTop = jasmine.createSpy();
            component.nativeVideoPlayerPlaceholderRef.nativeElement = {style: {height: '20px'}};
            component['nativePlayerSticky']();
            pubsubMap['IS_NATIVE_VIDEO_STICKED'](true);
            expect(component.updateFloatingMsgTop).toHaveBeenCalled();
          });
        });
      });
    });
  });
  describe('handleSpecialsLoaded', () => {
    it('should set specialsLoaded prop to true', () => {
      expect(component.specialsLoaded).toBeFalsy();
      component.handleSpecialsLoaded();
      expect(component.specialsLoaded).toBeTruthy();
    });
  });

  it('@isResultedOrRaceOff', () => {
    const ev = {
      isResulted: true,
      isStarted: false,
      isLiveNowEvent: true
    } as any;
    expect(component.isResultedOrRaceOff(ev)).toBe(true);

    ev.isResulted = false;
    expect(component.isResultedOrRaceOff(ev)).toBe(false);

    ev.isStarted = true;
    expect(component.isResultedOrRaceOff(ev)).toBe(false);

    ev.isLiveNowEvent = false;
    expect(component.isResultedOrRaceOff(ev)).toBe(true);
  });

  describe('@setRacingEDPMarkets', () => {
    it('should set EDP_MARKETS from CMS', () => {
      component.isMarketDescriptionAvailable = true;
      cmsService.getRacingEDPMarkets = jasmine.createSpy().and.returnValue(observableOf(EDP_MARKETS));
      component['setRacingEDPMarkets']();
      expect(cmsService.getRacingEDPMarkets).toHaveBeenCalled();
      expect(pubSubService.subscribe).toHaveBeenCalled();
    });

    it('should set EDP_MARKETS if CMS error', () => {
      component.isMarketDescriptionAvailable = false;
      cmsService.getRacingEDPMarkets = jasmine.createSpy().and.returnValue(throwError(null));
      component['setRacingEDPMarkets']();
      expect(cmsService.getRacingEDPMarkets).not.toHaveBeenCalled();
    });
  });

  describe('#toteForecastTricastMarket', () => {
    it('onExpandSection checker false', () => {
      const expandedSummary = [[false], [false]];
      component.onExpandSection(expandedSummary, 1, 0);

      expect(expandedSummary).toEqual([[false], [true]]);
      expect(component.isInfoHidden.info).toEqual(true);
    });

    it('onExpandSection ', () => {
      const expandedSummary = [[true], [true]];
      component.onExpandSection(expandedSummary, 1, 0);
      component.eventEntity = Object.assign({}, eventMock);

      expect(expandedSummary).toEqual([[true], [false]]);
      expect(component.isInfoHidden.info).toEqual(false);
    });
    it('toggleShowOptions', () => {
      const expandedSummary = [[false, true], [true, false]];
      component.toggleShowOptions(expandedSummary, 1, true);
      component.eventEntity = Object.assign({}, eventMock);

      expect(expandedSummary).toEqual([[false, true], [true, true]]);
    });
    
    it ('#Should call onExpandSection GA Tracking when isGreyhoundEdp is false', () => {
      const expandedSummary = [[true], [true]];
      component.eventEntity = Object.assign({}, eventMock);
      component.isGreyhoundEdp = false;
      component.onExpandSection(expandedSummary, 1, 0);
      
      const expectedParams = ['trackEvent', {
          event: 'trackEvent',
          eventAction: 'race card',
          eventCategory: 'horse racing',
          eventLabel:'show less',
          categoryID: '21',
          typeID: '1909',
          eventID: 11818323
        }];
        expect(component.isGreyhoundEdp).toBeFalsy();
  
        expect(gtmService.push).toHaveBeenCalledWith(...expectedParams);
      });

      it ('#Should call onExpandSection GA Tracking when isGreyhoundEdp is true', () => {
        const expandedSummary = [[false], [false]];
        component.eventEntity = Object.assign({}, eventMock);
        component.isGreyhoundEdp = true;
        component.onExpandSection(expandedSummary, 1, 0);
       
        const expectedParams = ['trackEvent', {
            event: 'trackEvent',
            eventAction: 'race card',
            eventCategory: 'greyhounds',
            eventLabel:'show more',
            categoryID: '21',
            typeID: '1909',
            eventID: 11818323
          }];
          expect(component.isGreyhoundEdp).toBeTruthy();
    
          expect(gtmService.push).toHaveBeenCalledWith(...expectedParams);
        });

    describe('#sponly', () => {
      it('should return false if both SP and LP are present', () => {
        const eventEntity = {
          markets: [{
            priceTypeCodes: 'LP,GP,SP,'
          }]
        } as any;
        const response = component['isSp'](eventEntity);
        expect(response).toBe(false);
      });
      it('should return true if only SP is present', () => {
        const eventEntity = {
          markets: [{
            priceTypeCodes: 'GP,SP,'
          }]
        } as any;
        const response = component['isSp'](eventEntity);
        expect(response).toBe(true);
      });
    });
  });

  describe('#setMarketsTooltip', () => {
    it('should not set secondary markets tooltip, if both conditions does not satisfy', () => {
      const config = {};
      cmsService.getFeatureConfig.and.returnValue(observableOf(config));
      component['setMarketsTooltip']();
      expect(component['secondaryMarketsTooltip']).toBe(undefined);
    });
    it('should not set secondary markets tooltip, if only one condition satisfy', () => {
      const config = {
          enabled: false
      };
      cmsService.getFeatureConfig.and.returnValue(observableOf(config));
      component['setMarketsTooltip']();
      expect(component['secondaryMarketsTooltip']).toBe(undefined);
    });
    it('should set secondary markets tooltip, if both condition satisfy(length > 100)', () => {
      const config = {
          enabled: true,
          title: 'Look below to find out what other markets are available Look below to find out what other markets hie'
      };
      cmsService.getFeatureConfig.and.returnValue(observableOf(config));
      component['setMarketsTooltip']();
      expect(component['secondaryMarketsTooltip']).toBe(`${config.title.substring(0,100)}...`);
    });
    it('should set secondary markets tooltip, if both condition satisfy(lngth < 100)', () => {
      const config = {
          enabled: true,
          title: 'welcome'
      };
      cmsService.getFeatureConfig.and.returnValue(observableOf(config));
      component['setMarketsTooltip']();
      expect(component['secondaryMarketsTooltip']).toBe(config.title);
    });
  });


  describe('#marketsContainer', () => {
    it('should set market container if viewchild exists', () => {
      elementRef.nativeElement.querySelector.and.returnValue({ 'element': 1} as any);
      component['marketDescriptionContainer'] = {} as any;
      expect(component.marketContainer).not.toBeNull();
    });
    it('should set market container if viewchild exists', () => {
      elementRef.nativeElement.querySelector.and.returnValue({ 'element': 1} as any);
      component['marketDescriptionContainer'] = null;
      expect(component.marketContainer).toBeUndefined();
    });
  });

  it('#toggleRacingPostVerdict', () => {
    const expectedParams = ['trackEvent', {
      eventCategory: 'horse racing',
      eventAction: 'race card',
      eventLabel: 'racing post verdict'
    }];

    component.toggleRacingPostVerdict();

    expect(gtmService.push).toHaveBeenCalledWith(...expectedParams);
  });
  it('childComponentLoaded should set initialized to true', () => {
    component.childComponentLoaded();
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  });
  describe('new test case for GA tracking', () => {
    it('#calling toggleShowOptionsGATracking when isGreyhoundEdp is false', () => {
      component.eventEntity = Object.assign({}, eventMock);
      component.isGreyhoundEdp = false;
      component.toggleShowOptionsGATracking(false);
      expect(racingGaService.toggleShowOptionsGATracking).toHaveBeenCalledWith(component.eventEntity, false, false);
    });

    it('#calling toggleShowOptionsGATracking when isGreyhoundEdp is true', () => {
      component.eventEntity = Object.assign({}, eventMock);
      component.isGreyhoundEdp = true;
      component.toggleShowOptionsGATracking(true);
      expect(racingGaService.toggleShowOptionsGATracking).toHaveBeenCalledWith(component.eventEntity, true, true);
    });
  });
  describe('updateFloatingMsgTop', () => {
    it('updateFloatingMsgTop with nativePlayerHeight', () => {
      elementRef.nativeElement.querySelector.and.returnValue({ style: {top: '20px', removeProperty: jasmine.createSpy('removeProperty')}} as any);
      component.updateFloatingMsgTop('200px');
      expect(elementRef.nativeElement.querySelector).toHaveBeenCalledWith('.floating-ihr-msg-sticky');
      expect(windowRef.nativeWindow.getComputedStyle).toHaveBeenCalled();
      windowRef.nativeWindow.getComputedStyle = jasmine.createSpy().and.returnValue({top: null});
      component.updateFloatingMsgTop('200px');
      expect(elementRef.nativeElement.querySelector).toHaveBeenCalledWith('.floating-ihr-msg-sticky');
      expect(windowRef.nativeWindow.getComputedStyle).toHaveBeenCalled();
    });
    it('updateFloatingMsgTop without nativePlayerHeight', () => {
      elementRef.nativeElement.querySelector.and.returnValue({ style: {removeProperty: jasmine.createSpy('removeProperty')}} as any);
      component.updateFloatingMsgTop();
      expect(elementRef.nativeElement.querySelector).toHaveBeenCalledWith('.floating-ihr-msg-sticky');
      expect(windowRef.nativeWindow.getComputedStyle).toHaveBeenCalled();
      elementRef.nativeElement.querySelector.and.returnValue({ style: null} as any);
      component.updateFloatingMsgTop();
      expect(elementRef.nativeElement.querySelector).toHaveBeenCalledWith('.floating-ihr-msg-sticky');
      expect(windowRef.nativeWindow.getComputedStyle).toHaveBeenCalled();
    });
  });

  describe('showWatchAndInsights', () => {
    it('EVFLAG_PVM', () => {
      component.eventEntity = {
        drilldownTagNames:['EVFLAG_PVM'],
        isUKorIRE: true,
        categoryId: HORSE_RACING_CATEGORY_ID
      } as any;
      component.insightsDrillDownTags = ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'];
      expect(component.showWatchAndInsights()).toBeTruthy();
    });

    it('EVFLAG_PVA', () => {
      component.eventEntity = {
        drilldownTagNames:['EVFLAG_PVA'],
        isUKorIRE: true,
        categoryId: HORSE_RACING_CATEGORY_ID
      } as any;
      component.insightsDrillDownTags = ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'];
      expect(component.showWatchAndInsights()).toBeTruthy();
    });

    it('EVFLAG_TEST: should return false', () => {
      component.eventEntity = {
        drilldownTagNames:['EVFLAG_TEST'],
        isUKorIRE: true,
        categoryId: HORSE_RACING_CATEGORY_ID
      } as any;
      component.insightsDrillDownTags = ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'];
      expect(component.showWatchAndInsights()).toBeFalsy();
    });
  });

  describe('#handleEvent EXTRA_PLACE_RACE_OFF subscription', () => {
    let update;
    beforeEach(() => {
      component.racingInMeeting = [component.eventEntity];
      update = component.eventEntity.id;
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === 'EXTRA_PLACE_RACE_OFF') {
          fn(update);
        }
      });
    });

    it('should update event rawIsOffCode to Y', () => {
      component['handleEvent']();
      expect(component.eventEntity.rawIsOffCode).toBeDefined()
    });
  });

  describe('#watchInFullScreen', () => {  
    it('Display streaming in Landscape mode', () => {
      const setGtmDataSpy = spyOn(component as any, 'setGtmData');
      component.watchInFullScreen();
      expect(nativeBridgeService.displayInLandscapeMode).toHaveBeenCalled();
      expect(setGtmDataSpy).toHaveBeenCalled();
    });
  });

  describe('#setGtmData', () => {  
    it('storing GA object', () => {
      component.eventEntity = {
        typeName: 'UK'
      } as any;
      component.setGtmData('test');
      expect(component['gtmService'].push).toHaveBeenCalled();
    });
  });

  describe('Play stream with GA tracking', () => {
    it('playStream on wrapper with watch and insights', () => {
      component.eventEntity = {
        drilldownTagNames:['EVFLAG_PVA'],
        isUKorIRE: true,
        rawIsOffCode: '-',
        categoryId: HORSE_RACING_CATEGORY_ID
      } as any;
      component.filter = 'hideVideoStream';
      component.isWrapper = true;      
      component.insightsDrillDownTags = ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'];     
      const setGtmDataSpy = spyOn(component as any, 'setGtmData');      
      component.playStream({ preventDefault: () => { } } as any);
      expect(setGtmDataSpy).toHaveBeenCalled();
    });
  
    it('playStream on wrapper with watch', () => {
      component.eventEntity = {
        drilldownTagNames:['EVFLAG_PVA'],
        isUKorIRE: true,
        rawIsOffCode: 'Y',
        categoryId: HORSE_RACING_CATEGORY_ID
      } as any;
      component.filter = 'hideVideoStream';
      component.isWrapper = true;      
      component.insightsDrillDownTags = ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'];   
      const setGtmDataSpy = spyOn(component as any, 'setGtmData');      
      component.playStream({ preventDefault: () => { } } as any);
      expect(setGtmDataSpy).toHaveBeenCalled();
    });
  });

  describe('showFullScreen', () => {
    it('Display full screen available option#1', () => {
      component.eventEntity = {
        drilldownTagNames:['EVFLAG_PVM'],
        isUKorIRE: true,
        categoryId: HORSE_RACING_CATEGORY_ID,
        rawIsOffCode: 'Y'
      } as any;
      component.showFullscreen = true;
      component.isWrapper = true;
      component.isFullScreenConfig = true;
      component.fullScreenDrillDownTags = ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'];
      expect(component.showFullScreen()).toBeTruthy();
    });

    it('Display full screen available option#2', () => {
      component.eventEntity = {
        drilldownTagNames:['EVFLAG_PVA'],
        isUKorIRE: true,
        categoryId: HORSE_RACING_CATEGORY_ID,
        rawIsOffCode: 'Y'
      } as any;
      component.showFullscreen = true;
      component.isWrapper = true;
      component.isFullScreenConfig = true;
      component.fullScreenDrillDownTags = ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'];
      expect(component.showFullScreen()).toBeTruthy();
    });

    it('Display full screen available option#3', () => {
      windowRef.nativeWindow.NativeBridge = null;
      component.eventEntity = {
        drilldownTagNames:['EVFLAG_PVA'],
        isUKorIRE: true,
        categoryId: HORSE_RACING_CATEGORY_ID,
        rawIsOffCode: 'Y'
      } as any;
      component.showFullscreen = true;
      component.isWrapper = true;
      component.isFullScreenConfig = true;
      expect(component.showFullScreen()).not.toBeTruthy();
    });    
  });

    /* should call isbogAvailable */
    it('should call isbogAvailable method', () => {
      component.isBOGAvailable(component.eventEntity,false);
      expect(component['isBOGAvailable'](component.eventEntity,false)).toBe(false);
      component.eventEntity.effectiveGpStartTime = new Date(new Date().getTime() - 86400000);
      component.isBOGAvailable(component.eventEntity,true);
      expect(component['isBOGAvailable'](component.eventEntity,true)).toBe(true);
    });

    it('should call isWebStreamAndBet method', () => {
      component['isWebStreamBet'] = true;
      component['filter'] = 'showVideoStream';
      deviceService.isWrapper = true;

      const isWebStreamAndBetVal = component['isWebStreamAndBet']();
      expect(isWebStreamAndBetVal).toBe(true);
    });

  describe('#getSpotlightedSelection', () => {
    it('should return the spotlighted outcome', () => {
      component.eventEntity = { markets: [{ name: 'Win or Each Way', outcomes: [{ runnerNumber: '1' }] }] } as any;
      component.racingPostVerdictData = { tips: [{ saddleNo: '1', name: 'SPOTLIGHT' }] } as any;
      const result = component['getSpotlightedSelection']();
      expect(result.runnerNumber).toEqual('1');
    });
    it('should return null when no spotlighted outcome found', () => {
      component.eventEntity = { markets: [{ name: 'Win or Each Way', outcomes: [{ runnerNumber: '1' }] }] } as any;
      component.racingPostVerdictData = { tips: [{ saddleNo: '1', name: 'NEWSHERALD' }] } as any;
      const result = component['getSpotlightedSelection']();
      expect(result).toEqual(null);
    });
    it('should return null when no outcomes found', () => {
      component.eventEntity = { markets: [{ name: 'Win or Each Way', outcomes: [] }] } as any;
      component.racingPostVerdictData = { tips: [{ saddleNo: '1', name: 'NEWSHERALD' }] } as any;
      const result = component['getSpotlightedSelection']();
      expect(result).toEqual(null);
    });
    it('should return null when outcomes are null', () => {
      component.eventEntity = { markets: [{ name: 'Win or Each Way', outcomes: null }] } as any;
      component.racingPostVerdictData = { tips: [{ saddleNo: '1', name: 'NEWSHERALD' }] } as any;
      const result = component['getSpotlightedSelection']();
      expect(result).toEqual(null);
    });
    it('should return null when no Win or Each Way market found', () => {
      component.eventEntity = { markets: [{ name: 'Win Market', outcomes: null }] } as any;
      component.racingPostVerdictData = { tips: [{ saddleNo: '1', name: 'NEWSHERALD' }] } as any;
      const result = component['getSpotlightedSelection']();
      expect(result).toEqual(null);
    });
    it('should return Win Only when no Win or Each Way market found', () => {
      component.eventEntity = { markets: [{ name: 'Win Only', outcomes: [{ runnerNumber: '1' }] }] } as any;
      component.racingPostVerdictData = { tips: [{ saddleNo: '1', name: 'SPOTLIGHT' }] } as any;
      const result = component['getSpotlightedSelection']();
      expect(result.runnerNumber).toEqual('1');
    });
    it('should return null when tips are null', () => {
      component.eventEntity = { markets: [{ name: 'Win Market', outcomes: null }] } as any;
      component.racingPostVerdictData = { tips: null } as any;
      const result = component['getSpotlightedSelection']();
      expect(result).toEqual(null);
    });
    it('should return null when data is null', () => {
      component.eventEntity = { markets: [{ name: 'Win Market', outcomes: null }] } as any;
      component.racingPostVerdictData = null;
      const result = component['getSpotlightedSelection']();
      expect(result).toEqual(null);
    });
    it('should return null when markets are null', () => {
      component.eventEntity = { markets: null } as any;
      component.racingPostVerdictData = null;
      const result = component['getSpotlightedSelection']();
      expect(result).toEqual(null);
    });
    it('should return null when eventEntity is null', () => {
      component.eventEntity = null as any;
      component.racingPostVerdictData = null;
      const result = component['getSpotlightedSelection']();
      expect(result).toEqual(null);
    });
  });
});

