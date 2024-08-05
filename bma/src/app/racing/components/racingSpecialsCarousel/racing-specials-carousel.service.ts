/**
 * Service is used for getting and handling enhanced events data.
 */
import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { TimeService } from '@core/services/time/time.service';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { RACING_SPECIAL } from '@racing/components/racingSpecialsCarousel/racing-specials-carousel.constant';
import { ChannelService } from '@core/services/liveServ/channel.service';

import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Injectable()
export class RacingSpecialsCarouselService {
  constructor(
    private siteServerService: SiteServerService,
    private timeService: TimeService,
    private cacheEventsService: CacheEventsService,
    private pubSubService: PubSubService,
    private channelService: ChannelService) {
  }
  /**
   * Get Racing Specials events from SS
   */
  getEvents(eventId: number): Promise<ISportEvent[]> {
    this.extendCacheParams(eventId);
    return this.cachedEvents(this.siteServerService.getRacingSpecialsEvents.bind(this.siteServerService),
      RACING_SPECIAL.cacheName + eventId)(eventId)
      .then((events: ISportEvent[]) => this.orderEvents(events) as ISportEvent[]);
  }

  subscribeForUpdates(events: ISportEvent[]): void {
    const channel = this.channelService.getLSChannelsFromArray(events);

    this.pubSubService.publish('SUBSCRIBE_LS', {
      channel,
      module: 'racing-specials'
    });
  }

  unSubscribeForUpdates(): void {
    this.pubSubService.publish('UNSUBSCRIBE_LS', 'racing-specials');
  }

  clearCache(eventId: number): void {
    this.cacheEventsService.clearByName(RACING_SPECIAL.cacheName + eventId);
  }

  orderEvents(events: (ISportEvent | IMarket | IOutcome)[]): (ISportEvent | IMarket | IOutcome)[] {
    return _.chain(events)
      .sortBy(data => data.name.toLowerCase())
      .sortBy('startTime')
      .sortBy('displayOrder')
      .value();
  }

  /**
   * Extends apiDataCacheInterval and storedData params for cache
   */
  private extendCacheParams(eventId: number): void {
    this.timeService.apiDataCacheInterval[RACING_SPECIAL.cacheName + eventId] = RACING_SPECIAL.cacheInterval;
    this.cacheEventsService.storedData[RACING_SPECIAL.cacheName + eventId] = {};
  }

  /** Store events or get new
   * @param {function} loaderFn - method for event load
   * @param {String} cacheName
   * @returns promise
   */
  private cachedEvents(loaderFn: Function, cacheName: string): (params: number) => { then: Function } {
    return params => {
      const store = _.partial(this.cacheEventsService.store, cacheName);
      const stored = this.cacheEventsService.stored(cacheName);
      // @ts-ignore
      return stored ? this.cacheEventsService.async(stored) : loaderFn(params).then(events => store(events));
    };
  }
}
