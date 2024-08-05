import {
  forkJoin as observableForkJoin,
  of as observableOf,
  Observable,
  throwError,
  Subject,
  Subscription,
  Observer
} from 'rxjs';
import { catchError, concatMap, map, finalize } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import * as _ from 'underscore';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { InplayDataService } from '@app/inPlay/services/inplayData/inplay-data.service';
import { InPlayStorageService } from '@inplayModule/services/inplayStorage/in-play-storage.service';
import { InplaySubscriptionManagerService } from '@app/inPlay/services/InplaySubscriptionManager/inplay-subscription-manager.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { LiveEventClockProviderService } from '@shared/components/liveClock/live-event-clock-provider.service';
import { CashOutLabelService } from '@core/services/cashOutLabel/cash-out-label.service';
import { UserService } from '@core/services/user/user.service';
import { StorageService } from '@core/services/storage/storage.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IRibbonCache, IRibbonData, IRibbonItem } from '@app/inPlay/models/ribbon.model';
import { IStructureCacheData, IStructureData } from '@app/inPlay/models/structure.model';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { EVENT_TYPES } from '@app/inPlay/constants/event-types.constant';
import { watchLiveItem } from '@app/inPlay/constants/watch-live-ribbon.constant';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { IRequestParams } from '@app/inPlay/models/request.model';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { inplayConfig, inplayLiveStreamConfig } from '@app/inPlay/constants/config';
import { IWSLiveUpdate } from '@app/inPlay/models/liveUpdates/live-updates.model';
import { IInplayAllSports } from '@app/inPlay/models/inplay-all-sports.model';
import { IEventCounter, IEventCounterMap } from '@app/inPlay/models/event-counter.model';
import { ICompetitionChangeMessage } from '@app/inPlay/models/liveUpdates/competition-change-message.model';
import { ISystemConfig } from '@core/services/cms/models';
import { IsPropertyAvailableService } from '@sb/services/isPropertyAvailable/is-property-available.service';
import { CommentsService } from '@core/services/comments/comments.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { InplayApiModule } from '@app/inPlay/inplay-api.module';
import { GamingService } from '@core/services/sport/gaming.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import environment from '@environment/oxygenEnvConfig';
@Injectable({
  providedIn: InplayApiModule
})
export class InplayMainService {
  expandedLeaguesCount: number;
  isLiveUpdatesHandlerAdded = false;
  isWidgetEnabled = false;
  isWatchLiveEnabled: boolean = true;

  private ribbonLoaded$: Subject<IRibbonCache>;
  private loadDataSubscription: Subscription;

  constructor(
    protected pubSubService: PubSubService,
    protected inPlayDataService: InplayDataService,
    protected inPlayStorageService: InPlayStorageService,
    protected inPlaySubscriptionManagerService: InplaySubscriptionManagerService,
    protected timeSyncService: TimeSyncService,
    protected liveEventClockProviderService: LiveEventClockProviderService,
    protected cashOutLabelService: CashOutLabelService,
    protected location: Location,
    protected userService: UserService,
    protected storageService: StorageService,
    protected cmsService: CmsService,
    protected windowRef: WindowRefService,
    protected isPropertyAvailableService: IsPropertyAvailableService,
    protected commentsService: CommentsService,
    protected router: Router,
    protected routingState: RoutingState,
    protected route: ActivatedRoute,
    protected sportsConfigService: SportsConfigService,
  ) {
    this._getSport = this._getSport.bind(this);
    this._getStructure = this._getStructure.bind(this);
    this._getCompetitionData = this._getCompetitionData.bind(this);
    this.filterAllSportsRibbonItems = this.filterAllSportsRibbonItems.bind(this);
    this._filterShowInPlay = this._filterShowInPlay.bind(this);
    this._addExpandProperties = this._addExpandProperties.bind(this);
    this.filterLiveStreamInPlay = this.filterLiveStreamInPlay.bind(this);
    this.addExpandLiveStream = this.addExpandLiveStream.bind(this);
  }

  /**
   * Shortcut for function to check if events contains at least one with cashOutAvailable
   * @param {ISportEvent[]} events
   * @return {boolean}
   */
  isCashoutAvailable(events: ISportEvent[]): boolean {
    if (!events) {
      return false;
    }

    return this.isPropertyAvailableService.isPropertyAvailable(
      this.cashOutLabelService.checkCondition).bind(this.cashOutLabelService)(events, [{ cashoutAvail: 'Y' }]
    );
  }

  /**
   * Get sport Id from ribbon for sport route
   * @param {string} targetUriCopy
   * @return {Observable<number>}
   */
  getSportId(targetUriCopy: string): Observable<number> {
    return this._getRibbon().pipe(
      map((ribbonCache: IRibbonCache) => {
        _.each(ribbonCache.data, (item: IRibbonItem) => {
          item.targetUriCopy = this.inPlayStorageService.clearLink(item.targetUriCopy);
        });
        const ribbonSport: IRibbonItem = _.findWhere(ribbonCache.data, { targetUriCopy });
        return ribbonSport ? ribbonSport.categoryId : null;
      }));
  }

  /**
   * Get first sport from ribbon
   * @return {object}
   */
  getFirstSport(ribbonCache): IRibbonItem {
    return ribbonCache.data.find((ribbonItem: IRibbonItem) => {
      return ribbonItem.targetUriCopy !== 'watchlive' && ribbonItem.targetUriCopy !== 'allsports';
    });
  }

  addRibbonURLHandler(): void {
    this._getRibbon()
      .subscribe((ribbonCache: IRibbonCache) => {
        const firstSport: IRibbonItem = this.getFirstSport(ribbonCache);
        const storageSportUri = this.getSportUri();
        const storageSportUriItem = ribbonCache.data.find((ribbonItem: IRibbonItem) => ribbonItem.targetUriCopy === storageSportUri);
        if (storageSportUri && storageSportUriItem) {
          this.router.navigateByUrl(`/in-play/${storageSportUri}`);
        } else {
          this.router.navigateByUrl(`/in-play/${firstSport.targetUriCopy}`);
        }
      });
  }

  /**
   * ShortCut to Init cache
   */
  initSportsCache(): void {
    this.inPlayStorageService.initSportsCache();
  }

  /**
   * Set current sport Uri to Storage
   * @param {object} route, object with custom route params data.
   */
  setSportUri(route: any): void {
    const path = this.location.path();

    if (this.userService.status && path.indexOf('in-play') > 0) {
      const homeInPlay = path === '/in-play/allsports' || path === '/in-play';
      if (route) {
        this.storageService.set(`inPlay-${this.userService.username}`, route);
      } else if (homeInPlay) {
        this.storageService.remove(`inPlay-${this.userService.username}`);
      }
    }
  }

  /**
   * Get sport Uri from Storage and redirect to right URL
   */
  getSportUri(): string {
    let sportUri: string = '';
    if (this.userService.status) {
      sportUri = this.storageService.get(`inPlay-${this.userService.username}`);
    }
    return sportUri;
  }

  /**
   * Provides ribbon data
   * @returns {}
   */
  getRibbonData(removeAllSportsItem = true): Observable<IRibbonCache> {
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.isWatchLiveEnabled = config && config.InPlayWatchLive && config.InPlayWatchLive.enabled;
    });

    return this._getRibbon().pipe(
      map((ribbonCache: IRibbonCache) => {
        this.inPlaySubscriptionManagerService.subscribe4RibbonUpdates();
        ribbonCache.data = this.filterAllSportsRibbonItems(ribbonCache.data, removeAllSportsItem);
        return ribbonCache;
      }));
  }

  /**
   * Provides virtuals sports with live event count
   * @returns {}
   */
  getVirtualsData(): Observable<any> {
    return this._getVirtuals().pipe(
      map((virtualSports: any) => {
        this.inPlaySubscriptionManagerService.subscribe4VirtualsUpdates();
        return virtualSports;
      }));
  }

  /**
   * Performs unsubscription for ribbon and structure updates.
   */
  unsubscribeForUpdates(): void {
    // If In-play widget is available on page - we do not need to unsubscribe for structure changes.
    if (!this.isWidgetEnabled) {
      this.inPlaySubscriptionManagerService.unsubscribe4RibbonUpdates();
      this.inPlaySubscriptionManagerService.unsubscribeForStructureUpdates();
    }
  }

  /**
   * Performs unsubscription for VR Live event updates.
   */
  unsubscribeForVRUpdates(): void {
    this.inPlaySubscriptionManagerService.unsubscribe4VRLiveEventUpdates();
  }



  /**
   * Provides structure data
   * @param {boolean} useCache
   * @return {Observable<IStructureData>}
   */
  getStructureData(useCache: boolean = false, expandUpcoming: boolean = false): Observable<IStructureCacheData> {
    if (!useCache || this.inPlayStorageService.isOutdatedStructure()) {
      return this._getStructure(expandUpcoming).pipe(
        map((structureData: IStructureData) => {
          this.inPlayStorageService.cacheStructure(structureData);
          this.inPlaySubscriptionManagerService.subscribeForStructureUpdates();

          return this.inPlayStorageService.structureCache.data;
        }));
    }

    this.inPlaySubscriptionManagerService.subscribeForStructureUpdates();
    return observableOf(this.inPlayStorageService.structureCache.data);
  }

  /**
   * Provides live stream structure data
   * @param {boolean} useCache
   * @return {Observable<IStructureData>}
   */
  getLiveStreamStructureData(useCache: boolean = false): Observable<IStructureCacheData> {
    if (!useCache || this.inPlayStorageService.isOutdatedStructure()) {
      return this.getLiveStreamStructure().pipe(
        map((liveStreamStructureData: IStructureData) => {
          this.inPlayStorageService.cacheStructure(liveStreamStructureData);
          this.inPlaySubscriptionManagerService.subscribeForStructureUpdates(true);

          return this.inPlayStorageService.structureCache.data;
        }));
    }

    this.inPlaySubscriptionManagerService.subscribeForStructureUpdates(true);
    return observableOf(this.inPlayStorageService.structureCache.data);
  }

  getExpandedLeaguesCount(): Observable<number> {
    if (this.expandedLeaguesCount) {
      return observableOf(this.expandedLeaguesCount);
    }

    return this.cmsService.getSystemConfig(null).pipe(
      map((configData: ISystemConfig) => {
        this.expandedLeaguesCount = Number(configData.InPlayCompetitionsExpanded.competitionsCount);
        return this.expandedLeaguesCount;
      }));
  }

  /**
   * Get parameter fo request data from MS
   * to get livenow/upcoming/livestream events
   * @param filter
   */
  getTopLevelTypeParameter(filter) {
    const filterMap = {
      'livenow': EVENT_TYPES.LIVE_EVENT,
      'upcoming': EVENT_TYPES.UPCOMING_EVENT,
      'liveStream': EVENT_TYPES.STREAM_EVENT,
      'upcomingLiveStream': EVENT_TYPES.UPCOMING_STREAM_EVENT
    };

    return filterMap[filter] || EVENT_TYPES.LIVE_EVENT;
  }

  /**
   * Provides sport data
   * @param {Object} requestParams - contains categoryId , isLiveNowType
   * @param {boolean} useCache
   * @returns {Promise}
   */
  getSportData(requestParams, useCache = true, subscribeForUpdates = true, competitionEvents: boolean = true, isHR: boolean = false, topMarkets?): Observable<ISportSegment> {
    requestParams.emptyTypes = 'Yes';
    requestParams.autoUpdates = 'No';
    if(topMarkets && topMarkets.length && requestParams.isLiveNowType && !(requestParams.marketSelector)) {
      requestParams.marketSelector = topMarkets[0].titleName;
    }

    requestParams.topLevelType = requestParams.topLevelType ||
      (requestParams.isLiveNowType ? EVENT_TYPES.LIVE_EVENT : EVENT_TYPES.UPCOMING_EVENT);
    if (!requestParams.marketSelector && requestParams.categoryId
      && environment.CATEGORIES_DATA.tierOne.includes(requestParams.categoryId.toString())
      && requestParams.isLiveNowType) {
      requestParams.marketSelector = 'Main Market';
    }
    return this._getSport(requestParams).pipe(
      concatMap((sportData: ISportSegment) => {
        this.inPlayStorageService.storeSport(requestParams, sportData);
        if (!this.isLiveUpdatesHandlerAdded) {
          this._addLiveUpdatesHandler();
          this.isLiveUpdatesHandlerAdded = true;
        }
        if(sportData[0] !== undefined){
          sportData = sportData[0];
          sportData.marketSelector = requestParams.marketSelector;
        }

        if (sportData && sportData.eventsByTypeName && sportData.eventsByTypeName.length > 0 && competitionEvents) {
          // get all competitions
          // then expand them all
          return this.initialSubscribeForMultipleCompetitions(sportData, requestParams, subscribeForUpdates, isHR);
        }

        return observableOf(sportData);
      }),
      map((sportData: ISportSegment) => {
        const sportId = requestParams.categoryId;
        const topLevelType = requestParams.topLevelType;
        const competitionChangesHandler = this.handleAddRemoveCompetition(sportId, topLevelType, requestParams.marketSelector);

        if (_.isUndefined(sportData.categoryId)) {
          sportData.categoryId = sportId;
          sportData.topLevelType = topLevelType;
        }

        this.inPlaySubscriptionManagerService.subscribeForSportCompetitionChanges(
          sportId,
          topLevelType,
          requestParams.marketSelector,
          competitionChangesHandler
        );

        return sportData;
      }),
      catchError(err => {
        return throwError(err);
      }));
  }

  initialSubscribeForMultipleCompetitions(sportData: ISportSegment,
                                          requestParams: IRequestParams,
                                          subscribeForUpdates: boolean, isHR:boolean=false): Observable<ISportSegment> {
    const expandedCompetitionsAmount = this.expandedLeaguesCount;
    const competitionsLoadingPromises = [];
    if(isHR) {
      const HREvents = [];
      const competitionsArray = [];
      sportData.eventsByTypeName.forEach((competitionSection: ITypeSegment, compIndex: number) => {
        competitionSection.events.forEach((eventData: ISportEvent)=> {
          HREvents.push(eventData);
        })
        HREvents.sort((event: ISportEvent, nextEvent: ISportEvent) => new Date(event.startTime).getTime() - new Date(nextEvent.startTime).getTime());
      });

      HREvents.forEach((event: ISportEvent, eventIndex: number)=> {
        sportData.eventsByTypeName.forEach((competitionSection: ITypeSegment) => {
          const isExist = competitionsArray.some((competition: ITypeSegment) => competition.typeId === competitionSection.typeId)
          if(event.typeId === competitionSection.typeId && !isExist) {
            const compIndex  = sportData.eventsByTypeName.indexOf(competitionSection);
            competitionsArray.push(sportData.eventsByTypeName[compIndex]);
          }             
        });    
      });
      sportData.eventsByTypeName = competitionsArray;
    }
    

    sportData.eventsByTypeName.forEach((competition, i) => {
      if (requestParams.marketSelector) {
        competition.marketSelector = requestParams.marketSelector;
      }

      if (i < expandedCompetitionsAmount) {
        // ---------
        const competitionId = parseInt(competition.typeId, 10);
        const updatedParams = _.extend(requestParams, {
          typeId: competitionId,
          // flag to detect should we modify markets marketMeaningMinorCode
          // and dispSortName in inPlayDataService(see modifyMainMarkets methods comment)
          modifyMainMarkets: true
        });

        const getCompetitionObservable = this._getCompetitionData(updatedParams, sportData.categoryCode).pipe(
          map((competitionEvents: ISportEvent[]) => {
            if (competitionEvents.length === 0) {
              sportData.eventsByTypeName.splice(i, 1);
            } else {
              this.checkAggregateMarkets(updatedParams, competition, competitionEvents);
              
              const eventIds = competitionEvents.map(event => event.id);
              if (subscribeForUpdates && !isHR) {
                this.inPlaySubscriptionManagerService.subscribeForLiveUpdates(eventIds);
              }
            }

            return competitionEvents;
          }));
          
        competitionsLoadingPromises.push(getCompetitionObservable);
      }
    });

    // forkJoin doesn't emit any value for empty array
    if (!competitionsLoadingPromises.length) {
      return observableOf(sportData);
    }

    return observableForkJoin(competitionsLoadingPromises).pipe(
      map(() => {
        return (this.addExpandLiveStream(null, sportData) as ISportSegment);
      }),
      catchError(err => {
        // GET COMPETITION ERROR
        console.warn(err);
        return throwError(err);
      }));
  }

  checkAggregateMarkets(requestParams: IRequestParams, competition: ITypeSegment, competitionEvents: ISportEvent[]) {
    if(this.isAggregated(requestParams)){
      const eventsList = [];
      [... new Set(competition.eventsIds)].forEach(event => {
        const commonEvent = competitionEvents.filter(ev => ev.id == event);
        const marketsList = commonEvent.map(b => b.markets[0]);
        marketsList.forEach(market => {
          market.name = requestParams.marketSelector;
        });
        commonEvent[0].markets = marketsList;
        eventsList.push(commonEvent[0]);
      });
      return competition.events = eventsList;
    }
    else {
      return competition.events = competitionEvents;
    }
  }

  subscribeForUpdates(competitionEvents: ISportEvent[]): void {
    if (!competitionEvents) { return; }
    const eventIds = competitionEvents.map((event: ISportEvent) => event.id);
    this.inPlaySubscriptionManagerService.subscribeForLiveUpdates(eventIds);
  }

  unsubscribeForSportCompetitionUpdates(sportData: ISportSegment): void {
    if (!sportData) {
      return;
    }
    const sportId = sportData.categoryId;
    const topLevelType = sportData.topLevelType;

    this.inPlaySubscriptionManagerService.unsubscribeForSportCompetitionChanges(sportId, topLevelType);
    if (sportData.eventsIds) {
      this.inPlayStorageService.removeEvents(sportData.eventsIds);
    }
  }

  /**
   * Unsubscribes for live updates for given event ids.
   * @private
   */
  unsubscribeForEventsUpdates(sportOrCompetitionObject: ISportSegment | ITypeSegment, clearStorage: boolean = true): void {
    const eventsIds = sportOrCompetitionObject.eventsIds;
    if (eventsIds) {
      this.inPlaySubscriptionManagerService.unsubscribeForLiveUpdates(eventsIds);
      clearStorage && this.inPlayStorageService.removeEvents(eventsIds);
    }
  }

  /**
   * Unsubscribes for live updates for given event.
   * @param sportOrCompetitionObject {ISportEvent} 
   * @param clearStorage {boolean} 
   */
  unsubscribeForEventUpdates(sportOrCompetitionObject: ISportEvent, clearStorage: boolean = true): void {
    const eventsIds = [sportOrCompetitionObject.id];
    if (eventsIds) {
      this.inPlaySubscriptionManagerService.unsubscribeForLiveUpdates(eventsIds);
      clearStorage && this.inPlayStorageService.removeEvents(eventsIds);
    }
  }

  /**
   * Remove sport and league and events from sport data
   * @param data {Object} as Structure Data
   * @param id {number} - event Id
   * @param viewByFilters {Array} - of filters
   */
  clearDeletedEventFromSport(data: IStructureData | ISportSegment, id: number, viewByFilters: string[]): void {
    const viewByFilter = viewByFilters.filter(vBF => _.contains(data[vBF].eventsIds, id)).toString();
    if (!viewByFilter || !data[viewByFilter]) {
      return;
    }
    const eventsByGroup = data[viewByFilter];
    const sportIndex = this.getLevelIndex(eventsByGroup.eventsBySports, 'eventsIds', id);

    if (sportIndex !== undefined) {
      const sport = eventsByGroup.eventsBySports[sportIndex];
      if (sport.eventsByTypeName.length) {
        this.clearDeletedEventFromType(sport, id);
      } else {
        sport.eventsIds = sport.eventsIds.filter(eId => eId !== id);
      }
      if (!sport.eventsIds.length) {
        eventsByGroup.eventsBySports.splice(sportIndex, 1);
      }
      eventsByGroup.eventsIds = eventsByGroup.eventsIds.filter(eId => eId !== id);
    }
  }

  /**
   * Remove league and events from sport data
   * @param data {Object} as Sport Data
   * @param eventId {number} - event Id
   */
  clearDeletedEventFromType(data: ISportSegment, eventId: number): void {
    const typeNameIndex = this.getLevelIndex(data.eventsByTypeName, 'eventsIds', eventId);

    if (typeNameIndex === undefined) {
      return;
    }
    const typeName = data.eventsByTypeName[typeNameIndex];
    const eventIndex = typeName && typeName.events && this.getLevelIndex(typeName.events, 'id', eventId);
    const eventsLength = typeName.eventsIds.length;

    if (eventIndex >= 0 && eventsLength === 1) {
      this.unsubscribeAndRemoveCompetition(data.topLevelType, data.categoryId, typeName.typeId);
    } else if (eventIndex !== undefined) {
      this._deleteEntity(typeName, 'events', eventIndex, eventId);
    }

    data.eventsIds = data.eventsIds.filter(eId => eId !== eventId);
  }

  /**
   * Calculate level index for event hierarchy
   * @param {array} entitiesArray
   * @param {string} propName
   * @param {number} eventId
   * @returns {number}
   */
  getLevelIndex(entitiesArray: ITypeSegment[] | ISportEvent[], propName: string, eventId: number): number {
    const arrLength = entitiesArray.length;

    for (let i = 0; i < arrLength; i++) {
      if (_.contains(entitiesArray[i][propName], eventId) || entitiesArray[i][propName] === eventId) {
        return i;
      }
    }
  }

  /**
   * Calculates filter value for change it after widget renew
   * @param viewByFilters
   * @returns {*}
   */
  getFilter(viewByFilters: string[]): string {
    const searchString = this.windowRef.nativeWindow.location.search;
    const isInplayTab = searchString.indexOf('tab=InPlay') >= 0;
    const inPlaySegment = this.routingState.getRouteParam('sport', this.route.snapshot).toLowerCase().replace(/-/g, '');
    const isInPlaySegment = inPlaySegment.indexOf('inplay') !== -1 ||
      this.routingState.getRouteParam('display', this.route.snapshot) === 'live';
    const filterInsex = (isInplayTab || isInPlaySegment) ? 1 : 0;

    return viewByFilters[filterInsex];
  }

  /**
   * Is available events in data structure
   * @param {Object} structureData
   * @param {Array} filters
   * return {Boolean}
   */
  areEventsAvailable(structureData: IStructureData, filters: string[]): boolean {
    return filters.some((filter: string) => this._isEventsInViewAvailable(structureData, filter));
  }

  publishEventCount(filter) {
    this.pubSubService.publish(this.pubSubService.API.EVENT_COUNT, filter);
  }

  /**
   * Generates switcher data
   * @param {function} onClickFn
   * @param {array} viewByFilters
   * @param {Object} data
   * @returns {[*,*]}
   */
  generateSwitchers(onClickFn: Function, viewByFilters: string[], data: IRibbonItem[], sportId?: number): ISwitcherConfig[] {
    const counter = this._getEventsCounter(data, sportId);
    return [{
      onClick: () => {
        onClickFn(viewByFilters[0]);
        this.publishEventCount(viewByFilters[0]);
      },
      viewByFilters: viewByFilters[0],
      name: 'inplay.byLiveNow',
      eventCount: counter && counter.livenow || counter && counter.liveStream
    }, {
      onClick: () => {
        onClickFn(viewByFilters[1]);
        this.publishEventCount(viewByFilters[1]);
      },
      viewByFilters: viewByFilters[1],
      name: 'inplay.byUpcoming',
      eventCount: counter && counter.upcoming || counter && counter.upcomingLiveStream
    }];
  }

  /**
   * Stores in-play widget state - whether widget is enabled or disabled.
   * @param {boolean} state
   */
  saveWidgetState(state: boolean): void {
    this.isWidgetEnabled = state;
  }

  /**
   * Load competition data from Microservice
   * @param {object} requestParams
   * @param {string} sportName
   * @private
   */
  _getCompetitionData(requestParams: IRequestParams, sportName: string): Observable<ISportEvent[]> {
    return this.inPlayDataService.loadData('competition', requestParams).pipe(
      map((competitionEvents: ISportEvent[]) => {
        if (!Array.isArray(competitionEvents)) {
          return [];
        }

        this.inPlayStorageService.resetCompetitionEvents(
          requestParams.topLevelType,
          requestParams.categoryId,
          requestParams.typeId,
          this.isAggregated(requestParams),
          competitionEvents);

        if (sportName) {
          this.updateCommentsDataFormat(sportName, competitionEvents);
        }

        this._addClockData(competitionEvents);

        return competitionEvents;
      }));
  }

  /**
   * Update eventsCount value for each sport
   * @param structure - structure of inplay page data
   * @param filter - indicator whether it is upcoming of livenow events count
   * @param eventCountersByCategory - event counters for each sport
   * @param isLiveStream - indicator whether it is livestream page
   */
  updateEachSportCounter(structure: ISportSegment, filter: string, eventCountersByCategory: IEventCounterMap,
                         isLiveStream: boolean): void {
    const eventsBySports = structure[filter].eventsBySports;
    if (!eventsBySports) {
      return;
    }
    eventsBySports.forEach((sport: ISportSegment) => {
      const currentCounter = eventCountersByCategory[sport.categoryId];
      const formatCount = count => Number((count || '').replace(/[()]/g, ''));
      if (!currentCounter) {
        return;
      }
      if (filter === 'livenow') {
        sport.eventCount = formatCount(isLiveStream ? currentCounter.liveStream : currentCounter.livenow);
        return;
      }
      if (filter === 'upcoming') {
        sport.eventCount = formatCount(isLiveStream ? currentCounter.upcomingLiveStream : currentCounter.upcoming);
      }
    });
  }

  updateEventsCounter(structure, filters: string[], eventsCounter: IEventCounter,
                      eventCountersByCategory: IEventCounterMap, isLiveStream: boolean = false,
                      type?: string): void {
      _.each(filters, (filter: string) => {
        const counter = Number(eventsCounter[filter]);
        if (!isNaN(counter) && structure[filter]) {
          structure[filter].eventCount = counter;
          this.updateEachSportCounter(structure, filter, eventCountersByCategory, isLiveStream);
        }
      });
      this.pubSubService.publish(`${this.pubSubService.API.EVENT_BY_SPORTS_CHANNEL}_${type}`, structure);
  }

  getEventCountersByCategory(data: IRibbonItem[]): IEventCounterMap {
    return data.reduce((obj, ribbonItem) =>
      Object.assign(obj, {[ribbonItem.categoryId]: this.getSingleEventCounter(ribbonItem) }), {});
  }

  getUnformattedEventsCounter(data: IRibbonItem[], sportId?: number): IEventCounter {
    return this._getEventsCounter(data, sportId, false);
  }

  /**
   * Get sport config for sport, and empty object for racing
   * @param sportName
   * @returns {Observable<GamingService | {}>}
   */
  getSportConfigSafe(sportName: string): Observable<GamingService | {}> {
    return new Observable((observer: Observer<GamingService | {}>) => {
      this.sportsConfigService.getSport(sportName).pipe(finalize(() => {
        observer.complete();
      }))
        .subscribe((data: GamingService) => {
          observer.next(data);
        }, () => observer.next({}));
    });
  }

  getSportName(sportSection: ISportSegment): string {
    return (sportSection.categoryPath || '').replace(/-/g, '');
  }

  extendSectionWithSportInstance(sportSection: ISportSegment, sportInstance: GamingService | { config?: { tier?: number } }): void {
    sportSection.tier = sportInstance?.config?.tier;
    sportSection.isTierOneSport = sportSection.tier === 1;
  }

  /**
   * returns filters array that should be applied to RibbonData (made fo easier extend)
   */
  protected getFiltersForRibbonData(): Function[] {
    return [this.filterAllSportsRibbonItems];
  }

  /**
   * returns modifiersData functions in array for _getStructure function to be able to run/apply them one by one
   */
  protected getStructureDataModifiers(): Function[] {
    return [this._filterShowInPlay, this._addExpandProperties];
  }

  /**
   * returns modifiersData functions in array for getLiveStreamStructure function to be able to run/apply them one by one
   */
  protected getLiveStreamStructureDataModifiers(): Function[] {
    return [this.filterLiveStreamInPlay, this.addExpandLiveStream];
  }

  /**
   * Get ribbonData and filter "Allsports" menu item in ribbonData if WatchLive is enabled
   * @param {IRibbonItem[]} data
   * @param {boolean} isWatchLive
   * @returns {IRibbonItem[]}
   */
  private filterAllSportsRibbonItems(data: IRibbonItem[], removeAllSportsItem = true): IRibbonItem[] {
    if (!this.isWatchLiveEnabled) { return data; }

    if (data && data[0] && data[0].categoryId !== watchLiveItem.categoryId) {
      data.unshift(watchLiveItem);
    }
    return removeAllSportsItem
      ? data.filter((menuItem: IRibbonItem) => menuItem.targetUriCopy !== 'allsports')
      : data;
  }

  /**
   * Subscribe for websockets messages
   * @private
   */
  private _addLiveUpdatesHandler(): void {
    this.pubSubService.subscribe('inplayLiveUpdate', this.pubSubService.API.WS_EVENT_LIVE_UPDATE,
      (eventId, message) => {
        this._handleLiveUpdate(eventId, message);
      });
  }

  /**
   * get ribbon data from service
   * @private
   */
  private _getRibbon(): Observable<IRibbonCache> {
    if (this.inPlayStorageService.isOutdatedRibbon()) {
      if (!this.ribbonLoaded$ || this.ribbonLoaded$.isStopped) {
        this.ribbonLoaded$ = new Subject();
        this.loadDataSubscription = this.inPlayDataService.loadData('ribbon', null)
          .subscribe((ribbonData: IRibbonData) => {
            ribbonData.items = this.getFilteredRibbonData(ribbonData.items, ...this.getFiltersForRibbonData());
            this.inPlayStorageService.cacheRibbon(ribbonData);
            this.ribbonLoaded$.next(this.inPlayStorageService.ribbonCache);
            this.ribbonLoaded$.complete();
            this.loadDataSubscription.unsubscribe();
          }, () => {
            this.ribbonLoaded$.next(this.inPlayStorageService.ribbonCache);
            this.ribbonLoaded$.complete();
          });
      }
      return this.ribbonLoaded$.asObservable();
    }

    return observableOf(this.inPlayStorageService.ribbonCache);
  }

  /**
   * get virtual live count data from service
   * @private
   */
  private _getVirtuals(): Observable<any> {
    return this.inPlayDataService.loadData('virtuals', null).pipe(
      map((structureData: IStructureData) => {
        return structureData;
      }));
  }

  /**
   * run functions one by one. Processed data used as argument for next function.
   * @param ribbonDataItems
   * @param filters
   */
  private getFilteredRibbonData(ribbonDataItems: IRibbonItem[] | any, ...filters: Function[]): IRibbonItem[] {
    return filters.reduce((accumulator: IRibbonItem[], currFn: Function) => currFn(accumulator), ribbonDataItems);
  }

  /**
   * Handles live updates for events.
   * @param {string} eventId
   * @param {IWSLiveUpdate} updateBody
   * @private
   */
  private _handleLiveUpdate(eventId: string, updateBody: IWSLiveUpdate): void {
    if (!this.inPlayStorageService.allEvents) {
      return;
    }

    const eventsToUpdate = this.inPlayStorageService.allEvents[eventId] ? [this.inPlayStorageService.allEvents[eventId]] : [];

    /**
     * Trigger to update events in wsUpdateEventFactory
     * {array} events - "inplay" filtered events with specific ID from update,
     * {object} updateDetails - ws update object
     */
    this.pubSubService.publish(this.pubSubService.API.WS_EVENT_UPDATE, {
      events: eventsToUpdate,
      update: updateBody
    });
  }

  /**
   * get structure data from service
   * @returns {Promise.<TResult>|*}
   * @private
   */
  private _getStructure(expandUpcoming: boolean = false): Observable<IStructureData> {
    return this.inPlayDataService.loadData('structure', null).pipe(
      map((structureData: IStructureData) => {
        if (structureData) {
          this.applyStructureDataModifiers([structureData, undefined, expandUpcoming], this.getStructureDataModifiers());
        }
        return structureData;
      }));
  }

  /**
   * Run functions one by one with the same attributes for all functions
   * @param data
   * @param fns
   */
  private applyStructureDataModifiers(data: any, fns: any) {
    fns.forEach(fn => fn(...data));
  }

  /**
   * get live stream structure data from micro-service
   */
  private getLiveStreamStructure(): Observable<IStructureData> {
    return this.inPlayDataService.loadData('ls_structure', null).pipe(
      map((liveStreamStructureData: IStructureData) => {
        if (liveStreamStructureData) {
          this.applyStructureDataModifiers([liveStreamStructureData], this.getLiveStreamStructureDataModifiers());
          watchLiveItem.liveStreamEventCount = liveStreamStructureData.liveStream.eventCount;
          watchLiveItem.upcommingLiveStreamEventCount = liveStreamStructureData.upcomingLiveStream.eventCount;
        }

        return liveStreamStructureData;
      }));
  }

  /**
   * Filter sports structure only for sports that should be shown on inPlay page
   * @param structureData
   * @returns {*}
   * @private
   */
  private _filterShowInPlay(structureData: IInplayAllSports): IInplayAllSports {
    // error handling
    if (_.has(structureData, 'error')) {
      return structureData;
    }

    inplayConfig.viewByFilters.forEach((filter: string) => {
      this.filterSports(structureData, filter);
    });

    return structureData;
  }

  /**
   * Filter sports structure only for sports that should be shown on inPlay page
   * @param structureData
   * @returns {*}
   * @private
   */
  private filterLiveStreamInPlay(structureData: IInplayAllSports): IInplayAllSports {
    // error handling
    if (_.has(structureData, 'error')) {
      return structureData;
    }

    inplayLiveStreamConfig.viewByFilters.forEach((filter: string) => {
      this.filterSports(structureData, filter);
    });

    return structureData;
  }

  /**
   * Remove Sports, which have showInPlay property with Falsy value
   * @param structureData
   * @param filter
   */
  private filterSports(structureData: IInplayAllSports, filter: string) {
    if (structureData[filter]) {
      structureData[filter].eventsBySports = structureData[filter].eventsBySports.filter(s => s.showInPlay);
    }
  }

  /**
   * get sport data from service
   * @param params
   * @returns {Promise.<TResult>|*}
   * @private
   */
  private _getSport(params: IRequestParams): Observable<ISportSegment|any> {
    return this.getExpandedLeaguesCount().pipe(
      concatMap(() => {
        return this.inPlayDataService.loadData('sports', params);
      }));
  }

  /**
   * Expand Sports of Competitions tab, according to CMS config
   * @param {object?} inplaySructureData
   * @param {object?} sportStructureData
   * @private
   */
  private _addExpandProperties<T>(inplaySructureData?: IInplayAllSports,
                                  sportStructureData?: ISportSegment,
                                  expandUpcoming: boolean = false): IInplayAllSports | ISportSegment {
    const expandedSportsCount = inplayConfig.expandedSportsCount;
    // sports list
    if (inplaySructureData) {
      for (let i = expandedSportsCount - 1; i >= 0; i--) {
        if (inplaySructureData.livenow && inplaySructureData.livenow.eventsBySports[i]) {
          inplaySructureData.livenow.eventsBySports[i].isExpanded = true;
        }

        if (expandUpcoming && inplaySructureData.upcoming && inplaySructureData.upcoming.eventsBySports[i]) {
          inplaySructureData.upcoming.eventsBySports[i].isExpanded = true;
        }
      }
      return inplaySructureData;
    }

    // sport competitions
    if (sportStructureData) {
      for (let i = this.expandedLeaguesCount - 1; i >= 0; i--) {
        if (sportStructureData.eventsByTypeName[i]) {
          sportStructureData.eventsByTypeName[i].isExpanded = true;
        }
      }

      return sportStructureData;
    }
  }

  /**
   * Expand Sports of Competitions tab, according to CMS config
   * @param {object?} inplaySructureData
   * @param {object?} sportStructureData
   * @private
   */
  private addExpandLiveStream<T>(inplaySructureData?: IInplayAllSports,
                                 sportStructureData?: ISportSegment): IInplayAllSports | ISportSegment {
    const expandedSportsCount = inplayLiveStreamConfig.expandedSportsCount;
    // sports list
    if (inplaySructureData) {
      for (let i = expandedSportsCount - 1; i >= 0; i--) {
        if (inplaySructureData.liveStream && inplaySructureData.liveStream.eventsBySports[i]) {
          inplaySructureData.liveStream.eventsBySports[i].isExpanded = true;
        }

        if (inplaySructureData.upcomingLiveStream && inplaySructureData.upcomingLiveStream.eventsBySports[i]) {
          inplaySructureData.upcomingLiveStream.eventsBySports[i].isExpanded = true;
        }
      }
      return inplaySructureData;
    }

    // sport competitions
    if (sportStructureData) {
      for (let i = this.expandedLeaguesCount - 1; i >= 0; i--) {
        if (sportStructureData.eventsByTypeName[i]) {
          sportStructureData.eventsByTypeName[i].isExpanded = true;
        }
      }
      return sportStructureData;
    }
  }

  /**
   * Update comments data format(adapt for UI templates)
   * @param {string} sportName
   * @param {array} competitionEvents - list of events
   * @returns {*}
   * @private
   */
  private updateCommentsDataFormat(sportName: string, competitionEvents: ISportEvent[]): ISportEvent[] {
    const methodName = `${sportName.toLowerCase()}MSInitParse`;
    const updater = this.commentsService[methodName];

    _.each(competitionEvents, (event: ISportEvent) => {
      if (event.comments && updater) {
        updater(event.comments);
      }
    });

    return competitionEvents;
  }

  /**
   * Decorate events with clock
   * @param {ISportEvent[]} competitionEvents
   * @private
   */
  private _addClockData(competitionEvents: ISportEvent[]): void {
    const serverTimeDelta = this.timeSyncService.getTimeDelta();

    competitionEvents.forEach(e => {
      if (e.initClock) {
        const clockData = e.initClock;

        // TODO move this initialisation to liveClock directive
        e.clock = this.liveEventClockProviderService.create(serverTimeDelta, clockData);
      }
    });
  }

  /**
   * Delete entity from particular level
   * @param group
   * @param propName
   * @param index
   * @param eventId
   * @private
   */
  private _deleteEntity(group: ITypeSegment, propName: string, index: number, eventId: number): void {
    group[propName].splice(index, 1);
    group.eventsIds = group.eventsIds.filter((groupEventId: number) => groupEventId !== eventId);

    if (propName === 'events') {
      this.inPlaySubscriptionManagerService.unsubscribeForLiveUpdates([eventId]);
    }
  }

  /**
   * Is available events in data structure
   * @param {IStructureData} structureData
   * @param {string} filter
   * @return {boolean}
   * @private
   */
  private _isEventsInViewAvailable(structureData: IStructureData, filter: string): boolean {
    return _.has(structureData[filter], 'eventsIds') && structureData[filter].eventsIds.length;
  }

  private getSingleEventCounter(ribbnSportData: IRibbonItem, format: boolean = true): IEventCounter {
    const liveEventCount = ribbnSportData && ribbnSportData.liveEventCount;
    const upcomingEventCount = ribbnSportData && ribbnSportData.upcomingEventCount;
    const liveStreamEventCount = ribbnSportData && ribbnSportData.liveStreamEventCount;
    const upcommingLiveStreamEventCount = ribbnSportData && ribbnSportData.upcommingLiveStreamEventCount;

    if (!format) {
      return {
        livenow: liveEventCount && liveEventCount.toString(),
        upcoming: upcomingEventCount && upcomingEventCount.toString(),
        liveStream: liveStreamEventCount && liveStreamEventCount.toString(),
        upcomingLiveStream: upcommingLiveStreamEventCount && upcommingLiveStreamEventCount.toString()
      };
    }
    return {
      livenow: liveEventCount && liveEventCount > 0 && `(${liveEventCount})`,
      upcoming: upcomingEventCount && upcomingEventCount > 0 && `(${upcomingEventCount})`,
      liveStream: liveStreamEventCount && liveStreamEventCount > 0 && `(${liveStreamEventCount})`,
      upcomingLiveStream: upcommingLiveStreamEventCount && upcommingLiveStreamEventCount > 0 && `(${upcommingLiveStreamEventCount})`
    };
  }

  /**
   * Get Events Counter (livenow, upcoming)
   * @param {Boolean} isWidget
   * @param {Object} data
   * @returns {{livenow: string, upcoming: string}}
   * @private
   */
  private _getEventsCounter(data: IRibbonItem[], sportId?: number, format: boolean = true): IEventCounter {
    let ribbnSportData;
    if (sportId) {
      ribbnSportData = _.findWhere(data, { categoryId: +sportId });
    } else {
      let routeName = this.routingState.getPathName();

      if (routeName === 'in-play') {
        routeName = 'allsports';
      } else if (routeName === 'live-stream') {
        routeName = 'watchlive';
      }

      ribbnSportData = _.findWhere(data, { targetUriCopy: routeName });
    }
    return this.getSingleEventCounter(ribbnSportData, format);
  }


  /**
   * Handle ws messages where new competition added or present competition removed
   * @param sportId
   * @param topLevelType
   * @param marketSelector
   * @returns {Function}
   */
  private handleAddRemoveCompetition(
    sportId: string,
    topLevelType: string,
    marketSelector?: string
  ): (websocketData: ICompetitionChangeMessage) => void {
    return (websocketData: ICompetitionChangeMessage) => {
      const addedCompetition = websocketData.added;
      const changedCompetitions = websocketData.changed;
      const removedCompetitionIds = websocketData.removed;

      if (removedCompetitionIds && removedCompetitionIds.length > 0) {
        removedCompetitionIds.forEach((competitionId: string | number) => {
          this.unsubscribeAndRemoveCompetition(topLevelType, sportId, competitionId as string);
        });
      }

      if (addedCompetition && Object.keys(addedCompetition).length) {
        Object.keys(addedCompetition).forEach((id: string) => {
          const competitionObject: ITypeSegment = addedCompetition[id];

          this.getAndUpdateCompetitionData(false, sportId, topLevelType, id, competitionObject, marketSelector);
        });
      }

      if (changedCompetitions && changedCompetitions.length > 0) {

        changedCompetitions.forEach((id: string) => {
          const competitionObject: ITypeSegment = this.inPlayStorageService.getSportCompetition(topLevelType, sportId, id);

          if (!(competitionObject?.isExpanded || sportId.toString() === environment.HORSE_RACING_CATEGORY_ID)) {
            this.callSpecificAndCommonCallbacks('INPLAY_COMPETITION_UPDATED', undefined, sportId, topLevelType);
            return;
          }

          this.getAndUpdateCompetitionData(true, sportId, topLevelType, id, competitionObject, marketSelector);
        });
      }
    };
  }

  /**
   * Get Competition Data and update storage
   * subscribe/unsubscribe for updates if changed
   * emit method
   * @param changed
   * @param sportId
   * @param topLevelType
   * @param typeId
   * @param competitionObject
   * @param marketSelector
   * @param {Boolean} modifyMainMarkets - flag to detect should we modify markets marketMeaningMinorCode
   * and dispSortName in inPlayDataService(see modifyMainMarkets methods comment)
   */
  private getAndUpdateCompetitionData(
    changed: boolean,
    sportId: string,
    topLevelType: string,
    typeId: string,
    competitionObject: ITypeSegment,
    marketSelector?: string,
    modifyMainMarkets: boolean = true
  ): void {
    const requestParams: IRequestParams = {
      categoryId: sportId,
      isLiveNowType: topLevelType === EVENT_TYPES.LIVE_EVENT || topLevelType === EVENT_TYPES.STREAM_EVENT,
      topLevelType,
      typeId,
      modifyMainMarkets: modifyMainMarkets
    };

    if (marketSelector) {
      requestParams.marketSelector = marketSelector;
    }

    this._getCompetitionData(requestParams, competitionObject.categoryCode)
      .subscribe((competitionEvents: ISportEvent[]) => {
        const updatedEventIds: number[] = competitionEvents.map((event: ISportEvent) => event.id);
        const method: string = changed ? 'INPLAY_COMPETITION_UPDATED' : 'INPLAY_COMPETITION_ADDED';
        const args: ITypeSegment = changed ? undefined : competitionObject;

        if (changed) {
          const removedEventIds: number[] = competitionObject.eventsIds.filter((eventId: number) => !updatedEventIds.includes(eventId));
          const addedEvents: ISportEvent[] = competitionEvents.filter(
            (event: ISportEvent) => !competitionObject.eventsIds.includes(event.id)
          );

          if (removedEventIds.length) {
            this.inPlaySubscriptionManagerService.unsubscribeForLiveUpdates(removedEventIds);
          }

          if (addedEvents.length) {
            this.subscribeForUpdates(addedEvents);
          }
        }

        competitionObject.events = competitionEvents;
        competitionObject.eventsIds = updatedEventIds;

        // Add loaded competition to sport and subscribe for new events live updates
        this.inPlayStorageService.addCompetition(topLevelType, sportId, competitionObject, this.isAggregated(requestParams));

        this.callSpecificAndCommonCallbacks(method, args, sportId, topLevelType);
      });
  }

  private callSpecificAndCommonCallbacks(method: string, args: any, sportId: string, topLevelType: string): void {
    if (method === 'INPLAY_COMPETITION_REMOVED') {
      this.pubSubService.publish(method, args);
      this.pubSubService.publish(`${method}:${sportId}:${topLevelType}`, args);
    }
    this.pubSubService.publish(method, args);
    this.pubSubService.publish(`${method}:${sportId}:${topLevelType}`, args);
  }

  /**
   * Remove competition from sport and usubscribe for all his events updates
   * @param topLevelType
   * @param sportId
   * @param competitionId
   */
  private unsubscribeAndRemoveCompetition(topLevelType: string, sportId: string, competitionId: string): void {
    const competitionObject = this.inPlayStorageService.getSportCompetition(topLevelType, sportId, competitionId);

    if (competitionObject) {
      this.inPlaySubscriptionManagerService.unsubscribeForLiveUpdates(competitionObject.eventsIds);
      this.inPlayStorageService.removeCompetition(topLevelType, sportId, competitionId);
      this.callSpecificAndCommonCallbacks('INPLAY_COMPETITION_REMOVED', competitionObject, sportId, topLevelType);

      // call event to reset expanded competitions flags in sport controller.
      this.pubSubService.publish(this.pubSubService.API.INPLAY_DATA_RELOADED);
    }
  }

  isAggregated(requestParams: IRequestParams): boolean {
    return requestParams['marketSelector'] && requestParams['marketSelector'].split(',').length > 1;
  } 
  
}
