import { ScoreMarketBaseService } from '@shared/services/scoreMarketBase/score-market-base.service';
import { IOutcome } from '@core/models/outcome.model';

describe('ScoreMarketBaseService', () => {

  let scoreMarket: ScoreMarketBaseService;
  const outcomes: IOutcome[] = [];
  beforeEach(() => {
    scoreMarket = new ScoreMarketBaseService();
  });

  it('should return an object containing TeamA array and TeamH array', () => {
    const result = scoreMarket.getMaxScoreValues(outcomes);

    expect(result).toEqual(jasmine.objectContaining({
      teamA: [0],
      teamH: [0]
    }));
  });

  it('it should get max score values', () => {
    const outcomesWithScores = [{
      outcomeMeaningScores: '0,1,'
    }, {
      outcomeMeaningScores: '2,3,'
    }, {
      outcomeMeaningScores: '4,3,'
    }];
    const result = scoreMarket.getMaxScoreValues(outcomesWithScores as IOutcome[]);

    expect(result).toEqual(jasmine.objectContaining({
      teamA: [0, 1, 3],
      teamH: [0, 2, 4]
    }));
  });

  it('should sort numbers based on index', () => {
    const outcomesWithScores = [{
      outcomeMeaningScores: '0,1,'
    }, {
      outcomeMeaningScores: '2,3,'
    }];
    const resultAway = scoreMarket['getNumbers'](outcomesWithScores as IOutcome[], 1);
    const resultHome = scoreMarket['getNumbers'](outcomesWithScores as IOutcome[], 0);

    expect(resultAway).toEqual([1, 3]);
    expect(resultHome).toEqual([0, 2]);
  });
});
