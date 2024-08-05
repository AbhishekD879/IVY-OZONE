import { ScoreMarketService } from '@edp/services/scoreMarket/score-market.service';

describe('score-market service', () => {
  let scoreMarket: ScoreMarketService;
  let marketsGroupService;

  beforeEach(() => {
    marketsGroupService = {
      getTeams: jasmine.createSpy('getTeams').and.callFake(v => v),
      removeScores: jasmine.createSpy('removeScores').and.callFake(v => v)
    };
    scoreMarket = new ScoreMarketService(marketsGroupService);
  });

  it('getTeams', () => {
    const teams: any[] = [{}, { name: 'team1', outcomeMeaningMinorCode: 1 }];
    expect(scoreMarket.getTeams(teams)).toEqual([
      { name: undefined, outcomeMeaningMinorCode: undefined },
      { name: 'team1', outcomeMeaningMinorCode: 1 }
    ]);
    expect(marketsGroupService.getTeams).toHaveBeenCalledTimes(1);
    expect(marketsGroupService.removeScores).toHaveBeenCalledTimes(1);
  });

  describe('getCombinedOutcome', () => {
    it('home wins', () => {
      const teams: any = { teamH: { score: 2, name: 'home' }, teamA: { score: 1, name: 'away' } };
      const outcomes: any[] = [{ name: 'home 2-1' }];
      expect(scoreMarket.getCombinedOutcome(teams, outcomes)).toBe(outcomes[0]);
    });

    it('away wins', () => {
      const teams: any = { teamH: { score: 1, name: 'home' }, teamA: { score: 2, name: 'away' } };
      const outcomes: any[] = [{ name: 'away 2-1' }];
      expect(scoreMarket.getCombinedOutcome(teams, outcomes)).toBe(outcomes[0]);
    });

    it('draw (no names)', () => {
      const teams: any = { teamH: { score: 1 }, teamA: { score: 1 } };
      const outcomes: any[] = [{ name: '1-1' }];
      expect(scoreMarket.getCombinedOutcome(teams, outcomes)).toBe(outcomes[0]);
    });
  });
});
