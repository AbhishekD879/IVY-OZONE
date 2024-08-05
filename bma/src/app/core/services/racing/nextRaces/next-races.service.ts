import { Injectable } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { NextRacesAbstractService } from '@core/services/racing/nextRaces/next-races-abstract.service';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { TemplateService } from '@shared/services/template/template.service';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Injectable()
export class NextRacesService extends NextRacesAbstractService {

  isNextRaces = true;
  cacheKey = 'nextRaces';

  constructor(
    protected cacheEventsService: CacheEventsService,
    protected templateService: TemplateService,
    protected channelService: ChannelService,
    protected pubSubService: PubSubService
  ) {
    super(cacheEventsService, templateService, channelService, pubSubService );
  }

  subscribeForUpdates(events: ISportEvent[]): string { // TODO: check!
    const subscriptionId = `next-races-${ Date.now() }`,
      channel = this.channelService.getLSChannelsFromArray(events);

    if (!channel.length) {
      return '';
    }

    this.pubSubService.publish('SUBSCRIBE_LS', {
      channel,
      module: subscriptionId
    });

    return subscriptionId;
  }

  unSubscribeForUpdates(subscriptionId: string): void {
    if (subscriptionId) {
      this.pubSubService.publish('UNSUBSCRIBE_LS', subscriptionId);
    }
  }

}
