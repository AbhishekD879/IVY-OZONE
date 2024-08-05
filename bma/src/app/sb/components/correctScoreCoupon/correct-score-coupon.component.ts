import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import * as _ from 'underscore';

import { CorrectScoreCouponService } from '@sb/components/correctScoreCoupon/correct-score-coupon.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

import { ICSEvent } from '@sb/components/correctScoreCoupon/correct-score-coupon.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { ISportEvent } from '@app/core/models/sport-event.model';

@Component({
  selector: 'correct-score-coupon',
  templateUrl: 'correct-score-coupon.component.html',
  styleUrls: ['correct-score-coupon.component.scss']
})
export class CorrectScoreCouponComponent implements OnInit, OnDestroy {
  @Input() couponEvents: ITypeSegment[] = [];

  headers: string[] = ['home', 'away', ''];

  private priceDelay: number = 250; // Show Price with current delay

  constructor(private correctScoreCouponService: CorrectScoreCouponService,
              private pubsubService: PubSubService) {}

  ngOnInit(): void {
    this.correctScoreCouponService.createCouponEvents(this.couponEvents, false);

    this.pubsubService.subscribe('CorrectScoreCoupon', this.pubsubService.API.BETSLIP_SELECTIONS_UPDATE, () => {
      setTimeout(() => this.correctScoreCouponService.createCouponEvents(this.couponEvents, true));
    });
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe('CorrectScoreCoupon');
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @param {ICSEvent} event
   * @return {string}
   */
  trackById(index: number, event: ICSEvent): string | any {
    return event.id ? `${index}${event.id}` : index.toString();
  }

  /**
   * Set outcome based on scores
   * @param {number} value
   * @param {string} team
   * @param {ICSEvent} event
   * @param {boolean} isCount
   */
  onScoreChange(value: number, team: string, event: ICSEvent, isCount: boolean = false): void {
    if (value && team && !event.isDelay) {
      const score = isCount ? event.teams[team].score + value : Number(value);
      if (score < event.teams[team].scores.length && score >= 0) {
        event.teams[team].score = score;
        event.isDelay = true;
        setTimeout(() => {
          event.isDelay = false;
          event.combinedOutcomes = this.correctScoreCouponService.getCombinedOutcome(event.teams, event.markets[0].outcomes);
        }, this.priceDelay);
      }
    }
  }

  /**
   * Check Disabled State
   * @param {ICSEvent} event
   * @param {string} team
   * @param {boolean} isTop
   * @returns {boolean}
   */
  isDisabled(event: ICSEvent, team: string, isTop: boolean = true): boolean {
    if (event.isActive) {
      return true;
    } else if (isTop) {
      return event.teams[team].score === event.teams[team].scores.length - 1;
    }
    return event.teams[team].score === 0;
  }

  /**
   * Check Hidden State
   * @returns {Boolean}
   */
  isHide(event: ICSEvent): boolean {
    const outcome = event.combinedOutcomes;
    return !(_.has(outcome, 'prices') && outcome.prices.length) || outcome.prices[0].isDisplayed === false ||
      outcome.outcomeStatusCode === 'S' || this.isSuspended(event);
  }

  /**
   * Check Arrow Hidden State
   * @returns {Boolean}
   */
  isArrowHide(event: ICSEvent | ISportEvent): boolean {
    return this.isSuspended(event) || event.isActive;
  }

  /**
   * Check Suspended State
   * @returns {Boolean}
   */
  isSuspended(event: ICSEvent | ISportEvent): boolean {
   return event.eventStatusCode === 'S' || event.markets[0].marketStatusCode === 'S';
  }
}
