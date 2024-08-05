import {
  CardViewFooterComponent
} from '@app/bigCompetitions/components/cardViewWidget/cardViewFooter/card-view-footer.component';
import { IBigCompetitionSportEvent } from '@app/bigCompetitions/models/big-competitions.model';
import { IMarket } from '@core/models/market.model';
import { of } from 'rxjs';

describe('CardViewFooterComponent', () => {

  let component;

  let marketTypeService;
  let sportEventHelperService;
  let filtersService;
  let sportsConfigService;

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
    name: '',
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
    insuranceMarkets: false,
    isOther: true,
    isWO: false
  } as IMarket;

  const event = {
    cashoutAvail: '',
    categoryCode: '',
    categoryId: '',
    categoryName: 'Football',
    displayOrder: 0,
    drilldownTagNames: '',
    eventIsLive: true,
    eventSortCode: '',
    eventStatusCode: '',
    id: 10,
    isUS: true,
    liveServChannels: '',
    liveServChildrenChannels: '',
    liveStreamAvailable: true,
    typeId: '',
    typeName: '',
    name: '',
    originalName: '',
    responseCreationTime: '',
    markets: [market, { ...market }],
    racingFormEvent: {
      class: ''
    },
    startTime: ''
  } as IBigCompetitionSportEvent;

  const expectedSportConfig = {
    path: 'football',
    id: '16',
    specialsTypeIds: [2297, 2562],
    dispSortName: 'MR',
    primaryMarkets: '|Match Betting|',
    viewByFilters: ['byLeaguesCompetitions', 'byTime'],
    oddsCardHeaderType: 'homeDrawAwayType',
    isMultiTemplateSport: false
  };

  const groupOutcome = {};

  beforeEach(() => {
    marketTypeService = {
      isMatchResultType: jasmine.createSpy().and.returnValue(false),
      isHomeDrawAwayType: jasmine.createSpy().and.returnValue(false)
    };
    sportEventHelperService = {
      isHomeDrawAwayType: jasmine.createSpy().and.returnValue(true)
    };
    filtersService = {
      groupBy: jasmine.createSpy().and.returnValue([[groupOutcome]])
    };
    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of(expectedSportConfig))
    };

    component = new CardViewFooterComponent(marketTypeService, sportEventHelperService, filtersService, sportsConfigService);
    component.event = event;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit when market is set', () => {
    component.market = event.markets[1];
    const outcomes = [{
      id: 2,
      icon: false,
      fakeOutcome: false,
      name: 'outcome'
    }];
    component.getGroupedOutcomes = jasmine.createSpy().and.returnValue(outcomes);
    component.ngOnInit();

    expect(sportsConfigService.getSport).toHaveBeenCalledWith('football');
    expect(component.headerHas2Columns).toBeTruthy();
    expect(component.market).toBe(event.markets[0]);
    expect(component.getGroupedOutcomes).toHaveBeenCalled();
    expect(component.groupedOutcomes).toEqual(outcomes);
    expect(marketTypeService.isMatchResultType).toHaveBeenCalledWith(component.market);
    expect(marketTypeService.isHomeDrawAwayType).toHaveBeenCalledWith(component.market);
  });

  it('#ngOnInit when market is not set', () => {
    component.market = null;
    component.ngOnInit();
    expect(component.headerHas2Columns).toBeFalsy();
    expect(component.market).toBe(event.markets[0]);
    expect(component.groupedOutcomes.length).toBe(1);
    expect(marketTypeService.isMatchResultType).not.toHaveBeenCalled();
    expect(marketTypeService.isHomeDrawAwayType).not.toHaveBeenCalled();
  });

  it('#ngOnInit when event.categoryName is not set', () => {
    component.event = {
      categoryName: 'categoryName',
      markets: []
    };

    component.ngOnInit();
    expect(component.market).toBe(undefined);
    expect(component.groupedOutcomes).toEqual([]);
  });

  it('#ngOnChanges when outcomesLength is in changes', () => {
    component.market = null;
    component.getGroupedOutcomes = jasmine.createSpy();
    component.ngOnChanges({
      'outcomesLength': {
          previousValue: null,
          currentValue: {},
          firstChange: true,
          isFirstChange: () => true
      }
    });
    expect(component.market).toBe(event.markets[0]);
    expect(component.getGroupedOutcomes).toHaveBeenCalled();
  });

  it('#ngOnChanges when there is no outcomesLength in changes', () => {
    component.market = null;
    component.getGroupedOutcomes = jasmine.createSpy();
    component.ngOnChanges({});
    expect(component.market).toBe(null);
    expect(component.groupedOutcomes).toBe(undefined);
    expect(component.getGroupedOutcomes).not.toHaveBeenCalled();
  });

  it('#ngOnChanges when there is no outcomesLength in changes', () => {
    component.market = null;
    component.event = {
      markets: []
    };
    component.getGroupedOutcomes = jasmine.createSpy('getGroupedOutcomes');

    component.ngOnChanges({ outcomesLength: {} });
    expect(component.market).toBe(undefined);
    expect(component.groupedOutcomes).toEqual([]);
    expect(component.getGroupedOutcomes).not.toHaveBeenCalled();
  });

  it('should return correct index', () => {
    const index = 5;
    expect(component.trackByIndex(index)).toBe(index);
  });

  it('should return correct group outcomes', () => {
    component.market = event.markets[0];
    component.getGroupedOutcomes();
    expect(component.getGroupedOutcomes()[0]).toBe(groupOutcome);
    expect(filtersService.groupBy).toHaveBeenCalledWith(component.market.outcomes, 'correctedOutcomeMeaningMinorCode');
  });

  it('ngOnDestroy: should unsubscribe from sports config', function () {
    component['sportsConfigSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component.ngOnDestroy();

    expect(component['sportsConfigSubscription'].unsubscribe).toHaveBeenCalled();
  });

  it('ngOnDestroy: should not unsubscribe from sports config', function () {
    component['sportsConfigSubscription'] = undefined;
    component.ngOnDestroy();

    expect(component['sportsConfigSubscription']).not.toBeDefined();
  });

  describe('isHomeDrawAwayType returns true', () => {
    beforeEach(() => {
      marketTypeService.isHomeDrawAwayType = jasmine.createSpy().and.returnValue(true);

      component = new CardViewFooterComponent(marketTypeService, sportEventHelperService, filtersService, sportsConfigService);
      component.event = event;
    });

    it('odd button wrapper should be shown when headerHas2Columns is false and index is 1',
      () => {
      component.headerHas2Columns = false;
      component.sportConfig = expectedSportConfig;
      expect(component.shouldShowOddButton(1)).toBeTruthy();
      expect(sportEventHelperService.isHomeDrawAwayType).toHaveBeenCalledWith(component.event, component.sportConfig);
    });

    it('odd button wrapper should not be shown when headerHas2Columns is true and index is 1',
      () => {
        component.headerHas2Columns = true;
        component.sportConfig = expectedSportConfig;
        expect(component.shouldShowOddButton(1)).toBeFalsy();
        expect(sportEventHelperService.isHomeDrawAwayType).toHaveBeenCalledWith(component.event, component.sportConfig);
    });

    it('odd button wrapper should be shown when headerHas2Columns is false and index is not 1',
      () => {
        component.headerHas2Columns = false;
        component.sportConfig = expectedSportConfig;
        expect(component.shouldShowOddButton(0)).toBeTruthy();
        expect(sportEventHelperService.isHomeDrawAwayType).toHaveBeenCalledWith(component.event, component.sportConfig);
    });

    it('odd button wrapper should be shown when headerHas2Columns is true and index is not 1',
      () => {
        component.headerHas2Columns = true;
        component.sportConfig = expectedSportConfig;
        expect(component.shouldShowOddButton(0)).toBeTruthy();
        expect(sportEventHelperService.isHomeDrawAwayType).toHaveBeenCalledWith(component.event, component.sportConfig);
      });

    it('odd button wrapper should be shown when headerHas3Columns is false and index is 1',
      () => {
        component.headerHas3Columns = false;
        component.sportConfig = expectedSportConfig;
        expect(component.shouldShowOddButton(1)).toBeTruthy();
        expect(sportEventHelperService.isHomeDrawAwayType).toHaveBeenCalledWith(component.event, component.sportConfig);
      });

    it('odd button wrapper should be shown when headerHas3Columns is false and index is not 1',
      () => {
        component.headerHas3Columns = false;
        component.sportConfig = expectedSportConfig;
        expect(component.shouldShowOddButton(0)).toBeTruthy();
        expect(sportEventHelperService.isHomeDrawAwayType).toHaveBeenCalledWith(component.event, component.sportConfig);
      });

    it('odd button wrapper should be shown when headerHas2Columns is true and index is not 1',
      () => {
        component.headerHas3Columns = true;
        component.sportConfig = expectedSportConfig;
        expect(component.shouldShowOddButton(0)).toBeTruthy();
        expect(sportEventHelperService.isHomeDrawAwayType).toHaveBeenCalledWith(component.event, component.sportConfig);
      });

    it('odd button wrapper should be shown when headerHas2Columns is false and index is not 1',
    () => {
      component['sportEventHelperService'].isHomeDrawAwayType = jasmine.createSpy('isHomeDrawAwayType')
        .and.returnValue(false);
      component.headerHas2Columns = false;
      component.sportConfig = expectedSportConfig;
      expect(component.shouldShowOddButton(0)).toBeTruthy();
      expect(sportEventHelperService.isHomeDrawAwayType).toHaveBeenCalledWith(component.event, component.sportConfig);
    });
  });

  describe('isHomeDrawAwayType returns false', () => {
    beforeEach(() => {
      marketTypeService.isHomeDrawAwayType = jasmine.createSpy().and.returnValue(false);

      component = new CardViewFooterComponent(marketTypeService, sportEventHelperService, filtersService, sportsConfigService);
      component.event = event;
    });

    it('odd button wrapper should be shown when headerHas2Columns is false and index is 1',
      () => {
        component.headerHas2Columns = false;
        component.sportConfig = expectedSportConfig;
        expect(component.shouldShowOddButton(1)).toBeTruthy();
        expect(sportEventHelperService.isHomeDrawAwayType).toHaveBeenCalledWith(component.event, component.sportConfig);
      });

    it('odd button wrapper should not be shown when headerHas2Columns is true and index is 1',
      () => {
        component.headerHas2Columns = true;
        component.sportConfig = expectedSportConfig;
        expect(component.shouldShowOddButton(1)).toBeFalsy();
        expect(sportEventHelperService.isHomeDrawAwayType).toHaveBeenCalledWith(component.event, component.sportConfig);
      });

    it('odd button wrapper should be shown when headerHas2Columns is false and index is not 1',
      () => {
        component.headerHas2Columns = false;
        component.sportConfig = expectedSportConfig;
        expect(component.shouldShowOddButton(0)).toBeTruthy();
        expect(sportEventHelperService.isHomeDrawAwayType).toHaveBeenCalledWith(component.event, component.sportConfig);
      });

    it('odd button wrapper should be shown when headerHas2Columns is true and index is not 1',
      () => {
        component.headerHas2Columns = true;
        component.sportConfig = expectedSportConfig;
        expect(component.shouldShowOddButton(0)).toBeTruthy();
        expect(sportEventHelperService.isHomeDrawAwayType).toHaveBeenCalledWith(component.event, component.sportConfig);
      });

    it('odd button wrapper should be shown when headerHas3Columns is false and index is 1',
      () => {
        component.headerHas3Columns = false;
        component.sportConfig = expectedSportConfig;
        expect(component.shouldShowOddButton(1)).toBeTruthy();
        expect(sportEventHelperService.isHomeDrawAwayType).toHaveBeenCalledWith(component.event, component.sportConfig);
      });

    it('odd button wrapper should be shown when headerHas3Columns is false and index is not 1',
      () => {
        component.headerHas3Columns = false;
        component.sportConfig = expectedSportConfig;
        expect(component.shouldShowOddButton(0)).toBeTruthy();
        expect(sportEventHelperService.isHomeDrawAwayType).toHaveBeenCalledWith(component.event, component.sportConfig);
      });

    it('odd button wrapper should be shown when headerHas3Columns is true and index is not 1',
      () => {
        component.headerHas3Columns = true;
        component.sportConfig = expectedSportConfig;
        expect(component.shouldShowOddButton(0)).toBeTruthy();
        expect(sportEventHelperService.isHomeDrawAwayType).toHaveBeenCalledWith(component.event, component.sportConfig);
      });
  });
});
