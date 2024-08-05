import { Component, Input } from '@angular/core';
import { IOutcome } from '@core/models/outcome.model';
import { IBetHistoryLeg } from '@app/betHistory/models/bet-history.model';
import TotePotPoolBet from '../../betModels/totePotPoolBetClass/TotePotPoolBetClass';

@Component({
  selector: 'tote-pot-pool-bet-card',
  templateUrl: './tote-pot-pool-bet-card.component.html'
})
export class TotePotPoolBetCardComponent {
  @Input() pool: TotePotPoolBet;
  @Input() isSportIconEnabled: boolean;

  /**
   * Get leg title
   * @param {Object} leg - pool leg object
   * @param {Number} index - leg index
   */
  getLegTitle(leg: IBetHistoryLeg, index: number): string {
    return `Leg ${index + 1} ${this.pool.getRaceTitle(leg)}`;
  }

  /**
   * Get outcome title
   * @param outcome - outcome entity
   * @returns {string} - outcome title
   */
  getOutcomeTitle(outcome: IOutcome): string {
    return outcome.isFavourite ? outcome.name : `${outcome.runnerNumber}. ${outcome.name}`;
  }

  /**
   * Track by function
   * @param {number} index
   * @param {IOutcome} outcome
   */
  trackByLeg(index: number, item: IBetHistoryLeg): string {
    return `${index}${item.eventId}${item.marketId}`;
  }

  /**
   * Track by function
   * @param {number} index
   * @param {IOutcome} outcome
   */
  trackByOutcome(index: number, outcome: IOutcome): string {
    return `${index}${outcome.id}`;
  }
}
