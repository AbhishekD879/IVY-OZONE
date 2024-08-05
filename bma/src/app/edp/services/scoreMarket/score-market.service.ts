import { Injectable } from '@angular/core';

import { ScoreMarketBaseService } from '@shared/services/scoreMarketBase/score-market-base.service';
import { MarketsGroupService } from '../marketsGroup/markets-group.service';
import { ITeams } from '@core/models/team.model';
import { IOutcome } from '@core/models/outcome.model';
import { IMarket } from '@core/models/market.model';
import * as _ from 'underscore';

@Injectable()
export class ScoreMarketService extends ScoreMarketBaseService {
  constructor(
    private marketsGroupService: MarketsGroupService
  ) {
    super();
  }

  /**
   * getCombinedOutcome()
   * @param {ITeams} teams
   * @param {IOutcome} outcomes
   * @returns {IOutcome}
   */
  getCombinedOutcome(teams: ITeams, outcomes: IOutcome[]): IOutcome {
    let outcomeName;

    if (teams.teamH.score > teams.teamA.score) {
      outcomeName = `${teams.teamH.name} ${teams.teamH.score}-${teams.teamA.score}`;
    } else if (teams.teamH.score < teams.teamA.score) {
      outcomeName = `${teams.teamA.name} ${teams.teamA.score}-${teams.teamH.score}`;
    } else {
      outcomeName = `Draw ${teams.teamH.score}-${teams.teamA.score}`;
    }

    const score = `${teams.teamH.score}-${teams.teamA.score}`,
      areTeamsDefined = !!(teams.teamA.name && teams.teamH.name);

    return areTeamsDefined ? this.getOutcomeByName(outcomes, outcomeName) : this.getOutcomeByScore(outcomes, score);
  }

  /**
   * getTeams()
   * @param {IMarket[]} markets
   * @returns {any[]}
   */
  getTeams(markets: IMarket[]): any[] {
    return _.map(this.marketsGroupService.getTeams(markets), outcome => ({
      name: outcome && outcome.name && this.marketsGroupService.removeScores(outcome.name),
      outcomeMeaningMinorCode: outcome && outcome.outcomeMeaningMinorCode
    }));
  }

  private getOutcomeByName(outcomes: IOutcome[], outcomeName: string): IOutcome {
    return _.findWhere(outcomes, { name: outcomeName });
  }

  private getOutcomeByScore(outcomes: IOutcome[], score: string): IOutcome {
    return _.find(outcomes, outcome => {
      return (outcome && _.isString(outcome.name)) && outcome.name.replace(/ /g, '').indexOf(score) >= 0;
    });
  }
}
