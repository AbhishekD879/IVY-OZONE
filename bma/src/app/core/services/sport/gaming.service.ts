import { Injectable } from '@angular/core';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { LiveUpdatesWSService } from '@core/services/liveUpdatesWS/liveUpdatesWS.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { SportService } from '@core/services/sport/sport.service';
import { TimeService } from '@core/services/time/time.service';
import { Observable } from 'rxjs';
import * as _ from 'underscore';
import { TemplateService } from '@shared/services/template/template.service';
import { OutcomeTemplateHelperService } from '@sb/services/outcomeTemplateHelper/outcome-template-helper.service';
import { ISportEvent, IEventData } from '@core/models/sport-event.model';
import { IEdpMarket, ISystemConfig, ISportConfig, ISportInstance } from '@core/services/cms/models';
import { ISportEventEntity } from '@core/models/sport-event-entity.model';
import { OUTRIGHTS_CONFIG } from '@core/constants/outrights-config.constant';
import { EventService } from '@sb/services/event/event.service';
import { ICouponEventsRequestParams } from '@core/models/coupon-events-request-params.model';
import { IGroupedByDateItem, ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { IMarket } from '@core/models/market.model';
import { IMarketCollection, IPill } from '@core/models/market-collection.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import environment from '@environment/oxygenEnvConfig';

@Injectable()
export class GamingService extends SportService implements ISportInstance {
  sportConfig: ISportConfig;
  specials: Function;
  coupons: Function;
  private readonly customCollections = ['build-your-bet', 'bet-builder', '5-a-side'];
  private readonly extraTabs = ['#GetAPrice', '#YourCall'];

  constructor(
    protected eventFactory: EventService,
    protected templateService: TemplateService,
    protected timeService: TimeService,
    protected filtersService: FiltersService,
    protected liveUpdatesWSService: LiveUpdatesWSService,
    protected channelService: ChannelService,
    protected outcomeTemplateHelper: OutcomeTemplateHelperService,
    protected cmsService: CmsService,
    protected commandService: CommandService,
    protected routingHelperService: RoutingHelperService,
    protected pubSubService: PubSubService
  ) {
    super(eventFactory, templateService, timeService, liveUpdatesWSService, channelService, filtersService, pubSubService);
    this.specials = this.todayEventsByClasses;
    this.coupons = this.couponsList;
  }

  createNewInstance(): ISportInstance {
    return new GamingService(this.eventFactory, this.templateService, this.timeService,
      this.filtersService, this.liveUpdatesWSService, this.channelService, this.outcomeTemplateHelper,
      this.cmsService, this.commandService, this.routingHelperService, this.pubSubService);
  }

  isFootball(): boolean {
    return this.sportConfig.config.request.categoryId === environment.CATEGORIES_DATA.footballId;
  }

  /**
   * subscribe for updates from events for LP page via liveServe PUSH updates (iFrame)!
   * @param events
   */
  subscribeLPForUpdates(events: ISportEvent[]): void {
    const channel = this.channelService.getLSChannelsFromArray(events);

    this.pubSubService.publish('SUBSCRIBE_LS', {
      channel,
      module: 'sb'
    });
  }

  /**
   * UnSubscribe for updates via liveServe PUSH updates (iFrame)!
   */
  unSubscribeLPForUpdates(): void {
    this.pubSubService.publish('UNSUBSCRIBE_LS', 'sb');
  }

  /**
   * Collects sEVENT, sEVMKT, sSELCN ids of given events and subscribes to live updates via WS LiveServe MS.
   * @param {ISportEvent[]} events
   * @param {number} typeId
   * @return {string}
   */
  subscribeEventChildsUpdates(events: ISportEvent[], typeId: number): string {
    const moduleName = `matches-${typeId}`;
    const channels = this.channelService.getEventsChildsLiveChannels(events);
    return this.liveUpdatesWSService.subscribe(channels, moduleName);
  }

  /**
   * Unsubscribes from WS LiveServe MS for ids cached by given key.
   * @param {string} key
   * @return {string}
   */
  unsubscribeEventChildsUpdates(key: string): void {
    this.liveUpdatesWSService.unsubscribe(key);
  }

  todayEventsByClasses(): Promise<ISportEvent[]> {
    return this.eventFactory.eventsByClasses(this.config.request);
  }

  competitionsInitClassIds(): Observable<ISystemConfig> {
    return this.cmsService.getSystemConfig();
  }

  outrights(): Promise<ISportEvent[]> {
    this.config.request.eventSortCode = this.getEventSortCode();

    return this.eventFactory.eventsByClasses(this.config.request)
      .then(data => this.templateService.filterBetInRunMarkets(data))
      .then(data => this.templateService.filterMultiplesEvents(data));
  }

  getEventSortCode(): string {
    return this.sportConfig.config.isOutrightSport ?
      OUTRIGHTS_CONFIG.outrightsSportSortCode :
      OUTRIGHTS_CONFIG.sportSortCode;
  }

  jackpot(): Promise<ISportEvent[] | void | boolean> {
    return this.eventFactory.getFootballJackpotList();
  }

  couponsList(): Promise<ISportEventEntity[]> {
    const requestParams = {
        couponCategoryId: this.config.request.categoryId,
        couponSiteChannelsContains: this.config.request.siteChannels,
        existsCouponEventStartTimeGreaterThanOrEqual: this.timeService.createTimeRange(this.config.tabs['coupons'].date).startDate,
        existsCouponEventSuspendAtTimeGreaterThan: this.timeService.getSuspendAtTime(),
        existsCouponEventIsNotStarted: true
      },
      couponsList = this.eventFactory.couponsList(
        _.extend({}, requestParams)
      );

    return Promise.all([couponsList, this.cmsService.getSystemConfig().toPromise()]).then(data => {
      const newBadgeConfig = data[1].FootballCouponsNewBadge || {};

      let coupons = [];

      coupons = data[0].map(coupon => {
        coupon.coupon.displayOrder = Number(coupon.coupon.displayOrder);
        if (coupon.coupon.name === newBadgeConfig.couponName) {
          _.extend(coupon.coupon, { enableCouponNewBadge: newBadgeConfig.enableCouponNewBadge });
        }
        return coupon.coupon;
      });

      return this.filtersService.orderBy(coupons, ['displayOrder', 'name']);
    });
  }

  couponEventsRequestParams(id: string): ICouponEventsRequestParams {
    const typeIdFilter = _.contains(this.categoriesData.footballCoupons.idsToIntersect, Number(id))
        ? { typeIdCodes: this.categoriesData.footballCoupons.typeIds } : {};
    return _.extend({}, {
      categoryId: this.config.request.categoryId,
      siteChannels: this.config.request.siteChannels,
      isNotStarted: true,
      startTime: this.timeService.createTimeRange(this.config.request.date).startDate,
      suspendAtTime: this.timeService.getSuspendAtTime(),
      childCount: true
    }, typeIdFilter);
  }

  couponEventsByCouponId(requestParams: ICouponEventsRequestParams): Promise<ISportEvent[]> {
    return this.eventFactory.couponEventsByCouponId(requestParams)
      .then(eventsArray => {
      _.forEach((eventsArray as any[]), eventEntity => {
        eventEntity.coupon = true;
        eventEntity.eventCorectedDay = this.templateService.getEventCorectedDay(eventEntity.startTime);
        this.outcomeTemplateHelper.setOutcomeMeaningMinorCode(eventEntity.markets, eventEntity);
      });

      return this.filtersService.orderBy(eventsArray, ['startTime', 'typeDisplayOrder', 'name']);
    });
  }

  filterOutFutureEvents(eventsArray: ISportEvent[]): ISportEvent[] {
    const upcomingEvents = eventsArray.filter((eventEntity) => {
      const reducedStartTime = this.timeService.reduceByCurrentTime(eventEntity.startTime);
      const correctDate = this.templateService.getEventCorectedDays(reducedStartTime as any);
      return ['Today', 'Tomorrow'].includes(correctDate);
    });
    return upcomingEvents;
  }

  results(): Promise<ISportEvent[]> {
    return Promise.resolve([]);
  }

  arrangeEventsBySection(eventsArray: ISportEvent[], isGroupByDate: boolean): ITypeSegment[] {
    const onlyMatches = eventsArray.filter(event => !OUTRIGHTS_CONFIG.sportSortCode.includes(event.eventSortCode));
    const onlyOutrights = eventsArray.filter(event => OUTRIGHTS_CONFIG.sportSortCode.includes(event.eventSortCode));

    const groupedMatches: ITypeSegment[] = this.groupEventsBySections(onlyMatches, isGroupByDate);
    const groupedOutrights: ITypeSegment[] = this.groupEventsBySections(onlyOutrights, isGroupByDate);

    const result = groupedOutrights.reduce(((aggregatedSegments: ITypeSegment[], outrightSegment: ITypeSegment): ITypeSegment[] => {
      const matchesSegment = groupedMatches.find(matchesGroupSegment => matchesGroupSegment.typeId === outrightSegment.typeId);
      if (matchesSegment) {
        matchesSegment.events.push(...outrightSegment.events);
        matchesSegment.groupedByDate.push(...outrightSegment.groupedByDate);
      } else {
        aggregatedSegments.push(outrightSegment);
      }

      return aggregatedSegments;
    }), groupedMatches);

    return result;
  }

  groupEventsBySections(eventsArray: ISportEvent[], isGroupByDate: boolean): ITypeSegment[] {
    const eventsBySections = {};
    const sortedEvents = this.filtersService.orderBy(eventsArray, ['startTime', 'markets[0].outcomes[0].name', 'displayOrder', 'name']);

    _.forEach(sortedEvents, eventEntity => {
      const correctDate = this.templateService.getEventCorectedDays((eventEntity as any).startTime);

      if (!eventsBySections[(eventEntity as any).typeId]) {
        eventsBySections[(eventEntity as any).typeId] = {
          classDisplayOrder: Number((eventEntity as any).classDisplayOrder),
          className: (eventEntity as any).className,
          categoryName: (eventEntity as any).categoryName,
          typeName: (eventEntity as any).typeName,
          typeDisplayOrder: Number((eventEntity as any).typeDisplayOrder),
          groupedByDate: {},
          events: [],
          typeId: (eventEntity as any).typeId
        };
      }

      if (!eventsBySections[(eventEntity as any).typeId].groupedByDate[correctDate] && isGroupByDate) {
        eventsBySections[(eventEntity as any).typeId].groupedByDate[correctDate] = {
          title: correctDate,
          startTime: (eventEntity as any).startTime,
          events: [],
          marketsAvailability: {}
        };
      }
      this.outcomeTemplateHelper.setOutcomeMeaningMinorCode((eventEntity as any).markets, eventEntity);
      (eventEntity as any).eventCorectedDay = this.templateService.getEventCorectedDay((eventEntity as any).startTime);

      eventsBySections[(eventEntity as any).typeId].events.push(eventEntity);

      if (!isGroupByDate) {
        return;
      }

      eventsBySections[(eventEntity as any).typeId].groupedByDate[correctDate].events.push(eventEntity);
      _.forEach(eventEntity.markets, market => {
        if (market.templateMarketName.toLowerCase()) {
          eventsBySections[(eventEntity as any).typeId].groupedByDate[correctDate]
            .marketsAvailability[market.templateMarketName.toLowerCase()] = true;
        }
        if (market.name.toLowerCase()) {
          eventsBySections[(eventEntity as any).typeId].groupedByDate[correctDate]
            .marketsAvailability[market.name.toLowerCase()] = true;
        }
      });
    });
    const results = this.objectToArray(eventsBySections);
    _.each(results, (res) => {
      res.groupedByDate = _.toArray(res.groupedByDate);
    });
    return results;
  }

  /**
   * Re-init marketsAvailability properties for event sections groupped by date data
   * When market undisplayed, we need to re-init only properties but not re-init whole sections to prevent blinking.
   * @param events -
   * @param eventsBySections
   */
  setMarketsAvailability(events: ISportEvent[], eventsBySections: ITypeSegment[]): void {
    eventsBySections.forEach((section: ITypeSegment) => {
      // TODO check groupedByDate value type , it is an array of IGroupedByDateItem , not an Obj
      section.groupedByDate.forEach((group: IGroupedByDateItem) => {
         group.marketsAvailability = {};
       });
    });

    _.forEach(events, (eventEntity: ISportEvent) => {
      const correctDate = this.templateService.getEventCorectedDays((eventEntity as any).startTime);
      eventsBySections.forEach((section: ITypeSegment) => {
        if (section.typeId === eventEntity.typeId) {
          eventEntity.markets.forEach((market: IMarket) => {
            const name = (market.templateMarketName && market.templateMarketName.toLowerCase()) || market.name.toLowerCase();

            // TODO check groupedByDate value type , it is an array of IGroupedByDateItem , not an Obj
            section.groupedByDate.forEach((group: IGroupedByDateItem) => {
              if (group.title === correctDate) {
                // TODO check marketsAvailability value type , it is a boolean
                (group.marketsAvailability[name] as any) = true;
              }
            });
          });
        }
      });
    });
  }

  updateCollectionsWithLiveMarket(liveMarket: IMarket, collections: IMarketCollection[],
                                  allMarkets: IMarket[], sportName: string): boolean {
    if (!liveMarket.outcomes || !liveMarket.outcomes.length) {
      return false;
    }

    liveMarket.viewType = this.templateService.getMarketViewType(liveMarket, sportName);
    liveMarket.outcomes = this.templateService.getMarketWithSortedOutcomes(liveMarket, allMarkets);

    const liveMarketCollectionIds = liveMarket.collectionIds && liveMarket.collectionIds.split(',').slice(0, -1),
      allMarketsCollection = _.findWhere(collections, { name: 'All Markets' }),
      isExitingLiveMarket = (allMarketsCollection as any).markets.some(allMarket => allMarket.id === liveMarket.id && !liveMarket.new),
      collectionsToUpdate = collections.filter(collection => _.contains(liveMarketCollectionIds, collection.id)),
      collectionsList = collectionsToUpdate.length ? collectionsToUpdate : [_.findWhere(collections, { name: 'Other Markets' })];

    if (isExitingLiveMarket) {
      this.updateCollections(liveMarket, collectionsList);
    } else {
      this.addToCollections(liveMarket, collectionsList);
    }

    return true;
  }

  /**
   * Filter and extend Market Collections
   * @description Remove Collections without markets and merge Collections with the same name
   * @param {IEventData} eventData
   * @param DS_GAME
   * @returns {IMarketCollection[]}
   */
  extendMarketsCollections(eventData: IEventData, DS_GAME): IMarketCollection[] {
    const collections = eventData.collection;
    // insert YC Tab
    if (!_.isEmpty(DS_GAME) && DS_GAME.isActive) {
      if (DS_GAME.isEnabledYCTab) {
        const YCTab = this.commandService.execute(this.commandService.API.GET_YC_TAB, [eventData.event[0]], {});
        collections.splice(0, 0, YCTab);
      }
      if (DS_GAME.isFiveASideAvailable) {
        const fiveASideTab = this.commandService.execute(this.commandService.API.GET_5ASIDE_TAB, [eventData.event[0]], {});
        fiveASideTab.isFiveASideNewIconAvailable = DS_GAME.isFiveASideNewIconAvailable;
        collections.splice(0, 0, fiveASideTab);
      }
    }
    return collections.reduce((collection, current) => {
      const sameName = collection.find(item => item.name === current.name);
      if (!sameName) {
        return collection.concat([current]);
      } else {
        if (!sameName.markets) { sameName.markets = []; }
        if (current.markets) {
          sameName.markets = _.uniq(sameName.markets.concat(current.markets));
        }
        return collection;
      }
    }, []).sort((a, b) => (a.displayOrder > b.displayOrder) ? 1 : (a.displayOrder < b.displayOrder) ? -1 : 0);
  }

  getCollectionsTabs(collections: IMarketCollection[], event: ISportEvent, EDP_MARKETS: IEdpMarket[], isMobileOnly: boolean): IMarketCollection[] {
    return this.getSortingFromCms(collections.filter(c => {
      return this.customCollections.indexOf(c.marketName) >= 0 || (c.markets && c.markets.length);
    }), EDP_MARKETS, event, isMobileOnly);
  }

  getSortingFromCms(collections: IMarketCollection[], EDP_MARKETS: IEdpMarket[], event: ISportEvent, isMobileOnly: boolean): IMarketCollection[] {
    if (isMobileOnly) {
      return _.sortBy(this.getSortingFromCmsForMobile(collections, EDP_MARKETS, event), 'index');
    }
    return _.sortBy(this.getSortingFromCmsForDesktop(collections, EDP_MARKETS, event), 'index');
  }

  getSortingFromCmsForMobile(collections: IMarketCollection[], EDP_MARKETS: IEdpMarket[], event: ISportEvent): any {
    const arrayLength = (EDP_MARKETS.length > collections.length) ? EDP_MARKETS.length : collections.length;
    const indexedCollection: IMarketCollection[] = [];
    let pills: IPill[] = [];
    collections.forEach((collection: IMarketCollection) => {
      if(collection.marketName || collection.name === 'All Markets' || this.extraTabs.includes(collection.name)) {
        const collectionIndex = _.findIndex(EDP_MARKETS, { name: collection.name });
        const collectionLink = collection.marketName || collection.name.toLowerCase().replace(/[^A-Za-z0-9 ]/g, '')
          .replace(/\s/g, '-');
        const tabUrl = this.routingHelperService.formEdpUrl(event);

        if (collectionIndex === -1) {
          collection.index = arrayLength;
        } else if (EDP_MARKETS[collectionIndex].lastItem) {
          collection.index = arrayLength + 1;
        } else {
          collection.index = collectionIndex;
        }

        indexedCollection.push({
          id: `tab-${collectionLink}`,
          marketName: collectionLink,
          label: collection.name,
          isFiveASideNewIconAvailable: collection.isFiveASideNewIconAvailable,
          url: collection.url || `/${tabUrl}/${collectionLink}`,
          index: collection.index
        });
      }
    });

    collections.forEach((collection: IMarketCollection) => {
      if(!collection.marketName && !this.extraTabs.includes(collection.name)) {
        const collectionIndex = _.findIndex(EDP_MARKETS, { name: collection.name });
        const collectionLink = collection.name.toLowerCase().replace(/[^A-Za-z0-9 ]/g, '')
          .replace(/\s/g, '-');

        if (collectionIndex === -1) {
          collection.index = arrayLength;
        } else if (EDP_MARKETS[collectionIndex].lastItem) {
          collection.index = arrayLength + 1;
        } else {
          collection.index = collectionIndex;
        }

        pills.push({
          marketName: collectionLink,
          active: false,
          label: collection.name,
          index: collection.index
        });
      }
    })

    pills = _.sortBy(pills, 'index');
    const index = indexedCollection.findIndex((col) => col.label === 'All Markets');
    if(index >= 0) {
      indexedCollection[index].pills = pills;
      indexedCollection[index].label = "Markets";
    }

    return indexedCollection;
  }

  getSortingFromCmsForDesktop(collections: IMarketCollection[], EDP_MARKETS: IEdpMarket[], event: ISportEvent): any {
    const arrayLength = (EDP_MARKETS.length > collections.length) ? EDP_MARKETS.length : collections.length;
    const indexedCollection = collections.map((collection: IMarketCollection) => {
      const collectionIndex = _.findIndex(EDP_MARKETS, { name: collection.name });
      const collectionLink = collection.marketName || collection.name.toLowerCase().replace(/[^A-Za-z0-9 ]/g, '')
        .replace(/\s/g, '-');
      const tabUrl = this.routingHelperService.formEdpUrl(event);
      if (collectionIndex === -1) {
        collection.index = arrayLength;
      } else if (EDP_MARKETS[collectionIndex].lastItem) {
        collection.index = arrayLength + 1;
      } else {
        collection.index = collectionIndex;
      }

      return {
        id: `tab-${collectionLink}`,
        marketName: collectionLink,
        label: collection.name,
        isFiveASideNewIconAvailable: collection.isFiveASideNewIconAvailable,
        url: collection.url || `/${tabUrl}/${collectionLink}`,
        index: collection.index
      };
    });

    return indexedCollection;
  }

  isAnyMarketByPattern(marketsArray, pattern) {
    return marketsArray.some(market => market.name.toString().match(pattern) !== null);
  }

  private updateCollections(market: IMarket, collectionsArray: IMarketCollection[]): void {
    _.forEach(collectionsArray, (collection: IMarketCollection) => {
      if (!collection || !collection.markets) {
        return;
      }

      const marketIndex = _.findIndex(collection.markets, { id: market.id });
      if (marketIndex > -1) {
        (collection as any).markets[marketIndex] = market;
      }
    });
  }

  private addToCollections(market: IMarket, collectionsArray: IMarketCollection[]): void {
    delete market.new;

    _.forEach(collectionsArray, collection => {
      if (!(collection as any).markets) {
        (collection as any).markets = [];
      }
      (collection as any).markets.push(market);
    });
  }
}
