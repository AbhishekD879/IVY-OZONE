import { AbstractScoreParser } from '@core/services/scoreParser/parsers/abstract-score-parser';
import { IScoreData, IScoreType } from '@core/services/scoreParser/models/score-data.model';

export class SimpleScoreParser extends AbstractScoreParser {
  protected type: IScoreType = 'Simple';
  protected pattern: RegExp =
    /^\s*(.*?)\s+(\d+)-(\d+)\s+(.*?)\s*$/;

  protected matcher(matchArray: string[]): IScoreData {
    const [, teamA, scoreA, scoreB, teamB] = matchArray;

    return {
      home: {
        name: teamA,
        score: scoreA
      },
      away: {
        name: teamB,
        score: scoreB
      }
    };
  }
}
