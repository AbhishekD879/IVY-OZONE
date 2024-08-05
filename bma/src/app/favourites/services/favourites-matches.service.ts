import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { EventService } from '@sb/services/event/event.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMatch } from '@sb/components/matchResultsSportTab/match.model';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { TemplateService } from '@shared/services/template/template.service';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { IMarket } from '@core/models/market.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Injectable()
export class FavouritesMatchesService {

  private readonly requestConfig = {
    marketsCount: true,
    dispSortName: ['MR'],
    dispSortNameIncludeOnly: ['MR'],
    includeUndisplayed: true
  };

  constructor(
    private eventService: EventService,
    private cacheEventsService: CacheEventsService,
    private templateService: TemplateService,
    private filtersService: FiltersService,
    private channelService: ChannelService,
    private pubSubService: PubSubService,
  ) { this.getFavouritesMatches = this.getFavouritesMatches.bind(this); }

  /**
   * removeMatch()
   * @param {IMatch} matches
   * @param {number} matchId
   * @returns {IMatch[]}
   */
  removeMatch(matches: IMatch[], matchId: number): IMatch[] {
    return _.reject(matches, match => +match.id === +matchId);
  }

  /**
   * getFavouritesMatches()
   * @param {string} subscriberName
   * @param {IMatch[]} matches
   * @returns {Promise<ISportEvent[]>}
   */
  getFavouritesMatches(subscriberName: string, matches: IMatch[]): Promise<ISportEvent[]> {
    const requestParams = { eventsIds: matches.map(match => match.id) };

    return this.eventService.favouritesMatches(_.extend(requestParams, this.requestConfig))
      .then(eventsArray => {
        const trimmedEvents = this.trimFinishedEvents(eventsArray);

        this.cacheEventsService.store(subscriberName, eventsArray);

        return this.applyTemplateProperties(trimmedEvents);
      });
  }

  /**
   * applyTemplateProperties()
   * @param {ISportEvent[]} events
   * @returns {ISportEvent[]}
   */
  applyTemplateProperties(events: ISportEvent[]): ISportEvent[] {
    this.templateService.addIconsToEvents(events);

    _.forEach(events, (event: ISportEvent) => {
      event.markets = _.sortBy(event.markets, (market: IMarket) => market.name === 'Match Result' ? 0 : 1);
      event.markets[0].outcomes.forEach(outcome => {
        outcome.isUS = event.isUS;
        outcome.correctedOutcomeMeaningMinorCode = this.templateService.getCorrectedOutcomeMeaningMinorCode(outcome);
      });
      event.markets[0].outcomes = this.filtersService.orderBy(event.markets[0].outcomes, ['correctedOutcomeMeaningMinorCode']);
      event.eventCorectedDay = this.templateService.getEventCorectedDay(event.startTime);
    });

    return events;
  }

  /**
   * trimFinishedEvents()
   * @param {ISportEvent[]} events
   * @returns {ISportEvent[]}
   */
  trimFinishedEvents(events: ISportEvent[]): ISportEvent[] {
    return events.map(event => {
      if (event.isFinished || !event.isDisplayed) {
        _.forEach(event.markets, (market: IMarket) => {
          market.outcomes = [];
        });
        event.marketsCount = 0;
      }
      return event;
    });
  }

  /**
   * subscribeForUpdates()
   * @param {ISportEvent[]} events
   * @param widget
   * @param bsTab
   */
  subscribeForUpdates(events: ISportEvent[], widget: string, bsTab: boolean): void {
    const channel = this.channelService.getLSChannelsFromArray(events, true, true);

    this.pubSubService.publish('SUBSCRIBE_LS', {
      channel,
      module: `favourites-matches${ widget ? '-widget' : '' }${ bsTab ? '-bsTab' : '' }`
    });
  }

  /**
   * unSubscribeForUpdates()
   */
  unSubscribeForUpdates(widget: string, bsTab: boolean): void {
    this.pubSubService.publish('UNSUBSCRIBE_LS', `favourites-matches${ widget ? '-widget' : '' }${ bsTab ? '-bsTab' : '' }`);
  }
}
