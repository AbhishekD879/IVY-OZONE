import { IScoreType } from '@core/services/scoreParser/models/score-data.model';
import { SetsPointsScoreParser } from '@core/services/scoreParser/parsers/sets-points-score-parser';
// ignoring next test as there's an issue with coverage report which shows covered line as uncovered branch
/* istanbul ignore next */
export class SetsLegsScoreParser extends SetsPointsScoreParser {
  protected type: IScoreType = 'SetsLegs';
}
