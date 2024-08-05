import { LadbrokesRacingEventComponent } from './racing-event.component';
import { RacingEventComponent } from '@racing/components/racingEventComponent/racing-event.component';

import { of as observableOf } from 'rxjs';
import { eventMock } from '@racing/components/racingEventComponent/racing-event.component.mock';

describe('LadbrokesRacingEventComponent', () => {
  let component: LadbrokesRacingEventComponent;
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
  let changeDetectorRef;
  let tools;
  let sbFilters;
  let location;
  let router;
  let sortByOptionsService;
  let route;
  let watchRulesService;
  let seoDataService;
  let elementRef;
  let racingGaService;

  beforeEach(() => {
    route = {
      snapshot: {
        queryParams: {}
      }
    };
    pubSubService = {
      API: {
        CLOSE_SORT_BY: 'CLOSE_SORT_BY',
        SORT_BY_OPTION: 'SORT_BY_OPTION'
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
        channelFunction('price');
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish')
    };
    windowRef = {
      nativeWindow: {
        document: {
          querySelector: jasmine.createSpy().and.returnValue({
            style: {},
            offsetHeight: 123
          }),
          getElementById: jasmine.createSpy().and.returnValue({
            offsetWidth: 123
          })
        },
        scrollTo: jasmine.createSpy()
      }
    };
    changeDetectorRef = {
      detach: jasmine.createSpy(),
      detectChanges: jasmine.createSpy()
    };
    timeService = {
      getCurrentTime: jasmine.createSpy('getCurrentTime'),
      minutesToMiliseconds: jasmine.createSpy('minutesToMiliseconds')
    };
    nativeBridgeService = {
      hideVideoStream: jasmine.createSpy('hideVideoStream'),
      playerStatus: false
    };
    ukToteService = {
      getTotePoolEventIds: jasmine.createSpy('getTotePoolEventIds').and.returnValue(['1', '2', '3']),
      getPoolsForEvent: jasmine.createSpy('getPoolsForEvent').and.returnValue(observableOf(['1', '2', '3']))
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
      setTopBarData: jasmine.createSpy('setTopBarData'),
      validateTooltip: jasmine.createSpy('validateTooltip').and.returnValue(true)
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('url'),
      formResultedEdpUrl: jasmine.createSpy('formResultedEdpUrl')
    };
    cmsService = {
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
          return observableOf({
            SortOptions: {
              enabled: true
            },
            TotePools: {
              Enable_UK_Totepools: true
            }
          });
        }
      })
    };
    tools = {
      getDaySuffix: jasmine.createSpy('getDaySuffix').and.returnValue('th')
    };
    sbFilters = {
      orderOutcomeEntities: jasmine.createSpy('orderOutcomeEntities').and.returnValue(eventMock.markets[0].outcomes)
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl'),
      events: {
        subscribe: jasmine.createSpy('events')
      }
    };
    location = jasmine.createSpyObj('location', ['replaceState', 'go']);
    sortByOptionsService = {
      get: jasmine.createSpy('get').and.returnValue('Racecard'),
      set: jasmine.createSpy('set'),
    };
    watchRulesService = {
      shouldShowCSBIframe: jasmine.createSpy('shouldShowCSBIframe')
    };
    seoDataService = {};

    elementRef = {
      nativeElement: {
        querySelector: jasmine.createSpy().and.returnValue(null)
      }
    } as any;

    racingGaService = {
      trackEvent: jasmine.createSpy('trckEvent'),
      toggleShowOptionsGATracking: jasmine.createSpy('toggleShowOptionsGATracking')
    };

    createComponent();
  });

  function createComponent() {
    component = new LadbrokesRacingEventComponent(
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
  }

  it('#formatAntepostTerms', () => {
    expect(component.formatAntepostTerms('antepost odds places 123, 1,2,3')).toBe('antepost Odds Places 123, 1,2,3');
  });

  it('#selectFallbackMarket should fill some component properties', () => {
    component.eventEntity = {
      sortedMarkets: [{
        label: 'Win or E/W',
        path: 'win'
      }]
    } as any;
    component['selectFallbackMarket'](component.eventEntity.sortedMarkets[0]);
    expect(component.selectedMarket).toBe('Win or E/W');
    expect(component.selectedMarketPath).toBe('win');
    expect(component.selectedMarketTypePath).toBeNull();
  });

  describe('#ngOnInit', () => {
    it('case if have eventEntity', () => {
      RacingEventComponent.prototype.ngOnInit = jasmine.createSpy('super.ngOnInit');
      component.expandedSummary = [];
      component.eventEntity = Object.assign({}, eventMock);
      component.eventEntity.markets = [
        { priceTypeCodes: 'SP,', outcomes: [], isGpAvailable: false },
        { priceTypeCodes: 'SP,', outcomes: [], isGpAvailable: false }] as any;
      component.sportName = 'greyhound';
      component.ngOnInit();

      expect(component.isRacingPostVerdictAvailable).toBeDefined();
      expect(component.isSpOnly).toEqual(true);
      expect(component.racingPostVerdictData).toEqual({} as any);
    });

    it('case if haven\'t eventEntity', () => {
      RacingEventComponent.prototype.ngOnInit = jasmine.createSpy('super.ngOnInit');
      component.expandedSummary = [];
      component.eventEntity = null;
      component.ngOnInit();

      expect(component.isSpOnly).not.toBeDefined();
      expect(component.isRacingPostVerdictAvailable).not.toBeDefined();
      expect(component.racingPostVerdictData).not.toBeDefined();
    });

    it('isSpOnly should be true', () => {
      RacingEventComponent.prototype.ngOnInit = jasmine.createSpy('super.ngOnInit');
      component.expandedSummary = [];
      component.eventEntity = Object.assign({}, eventMock);
      component.eventEntity.markets = [
        { priceTypeCodes: 'SP,', outcomes: [], isGpAvailable: true },
        { priceTypeCodes: 'SP,', outcomes: [] }] as any;
      component.ngOnInit();

      expect(component.isSpOnly).toBeTruthy();
    });

    it('isSpOnly should be false', () => {
      RacingEventComponent.prototype.ngOnInit = jasmine.createSpy('super.ngOnInit');
      component.expandedSummary = [];
      component.eventEntity = Object.assign({}, eventMock);
      component.ngOnInit();

      expect(component.isSpOnly).toBeFalsy();
    });

    it('should sort selections by racecard if there are all the runners numbers', () => {
      const unSortedMarkets = [{
        isLpAvailable: 'true',
        priceTypeCodes: 'SP,',
        outcomes: [{
          runnerNumber: 3,
          name: 'aname',
          prices: []
        }, {
          runnerNumber: 7,
          name: 'zname',
          prices: []
        }, {
          runnerNumber: 1,
          name: 'bname',
          prices: []
        }]
      }];
      const sortedByRacecard = [{
        isLpAvailable: 'true',
        priceTypeCodes: 'SP,',
        outcomes: [{
          runnerNumber: 1,
          name: 'bname',
          prices: []
        }, {
          runnerNumber: 3,
          name: 'aname',
          prices: []
        }, {
          runnerNumber: 7,
          name: 'zname',
          prices: []
        }]
      }];
      sbFilters.orderOutcomeEntities = jasmine.createSpy().and.returnValue(sortedByRacecard[0].outcomes);
      component.expandedSummary = [];
      component.eventEntity = Object.assign({}, eventMock);
      component.eventEntity.markets = unSortedMarkets as any;
      component.ngOnInit();

      expect(component.eventEntity.markets[0].outcomes as any).toEqual(sortedByRacecard[0].outcomes);
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

  it('onExpandSection checker false', () => {
    const expandedSummary = [[false], [false]];
    component.eventEntity = Object.assign({}, eventMock);
    component.onExpandSection(expandedSummary, 1, 0);

    expect(expandedSummary).toEqual([[false], [true]]);
    expect(component.isInfoHidden.info).toEqual(true);
  });

  it('onExpandSection ', () => {
    const expandedSummary = [[true], [true]];
    component.eventEntity = Object.assign({}, eventMock);
    component.onExpandSection(expandedSummary, 1, 0);

    expect(expandedSummary).toEqual([[true], [false]]);
    expect(component.isInfoHidden.info).toEqual(false);

  });

  it('toggleShowOptions', () => {
    const expandedSummary = [[false, true], [true, false]];
    component.eventEntity = Object.assign({}, eventMock);
    component.toggleShowOptions(expandedSummary, 1, true);

    expect(expandedSummary).toEqual([[false, true], [true, true]]);
  });
  it('#Should call onExpandSection GA Tracking when true', () => {
    const expandedSummary = [[true], [true]];
    component.eventEntity = Object.assign({}, eventMock);
    component.onExpandSection(expandedSummary, 1, 0);
    component.isGreyhoundEdp = true;
    const expectedParams = ['trackEvent', {
      event: 'trackEvent',
      eventAction: 'race card',
      eventCategory: "horse racing",
      eventLabel: 'show less',
      categoryID: '21',
      typeID: '1909',
      eventID: 11818323
    }];
    expect(component.isGreyhoundEdp).toBeTruthy()
    expect(gtmService.push).toHaveBeenCalledWith(...expectedParams);
  });

  it('#Should call onExpandSection GA Tracking when greyhounds', () => {
    const expandedSummary = [[true], [true]];
    component.eventEntity = Object.assign({}, eventMock);
    component.isGreyhoundEdp = true;
    component.onExpandSection(expandedSummary, 1, 0);
    const expectedParams = ['trackEvent', {
      event: 'trackEvent',
      eventAction: 'race card',
      eventCategory: "greyhounds",
      eventLabel: 'show less',
      categoryID: '21',
      typeID: '1909',
      eventID: 11818323
    }];
    expect(component.isGreyhoundEdp).toBeTruthy()
    expect(gtmService.push).toHaveBeenCalledWith(...expectedParams);
  });
  describe('toggleShowOptions for GA tracking', () => {
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
});
