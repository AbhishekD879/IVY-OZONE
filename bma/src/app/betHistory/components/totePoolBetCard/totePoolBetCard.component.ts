import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';
import TotePoolBet from '@app/betHistory/betModels/totePoolBet/tote-pool-bet.class';
import { IBetHistoryLeg } from '@app/betHistory/models/bet-history.model';
import { ToteService } from '@app/tote/services/mainTote/main-tote.service';

@Component({
  selector: 'tote-pool-bet-card',
  templateUrl: './totePoolBetCard.component.html',
  styleUrls: ['../betLegItem/bet-leg-item.component.scss']
})
export class TotePoolBetCardComponent {
  @Input() pool: TotePoolBet;
  @Input() isSportIconEnabled: boolean;

  constructor(
    private router: Router,
    private toteService: ToteService
  ) { }

  /**
   * Get outcome title
   * @param outcome - outcome entity
   * @param {Number} - @index index in array
   * @returns {string} - outcome title
   */
  getOutcomeTitle(outcome: IOutcome, index: number): string {
    if (!this.pool) {
      return '';
    }
    let outcomeTitle: string,
      showRunnerNumber: boolean;

    /**
     * If order of bet selection is matter than display place of runner,
     * in other case runner number should be displayed
     */
    if (this.pool.isOrderedBet) {
      outcomeTitle = `${index + 1}. ${outcome.name}`;
    } else {
      /**
       * Display runner number only for bets with more than 1 selections
       * @type {boolean}
       */
      showRunnerNumber = this.pool.poolOutcomes.length > 1 && !outcome.isFavourite;
      outcomeTitle = showRunnerNumber ? `${outcome.runnerNumber}. ${outcome.name}` : outcome.name;
    }

    return outcomeTitle;
  }

  /**
   * Check if event is live
   * @param leg
   */
  isEventLive(leg: IBetHistoryLeg): boolean {
    if (!leg || !leg.eventEntity) {
      return false;
    }
    const eventEntity: ISportEvent = leg.eventEntity,
      isEventFinished: boolean = eventEntity.isFinished || eventEntity.isResulted,
      isStartedAndNotFinished: boolean = eventEntity.isStarted && !isEventFinished;
    return eventEntity.eventIsLive || isStartedAndNotFinished;
  }

  /**
   * Track by function
   * @param {outcome} IOutcome
   */
  trackByFn(index: number, outcome: IOutcome): string {
    return `${index}_${outcome.id}`;
  }

  /**
   * Handle click on tote events
   * (navigation to old resulted ob events is impossible so skipped)
   *
   * @param pool
   */
  goToEvent(pool: TotePoolBet): void {
    const poolLeg: IBetHistoryLeg = pool && pool.leg && pool.leg[0];

    if (!poolLeg || !(poolLeg.eventId || poolLeg.toteEventId)) { return; }

    this.toteService.getToteLink(
      poolLeg.eventId,
      poolLeg.toteEventId,
      pool.isUkToteBet
    ).subscribe((eventUrl: string) => {
      if (eventUrl) {
        this.router.navigate([eventUrl]);
      } else {
        console.warn(`No OpenBet event found for "${poolLeg.eventId}", skip redirection.`); // TODO NewRelic instead?
      }
    });
  }
}
