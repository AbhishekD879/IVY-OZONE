/**
 * Service is used for getting and handling enhanced events data.
 */
import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { extraPlaceConfig } from './extra-place.constant';

import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { TimeService } from '@core/services/time/time.service';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ChannelService } from '@core/services/liveServ/channel.service';

import { ISportEvent } from '@core/models/sport-event.model';
import { ITrackEvent } from '@core/services/gtm/models';
import { IConstant } from '@core/services/models/constant.model';

@Injectable()
export class ExtraPlaceService {
  gtmObject: ITrackEvent = {
    event: 'trackEvent',
    eventCategory: 'horse racing',
    eventAction: 'extra place',
    eventLabel: 'collapse'
  };

  constructor(
    private siteServerService: SiteServerService,
    private timeService: TimeService,
    private cacheEventsService: CacheEventsService,
    private gtmService: GtmService,
    private pubSubService: PubSubService,
    private channelService: ChannelService
  ) {

    this.extendCacheParams();
  }
  /**
   * Get extra place events from SS
   */
  getEvents(params?: IConstant): Promise<ISportEvent[]> {
    const requestParams = _.extendOwn({
      startTime: this.timeService.selectTimeRangeStart()
    }, extraPlaceConfig.request, params);

    return this.cachedEvents(this.siteServerService.getExtraPlaceEvents.bind(this.siteServerService),
      extraPlaceConfig.cacheName)(requestParams)
      .then((events: ISportEvent[]) => _.sortBy(events, 'startTime'));
  }

  subscribeForUpdates(events: ISportEvent[]): string {
    const channel = this.channelService.getLSChannelsFromArray(events);
    let subscriptionId = '';

    if (channel.length) {
      subscriptionId = `extra-place-${ Date.now() }`;
      this.pubSubService.publish('SUBSCRIBE_LS', {
        channel,
        module: subscriptionId
      });
    }

    return subscriptionId;
  }

  unSubscribeForUpdates(channelsId: string): void {
    if (channelsId) {
      this.pubSubService.publish('UNSUBSCRIBE_LS', channelsId);
    }
  }

  /**
   * send GTM tracking, when user click on extra place card
   */
  sendGTM(eventLabel: string): void {
    this.gtmService.push('trackEvent', {
      eventCategory: 'horse racing',
      eventAction: 'extra place',
      eventLabel
    });
  }

  /* Store events or get new
   * @param {function} loaderFn - method for event load
   * @param {String} cacheName
   * @returns promise
   */
  cachedEvents(loaderFn: Function, cacheName: string) {
    return params => {
      const store = _.partial(this.cacheEventsService.store, cacheName);
      const stored = this.cacheEventsService.stored(cacheName);
      // @ts-ignore
      return stored ? this.cacheEventsService.async(stored) : loaderFn(params).then(events => store(events));
    };
  }

  /**
   * Extends apiDataCacheInterval and storedData params for cache
   */
  private extendCacheParams(): void {
    this.timeService.apiDataCacheInterval[extraPlaceConfig.cacheName] = extraPlaceConfig.cacheInterval;
    this.cacheEventsService.storedData[extraPlaceConfig.cacheName] = {};
  }
}
