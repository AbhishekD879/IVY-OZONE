
import { map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { Observable } from 'rxjs';

import { InplayHelperService } from '@ladbrokesDesktop/inPlay/services/inPlayHelper/inplay-helper.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { LiveEventClockProviderService } from '@shared/components/liveClock/live-event-clock-provider.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { StorageService } from '@core/services/storage/storage.service';
import { UserService } from '@core/services/user/user.service';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { EventService } from '@sb/services/event/event.service';
import { IRibbonItem } from '@app/inPlay/models/ribbon.model';
import { IFooter } from '@ladbrokesDesktop/inPlayLiveStream/models/footer.model';
import { ICompetitionGroupFormatted } from '@ladbrokesDesktop/inPlayLiveStream/models/competition-group.model';
import { InplayLivestreamData } from '@ladbrokesDesktop/inPlayLiveStream/models/inplay-livestream-data.model';
import { IRequestConfig } from '@ladbrokesDesktop/inPlayLiveStream/models/request-config.model';
import { RoutingHelperService } from '@app/core/services/routingHelper/routing-helper.service';

@Injectable()
export class InPlayLiveStreamService {

  constructor(
    private inplayHelperService: InplayHelperService,
    private timeSyncService: TimeSyncService,
    private liveEventClockProviderService: LiveEventClockProviderService,
    private pubSubService: PubSubService,
    private storageService: StorageService,
    private userService: UserService,
    private eventService: EventService,
    private routingHelperService: RoutingHelperService
  ) { }

  /**
   * Get data for single sport
   * @param {Number} categoryId
   * @param {String} categoryName
   * @param {Object} requestConfig
   * @param {IRibbonItem[]} menuItems
   */
  getData(categoryId: number,
          categoryName: string,
          requestConfig: IRequestConfig,
          menuItems: IRibbonItem[]): Observable<InplayLivestreamData> {
    return this.inplayHelperService.getData(categoryId, categoryName, requestConfig).pipe(
      map(events => {
        this.setStreamAvailability(events);
        this.addClockData(events);
        return {
          events,
          footer: this.prepareFooter(categoryName, menuItems, requestConfig.requestParams.topLevelType),
          competitions: this.groupByTypeId(events)
        };
      }));
  }

  /**
   * send GTM tracking
   * @param {String} eventAction
   * @param {String} eventLabel
   */
  sendGTM(eventAction: string, eventLabel: string): void {
    this.pubSubService.publish(this.pubSubService.API.PUSH_TO_GTM, ['trackEvent', {
      eventCategory: 'home',
      eventAction,
      eventLabel
    }]);
  }

  /**
   * Prepares footer link and title for tab
   * @param {String} categoryName
   * @param {IRibbonItem[]} menuItems
   * @param {String} topLevelType
   * @returns {Object}
   */
  prepareFooter(categoryName: string, menuItems: IRibbonItem[], topLevelType: string): IFooter {
    const menuItem: IRibbonItem = menuItems.find((el: IRibbonItem) => el.categoryName && el.categoryName.toLowerCase() === categoryName);

    if (!menuItem) {
      return;
    }

    const menuItemCount = menuItem.liveEventCount <= 4;
    let footer = {};

    if (topLevelType === 'LIVE_EVENT') {
      footer = {
        title: menuItemCount ? `View all in-play events` : `View all in-play ${categoryName}`,
        link: menuItemCount ? `/in-play` : `/in-play/${this.routingHelperService.getLastUriSegment(menuItem.targetUri)}`,
        action: () => {
          this.sendGTM('in-play', 'view all');
          return menuItemCount
            ? this.storageService.remove(`inPlay-${this.userService.username}`)
            : this.storageService.set(`inPlay-${this.userService.username}`, categoryName);
        }
      };
    } else {
      footer = {
        title: `View all Live Stream events`,
        link: `/live-stream`,
        action: () => {
          this.sendGTM('live stream', 'view all');
        }
      };
    }

    return footer as IFooter;
  }

  /**
   * Removes event after un displaying
   * @param {Object} data
   * @param {Number} eventId
   * @returns {Object}
   */
  removeEventFromCollection(data: ICompetitionGroupFormatted[], eventId: number): void {
    _.each(data, (competition: ICompetitionGroupFormatted) => {
      _.each(competition.events, (event: ISportEvent, index: number) => {
        if (event && event.id === eventId) {
          competition.events.splice(index, 1);
        }
      });
    });

    this.inplayHelperService.unsubscribeForLiveUpdates([{ id: eventId } as ISportEvent]);
  }

  /**
   * Removes competitions after un displaying last event
   * @param {Object} competitions
   * @param {String} typeIds
   * @returns {Object}
   */
  removeCompetitionFromCollection(competitions: ICompetitionGroupFormatted[], typeIds: string[]): void {
    typeIds.forEach((typeId: string) => {
      competitions.forEach( (competition: ICompetitionGroupFormatted, index: number) => {
        if (competition.events[0] && competition.events[0].typeId === typeId) {
          competitions.splice(index, 1);
        }
      });
    });
  }

  /**
   * Extends object by typeId
   * @param {Object} events
   * @returns {Object}
   */
  groupByTypeId(events: ISportEvent[]): ICompetitionGroupFormatted[] {
    const competitionsGroups = {};
    const competitionsGroupsArray = [];

    _.each(events, (value: ISportEvent) => {
      if (_.has(competitionsGroups, value.typeName)) {
        competitionsGroups[value.typeName].push(value);
      } else {
        competitionsGroups[value.typeName] = [value];
      }
    });

    for (const competitionsGroup in competitionsGroups) {
      if (competitionsGroups[competitionsGroup]) {
        competitionsGroupsArray.push({
          categoryName: competitionsGroup,
          events: competitionsGroups[competitionsGroup]
        });
      }
    }

    return competitionsGroupsArray;
  }

  /**
   * Generates switcher data
   * @param {function} onClickFn
   * @param {Array} viewByFilters
   * @returns {[*,*]}
   */
  generateSwitchers(onClickFn: Function, viewByFilters: string[]): ISwitcherConfig[] {
    const callConnect = filter => this.pubSubService.publish(this.pubSubService.API.EVENT_COUNT, filter);
    return [{
      onClick: () => {
        onClickFn(viewByFilters[0]);
        callConnect(viewByFilters[0]);
      },
      viewByFilters: viewByFilters[0],
      name: 'inplay.byInPlay'
    }, {
      onClick: () => {
        this.sendGTM('live stream', 'show events');
        onClickFn(viewByFilters[1]);
        callConnect(viewByFilters[1]);
      },
      viewByFilters: viewByFilters[1],
      name: 'inplay.byLiveStream'
    }];
  }

  private setStreamAvailability(events: ISportEvent[]): void {
    _.each(events, (event: ISportEvent) => {
      _.extend(event, this.eventService.isLiveStreamAvailable(event));
    });
  }

  /**
   * Decorate events with clock
   * @param events
   * @returns {*}
   * @private
   */
  private addClockData(events: ISportEvent[]): ISportEvent[] {
    if (events) {
      const serverTimeDelta = this.timeSyncService.getTimeDelta();
      events.forEach((e: ISportEvent) => {
        if (e.initClock) {
          const clockData = e.initClock;
          e.clock = this.liveEventClockProviderService.create(serverTimeDelta, clockData);
        }
      });
    }
    return events;
  }
}
