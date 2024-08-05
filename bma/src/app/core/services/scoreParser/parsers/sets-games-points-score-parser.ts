import { AbstractScoreParser } from '@core/services/scoreParser/parsers/abstract-score-parser';
import { IScoreData, IScoreType } from '@core/services/scoreParser/models/score-data.model';

export class SetsGamesPointsScoreParser extends AbstractScoreParser {
  protected type: IScoreType = 'SetsGamesPoints';
  protected pattern: RegExp =
    /^\s*(\*?)(.*?)\s*(\*?)\s+\((\d+)\)\s+(\d+)\s+(\w+)-(\w+)\s+(\d+)\s+\((\d+)\)\s+(\*?)\s*(.*?)(\*?)\s*$/;

  protected matcher(matchArray: string[]): IScoreData {
    const [, isServingALeft, teamA, isServingARight, scoreA,
      gameA, pointsA, pointsB, gameB, scoreB, isServingBLeft, teamB, isServingBRight] = matchArray;

    return {
      home: {
        name: teamA && teamA.replace(/\*/g, '').trim(),
        currentPoints: pointsA,
        score: scoreA,
        periodScore: gameA,
        isServing: isServingALeft === '*' || isServingARight === '*'
      },
      away: {
        name: teamB && teamB.replace(/\*/g, '').trim(),
        currentPoints: pointsB,
        periodScore: gameB,
        score: scoreB,
        isServing: isServingBLeft === '*' || isServingBRight === '*'
      }
    };
  }
}
