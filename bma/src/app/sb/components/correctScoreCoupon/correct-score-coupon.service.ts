import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { ScoreMarketBaseService } from '@shared/services/scoreMarketBase/score-market-base.service';
import { StorageService } from '@core/services/storage/storage.service';
import { TimeService } from '@core/services/time/time.service';

import { ICSTeams, ITeamsScores, ICSEvent } from '@sb/components/correctScoreCoupon/correct-score-coupon.model';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { IOutcome } from '@core/models/outcome.model';

@Injectable({
  providedIn: 'root'
})
export class CorrectScoreCouponService {
  constructor(private scoreMarketBaseService: ScoreMarketBaseService,
              private timeService: TimeService,
              private storageService: StorageService) {}

  /**
   * Set Events Object
   * @param {ITypeSegment[]} couponEvents
   * @param {boolean} isUpdated
   */
  createCouponEvents(couponEvents: ITypeSegment[], isUpdated?: boolean): void {
    _.each(couponEvents, (coupon: ITypeSegment) => {
      _.each(coupon.events, (event: ICSEvent) => {
        const outcomes: IOutcome[] = event.markets[0].outcomes;
        this.createCouponEvent(event, outcomes, isUpdated);
      });
    });
  }

  /**
   * Create Coupon active event
   * @param {ICSEvent} event
   * @param {IOutcome[]} outcomes
   * @param {boolean} isUpdated
   */
  createCouponEvent(event: ICSEvent, outcomes: IOutcome[], isUpdated?: boolean): void {
    event.isDelay = false;
    event.time = this.timeService.getEventTime(`${new Date(event.startTime)}`);
    if (this.getBetData.length) {
      const outcomeArray = _.filter(outcomes, outcome => {
        return _.flatten(_.pluck(this.getBetData, 'id')).toString().includes(outcome.id);
      });
      const outcomeObj =  outcomeArray.length && outcomeArray[0];
      if (outcomeObj) {
        const scores =  _.compact(outcomeObj.outcomeMeaningScores.split(',')).map(Number);
        event.teams = this.getTeams(event.name, outcomes, scores);
        event.isActive = true;
        event.combinedOutcomes = outcomeObj;
      } else {
        this.createEvent(event, outcomes, isUpdated);
      }
    } else {
      this.createEvent(event, outcomes, isUpdated);
    }
  }

  /**
   * Find combined outcome by team scores rsult.
   * @param {ICSTeams} teams
   * @param {IOutcome[]} outcomes
   * @returns {Object}
   */
  getCombinedOutcome(teams: ICSTeams, outcomes: IOutcome[]): IOutcome {
    const teamScores = `${teams.teamH.score.toString() + teams.teamA.score.toString()}`;
    const combinedOutcomes: IOutcome[] = _.filter(outcomes, (outcome: IOutcome) => {
      const outcomeScores = outcome.outcomeMeaningScores.replace(/,/g, '');
      return outcomeScores === teamScores;
    });
    return combinedOutcomes && combinedOutcomes[0] || { outcomeStatusCode: 'S' } as IOutcome;
  }

  /**
   * Find available scores for teams.
   * @param {Array} outcomes
   * @returns {Object}
   */
  private getScoreValues(outcomes: IOutcome[]): ITeamsScores {
    return this.scoreMarketBaseService.getMaxScoreValues(outcomes);
  }

  /**
   * Create team object.
   * @param {string[]} name
   * @param {IOutcome[]} outcomes
   * @param {string[]} scoresArray
   * @returns {Object}
   */
  private getTeams(name: string, outcomes: IOutcome[], scoresArray: number[] = []): ICSTeams {
    const teams: string[] = name.split(' v ');
    const scores: number[] = scoresArray.length ? scoresArray : [0, 0];
    return {
      teamH: { name: teams[0], score: scores[0], scores: this.getScoreValues(outcomes).teamH },
      teamA: { name: teams[1], score: scores[1], scores: this.getScoreValues(outcomes).teamA }
    };
  }

  /**
   * Create Coupon default event
   * @param {ICSEvent} event
   * @param {IOutcome[]} outcomes
   * @param {boolean} isUpdated
   */
  private createEvent(event: ICSEvent, outcomes: IOutcome[], isUpdated: boolean = false): void {
    event.isActive = false;
    if (!isUpdated) {
      event.teams = this.getTeams(event.name, outcomes);
      event.combinedOutcomes = this.getCombinedOutcome(event.teams, outcomes);
    }
  }

  /**
   * Get Bets from Storage
   * @returns {IBetSelection[]}
   */
  private get getBetData(): IBetSelection[] {
    return <IBetSelection[]>this.storageService.get('betSelections') || [];
  }
  private set getBetData(value:IBetSelection[]){}
}
