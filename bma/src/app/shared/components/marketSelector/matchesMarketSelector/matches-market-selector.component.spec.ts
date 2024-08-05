import { MatchesMarketSelectorComponent } from './matches-market-selector.component';
import { ICouponMarketSelector } from '../market-selector.model';
import { IMarket } from '@core/models/market.model';
import { of } from 'rxjs';

describe('MatchesMarketSelectorComponent', () => {
  let component: MatchesMarketSelectorComponent;
  let filtersService;
  let marketSelectorConfigService;
  let pubSubService;
  let marketSelectorTrackingService;
  let marketSelectorStorageService;
  let activatedRoute;

  const typeSegment = [{
    typeId: 971,
    events: [{
      id: 5112681,
      markets: [{
        templateMarketName: 'Match Result',
        outcomes: []
      }, {
        templateMarketName: 'To Qualify',
        outcomes: []
      }]
    }, {
      id: 3567838,
      markets: [{
        templateMarketName: 'Match Result',
        outcomes: []
      }]
    }]
  }] as any;

  const defaultSelectorData = [{
    SPORT_ID: 16,
    DEFAULT_SELECTED_OPTION: 'Match Result',
    MARKETS_NAME_ORDER: [
      'Match Result',
      'To Qualify',
      'Total Goals Over/Under 2.5',
      'Both Teams to Score',
      'To Win and Both Teams to Score',
      'Draw No Bet',
      'First-Half Result'
    ],
    MARKETS_NAMES: {
      'Match Result': 'Match Result',
      'Both Teams to Score': 'Both Teams to Score',
      'Total Goals Over/Under 2.5': 'Total Goals Over/Under 2.5',
      'Draw No Bet': 'Draw No Bet',
      'To Win and Both Teams to Score': 'To Win & Both Teams to Score',
      'First-Half Result': '1st Half Result',
      'To Qualify': 'To Qualify'
    }
  }];

  beforeEach(() => {
    filtersService = {
      getTeamName: jasmine.createSpy().and.returnValue('dynamo')
    };
    marketSelectorConfigService = {
      footballCoupons: defaultSelectorData,
      footballInplay: defaultSelectorData,
      modifyTemplateName: jasmine.createSpy(),
      getMarketOptions: jasmine.createSpy()
    };
    activatedRoute = {
      snapshot: {
          paramMap: {
              get: jasmine.createSpy('paramMap.get').and.returnValue('golf')
          },
          params: of({
            sport: 'golf',
            id: '18',
            display: 'upcoming'
        })
      },
      params: of({
          sport: 'golf',
          id: '18',
          display: 'upcoming'
      })
  };
    pubSubService = {
      API: {
        DELETE_EVENT_FROM_CACHE: 'DELETE_EVENT_FROM_CACHE',
        DELETE_MARKET_FROM_CACHE: 'DELETE_MARKET_FROM_CACHE'
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((domain, channel, fn) => fn && fn()),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    marketSelectorTrackingService = {
      pushToGTM: jasmine.createSpy('pushToGTM'),
      sendGTMDataOnMarketSelctorChange: jasmine.createSpy('sendGTMDataOnMarketSelctorChange')
    };
    marketSelectorStorageService = {
      storeSelectedOption: jasmine.createSpy(),
      restoreSelectedOption: jasmine.createSpy()
    };

    component = new MatchesMarketSelectorComponent(
      pubSubService,
      marketSelectorTrackingService,
      marketSelectorStorageService,
      filtersService,
      activatedRoute
    );

    component.selectorType = 'footballCoupons';
    component.multipleEventsDataSections = typeSegment;
  });

  describe('@ngOnInit', () => {
    it('should load selector for Football Coupons', () => {
      component.marketOptions = [{
        title: 'Match Result',
        templateMarketName: 'Match Betting',
        header: ['Home', 'Draw', 'Away']
      }, {
        title: 'Both Teams to Score',
        templateMarketName: 'Both Teams to Score',
        header: ['Yes', 'No']
      }];
      component.selectorType = 'footballCoupons';
      component.sportId = '16';
      component.targetTab = {
        marketsNames: [
          {templateMarketName: 'Match Result', title: 'Match Result'},
          {templateMarketName: 'To Qualify', title: 'To Qualify'},
          {templateMarketName: 'Match Result and Both Teams To Score', title: 'Match Result and Both Teams To Score'},
          {templateMarketName: 'Total Goals Over/Under 2.5', title: 'Total Goals Over/Under 2.5'},
          {templateMarketName: 'Both Teams to Score', title: 'Both Teams to Score'},
        ]
      } as any;
      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'MarketSelector', ['DELETE_EVENT_FROM_CACHE', 'DELETE_MARKET_FROM_CACHE'], jasmine.any(Function));
      expect(component.selectOptions).toEqual(component.marketOptions);
      component.targetTab = null;
      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'MarketSelector', ['DELETE_EVENT_FROM_CACHE', 'DELETE_MARKET_FROM_CACHE'], jasmine.any(Function));
      expect(component.selectOptions).toEqual(component.marketOptions);
    });

    it('should call pubsub and connect callbacks', () => {
      component['initData'] = jasmine.createSpy('initData');
      component.targetTab = {
        marketsNames: [
          {templateMarketName: 'Match Result', title: 'Match Result'},
          {templateMarketName: 'To Qualify', title: 'To Qualify'},
          {templateMarketName: 'Match Result and Both Teams To Score', title: 'Match Result and Both Teams To Score'},
          {templateMarketName: 'Total Goals Over/Under 2.5', title: 'Total Goals Over/Under 2.5'},
          {templateMarketName: 'Both Teams to Score', title: 'Both Teams to Score'},
        ]
      } as any;
      component.ngOnInit();

      expect(component['initData']).toHaveBeenCalledTimes(2);
    });

    it('should load selector for Inplay', () => {
      component.selectorType = 'footballInplay';
      component.sportId = '16';
      component.targetTab = {
        marketsNames: [
          {templateMarketName: 'Match Result', title: 'Match Result'},
          {templateMarketName: 'To Qualify', title: 'To Qualify'}
        ]
      } as any;
      component.ngOnInit();
      const selectOptions = [{
        templateMarketName: 'Match Result',
        title: 'Match Result'
      },
      {
        templateMarketName: 'To Qualify',
        title: 'To Qualify'
      }];
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'MarketSelector', ['DELETE_EVENT_FROM_CACHE', 'DELETE_MARKET_FROM_CACHE'], jasmine.any(Function));
      expect(component.selectOptions).toEqual(selectOptions);
    });

    it('selector data should be null', () => {
      component.selectorType = 'footballTest';
      component['initData'] = jasmine.createSpy('initData');
      component.marketOptions = [];
      component.targetTab = {
        label: '',
        marketsNames: []
      } as any;
      component.ngOnInit();
      expect(component.SELECTOR_DATA).toBe(null);
    });
  });

  describe('@ngOnDestroy', () => {
    it('should unsubscribe from Events', () => {
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalled();
    });
  });

  it('should create a component', () => {
    expect(component).toBeTruthy();
  });

  it('trackById should return a string', () => {
    const mockLeg = { id: '1', title: 'test' } as ICouponMarketSelector;
    const result = component.trackById(1, mockLeg);

    expect(result).toBe('11');
  });

  describe('#modifyMarket', () => {
    it('it should change templateMarketName if rawHandicapValue is exist in templateMarketName and sport is football', () => {
      component.sportName = 'football';
      const market = {
        templateMarketName: 'Over/Under Total Goals',
        rawHandicapValue: '1.5'
      } as IMarket;
      const resultMarket = {
        rawHandicapValue: '1.5',
        templateMarketName: 'Over/Under Total Goals 1.5'
      } as IMarket;
      const event = { categoryName: 'football' } as any;

      expect(component['modifyMarket'](market, event)).toEqual(resultMarket);
    });

    it('it should change templateMarketName if rawHandicapValue is exist in templateMarketName and sport is not football', () => {
      component.sportName = 'football';
      const market = {
        templateMarketName: 'Over/Under Total Goals',
        rawHandicapValue: '1.5'
      } as IMarket;
      const resultMarket = {
        rawHandicapValue: '1.5',
        templateMarketName: 'Over/Under Total Goals'
      } as IMarket;
      const event = { categoryName: 'cricket' } as any;

      expect(component['modifyMarket'](market, event)).toEqual(resultMarket);
    });
  });

  describe('filterMarkets', () => {
    it('filterMarkets should filter data by market for footballCoupons', () => {
      spyOn(component.hideEnhancedSection, 'emit');
      component.sportName = 'Football';
      component.sportId = '111';
      component.selectOptions = [{
        title: 'Match Result',
        templateMarketName: 'Match Betting',
        header: ['Home', 'Draw', 'Away']
      }, {
        title: 'Both Teams to Score',
        templateMarketName: 'Both Teams to Score',
        header: ['Yes', 'No']
      }];

      component.selectorType = 'footballCoupons';
      component.SELECTOR_DATA = marketSelectorConfigService.footballCoupons[0];
      component.filterMarkets('Match Betting,Both Teams to Score');

      expect(marketSelectorStorageService.storeSelectedOption).toHaveBeenCalledWith('football', 'Match Betting');
      expect(component.hideEnhancedSection.emit).toHaveBeenCalled();
      expect(component.marketFilterText).toEqual('Match Result');
    });
    it('filterMarkets should filter data by market for footballinplay', () => {
      spyOn(component.hideEnhancedSection, 'emit');
      component.sportName = 'Football';
      component.sportId = '111';
      component.selectOptions = [{
        templateMarketName: 'Match Betting,Both Teams to Score',
        title: 'Match Result'
      },
      {
        templateMarketName: 'To Qualify',
        title: 'To Qualify'
      }];

      component.selectorType = 'footballInplay';
      marketSelectorConfigService.footballInplay[0].MARKETS_NAMES['Match Betting,Both Teams to Score'] = 'Match Result';
      component.SELECTOR_DATA = marketSelectorConfigService.footballInplay[0];
      component.filterMarkets('Match Betting,Both Teams to Score');

      expect(marketSelectorStorageService.storeSelectedOption).toHaveBeenCalledWith('football', 'Match Betting,Both Teams to Score');
      expect(marketSelectorTrackingService.pushToGTM).toHaveBeenCalledWith('Match Result', '111');
      expect(component.hideEnhancedSection.emit).toHaveBeenCalled();
      expect(component.marketFilterText).toEqual('Match Result');

      component.sportId = '18';
      component.filterMarkets('Match Betting,Both Teams to Score');
    });
    it('filterMarkets should filter data by market for Darts and Update the GTM', () => {
      spyOn(component.hideEnhancedSection, 'emit');
      component.sportName = 'Darts';
      component.sportId = '13';
      component.selectOptions = [{
        templateMarketName: 'Total 180s Over/Under',
        title: 'Total 180s'
      },
      {
        templateMarketName: 'Match Result',
        title: 'Match Result'
      },
      {
        templateMarketName: 'Most 180s',
        title: 'Most 180s'
      }];

      component.selectorType = 'sportMatches';
      component.SELECTOR_DATA = {
        SPORT_ID: 13,
        DEFAULT_SELECTED_OPTION: 'Match Result',
        MARKETS_NAME_ORDER: [
          'Match Result', 'Most 180s', 'Leg Winner', 'Total 180s Over/Under', 'Leg Handicap', 'Match Handicap'
        ],
        MARKETS_NAMES: {
          'Match Result': 'Match Result',
          'Most 180s': 'Most 180s',
          'Leg Winner': 'Next Leg Winner',
          'Total 180s Over/Under,Total 180s': 'Total 180s',
          'Leg Handicap': 'Handicap',
          'Match Handicap': 'Handicap'
        }
      };
      component.filterMarkets('Total 180s Over/Under,Total 180s');
      expect(marketSelectorTrackingService.pushToGTM).toHaveBeenCalledWith('Total 180s', '13');
    });


    it(`should work with array of strings`, () => {
      const filters = ['Match Betting', 'Both Teams to Score'];
      component.selectOptions = [];
      spyOn(component.filterChange, 'emit');
      component.SELECTOR_DATA = marketSelectorConfigService.footballCoupons[0];
      component.filterMarkets(filters);

      expect(component.filterChange.emit).toHaveBeenCalledWith(filters[0]);
      expect(component.marketFilterText).toEqual('');
    });

    it(`should work with array of strings with only one item`, () => {
      const filters = ['Match Result'];
      component.selectOptions = [];
      component.sportId = '111';

      spyOn(component.filterChange, 'emit');
      component.SELECTOR_DATA = marketSelectorConfigService.footballCoupons[0];
      component.filterMarkets(filters);

      expect(component.filterChange.emit).toHaveBeenCalledWith(filters[0]);
      expect(component['marketSelectorTrackingService'].pushToGTM).toHaveBeenCalledWith('Match Result', '111');
      expect(component.marketFilterText).toEqual('');
    });
  });

  describe('storedSelectorOption', () => {
    it('marketFilter set with storedData when there is no storedSelectorOption data', () => {
      const marketArr = ['match betting'];
      const filters = ['match betting'];
      component.marketFilter = 'match betting';
      spyOn(component.filterChange, 'emit');
      component['initActiveOption'](marketArr);
      expect(component.filterChange.emit).toHaveBeenCalledWith(filters[0]);
    });
    it('marketFilter set with storedData when there is storedSelectorOption data', () => {
      const marketArr = ['match betting'];
      const filters = ['match betting'];
      component.marketFilter = 'match betting';
      spyOn(component.filterChange, 'emit');
      marketSelectorStorageService.restoreSelectedOption = jasmine.createSpy().and.returnValue('match betting');
      component['initActiveOption'](marketArr);
      expect(component.filterChange.emit).toHaveBeenCalledWith(filters[0]);
    });
  });
  it('should call ngOnChanges', () => {
    const changes = {
      multipleEventsDataSections: {
        currentValue: '12',
        previousValue: '11'
      },
      eventDataSection: {
        currentValue: '12',
        previousValue: '11'
      },
    }
   
    component.ngOnChanges(changes);
    expect(component).toBeTruthy();
  });

  it('should call getMarketNamesArray', () => {
    component.eventDataSection = {
      typeId: 971,
      events: [{
        id: 5112681,
        markets: [{
          templateMarketName: 'Match Result',
          outcomes: []
        }, {
          templateMarketName: 'To Qualify',
          outcomes: []
        }]
      }, {
        id: 3567838,
        markets: [{
          templateMarketName: 'Match Result',
          outcomes: []
        }]
      }]
    } as any;
    component.multipleEventsDataSections = undefined;
  
    expect(component['getMarketNamesArray']().length).toEqual(3);
  });
  it('should call getActiveOption', () => {
    component.SELECTOR_DATA = {DEFAULT_SELECTED_OPTION: 'Match Betting'} as any;
    expect(component['getActiveOption'](['Handicap Betting'])).toEqual('Handicap Betting');
  });
  it('should call sortMarketNames', () => {
    component['sortMarketNames'](['Handicap Betting','Match Result,Total Points'],['Handicap Betting'])
    expect(component).toBeTruthy();
  });
  it('should call modifyMarket', () => {
    const event = {
      id: 5112681,
      name: 'match1 vs match2',
      markets: [{
        templateMarketName: 'Match Result',
        name: 'Match Result',
        outcomes: []
      }, {
        templateMarketName: 'To Qualify',
        name: 'To Qualify',
        outcomes: []
      }]
    } as any;
    component.selectorType = 'Market';
    
    expect(component['modifyMarket']({templateMarketName: 'Match Betting', outcomes: []} as any, event).templateMarketName).toEqual('Match Result');
    expect(component['modifyMarket']({templateMarketName: 'To Qualify',name: 'To Qualify',
     outcomes: [{id: 1,name: 'To Qualify'},{id: 2,name: 'To Qualify'}]} as any, event).templateMarketName).toEqual('');
  });
});
