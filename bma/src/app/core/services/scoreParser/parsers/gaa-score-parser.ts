import { AbstractScoreParser } from '@core/services/scoreParser/parsers/abstract-score-parser';
import { IScoreData, IScoreType } from '@core/services/scoreParser/models/score-data.model';

export class GaaScoreParser extends AbstractScoreParser {
  private readonly scoreParser: string = '\\s+(\\d+-\\d+)-(\\d+-\\d+)\\s+';

  protected readonly scorePattern: RegExp = new RegExp(this.scoreParser, 'g');
  protected type: IScoreType = 'GAA';
  protected pattern: RegExp = new RegExp(`^\\s*(.*?)${this.scoreParser}(.*?)\\s*$`);

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
