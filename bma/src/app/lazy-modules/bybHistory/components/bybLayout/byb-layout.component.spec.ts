import { fakeAsync, tick } from '@angular/core/testing';
import { BybLayoutComponent } from './byb-layout.component';

describe('BybLayoutComponent', () => {
  let yourCallService;
  let yourCallMarketsService;
  let aggregateService;
  let dashBoardService;
  let bybSelectedSelectionsService;
  let component: BybLayoutComponent;

  beforeEach(() => {
    yourCallService = {
      sendToggleGTM: jasmine.createSpy('sendToggleGTM'),
      accordionsStateInit: jasmine.createSpy('accordionsStateInit')
    };

    yourCallMarketsService = {
      getAgregatedMarketsData: jasmine.createSpy('getAgregatedMarketsData').and.returnValue(Promise.resolve()),
      clear: jasmine.createSpy('clear'),
      showMarkets: jasmine.createSpy('showMarkets'),
      isRestoredNeeded: jasmine.createSpy('isRestoredNeeded').and.returnValue(true),
      restoreBet: jasmine.createSpy('restoreBet').and.returnValue(true),
      isAnyStoredBets: jasmine.createSpy('isAnyStoredBets').and.returnValue(true),
      loadMarket: jasmine.createSpy('loadMarket').and.returnValue(Promise.resolve({})),
      getStoredBetsMarketsNames: jasmine.createSpy('getStoredBetsMarketsNames').and.returnValue(['market1']),
      game: {
        homeTeam: 'homeTeam',
        visitingTeam: 'visitingTeam'
      },
      players: [{}],
      markets: [{
        key: 'Total Goals',
        grouping: 'Total Goals',
        markets: ['m1', 'm2']
      }, {
        key: 'market3',
        grouping: 'Both Teams To Score',
        markets: []
      },
      {
        key: 'Total Corners',
        grouping: 'Total Corners',
        markets: ['m1', 'm2']
      },
      {
        key: 'Match Booking Points',
        grouping: 'Match Booking Points',
        markets: ['m1', 'm2']
      }]
    };

    dashBoardService = {
      clear: jasmine.createSpy('clear'),
      eventObj: {}
    };
    aggregateService = {
      teamA: 'Arsenal',
      teamB: 'Liverpool'
    };
    bybSelectedSelectionsService = {
      eventEntity: {},
      marketFilterBYB: {},
      callGTM: jasmine.createSpy('callGTM').and.returnValue(true),
    };

    component = new BybLayoutComponent(
      yourCallMarketsService,
      dashBoardService,
      yourCallService,
      aggregateService,
      bybSelectedSelectionsService
    );

    component.eventEntity = {} as any;
  });

  describe('#trackByMarket', () => {
    it('should call trackByMarket method', () => {
      const result = component.trackByMarket(1, { title: 'title' } as any);

      expect(result).toEqual('1title');
    });
  });

  describe('#teams', () => {
    it('should get teams', () => {
      expect(component.teams).toEqual(['homeTeam', 'visitingTeam'] as any);
    });
  });

  describe('#players', () => {
    it('should get players', () => {
      expect(component.players).toEqual([{}] as any);
    });
  });

  describe('#getMarkets', () => {
    it('should call getMarkets method', fakeAsync(() => {
      component.eventEntity = { id: '12345', name: 'Event Name' } as any;
      component['getMarkets']();

      tick();

      expect(yourCallMarketsService.getAgregatedMarketsData).toHaveBeenCalled();
      expect(yourCallMarketsService.showMarkets).toHaveBeenCalled();
      expect(yourCallMarketsService.isAnyStoredBets).toHaveBeenCalledWith('12345');
      expect(yourCallMarketsService.getStoredBetsMarketsNames).toHaveBeenCalledWith('12345');
      expect(dashBoardService.eventObj).toEqual({ id: '12345', name: 'Event Name' });
    }));

    it('should call getMarkets method when no evententity', fakeAsync(() => {
      component.eventEntity = { id: '12345', name: 'Event Name' } as any;
      yourCallMarketsService.isAnyStoredBets.and.returnValue(false);
      component['getMarkets']();

      tick();

      expect(yourCallMarketsService.getAgregatedMarketsData).toHaveBeenCalled();
      expect(yourCallMarketsService.showMarkets).toHaveBeenCalled();
      expect(yourCallMarketsService.isAnyStoredBets).toHaveBeenCalledWith('12345');
      expect(yourCallMarketsService.getStoredBetsMarketsNames).not.toHaveBeenCalled();
      expect(dashBoardService.eventObj).toEqual({ id: '12345', name: 'Event Name' });
    }));

    it('should call getMarkets method with error', fakeAsync(() => {
      yourCallMarketsService.getAgregatedMarketsData.and.returnValue(Promise.reject());
      component['getMarkets']();

      tick();

      expect(yourCallMarketsService.getAgregatedMarketsData).toHaveBeenCalled();
      expect(yourCallMarketsService.showMarkets).not.toHaveBeenCalled();
      expect(yourCallMarketsService.isAnyStoredBets).not.toHaveBeenCalled();
      expect(yourCallMarketsService.getStoredBetsMarketsNames).not.toHaveBeenCalled();
      expect(dashBoardService.eventObj).toEqual({});
    }));
  });

  describe('#ngOnInit', () => {
    it('should call ngOnInit', () => {
      spyOn(component, 'init');
      component.ngOnInit();
      expect(component.init).toHaveBeenCalled();
    });
  });

  //init
  describe('#init', () => {
    it('should call init', () => {
      spyOn(component, 'replaceDefaultParticipantNames');
      spyOn(component, 'getMarkets' as any);
      component.init();
      expect(component.replaceDefaultParticipantNames).toHaveBeenCalled();
    });
  });

  //replaceDefaultParticipantNames
  describe('#replaceDefaultParticipantNames', () => {
    it('should call replaceDefaultParticipantNames', () => {
      spyOn(component, 'getMarkets' as any);
      component.replaceDefaultParticipantNames('Arsenal', 'Liverpool');
      expect(component.currMarkets.length).toBeGreaterThan(0);
    });
  });

  //fillData
  describe('#fillData', () => {
    it('should call fillData', () => {
      spyOn(component, 'addAllGroupMarkets');
      spyOn(component, 'addIdsToMap');
      component.fillData();
      expect(component.dataFilled).toBeTruthy();
    });

    it('should call fillData', () => {
      component.dataFilled = true;
      component.fillData();
      expect(component.dataFilled).toBeTruthy();
    });

    it('should call fillData without markets', () => {
      yourCallMarketsService.markets = null;
      component.dataFilled = false;
      component.fillData();
      expect(component.dataFilled).toBeFalsy();
    });
  });

  //addIdsToMap
  describe('#addIdsToMap', () => {
    it('should call fillData', () => {
      component.currMarketsMap.set('market3', {});
      component.addIdsToMap(yourCallMarketsService.markets);
      expect(component.currMarketsMap.size).toBeGreaterThan(0);
    });

    it('should call fillData without id', () => {
      component.currMarketsMap.set('market3', {});
      component.addIdsToMap([{ markets: { key: 'market3' }, key: 'market3' }] as any);
      expect(component.currMarketsMap.size).toBeGreaterThan(0);
    });
  });

  //addAllGroupMarkets
  describe('#addAllGroupMarkets', () => {
    it('should call fillData', () => {
      component.currMarkets = ['Total Goals', 'Total Corners', 'Match Booking Points'];
      spyOn(component, 'populateEnabledMarketSwitchers');
      component.addAllGroupMarkets();
      expect(component.allMarketsMap.size).toBeGreaterThan(0);
    });

    it('should call fillData', () => {
      component.currMarkets = ['Total Goals', 'Total Corners', 'Match Booking Points'];
      yourCallMarketsService.markets = [{
        key: 'Total Goals',
        grouping: 'Total Goals',
        markets: ['m1', 'm2']
      }];
      component.allMarketsMap = new Map();
      component.allMarketsMap.set('Total Goals', [1, 2, 3]);
      spyOn(component, 'populateEnabledMarketSwitchers');
      component.addAllGroupMarkets();
      expect(component.allMarketsMap.size).toBeGreaterThan(0);
    });
  });

  //onTabChange
  describe('#onTabChange', () => {
    it('should call onTabChange', () => {
      component.expandCollapseMap = [];
      component.onTabChange({ 'market': 'All Markets' });
      expect(component.expandCollapseMap[0]).toBeTruthy();
    });

    it('should call onTabChange and skip if', () => {
      component.openDefaultMap = new Map();
      component.expandCollapseMap = [];
      component.openDefaultMap.set('not', 0);
      component.onTabChange({ 'market': 'not' });
      expect(component.expandCollapseMap[0]).toBeTruthy();
    });

    it('should call onTabChange and skip if', () => {
      component.openDefaultMap = new Map();
      component.expandCollapseMap = [];
      component.openDefaultMap.set('not', 0);
      component.onTabChange({ 'market': 'not' });
      expect(component.expandCollapseMap[0]).toBeTruthy();
    });
  });

  //marketFilters
  describe('#marketFilters', () => {
    it('should call marketFilters return false', () => {
      const retVal = component.marketFilters({} as any, 0);
      expect(retVal).toBeFalsy();
    });

    it('should call marketFilters return true', () => {
      component.marketFilter = 'All Markets';
      const retVal = component.marketFilters({} as any, 0);
      expect(retVal).toBeTruthy();
    });

    it('should call marketFilters with popular Market', () => {
      component.marketFilter = 'Popular Markets';
      component.expandCollapseMap = [];
      component.openDefaultMap = new Map();
      const retVal = component.marketFilters({ popularMarket: true } as any, 0);
      expect(retVal).toBeTruthy();
    });

    it('should call marketFilters with popular Market1', () => {
      component.marketFilter = 'Popular Markets';
      component.expandCollapseMap = [];
      component.openDefaultMap = new Map();
      const retVal = component.marketFilters({ popularMarket: false } as any, 0);
      expect(retVal).toBeFalsy();
    });
  });

  //ngOnDestroy
  describe('#ngOnDestroy', () => {
    it('should call ngOnDestroy', () => {
      component.ngOnDestroy();
      expect(yourCallMarketsService.selectedSelectionsSet.size).toBe(0);
    });
  });

  //expandCollapse
  describe('#expandCollapse', () => {
    it('should call expandCollapse', () => {
      yourCallMarketsService.selectedSelectionsSet = new Set();
      component.expandCollapseMap = [];
      component.expandCollapse({} as any, 0);
      expect(yourCallMarketsService.selectedSelectionsSet.size).toBe(0);
    });

    it('should call expandCollapse', () => {
      yourCallMarketsService.selectedSelectionsSet = new Set();
      component.expandCollapseMap = [];
      component.expandCollapse({} as any, 5);
      expect(yourCallMarketsService.selectedSelectionsSet.size).toBe(0);
    });
  });

  //setExpandedMarkets
  describe('#setExpandedMarkets', () => {
    it('should call setExpandedMarkets', fakeAsync(() => {
      yourCallMarketsService.selectedSelectionsSet = new Set();
      component.expandCollapseMap = [true, false];
      component.markets = [{ key: 'Total Goals', type: 'group', markets: [{ key: 'k1' }] as any }] as any;
      component.setExpandedMarkets(['Total Goals']);
      tick();
      expect(yourCallMarketsService.restoreBet).toHaveBeenCalled();
    }));

    it('should call setExpandedMarkets', fakeAsync(() => {
      yourCallMarketsService.selectedSelectionsSet = new Set();
      component.expandCollapseMap = [true, false];
      component.markets = [{ key: 'Total Goals', type: 'group1', markets: [{ key: 'k1' }] as any }] as any;
      component.setExpandedMarkets(['Total Goals']);
      tick();
      expect(yourCallMarketsService.restoreBet).not.toHaveBeenCalled();
    }));

    it('should call setExpandedMarkets', fakeAsync(() => {
      yourCallMarketsService.selectedSelectionsSet = new Set();
      component.expandCollapseMap = [true, false];
      component.markets = [{ key: 'ANYTIME GOALSCORER', type: 'group1', markets: [{ key: 'k1' }] as any }] as any;
      component.setExpandedMarkets(['ANYTIME GOALSCORER']);
      tick();
      expect(yourCallMarketsService.restoreBet).toHaveBeenCalled();
    }));
  });

  //setExpandedByDefaultMarkets
  describe('#setExpandedByDefaultMarkets', () => {
    it('should call setExpandedByDefaultMarkets', () => {
      yourCallMarketsService.selectedSelectionsSet = new Set();
      component.expandCollapseMap = [true, false];
      component.markets = [{ key: 'Total Goals', type: 'group', available: true, markets: [{ key: 'k1' }] as any }] as any;
      component.setExpandedByDefaultMarkets();
      expect(component.markets.length).toBe(1);
    });

    it('should call setExpandedByDefaultMarkets', () => {
      yourCallMarketsService.selectedSelectionsSet = new Set();
      component.expandCollapseMap = [true, false];
      component.markets = [{ key: 'Total Goals', type: 'group', available: false, markets: [{ key: 'k1' }] as any }] as any;
      component.setExpandedByDefaultMarkets();
      expect(component.markets.length).toBe(1);
    });

    it('should call setExpandedByDefaultMarkets', () => {
      yourCallMarketsService.selectedSelectionsSet = new Set();
      component.expandCollapseMap = [true, false];
      component.markets = [];
      component.setExpandedByDefaultMarkets();
      expect(component.markets.length).toBe(0);
    });

    it('should call setExpandedByDefaultMarkets no markets', () => {
      component.markets = null;
      const retVal = component.setExpandedByDefaultMarkets();
      expect(retVal).toBeFalsy();
    });
  });

  //allMarkets
  describe('#allMarkets', () => {
    it('should call get allMarkets', () => {
      const retVal = component.allMarkets;
      expect(retVal.length).toBe(4);
    });

    it('should call set allMarkets', () => {
      component.allMarkets = [];
      expect(component.allMarkets.length).toBe(0);
    });
  });

  //PopulateEnabledMarketSwitchers
  describe('#populateEnabledMarketSwitchers', () => {
    it('should call populateEnabledMarketSwitchers with realdata', () => {
      component.players = [{
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "ARSENAL",
        "appearances": 21,
        "cleanSheets": 2,
        "tackles": 1.1,
        "passes": 17.7,
        "crosses": 17.7,
        "assists": 7,
        "shots": 1.8,
        "shotsOnTarget": 0.7,
        "shotsOutsideTheBox": 1.8,
        "goals": 4,
        "goalsInsideTheBox": 4,
        "goalsOutsideTheBox": 4,
        "cards": 0,
        "cardsRed": 0,
        "cardsYellow": 0,
        "penaltySaves": null,
        "conceeded": null,
        "saves": null,
        "isGK": false
      }] as any;
      const marketGroup = { popularMarket: true, marketType: 'Player Bet' ,available :true };
      component.enabledMarketSwitchers = {};
      component.populateEnabledMarketSwitchers(marketGroup as any);
      expect(component.enabledMarketSwitchers['Player Bets']).toBeTruthy();
    });

    it('should call populateEnabledMarketSwitchers with palyerbet', () => {
      component.players = [];
      const marketGroup = { popularMarket: true, marketType: 'Player Bet', available :true };
      component.enabledMarketSwitchers = {};
      component.populateEnabledMarketSwitchers(marketGroup as any);
      expect(component.enabledMarketSwitchers['Player Bets']).toBeTruthy();
    });

    it('should call populateEnabledMarketSwitchers with teambet', () => {
      const marketGroup = { popularMarket: false, marketType: 'Team Bet',available :true };
      component.enabledMarketSwitchers = {};
      component.populateEnabledMarketSwitchers(marketGroup as any);
      expect(component.enabledMarketSwitchers['Team Bets']).toBeTruthy();
    });
  });

  //marketStatus
  describe('#marketStatus', () => {
    it('should call marketStatus', () => {
      component.newMarkets = new Set();
      component.newMarkets.add('m1');
      const retVal = component.marketStatus({ grouping: 'm1' } as any);
      expect(retVal).toBeFalsy();
    });
  });

  //duplicate market status
  describe('#marketStatus', () => {
    it('should call marketStatus', () => {
      component.newMarkets = new Set();
      component.newMarkets.add('m1');
      const retVal = component.marketStatus({ grouping: 'm1' } as any);
      expect(retVal).toBeFalsy();
    });
  });
});
