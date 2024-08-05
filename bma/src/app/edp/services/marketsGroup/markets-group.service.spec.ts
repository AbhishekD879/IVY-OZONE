import { CashOutLabelService } from '@core/services/cashOutLabel/cash-out-label.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { IsPropertyAvailableService } from '@sb/services/isPropertyAvailable/is-property-available.service';
import { MarketsGroupService } from '@edp/services/marketsGroup/markets-group.service';
import { IOutcome } from '@core/models/outcome.model';
import { IGroupedMarket } from '@edp/services/marketsGroup/markets-group.model';
import { IMarket } from '@core/models/market.model';

describe('MarketsGroupService', () => {
  let service: MarketsGroupService;
  let market;
  let marketConfig;

  let isPropertyAvailableService: IsPropertyAvailableService,
    cashOutLabelService: CashOutLabelService,
    filterService: FiltersService;

  beforeEach(() => {
    market = {
      id: 'market_id',
      templateMarketName: 'Market name period'
    };
    marketConfig = {
      periods: [{
        marketsNames: ['Market name period']
      }]
    };
    isPropertyAvailableService = {
      isPropertyAvailable: () => {
        return () => {};
      }
    } as any;

    cashOutLabelService = {
      checkCondition: jasmine.createSpy()
    } as any;

    filterService = {
      orderBy: jasmine.createSpy().and.returnValue([]),
      filterAlphabetsOnly: jasmine.createSpy('filterAlphabetsOnly'),
      filterNumbersOnly: jasmine.createSpy('filterNumbersOnly')
    } as any;

    service = new MarketsGroupService(
      isPropertyAvailableService,
      cashOutLabelService,
      filterService
    );
  });

  it('should add Market to marketConfig in periods section', () => {
    service.generateMarketsGroup([market] as any, marketConfig as any);
    expect(marketConfig.periods[0]['markets'].length).toEqual(1);
    expect(marketConfig.periods[0]['markets'][0].id).toEqual(market.id);
  });

  it('should not add Market to marketConfig', () => {
    spyOn(service as any, 'getDisplayOrder').and.returnValue(1);
    market.templateMarketName = 'some template';
    service.generateMarketsGroup([market] as any, marketConfig as any);
    expect(marketConfig.periods[0]['markets'].length).toEqual(0);
  });

  describe('getSortedOutcomes', () => {
    it('should be added fake outcomes if there are not enough outcomes to display - header exist', () => {
      const groupedMarket = {
        name: 'Handicap Results',
        header: [{ name: 'Home' }, { name: 'Tie' }, { name: 'Away' } ],
        outcomesSort: ['outcomeMeaningMinorCode']
      } as IGroupedMarket;
      const outcomes = [
        { outcomeMeaningMinorCode: 1, name: 'name A', marketsNames: 'Total Goals', prices: [], cashoutAvail: 'N' },
        { outcomeMeaningMinorCode: 2, name: 'name B', marketsNames: 'Total Goals', prices: [], cashoutAvail: 'N' }] as IOutcome[];
      service['getSortedOutcomes'](outcomes, groupedMarket, true);
      expect(outcomes[2]).toEqual({
        fakeOutcome: true,
        name: 'Away',
        marketsNames: 'Total Goals',
        prices: [],
        cashoutAvail: 'N',
        outcomeMeaningMinorCode: 3
      } as IOutcome);
      expect(filterService.orderBy).toHaveBeenCalledWith(outcomes, ['outcomeMeaningMinorCode']);
    });

    it('should be added fake outcomes if there are not enough outcomes to display - header is not exist', () => {
      const groupedMarket = {
        name: 'Handicap Results',
        outcomesSort: ['sortOrder']
      } as IGroupedMarket;
      const outcomes = [
        { outcomeMeaningMinorCode: 1, name: 'name A', marketsNames: 'Total Goals', prices: [], cashoutAvail: 'Y' },
        { outcomeMeaningMinorCode: 3, name: 'name C', marketsNames: 'Total Goals', prices: [], cashoutAvail: 'Y' }] as IOutcome[];
      service['getSortedOutcomes'](outcomes, groupedMarket, true);
      expect(outcomes[2]).toEqual({
        fakeOutcome: true,
        name: 'name A',
        marketsNames: 'Total Goals',
        prices: [],
        cashoutAvail: 'Y',
        outcomeMeaningMinorCode: 2
      } as IOutcome);
      expect(filterService.orderBy).toHaveBeenCalledWith(outcomes, ['sortOrder']);
    });
  });

 describe('#createMarketWithTypeOverUnderMarket', () => {
    it('add drilldownTagNames property from market entity to groupedMarket entity with undefined', () => {
      const groupedMarket = {},
        marketEntity = {};
        service['getFilteredOutcome'] = jasmine.createSpy('getFilteredOutcome').and.returnValue({});
      // @ts-ignore
      service['createMarketWithTypeOverUnderMarket']([], marketEntity, {}, [], groupedMarket);
      expect(groupedMarket).toEqual({ drilldownTagNames: undefined });
    });

    it('add drilldownTagNames property from market entity to groupedMarket entity with valid value', () => {
      const groupedMarket = {},
        marketEntity = { drilldownTagNames: 'some,string,with,commas' };
        service['getFilteredOutcome'] = jasmine.createSpy('getFilteredOutcome').and.returnValue({});
      // @ts-ignore
      service['createMarketWithTypeOverUnderMarket']([], marketEntity, {}, [], groupedMarket);
      expect(groupedMarket).toEqual({ drilldownTagNames: 'some,string,with,commas' });
    });

    it('it should create market with type OverUnder', () => {
      const groupedMarket = {
        name: 'Match Result & Over/Under 2.5 Goals market',
        localeName: 'matchResultOverUnder25',
        marketsAvailable: false,
        template: 'cardHeader',
        type: 'overUnderMarket',
        outcomesSort: ['sortOrder'],
        marketSort: ['name'],
        sortByHeader: true,
        marketsTemplates: ['Match Result and Over/Under 2.5 Goals'],
        header: [{ name: 'over', sortOrder: 1 }, { name: 'under', sortOrder: 2 }],
        marketsNames: 'Match Result and Over/Under 2.5 Goals',
        drilldownTagNames: '',
        markets: []
      };
      const markets = [{
        name: 'B. M\'gladbach',
        marketTemplateName: 'Match Result and Over/Under 2.5 Goals',
        priceTypeCodes: 'LP',
        outcomes: [{
          outcomeMeaningMinorCode: 1,
          name: 'B. M\'gladbach and Over 2.5 Goals'
        }, {
          outcomeMeaningMinorCode: 1,
          name: 'B. M\'gladbach and Under 2.5 Goals'
        }]
      }, {
        name: 'Wolfsburg',
        marketTemplateName: 'Match Result and Over/Under 2.5 Goals',
        priceTypeCodes: 'LP',
        outcomes: [{
          outcomeMeaningMinorCode: 3,
          name: 'Wolfsburg and Over 2.5 Goals'
        }, {
          name: 'Wolfsburg and Under 2.5 Goals',
          outcomeMeaningMinorCode: 3
        }]
      }];
      const outcomes = [{
        outcomeMeaningMinorCode: 1,
        name: 'B. M\'gladbach and Over 2.5 Goals'
      }, {
        outcomeMeaningMinorCode: 1,
        name: 'B. M\'gladbach and Under 2.5 Goals'
      }];
      const resultMarket = {
        drilldownTagNames: undefined,
        header: [
          { name: 'over', sortOrder: 1 },
          { name: 'under', sortOrder: 2 }],
        localeName: 'matchResultOverUnder25',
        marketSort: ['name'],
        markets: [{
          cashoutAvail: undefined,
          name: 'B. M\'gladbach and Over 2.5 Goals',
          priceTypeCodes: 'LP',
          outcomes: [{
            outcomeMeaningMinorCode: 1,
            name: 'B. M\'gladbach and Over 2.5 Goals',
            sortOrder: 1
          }, {
            outcomeMeaningMinorCode: 1,
            name: 'B. M\'gladbach and Under 2.5 Goals',
            sortOrder: 2
          }]
        }, {
          cashoutAvail: undefined,
          name: 'B. M\'gladbach and Under 2.5 Goals',
          priceTypeCodes: 'LP',
          outcomes: [{
            outcomeMeaningMinorCode: 1,
            name: 'B. M\'gladbach and Over 2.5 Goals',
            sortOrder: 1
          }, {
            name: 'B. M\'gladbach and Under 2.5 Goals',
            outcomeMeaningMinorCode: 1,
            sortOrder: 2
          }]
        }],
        marketsAvailable: false,
        marketsNames: 'Match Result and Over/Under 2.5 Goals',
        marketsTemplates: ['Match Result and Over/Under 2.5 Goals'],
        name: 'Match Result & Over/Under 2.5 Goals market',
        outcomesSort: ['sortOrder'],
        sortByHeader: true,
        template: 'cardHeader',
        type: 'overUnderMarket'
      };
      filterService.orderBy = jasmine.createSpy('orderBy').and.returnValue(outcomes);
      service['getFilteredOutcome'] = jasmine.createSpy('getFilteredOutcome').and.returnValue({});
      // @ts-ignore
      service['createMarketWithTypeOverUnderMarket'](markets, markets[0], groupedMarket, outcomes, groupedMarket);
      expect(groupedMarket.markets[1]).toEqual(resultMarket.markets[1]);
    });
  });

  it('getTeams', () => {
    const markets = [];
    service['findTeams'] = jasmine.createSpy().and.returnValue({
      outcomes: [
        null, {
          outcomeMeaningMinorCode: 1
        },
        undefined
      ]
    });
    service['getFilteredOutcome'] = jasmine.createSpy('getFilteredOutcome').and.returnValue({});
    service.getTeams(markets, false);
    expect(service['findTeams']).toHaveBeenCalledTimes(1);
    expect(filterService.orderBy).toHaveBeenCalledTimes(1);
  });

  describe('getFilteredOutcome avid any other', () => {
    it('#1getTeams filter outcome if ', () => {
      const teams: any = {
        dispSortName: 'CS',
        outcomes: [
          { outcomeMeaningMinorCode: 1, outcomeMeaningScores: null, originalOutcomeMeaningMinorCode: 'H' },
          { outcomeMeaningMinorCode: 1, outcomeMeaningScores: '2,1', originalOutcomeMeaningMinorCode: 'S' }
        ]
      };
      const result = service['getFilteredOutcome'](teams.outcomes, teams, 'home');
      expect(result).not.toBeNull();
    });
    it('#1getTeams filter outcome if nodta home ', () => {
      const teams: any = {
        dispSortName: 'CS',
        outcomes: [
          { outcomeMeaningMinorCode: 3, outcomeMeaningScores: null, originalOutcomeMeaningMinorCode: 'H' },
          { outcomeMeaningMinorCode: 3, outcomeMeaningScores: '2,1', originalOutcomeMeaningMinorCode: 'S' }
        ]
      };
      const result = service['getFilteredOutcome'](teams.outcomes, teams, 'home');
      expect(result).toEqual(undefined);
    });
    it('#2getTeams filter outcome home else mr nodata home', () => {
      const teams: any = {
        dispSortName: 'MR',
        outcomes: [
          { outcomeMeaningMinorCode: 3, outcomeMeaningScores: null, originalOutcomeMeaningMinorCode: 'H' },
          { outcomeMeaningMinorCode: 3, outcomeMeaningScores: '2,1', originalOutcomeMeaningMinorCode: 'S' }
        ]
      };
      const result = service['getFilteredOutcome'](teams.outcomes, teams, 'home');
      expect(result).toEqual(undefined);
    });
    it('#2getTeams filter outcome home else ', () => {
      const teams: any = {
        dispSortName: 'MR',
        outcomes: [
          { outcomeMeaningMinorCode: 1, outcomeMeaningScores: null, originalOutcomeMeaningMinorCode: 'H' },
          { outcomeMeaningMinorCode: 1, outcomeMeaningScores: '2,1', originalOutcomeMeaningMinorCode: 'S' }
        ]
      };
      const result = service['getFilteredOutcome'](teams.outcomes, teams, 'home');
      expect(result).not.toBeNull();
    });
    it('#2getTeams filter outcome away if ', () => {
      const teams: any = {
        dispSortName: 'CS',
        outcomes: [
          { outcomeMeaningMinorCode: 3, outcomeMeaningScores: null, originalOutcomeMeaningMinorCode: 'H' },
          { outcomeMeaningMinorCode: 3, outcomeMeaningScores: '2,1', originalOutcomeMeaningMinorCode: 'S' }
        ]
      };
      const result = service['getFilteredOutcome'](teams.outcomes, teams, 'away');
      expect(result).not.toBeNull();
    });
    it('#2getTeams filter outcome away if nodata find ', () => {
      const teams: any = {
        dispSortName: 'CS',
        outcomes: [
          { outcomeMeaningMinorCode: 1, outcomeMeaningScores: null, originalOutcomeMeaningMinorCode: 'H' },
          { outcomeMeaningMinorCode: 1, outcomeMeaningScores: '2,1', originalOutcomeMeaningMinorCode: 'S' }
        ]
      };
      const result = service['getFilteredOutcome'](teams.outcomes, teams, 'away');
      expect(result).toEqual(undefined);
    });
    it('#2getTeams filter outcome away if nodata find ', () => {
      const teams: any = {
        dispSortName: 'CS',
        outcomes: [
          { outcomeMeaningMinorCode: 3, outcomeMeaningScores: null, originalOutcomeMeaningMinorCode: 'H' },
          { outcomeMeaningMinorCode: 3, outcomeMeaningScores: '2,1', originalOutcomeMeaningMinorCode: 'S' }
        ]
      };
      const result = service['getFilteredOutcome'](teams.outcomes, teams, 'away');
      expect(result).not.toBeNull();
    });
    it('#2getTeams filter outcome away else ', () => {
      const teams: any = {
        dispSortName: 'MR',
        outcomes: [
          { outcomeMeaningMinorCode: 3, outcomeMeaningScores: null, originalOutcomeMeaningMinorCode: 'H' },
          { outcomeMeaningMinorCode: 3, outcomeMeaningScores: '2,1', originalOutcomeMeaningMinorCode: 'S' }
        ]
      };
      const result = service['getFilteredOutcome'](teams.outcomes, teams, 'away');
      expect(result).not.toBeNull();
    });
    it('#2getTeams filter outcome away else nodata ', () => {
      const teams: any = {
        dispSortName: 'MR',
        outcomes: [
          { outcomeMeaningMinorCode: 1, outcomeMeaningScores: null, originalOutcomeMeaningMinorCode: 'H' },
          { outcomeMeaningMinorCode: 1, outcomeMeaningScores: '2,1', originalOutcomeMeaningMinorCode: 'S' }
        ]
      };
      const result = service['getFilteredOutcome'](teams.outcomes, teams, 'away');
      expect(result).toEqual(undefined);
    });
  });
  describe('getMarketsObg', () => {
    it('should sort market outcomes', () => {
      service['createMarketWithTypeMarketHeader'] = jasmine.createSpy('createMarketWithTypeMarketHeader');
      const markets: IMarket[] =
        [{ templateMarketName: 'tpl1',
          outcomes: [{}],
          liveServChannels: 'liveServChannels',
          isMarketBetInRun: 'true' } as IMarket];
      const groupedMarket: any = { type: 'marketHeader' };
      const marketPeriod: any = { marketsTemplates: ['tpl1'] };
      service['getMarketsObg'](markets, groupedMarket, marketPeriod);
      expect(filterService.orderBy).toHaveBeenCalledTimes(1);
      expect(marketPeriod.markets.length).toEqual(1);
      expect(service['outcomesArray'].length).toEqual(1);
      expect(service['outcomesArray'][0][0])
        .toEqual(jasmine.objectContaining({marketliveServChannels: 'liveServChannels', isMarketBetInRun: 'true'}));
    });
  });

  it('clearTeamName', () => {
    expect(service['clearTeamName']('')).toEqual('');
    expect(service['clearTeamName']('Team   A')).toEqual('Team A');
    expect(service['clearTeamName']('FC Viktoria Köln')).toEqual('FC Viktoria Köln');
  });

  it('updateMarketsGroup', () => {
    spyOn(service as any, 'updateMarketConfig');
    const groupedMarkets: any[] = [{ periods: [{}, {}] }, {}];
    service.updateMarketsGroup(market, groupedMarkets);
    expect(service['updateMarketConfig']).toHaveBeenCalledTimes(3);
  });

  describe('templateMarketInMarketsGroups', () => {
    it('should fund market groups by market name', () => {
      const groupedMarket = [];
      const dictionary = Object.create({ group1: [] });
      dictionary.group2 = ['name'];
      dictionary.group3 = [];
      service['groupedMarketToMarketsNamesDictionary'] = dictionary;
      expect(
        service.templateMarketInMarketsGroups(groupedMarket, 'name')
      ).toEqual(['group2'] as any);
    });

    it('should create markets dictionary', () => {
      spyOn(service as any, 'createGroupedMarketToMarketsNamesDictionary').and.returnValue({});
      service.templateMarketInMarketsGroups([], '');
      expect(service['createGroupedMarketToMarketsNamesDictionary']).toHaveBeenCalledTimes(1);
    });
  });

  describe('isMarketAvailable', () => {
    it('should return false (no all markets)', () => {
      expect(service.isMarketAvailable(null, null, null)).toBeFalsy();
    });

    it('should return false (no markets)', () => {
      expect(service.isMarketAvailable([], null, null)).toBeFalsy();
    });

    it('should return true', () => {
      service['getMarketNames'] = () => ['name'];
      expect(
        service.isMarketAvailable([], [{ templateMarketName: 'name' }] as any, {} as any)
      ).toBeTruthy();
    });
  });

  describe('removeScores', () => {
    it('no tema name', () => {
      expect(service.removeScores('')).toBe('');
    });

    it('should remove scores', () => {
      expect(service.removeScores('Team A 1-2')).toBe('Team A');
    });
  });

  describe('marketNamesArray', () => {
    it('market names as array', () => {
      const groupedMarket: any = { marketsNames: ['name1'] };
      const markets: any[] = [{ templateMarketName: 'name1' }, { templateMarketName: 'name2' }];
      service['marketNamesArray'](groupedMarket, markets);
      expect(service['marketsNames']).toEqual(['name1']);
    });

    it('market names as string', () => {
      const groupedMarket: any = { marketsNames: 'name2' };
      const markets: any[] = [{ templateMarketName: 'name1' }, { templateMarketName: 'name2' }];
      service['marketNamesArray'](groupedMarket, markets);
      expect(service['marketsNames']).toEqual(['name2']);
    });
  });

  describe('getMarketNames', () => {
    beforeEach(() => {
      spyOn(service as any, 'marketNamesArray');
    });

    it('market with periods', () => {
      service['getMarketNames']({ periods: [{}, {}] } as any, []);
      expect(service['marketNamesArray']).toHaveBeenCalledTimes(2);
    });

    it('market without periods', () => {
      service['getMarketNames']({} as any, []);
      expect(service['marketNamesArray']).toHaveBeenCalledTimes(1);
    });
  });

  it('findTeams', () => {
    const markets: any = [
      { dispSortName: 'MB', outcomes: [{}, { outcomeMeaningMinorCode: 1 }] },
      {
        dispSortName: 'MB',
        outcomes: [
          { outcomeMeaningMinorCode: 1 },
          { outcomeMeaningMinorCode: 2 },
          { outcomeMeaningMinorCode: 3 }
        ]
      }
    ];
    service['getFilteredOutcome'] = jasmine.createSpy('getFilteredOutcome').and.returnValue({});
    expect(service['findTeams'](markets, 'MB')).toEqual(markets[0]);
  });

  describe('findTeam', () => {
    beforeEach(() => {
      spyOn(service as any, 'clearTeamName');
    });

    it('team found', () => {
      service['getFilteredOutcome'] = jasmine.createSpy('getFilteredOutcome').and.returnValue({});
      service.getTeams = () => [{ outcomeMeaningMinorCode: 1 }] as any;
      service['findTeam']([], 1);
      expect(service['clearTeamName']).toHaveBeenCalledTimes(1);
    });

    it('team found', () => {
      service['getFilteredOutcome'] = jasmine.createSpy('getFilteredOutcome').and.returnValue({});
      service.getTeams = () => [] as any;
      service['findTeam']([], 1);
      expect(service['clearTeamName']).not.toHaveBeenCalled();
    });
  });

  describe('getTeamName', () => {
    const markets = Symbol('markets');
    let result;

    beforeEach(() => {
      spyOn(service as any, 'findTeam').and.callFake((m, code) => code === 1 ? 'Home team' : 'Away team');
      spyOn(service as any, 'clearTeamName').and.callThrough();
    });

    describe('should return Home team', () => {
      it('should return Home team', () => {
        result = (service as any).getTeamName(markets as any, ['Home 20 team market', 'coverage'], true);
      });
      it('should return Home team', () => {
        result = (service as any).getTeamName(markets as any, ['Home 20 team market', 'coverage'], false);
      });
      afterEach(() => {
        expect(result).toEqual('Home team');
        expect((service as any).clearTeamName.calls.allArgs()).toEqual([['Home 20 team market'], ['coverage']]);
      });
    });

    describe('should return Away team', () => {
      it('should return Home team', () => {
        result = (service as any).getTeamName(markets as any, ['not ho-me market'], true);
      });
      it('should return Home team', () => {
        result = (service as any).getTeamName(markets as any, ['not ho-me market'], false);
      });
      afterEach(() => {
        expect(result).toEqual('Away team');
        expect((service as any).clearTeamName).toHaveBeenCalledWith('not ho-me market');
      });
    });

    afterEach(() => {
      expect((service as any).findTeam.calls.allArgs()).toEqual([[markets, 1], [markets, 3]]);
    });
  });

  describe('getSortedOutcomes', () => {
    it('no outcomes', () => {
      expect(service['getSortedOutcomes'](null, null, false)).toBe(null);
    });

    it('should add fake outcome (by minor code)', () => {
      const outcomes: any = [{ outcomeMeaningMinorCode: 1 }];
      const groupedMarket: any = { header: ['home', 'away'] };
      service['getSortedOutcomes'](outcomes, groupedMarket, true);
      expect(outcomes[1]).toEqual(jasmine.objectContaining({ fakeOutcome: true }));
    });

    it('should add fake outcome (by market names)', () => {
      const outcomes: any = [{ outcomeMeaningMinorCode: 1 }];
      const groupedMarket: any = {
        marketsNames: ['mkt1', 'mkt2']
      };
      service['getSortedOutcomes'](outcomes, groupedMarket, false);
      expect(outcomes[1]).toEqual(jasmine.objectContaining({ fakeOutcome: true }));
    });

    it('should add sortOrder for outcome (header to market)', () => {
      const outcomes: any = [
        { outcomeMeaningMinorCode: 1, marketsNames: '1' },
        { outcomeMeaningMinorCode: 3, marketsNames: '3' }
      ];
      const groupedMarket: any = {
        header: ['home', 'away'],
        headerToMarket: { '1': { sortOrder: 1 }, '3': { sortOrder: 3 } }
      };
      service['getSortedOutcomes'](outcomes, groupedMarket, true);
      expect(outcomes[0].sortOrder).toBe(1);
      expect(outcomes[1].sortOrder).toBe(3);
    });

    it('should add sortOrder for outcome (sort by header)', () => {
      const outcomes: any = [
        { outcomeMeaningMinorCode: 1, name: 'home' },
        { outcomeMeaningMinorCode: 3, name: 'away' }
      ];
      const groupedMarket: any = {
        header: [{ name: 'home', sortOrder: 1 }, { name: 'away', sortOrder: 3 }],
        sortByHeader: {}
      };
      service['getSortedOutcomes'](outcomes, groupedMarket, true);
      expect(outcomes[0].sortOrder).toBe(1);
      expect(outcomes[1].sortOrder).toBe(3);
    });

    it('should not modify outcomes', () => {
      const outcomes: any = [{}];
      const groupedMarket: any = { marketsNames: '' };
      service['getSortedOutcomes'](outcomes, groupedMarket, false);
      expect(outcomes.length).toBe(1);
      expect(outcomes[0].sortOrder).not.toBeDefined();
    });
  });

  describe('isMarketType', () => {
    it('should return false (no market type)', () => {
      expect(service['isMarketType']('', '')).toBeFalsy();
    });

    it('should return true (market type as array)', () => {
      expect(service['isMarketType'](['mb'], 'mb')).toBeTruthy();
    });

    it('should return true (market type as string)', () => {
      expect(service['isMarketType']('mb', 'mb')).toBeTruthy();
    });
  });

  describe('createMarketWithTemplateRow', () => {
    it('should not sort outcomes', () => {
      service['createMarketWithTemplateRow'](null, null, {} as any);
      expect(filterService.orderBy).not.toHaveBeenCalled();
    });

    it('should sort outcomes', () => {
      const groupedMarket: any = { sortOrder: { '1': 1 } };
      const outcomes: any = [{ name: '1' }, { name: '2' }];
      service['createMarketWithTemplateRow']({} as any, outcomes, groupedMarket);
      expect(filterService.orderBy).toHaveBeenCalledTimes(1);
    });
  });

  it('createMarketWithTypeOverUnderMarket', () => {
    const markets: any[] = [{ name: 'A' }, { name: 'B' }];
    const marketPeriod: any = {};
    const outcomes: any[] = [{ name: 'A' }, { name: '' }];
    const groupedMarket: any = {};
    service['getFilteredOutcome'] = jasmine.createSpy('getFilteredOutcome').and.returnValue({});
    service.getTeams = () => markets;
    service['getSortedOutcomes'] = arr => arr;

    service['createMarketWithTypeOverUnderMarket'](
      markets, market, marketPeriod, outcomes, groupedMarket );

    expect(marketPeriod.markets).toEqual( [jasmine.objectContaining({ name: 'A'})] );
  });

  describe('createMarketWithTypeMarketHeader', () => {
    it('no goalscorer', () => {
      service['getFilteredOutcome'] = jasmine.createSpy('getFilteredOutcome').and.returnValue({});
      spyOn(service as any, 'createMarketWithTypeNoGoalscorer');
      service['createMarketWithTypeMarketHeader']([], {
        type: 'noGoalscorer'
      } as any);
      expect(service['createMarketWithTypeNoGoalscorer']).toHaveBeenCalledTimes(1);
    });

    it('should create markets and periods', () => {
      const markets: any[] = [
        { outcomeMeaningMinorCode: 1, name: 'teamA' },
        { outcomeMeaningMinorCode: 2, name: 'teamB' }
      ];
      const groupedMarket: any = {
        type: 'teams',
        markets: [{ outcomeMeaningMinorCode: 1 }]
      };
      service['outcomesArray'] = [
        { outcomeMeaningMinorCode: 1, prices: [{}] },
        { outcomeMeaningMinorCode: 2, prices: [{}], cashoutAvail: 'Y' },
        { outcomeMeaningMinorCode: 3, prices: [{}] }
      ];
      service['getSortedOutcomes'] = arr => arr;
      service['getTeams'] = arr => arr as any;

      service['createMarketWithTypeMarketHeader'](markets, groupedMarket);

      expect(groupedMarket.markets).toBeDefined();
      expect(groupedMarket.periods).toBeDefined();
    });
  });

  describe('createMarketWithTypeNoGoalscorer', () => {
    it('should not create no goalscorer market', () => {
      service['outcomesArray'] = [];
      const groupedMarket: any = {};
      service['createMarketWithTypeNoGoalscorer'](groupedMarket);
      expect(groupedMarket.noGoalscorer).not.toBeDefined();
    });

    it('should create no goalscorer market', () => {
      service['outcomesArray'] = [
        { outcomeMeaningMinorCode: 2 }
      ];
      service['getSortedOutcomes'] = arr => arr;
      const groupedMarket: any = {};
      service['createMarketWithTypeNoGoalscorer'](groupedMarket);
      expect(groupedMarket.noGoalscorer).toEqual( jasmine.objectContaining({ name: 'No Goalscorer' }) );
    });
  });

  describe('getMarketsObg', () => {
    let markets;
    let groupedMarket;
    let marketPeriod;

    beforeEach(() => {
      markets = [{ templateMarketName: 'tpl' }];
      groupedMarket = {};
      marketPeriod = { marketsTemplates: 'tpl' };
    });

    it('header to market', () => {
      groupedMarket.headerToMarket = { tpl: 'sort' };
      groupedMarket.outcomesSort = {};
      service['getMarketsObg'](markets, groupedMarket, marketPeriod);
      expect(filterService.orderBy).toHaveBeenCalledWith(['sort'], groupedMarket.outcomesSort);
    });

    it('market type "teamSwitch"', () => {
      groupedMarket.type = 'teamSwitch';
      spyOn(service as any, 'getTeamName');
      service['getMarketsObg'](markets, groupedMarket, marketPeriod);
      expect(service['getTeamName']).toHaveBeenCalledTimes(1);
    });

    it('market type "goalName"', () => {
      markets[0].name = 'teamA';
      groupedMarket.type = 'goalName';
      service['getMarketsObg'](markets, groupedMarket, marketPeriod);
      expect(markets[0].name).toEqual('teamA');
    });

    it('market type "goalName" (normalize name)', () => {
      markets[0].name = '1+ teamA';
      groupedMarket.type = 'goalName';
      service['getMarketsObg'](markets, groupedMarket, marketPeriod);
      expect(markets[0].name).toEqual('1+ teamA');
    });

    it('market type "handicapName"', () => {
      markets[0].outcomes = [{}];
      markets[0].rawHandicapValue = '1';
      groupedMarket.type = 'handicapName';
      service['getMarketsObg'](markets, groupedMarket, marketPeriod);
      expect(markets[0].name).toEqual('1');
    });

    it('market type "handicapNamePlus" (+1)', () => {
      markets[0].rawHandicapValue = '1';
      groupedMarket.type = 'handicapNamePlus';
      service['getMarketsObg'](markets, groupedMarket, marketPeriod);
      expect(markets[0].name).toEqual('+1');
    });

    it('market type "handicapNamePlus" (-1)', () => {
      markets[0].rawHandicapValue = '-1';
      groupedMarket.type = 'handicapNamePlus';
      service['getMarketsObg'](markets, groupedMarket, marketPeriod);
      expect(markets[0].name).toEqual('-1');
    });

    it('market type "marketName"', () => {
      spyOn(service as any, 'getTeamName');
      markets[0].name = 'teamA';
      groupedMarket.type = 'marketName';
      service['getMarketsObg'](markets, groupedMarket, marketPeriod);
      expect(service['getTeamName']).toHaveBeenCalledTimes(1);
    });

    it('market type "minorCode"', () => {
      spyOn(service as any, 'getSortedOutcomes');
      groupedMarket.type = 'minorCode';
      service['getMarketsObg'](markets, groupedMarket, marketPeriod);
      expect(service['getSortedOutcomes']).toHaveBeenCalledTimes(1);
    });

    it('market template row', () => {
      groupedMarket.template = 'row';
      spyOn(service as any, 'createMarketWithTemplateRow');
      service['getMarketsObg'](markets, groupedMarket, marketPeriod);
      expect(service['createMarketWithTemplateRow']).toHaveBeenCalledTimes(1);
    });

    it('market type "overUnderMarket"', () => {
      spyOn(service as any, 'createMarketWithTypeOverUnderMarket');
      groupedMarket.type = 'overUnderMarket';
      service['getMarketsObg'](markets, groupedMarket, marketPeriod);
      expect(service['createMarketWithTypeOverUnderMarket']).toHaveBeenCalledTimes(1);
    });

    it('teams HDA (type - "marketHeader")', () => {
      spyOn(service as any, 'createMarketWithTypeMarketHeader');
      markets[0].outcomes = [{}];
      groupedMarket.type = 'marketHeader';
      service['getMarketsObg'](markets, groupedMarket, marketPeriod);
      expect(service['createMarketWithTypeMarketHeader']).toHaveBeenCalledTimes(1);
    });

    it('teams HDA (type - "teams")', () => {
      spyOn(service as any, 'createMarketWithTypeMarketHeader');
      markets[0].outcomes = [{}];
      groupedMarket.type = 'teams';
      service['getMarketsObg'](markets, groupedMarket, marketPeriod);
      expect(service['createMarketWithTypeMarketHeader']).toHaveBeenCalledTimes(1);
    });

    it('marketType "headerTeamName"', () => {
      service['getTeamName'] = () => 'teamA';
      groupedMarket.marketSort = {};
      groupedMarket.type = 'headerTeamName';
      service['getMarketsObg'](markets, groupedMarket, marketPeriod);
      expect(groupedMarket.name).toBe('Over/Under Goals teamA');
    });

    it('no markets', () => {
      markets = [{}];
      service['getMarketsObg'](markets, groupedMarket, marketPeriod);
      expect(service['allGroupedMarkets']).toEqual([]);
    });
  });

  describe('generateMarkets', () => {
    beforeEach(() => {
      spyOn(service as any, 'getMarketsObg');
    });

    it('market with periods', () => {
      service['generateMarkets']([], { periods: [{}, {}] } as any);
      expect(service['getMarketsObg']).toHaveBeenCalledTimes(2);
    });

    it('should set markets available', () => {
      (service['getMarketsObg'] as any).and.callFake(() => {
        service['allGroupedMarkets'] = [{}];
      });
      const groupedMarket: any = {};
      service['generateMarkets']([], groupedMarket);
      expect(groupedMarket.marketsAvailable).toBeTruthy();
    });
  });

  it('getDisplayOrder', () => {
    const markets: any[] = [
      { templateMarketName: 'a', displayOrder: 2 },
      { templateMarketName: 'b', displayOrder: 3 },
      { templateMarketName: 'c', displayOrder: 1 },
      {}
    ];
    expect(service['getDisplayOrder'](markets, ['a', 'b', 'c'])).toEqual(markets[2]);
  });

  it('updateMarketConfig', () => {
    spyOn(service as any, 'getMarketsObg');
    const marketPeriod: any = { markets: [{ id: 'market_id' }, {}] };
    service['updateMarketConfig'](marketPeriod, market, {} as any);
    expect(service['getMarketsObg']).toHaveBeenCalledTimes(1);
  });

  it('createGroupedMarketToMarketsNamesDictionary', () => {
    const groupedMarket: any = [
      { localeName: 'name1', periods: [{ marketsNames: ['marketA'] }] },
      { localeName: 'name2', marketsNames: ['marketB'] }
    ];
    service['createGroupedMarketToMarketsNamesDictionary'](groupedMarket);
    expect(service['groupedMarketToMarketsNamesDictionary']).toEqual({
      name1: ['marketA'], name2: ['marketB']
    });
  });
});
