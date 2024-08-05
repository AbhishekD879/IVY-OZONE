import { of as observableOf, of, Subscription, throwError } from 'rxjs';
import { fakeAsync, flush, tick } from '@angular/core/testing';

import { VirtualSportClassesComponent } from '@app/vsbr/components/virtualSportClasses/virtual-sport-classes.component';
import { ISportEventEntity } from '@core/models/sport-event-entity.model';
import { EDP_MARKETS, eventMock } from '@app/racing/components/racingEventComponent/racing-event.component.mock';
import environment from '@environment/oxygenEnvConfig';

describe('VirtualSportClassesComponent', () => {
  let component: VirtualSportClassesComponent;

  const menuMock = [
    {
      name: 'football',
      inApp: true,
      svgId: 'svgId',
      targetUri: '/football',
      targetUriSegment: '/footballSegment',
      priority: 1,
      childMenuItems: [],
      label: null,
      displayOrder: 1,
      alias: 'hourse-racing',
      svg: 'svg'
    },
    {
      name: 'hourse',
      inApp: true,
      svgId: 'string',
      targetUri: '/hourse',
      targetUriSegment: '',
      priority: 1,
      childMenuItems: [
        {
          name: 'hourse-test',
          inApp: true,
          svgId: 'string',
          targetUri: '/hourse-test',
          targetUriSegment: '',
          priority: 1,
        }
      ],
      label: null,
      displayOrder: 1,
      alias: 'hourse-racing',
      svg: 'svg',
    }
  ];
  const unSortedMarketsMock = [{
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
  const unSortedMarkets = unSortedMarketsMock;
  const categoryAliases = {
    parentAlias: 'parentAlias',
    childAlias: 'childAlias'
  };
  const data = [
    {
      id: 2,
      event: {
        startTimeUnix: '123',
        id: 2,
        children: [{
          market: {
            displayOrder: '1',
            outcomes: [{ name: 'unnamed favourite', isFavourite: true }, { name: '', isFavourite: false }]
          }
        }]
      },
      title: 'any'
    },
    {
      id: 1,
      event: {
        startTimeUnix: '123',
        id: 1,
        children: [{
          market: {
            displayOrder: '2',
            outcomes: [{ name: 'unnamed favourite', isFavourite: true }, { name: '', isFavourite: false }]
          }
        }]
      },
      title: 'any2'
    }
  ] as any;

  const filterService = {
    removeLineSymbol: () => '',
    orderBy: jasmine.createSpy('orderBy')
  } as any;
  const activatedRouteStub = {
    params: observableOf({ alias: 'alias' }),
    snapshot: {
      params: {
        alias: 'alias',
        eventId: 1
      }
    }
  } as any;
  const routerStub = {
    navigate: jasmine.createSpy('navigate')
  } as any;
  const windowRefStub = {
    nativeWindow: {
      setInterval: jasmine.createSpy('setInterval').and.callFake((callback) => {
        callback && callback();
      }),
      clearInterval: jasmine.createSpy('clearInterval')
    }
  } as any;

  const changeDetector = {
    detach: jasmine.createSpy('detach'),
    detectChanges: jasmine.createSpy('detectChanges')
  } as any;

  const panelStateStub = {
    getPanelsStates: jasmine.createSpy('getPanelsStates').and.returnValue('open'),
    changeStatePanel: () => { }
  } as any;

  const datePipeStub = {
    transform: jasmine.createSpy('transform')
  } as any;
  const timeServiceStub = {
    goForNextVsEvent: jasmine.createSpy('jasmine.createSpy(')
  } as any;
  const HORSE_RACING_CATEGORY_ID = environment.HORSE_RACING_CATEGORY_ID;
  const virtualSportsService = {
    subscribeVSBRForUpdates: jasmine.createSpy('subscribeVSBRForUpdates'),
    unSubscribeVSBRForUpdates: jasmine.createSpy('unSubscribeVSBRForUpdates'),
    getAliasesByClassId: jasmine.createSpy().and.returnValue(categoryAliases),
    getActiveClass: jasmine.createSpy().and.returnValue({ class: {} }),
    filterEvents: jasmine.createSpy().and.returnValue(data),
    getEventsWithRacingForms: jasmine.createSpy().and.returnValue(Promise.resolve(data)),
    getMarketSectionsArray: jasmine.createSpy().and.returnValue({ market: { displayOrder: '1' } }),
    genTerms: jasmine.createSpy().and.returnValue('terms'),
    showTerms: jasmine.createSpy().and.returnValue(true),
    getCategoryByAlias: jasmine.createSpy().and.returnValue('16'),
    getAliasByCategory: jasmine.createSpy().and.returnValue('16'),
    unsubscribeFromUpdates: jasmine.createSpy('unsubscribeFromUpdates'),
    normalizeData: jasmine.createSpy('normalizeData').and.returnValue({
      markets: [{
        template: 'WinEw',
        outcomes: [
          { name: 'unnamed favourite', isFavourite: true }, { name: '', isFavourite: false }
        ]
      }],
    } as any)
  } as any;

  const greyhoundService = {
    unSubscribeEDPForUpdates: jasmine.createSpy(),
    subscribeEDPForUpdates: jasmine.createSpy(),
    sortRacingMarketsByTabs: jasmine.createSpy().and.returnValue('123321123'),
    getTypeNamesEvents: jasmine.createSpy().and.returnValue(Promise.resolve({})),
    getConfig: jasmine.createSpy().and.returnValue({ name: 'greyhound' }),
    getGreyhoundEvent: jasmine.createSpy().and.returnValue(Promise.resolve([{ id: '1' }])),
    getGeneralConfig: jasmine.createSpy().and.returnValue({ PRESIM_STOP_TRACK_INTERVAL: '' }),
    sortMarketsName: jasmine.createSpy()
      .and.returnValue({ typeName: '', markets: [{ outcomes: [{ name: '' }] }] as any[] }),
  } as any;

  const deviceServiceStub = {} as any;

  const nativeBridgeStub = {
    onVirtualsSelected: jasmine.createSpy()
  } as any;

  const pubsub = {
    publish: jasmine.createSpy('publish'),
    subscribe: jasmine.createSpy('subscribe').and.callFake((a: string, p: string[] | string, fn: Function) => {
      if (p === 'VS_EVENT_FINISHED') {
        fn({ eventId: 1 });
      } else if (p === 'VIRTUAL_ORIENTATION_CHANGED') {
        fn(1);
      } else {
        fn();
      }
    }),
    unsubscribe: jasmine.createSpy(),
    API: {
      VIRTUAL_ORIENTATION_CHANGES: 'VIRTUAL_ORIENTATION_CHANGED',
      VS_EVENT_FINISHED: 'VS_EVENT_FINISHED',
      RELOAD_COMPONENTS: 'RELOAD_COMPONENTS',
      AUTOSEO_DATA_UPDATED: 'AUTOSEO_DATA_UPDATED',
      SORT_BY_OPTION: 'SORT_BY_OPTION',
      LIVE_MARKET_FOR_EDP: 'LIVE_MARKET_FOR_EDP'
    },
  } as any;

  const virtualMenuDataService = {
    setMenu: jasmine.createSpy('getChildMenuItems').and.returnValue(menuMock),
    getChildMenuItems: jasmine.createSpy('getChildMenuItems').and.returnValue(menuMock)
  } as any;

  const vsMapperService = {
    getParentByAlias: jasmine.createSpy('getParentByAlias').and.returnValue({ ctaButtonText: 'ctaButtonText', ctaButtonUrl: '/ctaBUrl' })
  } as any;

  let elementRef;
  const sortByOptionsService = {
    get: jasmine.createSpy('get').and.returnValue('Price'),
    set: jasmine.createSpy('set'),
  } as any;

  const localeService = {
    getString: jasmine.createSpy('getString').and.returnValue('test_string')
  } as any;

  const cmsObservableResult = {
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
  const cmsService = {
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
  } as any;

  const racingPostService = {
    updateRacingEventsList: jasmine.createSpy('updateRacingEventsList').and.returnValue(of({}))
  } as any;

  const racingGaService = {
    trackEvent: jasmine.createSpy('trckEvent'),
    updateGATracking: jasmine.createSpy('updateGATracking'),
    toggleShowOptionsGATracking: jasmine.createSpy('toggleShowOptionsGATracking')
  } as any;

  const gtmService = {
    push: jasmine.createSpy('push')
  } as any;

  const horseracing = {
    getEvent: jasmine.createSpy('getEvent').and.returnValue(Promise.resolve(['poolEventEntity'])),
    isRacingSpecials: jasmine.createSpy('isRacingSpecials'),
    getConfig: jasmine.createSpy().and.returnValue({ name: 'horseracing' }),
    getSortingFromCms: jasmine.createSpy('getSortingFromCms').and.returnValue({}),
    isToteForecastTricasMarket: jasmine.createSpy('isToteForecastTricasMarket').and.returnValue(true)
  } as any;

  const watchRulesService = {
    shouldShowCSBIframe: jasmine.createSpy('shouldShowCSBIframe'),
    isInactiveUser: jasmine.createSpy('isInactiveUser')
  } as any;

  const performGroupService = {
    isEventStarted: jasmine.createSpy('isEventStarted').and.returnValue(false),
    performGroupId: jasmine.createSpy('performGroupId').and.returnValue(observableOf(true)),
    getVideoUrl: jasmine.createSpy('getVideoUrl').and.callFake(v => observableOf(v)),
    getElementWidth: jasmine.createSpy('isEventStarted')
  } as any;

  const routingState = {
    getCurrentSegment: jasmine.createSpy().and.returnValue('horseracing')
  } as any;
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
  const sbFilters = {
    orderOutcomeEntities: jasmine.createSpy('orderOutcomeEntities').and.returnValue([{
      id: 'outcome1'
    },
    {
      id: 'outcome2'
    }]),
    orderOutcomesByName: jasmine.createSpy('orderOutcomeEntities').and.returnValue(sortedByName)
  } as any;

  beforeEach(() => {
    component = new VirtualSportClassesComponent(windowRefStub, filterService,
      timeServiceStub, datePipeStub, panelStateStub, virtualSportsService, activatedRouteStub,
      routerStub, deviceServiceStub, nativeBridgeStub, pubsub, changeDetector, virtualMenuDataService, vsMapperService,
      greyhoundService, routingState, watchRulesService, horseracing, sbFilters, racingPostService, cmsService, localeService, sortByOptionsService,
      gtmService, racingGaService, performGroupService, elementRef);

    component['eventId'] = '1';
    component.activeClass = { class: {} } as any;
    component.events = data;
    component['paramsSubscriber'] = new Subscription();
    component['currentEventIndex'] = 1;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('@ngOnInit', () => {
    it('should init component, reload if connection is lost, close dialogs', () => {
      component.ngOnInit();
      component.eventsData = [{ event: {} }] as any;
      expect(component.eventsData).toBeTruthy();
    });

    it('should init component data', fakeAsync(() => {
      component['updateFinishedStatus'] = jasmine.createSpy('updateFinishedStatus');
      deviceServiceStub.isWrapper = true;
      component.addChangeDetection = jasmine.createSpy('component');
      const localEvent = {
        markets: [{
          template: 'WinEw',
          ncastTypeCodes: 'CF, CT',
          outcomes: [{}, {}, {}]
        }, {
          template: 'Vertical',
          marketName: 'place',
          outcomes: [{}, {}, {}]
        }, {
          template: 'Vertical',
          marketName: 'show',
          outcomes: [{}, {}, {}]
        }]
      } as any;
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(localEvent);

      component.ngOnInit();
      tick();

      expect(component.addChangeDetection).toHaveBeenCalled();
      expect(component.categoryAlias).toEqual('alias');

      component['prepareEventsForTabs']();
      expect(datePipeStub.transform).toHaveBeenCalledWith('123', 'HH:mm');
      expect(component['currentEventIndex']).toBe(0);

      expect(component['panelsStates']).toEqual('open');
      expect(pubsub.subscribe)
        .toHaveBeenCalledWith('VirtualSportClassesCtrl', 'VS_EVENT_FINISHED', jasmine.any(Function));
      expect(component['requestedEventNotFound']).toBe(false);
      expect(component['updateFinishedStatus']).toHaveBeenCalledWith(1 as any);
      flush();
    }));

    it('should handle error on subscription', fakeAsync(() => {
      virtualSportsService.getEventsWithRacingForms = jasmine.createSpy().and.returnValue(Promise.reject());
      component.ngOnInit();
      tick();
      expect(component['state'].error).toBe(true);
    }));

    it('should init component and route.params should throw error', fakeAsync(() => {
      component.showError = jasmine.createSpy('showError');
      activatedRouteStub.params = throwError('error');
      component.ngOnInit();
      tick(200);
      expect(component.showError).toHaveBeenCalled();
    }));

    it('should set param as virtual-horse-racing', fakeAsync(() => {
      activatedRouteStub.params = observableOf({ eventId: 1 });
      deviceServiceStub.isWrapper = false;
      component.ngOnInit();
      tick();
      expect(virtualSportsService.getEventsWithRacingForms).toHaveBeenCalled();
    }));

    it('should set currentEventIndex > 0', fakeAsync(() => {
      data[0].event.id = 0;
      data[1].event.id = 1;
      activatedRouteStub.snapshot.params.eventId = '1';
      virtualSportsService.getEventsWithRacingForms = jasmine.createSpy().and.returnValue(Promise.resolve(data));
      component.ngOnInit();
      tick();
      expect(component['currentEventIndex']).toBe(0);
      expect(component['requestedEventNotFound']).toBeFalsy();

      component.getEventStartTime(123);
      expect(datePipeStub.transform).toHaveBeenCalled();
    }));

    it('should call ngOnInit() and check currentEventIndex', fakeAsync(() => {
      activatedRouteStub.snapshot.params.eventId = '23';
      component.eventsData = [{ event: { id: '2' } }] as any;
      component.ngOnInit();
      tick();
      expect(component['currentEventIndex']).toBeFalsy();
    }));

    it('should set currentEventIndex === 0', fakeAsync(() => {
      activatedRouteStub.snapshot.params.eventId = undefined;
      deviceServiceStub.isWrapper = true;
      component.eventsData = data;
      component.ngOnInit();
      tick();
      expect(component['currentEventIndex']).toBeFalsy();
    }));

    it('should not navigate if category aliases are equal', fakeAsync(() => {
      pubsub.subscribe.and.callFake((a, p, fn) => {
        if (p === 'VS_EVENT_FINISHED') {
          fn({ eventId: undefined, alias: 16 });
        } else {
          fn();
        }
      });
      component['categoryAlias'] = '16';
      deviceServiceStub.isWrapper = true;
      component.ngOnInit();
      tick();
      expect(nativeBridgeStub.onVirtualsSelected).toHaveBeenCalledWith('16', 1);
    }));

    it('should not navigate to virtual sports if orientation changed', fakeAsync(() => {
      deviceServiceStub.isWrapper = true;
      activatedRouteStub.snapshot.params['alias'] = null;
      virtualSportsService.getAliasesByClassId = jasmine.createSpy().and.returnValue(null);
      component.ngOnInit();
      tick();
      expect(pubsub.subscribe).toHaveBeenCalled();
    }));

    it('should init events subscription for liveserve updates', fakeAsync(() => {
      component.ngOnInit();
      tick();

      expect(virtualSportsService.unSubscribeVSBRForUpdates).toHaveBeenCalled();
      expect(virtualSportsService.subscribeVSBRForUpdates).toHaveBeenCalledWith(data);
    }));
    it('should call virtualAutoseoData', fakeAsync(() => {
      spyOn(component as any, 'virtualAutoseoData').and.callThrough();
      component.ngOnInit();
      tick();
      expect(component['virtualAutoseoData']).toHaveBeenCalled();
    }));

    it('should enter isLegendsSport', fakeAsync(() => {
      component['updateFinishedStatus'] = jasmine.createSpy('updateFinishedStatus');
      deviceServiceStub.isWrapper = true;
      component.addChangeDetection = jasmine.createSpy('component');
      component['syncToApplySorting'] = jasmine.createSpy('syncToApplySorting');
      const localEvent = {
        categoryCode: 'HORSE_RACING',
        markets: [{
          template: 'WinEw',
          ncastTypeCodes: 'CF, CT',
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
        }, {
          template: 'Vertical',
          marketName: 'place',
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
        }, {
          template: 'Vertical',
          marketName: 'show',
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
        }]
      } as any;
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
      component.event = { markets: unSortedMarkets } as any;
      component['update'] = jasmine.createSpy('update');
      component['deleteEvents'] = jasmine.createSpy('deleteEvents');
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(localEvent);
      virtualSportsService.getActiveClass = jasmine.createSpy('getActiveClass').and.returnValue({ class: {}, classId: '223' });
      component.ngOnInit();
      tick();

      expect(component.addChangeDetection).toHaveBeenCalled();
      component['prepareEventsForTabs']();
      expect(datePipeStub.transform).toHaveBeenCalledWith('123', 'HH:mm');
      expect(component['currentEventIndex']).toBe(0);

      expect(pubsub.subscribe)
        .toHaveBeenCalledWith('VirtualSportClassesCtrl', 'VS_EVENT_FINISHED', jasmine.any(Function));
      expect(component['requestedEventNotFound']).toBe(false);
      flush();

      // isAntepostMarket false
      const localEventAnte = {
        categoryCode: 'HORSE_RACING',
        markets: [{
          template: 'WinEw',
          ncastTypeCodes: 'CF, CT',
          isAntepost: 'true',
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
        }, {
          template: 'Vertical',
          marketName: 'place',
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
        }, {
          template: 'Vertical',
          marketName: 'show',
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
        }]
      } as any;
      // isAntepost is true
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(localEventAnte);
      component.event = { markets: [...unSortedMarkets] } as any;
      component.event.markets[0].isAntepost = 'true';
      component.ngOnInit();
      tick();

      // isHR is false
      const localEventNonHR = { ...localEventAnte, categoryCode: 'GREYHOUND' };
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(localEventNonHR);
      component.event = { markets: [...unSortedMarkets] } as any;
      component.event.markets[0].isAntepost = 'true';
      component.ngOnInit();
      tick();

      // SortOptions.enabled false
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(localEventNonHR);
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of({
        ...cmsObservableResult, SortOptions: {
          enabled: false
        }
      }));
      component.event = { markets: [...unSortedMarkets] } as any;
      component.event.markets[0].isAntepost = 'true';
      component.ngOnInit();
      tick();

      // SortOptions null
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(localEventNonHR);
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of({ ...cmsObservableResult, SortOptions: null }));
      component.event = { markets: [...unSortedMarkets] } as any;
      component.event.markets[0].isAntepost = 'true';
      component.ngOnInit();
      tick();

      // getFeatureConfig all true
      const config = {
        showFullScreen: true,
        fullScreenDrillDownTags: ['EVFLAG_PVM', 'EVFLAG_PVA'],
        insightsDrillDownTags: ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'],
      };
      cmsService.getFeatureConfig.and.returnValue(observableOf(config));
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(localEventNonHR);
      component.event = { markets: [...unSortedMarkets] } as any;
      component.event.markets[0].isAntepost = 'true';
      component.ngOnInit();
      tick();

      // getFeatureConfig fullScreenDrillDownTags null
      cmsService.getFeatureConfig.and.returnValue(observableOf({ ...config, fullScreenDrillDownTags: null }));
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(localEventNonHR);
      component.event = { markets: [...unSortedMarkets] } as any;
      component.event.markets[0].isAntepost = 'true';
      component.ngOnInit();
      tick();

      // getFeatureConfig showFullScreen null
      cmsService.getFeatureConfig.and.returnValue(observableOf({ ...config, showFullScreen: null }));
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(localEventNonHR);
      component.event = { markets: [...unSortedMarkets] } as any;
      component.event.markets[0].isAntepost = 'true';
      component.ngOnInit();
      tick();

      // getFeatureConfig data null
      cmsService.getFeatureConfig.and.returnValue(observableOf(null));
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(localEventNonHR);
      component.event = { markets: [...unSortedMarkets] } as any;
      component.event.markets[0].isAntepost = 'true';
      component.ngOnInit();
      tick();

      // getFeatureConfig all true
      cmsService.getFeatureConfig.and.returnValue(observableOf({ ...config, showFullScreen: null }));
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(localEventNonHR);
      component.event = { markets: [...unSortedMarkets] } as any;
      component.event.markets[0].isAntepost = 'true';
      component.ngOnInit();
      tick();

      // getFeatureConfig all true
      cmsService.getFeatureConfig.and.returnValue(observableOf({ ...config, insightsDrillDownTags: false }));
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(localEventNonHR);
      component.event = { markets: [...unSortedMarkets] } as any;
      component.event.markets[0].isAntepost = 'true';
      component.ngOnInit();
      tick();
    }));
  });

  it('isAntepostMarket', () => {
    component.event = { markets: [...unSortedMarkets] } as any;
    component.event.markets[0].isAntepost = 'true';
    expect(component['isAntepostMarket']()).toBeTruthy();

    component.event.markets[0] = null;
    expect(component['isAntepostMarket']()).toBeFalsy();

    component.event.markets = null;
    expect(component['isAntepostMarket']()).toBeFalsy();

    component.event = null;
    expect(component['isAntepostMarket']()).toBeFalsy();
  });



  describe('@ngOnDestroy', () => {
    it('should destroy component, unsync, unsubscribe', () => {
      component['pollingTimer'] = 1;
      component['timeOutListener'] = 2;
      component['paramsSubscriber'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.ngOnDestroy();
      expect(windowRefStub.nativeWindow.clearInterval).toHaveBeenCalledWith(2);
      expect(windowRefStub.nativeWindow.clearInterval).toHaveBeenCalledWith(1);
      expect(pubsub.unsubscribe).toHaveBeenCalledWith(jasmine.any(String));
      expect(component['paramsSubscriber'].unsubscribe).toHaveBeenCalled();
      expect(virtualSportsService.unSubscribeVSBRForUpdates).toHaveBeenCalled();
    });
  });

  describe('@onTabClick', () => {
    it('should check event tab click callback ', () => {
      deviceServiceStub.isWrapper = true;
      const mockTab = {
        tab: {
          event: {
            id: '111'
          }
        }
      };

      component.categoryId = '290';
      spyOn<any>(component, 'update').and.returnValue(true);

      component.onTabClick(mockTab as any);
      expect(component['nativeBridge'].onVirtualsSelected).toHaveBeenCalledWith('290', '111');
    });

    it('hould check event tab click and currentEventIndex', fakeAsync(() => {
      activatedRouteStub.snapshot.params.eventId = '111';
      component.events = [{ event: { id: '111' } }] as any;
      const mockTab = {
        tab: {
          event: {
            id: '111'
          }
        }
      };
      component.onTabClick(mockTab as any);
      tick();
      expect(component['currentEventIndex']).toBeFalsy();
    }));


    it('should check event tab click callback when deviceServiceStub.isWrapper = false', () => {
      deviceServiceStub.isWrapper = false;
      const mockTabs = {
        tab: {
          event: {
            id: '112'
          }
        }
      };

      component.categoryId = '291';
      spyOn<any>(component, 'update').and.returnValue(true);

      component.onTabClick(mockTabs as any);
      expect(component['nativeBridge'].onVirtualsSelected).not.toHaveBeenCalledWith('291', '112');
    });

  });

  describe('@updateCurrentEvent', () => {
    it('should set currentEvent if events are exist', () => {
      component['setSwitchers'] = jasmine.createSpy('setSwitchers');
      component.currentEventIndex = 0;
      component.events = [{ id: '1' }, { id: '2' }] as any;
      component['updateCurrentEvent']();
      expect(component.currentEvent).toEqual({ id: '1' } as any);
      expect(virtualSportsService.getMarketSectionsArray).toHaveBeenCalledWith({ id: '1' });
      expect(filterService.orderBy).toHaveBeenCalled();
      expect(component['setSwitchers']).toHaveBeenCalled();
    });

    it('should NOT set currentEvent if events are not exist', () => {
      component['setSwitchers'] = jasmine.createSpy('setSwitchers');
      component.currentEventIndex = 1;
      component.events = [] as any;
      component['updateCurrentEvent']();
      expect(component.currentEvent).toEqual(undefined);
      expect(component['setSwitchers']).not.toHaveBeenCalled();
    });

    it('should call syncToApplySorting when isLegendsSport is true', () => {
      component.isLegendsSport = true;
      component['setSwitchers'] = jasmine.createSpy('setSwitchers');
      component['syncToApplySorting'] = jasmine.createSpy('syncToApplySorting');
      component.currentEventIndex = 0;
      component.events = [{ id: '1' }, { id: '2' }] as any;
      component.sportName = 'horse-racing';
      component.event = { isUKorIRE: true } as any;
      component['updateCurrentEvent']();
      expect(component.currentEvent).toEqual({ id: '1' } as any);
      expect(virtualSportsService.getMarketSectionsArray).toHaveBeenCalledWith({ id: '1' });
      expect(filterService.orderBy).toHaveBeenCalled();
      expect(component['syncToApplySorting']).toHaveBeenCalled();
      component.sportName = 'horse-racing';
      component.event = { isUKorIRE: true } as any;
      component.showQuantumLeap = false;
      component['updateCurrentEvent']();
      expect(component.showQuantumLeap).toBeTruthy();
      component.showQuantumLeap = false;
      component.sportName = 'greyhound';
      component.event = { isUKorIRE: false } as any;
      component['updateCurrentEvent']();
      expect(component.showQuantumLeap).toBeFalsy();
      component.showQuantumLeap = false;
      component.sportName = 'greyhound';
      component.event = null;
      component['updateCurrentEvent']();
      expect(component.showQuantumLeap).toBeFalsy();
    });
  });

  describe('@switchers', () => {
    it('should check switchers', () => {
      component.currentEvent = <any>{ event: { className: 'footballClass' } };
      const event = {
        markets: [{
          template: 'WinEw',
          ncastTypeCodes: 'CF, CT',
          outcomes: [{}, {}, {}]
        }]
      } as any;
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(event);
      component['setSwitchers']();

      component.switchers[0].onClick();
      expect(component.filter).toEqual('winew');

      component.switchers[1].onClick();
      expect(component.filter).toEqual('forecast');

      component.switchers[2].onClick();
      expect(component.filter).toEqual('tricast');
    });
  });

  describe('@setSwitchers', () => {
    it('should set all WinOrEW Markets if they are exist and have outcomes', () => {
      component.currentEvent = <any>{ event: { className: 'footballClass' } };
      const event = {
        markets: [{
          template: 'WinEw',
          ncastTypeCodes: 'CF, CT',
          outcomes: [{}, {}, {}]
        }]
      } as any;
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(event);
      component['setSwitchers']();

      expect(component.terms).toEqual('terms');
      expect(component.filter).toEqual('winew');
      expect(component.switchers).toEqual([{
        onClick: jasmine.any(Function),
        viewByFilters: 'winew',
        name: 'Win/Each Way'
      }, {
        onClick: jasmine.any(Function),
        viewByFilters: 'forecast',
        name: 'Forecast'
      }, {
        onClick: jasmine.any(Function),
        viewByFilters: 'tricast',
        name: 'Tricast'
      }]);
    });

    it('should set WinOrEW Markets even if ncastTypeCodes undefined', () => {
      component.currentEvent = <any>{ event: { className: 'footballClass' } };
      const event = {
        markets: [{
          template: 'WinEw',
          outcomes: []
        }]
      } as any;
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(event);
      component['setSwitchers']();

      expect(component.filter).toEqual('winew');
      expect(component.hasWinOrEachWay).toEqual(true);
      expect(component.switchers.length).toEqual(1);
    });

    it('should set WinOrEW Market and ForecastMarket if all outcomes are available', () => {
      component.currentEvent = <any>{ event: { className: 'footballClass' } };
      const event = {
        markets: [{
          template: 'WinEw',
          ncastTypeCodes: 'CF',
          outcomes: [{}, {}, {}]
        }]
      } as any;
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(event);
      component['setSwitchers']();

      expect(component.filter).toEqual('winew');
      expect(component.switchers).toEqual([{
        onClick: jasmine.any(Function),
        viewByFilters: 'winew',
        name: 'Win/Each Way'
      }, {
        onClick: jasmine.any(Function),
        viewByFilters: 'forecast',
        name: 'Forecast'
      }]);
    });

    it('should set only WinOrEW Market if Forecast Market is exist but outcomes are NOT available', () => {
      component.currentEvent = <any>{ event: { className: 'footballClass' } };
      const event = {
        markets: [{
          template: 'WinEw',
          ncastTypeCodes: 'CF',
          outcomes: []
        }]
      } as any;
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(event);
      component['setSwitchers']();

      expect(component.filter).toEqual('winew');
      expect(component.switchers).toEqual([{
        onClick: jasmine.any(Function),
        viewByFilters: 'winew',
        name: 'Win/Each Way'
      }]);
    });

    it('should set WinOrEW Market and TriCast Market if all outcomes are available', () => {
      component.currentEvent = <any>{ event: { className: 'footballClass' } };
      const event = {
        markets: [{
          template: 'WinEw',
          ncastTypeCodes: 'CT',
          outcomes: [{}, {}, {}]
        }]
      } as any;
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(event);
      component['setSwitchers']();

      expect(component.filter).toEqual('winew');
      expect(component.switchers).toEqual([{
        onClick: jasmine.any(Function),
        viewByFilters: 'winew',
        name: 'Win/Each Way'
      }, {
        onClick: jasmine.any(Function),
        viewByFilters: 'tricast',
        name: 'Tricast'
      }]);
    });

    it('should set only WinOrEW Market if TriCast Market is exist but outcomes are NOT available', () => {
      component.currentEvent = <any>{ event: { className: 'footballClass' } };
      const event = {
        markets: [{
          template: 'WinEw',
          ncastTypeCodes: 'CT',
          outcomes: []
        }]
      } as any;
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(event);
      component['setSwitchers']();

      expect(component.filter).toEqual('winew');
      expect(component.switchers).toEqual([{
        onClick: jasmine.any(Function),
        viewByFilters: 'winew',
        name: 'Win/Each Way'
      }]);
    });

    it('should clear terms value if there is no terms', () => {
      const event = {
        markets: [{
          marketName: 'marketName',
          template: 'Vertical',
          ncastTypeCodes: undefined,
          outcomes: []
        }]
      } as any;
      virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(event);
      component['setSwitchers']();

      expect(component.terms).toEqual('');
    });
  });

  describe('@update', () => {
    it('should call updateCurrentEvent', () => {
      component['updateCurrentEvent'] = jasmine.createSpy('updateCurrentEvent');

      component['update']();

      expect(component['updateCurrentEvent']).toHaveBeenCalled();
    });
  });

  it('@updateFinishedStatus should update isFinished status', () => {
    component['updateFinishedStatus']('1');
    expect(component.events[1].event.isFinished).toEqual('true');
  });

  it('@addChangeDetection should run change detection', () => {
    component.addChangeDetection();

    expect(changeDetector.detach).toHaveBeenCalled();
    expect(windowRefStub.nativeWindow.setInterval).toHaveBeenCalledWith(jasmine.any(Function), 500);
    expect(changeDetector.detectChanges).toHaveBeenCalled();
  });

  describe('@goToVirtual', () => {
    it('should call goToVirtual()', fakeAsync(() => {
      component.goToCtaUrl();
      expect(routerStub.navigate).toHaveBeenCalled();
    }));

    it('should call goToVirtual() if ctaUrl = undefined', fakeAsync(() => {
      component.ctaUrl = '/football';
      component.goToCtaUrl();
      expect(routerStub.navigate).toHaveBeenCalled();
    }));
  });

  describe('goToNextIfStarted', () => {
    it('should return true', () => {
      component.events = [{
        event: { startTimeUnix: Date.now() / 2 }
      }] as any;

      expect(component['goToNextIfStarted'](0)).toBeTruthy();
      expect(component.events[0].event.isStarted).toBeDefined();
    });

    it('should return false', () => {
      component.events = [{
        event: { startTimeUnix: Date.now() * 2 }
      }] as any;

      expect(component['goToNextIfStarted'](0)).toBeFalsy();
      expect(component.events[0].event.isStarted).toBeDefined();
    });

    it('should return false if event is invalid', () => {
      component.events = [] as any;
      expect(component['goToNextIfStarted'](0)).toBeFalsy();
    });
  });

  describe('hasEventFinished', () => {
    it('should return true', () => {
      component.events = [{
        event: { isFinished: 'true' }
      }] as any;
      expect(component['hasEventFinished'](0)).toBeTruthy();
    });

    it('should return false', () => {
      component.events = [] as any;
      expect(component['hasEventFinished'](0)).toBeFalsy();
    });
  });

  describe('activeStatePanel', () => {
    beforeEach(() => {
      component.currentEventIndex = 0;
    });

    it('panel exists', () => {
      component.panelsStates = [{ '1': {} }];
      expect(component.activeStatePanel('1')).toBeTruthy();
    });

    it('panel doesn\'t exist', () => {
      component.panelsStates = [];
      expect(component.activeStatePanel('1')).toBeFalsy();
    });

    it('should call activeStatePanel', () => {
      const panelId = undefined;

      component.activeStatePanel(panelId);
      expect(component['panelsStates']).toBeDefined();
    });
  });

  it('getEventStartTime', () => {
    component.currentEvent = {
      event: { startTimeUnix: 123 }
    } as any;
    component.getEventStartTime(123);
    expect(datePipeStub.transform).toHaveBeenCalledWith(
      component.currentEvent.event.startTimeUnix, 'HH:mm');
  });

  it('getEventStartDate', () => {
    component.currentEvent = {
      event: { startTimeUnix: 123 }
    } as any;
    component.getEventStartDate(123);
    expect(datePipeStub.transform).toHaveBeenCalledWith(
      component.currentEvent.event.startTimeUnix, 'yyyy-MM-dd');
  });

  it('should call trackMarketSectionById method', () => {
    const result = component.trackMarketSectionById(1, { id: 'test' });
    expect(result).toEqual('1test');
  });

  it('should call changeStatePanel', () => {
    const panelId = 'panelId';

    component.changeStatePanel(panelId);
    expect(component['panelsStates']).toBeDefined();
    expect(component['panelsStates']).toBeTruthy();
  });

  describe('deleteEvents', () => {
    it('should call deleteEvents()', () => {
      component['eventId'] = '22';
      component.eventsData = [{ event: { id: '2' } }] as any;
      component.currentEvent = { id: 13 } as ISportEventEntity;
      component['deleteEvents'](['1']);

      expect(component['currentEventIndex']).toBe(0);
    });

    it('should do nothing if no events', () => {
      component['update'] = jasmine.createSpy('update');
      component.events = [] as any;
      component['deleteEvents'](['1']);

      expect(component['update']).not.toHaveBeenCalled();
    });

    it('should reload virtuals if last event is deleted', () => {
      component['update'] = jasmine.createSpy('update');
      component.events = [{ event: { id: 1 } }] as any;
      component['deleteEvents'](['1']);

      expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.RELOAD_COMPONENTS);
      expect(component['update']).not.toHaveBeenCalled();
    });
  });

  it('should not call deleteEvents()', () => {
    component['deleteEvents'] = jasmine.createSpy('deleteEvents');

    component.events = [{
      id: 1,
      event: { startTimeUnix: Date.now() * 2, id: 1 }
    },
    {
      id: 2,
      event: { startTimeUnix: Date.now() * 2, id: 2 }
    }, {
      id: 3,
      event: { startTimeUnix: Date.now() * 2, id: 3 }
    }] as any;
    component['removeOutdatedEvents']();
    expect(component['deleteEvents']).not.toHaveBeenCalled();
  });

  it('getMarketSwitcherConfig should return switcher config for specific filter name', () => {
    const result = component['getMarketSwitcherConfig']('winew');
    expect(result).toEqual({
      onClick: jasmine.any(Function),
      viewByFilters: 'winew',
      name: 'Win/Each Way'
    });
  });

  it('getMarketSwitcherConfig should return undefined if filterName is invalid', () => {
    const result = component['getMarketSwitcherConfig']('test');

    expect(result).toBeUndefined();
  });

  it('setSwitchers should add switchers if there are few valid markets and one of them is winEw', () => {
    component.currentEvent = <any>{ event: { className: 'footballClass' } };
    component['getMarketSwitcherConfig'] = jasmine.createSpy('getMarketSwitcherConfig');
    const localEvent = {
      markets: [{
        template: 'WinEw',
        ncastTypeCodes: 'CF, CT',
        outcomes: [{}, {}, {}]
      }, {
        template: 'Vertical',
        marketName: 'place',
        outcomes: [{}, {}, {}]
      }, {
        template: 'Vertical',
        marketName: 'show',
        outcomes: [{}, {}, {}]
      }]
    } as any;
    const winMarket = localEvent.markets[0];

    virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(localEvent);

    component['setSwitchers']();

    expect(component.event).toEqual(localEvent);
    expect(virtualSportsService.normalizeData).toHaveBeenCalled();

    expect(virtualSportsService.genTerms).toHaveBeenCalled();
    expect(virtualSportsService.showTerms).toHaveBeenCalled();

    expect(virtualSportsService.genTerms).toHaveBeenCalledWith(winMarket);
    expect(virtualSportsService.showTerms).toHaveBeenCalledWith(winMarket);

    expect(component.filter).toEqual('winew');
    expect(component.market).toEqual(winMarket);
    expect(component.hasWinOrEachWay).toBeTruthy();
    expect(component['getMarketSwitcherConfig']).toHaveBeenCalledTimes(5);

    expect(component.switchers.length).toEqual(5);
  });

  it('setSwitchers should add switcher if event contain only one market and it follow expectations', () => {
    component['getMarketSwitcherConfig'] = jasmine.createSpy('getMarketSwitcherConfig');
    const localEvent = {
      markets: [{
        template: 'Vertical',
        marketName: 'place',
        outcomes: [{}, {}, {}]
      }]
    } as any;
    virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(localEvent);

    component['setSwitchers']();

    expect(component.event).toEqual(localEvent);
    expect(virtualSportsService.normalizeData).toHaveBeenCalled();

    expect(component.hasWinOrEachWay).toBeFalsy();
    expect(component['getMarketSwitcherConfig']).toHaveBeenCalledTimes(1);

    expect(component.switchers.length).toEqual(1);
  });

  it('setSwitchers should add winEw market even if it does not contain ncastTypeCodes', () => {
    component.currentEvent = <any>{ event: { className: 'footballClass' } };
    component['getMarketSwitcherConfig'] = jasmine.createSpy('getMarketSwitcherConfig');
    const localEvent = {
      markets: [{
        template: 'WinEw',
        ncastTypeCodes: undefined,
        outcomes: [{}, {}, {}]
      }]
    } as any;
    virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(localEvent);

    component['setSwitchers']();

    expect(component.event).toEqual(localEvent);
    expect(virtualSportsService.normalizeData).toHaveBeenCalled();
    expect(component.hasWinOrEachWay).toEqual(true);
    expect(component['getMarketSwitcherConfig']).toHaveBeenCalledTimes(1);
    expect(component.switchers.length).toEqual(1);
  });

  it('setSwitchers shouldn\'t add switchers if there are no markets in event', () => {
    const localEvent = {
      markets: []
    } as any;
    virtualSportsService.normalizeData = jasmine.createSpy('normalizeData').and.returnValue(localEvent);

    component['setSwitchers']();

    expect(component.event).toEqual(localEvent);
    expect(virtualSportsService.normalizeData).toHaveBeenCalled();
    expect(component.hasWinOrEachWay).toBeFalsy();
    expect(component.switchers.length).toEqual(0);
  });
  describe('virtualAutoseoData', () => {
    it('should assign autoSeoData object and publish the data', () => {
      component.parentCategoryAlias = 'football';
      component.categoryAlias = 'UK-FOOTBALL';
      component['virtualAutoseoData']();
      expect(component['autoSeoData']).toBeDefined();
      expect(component['autoSeoData']['isOutright']).toBeFalse();
      expect(component['autoSeoData']['categoryName']).toEqual(component.parentCategoryAlias);
      expect(component['autoSeoData']['typeName']).toEqual(component.categoryAlias);
      expect(pubsub.publish).toHaveBeenCalledWith('AUTOSEO_DATA_UPDATED', jasmine.any(Object));
    });
  });

  it('should apply sorting by price with markets as null', () => {
    component.expandedSummary = [];
    component.sortBy = 'Price';
    component.event = {
      markets: [{
        template: 'WinEw',
        outcomes: [
          { name: 'unnamed favourite', isFavourite: true, prices: [] }, { name: '', isFavourite: false, prices: [] }
        ]
      }]
    } as any;
    component['applySortBy'] = jasmine.createSpy('applySortBy');
    component['applySortByName'] = jasmine.createSpy('applySortByName');
    component['syncToApplySorting']();
    expect(component['applySortBy']).toHaveBeenCalled();
    expect(component['applySortByName']).not.toHaveBeenCalled();
  });

  it('should apply sorting by price', () => {
    component.expandedSummary = [];
    component.sortBy = 'Price';
    component.event = {
      markets: [{
        template: 'WinEw',
        outcomes: [
          { name: 'unnamed favourite', isFavourite: true, prices: [] }, { name: '', isFavourite: false, prices: [] }
        ]
      }]
    } as any;
    component['applySortBy'] = jasmine.createSpy('applySortBy');
    component['syncToApplySorting']();
    expect(component['applySortBy']).toHaveBeenCalledWith('Price');
  });

  describe('#setMarketsInfo', () => {
    it('setMarketsInfo', () => {
      component.expandedSummary = [];
      component['setMarketsInfo']({
        outcomes: [
          { name: 'unnamed favourite', isFavourite: true }, { name: '', isFavourite: false }
        ]
      } as any, 0);
      expect(component.expandedSummary[0].length).toEqual(1);
    });
  });

  it('onPlayLiveStreamError', () => {
    const error = { value: 'error' };
    // createComponent();
    component.isWrapper = false;
    component.streamFilter = 'test_string';

    component.onPlayLiveStreamError(error);
    expect(component.streamFilter).toBe('test_string');

    // createComponent();
    watchRulesService.isInactiveUser.and.returnValue(false);
    component.isWrapper = true;

    component.onPlayLiveStreamError(error);
    expect(component.streamFilter).toBe('hideStream');
  });

  it('onPlayLiveStreamError: should not hide stream if user get inactive qualification error', () => {
    const error = { value: 'inactiveError' };
    // createComponent();
    component.filter = 'test_string';
    watchRulesService.isInactiveUser.and.returnValue(true);
    component.isWrapper = true;

    component.onPlayLiveStreamError(error);
    expect(component.filter).toBe('test_string');
  });

  describe('#toteForecastTricastMarket', () => {
    it('onExpandSection checker false', () => {
      const expandedSummary = [[false], [false]];
      component.event = Object.assign({}, eventMock);
      component.onExpandSection(expandedSummary, 1, 0);

      expect(expandedSummary).toEqual([[false], [true]]);
      expect(component.isInfoHidden.info).toEqual(true);
    });

    it('onExpandSection ', () => {
      const expandedSummary = [[true], [true]];
      component.event = Object.assign({}, eventMock);
      component.onExpandSection(expandedSummary, 1, 0);

      expect(expandedSummary).toEqual([[true], [false]]);
      expect(component.isInfoHidden.info).toEqual(false);
    });
    it('toggleShowOptions', () => {
      const expandedSummary = [[false, true], [true, false]];
      component.event = Object.assign({}, eventMock);
      component.toggleShowOptions(expandedSummary, 1, true);

      expect(expandedSummary).toEqual([[false, true], [true, true]]);
    });

    it('#Should call onExpandSection GA Tracking when isGreyhoundEdp is false', () => {
      const expandedSummary = [[true], [true]];
      component.event = Object.assign({}, eventMock);
      component.isGreyhoundEdp = false;
      component.onExpandSection(expandedSummary, 1, 0);

      const expectedParams = ['trackEvent', {
        event: 'trackEvent',
        eventAction: 'race card',
        eventCategory: 'horse racing',
        eventLabel: 'show less',
        categoryID: '21',
        typeID: '1909',
        eventID: 11818323
      }];
      expect(component.isGreyhoundEdp).toBeFalsy();

      expect(gtmService.push).toHaveBeenCalledWith(...expectedParams);
    });

    it('#Should call onExpandSection GA Tracking when isGreyhoundEdp is true', () => {
      const expandedSummary = [[false], [false]];
      component.event = Object.assign({}, eventMock);
      component.isGreyhoundEdp = true;
      component.onExpandSection(expandedSummary, 1, 0);
      expect(component.isGreyhoundEdp).toBeTruthy();
    });
  });

  it('toggleShowOptions', () => {
    const expandedSummary = [[false, true], [true, false]];
    component.toggleShowOptions(expandedSummary, 1, true);
    component.event = Object.assign({}, eventMock);

    expect(expandedSummary).toEqual([[false, true], [true, true]]);
  });

  describe('sortOptionsEnabledFn', () => {
    it('general flow', () => {
      component.event = Object.assign({}, eventMock);
      component.sortOptionsEnabled = false;
      component.selectedMarket = 'Test Tab';
      component.toteLabel = 'Totepool';
      const market = component.event.markets[0];
      expect(component.sortOptionsEnabledFn(true, false, market)).toBeFalsy();

      component.sortOptionsEnabled = true;
      expect(component.sortOptionsEnabledFn(true)).toBeTruthy();
      market.outcomes[0].prices = [
        {
          id: '210',
          priceType: 'LP',
          priceNum: '4',
          priceDen: '1',
          priceDec: 5,
          isActive: 'true',
          displayOrder: '1',
          isDisplayed: true,
          liveShowTimer: {}
        }
      ] as any;
      expect(component.sortOptionsEnabledFn(true, false, market)).toBeTruthy();

      market.outcomes[0].prices = [];
      expect(component.sortOptionsEnabledFn(true, false, market)).toBeFalsy();

      expect(component.sortOptionsEnabledFn(false)).toBeFalsy();

      component.selectedMarket = 'Totepool';
      expect(component.sortOptionsEnabledFn(true)).toBeFalsy();
    });

    it('should not show sort option when there are no prices and no market in params', () => {
      component.event = Object.assign({}, eventMock);
      component.selectedMarket = 'Top Finish';
      component.event.sortedMarkets = [
        { name: 'Top Finish', markets: [{ id: '14213044' }] }, { name: 'More Markets' }
      ] as any;
      const market = undefined;

      expect(component.sortOptionsEnabledFn(false, true, market)).toBeFalsy();
    });

    it('should show sort option when there are prices and and no market in params', () => {
      component.event = Object.assign({}, eventMock);
      component.sortOptionsEnabled = true;
      component.selectedMarket = 'Top Finish';
      component.event.sortedMarkets = [
        {
          name: 'Top Finish', markets: [{
            id: '14213044', outcomes: [
              { prices: [{ id: '1' }, { id: '2' }], isLpAvailable: true }
            ], isLpAvailable: true
          }]
        },
        { name: 'More Markets' }
      ] as any;
      const market = undefined;

      expect(component.sortOptionsEnabledFn(true, true, market)).toBeTruthy();
    });

    it('should be truthy if selectedMarket is not defined', () => {
      component.event = Object.assign({}, eventMock);
      component.sortOptionsEnabled = true;
      component.selectedMarket = undefined;
      component.toteLabel = 'Tote';
      component.event.sortedMarkets = [
        { name: 'Win or Each Way', label: 'Win or E/W' },
        { label: 'Forecast', path: 'forecast' },
        { label: 'Totepool', path: 'totepool' }
      ] as any;

      expect(component.sortOptionsEnabledFn(true, true)).toBeTruthy();
    });

    it('should be truthy if selected market do not have markets', () => {
      component.event = Object.assign({}, eventMock);
      component.sortOptionsEnabled = true;
      component.selectedMarket = 'Win or Each Way';
      component.toteLabel = 'Tote';
      component.event.sortedMarkets = [
        { name: 'Win or Each Way', label: 'Win or E/W' },
        { label: 'Forecast', path: 'forecast' },
        { label: 'Totepool', path: 'totepool' }
      ] as any;

      expect(component.sortOptionsEnabledFn(true, true)).toBeTruthy();
    });

    it('should be falsy if prices are not appropriate prices to sort', () => {
      component.event = Object.assign({}, eventMock);
      component.sortOptionsEnabled = true;
      component.selectedMarket = 'Win Only';
      component.event.sortedMarkets = [
        { name: 'Win or Each Way', label: 'Win or E/W' },
        { label: 'Forecast', path: 'forecast' },
        { label: 'Totepool', path: 'totepool' },
        { name: 'Win Only', label: 'Win Only', outcomes: [{ prices: [] }, { prices: [] }] },
      ] as any;

      expect(component.sortOptionsEnabledFn(true, true)).toBeFalsy();
    });

    it('should be truthy if there are appropriate prices to sort', () => {
      component.event = Object.assign({}, eventMock);
      component.sortOptionsEnabled = true;
      component.selectedMarket = 'Win Only';
      component.event.sortedMarkets = [
        { name: 'Win or Each Way', label: 'Win or E/W' },
        { label: 'Forecast', path: 'forecast' },
        { label: 'Totepool', path: 'totepool' },
        {
          name: 'Win Only', label: 'Win Only', isLpAvailable: true,
          outcomes: [{ prices: [{ priceDen: 12, priceNum: 4 }] }]
        },
      ] as any;

      expect(component.sortOptionsEnabledFn(true, true)).toBeTruthy();
    });
  });

  describe('new test case for GA tracking', () => {
    it('#calling toggleShowOptionsGATracking when isGreyhoundEdp is false', () => {
      component.event = Object.assign({}, eventMock);
      component.isGreyhoundEdp = false;
      component.toggleShowOptionsGATracking(false);
      expect(racingGaService.toggleShowOptionsGATracking).toHaveBeenCalledWith(component.event, false, false);
    });

    it('#calling toggleShowOptionsGATracking when isGreyhoundEdp is true', () => {
      component.event = Object.assign({}, eventMock);
      component.isGreyhoundEdp = true;
      component.toggleShowOptionsGATracking(true);
      expect(racingGaService.toggleShowOptionsGATracking).toHaveBeenCalledWith(component.event, true, true);
    });
  });

  describe('showWatchAndInsights', () => {
    it('EVFLAG_PVM', () => {
      component.event = {
        drilldownTagNames: ['EVFLAG_PVM'],
        isUKorIRE: true,
        categoryId: HORSE_RACING_CATEGORY_ID
      } as any;
      component.insightsDrillDownTags = ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'];
      expect(component.showWatchAndInsights()).toBeTruthy();
    });

    it('EVFLAG_PVA', () => {
      component.event = {
        drilldownTagNames: ['EVFLAG_PVA'],
        isUKorIRE: true,
        categoryId: HORSE_RACING_CATEGORY_ID
      } as any;
      component.insightsDrillDownTags = ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'];
      expect(component.showWatchAndInsights()).toBeTruthy();
    });

    it('EVFLAG_TEST: should return false', () => {
      component.event = {
        drilldownTagNames: ['EVFLAG_TEST'],
        isUKorIRE: true,
        categoryId: HORSE_RACING_CATEGORY_ID
      } as any;
      component.insightsDrillDownTags = ['EVFLAG_PVM', 'EVFLAG_PVA', 'EVFLAG_RVA'];
      expect(component.showWatchAndInsights()).toBeFalsy();
    });
  });

  it('#onLiveStreamStarted  set videoStreamStarted to true', () => {
    component.onLiveStreamStarted();
    expect(component.videoStreamStarted).toBeTruthy();
  });

  it('#onPlayerLoadedStatus  set playerLoaded to true', () => {
    component.onPlayerLoadedStatus();
    expect(component.playerLoaded).toBeTruthy();
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
      component.event = { id: '123' } as any;
      // component.event = Object.assign({}, eventMock);
    });

    it('should apply sorting on init and subscription', () => {
      component.sortBy = 'price';
      component.event.markets = unSortedMarkets as any;
      component['syncToApplySorting']();

      expect(component['applySortBy']).toHaveBeenCalled();
    });

    it('should apply sorting by name', () => {
      sbFilters.orderOutcomesByName = jasmine.createSpy().and.returnValue(sortedByName);
      component.expandedSummary = [];
      component.sortBy = 'Name';
      component.event.markets = unSortedMarkets as any;
      component['syncToApplySorting']();

      expect(component.event.markets[0].outcomes[0].runnerNumber as any).toEqual(sortedByName[0].runnerNumber);
    });

    it('should apply sorting by price', () => {
      component.expandedSummary = [];
      component.sortBy = 'Price';
      component.event.markets = unSortedMarkets as any;
      component['applySortBy'] = jasmine.createSpy('applySortBy');
      component['syncToApplySorting']();
      expect(component['applySortBy']).toHaveBeenCalled();
    });
    it('#Should call updateGATracking and applySortBy', () => {
      component.isGreyhoundEdp = true;
      component.sortBy = 'price';
      component.event.markets = unSortedMarkets as any;
      component['syncToApplySorting']();
      expect(component['applySortBy']).toHaveBeenCalled();
    });
    it('#Should call SORT_BY_OPTION pubsub with event id null', () => {
      component.isGreyhoundEdp = true;
      component.sortBy = 'price';
      component.event.markets = unSortedMarkets as any;
      component.sortOptionsEnabled = true;
      component['pubsub'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === pubsub.API.SORT_BY_OPTION) {
          fn();
        }
      });
      component.event.id = null;
      component['syncToApplySorting']();
      expect(component['applySortBy']).toHaveBeenCalled();
    });
  });

  it('#applySortByName runnerNumber', () => {
    component['setMarketsInfo'] = jasmine.createSpy('setMarketsInfo');
    component.expandedSummary = [];
    component.sortBy = 'Price';
    component.event = {
      markets: [{
        template: 'WinEw',
        outcomes: [
          { name: 'unnamed favourite', isFavourite: true, prices: [] }, { name: '', isFavourite: false, prices: [] },
          { runnerNumber: '1', name: 'Test (RES)', displayOrder: 2 }
        ]
      }]
    } as any;
    sbFilters.orderOutcomesByName = jasmine.createSpy().and.returnValue([
      { name: 'unnamed favourite', isFavourite: true, prices: [] }, { name: '', isFavourite: false, prices: [] },
      { runnerNumber: '1', name: 'Test (RES)', displayOrder: 2 }
    ]);
    component['applySortByName']();

    component.event = {
      markets: [{
        template: 'WinEw',
        outcomes: [
          { name: 'unnamed favourite', isFavourite: true, prices: [] }, { name: '', isFavourite: false, prices: [] },
          { name: 'Test', displayOrder: 2 }
        ]
      }]
    } as any;
    sbFilters.orderOutcomesByName = jasmine.createSpy().and.returnValue([
      { name: 'unnamed favourite', isFavourite: true, prices: [] }, { name: '', isFavourite: false, prices: [] },
      { runnerNumber: '1', name: 'Test (RES)', displayOrder: 2, children: [{ price: 1 }] }
    ]);
    component['applySortByName']();
    sbFilters.orderOutcomesByName = jasmine.createSpy().and.returnValue([
      { name: 'unnamed favourite', isFavourite: true, prices: [] }, { name: '', isFavourite: false, prices: [] },
      { runnerNumber: '1', name: 'Test (RES)', displayOrder: 2, children: [{ price: 0 }] }
    ]);
    component['applySortByName']();
    sbFilters.orderOutcomesByName = jasmine.createSpy().and.returnValue([
      { name: 'unnamed favourite', isFavourite: true, prices: [] }, { name: '', isFavourite: false, prices: [] },
      { runnerNumber: '1', name: 'Test (RES)', displayOrder: 2, children: [{}] }
    ]);
    component['applySortByName']();
    sbFilters.orderOutcomesByName = jasmine.createSpy().and.returnValue([
      { name: 'unnamed favourite', isFavourite: true, prices: [] }, { name: '', isFavourite: false, prices: [] },
      { runnerNumber: '1', name: 'Test (RES)', displayOrder: 2, children: null }
    ]);
    component['applySortByName']();
    expect(component['setMarketsInfo']).toHaveBeenCalled();
  });

  it('applySortBy', () => {
    component['setOutcomeFavourite'] = jasmine.createSpy('setOutcomeFavourite');
    component.event = { id: '123' } as any;
    component.event.markets = unSortedMarkets as any;
    component.market = unSortedMarkets[0] as any;
    component.sortBy = null;
    component.expandedSummary = [];
    component['applySortBy']('PRICE');

    expect(component.sortBy).toBe('PRICE');
    expect(sbFilters.orderOutcomeEntities).toHaveBeenCalledWith(jasmine.any(Object), true, true, true, false, false, true);
    expect(component['setOutcomeFavourite']).toHaveBeenCalledWith(jasmine.any(Object));

    component['applySortBy']('RACECARD');
    expect(component.sortBy).toBe('RACECARD');
    expect(sbFilters.orderOutcomeEntities).toHaveBeenCalledWith(jasmine.any(Object), true, true, true, false, false, true);
  });

  it('racingService when not in horse racing sport', () => {
    component.isHorseRacingScreen = false;
    const result = component['racingService'];
    expect(result.getConfig().name).toEqual('greyhound');
  });

  it('#calculateVideoPlayerHeight ', () => {
    performGroupService.getElementWidth.and.returnValue(700);
    component['calculateVideoPlayerHeight']();
    expect(component.frameWidth).toEqual(600);

    performGroupService.getElementWidth.and.returnValue(500);
    component['calculateVideoPlayerHeight']();
    expect(component.frameWidth).toEqual(500);

    performGroupService.getElementWidth.and.returnValue(500);
    component['calculateVideoPlayerHeight']();
    component.frameWidth = 500;
    expect(component.frameWidth).toEqual(500);
  });
});