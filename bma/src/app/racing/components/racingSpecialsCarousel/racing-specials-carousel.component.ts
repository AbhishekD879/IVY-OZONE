import { Component, Input, OnInit, OnDestroy, EventEmitter, Output } from '@angular/core';
import { Subscription, from } from 'rxjs';
import { map } from 'rxjs/operators';
import * as _ from 'underscore';

import { RacingSpecialsCarouselService } from '@racing/components/racingSpecialsCarousel/racing-specials-carousel.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { ISystemConfig } from '@core/services/cms/models';

@Component({
  selector: 'racing-specials-carousel',
  styleUrls: ['./racing-specials-carousel.component.scss'],
  templateUrl: 'racing-specials-carousel.component.html'
})
export class RacingSpecialsCarouselComponent implements OnInit, OnDestroy {
  @Input() eventId: number;
  @Output() readonly eventsLoaded: EventEmitter<void> = new EventEmitter();

  carouselName: string = 'racing-specials-carousel';
  items: ISportEvent[] = [];
  isSingleSlide: boolean = false;
  outcomesLength: number;
  label: string = 'Specials';
  readonly tag = 'racingSpecialsCarouselComponent';

  private racingSpecialsCarouselSubscription: Subscription;

  constructor(
    private cmsService: CmsService,
    private racingSpecialsCarouselService: RacingSpecialsCarouselService,
    private pubSubService: PubSubService) {}

  ngOnInit(): void {
    this.cmsService.getSystemConfig()
      .subscribe((cmsConfig: ISystemConfig) => {
        const config: { enable: boolean, label: string } = cmsConfig.RacingSpecialsCarousel || { enable: false };

        if (!config.enable) {
          this.eventsLoaded.emit();
          return false;
        }
        this.label = config.label || this.label;
        this.initData();
        return true;
      }, (error) => {
        this.eventsLoaded.emit();
        console.warn(error);
      });
  }

  ngOnDestroy(): void {
    // unSubscribe LS Updates via WS
    if (this.items.length) {
      this.racingSpecialsCarouselService.clearCache(this.eventId);
      // unSubscription from liveServe PUSH updates
      this.racingSpecialsCarouselService.unSubscribeForUpdates();
      this.pubSubService.unsubscribe(this.tag);
    }

    this.racingSpecialsCarouselSubscription && this.racingSpecialsCarouselSubscription.unsubscribe();
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @param {ISportEvent} event
   * @return {string}
   */
  trackById(index: number, event: ISportEvent): string {
    return event.id ? `${index}${event.id}` : index.toString();
  }

  /**
   * Order events, outcomes, markets
   * @param {(ISportEvent | IMarket | IOutcome)[]} entity
   * @returns {(ISportEvent | IMarket | IOutcome)[]}
   */
  orderEntity(entity: (ISportEvent | IMarket | IOutcome)[]): (ISportEvent | IMarket | IOutcome)[] {
    return this.racingSpecialsCarouselService.orderEvents(entity);
  }

  /**
   * @param {object} outcomeEntity
   * @return {boolean}
   */
  isFavourite(outcomeEntity: IOutcome): boolean {
    return +outcomeEntity.outcomeMeaningMinorCode > 0 ||
      outcomeEntity.name.toLowerCase() === 'unnamed favourite' ||
      outcomeEntity.name.toLowerCase() === 'unnamed 2nd favourite';
  }

  private initData(): void {
    this.racingSpecialsCarouselSubscription = from(this.racingSpecialsCarouselService.getEvents(this.eventId))
      .pipe(map((races: ISportEvent[]) => {
        this.items = this.filterEvents(races);
        this.setOutcomesLength(this.items);

        if (this.items.length) {
          // Subscription from liveServe PUSH updates
          this.racingSpecialsCarouselService.subscribeForUpdates(this.items);
        }
      }))
      .subscribe(
        () => {},
        () => {
          this.items = [];
        },
        () => {
          this.eventsLoaded.emit();
        }
      );

    this.pubSubService.subscribe(
        this.tag,
        [this.pubSubService.API.DELETE_EVENT_FROM_CACHE, this.pubSubService.API.DELETE_MARKET_FROM_CACHE],
        (eventId: number) => {
          this.items = this.filterEvents(_.filter(this.items, item => item.id !== eventId));
          this.setOutcomesLength(this.items);
        });

    this.pubSubService.subscribe(this.tag, this.pubSubService.API.DELETE_SELECTION_FROMCACHE, () => {
      this.setOutcomesLength(this.items);
    });
  }

  private setOutcomesLength(events: ISportEvent[]): void {
    const markets = events && _.flatten(_.pluck(this.filterEvents(events), 'markets'));
    const outcomes = _.flatten(_.pluck(markets, 'outcomes'));
    this.outcomesLength = outcomes.length;
    this.isSingleSlide = outcomes.length === 1;
  }

  private filterEvents(events: ISportEvent[]): ISportEvent[] {
    return _.filter(events, (event: ISportEvent) => {
      return !event.isFinished || !event.isResulted;
    });
  }
}

