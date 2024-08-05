import { Component, OnInit, OnDestroy, Input, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription, from } from 'rxjs';

import { ISportEvent } from '@core/models/sport-event.model';
import { ExtraPlaceService } from '@core/services/racing/extraPlace/extra-place.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { ITrackEvent } from '@core/services/gtm/models';
import { LocaleService } from '@core/services/locale/locale.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { TemplateService } from '@app/shared/services/template/template.service';
import { IMarket } from '@app/core/models/market.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'extra-place-home-module',
  templateUrl: 'extra-place-home.component.html',
  styleUrls: ['extra-place-home.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ExtraPlaceHomeComponent implements OnInit, OnDestroy {
  @Input() limit: number;

  events: ISportEvent[] = [];
  gtmObject: ITrackEvent;
  subscribedChannelsId: string = '';
  KEY_NOT_FOUND: string = 'KEY_NOT_FOUND';

  private eventsSubscription: Subscription;

  constructor(
    public filterService: FiltersService,
    public extraPlaceService: ExtraPlaceService,
    public gtmService: GtmService,
    public routingHelperService: RoutingHelperService,
    public localeService: LocaleService,
    public router: Router,
    public templateService: TemplateService,
    public pubSubService: PubSubService,
    private changeDetectorRef: ChangeDetectorRef) {
  }

  ngOnInit(): void {
    this.eventsSubscription = from(this.extraPlaceService.getEvents({
      racingFormEvent: true
    })).subscribe((races: ISportEvent[]) => {
      this.events = races.filter((race: ISportEvent) =>
        race.markets && race.markets.length).slice(0, this.limit);

      this.templateService.setCorrectPriceType(this.events, false, true);

      // subscribe LS Updates via PUSH
      this.subscribedChannelsId = this.extraPlaceService.subscribeForUpdates(this.events);
      this.changeDetectorRef.markForCheck();
    });

    this.pubSubService.subscribe('extraPlaceHomeComponent',
      [this.pubSubService.API.EXTRA_PLACE_RACE_OFF, this.pubSubService.API.DELETE_EVENT_FROM_CACHE],
      (eventId: number) => {
      this.events = this.events.filter((item: ISportEvent) => item.id !== eventId);
      this.changeDetectorRef.markForCheck();
    });
  }

  ngOnDestroy(): void {
    // unSubscribe LS Updates via WS
    this.extraPlaceService.unSubscribeForUpdates(this.subscribedChannelsId);
    this.pubSubService.unsubscribe('extraPlaceHomeComponent');
    this.eventsSubscription && this.eventsSubscription.unsubscribe();
  }

  /**
   * Parse going from event entity
   * @param {ISportEvent} race
   * @returns {string}
   */
  parseGoing(race: ISportEvent): string {
    const going =  this.localeService.getString(`racing.racingFormEventGoing.${race.racingFormEvent.going}`);
    return going === this.KEY_NOT_FOUND ? '' : going;
  }

  showEchWayTerms(market: IMarket): boolean {
    return !!(market.eachWayPlaces && market.eachWayFactorDen && market.eachWayFactorNum);
  }

  /**
   * Parse Distance from event entity
   * @param {ISportEvent} race
   * @returns {string}
   */
  parseDistance(race: ISportEvent): string {
    return this.filterService.distance(race.racingFormEvent.distance);
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
   * Go to the sport event
   */
  goToEvent(eventEntity: ISportEvent): void {
    this.sendGTM();
    const url = this.formEdpUrl(eventEntity);
    this.router.navigateByUrl(url);
  }

  /**
   * Forms event details page.
   * @param {Object} eventEntity
   * @return {string}
   */
  formEdpUrl(eventEntity: ISportEvent): string {
    origin = '?origin=offers-and-features';
    return `${this.routingHelperService.formEdpUrl(eventEntity)}${origin}`;
  }

  /**
   * Send GTM
   */
  private sendGTM() {
    this.gtmService.push('trackEvent', {
      eventCategory: 'horse racing',
      eventAction: 'extra place race module',
      eventLabel: 'view event'
    });
  }
}

