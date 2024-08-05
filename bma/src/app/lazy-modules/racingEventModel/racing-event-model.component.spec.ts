import { of as observableOf } from 'rxjs';
import { DesktopRacingEventModelComponent } from './racing-event-model.component';
import { IMarket } from '@core/models/market.model';

describe('Coral DesktopRacingEventModelComponent', () => {
  let component: DesktopRacingEventModelComponent;
  let windowRef;
  let timeService;
  let pubSubService;
  let nativeBridgeService;
  let ukToteService;
  let lpAvailabilityService;
  let deviceService;
  let gtmService;
  let streamTrackingService;
  let dialogService;
  let filterService;
  let localeService;
  let horseracingService;
  let routingHelperService;
  let cmsService;
  let coreToolsService;
  let sbFiltersService;
  let routerService;
  let locationService;
  let sortByOptionsService;
  let eventEntity;
  let route;
  let pools;
  let changeDetectorRef;
  let watchRulesService;
  let seoDataService;
  let elementRef;
  let racingGaService;
  const market = {
    cashoutAvail: '',
    correctPriceTypeCode: '',
    dispSortName: '',
    eachWayFactorNum: '',
    eachWayFactorDen: '',
    eachWayPlaces: '',
    id: '',
    isLpAvailable: true,
    isMarketBetInRun: true,
    isSpAvailable: true,
    liveServChannels: '',
    isEachWayAvailable: false,
    liveServChildrenChannels: '',
    marketsNames: '',
    marketStatusCode: '',
    name: 'test',
    nextScore: 0,
    outcomes: [],
    periods: [],
    priceTypeCodes: '',
    terms: '',
    templateMarketId: 0,
    templateMarketName: '',
    viewType: 'inplay',
    label: 'label',
    isTopFinish: true,
    isToFinish: false,
    collapseMarket: false,
    insuranceMarkets: false,
    isOther: true,
    isWO: false
  } as IMarket;
  const topFinishedMarket = {
    cashoutAvail: '',
    correctPriceTypeCode: '',
    dispSortName: '',
    eachWayFactorNum: '',
    eachWayFactorDen: '',
    eachWayPlaces: '',
    id: '',
    isLpAvailable: true,
    isMarketBetInRun: true,
    isSpAvailable: true,
    liveServChannels: '',
    isEachWayAvailable: false,
    liveServChildrenChannels: '',
    marketsNames: '',
    marketStatusCode: '',
    name: 'Ante-post',
    nextScore: 0,
    outcomes: [],
    periods: [],
    priceTypeCodes: '',
    terms: '',
    templateMarketId: 0,
    templateMarketName: '',
    viewType: 'inplay',
    label: 'sb.topFinishMarkets',
    isTopFinish: true,
    isToFinish: false,
    insuranceMarkets: false,
    isOther: true,
    isWO: false
  } as IMarket;
  


  beforeEach(() => {
    route = {
      snapshot: {
        queryParams: {}
      }
    };
    eventEntity = {
      id: 1,
      name: 'Event Name',
      startTime: 1540915600000,
      terms: 'Each Way: undefined/undefined odds - places ',
      label: 'Win Only',
      isUKorIRE: true,
      racingFormEvent:{
        overview:'test'
      },
      markets: [{
        id: '22',
        eventId: '1',
        label: 'Outcome name',
        outcomes: [{
          id: '333',
          marketId: '22',
          name: 'Outcome name',
          prices: [{
            id: '4444',
            priceType: 'LP',
            priceNum: '4',
            priceDen: '1',
            priceDec: 5,
            isActive: 'true',
            displayOrder: '1',
            isDisplayed: true
          }]
        }]
      }],
      sortedMarkets: [{
        label: 'Totepool',
        path: 'totepool',
      }],
      outcomes: []
    };
    pools = [{
      id: 11478540,
      provider: 'U',
      type: 'UQDP',
      currencyCode: 'GBP',
      marketIds: ['422861483', '422861484', '422861485', '422861486'],
      legCount: '4',
      isActive: true,
      minTotalStake: '1.00',
      maxTotalStake: '1000000.00',
      minStakePerLine: '0.10',
      maxStakePerLine: '1000000.00',
      stakeIncrementFactor: '0.10',
      responseCreationTime: '2019-11-22T10:58:14.610Z',
      poolType: 'UQDP'
    }];
    windowRef = {
      nativeWindow: {
        clearInterval: jasmine.createSpy(),
        setInterval: jasmine.createSpy().and.callFake((fn, timer) => fn && fn()),
        document: {
          querySelector: jasmine.createSpy(),
          removeEventListener: jasmine.createSpy(),
          getElementById: jasmine.createSpy().and.returnValue({
            offsetWidth: 123
          }),
          addEventListener: jasmine.createSpy(),
        },
        scrollTo: jasmine.createSpy()
      }
    };
    timeService = {
      getCurrentTime: jasmine.createSpy(),
      minutesToMiliseconds: jasmine.createSpy(),
      formatByPattern: jasmine.createSpy().and.returnValue('2018-11-7')
    };
    pubSubService = {
      API: {
        CLOSE_SORT_BY: 'CLOSE_SORT_BY',
        SORT_BY_OPTION: 'SORT_BY_OPTION'
      },
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      publish: jasmine.createSpy()
    };
    nativeBridgeService = {
      hideVideoStream: jasmine.createSpy(),
      playerStatus: false
    };
    ukToteService = {
      getTotePoolEventIds: jasmine.createSpy(),
      getPoolsForEvent: jasmine.createSpy()
    };
    lpAvailabilityService = {
      check: jasmine.createSpy()
    };
    deviceService = {
      isTablet: true,
      isDesktop: true,
      isWrapper: true,
      isTabletLandscape: false
    };
    gtmService = {
      push: jasmine.createSpy()
    };
    streamTrackingService = {
      checkIdForDuplicates: jasmine.createSpy(),
      addIdToTrackedList: jasmine.createSpy()
    };
    dialogService = {
      openDialog: jasmine.createSpy()
    };
    filterService = {
      distance: jasmine.createSpy(),
      orderBy: jasmine.createSpy().and.returnValue(eventEntity.markets),
      date: jasmine.createSpy().and.returnValue('2018-11-7')
    };
    localeService = {
      getString: jasmine.createSpy()
    };
    horseracingService = {
      getEvent: jasmine.createSpy(),
      sortMarketsName: jasmine.createSpy().and.returnValue(eventEntity),
      sortRacingMarketsByTabs: jasmine.createSpy().and.returnValue(eventEntity.markets),
      getSortingFromCms: jasmine.createSpy('getSortingFromCms').and.returnValue({}),
      isToteForecastTricasMarket: jasmine.createSpy('isToteForecastTricasMarket').and.returnValue(true)
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy(),
      formResultedEdpUrl: jasmine.createSpy()
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        SortOptions: {
          enabled: true
        },
        TotePools: {
          Enable_UK_Totepools: true
        },
        RacingEDPMarketsDescription: {
          enabled: false
        },
        enabled: true,
        title: 'welcome'
      })),
      getFeatureConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        enabled: true,
        title: 'welcome'
      }))
    };
    coreToolsService = {
      getDaySuffix: jasmine.createSpy()
    };
    sbFiltersService = {
      orderOutcomeEntities: jasmine.createSpy()
    };
    routerService = {
      navigateByUrl: jasmine.createSpy(),
      events: {
        subscribe: jasmine.createSpy()
      }
    };
    locationService = jasmine.createSpyObj('location', ['replaceState', 'go']);
    changeDetectorRef = {};
    sortByOptionsService = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set'),
    };

    changeDetectorRef = seoDataService = {};

    watchRulesService = {
      shouldShowCSBIframe: jasmine.createSpy('shouldShowCSBIframe')
    };

    elementRef = {
      nativeElement: {
        querySelector: jasmine.createSpy().and.returnValue({ class: 'market-container' })
      }
    } as any;

    racingGaService = {
      trackEvent: jasmine.createSpy('trckEvent')
    };

    component = new DesktopRacingEventModelComponent(
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
      horseracingService,
      routingHelperService,
      cmsService,
      coreToolsService,
      sbFiltersService,
      routerService,
      locationService,
      changeDetectorRef,
      sortByOptionsService,
      route,
      watchRulesService,
      seoDataService,
      elementRef,
      racingGaService
    );
    component.eventEntity = eventEntity;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });
  describe('#addForecastTricastTabs', () => {
    describe('#addForecastTricastTabs TotePools, InternationalTotePool configs', () => {
      beforeEach(() => {
        const poolEventEntities = [{
          id: 229472480,
          name: '3m HCap Chase',
          eventStatusCode: 'A',
          isActive: true
        }];

        ukToteService.getTotePoolEventIds.and.returnValue(['229472480']);
        ukToteService.getPoolsForEvent.and.returnValue(observableOf(pools));
        horseracingService.getEvent.and.returnValue(observableOf(poolEventEntities));

        component['addTotePoolTab'] = jasmine.createSpy('addTotePoolTab');
        component['setMarketTabs'] = jasmine.createSpy('setMarketTabs');
        component['selectFallbackMarket'] = jasmine.createSpy('selectFallbackMarket');
        component['getMarketByPath'] =
          jasmine.createSpy('getMarketByPath').and.returnValue({ label: 'Totepool', path: 'totepool' });
        component['getTotePoolTypeByPath'] =
          jasmine.createSpy('getTotePoolTypeByPath').and.returnValue('Totepool type');
      });

      it('should call selectedFallbackMarket when isTotepoolMarket = true, Enable_UK_Totepools = false', () => {
        cmsService.getSystemConfig.and.returnValue(observableOf({
          TotePools: {
            Enable_UK_Totepools: false
          }
        }));
        component.selectedMarketPath = 'totepool';

        component.configForecastTricastTabs();

        expect(component.selectedMarketTypePath).toEqual(undefined);
        expect(component['selectFallbackMarket']).toHaveBeenCalled();
      });

      it('should add ForecastTricasTab', () => {
        cmsService.getSystemConfig.and.returnValue(observableOf({
          TotePools: {
            Enable_UK_Totepools: true
          },
          InternationalTotePool: {
            Enable_International_Totepools: false,
            Enable_International_Totepools_On_RaceCard: true
          }
        }));

        component.configForecastTricastTabs();

        expect(component.selectedMarketTypePath).toEqual(undefined);
        expect(component['setMarketTabs']).toHaveBeenCalled();
      });

      it('should call selectFallbackMarket, selectedMarketPath = false', () => {
        cmsService.getSystemConfig.and.returnValue(observableOf({
          TotePools: {
            Enable_UK_Totepools: false
          },
          InternationalTotePool: {
            Enable_International_Totepools: true,
            Enable_International_Totepools_On_RaceCard: true
          }
        }));
        eventEntity.isUKorIRE = false;

        component.selectedMarketPath = '';

        component.configForecastTricastTabs();

        expect(component['addTotePoolTab']).toHaveBeenCalled();
        expect(component.selectedMarketTypePath).toEqual(undefined);
        expect(component['setMarketTabs']).toHaveBeenCalled();
      });

      it('should call getMarketByPath', () => {
        cmsService.getSystemConfig.and.returnValue(observableOf({
          TotePools: {
            Enable_UK_Totepools: false
          },
          InternationalTotePool: {
            Enable_International_Totepools: true,
            Enable_International_Totepools_On_RaceCard: true
          }
        }));
        eventEntity.isUKorIRE = false;

        component.selectedMarketPath = 'totepool';

        component.configForecastTricastTabs();

        expect(component['addTotePoolTab']).toHaveBeenCalled();
        expect(component.selectedMarket).toEqual('Totepool');
        expect(component.selectedMarketType).toEqual('Totepool type');
        expect(component['setMarketTabs']).toHaveBeenCalled();
      });

      it('should call empty()', () => {
        cmsService.getSystemConfig.and.returnValue(observableOf({
          TotePools: {
            Enable_UK_Totepools: false
          }
        }));
        component.selectedMarketPath = '';

        component.configForecastTricastTabs();

        // expect to call empty()
      });
    });

    describe('#addForecastTricastTabs check poolEventIds', () => {
      beforeEach(() => {
        const poolEventEntities = [{
          id: 229472480,
          name: '3m HCap Chase',
          eventStatusCode: 'A',
          isActive: true
        }];

        component['addTotePoolTab'] = jasmine.createSpy('addTotePoolTab');
        component['setMarketTabs'] = jasmine.createSpy('setMarketTabs');
        horseracingService.getEvent.and.returnValue(observableOf(poolEventEntities));
        component['selectFallbackMarket'] = jasmine.createSpy('selectFallbackMarket');
        component['getMarketByPath'] =
          jasmine.createSpy('getMarketByPath').and.returnValue({ label: 'Totepool', path: 'totepool' });
        component['getTotePoolTypeByPath'] =
          jasmine.createSpy('getTotePoolTypeByPath').and.returnValue('Totepool type');
      });

      it('shoud get totel label', () => {
        component.configForecastTricastTabs();

        expect(localeService.getString).toHaveBeenCalledWith('uktote.totepool');
      });

      it('should call addForecastTricast tab', () => {
        ukToteService.getTotePoolEventIds.and.returnValue(['229472480']);
        ukToteService.getPoolsForEvent.and.returnValue(observableOf(pools));

        component.configForecastTricastTabs();

        expect(component['addTotePoolTab']).toHaveBeenCalled();
        expect(component.selectedMarket).toEqual(undefined);
        expect(component['setMarketTabs']).toHaveBeenCalled();
      });

      it('should call selectFallbackMarket when poolEventIds is empty and isTotepoolMarket = true', () => {
        ukToteService.getTotePoolEventIds.and.returnValue([]);

        component.selectedMarketPath = 'totepool';
        component.configForecastTricastTabs();

        expect(component['selectFallbackMarket']).toHaveBeenCalled();
      });

    });

    describe('#addForecastTricastTabs check pools', () => {
      beforeEach(() => {
        const poolEventEntities = [{
          id: 229472480,
          name: '3m HCap Chase',
          eventStatusCode: 'A',
          isActive: true
        }];

        component['addTotePoolTab'] = jasmine.createSpy('addTotePoolTab');
        component['setMarketTabs'] = jasmine.createSpy('setMarketTabs');
        component['isAllowedPool'] = jasmine.createSpy('isAllowedPool').and.returnValue(true);
        horseracingService.getEvent.and.returnValue(observableOf(poolEventEntities));
        component['selectFallbackMarket'] = jasmine.createSpy('selectFallbackMarket');
        component['getMarketByPath'] =
          jasmine.createSpy('getMarketByPath').and.returnValue({ label: 'Totepool', path: 'totepool' });
        component['getTotePoolTypeByPath'] =
          jasmine.createSpy('getTotePoolTypeByPath').and.returnValue('Totepool type');
      });

      it('should have pools', () => {
        ukToteService.getTotePoolEventIds.and.returnValue(['229472480']);
        ukToteService.getPoolsForEvent.and.returnValue(observableOf(pools));

        component.configForecastTricastTabs();

        expect(component['addTotePoolTab']).toHaveBeenCalled();
        expect(component['isAllowedPool']).toHaveBeenCalled();
        expect(component.selectedMarket).toEqual(undefined);
        expect(component['setMarketTabs']).toHaveBeenCalled();
      });

      it('should call empty()', () => {
        ukToteService.getTotePoolEventIds.and.returnValue([]);
        ukToteService.getPoolsForEvent.and.returnValue(observableOf(null));

        component.selectedMarketPath = '';
        component.configForecastTricastTabs();

        // expect to call empty()
      });

      it('should have pools, selectedMarket,  selectedMarketType', () => {
        ukToteService.getTotePoolEventIds.and.returnValue(['229472480']);
        ukToteService.getPoolsForEvent.and.returnValue(observableOf(pools));

        component.selectedMarketPath = 'totepool';

        component.configForecastTricastTabs();

        expect(component['addTotePoolTab']).toHaveBeenCalled();
        expect(component.selectedMarket).toEqual('Totepool');
        expect(component.selectedMarketType).toEqual('Totepool type');
        expect(component['setMarketTabs']).toHaveBeenCalled();
        expect(horseracingService.getEvent).toHaveBeenCalled();
      });

      it('should call selectFallbackMarket when pools is empty', () => {
        ukToteService.getTotePoolEventIds.and.returnValue(['229472480']);
        ukToteService.getPoolsForEvent.and.returnValue(observableOf(null));

        component.selectedMarketPath = 'totepool';
        component.configForecastTricastTabs();

        expect(component['selectFallbackMarket']).toHaveBeenCalled();
      });

      it('should not call selectFallbackMarket when pools is not empty', () => {
        ukToteService.getTotePoolEventIds.and.returnValue(['229472480']);
        ukToteService.getPoolsForEvent.and.returnValue(observableOf(null));

        component.selectedMarketPath = 'test';
        component.configForecastTricastTabs();

        expect(component['selectFallbackMarket']).not.toHaveBeenCalled();
      });
    });
  });

  it('should sort racing markets according to eventId', () => {
    component.ngOnInit();
    expect(component.eventId).toEqual(eventEntity.id);
    expect(horseracingService.sortMarketsName).toHaveBeenCalled();
    expect(horseracingService.sortRacingMarketsByTabs).toHaveBeenCalledWith(eventEntity.markets, eventEntity.id.toString());
  });

  it('Check selected market', () => {
    component.ewLabel = 'Outcome name';
    component.ngOnInit();
    expect(component.selectedMarket).toEqual('Outcome name');
  });
  it('Check isTotepoolMarket and selectedMarketPath', () => {
    component.eventEntity.racingFormEvent = undefined;
    component.ngOnInit();
    component.selectedMarketPath = 'totepool';
    component.configForecastTricastTabs();
  });
  it('Should call change method and set selected market value', () => {
    component.change(market);
    
    expect(component.selectedMarket).toEqual('label');
    expect(component.isDescriptionAvailable).toBeFalse();
  });
  it('Should call formatEventTerms method and return eventTerms', () => {
    const result = component.formatEventTerms('testEvent9/9 ODDS');
    
    expect(result).toEqual('testEvent<strong>9/9 ODDS</strong>');
  });
  it('should call displayMarketHeader method and return marketEntity name as empty string', () => {
    component.selectedMarket = 'test';
    const result = component.displayMarketHeader(topFinishedMarket);
    
    expect(result).toEqual('');
  });
  it('Should call displayMarketHeader method and return marketEntity name as Ante-post', () => {
    component.selectedMarket = undefined;
    const result = component.displayMarketHeader(topFinishedMarket);
    
    expect(result).toEqual('');
  });
  it('Should call displayMarketHeader method and return marketEntity name as ""', () => {
    component.selectedMarket = undefined;
    topFinishedMarket.name = 'test';
    const result = component.displayMarketHeader(topFinishedMarket);
    
    expect(result).toEqual('test');
  });
  it('displayMarketPanel should return true if selected market name same as label',()=>{
    component.change(market);
    const result = component.displayMarketPanel(market);

    expect(result).toBeTrue;
  })
  it('displayMarketPanel should return false',()=>{
    component.selectedMarket = 'test123';
    const result = component.displayMarketPanel(market);

    expect(result).toEqual(false);
  })
  it('displayMarketPanel should return false',()=>{
    market.isToFinish = true;
    market.insuranceMarkets = true;
    market.isOther = true;
    market.isWO = true;
    component.selectedMarket = undefined;
    const result = component.displayMarketPanel(market);

    expect(result).toEqual(true);
  });
  it('ngOndestroy', ()=> {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('DesktopRacingEventModelComponent1');
  });
});
