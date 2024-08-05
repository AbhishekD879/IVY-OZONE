import { Injectable } from '@angular/core';

import { ITeamsScores } from '@core/models/team.model';
import { IOutcome } from '@core/models/outcome.model';
import * as _ from 'underscore';

@Injectable()
export class ScoreMarketBaseService {

  /**
   * getMaxScoreValues()
   * @param {IOutcome[]} outcomes
   * @returns {Object}
   */
  getMaxScoreValues(outcomes: IOutcome[]): ITeamsScores {
    const homeScores = this.getNumbers(outcomes, 0);
    const awayScores = this.getNumbers(outcomes, 1);

    // fix when no outcomes with 0 count, we need to start counter from 0 to handle up/down score switch
    if (homeScores.indexOf(0) === -1) { homeScores.unshift(0); }
    if (awayScores.indexOf(0) === -1) { awayScores.unshift(0); }

    return {
      teamA: awayScores,
      teamH: homeScores
    };
  }

  /**
   * getNumbers()
   * @param {IOutcome[]} outcomesList
   * @param {number} index
   * @returns {number[]}
   */
  private getNumbers(outcomesList: IOutcome[], index: number): number[] {
    return _.uniq(_.map(outcomesList, outcome => {
      return Number(outcome.outcomeMeaningScores.split(',')[index]);
    }).sort((a: number, b: number) => a > b ? 1 : -1), true);
  }
}
