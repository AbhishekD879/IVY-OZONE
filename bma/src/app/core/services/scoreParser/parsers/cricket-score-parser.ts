import { AbstractScoreParser } from '@core/services/scoreParser/parsers/abstract-score-parser';
import { IScoreData, IScoreType } from '@core/services/scoreParser/models/score-data.model';

export class CricketScoreParser extends AbstractScoreParser {
  private readonly teamVS: string = '(\\s+v\\s+)';
  private readonly teamName: string = '\\s*(.*?)\\s?';
  private readonly scoreParser: string = '(\\s+\\d+(?:\\/\\d+d?)?)?(\\s+\\d+(?:\\/\\d+d?)?)?(?!st)(?!nd)(?!rd)(?!th)';
  private readonly teamSide: string = `${this.teamName}${this.scoreParser}`;

  protected readonly scorePattern: RegExp = new RegExp(this.scoreParser, 'gi');
  protected pattern: RegExp = new RegExp(`${this.teamSide}${this.teamVS}${this.teamSide}\\s*$`, 'i');
  protected type: IScoreType = 'BoxScore';

  protected matcher(matchArray: string[]): IScoreData {
    matchArray = matchArray.map((matchItem: string) => matchItem && matchItem.trim() || undefined);

    const [, homeName, home1inn, home2inn, ,
      awayName, away1inn, away2inn] = matchArray;

    if (!home1inn && !away1inn) {
      // no scores captured for at least one innings
      return;
    }

    return {
      home: {
        name: homeName,
        score: this.composeScore(home1inn, home2inn),
        inn1: home1inn,
        inn2: home2inn,
      },
      away: {
        name: awayName,
        score: this.composeScore(away1inn, away2inn),
        inn1: away1inn,
        inn2: away2inn,
      }
    };
  }

  private composeScore(inn1: string, inn2: string): string {
    return inn2
      ? `${inn1} ${inn2}`
      : inn1;
  }
}
