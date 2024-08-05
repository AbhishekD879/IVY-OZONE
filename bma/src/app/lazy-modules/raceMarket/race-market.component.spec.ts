import { fakeAsync, tick } from '@angular/core/testing';
import { RaceMarketComponent } from './race-market.component';
import { horseracingConfig } from '@core/services/racing/config/horseracing.config';
import { eventMock, mockMarket, mockEvent, greyhoundsGATrackingMock, horseRacingGATrackingMockwithshowless } from '@racing/components/racingEventComponent/racing-event.component.mock';

describe('RaceMarketComponent', () => {
  let component;
  let pubsub,
    raceOutcomeData,
    filterService,
    locale,
    sbFiltersService,
    racingService;
  let gtmService;
  let racingGaService;
  beforeEach(() => {

    pubsub = {
      unsubscribe: jasmine.createSpy(),
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => cb && cb('3')),
      publishSync: jasmine.createSpy(),
      API: {
        DELETE_EVENT_FROM_CACHE: 'DELETE_EVENT_FROM_CACHE',
        DELETE_MARKET_FROM_CACHE: 'DELETE_MARKET_FROM_CACHE',
        OUTCOME_UPDATED: 'OUTCOME_UPDATED',
      }
    };

    filterService = { orderBy: jasmine.createSpy('orderBy').and.returnValue([]) };
    locale = { getString: jasmine.createSpy('getString') };
    raceOutcomeData = {
      isGenericSilk: { bind: jasmine.createSpy('isGenericSilk') },
      isGreyhoundSilk: { bind: jasmine.createSpy('isGreyhoundSilk') },
      isNumberNeeded: { bind: jasmine.createSpy('isNumberNeeded') },
      getSilkStyle: { bind: jasmine.createSpy('getSilkStyle') }
    };
    sbFiltersService = {
      orderOutcomeEntities: jasmine.createSpy('orderOutcomeEntities')
    };

    racingService = {
      isRacingSpecials: jasmine.createSpy('isRacingSpecials'),
      setGroupedMarketHeader: jasmine.createSpy('setGroupedMarketHeader').and.returnValue(['1', '2'])
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    racingGaService = {
      toggleShowOptionsGATracking: jasmine.createSpy('toggleShowOptionsGATracking')
    }
    component = new RaceMarketComponent(
      raceOutcomeData,
      filterService,
      locale,
      pubsub,
      sbFiltersService,
      racingService,
      gtmService,
      racingGaService
    );
    component.eventEntity = mockEvent;
    component.expandedSummary = [[true]];
    component.sm = 'testName';
    component['config'] = horseracingConfig;
  });

  describe('@ngOnInit', () => {
    beforeEach(() => {
      component.marketEntity = {
        outcomes: [],
      } as any;
    });

    it('should create component', () => {
      expect(component).toBeDefined();
    });

    it('should trigger pubsub callback', fakeAsync(() => {
      const label = 'market label';
      component.eventEntity.sortedMarkets[0].label = label;
      component.sm = label;

      component.ngOnInit();

      expect(pubsub.subscribe).toHaveBeenCalledWith('RaceMarketComponent', 'OUTCOME_UPDATED', jasmine.any(Function));
      expect(pubsub.subscribe).toHaveBeenCalledWith(
        'RaceMarketComponent', ['DELETE_EVENT_FROM_CACHE', 'DELETE_MARKET_FROM_CACHE'], jasmine.any(Function)
      );
      expect(racingService.setGroupedMarketHeader).toHaveBeenCalledTimes(2);
    }));

    it(`should Not setGroupedMarketHeader if Not find sortedMarket`, fakeAsync(() => {
      component.isCoralDesktopRaceControls = true;
      component.ngOnInit();

      expect(racingService.setGroupedMarketHeader).not.toHaveBeenCalled();
    }));

    it('should call setOutcomeFavourite and push elem to expandedSummary array', () => {
      component.getRaceMarkets = jasmine.createSpy('getRaceMarkets').and.returnValue([1]);
      component.getUniqueOutcomes = jasmine.createSpy('getUniqueOutcomes').and.returnValue(['a']);
      component.setOutcomeFavourite = jasmine.createSpy('setOutcomeFavourite');
      spyOn(component.expandedSummary, 'push');

      component.ngOnInit();

      expect(component.marketEntity).toBeDefined();
      expect(component.setOutcomeFavourite).toHaveBeenCalledWith('a');
      expect(component.setOutcomeFavourite).toHaveBeenCalledTimes(1);
      expect(component.expandedSummary.push).toHaveBeenCalled();
    });
  });

  it('getSprites with silkName', () => {
    component.marketEntity = {
      outcomes: [{ racingFormOutcome: { silkName: 'silkName' } },
      { racingFormOutcome: { silkName: 'silkName2' } },
      { racingFormOutcome: { silkName: 'silkName2' } },
      { racingFormOutcome: { silkName: 'silkName1' } }
      ]
    } as any;
    component.getSprites();
  });

  it('getSprites without silkName', () => {
    component.marketEntity = {
      outcomes: []
    } as any;
    component.getSprites();
  });

  it('trackByIndex should return index', () => {
    expect(component.trackByIndex(1)).toBe(1);
  });

  it('trackById should return value.id', () => {
    const value = { id: 2 };
    expect(component.trackById(0, value)).toBe(2);
  });

  it('getFilteredName should call removeLineSymbol method', () => {
    filterService.removeLineSymbol = jasmine.createSpy('removeLineSymbol');
    component.getFilteredName('test');

    expect(filterService.removeLineSymbol).toHaveBeenCalledWith('test');
  });

  it('nameWithoutNonRunner should call removenNonRunnerFromHorseName method', () => {
    filterService.removenNonRunnerFromHorseName = jasmine.createSpy('removenNonRunnerFromHorseName');
    component.nameWithoutNonRunner('test');
    expect(filterService.removenNonRunnerFromHorseName).toHaveBeenCalledWith('test');
  });

  describe('@displayMarketPanel', () => {
    it('should return true', () => {
      locale.getString = jasmine.createSpy('getString').and.returnValue('test');
      const markerEntity = {
        label: 'test',
        isTopFinish: true,
        isToFinish: true,
        collapseMarket: false,
        insuranceMarkets: true,
        isOther: true,
        isWO: true
      } as any;
      component.sm = 'test';

      expect(component.displayMarketPanel(markerEntity)).toBe(true);
    });

    it('should return false', () => {
      locale.getString = jasmine.createSpy('getString').and.returnValue('no');
      const markerEntity = {
        label: 'none',
        isTopFinish: false,
        isToFinish: false,
        collapseMarket: true,
        insuranceMarkets: false,
        isOther: false,
        isWO: false
      } as any;
      component.sm = 'test';

      expect(component.displayMarketPanel(markerEntity)).toBe(false);
    });
  });

  describe('getDefaultSilk', () => {
    const event: any = {};
    it('When there is no racing form outcome and sportId is not equal to categoryId', () => {
      const outcome: any = {};
      event.sportId = '20';
      horseracingConfig.config.request.categoryId = '21';
      const expectedResult = component.getDefaultSilk(event, outcome);
      expect(expectedResult).toEqual(false);
    });

    it('When there is no racing form outcome and sportId is equal to categoryId', () => {
      const outcome: any = {};
      event.sportId = '21';
      horseracingConfig.config.request.categoryId = '21';
      const expectedResult = component.getDefaultSilk(event, outcome);
      expect(expectedResult).toEqual(true);
    });

    it('When there is racing form outcome and sportId is not equal to categoryId', () => {
      const outcome: any = { racingFormOutcome: { silkName: 'silkName' } };
      event.sportId = '20';
      horseracingConfig.config.request.categoryId = '21';
      const expectedResult = component.getDefaultSilk(event, outcome);
      expect(expectedResult).toEqual(false);
    });

    it('When there is racing form outcome and sportId is equal to categoryId', () => {
      const outcome: any = { racingFormOutcome: { silkName: 'silkName' } };
      event.sportId = '21';
      horseracingConfig.config.request.categoryId = '21';
      const expectedResult = component.getDefaultSilk(event, outcome);
      expect(expectedResult).toEqual(false);
    });

  });

  describe('@ngOnChanges', () => {
    beforeEach(() => {
      spyOn(component, 'getRaceMarkets').and.returnValue([{}]);
      spyOn(component, 'getUniqueOutcomes').and.returnValue([]);
    });

    it('should reorder outcomes if isSortByChanged is triggered', fakeAsync(() => {
      const changes = {
        sortBy: {
          currentValue: 'Price',
          previousValue: 'Rececard'
        }
      } as any;
      component.ngOnChanges(changes);
      tick();
      expect(component.getRaceMarkets).toHaveBeenCalled();
      expect(component.getUniqueOutcomes).toHaveBeenCalled();
    }));

    it('should reorder outcomes if eventEntity is triggered', fakeAsync(() => {
      const changes = {
        eventEntity: {}
      } as any;
      component.ngOnChanges(changes);
      tick();
      expect(component.getRaceMarkets).toHaveBeenCalled();
      expect(component.getUniqueOutcomes).toHaveBeenCalled();
    }));

    it('should reorder outcomes if sm is triggered', fakeAsync(() => {
      const changes = {
        sm: {}
      } as any;
      component.ngOnChanges(changes);
      tick();
      expect(component.getRaceMarkets).toHaveBeenCalled();
      expect(component.getUniqueOutcomes).toHaveBeenCalled();
    }));

    it('should NOT reorder outcomes if isSortByChanged is triggered with same value', fakeAsync(() => {
      const changes = {
        sortBy: {
          currentValue: 'Price',
          previousValue: 'Price'
        }
      } as any;
      component.ngOnChanges(changes);
      tick();
      expect(component.getRaceMarkets).not.toHaveBeenCalled();
      expect(component.getUniqueOutcomes).not.toHaveBeenCalled();
    }));

    it('should NOT reorder outcomes if isSortByChanged is NOT triggered', fakeAsync(() => {
      const changes = {} as any;
      component.ngOnChanges(changes);
      tick();
      expect(component.getRaceMarkets).not.toHaveBeenCalled();
      expect(component.getUniqueOutcomes).not.toHaveBeenCalled();
    }));
  });

  describe('@sortOutcomes', () => {
    it('should sort outcomes by Price', () => {
      component.sortBy = 'Price';
      component['sortOutcomes']([], true);
      expect(sbFiltersService.orderOutcomeEntities).toHaveBeenCalledWith([], true, true, false, false, false, false);
    });

    it('should sort outcomes by NonRunner: isLpAvailable=false', () => {
      component.sortBy = 'Price';
      component['sortOutcomes']([], false);
      expect(sbFiltersService.orderOutcomeEntities).toHaveBeenCalledWith([], false, true, true, false, false, false);
    });

    it('should sort outcomes by Number: isLpAvailable=false', () => {
      component.sortBy = 'Racecard';
      component['sortOutcomes']([], false);
      expect(sbFiltersService.orderOutcomeEntities).toHaveBeenCalledWith([], false, true, true, false, false, false);
    });

    it('should sort outcomes by Number: sortBy === "Racecard"', () => {
      component.sortBy = 'Racecard';
      component['sortOutcomes']([], true);
      expect(sbFiltersService.orderOutcomeEntities).toHaveBeenCalledWith([], false, true, true, false, false, false);
    });
  });

  it('isGroupedRaceMarket should check is it grouped market or no', () => {
    const market = { name: 'Place Insurance 2' } as any;
    expect(component.isGroupedRaceMarket(market)).toBeTruthy();
  });

  describe('@getHeader', () => {
    it('should return null when markets name and sm value are equal', () => {
      const actualResult = component.getHeader(mockMarket, mockEvent);

      expect(actualResult).toBe(null);
    });

    it('should get and sort related grouped markets header', () => {
      mockMarket.isTopFinish = true;
      const actualResult = component.getHeader(mockMarket, mockEvent);

      expect(actualResult).toEqual([]);
    });

    it('should return null when groupedMarket is undefined', () => {
      mockMarket.isTopFinish = true;
      const mockEventEmpty = {};
      const actualResult = component.getHeader(mockMarket, mockEventEmpty);

      expect(actualResult).toBe(null);
    });
  });

  describe('@getOutcomeForRaceMarket', () => {
    const outcomes = [{
      id: 1,
      name: 'test1'
    },
    {
      id: 2,
      name: 'test2'
    }];

    it('should return outcome for race market', () => {
      expect(component.getOutcomeForRaceMarket(outcomes, 'test2')).toEqual({ id: 2, name: 'test2' });
    });

    it('should return undefined if no outcome found', () => {
      expect(component.getOutcomeForRaceMarket(outcomes, 'test3')).toEqual(undefined);
    });
  });

  describe('@definePriceType', () => {
    it('should return SP', () => {
      const marketEntity = {
        isSpAvailable: true,
        isLpAvailable: false
      };

      expect(component.definePriceType(marketEntity, {}, true)).toBe('SP');
    });

    it('should return LP', () => {
      const marketEntity = {
        isSpAvailable: false,
        isLpAvailable: true
      };

      expect(component.definePriceType(marketEntity, {}, false)).toBe('LP');
    });

    it('should return SP both true', () => {
      const marketEntity = {
        isSpAvailable: true,
        isLpAvailable: true
      };

      const outcomeEntity = {
        prices: [{}]
      };

      expect(component.definePriceType(marketEntity, outcomeEntity, true)).toBe('SP');
    });

    it('should return LP both false', () => {
      const marketEntity = {
        isSpAvailable: false,
        isLpAvailable: false
      };

      expect(component.definePriceType(marketEntity, {}, false)).toBe('LP');
    });
  });

  describe('@setOutcomeFavourite', () => {
    it('should set isFavourite to true', () => {
      const outomeEntity = {
        isFavourite: null,
        outcomeMeaningMinorCode: 1,
        name: 'unnamed favourite'
      };

      component.setOutcomeFavourite(outomeEntity);

      expect(outomeEntity.isFavourite).toBe(true);
    });

    it('should set isFavourite to false', () => {
      const outomeEntity = {
        isFavourite: null,
        outcomeMeaningMinorCode: 0,
        name: 'test'
      };

      component.setOutcomeFavourite(outomeEntity);

      expect(outomeEntity.isFavourite).toBe(false);
    });
  });

  describe('@isHistoricPrices', () => {
    it('should return true', () => {
      const outomeEntity = {
        name: 'test',
        isFavourite: false
      };
      const marketEntity = {
        outcomes: true,
        name: 'test'
      };
      component.getOutcomeForRaceMarket = jasmine.createSpy('getOutcomeForRaceMarket').and.returnValue({
        isFavourite: false
      });
      component.definePriceType = jasmine.createSpy('definePriceType').and.returnValue('test');

      expect(component.isHistoricPrices(marketEntity, outomeEntity)).toBe(true);
    });

    it('should return false', () => {
      const outomeEntity = {
        name: 'test',
        isFavourite: false
      };
      const marketEntity = {
        outcomes: true,
        name: 'test'
      };
      component.getOutcomeForRaceMarket = jasmine.createSpy('getOutcomeForRaceMarket').and.returnValue({
        isFavourite: true
      });
      component.definePriceType = jasmine.createSpy('definePriceType').and.returnValue('SP');

      expect(component.isHistoricPrices(marketEntity, outomeEntity)).toBe(false);
    });
  });

  describe('@defPriceType', () => {
    it('should return SP', () => {
      const marketEntity = {
        isSpAvailable: true,
        isLpAvailable: false
      };
      const outcomeEntity = {
        name: 'test'
      };
      component.getOutcomeForRaceMarket = jasmine.createSpy('getOutcomeForRaceMarket').and.returnValue({});

      expect(component.defPriceType(marketEntity, outcomeEntity)).toBe('SP');
    });

    it('should return LP', () => {
      const marketEntity = {
        isSpAvailable: false,
        isLpAvailable: true
      };
      const outcomeEntity = {
        name: 'test'
      };
      component.getOutcomeForRaceMarket = jasmine.createSpy('getOutcomeForRaceMarket').and.returnValue({});

      expect(component.defPriceType(marketEntity, outcomeEntity)).toBe('LP');
    });
  });

  describe('@isNumber', () => {
    it('should return true', () => {
      const outcomeEntity = {
        name: 'test',
        isFavourite: false
      };
      component.isNumberNeeded = jasmine.createSpy('isNumberNeeded').and.returnValue(true);

      expect(component.isNumber(outcomeEntity)).toBe(true);
    });

    it('should return false', () => {
      const outcomeEntity = {
        name: 'test',
        isFavourite: true
      };
      component.isNumberNeeded = jasmine.createSpy('isNumberNeeded').and.returnValue(false);

      expect(component.isNumber(outcomeEntity)).toBe(false);
    });
  });

  describe('onInit hook should', () => {

    it('get race markets on ini and subscribe on further updates', () => {
      spyOn(component, 'getRaceMarkets').and.returnValue([]);
      spyOn(component, 'getUniqueOutcomes');
      component.marketEntity = {
        outcomes: []
      } as any;
      component.ngOnInit();

      expect(component.getRaceMarkets).toHaveBeenCalledTimes(3);
      expect(pubsub.subscribe).toHaveBeenCalled();
      expect(component.getUniqueOutcomes).not.toHaveBeenCalled();
      expect(racingService.isRacingSpecials).toHaveBeenCalledWith(component.eventEntity);
    });

    it('get unique outcomes from race markets on updates', fakeAsync(() => {
      spyOn(component, 'getRaceMarkets').and.returnValue([{}]);
      spyOn(component, 'getUniqueOutcomes').and.returnValue([]);
      component.marketEntity = {
        outcomes: []
      } as any;
      component.ngOnInit();
      tick(1500);

      expect(component.getRaceMarkets).toHaveBeenCalledTimes(4);
      expect(component.getUniqueOutcomes).toHaveBeenCalledTimes(3);
    }));
  });

  describe('getUniqueOutcomes', () => {
    it('orderOutcomeEntities', () => {
      component.groupedMarket = [{
        outcomes: [{ name: '1', runnerNumber: 1, prices: [{}] }]
      }] as any;
      component.getUniqueOutcomes({} as any);
      expect(sbFiltersService.orderOutcomeEntities).toHaveBeenCalledTimes(1);
    });
  });

  it('getRaceMarkets should set array of groupedMarket and order it by component.raceMarketOrder', () => {
    const marketsMock = [
      {
        ...mockMarket,
        customOrder: 2
      },
      {
        ...mockMarket,
        customOrder: 1
      }
    ];
    component.getRaceMarkets(marketsMock);
    expect(component.groupedMarket).toBeDefined();
    expect(filterService.orderBy).toHaveBeenCalled();
  });
  describe('ngOnDestroy', () => {
    it('on call', () => {
      component.ngOnDestroy();
      expect(pubsub.unsubscribe).toHaveBeenCalled();
    });
  });
  it('@onExpandSection should set expand status', () => {
    const expectedResult = [[false], [true, true, true]];
    component.eventEntity = Object.assign({}, eventMock);
    component.onExpandSection(expectedResult, 0);

    expect(expectedResult).toEqual([[true], [true, true, true]]);
    expect(component.isInfoHidden.info).toEqual(true);
  });
  it('#Should call onExpandSection GA Tracking when true and isGreyhoundEdp is true', () => {
    const expectedResult = [[false], [true, true, true]];
    component.eventEntity = Object.assign({}, eventMock);
    component.isGreyhoundEdp = true;
    component.onExpandSection(expectedResult, 1, 0);
    const expectedParams = ['trackEvent', greyhoundsGATrackingMock];
    expect(component.isGreyhoundEdp).toBeTruthy()
    expect(gtmService.push).toHaveBeenCalledWith(...expectedParams);
  });

  it('#Should call onExpandSection GA Tracking when true and isGreyhoundEdp is false', () => {
    const expectedResult = [[true]];
    component.isGreyhoundEdp = false;
    component.eventEntity = Object.assign({}, eventMock);
    component.onExpandSection(expectedResult, 0);
    const expectedParams = ['trackEvent', horseRacingGATrackingMockwithshowless];
    expect(component.isGreyhoundEdp).toBeFalsy();
    expect(gtmService.push).toHaveBeenCalledWith(...expectedParams);
  });
  it('toggleShowOptions', () => {
    const expandedSummary = [[true, false], [false, true]];
    component.toggleShowOptions(expandedSummary, true);
    expect(expandedSummary).toEqual([[true, true], [false, true]]);
  });

  describe('#toggleShowOptions', () => {
    it('should be no change in expandedSummary if  it is empty array', () => {
      const expandedSummary = [];
      component.toggleShowOptions(expandedSummary, true);
      expect(expandedSummary).toEqual([]);
    });
    it('should be no change in expandedSummary if  it is null', () => {
      const expandedSummary = null;
      component.toggleShowOptions(expandedSummary, true);
      expect(expandedSummary).toEqual(null);
    });
    it('should be no change in expandedSummary if  it is null', () => {
      const expandedSummary = [[true, false]];
      component.toggleShowOptions(expandedSummary, false);
      expect(expandedSummary).toEqual([[false, false]]);
    });
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
