import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { CacheEventsService } from '@app/core/services/cacheEvents/cache-events.service';
import { ChannelService } from '@app/core/services/liveServ/channel.service';
import { SiteServerService } from '@app/core/services/siteServer/site-server.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IFilterParam } from '@core/models/filter-param.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ISystemConfig } from '@core/services/cms/models';
import { IRacingDataHubConfig, IRacingPostHRResponse } from '@core/services/racing/racingPost/racing-post.model';
import { CmsService } from '@core/services/cms/cms.service';
import { RacingPostService } from '@core/services/racing/racingPost/racing-post.service';
import { EventService } from '@app/sb/services/event/event.service';

import { from, forkJoin, throwError } from 'rxjs';
import { map, concatMap, catchError } from 'rxjs/operators';

@Injectable()
export class BuildYourRaceCardPageService {
  moduleName: string = 'buildYouRaceCard';
  private requestParams = {
    priceHistory: true,
    externalKeysEvent: true
  };

  constructor(
    private cacheEventsService: CacheEventsService,
    private siteServerService: SiteServerService,
    private channelService: ChannelService,
    private pubSubService: PubSubService,
    private cmsService: CmsService,
    private racingPostService: RacingPostService,
    private eventService: EventService
  ) {}

  subscribeForUpdates(events: ISportEvent[]): void {
    const channel = this.channelService.getLSChannelsFromArray(events);

    this.pubSubService.publish('SUBSCRIBE_LS', {
      channel,
      module: 'build-your-race-card'
    });
  }

  unSubscribeForUpdates(): void {
    this.pubSubService.publish('UNSUBSCRIBE_LS', 'build-your-race-card');
  }
  /**
   * Get events by event ids
   * @param eventsIds
   * @return Promise with list of events
   */
  getEvents(eventsIds: string): Promise<ISportEvent[]> {
    return this.cmsService.getSystemConfig().pipe(
      map((data: ISystemConfig) => {
        return data.RacingDataHub;
      }),
      concatMap((raceInfoConfig: IRacingDataHubConfig) => {
        const requestParams = this.getRequestParams(raceInfoConfig.isEnabledForHorseRacing),
          res = [from(this.siteServerService.getEvent(eventsIds, requestParams, false)),
            this.racingPostService.getHorseRacingPostById(eventsIds)];

        if (!raceInfoConfig.isEnabledForHorseRacing) {
          res.pop();
        }
        return forkJoin(res);
      }),
      map(([eventData, raceData]: [ISportEvent[], IRacingPostHRResponse]) => {
        return this.racingPostService.mergeHorseRaceData(eventData, raceData);
      }),
      catchError((error) => {
        console.error(`Error loading horse data for OB events ${eventsIds}`, error);
        return throwError(error);
      })
    ).toPromise()
      .then((events: ISportEvent[]) => {
        let stored: ISportEvent[] = this.cacheEventsService.store('events', this.moduleName, events);
        stored = stored.map((el: ISportEvent) => ({
          ...el,
          isUKorIRE: this.eventService.isUKorIRE(el)
        }));

        return _.sortBy(_.sortBy(stored, 'name'), 'startTime');
      });
  }

  private getRequestParams(isRDHEnabled): IFilterParam {
    return !isRDHEnabled ? Object.assign({ racingFormOutcome: true, racingFormEvent: true }, this.requestParams) : this.requestParams;
  }
}
