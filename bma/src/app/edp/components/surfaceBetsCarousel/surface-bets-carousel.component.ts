import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISurfaceBetModule } from '@shared/models/surface-bet-module.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { IEdpSurfaceBetDto } from '@core/services/cms/models/surface-bet-dto.model';
import { ISurfaceBetEvent } from '@shared/models/surface-bet-event.model';

@Component({
  selector: 'edp-surface-bets-carousel',
  templateUrl: './surface-bets-carousel.component.html'
})

export class EdpSurfaceBetsCarouselComponent implements OnInit, OnDestroy {
  @Input() eventId: number;

  public module: ISurfaceBetModule;
  private eventsDataSubscription: Subscription;

  constructor(
    private cmsService: CmsService,
    private channelService: ChannelService,
    private cacheEventsService: CacheEventsService,
    private pubSubService: PubSubService
  ) {
  }

  ngOnInit(): void {
    this.eventsDataSubscription = this.cmsService.getEDPSurfaceBets(this.eventId).subscribe((bets: IEdpSurfaceBetDto[]) => {
      let events = bets.map((bet: IEdpSurfaceBetDto) => {
        const event = bet.selectionEvent as ISurfaceBetEvent;
        event.oldPrice = bet.price;
        event.svg = bet.svg;
        event.svgId = bet.svgId;
        event.title = bet.title;
        event.content = bet.content;
        event.svgBgId = bet.svgBgId;
        event.svgBgImgPath = bet.svgBgImgPath;
        event.contentHeader = bet.contentHeader;
        return event;
      });

      events = this.cacheEventsService.store('surfaceBetEvents', events);
      this.subscribeForUpdates(events);
      this.module = {
        data: events
      } as ISurfaceBetModule;
    });
  }

  ngOnDestroy(): void {
    this.pubSubService.publish('UNSUBSCRIBE_LS', 'edp-surface-bets');

    if (this.eventsDataSubscription) {
      this.eventsDataSubscription.unsubscribe();
    }
  }

  private subscribeForUpdates(events: ISportEvent[]): void {
    const channel = this.channelService.getLSChannelsFromArray(events);

    this.pubSubService.publish('SUBSCRIBE_LS', {
      channel,
      module: 'edp-surface-bets'
    });
  }

}
