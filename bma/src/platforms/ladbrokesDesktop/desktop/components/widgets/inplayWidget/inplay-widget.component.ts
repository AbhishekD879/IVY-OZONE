import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import * as _ from 'underscore';
import { Router } from '@angular/router';

import { InplayHelperService } from '@ladbrokesDesktop/inPlay/services/inPlayHelper/inplay-helper.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { IRequestConfig } from '@inPlayLiveStream/models/request-config.model';
import { UserService } from '@core/services/user/user.service';
import { StorageService } from '@core/services/storage/storage.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'inplay-widget',
  templateUrl: './inplay-widget.component.html',
  styleUrls: ['./inplay-widget.component.scss']
})
export class InplayWidgetComponent implements OnInit, OnDestroy {
  @Input() categoryId: number;
  @Input() sportName: string;

  isHovered: boolean;
  pending: boolean = true;
  events: ISportEvent[] = [];
  widgetTitle: string = 'in-play';
  widgetMoreLink: string = '/in-play';
  widgetMoreTitle: string = 'View All In-Play Events';
  carouselName: string = 'inplay-widget-carousel';

  private maxCount = 10;
  private requestConfig: IRequestConfig = {
    requestParams: {
      topLevelType: 'LIVE_EVENT'
    },
    socket: {
      sport: {
        emit: 'GET_SPORT',
        on(data) {
          return `IN_PLAY_SPORTS::${data.categoryId}::LIVE_EVENT`;
        }
      },
      competition: {
        emit: 'GET_TYPE',
        on(data) {
          return `IN_PLAY_SPORT_TYPE::${data.categoryId}::LIVE_EVENT::${data.typeId}`;
        }
      }
    },
    cachePrefix: 'inPlayWidget',
    limit: this.maxCount
  };
  private isFirstTimeCollapsed = false;
  private readonly syncName = 'inPlayWidget';
  private dataSubscription: Subscription;

  constructor(
    private inplayHelperService: InplayHelperService,
    private routingHelperService: RoutingHelperService,
    private sportEventHelperService: SportEventHelperService,
    private pubSubService: PubSubService,
    private router: Router,
    private carouselService: CarouselService,
    private storageService: StorageService,
    private userService: UserService
  ) { }

  ngOnInit(): void {
    this.dataSubscription = this.inplayHelperService.getData(this.categoryId, this.sportName, this.requestConfig)
      .subscribe((events: ISportEvent[]) => {
        this.events = [...events];
        this.pending = events.length === 0;
        this.widgetMoreLink = events.length > 1 ? `/in-play/${this.sportName}` : '/in-play';
        this.checkWidgetVisibility(!_.isEmpty(this.events));
      }, (error: string) => {
        console.warn(error);
      });

    this.pubSubService.subscribe(this.syncName, this.pubSubService.API.DELETE_EVENT_FROM_CACHE, eventId => {
      const eventIndex = this.events.findIndex((event: ISportEvent) => Number(event.id) === Number(eventId));

      if (eventIndex >= 0) {
        this.events.splice(eventIndex, 1);
        this.inplayHelperService.unsubscribeForLiveUpdates([{ id: eventId } as ISportEvent]);

        if (this.events.length === 0) {
          this.checkWidgetVisibility(false);
        }
      }
    });

    this.pubSubService.subscribe(this.syncName, this.pubSubService.API.RELOAD_IN_PLAY, () => {
      this.ngOnDestroy();
      this.ngOnInit();
    });
  }

  ngOnDestroy(): void {
    this.dataSubscription && this.dataSubscription.unsubscribe();
    this.pubSubService.unsubscribe(this.syncName);
    this.events = [];
  }

  trackById(index: number, event: ISportEvent): number {
    return event.id;
  }

  /**
   * Check if event is outright
   * @param event
   * @returns {boolean}
   */
  isOutrightEvent(event: ISportEvent): boolean {
    return this.sportEventHelperService.isOutrightEvent(event);
  }

  /**
   * Go to next slide
   */
  prevSlide(): void {
    this.carouselService.get(this.carouselName).previous();
    this.inplayHelperService.sendGTM('navigate left', this.sportName);
  }

  /**
   * Go to previous slide
   */
  nextSlide(): void {
    this.carouselService.get(this.carouselName).next();
    this.inplayHelperService.sendGTM('navigate right', this.sportName);
  }

  /**
   * send GTM tracking, collapse accordion
   */
  sendCollapseGTM(): void {
    if (this.isFirstTimeCollapsed) {
      return;
    }
    this.inplayHelperService.sendGTM('collapse', this.sportName);
    this.isFirstTimeCollapsed = true;
  }

  /**
   * send GTM tracking, view all
   */
  sendViewAllGTM(): void {
    this.events.length <= 1 ? this.storageService.remove(`inPlay-${this.userService.username}`)
      : this.storageService.set(`inPlay-${this.userService.username}`, this.sportName);
    this.inplayHelperService.sendGTM('view all', this.sportName);
  }

  /**
   * Check if previous action is available. Needs to show/hide previous action arrow.
   * @returns {boolean}
   */
  isPrevActionAvailable(): boolean {
    return this.isFirstSlide();
  }

  /**
   * Check if next slide action is available. Needs to show/hide next action arrow.
   * @returns {boolean}
   */
  isNextActionAvailable(): boolean {
    return !this.isLastSlide();
  }

  /**
   * Checking if current slide is last
   * @returns {boolean}
   */
  isLastSlide(): boolean {
    const carousel = this.carouselService.get(this.carouselName);
    return carousel.currentSlide === (carousel.slidesCount - 1);
  }

  /**
   * Checking if current slide is first
   * @returns {boolean}
   */
  isFirstSlide(): boolean {
    const carousel = this.carouselService.get(this.carouselName);
    return carousel.currentSlide !== 0;
  }

  /**
   * Check if only one event is present
   * @returns {boolean}
   */
  isSingleEvent(): boolean {
    return this.events.length === 1;
  }

  /**
   * Check if Cashout is enabled for event
   * @param event
   * @returns {*}
   */
  isCashOutEnabled(event: ISportEvent): boolean {
    return this.sportEventHelperService.isCashOutEnabled(event);
  }

  /**
   * @param event {object} event entity
   */
  goToEDP(event: ISportEvent): void {
    const EDPpath = this.routingHelperService.formEdpUrl(event);
    this.router.navigate([EDPpath]);
  }

  /**
   * Check InPlay Widget Visibility
   * @param {Boolean} isData
   * @private
   */
  private checkWidgetVisibility(isData: boolean): void {
    this.pubSubService.publish(this.pubSubService.API.WIDGET_VISIBILITY, { inPlay: isData });
  }
}
