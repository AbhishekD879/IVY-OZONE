import { CorrectScoreService } from '@edp/components/markets/correctScore/correct-score.service';

describe('CorrectScoreService', () => {
  let service: CorrectScoreService;
  let scoreMarketService;
  let marketsGroupFactory;

  const outcome = {
    id: '111',
    prices: [{
      priceDec: 10.111
    }]
  };
  const market = {
    id: '555',
  } as any;
  const marketGroup = [market];
  const scoreMarketServiceTeams = [{name: 'Score Market TeamH'}, {name: 'Score Market TeamA'}];

  beforeEach(() => {
    scoreMarketService = {
      getMaxScoreValues: jasmine.createSpy(),
      getCombinedOutcome: jasmine.createSpy().and.returnValue(outcome),
      getTeams: jasmine.createSpy().and.returnValue(scoreMarketServiceTeams)
    };
    marketsGroupFactory = {
      getTeams: jasmine.createSpy().and.returnValue([])
    };

    service = new CorrectScoreService(scoreMarketService, marketsGroupFactory);
  });

  it('should create service', () => {
    expect(service).toBeDefined();
  });

  it('getMaxScoreValues', () => {
    service.getMaxScoreValues([]);
    expect(scoreMarketService.getMaxScoreValues).toHaveBeenCalled();
  });

  describe('getTeams', () => {
    it('should create teams by ScoreMarketService', () => {
      const result = service.getTeams(marketGroup);
      const expectResult = {
        teamH: { name: 'Score Market TeamH', score: 0 },
        teamA: { name: 'Score Market TeamA', score: 0 }
      };

      expect(scoreMarketService.getTeams).toHaveBeenCalledWith(marketGroup);
      expect(result).toEqual(expectResult);

      marketsGroupFactory.getTeams.and.returnValue([{
        name: undefined
      }]);
      expect(result).toEqual(expectResult);

      marketsGroupFactory.getTeams.and.returnValue([{
        name: 'Team A'
      }]);
      expect(result).toEqual(expectResult);
    });

    it('should create teams by marketsGroupFactory', () => {
      marketsGroupFactory.getTeams.and.returnValue([{
        name: 'Team A 5 - 1 Team B'
      }]);
      const result = service.getTeams(marketGroup);

      expect(scoreMarketService.getTeams).toHaveBeenCalledWith(marketGroup);
      expect(result).toEqual( {
        teamH: { name: 'Team A', score: 0 },
        teamA: { name: 'Team B', score: 0 }
      });
    });
  });

  it('should create teams by ScoreMarketService if teams by marketsGroupFactory are NOT valid', () => {
    marketsGroupFactory.getTeams.and.returnValue([{ name: 'team A 3' }]);
    scoreMarketService.getTeams.and.returnValue([{ name: 'Team a' }, { name: 'Team b' }]);
    // @ts-ignore
    const result = service.getTeams([ { id: 111 } ]);
    const expectResult = {
      teamH: { name: 'Team a', score: 0 },
      teamA: { name: 'Team b', score: 0 }
    };

    expect(result).toEqual(expectResult);
  });

  it('getMaxScoreValues', () => {
    const result = service.getCombinedOutcome({}, {}, {}, {});
    expect(scoreMarketService.getCombinedOutcome).toHaveBeenCalled();

    expect(result).toEqual({
      id: '111',
      prices: [{
        priceDec: '10.11'
      }]
    } as any);
  });

  it('getCombinedOutcome shoudl NOT transorm price when no price inside outcome', () => {
    const outcome2 = { id: '111', name: 'team A', prices: [] };

    scoreMarketService.getCombinedOutcome.and.returnValue(outcome2);
    const result = service.getCombinedOutcome({}, {}, {}, {});

    // @ts-ignore
    expect(result).toEqual(outcome2);
  });

  it('getCombinedOutcome shoudl NOT transorm price when no price property inside outcome', () => {
    const outcome2 = { id: '111', name: 'team A' };

    scoreMarketService.getCombinedOutcome.and.returnValue(outcome2);
    const result = service.getCombinedOutcome({}, {}, {}, {});

    // @ts-ignore
    expect(result).toEqual(outcome2);
  });
});
