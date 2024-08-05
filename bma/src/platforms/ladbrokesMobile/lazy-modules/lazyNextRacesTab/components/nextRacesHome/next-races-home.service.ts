import { Injectable } from '@angular/core';

import { ISportEvent } from '@core/models/sport-event.model';

import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { TemplateService } from '@shared/services/template/template.service';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { FiltersService } from '@app/core/services/filters/filters.service';
import {
  NextRacesHomeService as CoralNextRacesHomeService
} from '@lazy-modules/lazyNextRacesTab/components/nextRacesHome/next-races-home.service';

@Injectable({providedIn:'root'})
export class NextRacesHomeService extends CoralNextRacesHomeService {
  constructor(
    public cacheEventsService: CacheEventsService,
    public templateService: TemplateService,
    public channelService: ChannelService,
    public pubsubService: PubSubService,
    public localeService: LocaleService,
    public filterService: FiltersService
  ) {
    super(
      cacheEventsService,
      templateService,
      channelService,
      pubsubService,
      localeService,
      filterService
    );
  }

  /**
   * Track Next Races full race card click
   * @param sport ISportEvent
   * @param moduleType
   */
  trackNextRace(sport?: ISportEvent, moduleType?: string): void {
    this.pubsubService.publish(this.pubsubService.API.PUSH_TO_GTM, ['trackEvent', {
      eventCategory: (moduleType === 'greyhound' || moduleType === 'horseracing') ? 'navigation' : 'widget',
      eventAction: 'next races',
      eventLabel: sport && (moduleType === 'greyhound' || moduleType === 'horseracing') ?
        `${sport.typeName} / ${sport.localTime}` :
        'view race card',
        ...(sport && sport.categoryId === '39' && {positionEvent: 'virtual'})
    }]);
  }
}
