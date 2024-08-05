import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subject } from 'rxjs';

import { PubSubService } from '@coreModule/services/communication/pubsub/pubsub.service';
import { PrivateMarketsService } from '@coreModule/services/privateMarkets/private-markets.service';
import { UserService } from '@core/services/user/user.service';
import { SessionService } from '@authModule/services/session/session.service';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { IMarket } from '@app/core/models/market.model';
import { IOutcome } from '@app/core/models/outcome.model';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'private-markets',
  templateUrl: './private-markets.component.html',
  styleUrls: ['./private-markets.component.scss']
})
export class PrivateMarketsComponent implements OnInit, OnDestroy {
  events: ISportEvent[] = [];
  maxElements: number = 3;
  isExpanded: boolean = true;
  private readonly title = 'PrivateMarketsComponent';

  private unsubscribe$: Subject<void> = new Subject<void>();

  constructor(
    private pubSubService: PubSubService,
    private userService: UserService,
    private privateMarketsService: PrivateMarketsService,
    private sessionService: SessionService
  ) { }

  ngOnInit(): void {
    this.sessionService.whenUserSession()
      .subscribe(() => this.loadPrivateMarkets(), err => console.error(err));

    this.pubSubService.subscribe(this.title, [this.pubSubService.API.PRIVATE_MARKETS_TAB, this.pubSubService.API.SUCCESSFUL_LOGIN], () => {
      this.loadPrivateMarkets();
    });

    this.pubSubService.subscribe(this.title, this.pubSubService.API.LIVE_SERVE_MS_UPDATE, () => {
      const isNoVisibleEvents = this.checkOutcomes();

      if (isNoVisibleEvents) {
        this.events = [];
      }
    });

    this.pubSubService.subscribe(this.title, this.pubSubService.API.SESSION_LOGOUT, () => {
      this.privateMarketsService.unsubscribe(this.events);
      this.events = [];
    });
  }

  ngOnDestroy(): void {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
    this.pubSubService.unsubscribe(this.title);
    this.privateMarketsService.unsubscribe(this.events);
  }

  /**
   * Limit the number of markets
   * @param {IMarket} market – The market for showing
   * @param {IOutcome[]} outcomes – Outcomes for slicing if they out of the limit
   * @returns {IOutcome[]} – The partial or full number of outcomes
   */
  limitTo(market: IMarket, outcomes: IOutcome[]): IOutcome[] {
    if (!market.allShown && this.maxElements) {
      return outcomes.slice(0, this.maxElements);
    }
    return outcomes;
  }

  /**
   * Defines how to track changes for iterable items
   * @param {number} i – Index of the item
   * @param {ISportEvent} event - An item for tracking changes
   * @returns {string} – Value for tracking
   */
  trackByEvents(i: number, event: ISportEvent): string {
    return `${event.id}_${event.categoryId}`;
  }

  /**
   * Defines how to track changes for iterable items
   * @param {number} i – Index of the item
   * @param {IMarket} market - An item for tracking changes
   * @returns {string} – Value for tracking
   */
  trackByMarkets(i: number, market: IMarket): string {
    return market.id;
  }

  /**
   * Defines how to track changes for iterable items
   * @param {number} i – Index of the item
   * @param {IOutcome} outcome - An item for tracking changes
   * @returns {string} – Value for tracking
   */
  trackByOutcomes(i: number, outcome: IOutcome): string {
    return outcome.id;
  }

  /**
   * Check the 'isDisplayed' property of outcomes
   * @returns {boolean} status
   */
  private checkOutcomes(): boolean {
    return this.events && this.events.length &&
      this.events[0].markets.every((market: IMarket) => {
        return market.outcomes.every((outcome: IOutcome) => {
          return outcome != null && (Object.hasOwnProperty.call(outcome, 'isDisplayed') && !outcome.isDisplayed);
        });
      });
  }

  /**
   * Receive private markets
   */
  private loadPrivateMarkets(): void {
    if (this.userService && this.userService.status) {
      this.privateMarketsService.markets().pipe(
        takeUntil(this.unsubscribe$)
      ).subscribe((events: ISportEvent[]) => {
          this.privateMarketsService.subscribe(events);
          this.events = events;
        });
    }
  }
}
