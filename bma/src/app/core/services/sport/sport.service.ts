import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { forkJoin, from, Observable, throwError } from 'rxjs';
import { map, catchError } from 'rxjs/operators';

import environment from '@environment/oxygenEnvConfig';
import { IClassTypeName, IClassItem } from '@core/models/class-type-name.model';
import { IGroupedRace } from '@core/models/grouped-race.model';
import { IScoreboardConfig } from '@core/models/scoreboard-config.model';
import { ISportCollectionData } from '@core/models/sport-collection-data.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { ISportServiceConfig } from '@core/models/sport-service-config.model';
import { ISportServiceRequestConfig } from '@core/models/sport-service-request-config.model';
import { ITab } from '@core/models/tab.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { LiveUpdatesWSService } from '@core/services/liveUpdatesWS/liveUpdatesWS.service';
import { TimeService } from '@core/services/time/time.service';
import { EventService } from '@sb/services/event/event.service';
import { TemplateService } from '@shared/services/template/template.service';
import { IInitialSportConfig } from '@core/services/sport/config/initial-sport-config.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IMarket } from '@core/models/market.model';

@Injectable()
export class SportService {

  public config: ISportServiceConfig;
  public readonlyRequestConfig: ISportServiceRequestConfig;
  public extension?: string;
  public marketList: IMarket[];

  protected generalConfig: IInitialSportConfig;
  protected categoriesData: any;

  constructor(
    protected eventFactory: EventService,
    protected templateService: TemplateService,
    protected timeService: TimeService,
    protected liveUpdatesWSService: LiveUpdatesWSService,
    protected channelService: ChannelService,
    protected filtersService: FiltersService,
    protected pubSubService: PubSubService,
  ) {
    this.categoriesData = environment.CATEGORIES_DATA;
  }

  /**
   * subscribe for updates from events for EDP page via liveServe PUSH updates (iFrame)!
   * @param {object} event
   * @param {boolean} subscribeForScores
   */
  subscribeEDPForUpdates(event: ISportEvent, subscribeForScores: boolean = false): void {
    const channel = this.channelService.getLSChannels(event, true, subscribeForScores);

    this.pubSubService.publish('SUBSCRIBE_LS', {
      channel,
      module: 'edp'
    });
  }

  /**
   * UnSubscribe EDP page for updates via liveServe PUSH updates (iFrame)!
   */
  unSubscribeEDPForUpdates(): void {
    this.pubSubService.publish('UNSUBSCRIBE_LS', 'edp');
  }

  /**
   * Subscribe coupons for updates via liveServe PUSH updates (iFrame)!
   * @param events
   * @param couponId
   * @returns {Array}
   */
  subscribeCouponsForUpdates(events: ISportEvent[], couponId: string): void {
    const channel: string[] = this.channelService.getLSChannelsForCoupons(events);

    this.pubSubService.publish('SUBSCRIBE_LS', {
      channel,
      module: `coupon-${couponId}`
    });
  }

  /**
   * UnSubscribe coupons for updates via liveServe PUSH updates (iFrame)!
   * @param couponId
   */
  unSubscribeCouponsForUpdates(couponId: string): void {
    this.pubSubService.publish('UNSUBSCRIBE_LS', `coupon-${couponId}`);
  }

  /**
   * extendRequestConfig()
   * @param {string} tabName
   * @returns {ISportServiceRequestConfig}
   */
  extendRequestConfig(tabName: string): ISportServiceRequestConfig {
    const request: ISportServiceRequestConfig = this.config.request = {},
      tab = tabName === 'upcoming' ? 'today' : tabName === 'antepost' ? 'future' : tabName,
      tabs = this.config.tabs ? this.config.tabs[tab] : {};
    let dateParam;

    if (tabName === 'upcoming' && (this.readonlyRequestConfig && this.readonlyRequestConfig.categoryId !== environment.CATEGORIES_DATA.golfId)) {
      const isTier1Or2 = _.contains([1, 2], this.config.tier);
      dateParam = isTier1Or2 ? 'pre48h' : 'antepost';
    } else if ((tabName === 'golf_matches' || tabName === 'upcoming')
      && this.readonlyRequestConfig && this.readonlyRequestConfig.categoryId === environment.CATEGORIES_DATA.golfId) {
      dateParam = 'allEvents';
    } else {
      dateParam = tabName;
    }


    _.extend(request, this.readonlyRequestConfig, {
      date: dateParam,
      suspendAtTime: this.timeService.getSuspendAtTime()
    }, tabs);

    if (tabName === 'outrights') {
      request.limitOutcomesCount = 1;
      request.limitMarketCount = 1;
    }

    if (tabName === 'outrights' || tabName === 'specials') {
      delete request.dispSortName;
      delete request.dispSortNameIncludeOnly;
      delete request.marketTemplateMarketNameIntersects;
    }

    if (tabName === 'specials') {
      request.limitOutcomesCount = 2;
    }

    // Replace marketsCount param with childCount if we are on SLP and category is not horse racing or greyhounds.
    const horseracingId = Number(environment.CATEGORIES_DATA.racing.horseracing.id);
    const greyhoundId = Number(environment.CATEGORIES_DATA.racing.greyhound.id);
    const isRacing = (Number(request.categoryId) === greyhoundId) || (Number(request.categoryId) === horseracingId);
    const tabsWithChildCount = ['today', 'tomorrow', 'future', 'upcoming'];
    const isTabWithChildCount = tabsWithChildCount.includes(tabName);

    if (!isRacing && request.marketsCount && isTabWithChildCount) {
      request.childCount = true;
      delete request.marketsCount;
    }

    if (tabName === 'allEvents' ||(request && (request.categoryId == environment.CATEGORIES_DATA.golfId && request.date == 'allEvents' && tabName !== 'upcoming'))) {
      _.extend(request, this.readonlyRequestConfig, {
        templateMarketNameNotEquals: '|Outright|',
        isNotStarted: true,
      }, tabs);
    }

    if (tabName === 'matchesTab') {
      _.extend(request, this.readonlyRequestConfig, {
        isNotStarted: true,
      }, tabs);
    }


    return request;
  }

  /**
   * setConfig()
   * @param {ISportServiceConfig} config
   * @returns {this}
   */
  setConfig(config: ISportServiceConfig): this {
    if (config) {
      this.config = Object.assign({}, config);
      this.readonlyRequestConfig = Object.assign({}, config.request);
    }

    return this;
  }

  /**
   * getConfig()
   * @returns {ISportServiceConfig}
   */
  getConfig(): ISportServiceConfig {
    return this.config;
  }

  /**
   * getSport()
   * @returns {this}
   */
  getSport(): this {
    return this;
  }

  /**
   * isDisplayAndFilterCorrect()
   * @param {ITab[]} tabs
   * @param {string} selectedTab
   * @param {string[]} filters
   * @param {string} selectedFilter
   * @returns {boolean}
   */
  isDisplayAndFilterCorrect(tabs: ITab[], selectedTab: string, filters?: string[], selectedFilter?: string): boolean {
    const clearTabs = [];

    let tab = null,
      correctFilter = false,
      result;

    _.forEach(tabs, tabId => {
      tab = tabId.id.split('-');
      clearTabs.push(tab[1]);
    });

    const correctTab = clearTabs.indexOf(selectedTab) > -1;

    if (filters) {
      correctFilter = filters.indexOf(selectedFilter) > -1;
      result = correctTab && correctFilter;
    } else {
      result = correctTab;
    }

    return result;
  }
  /**
   * Sets the list for markets in Template Service
   * @param data: IMarket
   */
  setMarketList(data: IMarket[]) {
    this.templateService.marketList = data;
  }
  /**
   * getById()
   * @param {string} eventId
   * @param {boolean} useCache
   * @param {boolean} isSortOutcomes
   * @returns {Promise<ISportEvent>}
   */
  getById(eventId: string, useCache: boolean, isSortOutcomes: boolean = true, isMTASport?: boolean): Observable<any> {
    const $event: Observable<ISportEvent[]> = from(this.getEvent(eventId, useCache, isMTASport))
      .pipe(
        map(data => this.checkEventMarkets(data)),
        map(data => this.filterEmptyMarkets(data, isMTASport)),
        catchError((err) => throwError(err))
      );

    // @ts-ignore
    const $collection: Observable<ISportCollectionData[]> = from(
      // @ts-ignore
      this.eventFactory.getNamesOfMarketsCollection(Number(this.config.request.categoryId))
    ).pipe(catchError((err) => throwError(err)));

    return forkJoin([$event, $collection])
      .pipe(
        map(([event, collection]) => ({
          event,
          collection: this.initMarketsByCollection(event, collection, this.config, isSortOutcomes)
        })
        )
      );
  }

  /**
   * getByTab()
   * @param {string} tabName
   * @param {boolean} isGrouped
   * @returns {Promise<ISportEvent[]>}
   */
  getByTab(tabName: string, isGrouped?: boolean): Promise<ISportEvent[]> {
    this.extendRequestConfig(tabName);
    return this.getEvents(tabName);
  }

  /**
   * getScoreboardConfig()
   * @returns {IScoreboardConfig}
   */
  getScoreboardConfig(): IScoreboardConfig | void {
    return this.config.scoreboardConfig;
  }

  /**
   * getEvents()
   * @param {string} selectedTab
   * @param {boolean} isGrouped
   * @returns {Promise<ISportEvent[]>}
   */
  protected getEvents(selectedTab: string, isGrouped?: boolean): Promise<ISportEvent[]> {
    return this[this.config.eventMethods[selectedTab]]();
  }

  /**
   * getEvent()
   * @param {string} eventId
   * @param {boolean} useCache
   * @returns {ISportEvent[]}
   */
  protected getEvent(eventId: string, useCache: boolean, isMTASport?: boolean): Promise<ISportEvent[]> {
    const filters = this.config.eventRequest ? this.config.eventRequest : {};
    return this.eventFactory.getEvent(eventId, filters, true, useCache, isMTASport);
  }

  /**
   * blocker()
   * @returns {Promise<Array<void>>}
   */
  protected blocker(): Promise<Array<void>> {
    return Promise.resolve([]);
  }

  /**
   * objectToArray()
   * @param {Object} obj
   * @returns {Array<any>}
   */
  protected objectToArray(obj: Object): Array<any> {
    return _.values(obj);
  }

  /**
   * getLiveStreamGroups()
   * @param {IClassTypeName[]} classesTypeNames
   * @param {IGroupedRace[]} groupedRacing
   * @returns {IClassTypeName[]}
   */
  protected getLiveStreamGroups(classesTypeNames: IClassTypeName[], groupedRacing: IGroupedRace[]): IClassTypeName[] {
    _.forEach(classesTypeNames, (names, index) => {
      const classType = _.find(groupedRacing, num => {
        // @ts-ignore: forEach goes through the Object, ts throws error
        return num.flag === index;
      });

      let classEvents;

      if (!!classType && classType.data) {
        // @ts-ignore
        _.forEach(names, (item: IClassItem) => {
          // @ts-ignore
          classEvents = classType.data.filter(event => event.name === item.name);

          if (classEvents.length === 0) {
            // @ts-ignore
            classEvents = classType.data.filter(event => event.typeName === item.name);
          }

          if (classEvents && classEvents.length > 0) {
            item.liveStreamAvailable = this.eventFactory.isAnyLiveStreamAvailable(classEvents);
          }
        });
      }
    });

    return classesTypeNames;
  }

  /**
   * getCashoutAvailGroups()
   * @param {IClassTypeName[]} classesTypeNames
   * @param {IGroupedRace[]} groupedRacing
   * @returns {IClassTypeName[]}
   */
  protected getCashoutAvailGroups(classesTypeNames: IClassTypeName[], groupedRacing: IGroupedRace[]): IClassTypeName[] {
    const cashoutConfig = [{
      cashoutAvail: 'Y'
    }];

    let classType,
      classEvents;

    _.forEach(classesTypeNames, (names, index) => {
      classType = _.find(groupedRacing, num => {
        // @ts-ignore: forEach goes through the Object, ts throws error
        return num.flag === index;
      });

      if (!!classType && classType.data) {
        // @ts-ignore
        _.forEach(names, (item: IClassItem) => {
          classEvents = classType.data.filter(event => event.name === item.name);

          if (classEvents.length === 0) {
            classEvents = classType.data.filter(event => event.typeName === item.name);
          }

          if (classEvents && classEvents.length > 0) {
            item.typeDisplayOrder = _.min(_.pluck(classEvents, 'typeDisplayOrder'));
            item.cashoutAvail = this.eventFactory.isAnyCashoutAvailable(classEvents, cashoutConfig);
          }
        });
      }
    });

    return classesTypeNames;
  }

  /**
   * isMarketTabCorrect()
   * @param {ITab[]} tabs
   * @param {string} selectedTab
   */
  protected isMarketTabCorrect(tabs: ITab[], selectedTab: string): boolean {
    const clearTabs = [];

    _.forEach(tabs, tabId => {
      clearTabs.push(tabId.id.replace(/tab-/g, ''));
    });
    // Handle case when tab name for main markets was changed to 'Main'
    return clearTabs.indexOf(selectedTab) > -1 ||
      (selectedTab === 'main-markets' && clearTabs.indexOf('main') > -1);
  }

  /**
   * checkEventMarkets()
   * @param {ISportEvent[]} events
   * @returns {ISportEvent[]}
   */
  protected checkEventMarkets(events: ISportEvent[]): ISportEvent[] {
    if (events && events.length && events[0].markets.length > 0) {
      return this.templateService.filterBetInRunMarkets(events);
    }

    return events;
  }

  /**
   * filterEmptyMarkets()
   * @param {ISportEvent[]} events
   * @returns {ISportEvent[]}
   */
  protected filterEmptyMarkets(events: ISportEvent[], isMTASport?: boolean): ISportEvent[] {
    if (events && events.length) {
      events[0].markets = isMTASport ? events[0].markets
      .filter(market => !!market.isDisplayed) : events[0].markets
        .filter(market => market.outcomes && market.outcomes.length);
    }

    return events;
  }

  /**
   * Make markets by collection data.
   *
   * @param events
   * @param sportCollectionsData
   * @param sportConfig
   * @param isSortOutcomes
   */
  protected initMarketsByCollection(events: ISportEvent[], sportCollectionsData: ISportCollectionData[],
    sportConfig: ISportServiceConfig, isSortOutcomes: boolean = true): any {
    if (_.isUndefined(events) || (events && !events.length)) {
      return [];
    }

    const sportName = sportConfig.name;
    const otherMarket = 'Other Markets';
    const mainMarket = 'Main Markets';
    const collectionIds = _.pluck(sportCollectionsData, 'id');
    const otherMarkets = [];
    const otherMarketsCollection = { name: otherMarket, markets: [] };

    let mainMarkets;
    let marketCollectionIds: string[];
    if (events[0].markets) {
      this.setMarketList(events[0].markets);
    }

    (events[0].markets || []).forEach(market => {
      const sportForViewType = market.rawHandicapValue ? null : sportName;
      market.viewType = this.templateService.getMarketViewType(market, sportForViewType);
      if ((market.outcomes && market.outcomes.length) && (isSortOutcomes || market.rawHandicapValue)) {
        const marketsForSortingOutcomes = market.rawHandicapValue ? null : events[0].markets;
        market.outcomes = this.templateService.getMarketWithSortedOutcomes(market, marketsForSortingOutcomes);
      
      }

      marketCollectionIds = market.collectionIds && market.collectionIds.split(',').slice(0, -1);
      (sportCollectionsData || []).forEach((element, index) => {
        if (_.contains(marketCollectionIds, element.id)) {
          if (!_.has(sportCollectionsData[index], 'markets')) {
            sportCollectionsData[index].markets = [];
          }
          sportCollectionsData[index].markets.push(market);
        }
      });

      if (!_.intersection(collectionIds, marketCollectionIds).length) {
        otherMarkets.push(market);
      }
    });

    const mainMarketIndex = (sportCollectionsData || []).findIndex(value => value.name === mainMarket);

    if (mainMarketIndex !== -1) {
      mainMarkets = sportCollectionsData.splice(mainMarketIndex, 1);
      sportCollectionsData.unshift(mainMarkets[0]);
    }

    if (otherMarkets.length) {
      otherMarketsCollection.markets = _.uniq(otherMarkets);
    }

    sportCollectionsData.push(otherMarketsCollection);
    sportCollectionsData.unshift({
      name: 'All Markets',
      markets: events[0].markets
    });

    return sportCollectionsData;
  }
}
