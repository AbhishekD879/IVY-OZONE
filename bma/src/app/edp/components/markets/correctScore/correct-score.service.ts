import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { MarketsGroupService } from '@edp/services/marketsGroup/markets-group.service';
import { ITeamsScores, ITeams } from '@core/models/team.model';
import { IOutcome } from '@core/models/outcome.model';
import { IMarket } from '@core/models/market.model';
import { ScoreMarketService } from '@edp/services/scoreMarket/score-market.service';

@Injectable()
export class CorrectScoreService {
  constructor(
    private scoreMarketService: ScoreMarketService,
    private marketsGroupFactory: MarketsGroupService) {
  }

  /**
   * Find max available scores for teams.
   * @param {Array} outcomes
   * @returns {Object}
   */
  getMaxScoreValues(outcomes: IOutcome[]): ITeamsScores {
    return this.scoreMarketService.getMaxScoreValues(outcomes);
  }

  /**
   * Find team names.
   * @param marketGroup {Array}
   * @returns {Object}
   */
  getTeams(marketGroup: IMarket[]): ITeams {
    let teamsNamesString: string,
      names: string[];
    let teams = this.scoreMarketService.getTeams(marketGroup);
    const outcomes: IOutcome[] = this.marketsGroupFactory.getTeams(marketGroup);

    if (_.isArray(outcomes) && outcomes.length > 0) {
      teamsNamesString = outcomes[0] && _.isString(outcomes[0].name) &&
        outcomes[0].name.replace(/\(?(\d+)?\)?\s(\d+)\s?-\s?(\d+)\s\(?(\d+)?\)?/g, ' v ');
      names = _.isString(teamsNamesString) && teamsNamesString.split(' v ');

      if (_.isArray(names) && names.length > 1) {
        teams = [{ name: names[0] }, { name: names[1] }];
      }
    }

    return {
      teamH: { name: teams[0] && teams[0].name, score: 0 },
      teamA: { name: teams[1] && teams[1].name, score: 0 }
    };
  }

  /**
   * Find combined outcome by team scores rsult.
   * @param teams {Object}
   * @param outcomes {Array}
   * @returns {Object}
   */
  getCombinedOutcome(teams, outcomes, event, market): IOutcome {
    const combinedOutcome = this.scoreMarketService.getCombinedOutcome(teams, outcomes);

    if (_.has(combinedOutcome, 'prices') && combinedOutcome.prices.length) {
      combinedOutcome.prices[0].priceDec = Number(combinedOutcome.prices[0].priceDec).toFixed(2);
    }
    return combinedOutcome;
  }
}
