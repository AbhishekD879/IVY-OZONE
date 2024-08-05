import { Injectable } from '@angular/core';
import { IFilterParam } from '@core/models/filter-param.model';
import { ISSRequestParamsModel } from '@core/models/ss-request-params.model';
import { TimeService } from '@core/services/time/time.service';
import * as _ from 'underscore';

@Injectable()
export class SimpleFiltersService {

  simpleFiltersBank = {
    extraPlaceMarkets: ['siteChannels', 'isNotFinished', 'isNotResulted', 'isNotStarted', 'isNotLiveNowEvent',
      'isRawIsOffCodeNotY', 'marketDrilldownTagNamesContains', 'templateMarketNameOnlyEquals', 'racingFormEvent',
      'limitOutcomesCount'],
    eventsByClasses: [
      'siteChannels', 'typeFlagCodes', 'startTime',
      'endTime', 'dispSortName', 'dispSortNameIncludeOnly',
      'eventSortCode', 'isFinished', 'isNotFinished', 'isStarted', 'isNotStarted',
      'eventStatusCode', 'suspendAtTime', 'limitOutcomesCount', 'limitMarketCount'
    ],
    eventsByClassesRaw: [
      'isNotFinished', 'startTime', 'endTime', 'externalKeysEvent'
    ],
    eventsList: [
      'categoryId', 'siteChannels', 'typeFlagCodes', 'startTime',
      'endTime', 'eventSortCode', 'isFinished', 'isNotFinished', 'isStarted',
      'eventStatusCode', 'eventDrilldownTagNamesContains', 'classId',
      'eventDrilldownTagNamesIntersects', 'suspendAtTime', 'typeName', 'excludeTypeIdCodes'
    ],
    liveEventsByEvents: [
      'dispSortName', 'dispSortNameIncludeOnly',
      'isStarted', 'marketTemplateMarketNameIntersects',
      'marketBetInRunExists', 'marketBetInRun', 'isNotStarted', 'suspendAtTime', 'templateMarketNameOnlyIntersects'
    ],
    liveOutrightEventsByEvents: [
      'isStarted', 'eventSortCode', 'categoryCode', 'limitMarketCount', 'limitOutcomesCount',
      'marketBetInRunExists', 'marketBetInRun', 'isNotStarted', 'suspendAtTime'
    ],
    eventsByEventsIds: [
      'dispSortName', 'dispSortNameIncludeOnly', 'includeUndisplayed',
      'isStarted', 'marketTemplateMarketNameIntersects',
      'marketBetInRunExists', 'isNotStarted', 'suspendAtTime', 'templateMarketNameOnlyIntersects'
    ],
    eventsByOutcomeIds: [
      'dispSortName', 'dispSortNameIncludeOnly',
      'isStarted', 'marketTemplateMarketNameIntersects',
      'marketBetInRunExists', 'isNotStarted', 'suspendAtTime', 'templateMarketNameOnlyIntersects',
      'racingFormOutcome', 'includeRestricted', 'includeUndisplayed', 'externalKeysEvent',
      'externalKeysMarket', 'externalKeysOutcome','priceHistory'
    ],
    nextEventsByType: [
      'startTime', 'endTime',
      'typeFlagCodes', 'priceTypeCodes', 'isActive', 'marketName',
      'excludeUnnamedFavourites', 'racingFormOutcome', 'limitOutcomesCount', 'suspendAtTime',
      'siteChannels', 'outcomeStatusCode', 'marketStatusCodeExists', 'marketStatusCode', 'eventStatusCode'
    ],
    eventsByTypeWithMarketCounts: [
      'isNotStarted', 'noEventSortCodes', 'typeHasOpenEvent', 'marketsCount',
      'dispSortName', 'dispSortNameIncludeOnly', 'marketTemplateMarketNameIntersects',
      'templateMarketNameOnlyIntersects', 'competitionTemplateMarketNameOnlyIntersects', 'competitionTemplateMarketName'
    ],
    eventsByTypeId: ['isNotStarted', 'eventSortCode', 'typeHasOpenEvent', 'marketsCount', 'suspendAtTime',
      'dispSortName', 'dispSortNameIncludeOnly', 'marketTemplateMarketNameIntersects', 'templateMarketNameOnlyIntersects'
    ],
    eventsByCategory: [
      'siteChannels', 'typeFlagCodes', 'startTime', 'marketDrilldownTagNamesContains',
      'endTime', 'dispSortName', 'dispSortNameIncludeOnly', 'marketTemplateMarketNameIntersects',
      'eventSortCode', 'isNotStarted', 'isStarted', 'marketName', 'suspendAtTime', 'excludeEventsClassIds',
      'marketDrilldownTagNamesNotContains', 'templateMarketNameOnlyIntersects', 'eventDrilldownTagNamesNotIntersects',
      'eventDrilldownTagNamesIntersects', 'eventDrilldownTagNamesContains', 'eventDrilldownTagNamesNotContains', 'isNotResulted',
      'externalKeysEvent', 'limitOutcomesCount', 'limitMarketCount','templateMarketNameNotEquals'
    ],
    resultsByClasses: [
      'categoryId', 'siteChannels', 'typeFlagCodes', 'startTime',
      'endTime', 'dispSortName', 'dispSortNameIncludeOnly', 'marketTemplateMarketNameIntersects',
      'eventSortCode', 'marketName', 'racingFormOutcome', 'isResulted', 'suspendAtTime',
      'templateMarketNameOnlyIntersects', 'resultedIncludeUndisplayed'
    ],
    resultedEvents: ['resultedMarketName', 'resultedMarketPriceTypeCodesIntersects',
      'resultedOutcomeResultCodeNotEquals', 'resultedOutcomesExcludeUnnamedFavourites',
      'resultedIncludeUndisplayed'
    ],
    inPlayEventsByIds: ['endTime', 'startTime', 'isStarted',
      'eventDrilldownTagNamesContains', 'eventDrilldownTagNamesIntersects'
    ],
    nextEventsByIds: [
      'typeFlagCodes', 'priceTypeCodesExists', 'isActive', 'templateMarketNameOnlyEquals', 'marketTemplateMarketNameIntersects', 'priceHistory', 'siteChannels',
      'marketStatusCodeExists', 'marketStatusCode', 'outcomeStatusCode', 'eventStatusCode', 'isRawIsOffCodeNotY',
      'excludeUnnamedFavourites', 'limitOutcomesCount', 'racingFormOutcome'
    ],
    couponEventsByCouponId: [
      'dispSortName', 'dispSortNameIncludeOnly',
      'includeUndisplayed', 'startTime', 'suspendAtTime',
      'marketTemplateMarketNameIntersects', 'templateMarketNameOnlyIntersects', 'eventSortCode', 'siteChannels', 'isStarted',
      'isNotStarted', 'marketBetInRunExists', 'childCount'
    ],
    eventsByMarkets: [
      'isNotStarted',
      'racingFormOutcome',
      'includeUndisplayed',
      'externalKeysEvent'
    ],
    typesByClasses: {
      typeHasOpenEvent: true
    },
    inPlayEventsWithOutOutcomes: [
      'categoryId', 'siteChannels', 'startTime', 'endTime',
      'eventDrilldownTagNamesContains', 'eventDrilldownTagNamesIntersects',
      'isLiveNowOrFutureEvent', 'suspendAtTime',
      'dispSortNameIncludeOnly', 'marketTemplateMarketNameIntersectsOnly'
    ]
  };

  private readonly dictionary = {
    categoryId: ['simpleFilter=event.categoryId:intersects:'],
    classId: ['simpleFilter=event.classId:equals:'],
    siteChannels: ['simpleFilter=event.siteChannels:contains:'],
    marketSiteChannels: ['simpleFilter=market.siteChannels:contains:'],
    outcomeSiteChannels: ['simpleFilter=outcome.siteChannels:contains:'],
    limitToMarketDisplayOrderIsLowest: ['limitTo=market.displayOrder:isLowest'],
    startTime: ['simpleFilter=event.startTime:greaterThanOrEqual:'],
    endTime: ['simpleFilter=event.startTime:lessThan:'],
    suspendAtTime: ['simpleFilter=event.suspendAtTime:greaterThan:'],
    isOpenEvent: ['simpleFilter=event.isOpenEvent:isTrue'],
    isActive: ['simpleFilter=event.isActive:isTrue'],
    marketIsActive: ['simpleFilter=market.isActive:isTrue'],
    marketDrilldownTagNamesContains: ['existsFilter=event:simpleFilter:market.drilldownTagNames:intersects:'],
    marketDrilldownTagNamesNotContains: ['existsFilter=event:simpleFilter:market.drilldownTagNames:notIntersects:'],
    // gets Events that contains DrilldownTagNames
    eventDrilldownTagNamesContains: ['simpleFilter=event.drilldownTagNames:contains:'],
    // gets Events that not contains DrilldownTagNames
    eventDrilldownTagNamesNotContains: ['simpleFilter=event.drilldownTagNames:notContains:'],
    // gets Events that intersects DrilldownTagNames
    eventDrilldownTagNamesIntersects: ['simpleFilter=event.drilldownTagNames:intersects:'],
    // gets Events that not intersects DrilldownTagNames
    eventDrilldownTagNamesNotIntersects: ['simpleFilter=event.drilldownTagNames:notIntersects:'],
    // get events with markets that contains at least 1 market in live - marketBetInRunExists
    marketBetInRunExists: ['existsFilter=event:simpleFilter:market.isMarketBetInRun:isTrue'],
    // get events with markets that have isMarketBetInRun attribute - marketBetInRun
    marketBetInRun: ['simpleFilter=market.isMarketBetInRun'],
    // Means show only 1 market - 'Match Result' - W/D/W
    dispSortName: ['simpleFilter=market.dispSortName:intersects:'],
    // Means get events that contains markets 'Match Result' only - W/D/W
    dispSortNameIncludeOnly: ['existsFilter=event:simpleFilter:market.dispSortName:intersects:'],
    // Means include events that are finished
    isFinished: ['simpleFilter=event.isFinished:isTrue'],
    // Means include events that are NOT finished
    isNotFinished: ['simpleFilter=event.isFinished:isFalse'],
    // Means get live events (live now - started)
    isStarted: ['simpleFilter=event.isStarted'],
    // Means get finished events with that have result
    isResulted: ['simpleFilter=event.isResulted:isTrue'],
    // Means get not resulted events
    isNotResulted: ['simpleFilter=event.isResulted:isFalse'],
    // Means get live events (not started)
    isNotStarted: ['simpleFilter=event.isStarted:isFalse'],
    // Means get live events (live now)
    isRawIsOffCodeNotY: ['simpleFilter=event.rawIsOffCode:notEquals:Y'],
    // Means get all N & N/A
    isLiveNowEvent: ['simpleFilter=event.isLiveNowEvent'],
    isNotLiveNowEvent: ['simpleFilter=event.isLiveNowEvent:isFalse'],
    isNext24HourEvent: ['simpleFilter=event.isNext24HourEvent'],
    // Means get live events (live later)
    isLiveNowOrFutureEvent: ['simpleFilter=event.isLiveNowOrFutureEvent:isTrue'],
    // for Outright - are a special type of market
    eventSortCode: ['simpleFilter=event.eventSortCode:intersects:'],
    // only for racing next races
    typeFlagCodes: ['simpleFilter=event.typeFlagCodes:intersects:'],
    typeIdCodes: ['simpleFilter=event.typeId:intersects:'],
    // exclude Type Ids
    excludeTypeIdCodes: ['simpleFilter=event.typeId:notEquals:'],
    // get events without type flag codes
    noEventSortCodes: ['simpleFilter=event.eventSortCode:notIntersects:'],
    // only for racing next races - means - get only markets with SP (Starting Price) and LP (Live Price) bet types
    priceTypeCodes: ['simpleFilter=market.priceTypeCodes:intersects:'],
    priceTypeCodesExists: ['existsFilter=event:simpleFilter:market.priceTypeCodes:intersects:'],
    // get only events with market name AND ONLY 1 market with name, currently name = '|Win or Each Way|'
    marketName: ['existsFilter=event:simpleFilter:market.name:equals:', 'simpleFilter=market.name:equals:'],
    // get events by market names (used for football events to retrieve 6 markets)
    templateMarketNameOnlyIntersects: ['simpleFilter=market.templateMarketName:intersects:' +
    '|Match Betting|,|Over/Under Total Goals|,|Both Teams to Score|,|To Qualify|,' +
    '|Draw No Bet|,|First-Half Result|,|Match Result and Both Teams To Score|,|2Up - Instant Win|,' + '|' + encodeURIComponent('2Up&Win Early Payout') + '|,' + 'Match Betting,' +
    'Over/Under Total Goals,Both Teams to Score,To Qualify,Draw No Bet,First-Half Result,2Up - Instant Win,' + encodeURIComponent('2Up&Win Early Payout') + ',' +
    'Match Result and Both Teams To Score'],
    templateMarketNameOnlyEquals: ['simpleFilter=market.templateMarketName:equals:'],
    // matches simple filter on football competition page
    competitionTemplateMarketNameOnlyIntersects: ['simpleFilter=market.templateMarketName:intersects:' +
    '|Match Betting|,|Over/Under Total Goals|,|Both Teams to Score|,|To Qualify|,' +
    '|Draw No Bet|,|First-Half Result|,|Next Team to Score|,|Extra-Time Result|,|2Up - Instant Win|,' + '|' + encodeURIComponent('2Up&Win Early Payout') + '|,' +
    'Match Betting,Over/Under Total Goals,Both Teams to Score,To Qualify,Draw No Bet,First-Half Result,' +
    'Next Team to Score,Extra-Time Result,' + encodeURIComponent('2Up&Win Early Payout') + ',' + '2Up - Instant Win,Match Result and Both Teams To Score,|Match Result and Both Teams To Score|'],
    // matches simple filter only for Match Betting market
    competitionTemplateMarketName: ['simpleFilter=market.templateMarketName:intersects:' +
    '|Match Betting|'],
    
    // only Resulted events with Resulted market name AND ONLY 1 market with name, currently name = '|Win or Each Way|'
    resultedMarketName: ['existsFilter=resultedEvent:simpleFilter:resultedMarket.name:intersects:',
      'simpleFilter=resultedMarket.name:intersects:'],
    resultedMarketPriceTypeCodesIntersects: ['simpleFilter=resultedMarket.priceTypeCodes:intersects:'],
    resultedOutcomeResultCodeNotEquals: ['simpleFilter=resultedOutcome.resultCode:notEquals:'],
    // only markets from market collection Names
    marketTemplateMarketNameIntersects: ['simpleFilter=market.templateMarketName:intersects:'],
    // only markets from market collection Names
    marketTemplateMarketNameIntersectsOnly: ['existsFilter=event:simpleFilter:market.templateMarketName:intersects:'],
    // means event status, example: A - Active, S - suspended
    eventStatusCode: ['simpleFilter=event.eventStatusCode:equals:'],
    // means market status, example: A - Active, S - suspended
    marketStatusCodeExists: ['existsFilter=event:simpleFilter:market.marketStatusCode:equals:'],
    // means market status, example: A - Active, S - suspended
    marketStatusCode: ['simpleFilter=market.marketStatusCode:equals:'],
    // means outcomes status, example: A - Active, S - suspended
    outcomeStatusCode: ['simpleFilter=outcome.outcomeStatusCode:equals:'],
    // used for retrieving Enhanced Multiples events
    typeName: ['simpleFilter=event.typeName:equals:'],
    // excludes events with classes Ids
    excludeEventsClassIds: ['simpleFilter=event.classId:notIntersects:'],
    // only for horseracing next races - means exclude outcomes with names - Unnamed Favorite & Unnamed 2nd Favorite
    excludeUnnamedFavourites: ['simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1',
      'simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2'],
    // means exclude resulted Outcomes with names - Unnamed Favorite & Unnamed 2nd Favorite
    resultedOutcomesExcludeUnnamedFavourites: ['simpleFilter=resultedOutcome.outcomeMeaningMinorCode:notEquals:1',
      'simpleFilter=resultedOutcome.outcomeMeaningMinorCode:notEquals:2'],
    // means get only events with markets within outcomes count (for example - next races)
    limitOutcomesCount: ['limitRecords=outcome:'],
    // means get only events with markets count
    limitMarketCount: ['limitRecords=market:'],
    // only for racing next races and horseracing event (silks, jockeys)
    racingFormOutcome: ['racingForm=outcome'],
    // only for racing events (race overview, title, number, distance, etc.)
    racingFormEvent: ['racingForm=event'],
    // only for football
    scorecast: ['scorecast=true'],
    // for private markets
    includeRestricted: ['includeRestricted=true'],
    // get Types that have events
    typeHasOpenEvent: ['type.hasOpenEvent:isTrue'],
    // include events or commentaries which are undisplayed
    includeUndisplayed: ['includeUndisplayed=true'],
    resultedIncludeUndisplayed: ['includeUndisplayed=true'],
    priceHistory: ['priceHistory=true'],
    classCategoryIdIntersects: ['simpleFilter=class.categoryId:intersects:'],
    classSiteChannelsContains: ['simpleFilter=class.siteChannels:contains:'],
    couponSiteChannelsContains: ['simpleFilter=coupon.siteChannels:contains:'],
    existsClassEventSiteChannelsContains: ['existsFilter=class:simpleFilter:event.siteChannels:contains:'],
    existsClassEventIsNext24HourEvent: ['existsFilter=class:simpleFilter:event.isNext24HourEvent'],
    existsClassEventIsLiveNowEvent: ['existsFilter=class:simpleFilter:event.isLiveNowEvent'],
    classHasLiveNowEvent: ['simpleFilter=class.hasLiveNowEvent'],
    classHasNext24HourEvent: ['simpleFilter=class.hasNext24HourEvent'],
    existsMarketOutcomeOutcomeMeaningMajorCodeIn: ['existsFilter=market:simpleFilter:outcome.outcomeMeaningMajorCode:in:'],
    couponCategoryId: ['simpleFilter=coupon.categoryId:equals:'],
    existsCouponEventStartTimeGreaterThanOrEqual: ['existsFilter=coupon:simpleFilter:event.startTime:greaterThanOrEqual:'],
    existsCouponEventSuspendAtTimeGreaterThan: ['existsFilter=coupon:simpleFilter:event.suspendAtTime:greaterThan:'],
    existsCouponEventIsNotStarted: ['existsFilter=coupon:simpleFilter:event.isStarted:isFalse'],
    poolProvider: ['simpleFilter=pool.provider:in:'],
    poolIsActive: ['simpleFilter=pool.isActive:isTrue'],
    poolTypes: ['simpleFilter=pool.type:intersects:'],
    eventIdEquals: ['simpleFilter=event.id:equals:'],
    resultedDrawFrom: ['simpleFilter=resultedDraw.drawAtTime:greaterThan:'],
    resultedDrawTo: ['simpleFilter=resultedDraw.drawAtTime:lessThan:'],
    sportId: ['simpleFilter=sport.id:equals:'],
    // OB functionality for events/markets/outcomes linking
    externalKeysEvent: ['externalKeys=event'],
    externalKeysMarket: ['externalKeys=market'],
    externalKeysOutcome: ['externalKeys=outcome'],
    externalKeys: ['externalKeys=true'],
    childCount: ['childCount=event'],
    outcomeTeamExtIds: ['simpleFilter=outcome.teamExtIds:intersects:'],
    templateMarketNameNotEquals:['simpleFilter=market.templateMarketName:notEquals:'],
  };

  constructor(
    private time: TimeService
  ) { }

  /**
   * genFilters()
   * @param {IFilterParam} params
   * @returns {string}
   */
  genFilters(params: IFilterParam = {}): string {
    let filters = [];

    for (const prop in params) {
      if (this.dictionary[prop] && params[prop]) {
        filters = filters.concat(this.createFilterStrings(this.dictionary[prop], params[prop]));
      }
    }

    return filters.join('&');
  }

  /**
   * createFilterStrings()
   * @param {string[]} stringsArr
   * @param {string | boolean} value
   * @returns {string[]}
   */
  createFilterStrings(stringsArr: string[], value: string|boolean): string[] {
    const strVal = typeof (value) === 'boolean' ? '' : value,
      val = Array.isArray(value) ? value.join(',') : strVal;

    return stringsArr.map(str => str + val);
  }

  /**
   * getFilterParams()
   * @param {IFilterParam} params
   * @param {string[]} filterLst
   * @param {boolean} ampersandInStart
   * @param {boolean} ampersandInEnd
   * @returns {ISSRequestParamsModel}
   */
  getFilterParams(params: IFilterParam, filterLst: string[], ampersandInStart = false, ampersandInEnd = false): ISSRequestParamsModel {
    const scopeParams = params.isRacing
      ? _.extend({}, params, this.time.getRacingTimeRangeForRequest(params.date))
      : _.extend({}, params, this.time.getTimeRangeForRequest(params.date));
    if (scopeParams.startTime) {
      scopeParams.startTime = this.time.roundTo30seconds(scopeParams.startTime);
    }
    if (scopeParams.endTime) {
      scopeParams.endTime = this.time.roundTo30seconds(scopeParams.endTime);
    }
      const filters = _.extend({}, _.pick(scopeParams, filterLst)),
      reqStr = this.genFilters(filters),
      ampersandStart = ampersandInStart ? '&' : '',
      ampersandEnd = ampersandInEnd ? '&' : '';

    return reqStr ? { simpleFilters: ampersandStart + reqStr + ampersandEnd } : {};
  }
}
