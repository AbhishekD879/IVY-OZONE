import { Injectable } from '@angular/core';
import { InplayApiModule } from '@app/inPlay/inplay-api.module';
import * as _ from 'underscore';

import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { inplayCacheConfig } from '@app/inPlay/constants/config';
import { watchLiveItem } from '@app/inPlay/constants/watch-live-ribbon.constant';
import { WsUpdateEventService } from '@core/services/wsUpdateEvent/ws-update-event.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

import { IRequestParams } from '@app/inPlay/models/request.model';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { IRibbonCache, IRibbonData, IRibbonItem } from '@app/inPlay/models/ribbon.model';
import {
  IStructureCache,
  IStructureData,
  IStructureTopLevelTypeData
} from '@app/inPlay/models/structure.model';
import { ISportDataStorage } from '@app/inPlay/models/sport-data.model';
import { ISystemConfig } from '@core/services/cms/models';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { EVENT_TYPES_BY_TOP_LEVEL } from '@app/inPlay/constants/event-types.constant';

@Injectable({
  providedIn: InplayApiModule
})
export class InPlayStorageService {
  /**
   * intervals for ribbon and structure cache
   * @type {{ribbonCache: *, structureCache: *}}
   */
  intervals = {
    ribbonCache: inplayCacheConfig.cacheInterval,
    sportCache: inplayCacheConfig.sportCacheInterval,
    structureCache: inplayCacheConfig.cacheInterval
  };

  /**
   * Ribbon cache object
   * @type {{data: Array, lastUpdated: number}}
   */
  ribbonCache: IRibbonCache = {
    data: [],
    lastUpdated: 0
  };

  /**
   * Stracture cache object
   * @type {{data: Array, lastUpdated: number}}
   */
  structureCache: IStructureCache = {
    data: {},
    lastUpdated: 0
  };

  /**
   * sport Data Cache
   * @type {{}}
   */
  sportDataCache: ISportDataStorage;

  /**
   * All events Cache separated by widget(area) name
   * @type Object - properties are widget(modules) names
   */
  allEvents: {};

  /**
   * Timeout for cache to remove them after view were destroyed
   * @type number
   */
  timeOuts: number;

  /**
   * Get cms 'enabled' checkbox value for 'Watch Live' tab
   * @type boolean
   */
  isWatchLiveEnabled: boolean;

  /**
   * check if it's home screen
   */
  isHomeScreen: boolean;

  // cached system config
  systemConfig: ISystemConfig;

  constructor(
    private windowRef: WindowRefService,
    private pubsubService: PubSubService,
    private wsUpdateEventService: WsUpdateEventService,
    private cmsService: CmsService,
    private routingState: RoutingState
  ) {
    this.wsUpdateEventService.subscribe();
    this.clearLink = this.clearLink.bind(this);
    this.onRibbonUpdate = this.onRibbonUpdate.bind(this);
  }

  /**
   * Checks is lastUpdate expired
   * @param lastUpdated
   * @param timeInterval
   * @returns {boolean}
   */
  isOutDated(lastUpdated: number, timeInterval: number): boolean {
    return (Date.now() > lastUpdated + timeInterval);
  }

  /**
   * Cache the ribbon data and returns them cached
   * @param {object} ribbonData
   * @returns {}
   */
  cacheRibbon(ribbonData: IRibbonData): IRibbonCache {
    if (ribbonData) {
      _.each(ribbonData.items, (item: IRibbonItem) => {
        item.targetUri = this.clearLink(item.targetUri);
        item.targetUriCopy = this.clearLink(item.targetUriCopy);
      });

      this.ribbonCache.data = ribbonData.items;
      this.ribbonCache.lastUpdated = Date.now();
    }

    return this.ribbonCache;
  }
  
  /**
   * Callback with closure that updates virtual data from subscriber
   * @returns void
   */
  onVirtualsUpdate(virtualsData: any): void {
    this.pubsubService.publish(this.pubsubService.API.VIRTUAL_EVENT_COUNT_UPDATE, [virtualsData]);
  }

  /**
   * Callback with closure that updates ribbon cache on ribbon updates from subscriber
   * @returns void
   */
  onRibbonUpdate(ribbonData?: IRibbonData): void {
    if (this.systemConfig) {
      this.updateRibbonData(ribbonData);
    } else {
      this.cmsService.getSystemConfig()
        .subscribe((config: ISystemConfig) => {
          this.systemConfig = config;
          this.isWatchLiveEnabled = config && config.InPlayWatchLive && config.InPlayWatchLive.enabled;

          this.updateRibbonData(ribbonData);
        });
    }
  }

  updateRibbonData(ribbonData: IRibbonData): void {
    this.updateUniqueTabsData(ribbonData);

    _.each(ribbonData.items, (item: IRibbonItem) => {
      item.targetUri = this.clearLink(item.targetUri);
      item.targetUriCopy = this.clearLink(item.targetUriCopy);
    });

    this.pubsubService.publish(this.pubsubService.API.EVENT_COUNT_UPDATE, [ribbonData.items]);

    this.ribbonCache.data = ribbonData.items;
    this.ribbonCache.lastUpdated = Date.now();
  }

  updateUniqueTabsData(ribbonData: IRibbonData): void {
    const routeUrl = this.routingState.getCurrentUrl();
    const isWatchLiveTab = ['/in-play/watchlive', '/live-stream', '/home/live-stream'].includes(routeUrl);
    const isHomeInplayTabUrl = routeUrl === '/home/in-play';
    const allsportTabData = ribbonData.items[0].categoryId === 0 ? ribbonData.items[0] : null;

    this.isHomeScreen = routeUrl === '/';

    // insert watchlive tab
    if (ribbonData.items[0].categoryId !== watchLiveItem.categoryId && this.isWatchLiveEnabled && !this.isHomeScreen) {
      ribbonData.items.unshift(watchLiveItem);
    }

    // apply updated livestream events counters
    if (isWatchLiveTab && allsportTabData) {
      watchLiveItem.liveStreamEventCount = allsportTabData.liveStreamEventCount;
      watchLiveItem.upcommingLiveStreamEventCount = allsportTabData.upcommingLiveStreamEventCount;
    }

    // leave allsports tab for home - inplay tab, to get counters update.
    if (!isHomeInplayTabUrl) {
      ribbonData.items = _.filter(ribbonData.items, (menuItem: IRibbonItem) => menuItem.targetUriCopy !== 'allsports');
    }
  }

  /**
   * Creates callback with closure for updates of sport structure.
   * @return {Function}
   */
  onStructureUpdate(structureData: IStructureCache) {
    _.each(inplayCacheConfig.viewByFilters, (filter: string) => {
      if (this.structureCache.data[filter] && !_.isEmpty(this.structureCache.data[filter]) && structureData[filter]) {
        this.updateSportCategories(this.structureCache.data[filter], structureData[filter]);
      }
    });
  }

  /**
   * Cache structure data and returns cached structure
   * @param {} structureData
   * @returns {}
   */
  cacheStructure(structureData: IStructureData): void {
    if (structureData) {
      _.each(inplayCacheConfig.viewByFilters, (filter: string) => {
        if (structureData[filter]) {
          this.structureCache.data[filter] = structureData[filter];
        }
      });

      this.structureCache.lastUpdated = Date.now();
    }
  }

  /**
   * Update and sync eventsBySports in structureCache
   * @param sportData
   * @param topLevelType
   * @param categoryId
   */
  updateStructureCacheSportData(sportData: ISportSegment, topLevelType: string, categoryId: string): void {
    const sportType = EVENT_TYPES_BY_TOP_LEVEL[topLevelType];
    if (!this.structureCache.data[sportType]) {
      return;
    }
    const eventsBySportsCached = this.structureCache.data[sportType].eventsBySports;
    const index: number = _.findIndex(eventsBySportsCached, (el: ITypeSegment) => el.categoryId === categoryId);

    _.keys(eventsBySportsCached[index]).forEach((key: string) => {
      if (sportData[key]) { return; }
      sportData[key] = eventsBySportsCached[index][key];
    });

    eventsBySportsCached[index] = sportData;

    this.structureCache.lastUpdated = Date.now();
  }

  /**
   * Initiate Cache by creating cache's
   */
  initSportsCache(): void {
    if (this.timeOuts) {
      clearTimeout(this.timeOuts);
    }

    if (!this.sportDataCache) {
      this.sportDataCache = {};
    }
  }

  /**
   * Destroy Sport Cache
   */
  destroySportsCache(): void {
    /**
     * Calculate info for deleting
     * @type {number} - seconds
     */
    const timeOutTime = inplayCacheConfig.cacheInterval;

    /**
     * remove cache on timeout
     */
    this.timeOuts = this.windowRef.nativeWindow.setTimeout(() => {
      /**
       * delete sportDataCache
       */
      delete this.sportDataCache;
      delete this.allEvents;
      /**
       * delete self
       */
      delete this.timeOuts;
    }, timeOutTime);
  }

  /**
   * Store sport and it events by merging sport data with it events
   * @param {object} sportParams
   * @param {object} sportData
   * @returns {*}
   */
  storeSport(sportParams: IRequestParams, sportData: ISportSegment) {
    if (!sportData.eventsByTypeName) {
      sportData.eventsByTypeName = [];
    }

    return this.storeSportData(sportData,
      sportParams.topLevelType,
      sportParams.categoryId);
  }

  /**
   * retrieve Competition object from Sport
   * @param {string} topLevelType - LIVE_EVENT / UPCOMING_EVENT
   * @param {string} sportId
   * @param {string|number} competitionId
   * @returns {object} - competition object
   */
  getSportCompetition(topLevelType: string, sportId: string, competitionId: string): ITypeSegment {
    const sport = this.sportDataCache[topLevelType][sportId].data;
    return _.find(sport.eventsByTypeName, (competition: ITypeSegment) => parseInt(competition.typeId, 10) === parseInt(competitionId, 10));
  }

  /**
   * Replace old events list with the new one
   * @param topLevelType
   * @param sportId
   * @param competitionId
   * @param eventsList
   */
  resetCompetitionEvents(topLevelType: string, sportId: string, competitionId: string, isAggregated: boolean, eventsList: ISportEvent[]): void {
    this.sportDataCache = this.sportDataCache || {};
    const competitionToUpdate = this.getSportCompetition(topLevelType, sportId, competitionId);

    if (competitionToUpdate) {
      competitionToUpdate.events = eventsList;
    }

    this.allEvents = this.allEvents || {};
    this.addEvents(eventsList, isAggregated);
  }

  addEvents(events: ISportEvent[], isAggregated: boolean): void {
    events.forEach((event) => {
      if (this.allEvents[event.id] && isAggregated) {
        this.allEvents[event.id].markets = [...this.allEvents[event.id].markets,...event.markets];
      } else {
        this.allEvents[event.id] = event;
      }
    });
  }

  removeEvents(events: (string | number | ISportEvent)[]): void {
    events && events.forEach((event) => {
      const id = typeof event !== 'string' && typeof event !== 'number' ? event && event.id : event;
      if (id !== null && id !== undefined) {
        this.allEvents && delete this.allEvents[id];
      }
    });
  }

  /**
   * Add new competition to Sport
   * @param {string} topLevelType - LIVE_EVENT / UPCOMING_EVENT
   * @param {string} sportId
   * @param {object} competitionObject
   */
  addCompetition(topLevelType: string, sportId: string, competitionObject: ITypeSegment, isAggregated: boolean) {
    const sport = this.sportDataCache[topLevelType][sportId].data;
    const competitionIndexInSport = _.findIndex(sport.eventsByTypeName,
      (category: ITypeSegment) => category.typeId === competitionObject.typeId);

    if (competitionIndexInSport === -1) {
      sport.eventsByTypeName.push(competitionObject);
    } else {
      sport.eventsByTypeName[competitionIndexInSport] = competitionObject;
    }
    this.addEvents(competitionObject.events, isAggregated);
  }

  /**
   * Remove competition from Sport
   * @param {string} topLevelType - LIVE_EVENT / UPCOMING_EVENT
   * @param {string} sportId
   * @param {string} competitionId
   */
  removeCompetition(topLevelType, sportId, competitionId) {
    const sport = this.sportDataCache[topLevelType][sportId].data;
    const competitionIndex = _.findIndex(sport.eventsByTypeName, { typeId: competitionId });
    const { events } = sport.eventsByTypeName[competitionIndex];

    if (events) {
      this.removeEvents(events);
    }
    sport.eventsByTypeName.splice(competitionIndex, 1);
  }

  /**
   * Store sport Data
   * @param {object} sportData
   * @param {string} topLevelType
   * @param {number} categoryId
   * @returns {*}
   */
  storeSportData(sportData: ISportSegment, topLevelType: string, categoryId: string): ISportSegment {
    if (!this.sportDataCache) {
      this.sportDataCache = {};
    }

    if (!this.sportDataCache[topLevelType]) {
      this.sportDataCache[topLevelType] = {};
    }

    this.sportDataCache[topLevelType][categoryId] = { data: sportData, lastUpdated: Date.now() };

    // 'setTimeout' used for asynchronous synchronization 'sportDataCache' with 'structureCache'.
    // view use 'sportDataCache' and do Not need wait for it.
    setTimeout(() => this.updateStructureCacheSportData(sportData, topLevelType, categoryId), 100);

    return this.sportDataCache[topLevelType][categoryId].data;
  }

  isOutdatedStructure(): boolean {
    return this.isOutDated(this.structureCache.lastUpdated, this.intervals.structureCache);
  }

  isOutdatedRibbon(): boolean {
    return this.isOutDated(this.ribbonCache.lastUpdated, this.intervals.ribbonCache);
  }

  /**
   * Clear link
   * @param {string} link
   * @returns {string}
   */
  clearLink(link: string): string {
    return link.replace('#/', '/').replace('sport/', '');
  }

  /**
   * Adds new sport categories from updatedCategories to cachedCategories by given ids.
   * @param {Array} ids
   * @param {Array} cachedCategories
   * @param {Array} updatedCategories
   */
  private addSportCategories(ids: string[], cachedCategories: ISportSegment[], updatedCategories: ISportSegment[]): void {
    _.each(updatedCategories, (category: ISportSegment) => {
      const isNewCategoryValid = category.showInPlay && _.contains(ids, category.categoryId);

      if (isNewCategoryValid) {
        cachedCategories.push(category);
      }
    });
  }

  /**
   * ARemoves sport categories by given ids from categories list.
   * @param {Array} ids
   * @param {Array} categories
   */
  private removeSportCategories(ids: string[], categories: ISportSegment[]): void {
    for (let index = categories.length - 1; index >= 0; index--) {
      const sport = categories[index];

      if (_.contains(ids, sport.categoryId)) {
        categories.splice(index, 1);
      }
    }
  }

  /**
   * Updates cacheData with new updateData.
   * @param {Object} cacheData
   * @param {Object} updateData
   */
  private updateSportCategories(cacheData: IStructureTopLevelTypeData, updateData: IStructureTopLevelTypeData): void {
    const oldCategoryIds = _.pluck(cacheData.eventsBySports, 'categoryId'),
      newCategoryIds = _.pluck(updateData.eventsBySports, 'categoryId'),
      categoriesToRemove = _.difference(oldCategoryIds, newCategoryIds),
      categoriesToAdd = _.difference(newCategoryIds, oldCategoryIds);

    if (categoriesToRemove.length) {
      this.removeSportCategories(categoriesToRemove, cacheData.eventsBySports);
    }

    if (categoriesToAdd.length) {
      this.addSportCategories(categoriesToAdd, cacheData.eventsBySports, updateData.eventsBySports);
    }

    cacheData.eventsIds = updateData.eventsIds;
  }
}
