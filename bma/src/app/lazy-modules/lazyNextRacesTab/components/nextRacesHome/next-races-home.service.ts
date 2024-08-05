import { Injectable } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { IFilterParam } from '@core/models/filter-param.model';

import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { TemplateService } from '@shared/services/template/template.service';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { FiltersService } from '@app/core/services/filters/filters.service';
import { ICombinedRacingConfig } from '@core/services/cms/models/system-config';
import { NextRacesAbstractService } from '@core/services/racing/nextRaces/next-races-abstract.service';

@Injectable({
  providedIn: 'root'
})
export class NextRacesHomeService extends NextRacesAbstractService {

  isNextRaces = true;
  cacheKey = 'nextRacesHome';

  constructor(
    public cacheEventsService: CacheEventsService,
    public templateService: TemplateService,
    public channelService: ChannelService,
    public pubsubService: PubSubService,
    public localeService: LocaleService,
    public filterService: FiltersService
  ) {
    super(cacheEventsService, templateService, channelService, pubsubService);
  }

  subscribeForUpdates(events: ISportEvent[]): string {
    const channel = this.channelService.getLSChannelsFromArray(events);
    let subscriptionId = '';

    if (channel.length) {
      subscriptionId = `next-races-home-${ Date.now() }`;
      this.pubSubService.publish('SUBSCRIBE_LS', {
        channel,
        module: subscriptionId
      });
    }

    return subscriptionId;
  }

  unSubscribeForUpdates(subscriptionId: string): void {
    if (subscriptionId) {
      this.pubSubService.publish('UNSUBSCRIBE_LS', subscriptionId);
    }
  }

  /**
   * send GTM tracking, via pubsub
   * @param {String} eventName - event name
   * @param {String} sportName - sport name
   */
  sendGTM(eventLabel: string, eventCategory: string): void {
    this.pubsubService.publish(this.pubsubService.API.PUSH_TO_GTM, ['trackEvent', {
      eventCategory,
      eventAction: 'next races',
      eventLabel
    }]);
  }

  /**
   * Track Next Races full race card click
   * @param sport ISportEvent
   */
  trackNextRace(sport?: ISportEvent): void {
    this.pubsubService.publish(this.pubsubService.API.PUSH_TO_GTM, ['trackEvent', {
      eventCategory: 'navigation',
      eventAction: 'next races',
      eventLabel: `${sport.typeName} / ${sport.localTime}`,
      ...(sport && sport.categoryId === '39' && {positionEvent: 'virtual'})
    }]);
  }

  /**
   * Get itv events
   */
  isItvEvent(event: ISportEvent): boolean {
    const isItvEvent = event.drilldownTagNames ? event.drilldownTagNames.indexOf('EVFLAG_FRT') >= 0 : false;

    return isItvEvent;
  }


  getGoing(going: string): string {
    const KEY_NOT_FOUND = 'KEY_NOT_FOUND';
    let stage = this.localeService.getString(`racing.racingFormEventGoing.${going}`);

    if (stage === KEY_NOT_FOUND) {
      stage = '';
    }

    return stage;
  }

  getDistance(distance: string): string {
    return this.filterService.distance(distance);
  }

  // Temporary solution, in future Greyhounds should get configs from CMS as
  // for now all values remain hard coded
  /**
   * Get Greyhounds Next races config
   * @params{object} cms config
   * @returns{object} ready configs
   */
  protected getGHNextRacesModuleConfigCMS(config: ICombinedRacingConfig): IFilterParam {
    const result = super.getGHNextRacesModuleConfigCMS(config);
    result.racingFormEvent = result.racingFormOutcome;

    return result;
  }

  /**
   * Get Horse Racing Next races config from CMS
   * @params{object} cms config
   * @returns{object} ready configs
   */
  protected getHRNextRacesModuleConfigCMS(config: ICombinedRacingConfig): IFilterParam {
    const filterObject = super.getHRNextRacesModuleConfigCMS(config);
    filterObject.racingFormEvent = filterObject.racingFormOutcome;

    return filterObject;
  }

}
