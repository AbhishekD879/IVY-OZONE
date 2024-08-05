import { AbstractScoreParser } from '@core/services/scoreParser/parsers/abstract-score-parser';
import { IScoreData, IScoreType } from '@core/services/scoreParser/models/score-data.model';

export class SetsPointsScoreParser extends AbstractScoreParser {
  protected type: IScoreType = 'SetsPoints';
  protected pattern: RegExp =
    /^\s*(\*?)(.*?)\s*(\*?)\s+\((\d+)\)\s+(\d+)-(\d+)\s+\((\d+)\)\s+(\*?)\s*(.*?)(\*?)\s*$/;

  protected matcher(matchArray: string[]): IScoreData {
    const [, isServingALeft, teamA, isServingARight, scoreA, pointsA, pointsB, scoreB, isServingBLeft, teamB, isServingBRight] = matchArray;

    return {
      home: {
        name: teamA && teamA.replace(/\*/g, '').trim(),
        currentPoints: pointsA,
        score: scoreA,
        isServing: isServingALeft === '*' || isServingARight === '*'
      },
      away: {
        name: teamB && teamB.replace(/\*/g, '').trim(),
        currentPoints: pointsB,
        score: scoreB,
        isServing: isServingBLeft === '*' || isServingBRight === '*'
      }
    };
  }
}
