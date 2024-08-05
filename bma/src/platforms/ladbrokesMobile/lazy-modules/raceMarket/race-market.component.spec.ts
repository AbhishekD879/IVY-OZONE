import { LadbrokesRaceMarketComponent as RaceMarketComponent } from './race-market.component';
import { eventMock } from '@racing/components/racingEventComponent/racing-event.component.mock';

describe('RaceMarketComponent', () => {
  let component;
  let pubsub,
    raceOutcomeData,
    filterService,
    locale,
    sbFiltersService,
    racingService,
    gtmService;
  let mockMarket;
  let mockEvent;
  let racingGaService;

  beforeEach(() => {
    mockMarket = {
      cashoutAvail: '',
      correctPriceTypeCode: '',
      dispSortName: '',
      eachWayFactorNum: '',
      eachWayFactorDen: '',
      eachWayPlaces: '',
      id: '',
      isGpAvailable: false,
      isLpAvailable: false,
      isMarketBetInRun: false,
      isSpAvailable: false,
      liveServChannels: '',
      isEachWayAvailable: false,
      liveServChildrenChannels: '',
      marketsNames: '',
      marketStatusCode: '',
      name: 'testName',
      nextScore: 1,
      outcomes: [],
      periods: [],
      priceTypeCodes: '',
      terms: '',
      templateMarketId: 1,
      templateMarketName: '',
      viewType: '',
      label: '',
      isTopFinish: false,
      isToFinish: false,
      insuranceMarkets: false,
      isOther: false,
      isWO: false,
      header: ['1', '2', '3'],
      markets: [
        {
          id: '1'
        },
        {
          id: '2'
        },
        {
          id: '3'
        }
      ]
    };
    mockEvent = {
      cashoutAvail: '',
      categoryCode: '',
      categoryId: '',
      categoryName: '',
      comments: {
        teams: {},
      },
      displayOrder: 1,
      drilldownTagNames: '',
      eventIsLive: false,
      eventSortCode: '',
      eventStatusCode: '',
      groupedLimit: 1,
      id: 1,
      isStarted: false,
      isUS: false,
      liveServChannels: '',
      liveServChildrenChannels: '',
      liveStreamAvailable: false,
      markets: [mockMarket],
      marketsCount: 1,
      name: '',
      originalName: '',
      responseCreationTime: '',
      racingFormEvent: {
        class: ''
      },
      startTime: '',
      streamProviders: {
        ATR: false,
        IMG: false,
        Perform: false,
        RPGTV: false,
        RacingUK: false,
        iGameMedia: false
      },
      svgId: '',
      typeId: '',
      typeName: '',
      outcomeId: 1,
      sortedMarkets: [mockMarket]
    };
    pubsub = {
      unsubscribe: jasmine.createSpy(),
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => cb && cb({})),
      publishSync: jasmine.createSpy(),
      API: {
        OUTCOME_UPDATED: 'OUTCOME_UPDATED',
      }
    };

    gtmService = {
      push: jasmine.createSpy('gt,Service.push')
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
  });

  describe('isShowMore', () => {
    it('returns true', () => {
      let result;
      const outcomeMock = {
        timeFormData: {},
        racingFormOutcome: {}
      } as any;

      result = component.isShowMore(outcomeMock);
      expect(result).toBeTruthy();

      component.isGreyhoundEdp = true;
      outcomeMock.racingFormOutcome = { overview: true } as any;
      result = component.isShowMore(outcomeMock);
      expect(result).toBeTruthy();
    });

    it('returns false', () => {
      let result;
      let outcomeEntity = {} as any;

      result = component.isShowMore(outcomeEntity);
      expect(result).toBeFalsy();

      outcomeEntity = { isFavourite: true };
      result = component.isShowMore(outcomeEntity);
      expect(result).toBeFalsy();
    });
  });

  it('@toggleShowOptions should change array values', () => {
    const expandedSummary = [[true, false], [false, true]];
    component.toggleShowOptions(expandedSummary, true);
    expect(expandedSummary).toEqual([[true, true], [false, true]]);
  });

  it('@onExpand should set expand status', () => {
    const testArray = [[true, true, true], [false]];
    component.eventEntity = Object.assign({}, eventMock);
    component.onExpand(testArray, 1);
    expect(component.isInfoHidden.info).toEqual(true);
  });

  it('#Should call onExpand GA Tracking when true', () => {
    const expectedResult = [[false], [true, true, true]];
    component.eventEntity = Object.assign({}, eventMock);
    component.onExpand(expectedResult, 0);
    component.isGreyhoundEdp = true;
    const expectedParams = ['trackEvent', {
      event: 'trackEvent',
      eventAction: 'race card',
      eventCategory: "horse racing",
      eventLabel: 'show more',
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
