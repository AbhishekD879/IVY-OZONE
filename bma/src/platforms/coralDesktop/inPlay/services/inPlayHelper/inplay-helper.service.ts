import { forkJoin as observableForkJoin, of as observableOf,  Observable } from 'rxjs';
import { map, concatMap } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { InplayApiModule } from '@app/inPlay/inplay-api.module';
import * as _ from 'underscore';

import { WsUpdateEventService } from '@core/services/wsUpdateEvent/ws-update-event.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';
import { InPlayStorageService } from '@inplayModule/services/inplayStorage/in-play-storage.service';
import { CommentsService } from '@core/services/comments/comments.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import {
  IDefaultConfig, IInplayLiveStreamRequestParams,
  IRequestConfig,
  ISocketRequestConfig
} from '@inPlayLiveStream/models/request-config.model';
import { WsConnector } from '@core/services/wsConnector/ws-connector';
import { ISocketConnection } from '@core/models/socket-connection.model';
import { IRibbonData } from '@app/inPlay/models/ribbon.model';

@Injectable({
  providedIn: InplayApiModule
})
export class InplayHelperService {
  connection: ISocketConnection;
  cachePrefix: string;
  MATCH_RESULT_MARKET_IDENTIFICATOR: string = 'MR';
  FOOTBALL_MARKETS_TO_MODIFY: string[] = ['To Qualify', 'Penalty Shoot Out Winner', 'Penalty Shoot-Out Winner'];
  defaultConfig: IDefaultConfig = {
    requestParams: {
      emptyTypes: 'Yes',
      autoUpdates: 'No',
      isLiveNowType: true
    },
    socket: {
      structure: {
        emit: 'GET_INPLAY_LS_STRUCTURE',
        on: `INPLAY_LS_STRUCTURE`
      },
      ribbon: {
        emit: 'GET_LS_RIBBON',
        on: `INPLAY_LS_SPORTS_RIBBON`
      }
    }
  };

  private ribbonChangedMeassage: string = 'IN_PLAY_LS_SPORTS_RIBBON_CHANGED';
  private isLiveUpdatesHandlerAdded: boolean = false;

  constructor(
    private coreToolsService: CoreToolsService,
    private pubsubService: PubSubService,
    private wsUpdateEventService: WsUpdateEventService,
    private commentsService: CommentsService,
    private cacheEventsService: CacheEventsService,

    private inplayConnectionService: InplayConnectionService,
    private inPlayStorageService: InPlayStorageService
  ) {
    this.wsUpdateEventService.subscribe();
  }

  /**
   * @param {Number} categoryId
   * @param {String} sportName
   * @param {Object} requestConfig
   */
  getData(categoryId: number, sportName: string, requestConfig: IRequestConfig): Observable<any> {
    const config = this.coreToolsService.merge(requestConfig, this.defaultConfig);

    return this.getSportData(categoryId, sportName, config).pipe(
      concatMap((sportData: ISportSegment) => {
        if (sportData.eventsByTypeName) {
          return this.getEventsByCompetitions(sportData, sportName, config);
        }
        return observableOf([]);
      }));
  }

  getSportData(categoryId: number, sportName: string, config: IRequestConfig) {
    return this.inplayConnectionService.connectComponent().pipe(
      concatMap((connection: WsConnector) => {
        this.connection = connection.connection;
        this.setCachePrefix(config.cachePrefix);
        if (!this.isLiveUpdatesHandlerAdded) {
          this.addLiveUpdatesHandler();
          this.isLiveUpdatesHandlerAdded = true;
        }
        return this.getSport(categoryId, config);
      }));
  }

  /**
   * Load data for Ribbon
   * @param {Object} requestConfig
   */
  getRibbonData(requestConfig: IRequestConfig): Observable<IRibbonData> {
    const config = this.coreToolsService.merge(requestConfig, this.defaultConfig);

    return this.inplayConnectionService.connectComponent().pipe(
      concatMap((connection: WsConnector) => {
        this.connection = connection.connection;
        return this.loadData('ribbon', config);
      }));
  }

  /**
   * subscribes for RibbonUpdates
   * @private
   */
  subscribe4RibbonUpdates(): void {
    const handlerFunction = this.inPlayStorageService.onRibbonUpdate;
    this.addEventListener(this.ribbonChangedMeassage, handlerFunction);
    this.emit('subscribe', this.ribbonChangedMeassage);
  }

  /**
   * Unsubscribes for RibbonUpdates.
   * @private
   */
  unsubscribe4RibbonUpdates(): void {
    this.emit('unsubscribe', this.ribbonChangedMeassage);
  }

  /**
   * subscription to remove/add competition from sport
   * when the last event undisplayed, or first event added.
   */
  subscribeForSportCompetitionChanges(sportId, topLevelType): void {
    this.addEventListener(`IN_PLAY_SPORT_COMPETITION_CHANGED::${sportId}::${topLevelType}`, (data: any) => {
      if (data.added.length) {
        this.pubsubService.publish(this.pubsubService.API.INPLAY_LS_COMPETITION_ADDED, data);
      }
      if (data.removed.length) {
        this.pubsubService.publish(this.pubsubService.API.INPLAY_LS_COMPETITION_REMOVED, data);
      }

    });
    this.emit('subscribe', `IN_PLAY_SPORT_COMPETITION_CHANGED::${sportId}::${topLevelType}`);
  }

  /**
   * unsubscribe to remove/add competition from sport
   */
  unsubscribeForSportCompetitionChanges(sportId: number, topLevelType: string): void {
    this.emit('unsubscribe', `IN_PLAY_SPORT_COMPETITION_CHANGED::${sportId}::${topLevelType}`);
  }

  /**
   * Get events
   * @return {string} events
   */
  getEventsByCompetitions(sportData: ISportSegment, sportName: string, requestConfig: IRequestConfig): Observable<ISportEvent[]> {
    const competitionsLoadingObservables = [];
    let events = [];
    let eventCount = null;

    sportData.eventsByTypeName.forEach((competition: ITypeSegment) => {
      if (eventCount <= requestConfig.limit) {
        eventCount += competition.eventCount;
        requestConfig.requestParams.typeId = competition.typeId;
        const requestParams = {... requestConfig.requestParams };
        const getCompetitionData = requestConfig.socket.competition;

        const loadingObservable = this.get(getCompetitionData, requestParams).pipe(
          map((competitionEvents: ISportEvent[]) => {
            this.getTitleForEvent(competitionEvents, competition);
            events = events.concat(competitionEvents);
            // for competition response and only for football
            // when no market selector or "main market" market selector
            // modify main markets template view (home/away => home/draw/away)
            if (sportName === 'football') {
              this.modifyMainMarkets(events);
            }
          }));

        competitionsLoadingObservables.push(loadingObservable);
      }
    });

    return observableForkJoin(competitionsLoadingObservables).pipe(
      map(() => events.splice(0, requestConfig.limit)),
      map((data: ISportEvent[]) => this.updateCommentsDataFormat(data, sportName)),
      map((data: ISportEvent[]) => this.storeEventsToCache(data)),
      map((data: ISportEvent[]) => this.subscribeForLiveUpdates(data)));
  }

  /**
   * Subscribe for live Updates via WS
   * @param events
   * @return {Array} events
   * @private
   */
  subscribeForLiveUpdates(events: ISportEvent[]): ISportEvent[] {
    const ids = _.map(events, (event: ISportEvent) => event.id);
    if (ids && ids.length) {
      this.emit('subscribe', ids);
    }
    return events;
  }

  /**
   * UnSubscribe for live Updates via WS
   * @param events
   * @return {Array} events
   * @private
   */
  unsubscribeForLiveUpdates(events: ISportEvent[]): void {
    const ids = _.map(events, (event: ISportEvent) => event.id);
    if (ids && ids.length) {
      this.emit('unsubscribe', ids);
    }
  }

  /**
   * Get data from WS related to event
   * @param {String} eventName
   * @param {Object} emitData
   * @returns {Observable}
   */
  get(eventName: ISocketRequestConfig, emitData: IInplayLiveStreamRequestParams): Observable<ISportSegment | ISportEvent[]>  {
    const onEventName = eventName.on(emitData);
    const emitEventName = eventName.emit;

    return Observable.create(observer => {
      this.addEventListener(onEventName, (wsData: ISportSegment) => {
        observer.next(wsData);
        observer.complete();
      });

      this.emit(emitEventName, emitData);
    });
  }

  /**
   * Emits an event to the socket identified by the string name.
   * @param {String} event
   * @param {Object} data
   */
  emit(event: string, data: any): void {
    this.connection && this.connection.emit(event, data);
  }

  /**
   * send GTM tracking, when user click on eventName
   * @param {String} eventName - event name
   * @param {String} sportName - sport name
   */
  sendGTM(eventName: string, sportName: string): void {
    this.pubsubService.publish(this.pubsubService.API.PUSH_TO_GTM, ['trackEvent', {
      eventCategory: 'widget',
      eventAction: 'in play',
      eventLabel: `${eventName}`,
      sport: `${sportName}`
    }]);
  }

  /**
   * Handles live updates for events.
   * @param {string} eventId
   * @param {IWSLiveUpdate} message
   * @private
   */
  handleLiveUpdate(eventId: string, message: string): void {
    const eventToUpdate = parseInt(eventId, 10);
    const eventsToUpdate = _.find(this.cacheEventsService.storedData[this.getCachePrefix()].data, { id: eventToUpdate });

    if (eventsToUpdate) {
      this.pubsubService.publish(this.pubsubService.API.WS_EVENT_UPDATE, {
        events: [eventsToUpdate],
        update: message
      });
    }
  }

  // prepare to close inplay connection when livestream component is destroyed
  disconnect(): void {
    this.inplayConnectionService.disconnectComponent();
  }

  /**
   * Load data via websockets
   * @param {string} dataType
   * @param {object} requestConfig
   * @returns {Observable} - Observable, resolved after getting response message.
   */
  private loadData(dataType: string, requestConfig: IRequestConfig): Observable<IRibbonData> {
    const loadDataPromiseTimeout = 3000;
    const requestMessage = requestConfig.socket[dataType].emit;
    const responseMessage = requestConfig.socket[dataType].on;

    return Observable.create(observer => {
      // create a timeout to reject promise if not resolved
      const timer = setTimeout(() => {
        observer.error('No response after 3 seconds');
      }, loadDataPromiseTimeout);

      this.addEventListener(responseMessage, (wsData: IRibbonData) => {
        clearTimeout(timer);
        if (wsData && !_.isEmpty(wsData.items)) {
          observer.next(wsData);
          observer.complete();
        } else {
          observer.error('no data');
        }
      });

      this.emit(requestMessage, requestConfig.requestParams);
    });
  }

  /**
   * To qualify and Penalty markets have "home/away" type,
   * but we need to show all sections with "home/draw/away" odds card header.
   * thats why we need to emulate MatchResult market.
   * @param events
   */
  private modifyMainMarkets(events: ISportEvent[]): void {
    _.forEach(events, (event: ISportEvent) => {
      // each event has only one market
      const market = event.markets[0];

      if (market && _.contains(this.FOOTBALL_MARKETS_TO_MODIFY, market.templateMarketName)) {
        market.marketMeaningMinorCode = this.MATCH_RESULT_MARKET_IDENTIFICATOR;
        market.dispSortName = this.MATCH_RESULT_MARKET_IDENTIFICATOR;
      }
    });
  }

  /**
   * get name for event
   * @param {Array} competitionEvents
   * @param {Object} competition
   * @private
   */
  private getTitleForEvent(competitionEvents: ISportEvent[], competition: ITypeSegment): ISportEvent[] {
    competitionEvents.forEach((event: ISportEvent) => {
      if (this.getCachePrefix() === 'inplaySection') {
        event.typeName = competition.typeSectionTitleOneSport;
      } else {
        event.typeName = competition.typeSectionTitleAllSports;
      }
    });
    return competitionEvents;
  }

  /**
   * Set cache prefix
   * @param prefix
   * @private
   */
  private setCachePrefix(prefix): void {
    this.cachePrefix = prefix;
  }

  /**
   * Get cache prefix
   * @returns {null | string}
   * @private
   */
  private getCachePrefix(): string {
    return this.cachePrefix;
  }

  /**
   * Add listener for live updates
   * @private
   */
  private addLiveUpdatesHandler(): void {
    this.pubsubService.subscribe('inplaySectionLiveUpdate',
      this.pubsubService.API.WS_EVENT_LIVE_UPDATE,
      (eventId, message) => {
        this.handleLiveUpdate(eventId, message);
      });
  }

  /**
   * Get sport
   * @return {Observable} sport structure
   */
  private getSport(categoryId: number, requestConfig: IRequestConfig): Observable<ISportSegment> {
    requestConfig.requestParams.categoryId = categoryId;
    return this.get(requestConfig.socket.sport, requestConfig.requestParams) as Observable<ISportSegment>;
  }

  /**
   * Register a new handler for the given event.
   *
   * @param {string} event
   * @param {function} callback
   */
  private addEventListener(event: string, callback: Function): void {
    this.connection.on(event, callback);
  }


  /**
   * Update comments data format(adapt for UI templates)
   * @param events - events list
   * @param sportName - sport name
   * @private
   */
  private updateCommentsDataFormat(events: ISportEvent[], sportName: string): ISportEvent[] {
    if (events.length) {
      _.each(events, (event: ISportEvent) => {
        const methodName = `${sportName}MSInitParse`,
          updater = this.commentsService[methodName];
        if (event.comments && updater) {
          updater(event.comments);
        }
      });
    }
    return events;
  }

  /**
   * Store events to cache
   * @param {Array} events
   * @private
   */
  private storeEventsToCache(events: ISportEvent[]): ISportEvent[] {
    return this.cacheEventsService.store(this.getCachePrefix(), events);
  }
}
