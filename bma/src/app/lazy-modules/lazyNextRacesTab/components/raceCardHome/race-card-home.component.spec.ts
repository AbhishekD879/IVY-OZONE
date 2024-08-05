import { RaceCardHomeComponent } from './race-card-home.component';
import { fakeAsync } from '@angular/core/testing';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { of as observableOf } from 'rxjs';
import { IOutcome } from '@core/models/outcome.model';

describe('#RaceCardHomeComponent', () => {
  let component: RaceCardHomeComponent;
  let raceOutcomeData;
  let routingHelperService;
  let nextRacesHomeService;
  let localeService;
  let sbFiltersService;
  let filtersService;
  let pubSubService;
  let router;
  let eventService;
  let virtualSharedService;
  let datePipe;
  let changeDetectorRef;
  let cmsService;
  let sortByOptionsService;
  let horseracing;
  let cmsObservableResult;
  let racingGaService;


  const mockString = 'seeAll';
  let raceDataMock;

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

  const sortedByNameMock = [{
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

  beforeEach(fakeAsync(() => {
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
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue(mockString)
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    filtersService = {
      removeLineSymbol: jasmine.createSpy('removeLineSymbol')
    };
    nextRacesHomeService = {
      trackNextRace: jasmine.createSpy('trackNextRace'),
      isItvEvent: jasmine.createSpy('isItvEvent'),
      getGoing: jasmine.createSpy('getGoing'),
      getDistance: jasmine.createSpy('getDistance')
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl')
    };
    raceOutcomeData = {
      isGenericSilk: jasmine.createSpy('isGenericSilk'),
      isGreyhoundSilk: jasmine.createSpy('isGreyhoundSilk'),
      isNumberNeeded: jasmine.createSpy('isNumberNeeded'),
      getSilkStyle: jasmine.createSpy('getSilkStyle')
    };
    sbFiltersService = {
      orderOutcomeEntities: jasmine.createSpy('orderOutcomeEntities').and.returnValue([{
        id: 'outcome1'
      },
      {
        id: 'outcome2'
      }]),
      orderOutcomesByName: jasmine.createSpy('orderOutcomeEntities')
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    eventService = {
      isLiveStreamAvailable: jasmine.createSpy('isLiveStreamAvailable').and.returnValue({
        liveStreamAvailable: true
      })
    };
    virtualSharedService = {
      isVirtual: jasmine.createSpy('isVirtual').and.returnValue(true),
      formVirtualEventUrl: jasmine.createSpy('formVirtualEventUrl')
    };
    datePipe = {
      transform: () => '20:15'
    } as any;

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
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
          return observableOf(cmsObservableResult);
        }
      }),
      getFeatureConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf(cmsObservableResult))
    };
    cmsObservableResult = {
      SortOptions: {
        enabled: true
      },
    };
    sortByOptionsService = {
      get: jasmine.createSpy('get').and.returnValue('Price'),
      set: jasmine.createSpy('set'),
    };
    horseracing = {
      getEvent: jasmine.createSpy('getEvent').and.returnValue(Promise.resolve(['poolEventEntity'])),
      isRacingSpecials: jasmine.createSpy('isRacingSpecials'),
      setTopBarData: jasmine.createSpy('setTopBarData'),
      validateTooltip: jasmine.createSpy('validateTooltip').and.returnValue(true)
    };
    racingGaService = {
      updateGATracking: jasmine.createSpy('updateGATracking'),
    };

    component = new RaceCardHomeComponent(raceOutcomeData, routingHelperService, nextRacesHomeService, localeService,
      sbFiltersService, filtersService, pubSubService, router, eventService, virtualSharedService, datePipe, changeDetectorRef, cmsService, sortByOptionsService, horseracing, racingGaService);
    (component['_raceData'] as any) = raceDataMock;
    (component['_raceDataCollection'] as any) = raceDataMock;
  }));

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should call proper setter methods on raceData assign', () => {
    component['raceDataSub'].next = jasmine.createSpy();
    component['processOutcomes'] = jasmine.createSpy();
    component.raceData = raceDataMock;

    expect(component['_raceData'][0].markets[0].id).toEqual('12345');
    expect(component['processOutcomes']).toHaveBeenCalled();
    expect(component['raceDataSub'].next).toHaveBeenCalledWith(raceDataMock);
    expect(component.raceData$).toBeDefined();
  });

  it('should call proper setter methods on raceDataCollection assign', () => {
    component.raceDataCollection = raceDataMock;
    expect(component['_raceDataCollection'][0].markets[0].id).toEqual('12345');
  });

  describe('ngOnInit', () => {
    it('should init component', () => {
      component['processOutcomes'] = jasmine.createSpy();
      component.ngOnInit();

      expect(component.raceIndex).toEqual(0);
      expect(component.raceOrigin).toEqual('');
      expect(component.seeAllRaceText).toEqual('seeAll');
      expect(component.eventCategory).toEqual('widget');
      expect(component.limit).toEqual(undefined);
      expect(component.isShowAllActive).toBeFalsy();

      expect(localeService.getString).toHaveBeenCalledWith('sb.seeAll');
      expect(pubSubService.subscribe).toHaveBeenCalledWith('RaceCardHomeComponent123', 'OUTCOME_UPDATED', jasmine.any(Function));
    });

    it('should set limits for featured module', () => {
      component.isFeaturedRaceCard = true;
      component.selectionsLimit = 10;
      component.ngOnInit();

      expect(component.limit).toEqual(10);
    });

    it('should add race types to cards', () => {
      component['_raceData'][0].racingFormEvent = {
        raceType: 'raceType',
        distance: 'distance',
        going: 'going'
      };
      component.ngOnInit();

      expect(localeService.getString).toHaveBeenCalledWith('racing.raceType.raceType');
    });

    it('when no race data', () => {
      component['processOutcomes'] = jasmine.createSpy('processOutcomes');
      component.isFeaturedRaceCard = true;
      component['_raceData'][0] = undefined;
      component.ngOnInit();

      expect(component.isShowAllActive).toEqual(false);
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith('RaceCardHomeComponent', 'OUTCOME_UPDATED', jasmine.any(Function));
    });

    it('should set isShowAllActive for featured module', () => {
      const arrayOfOutcomesMock: any = [{}, {}, {}, {}, {}];
      component['_raceData'][0].markets[0].outcomes = component['_raceData'][0].markets[0].outcomes.concat(arrayOfOutcomesMock);

      component.isFeaturedRaceCard = true;
      component.selectionsLimit = 3;
      component.ngOnInit();

      expect(component.limit).toEqual(3);
      expect(component.isShowAllActive).toBeTruthy();
    });

    it('should process outcomes on OUTCOME_UPDATED', () => {
      spyOn(component as any, 'processOutcomes').and.callThrough();
      component.raceOrigin = 'uk';
      component['raceMarkets'] = ['1'];
      component.isFeaturedRaceCard = true;
      component.selectionsLimit = 1;
      const market = { id: '1', outcomes: [{}, {}] };
      pubSubService.subscribe.and.callFake((name, channel, cb) => cb(market));

      component.ngOnInit();
    });

    it('should not process outcomes on OUTCOME_UPDATED', () => {
      spyOn(component as any, 'processOutcomes').and.callThrough();
      component['raceMarkets'] = [];
      pubSubService.subscribe.and.callFake((name, channel, cb) => cb({ id: '1' }));

      component.ngOnInit();

      expect(component['processOutcomes']).toHaveBeenCalled();
    });

    it('should call router for virtual GH', () => {
      spyOn(component as any, 'processOutcomes').and.callThrough();
      router['url'] = 'greyhound - racing';
      component['raceMarkets'] = [];
      pubSubService.subscribe.and.callFake((name, channel, cb) => cb({ id: '1' }));

      component.ngOnInit();
      expect(component.isVirtualHR).toBeFalsy();

      router['url'] = 'horseracing - racing';
      component.ngOnInit();
      expect(component.isVirtualHR).toBeTruthy();
    });
  });

  describe('ngOnChanges', () => {
    it('#ngOnChanges should call processOutcomes', () => {
      spyOn(component as any, 'processOutcomes');
      component.ngOnChanges({raceData: raceDataMock} as any);
      expect(component['processOutcomes']).toHaveBeenCalled();
    });
  });
  describe('ngOnInit should handle WS_EVENT_UPDATED message', () => {
    it('and detect changes', () => {
      pubSubService.subscribe.and.callFake((nm, ch, cb) => ch === 'WS_EVENT_UPDATED' && cb({ id: 123 }));
      component.ngOnInit();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalledTimes(2);
    });

    it('and do not detect changes', () => {
      pubSubService.subscribe.and.callFake((nm, ch, cb) => ch === 'WS_EVENT_UPDATED' && cb({ id: 456 }));
      component.ngOnInit();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalledTimes(1);
    });
  });

  it('#toggleShow test component state', () => {
    component.allShown = false;
    component.isFeaturedRaceCard = true;
    component.selectionsLimit = 10;

    component.toggleShow();
    expect(component.allShown).toEqual(true);
    expect(component.limit).toEqual(undefined);

    component.toggleShow();
    expect(component.allShown).toEqual(false);
    expect(component.limit).toEqual(component.selectionsLimit);
  });

  it('#ngOnDestroy', () => {
    component['channelName'] = 'RaceCardHomeComponent123';

    component.ngOnDestroy();

    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('RaceCardHomeComponent123');
  });

  it('#trackByEvents', () => {
    const result = component.trackByEvents(1, ({
      id: '12345',
      name: 'name',
      categoryId: '12'
    } as any));

    expect(result).toEqual('1_12345_name_12');
  });

  it('#isEventVirtual', () => {
    const result = component.isEventVirtual(({
      id: '12345',
      name: 'name',
      categoryId: '39'
    } as any));

    expect(result).toEqual(true);
  });
  it('#trackByMarkets', () => {
    const result = component.trackByMarkets(1, ({
      id: '12345',
      name: 'name',
      marketStatusCode: 'A'
    } as any));

    expect(result).toEqual('1_12345_name_A');
  });

  it('#trackByOutcomes', () => {
    const result = component.trackByOutcomes(1, ({
      id: '12345',
      name: 'name',
      runnerNumber: '2'
    } as any));

    expect(result).toEqual('1_12345_name_2');
  });

  it('#removeLineSymbol', () => {
    component.removeLineSymbol('removeLineSymbol');

    expect(filtersService.removeLineSymbol).toHaveBeenCalledWith('removeLineSymbol');
  });

  describe('#getEventName', () => {
    it('should return name if event has nameOverride', () => {
      component.isVirtual = false;
      const result = component.getEventName(({
        typeName: 'London',
        name: 'London2',
        nameOverride: 'London1'
      }) as any);

      expect(result).toEqual('London1');
    });

    it('should return name if event without nameOverride', () => {
      component.isVirtual = false;
      const result = component.getEventName(({
        localTime: '2',
        typeName: 'London',
        name: 'London2'
      }) as any);

      expect(result).toEqual('2 London');
    });

    it('should return correct virtual name', () => {
      component.isVirtual = true;
      const event = { id: 1, categoryId: 39, name: '18:15 Laddies Leap\'s Lane' } as any;
      expect(component.getEventName(event)).toBe('18:15 Laddies Leap\'s Lane');
    });

    it('should return correct virtual name', () => {
      component.isVirtual = true;
      const event = { id: 1, categoryId: 39, name: '18:15 Laddies Leap\'s Lane',originalName: 'org', categoryCode: 'VIRTUAL'} as any;
      expect(component.getEventName(event)).toBe('org');
    });
  });

  describe('formEdpUrl', () => {
    it('should create EDP url', () => {
      component.formEdpUrl(({ id: '1' } as any));

      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith({ id: '1' });
    });

    it('should create Virtual url', () => {
      component.isVirtual = true;
      component.formEdpUrl(({ id: '2', categoryId: '39' } as any));

      expect(virtualSharedService.formVirtualEventUrl).toHaveBeenCalledWith({ id: '2', categoryId: '39' });
    });
  });

  it('#getRunnerNumber return runner number', () => {
    expect(component.getRunnerNumber({} as any)).toBe(undefined);
    expect(component.getRunnerNumber({ runnerNumber: '3' } as any)).toBe('3');
    expect(component.getRunnerNumber({ racingFormOutcome: {} } as any)).toBe(undefined);
    expect(component.getRunnerNumber({ racingFormOutcome: { draw: '6' } } as any)).toBe('6');
  });

  describe('#isCashoutAvailable', () => {
    it('should return isCashoutAvailable', () => {
      const result = component.isCashoutAvailable(({
        cashoutAvail: 'Y',
        viewType: '',
      }) as any);

      expect(result).toEqual(true);
    });

    it('should return isCashoutAvailable when view type handicaps', () => {
      const result = component.isCashoutAvailable(({
        cashoutAvail: 'N',
        viewType: 'handicaps',
      }) as any);

      expect(result).toEqual(true);
    });

    it('should return isCashoutAvailable when no cashout', () => {
      const result = component.isCashoutAvailable(({
        cashoutAvail: 'N',
        viewType: '',
      }) as any);

      expect(result).toEqual(false);
    });
  });

  it('#formEdpUrl', () => {
    component.formEdpUrl(({ id: '12312312' } as any));

    expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith({ id: '12312312' });
  });

  it('#trackEvent', () => {
    spyOn(component, 'formEdpUrl').and.returnValue('/event/1212');
    component.trackEvent(({ id: '12312312' } as any));

    expect(nextRacesHomeService.trackNextRace).toHaveBeenCalled();
    expect(router.navigateByUrl).toHaveBeenCalledWith('/event/1212');
  });

  it('#isItvEvent', () => {
    component.isItvEvent(({ id: '12312312' } as any));

    expect(nextRacesHomeService.isItvEvent).toHaveBeenCalledWith({ id: '12312312' });
  });

  it('#getGoing', () => {
    component.getGoing('G');

    expect(nextRacesHomeService.getGoing).toHaveBeenCalledWith('G');
  });

  it('#getDistance', () => {
    component.getDistance('Distance');

    expect(nextRacesHomeService.getDistance).toHaveBeenCalledWith('Distance');
  });

  describe('#showEchWayTerms', () => {
    it('#showEchWayTerms if market has eachWayPlaces', () => {
      const result = component.showEchWayTerms(({
        eachWayPlaces: true,
        eachWayFactorDen: '1',
        eachWayFactorNum: '7'
      } as any));

      expect(result).toEqual(true);
    });

    it('#showEchWayTerms does not have eachWayPlaces', () => {
      const result = component.showEchWayTerms(({
        eachWayPlaces: false,
        eachWayFactorDen: '',
        eachWayFactorNum: ''
      } as any));

      expect(result).toEqual(false);
    });
  });

  it('#isGenericSilk', () => {
    component.isGenericSilk(({ name: 'event' } as any), ({ anme: 'outcome' } as any));

    expect(raceOutcomeData.isGenericSilk).toHaveBeenCalledWith({ name: 'event' }, { anme: 'outcome' });
  });

  it('#isGreyhoundSilk', () => {
    component.isGreyhoundSilk(({ name: 'event' } as any), ({ anme: 'outcome' } as any));

    expect(raceOutcomeData.isGreyhoundSilk).toHaveBeenCalledWith({ name: 'event' }, { anme: 'outcome' });
  });

  it('#isNumberNeeded', () => {
    component.isNumberNeeded(({ name: 'event' } as any), ({ anme: 'outcome' } as any));

    expect(raceOutcomeData.isNumberNeeded).toHaveBeenCalledWith({ name: 'event' }, { anme: 'outcome' });
  });

  it('#getSilkStyle', () => {
    component.getSilkStyle(([{ name: 'event' }] as any), ({ anme: 'outcome' } as any));

    expect(raceOutcomeData.getSilkStyle).toHaveBeenCalledWith([{ name: 'event' }], { anme: 'outcome' });
  });

  it('#isStreamLabelShown', () => {
    const result = component.isStreamLabelShown(({ name: 'event' } as any));

    expect(eventService.isLiveStreamAvailable).toHaveBeenCalledWith({ name: 'event' });
    expect(result).toEqual(true);
  });

  describe('#processOutcomes', () => {
    beforeEach(() => {
      component['applyFilters'] = jasmine.createSpy('applyFilters').and.returnValue([]);
      (component['_raceData'] as any) = [
        {
          id: 123,
          markets: [
            { id: '98765', outcomes: [] },
            { id: '12345', outcomes: [] }
          ]
        },
        {
          id: 1234
        }
      ];
    });
    it('should Sort and filter outcomes of market(s)', () => {
      component['processOutcomes']();

      expect(component['applyFilters']).toHaveBeenCalledWith({
        id: '12345',
        outcomes: []
      } as any);
      expect(component['raceMarkets']).toEqual(['98765', '12345']);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should Sort and filter outcomes of market(s) for updatedMarket', () => {
      component['processOutcomes'](({
        id: '12345',
        outcomes: []
      } as any));

      expect(component['applyFilters']).toHaveBeenCalledWith({
        id: '12345',
        outcomes: []
      } as any);
      expect(component['raceMarkets']).toEqual([]);
    });
    it('should not Sort and filter outcomes of market(s) for updatedMarket', () => {
      sortByOptionsService = {
        get: jasmine.createSpy('get').and.returnValue('Racecard'),
        set: jasmine.createSpy('set')
      };
      component = new RaceCardHomeComponent(raceOutcomeData, routingHelperService, nextRacesHomeService, localeService,
        sbFiltersService, filtersService, pubSubService, router, eventService, virtualSharedService, datePipe, changeDetectorRef, cmsService, sortByOptionsService, horseracing, racingGaService);
      component['applyFilters'] = jasmine.createSpy('applyFilters').and.returnValue([]);
      (component['_raceData'] as any) = [
        {
          id: 123,
          markets: [
            { id: '98765', outcomes: [] },
            { id: '12345', outcomes: [] }
          ]
        }
      ];
      component['processOutcomes'](({
        id: '12345',
        outcomes: []
      } as any));
      component

      expect(component['applyFilters']).not.toHaveBeenCalled();
      expect(component['raceMarkets']).toEqual([]);
    });
  });

  describe('#getRaceType', () => {
    it('should return race type with going', () => {
      localeService.getString.and.returnValue('Flat Turf');
      const result = component['getRaceType']({
        raceType: 'raceType',
        going: 'going',
        distance: 'distance'
      });

      expect(result).toEqual('Flat Turf - ');
    });

    it('should return race type without going', () => {
      localeService.getString.and.returnValue('Flat Turf');
      const result = component['getRaceType']({
        raceType: 'raceType',
        distance: 'distance'
      } as any);

      expect(result).toEqual('Flat Turf - ');
    });

    it('should return race type without going and distance', () => {
      localeService.getString.and.returnValue('Flat Turf');
      component.showTimer = true;
      const result = component['getRaceType']({
        raceType: 'raceType'
      } as any);

      expect(result).toEqual('Flat Turf - ');
    });

    it('should return race type without going and distance and without timer', () => {
      localeService.getString.and.returnValue('Flat Turf');
      component.showTimer = false;
      const result = component['getRaceType']({
        raceType: 'raceType'
      } as any);

      expect(result).toEqual('Flat Turf');
    });

    it('should return epty string when key not found', () => {
      localeService.getString.and.returnValue('KEY_NOT_FOUND');
      const result = component['getRaceType']({
        raceType: 'raceType',
        distance: 'distance'
      } as any);

      expect(result).toEqual('');
    });
  });

  describe('#applyFilters', () => {
    it('should filter outcomes of market', () => {
      component.hideNonRunners = false;
      component.hideFavourite = false;
      const result = component['applyFilters'](({
        outcomes: [],
        isLpAvailable: 'Yes',
      } as any));
      expect(sbFiltersService.orderOutcomeEntities).toHaveBeenCalledWith([], 'Yes', true, true, false, false, false);
      expect(result).toEqual(([{
        id: 'outcome1'
      },
      {
        id: 'outcome2'
      }] as any));
    });

    it('should filter outcomes of market and splice for max selections on card', () => {
      component.raceMaxSelections = 1;
      const result = component['applyFilters'](({
        outcomes: [],
        isLpAvailable: 'Yes',
      } as any));
      expect(sbFiltersService.orderOutcomeEntities).toHaveBeenCalledWith([], 'Yes', true, true, undefined, undefined, false);
      expect(result).toEqual(([{
        id: 'outcome1'
      }] as any));
    });
  });
  it('ngOnInit with raceData', fakeAsync(() => {
    spyOn(component, 'isAntepostMarket');
    component['syncToApplySorting'] = jasmine.createSpy();
    component.ngOnInit()
    expect(component.sortBy).toEqual('Price');
  }));
  it('ngOnInit with sortby info ', fakeAsync(() => {
    spyOn(component, 'isAntepostMarket');
    component['syncToApplySorting'] = jasmine.createSpy();
    component.isGreyhoundEdp = component['_raceData'][0].categoryCode !== 'HORSE_RACING';
    component.ngOnInit();
    expect(component.sortBy).toEqual('Price');
    expect(sortByOptionsService.get).toHaveBeenCalled();
    expect(cmsService.getSystemConfig).toHaveBeenCalled();
    expect(component.sortOptionsEnabled).toBeTruthy();
    expect(component.isAntepostMarket).toHaveBeenCalled();
    expect(component['syncToApplySorting']).toHaveBeenCalled();
  }));

  it('should set isGreyhound property', () => {
    component['_raceData'][0].categoryCode = 'GreyHoundEdp';
    component.ngOnInit();

    expect(component.isGreyhoundEdp).toEqual(true);
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
  it('isAntepostMarket', () => {
    component['_raceData'][0].markets[0].isAntepost = 'true';
    expect(component.isAntepostMarket()).toBeTruthy();

    component['_raceData'][0].markets[0].isAntepost = null;
    expect(component.isAntepostMarket()).toBeFalsy();
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
  it('applySortBy', () => {
    spyOn(component, 'setOutcomeFavourite');
    component.sortBy = null;
    component.expandedSummary = [];
    component['applySortBy']('PRICE');

    expect(component.sortBy).toBe('PRICE');

    const result1 = component['applyFilters'](({
      outcomes: [],
      isLpAvailable: 'Yes',
    } as any));
    expect(sbFiltersService.orderOutcomeEntities).toHaveBeenCalledWith([], 'Yes', true, true, undefined, undefined, false);
    expect(component.expandedSummary).toEqual([[false, false]]);
    expect(component.setOutcomeFavourite).toHaveBeenCalledWith(jasmine.any(Object));

    component['applySortBy']('RACECARD');
    expect(component.sortBy).toBe('RACECARD');
    component.hideNonRunners = false;
    component.hideFavourite = false;
    const result2 = component['applyFilters'](({
      outcomes: [],
      isLpAvailable: 'Yes',
    } as any));
    expect(sbFiltersService.orderOutcomeEntities).toHaveBeenCalledWith([], 'Yes', true, true, false, false, false);
  });

  it('applySortBy byPrice is false', () => {
    spyOn(component, 'setOutcomeFavourite');
    component['_raceData'][0].markets[0].outcomes[0] = {} as any;
    component['_raceData'][0].markets[0].isLpAvailable = true;
    component['_raceData'][0].markets[0].outcomes[0].runnerNumber = '5';
    component.sortBy = null;
    component.expandedSummary = [];
    component['applySortBy']('NotPrice');
    expect(component.setOutcomeFavourite).toHaveBeenCalledWith(jasmine.any(Object));
  });

  it('applySortBy byPrice is false and isOnload as true', () => {
    (component['_raceData'] as any) = [
      {
        id: 1234,
        markets: null
      }
    ];
    component.sortBy = null;
    component.expandedSummary = [];
    component['applySortBy']('NotPrice', true);
    expect(sbFiltersService.orderOutcomeEntities).not.toHaveBeenCalled();
  });

  describe('syncToApplySorting', () => {
    const unSortedMarkets = unSortedMarketsMock;
    const sortedByName = sortedByNameMock;

    beforeEach(() => {
      component['applySortBy'] = jasmine.createSpy();
      component.sortOptionsEnabled = true;
    });

    it('should apply sorting on init and subscription', () => {
      component.sortBy = 'price';
      component['syncToApplySorting']();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('RaceCardHomeComponent', pubSubService.API.SORT_BY_OPTION, jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith('raceCardHome', pubSubService.API.LIVE_MARKET_FOR_EDP, jasmine.any(Function));
      expect(component['applySortBy']).toHaveBeenCalledWith('price', true);
    });
    it('#Should call updateGATracking and applySortBy', () => {
      component.isGreyhoundEdp = true;
      component.sortBy = 'price';
      const market = { id: '1', outcomes: [{}, {}] };
      pubSubService.subscribe.and.callFake((name, channel, cb) => cb(market));
      component['syncToApplySorting']();
      expect(racingGaService['updateGATracking']).toHaveBeenCalled();
      expect(component.applySortBy).toHaveBeenCalledWith('price');
    });

    it('#Should call applySortBy when sortOptionsEnabled is false', () => {
      component.sortOptionsEnabled = false;
      component.sortBy = 'price';
      const market = { id: '1', outcomes: [{}, {}] };
      pubSubService.subscribe.and.callFake((name, channel, cb) => cb(market));
      component['syncToApplySorting']();
      expect(component['applySortBy']).toHaveBeenCalledWith('price');
    });


    it('should apply sorting by name', () => {
      sbFiltersService.orderOutcomesByName = jasmine.createSpy().and.returnValue(sortedByName);
      component.expandedSummary = [];
      component.sortBy = 'Name';
      component['_raceData'][0].markets = unSortedMarkets as any;
      component['syncToApplySorting']();
      expect(component['_raceData'][0].markets[0].outcomes as any).toEqual(sortedByName);
    });

    it('should apply sorting by price', () => {
      component.expandedSummary = [];
      component.sortBy = 'Price';
      component['_raceData'][0].markets = unSortedMarkets as any;
      component.applySortBy = jasmine.createSpy('applySortBy');
      component['syncToApplySorting']();
      expect(component.applySortBy).toHaveBeenCalledWith('Price', true);
    });

    it('should apply sorting by price with markets as null', () => {
      component.expandedSummary = [];
      component.sortBy = 'Name';
      component['_raceData'][0].markets = null;
      component.applySortBy = jasmine.createSpy('applySortBy');
      component['applySortByName'] = jasmine.createSpy('applySortByName');
      component['syncToApplySorting']();
      expect(component.applySortBy).toHaveBeenCalled();
      expect(component['applySortByName']).not.toHaveBeenCalled();
    });
  });
  describe('sortOptionsEnabledFn', () => {
    it('general flow', () => {
      component.sortOptionsEnabled = false;
      const market = component['_raceData'][0].markets[0];
      expect(component.sortOptionsEnabledFn(true, false, market)).toBeFalsy();

      component.sortOptionsEnabled = true;
      expect(component.sortOptionsEnabledFn(true)).toBeTruthy();
      expect(component.sortOptionsEnabledFn(true, true, null)).toBeTruthy();
      market.outcomes = [{ prices: [] }] as any;
      market.outcomes[0].prices = [];
      expect(component.sortOptionsEnabledFn(true, false, market)).toBeFalsy();

      expect(component.sortOptionsEnabledFn(false)).toBeFalsy();
      component.sortOptionsEnabled = false;
      expect(component.sortOptionsEnabledFn(true)).toBeFalsy();
    });

    it('should not show sort option when there are no prices and no market in params', () => {
      component['_raceData'][0] = [
        { markets: [{ id: '14213044' }] }, { name: 'More Markets' }
      ] as any;
      const market = undefined;

      expect(component.sortOptionsEnabledFn(false, market)).toBeFalsy();
    });

    it('should show sort option when there are prices and and no market in params', () => {
      component.sortOptionsEnabled = true;
      component['_raceData'][0] = [
        {
          markets: [{
            id: '14213044', outcomes: [
              { prices: [{ id: '1' }, { id: '2' }], isLpAvailable: true }
            ], isLpAvailable: true
          }]
        },
        { name: 'More Markets' }
      ] as any;
      const market = undefined;

      expect(component.sortOptionsEnabledFn(true, market)).toBeTruthy();
    });

    it('should be falsy if prices are not appropriate prices to sort', () => {
      component.sortOptionsEnabled = true;
      component['_raceData'][0] = [
        { outcomes: [{ prices: [] }, { prices: [] }] },
      ] as any;

      expect(component.sortOptionsEnabledFn(false)).toBeFalsy();
    });

    it('should be truthy if there are appropriate prices to sort', () => {
      component.sortOptionsEnabled = true;
      component['_raceData'][0] = [
        {
          isLpAvailable: true,
          outcomes: [{ prices: [{ priceDen: 12, priceNum: 4 }] }]
        },
      ] as any;

      expect(component.sortOptionsEnabledFn(true)).toBeTruthy();
    });

    it('should be truthy if there are appropriate prices to sort with some outcomes', () => {
      component.sortOptionsEnabled = true;
      const market = {
        id: '14213044',
        outcomes: [{ prices: [{ id: '1' }, { id: '2' }], isLpAvailable: true }],
        isLpAvailable: true
      } as any;
      expect(component.sortOptionsEnabledFn(true, true, market)).toBeTruthy();
    });

    it('should be falsy if there are appropriate prices to sort with no outcomes', () => {
      component.sortOptionsEnabled = true;
      const market = {
        id: '14213044',
        outcomes: [{ prices: [], isLpAvailable: true }],
        isLpAvailable: true
      } as any;
      expect(component.sortOptionsEnabledFn(true, true, market)).toBeFalsy();
    });
  });
  describe('#sponly', () => {
    it('should return false if both SP and LP are present', () => {
      const _raceData = {
        markets: [{
          priceTypeCodes: 'LP,GP,SP,'
        }]
      } as any;
      const response = component['isSp'](_raceData);
      expect(response).toBe(false);
    });
    it('should return true if only SP is present', () => {
      const _raceData = {
        markets: [{
          priceTypeCodes: 'GP,SP,'
        }]
      } as any;
      const response = component['isSp'](_raceData);
      expect(response).toBe(true);
    });
    it('should return false when markets is null', () => {
      const _raceData = {
        markets: null
      } as any;
      const response = component['isSp'](_raceData);
      expect(response).not.toBe(true);
    });
  });
});
