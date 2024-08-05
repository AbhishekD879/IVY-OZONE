import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { PrivateMarketsService } from '@core/services/privateMarkets/private-markets.service';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UpdateEventService } from '@core/services/updateEvent/update-event.service';

@Component({
  selector: 'private-markets-tab',
  templateUrl: './private-markets-tab.html'
})
export class PrivateMarketsTabComponent implements OnInit, OnDestroy {
  maxElements: number = 3;
  isExpanded: boolean = true;
  events: ISportEvent[];

  private privateMarketsSubscription: Subscription;
  private onInitSubscription: Subscription;

  constructor(
    private privateMarketsService: PrivateMarketsService,
    private pubSubService: PubSubService,
    // eslint-disable-next-line
    private updateEventService: UpdateEventService // for events subscription (done in service init)
  ) {}

  ngOnInit(): void {
    this.onInitSubscription = this.privateMarketsService.markets()
      .subscribe((events: ISportEvent[]) => {
        this.events = events;
        this.privateMarketsService.subscribe(events);

        this.addEventListeners();
        this.checkVisibleEvents();
    });
  }

  addEventListeners(): void {
    this.pubSubService.subscribe('PrivateMarketsTabComponent', this.pubSubService.API.RELOAD_COMPONENTS, () => {
      this.reloadComponent();
    });

    this.pubSubService.subscribe('PrivateMarketsTabComponent', this.pubSubService.API.LIVE_SERVE_MS_UPDATE, () => {
      this.checkVisibleEvents();
    });

    this.pubSubService.subscribe('PrivateMarketsTabComponent', 'PRIVATE_MARKETS_TAB', () => this.loadEvents());
  }

  ngOnDestroy(): void {
    this.onInitSubscription && this.onInitSubscription.unsubscribe();
    this.privateMarketsSubscription && this.privateMarketsSubscription.unsubscribe();
    this.pubSubService.unsubscribe('PrivateMarketsTabComponent');
    this.privateMarketsService.unsubscribe(this.events);
  }

  reloadComponent(): void {
    this.ngOnDestroy();
    this.events = null;
    this.ngOnInit();
  }

  /**
   * Track by function
   * @param {number} index
   * @returns {string}
   */
  trackEventsByFn(index: number): number {
    return index;
  }

  /**
   * Track by function
   * @param {number} index
   * @returns {string}
   */
  trackMarketsByFn(index: number): number {
    return index;
  }

  /**
   * Track by function
   * @param {number} index
   * @returns {string}
   */
  trackOutcomesByFn(index: number): number {
    return index;
  }

  private loadEvents(): void {
    this.privateMarketsSubscription && this.privateMarketsSubscription.unsubscribe();

    this.privateMarketsSubscription = this.privateMarketsService.markets()
      .subscribe((pmEvents: ISportEvent[]) => {
        this.events = pmEvents;
        this.checkVisibleEvents();
    });
  }

  private checkVisibleEvents(): void {
    const isNoVisibleEvents = this.events && (this.events.length === 0 ||
      this.events[0].markets.every((market: IMarket) =>
        market.outcomes.every((outcome: IOutcome) =>
          Object.keys(outcome).includes('isDisplayed') && !outcome.isDisplayed
        )
      ));

    if (isNoVisibleEvents) {
      this.pubSubService.publish(this.pubSubService.API.HIDE_PRIVATE_MARKETS_TAB);
    }
  }
}
