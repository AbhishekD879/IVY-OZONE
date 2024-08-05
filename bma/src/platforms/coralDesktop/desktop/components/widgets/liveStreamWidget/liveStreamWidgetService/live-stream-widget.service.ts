
import { of as observableOf, Observable } from 'rxjs';
import { concatMap, map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { ISocketConnection } from '@core/models/socket-connection.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { oddsCardConstant } from '@platform/shared/constants/odds-card-constant';
import { ILivestreamColumnsData } from '@desktop/models/live-stream-widget.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { IRequestConfig } from '@inPlayLiveStream/models/request-config.model';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { CommentsService } from '@core/services/comments/comments.service';
import { WsUpdateEventService } from '@core/services/wsUpdateEvent/ws-update-event.service';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IBaseObject } from '@app/inPlay/models/base-object.model';
import { InplayHelperService } from '@coralDesktop/inPlay/services/inPlayHelper/inplay-helper.service';
import { FiltersService } from '@core/services/filters/filters.service';

@Injectable()
export class LiveStreamWidgetService {
  connection: ISocketConnection;

  private isLiveUpdatesHandlerAdded: boolean;
  private requestConfig: IRequestConfig = {
    requestParams: {
      emptyTypes: 'Yes',
      autoUpdates: 'No',
      isLiveNowType: true,
      topLevelType: 'STREAM_EVENT',
    },
    socket: {
      sport: {
        emit: 'GET_SPORT',
        on(data) {
          return `IN_PLAY_SPORTS::${data.categoryId}::STREAM_EVENT`;
        }
      },
      competition: {
        emit: 'GET_TYPE',
        on(data) {
          return `IN_PLAY_SPORT_TYPE::${data.categoryId}::STREAM_EVENT::${data.typeId}`;
        }
      }
    }
  };

  constructor(
    private pubSubService: PubSubService,
    private cacheEventsService: CacheEventsService,
    private wsUpdateEventService: WsUpdateEventService,
    private commentsService: CommentsService,
    private inplayHelperService: InplayHelperService,
    private filtersService: FiltersService
  ) {
    this.wsUpdateEventService.subscribe();
  }
  /**
   * Get Sport Event
   * @param {Number} categoryId
   * @param {String} sportName
   * @param {Array<number>} omitEventIds omits events with given ids
   */
  getData(categoryId: number, sportName: string, omitEventIds?: number[]): Observable<ISportEvent> {
    return this.inplayHelperService.getSportData(categoryId, sportName, this.requestConfig).pipe(
      concatMap((sportData: ISportSegment) => {
        if (!this.isLiveUpdatesHandlerAdded) {
          this.addLiveUpdatesHandler();
          this.isLiveUpdatesHandlerAdded = true;
        }

        if (sportData.eventsByTypeName && sportData.eventsByTypeName.length) {
          return this.getEventsByCompetition(sportData, sportName, this.requestConfig, omitEventIds);
        }

        return observableOf(null);
      }));
  }

  getEventsByCompetition(sportData: ISportSegment, sportName: string, requestConfig: IRequestConfig,
                          omitEventIds?: number[]): Observable<ISportEvent> {
    if (omitEventIds && omitEventIds.length) {
      sportData.eventsByTypeName = sportData.eventsByTypeName.filter((competition: ITypeSegment) => {
        return !competition.eventsIds.every((eventId: number) => omitEventIds.includes(eventId));
      });
    }
    const selectedCompetition = sportData.eventsByTypeName[0];
    if (selectedCompetition) {
      requestConfig.requestParams.typeId = selectedCompetition.typeId;
      const requestParams = { ...requestConfig.requestParams };
      const getCompetitionData = requestConfig.socket.competition;

      const competition$ = this.inplayHelperService.get(getCompetitionData, requestParams).pipe(
        map((competitionEvents: ISportEvent[]) => {
          competitionEvents.forEach(event => {
            event.typeName = selectedCompetition.typeSectionTitleAllSports;
          });
          return competitionEvents;
        }));
      return competition$.pipe(
        map((data: ISportEvent[]) => [].concat(...data)),
        map((data: ISportEvent[]) => this.extractNewestSportEvent(data, omitEventIds)),
        map((data: ISportEvent[]) => data.length ? this.storeEventsToCache(data) : data),
        map((data: ISportEvent[]) => this.inplayHelperService.subscribeForLiveUpdates(data)),
        map((data: ISportEvent[]) => this.updateCommentsDataFormat(data[0], sportName)));
    }
    return observableOf(null);
  }

  /**
   * send GTM tracking, when user click on eventName
   * @param {String} eventName - event name
   * @param {String} sportName - sport name
   */
  sendGTM(eventName: string, sportName: string): void {
    this.pubSubService.publish(this.pubSubService.API.PUSH_TO_GTM, ['trackEvent', {
      eventCategory: 'widget',
      eventAction: 'watch live',
      eventLabel: `${eventName}`,
      sport: `${sportName}`
    }]);
  }

  /**
   * Find Odds Header
   * @param {Object} market
   * @param {String} sportName
   * @param {boolean} isColumn
   */
  findOddsHeader(market, sportName, isColumn): string | ILivestreamColumnsData {
    const isThreeType = market.viewType === 'Scorer' ||
      market.viewType === 'WDW' || market.outcomes.length === 3;
    const isYesNoType = _.contains(['BO', 'GB'], market.dispSortName);
    const isHomeAwayType = _.contains(['TN'], market.dispSortName);
    const isOverUnderType = _.contains(['L', 'I'], market.marketMeaningMajorCode);
    const isNoGoalType = market.templateMarketName === 'Next Team to Score';
    const isOneTwoThreeType = isThreeType && sportName === 'golf';
    const isHomeDrawAwayType = (isThreeType && !isOneTwoThreeType) ||
      (sportName === 'football' && _.contains(oddsCardConstant.MARKET_TYPES, market.templateMarketName));
    const isOneTwoType = !isNoGoalType && !isHomeDrawAwayType && !isHomeAwayType &&
      !isOverUnderType && !isYesNoType && !isOneTwoThreeType;

    if (isColumn) {
      return {
        columns2: isOneTwoType || isHomeAwayType || isOverUnderType || isYesNoType,
        columns3: isOneTwoThreeType || isNoGoalType || isHomeDrawAwayType
      };
    }

    return _.findKey({
      '1,2,2': isOneTwoType,
      'home,away,noGoal': isNoGoalType,
      'home,draw,away': isHomeDrawAwayType,
      'home,away,away': isHomeAwayType,
      'over,under,under': isOverUnderType,
      'yes,no,no': isYesNoType,
      '1,2,3': isOneTwoThreeType
    }, undefined);
  }

  /**
   * Extracting the event by order and startTime
   * @private
   * @param data<ISportEvent[]> array of events
   * @param omitEventIds omits events with given ids
   */
  private extractNewestSportEvent(data: ISportEvent[], omitEventIds?: number[]): ISportEvent[] {
    let sportsEvents = data;

    if (omitEventIds && omitEventIds.length) {
      sportsEvents = sportsEvents.filter(e => !omitEventIds.includes(e.id));
    }

    const orderedList = this.filtersService.orderBy(sportsEvents, ['startTime', 'displayOrder', 'name']);

    return (orderedList && orderedList[0] && [orderedList[0]]) || [];
  }

  /**
   * Add listener for live updates
   * @private
   */
  private addLiveUpdatesHandler(): void {
    this.pubSubService.subscribe('LiveStreamWidgetService', this.pubSubService.API.WS_EVENT_LIVE_UPDATE,
      (eventId: string, messageBody: IBaseObject) => {
        this.handleLiveUpdate(eventId, messageBody);
      });
  }

  /**
   * Handles live updates for events.
   * @private
   */
  private handleLiveUpdate(eventId: string, messageBody: IBaseObject): void {
    const eventsToUpdate = _.find(this.cacheEventsService.storedData.LSWidget.data, { id: parseInt(eventId, 10) });

    /**
     * Trigger to update events in wsUpdateEventFactory
     * {array} events - "liveStream" filtered events with specific ID from update,
     * {object} updateDetails - ws update object
     */
    if (eventsToUpdate) {
      this.pubSubService.publish(this.pubSubService.API.WS_EVENT_UPDATE, {
        events: [eventsToUpdate],
        update: messageBody
      });
    }
  }

  /**
   * Store events to cache
   * @param {Array} events
   * @private
   */
  private storeEventsToCache(events): ISportEvent[] {
    return this.cacheEventsService.store('LSWidget', events);
  }

  /**
   * Update comments data format(adapt for UI templates)
   * @param event - event
   * @param sportName - sport name
   * @private
   */
  private updateCommentsDataFormat(event: ISportEvent, sportName: string): ISportEvent {
    const methodName = `${sportName}MSInitParse`,
      updater = this.commentsService[methodName];
    if (event && event.comments && updater) {
      updater(event.comments);
    }
    return event;
  }
}
