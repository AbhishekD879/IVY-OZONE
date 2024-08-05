'use strict';

const _ = require('underscore');

module.exports = function(filtersObj = {}) {
  const filters = [];

  if (filtersObj.classCategoryIdEquals) {
    filters.push(`simpleFilter=class.categoryId:equals:${filtersObj.classCategoryIdEquals}`);
  }

  if (filtersObj.categoryId) {
    filters.push(`simpleFilter=event.categoryId:intersects:${filtersObj.categoryId}`);
  }

  if (filtersObj.categoryCode) {
    filters.push(`simpleFilter=event.categoryCode:intersects:${filtersObj.categoryCode}`);
  }

  // means get events with reffering to siteChanels
  if (filtersObj.siteChannels) {
    filters.push(`simpleFilter=event.siteChannels:contains:${filtersObj.siteChannels}`);
  }

  if (filtersObj.startTime) {
    filters.push(`simpleFilter=event.startTime:greaterThanOrEqual:${filtersObj.startTime}`);
  }

  if (filtersObj.endTime) {
    filters.push(`simpleFilter=event.startTime:lessThan:${filtersObj.endTime}`);
  }

  // TODO: I've changed 'greaterThan' to 'greaterThanOrEqual'
  if (filtersObj.suspendAtTime) {
    filters.push(`simpleFilter=event.suspendAtTime:greaterThanOrEqual:${filtersObj.suspendAtTime.replace(/\.\d\d\dZ/, '.000Z')}`);
  }

  if (filtersObj.isActive) {
    filters.push('simpleFilter=event.isActive:isTrue');
  }

  // gets Events that contains DrilldownTagNames
  if (filtersObj.eventDrilldownTagNamesContains) {
    filters.push(`simpleFilter=event.drilldownTagNames:contains:${filtersObj.eventDrilldownTagNamesContains}`);
  }

  // gets Events that intersects DrilldownTagNames
  if (filtersObj.eventDrilldownTagNamesIntersects) {
    filters.push(`simpleFilter=event.drilldownTagNames:intersects:${filtersObj.eventDrilldownTagNamesIntersects}`);
  }

  // get events with markets that contains at least 1 market in live - marketBetInRunExists
  if (filtersObj.marketBetInRunExists) {
    filters.push('existsFilter=event:simpleFilter:market.isMarketBetInRun:isTrue');
  }

  // get events with markets that have isMarketBetInRun attribute - marketBetInRun
  if (filtersObj.marketBetInRun) {
    filters.push('simpleFilter=market.isMarketBetInRun:isTrue');
  }

  // Means show only 1 market - 'Match Result' - W/D/W
  if (filtersObj.dispSortName) {
    if (_.isArray(filtersObj.dispSortName)) {
      filtersObj.dispSortName = filtersObj.dispSortName.join(',');
    }

    if (filtersObj.dispSortName === 'isNotEmpty') {
      filters.push(`simpleFilter=market.dispSortName:${filtersObj.dispSortName}`);
    } else {
      filters.push(`simpleFilter=market.dispSortName:intersects:${filtersObj.dispSortName}`);
    }
  }

  // Means get events that contains markets 'Match Result' only - W/D/W
  if (filtersObj.dispSortNameIncludeOnly) {
    if (_.isArray(filtersObj.dispSortNameIncludeOnly)) {
      filtersObj.dispSortNameIncludeOnly = filtersObj.dispSortNameIncludeOnly.join(',');
    }
    filters.push(`existsFilter=event:simpleFilter:market.dispSortName:intersects:${filtersObj.dispSortNameIncludeOnly}`);
  }

  // Means exclude or include events that finished
  if (filtersObj.isFinished !== undefined) {
    filters.push(`simpleFilter=event.isFinished:is${filtersObj.isFinished.toString().charAt(0)
        .toUpperCase()}${filtersObj.isFinished.toString().slice(1)}`);
  }

  // Means get live events (live now - started)
  if (filtersObj.isStarted) {
    filters.push('simpleFilter=event.isStarted:isTrue');
  }

  // Means get finished events with that have result
  if (filtersObj.isResulted) {
    filters.push('simpleFilter=event.isResulted:isTrue');
  }

  // Means get live events (not started)
  if (filtersObj.isNotStarted) {
    filters.push('simpleFilter=event.isStarted:isFalse');
  }

  // Means get live events (live later)
  if (filtersObj.isLiveNowOrFutureEvent) {
    filters.push('simpleFilter=event.isLiveNowOrFutureEvent:isTrue');
  }

  // for Outright - are a special type of market
  if (filtersObj.eventSortCode) {
    filters.push(`simpleFilter=event.eventSortCode:intersects:${filtersObj.eventSortCode}`);
  }

  // only for racing next races
  if (filtersObj.typeFlagCodes) {
    filters.push(`simpleFilter=event.typeFlagCodes:intersects:${filtersObj.typeFlagCodes}`);
  }

  // only for racing next races - means - get only markets with SP (Starting Price) and LP (Live Price) bet types
  if (filtersObj.priceTypeCodes) {
    filters.push(`simpleFilter=market.priceTypeCodes:intersects:${filtersObj.priceTypeCodes}`);
  }

  // get only events with market name AND ONLY 1 market with name, currently name = '|Win or Each Way|'
  if (filtersObj.marketName) {
    filters.push(`existsFilter=event:simpleFilter:market.name:equals:${filtersObj.marketName}`);
    filters.push(`simpleFilter=market.name:equals:${filtersObj.marketName}`);
  }

  // only Resulted events with Resulted market name AND ONLY 1 market with name, currently name = '|Win or Each Way|'
  if (filtersObj.resultedMarketName) {
    filters.push(`existsFilter=resultedEvent:simpleFilter:resultedMarket.name:equals:${filtersObj.resultedMarketName}`);
    filters.push(`simpleFilter=resultedMarket.name:equals:${filtersObj.resultedMarketName}`);
  }

  if (filtersObj.resultedMarketPriceTypeCodesIntersects) {
    if (_.isArray(filtersObj.resultedMarketPriceTypeCodesIntersects)) {
      filtersObj.resultedMarketPriceTypeCodesIntersects = filtersObj.resultedMarketPriceTypeCodesIntersects.join(',');
    }
    filters.push(`simpleFilter=resultedMarket.priceTypeCodes:intersects:${filtersObj.resultedMarketPriceTypeCodesIntersects}`);
  }

  if (filtersObj.resultedOutcomeResultCodeNotEquals) {
    filters.push(`simpleFilter=resultedOutcome.resultCode:notEquals:${filtersObj.resultedOutcomeResultCodeNotEquals}`);
  }

  // only markets from market collection Names
  if (filtersObj.marketCollectionNamesIntersects) {
    let param = '';
    if (_.isArray(filtersObj.marketCollectionNamesIntersects)) {
      param = filtersObj.marketCollectionNamesIntersects.map(s => `|${s}|`).join(',');
    } else {
      param = `|${filtersObj.marketCollectionNamesIntersects}|`;
    }
    filters.push(`simpleFilter=market.collectionNames:intersects:${param}`);
  }

  // means event status, example: A - Active, S - suspended
  if (filtersObj.eventStatusCode) {
    filters.push(`simpleFilter=event.eventStatusCode:equals:${filtersObj.eventStatusCode}`);
  }

  // means market status, example: A - Active, S - suspended
  if (filtersObj.marketStatusCodeExists) {
    filters.push(`existsFilter=event:simpleFilter:market.marketStatusCode:equals:${filtersObj.marketStatusCodeExists}`);
  }

  // means market status, example: A - Active, S - suspended
  if (filtersObj.marketStatusCode) {
    filters.push(`simpleFilter=market.marketStatusCode:equals:${filtersObj.marketStatusCode}`);
  }

  // means outcomes status, example: A - Active, S - suspended
  if (filtersObj.outcomeStatusCode) {
    filters.push(`simpleFilter=outcome.outcomeStatusCode:equals:${filtersObj.outcomeStatusCode}`);
  }

  // used for retrieving Enhanced Multiples events
  if (filtersObj.typeName) {
    filters.push(`simpleFilter=event.typeName:equals:${filtersObj.typeName}`);
  }

  // only for horseracing next races - means exclude outcomes with names - Unnamed Favorite & Unnamed 2nd Favorite
  if (filtersObj.excludeUnnamedFavourites) {
    filters.push('simpleFilter=outcome.name:notEquals:UNNAMED FAVOURITE');
    filters.push('simpleFilter=outcome.name:notEquals:|UNNAMED FAVOURITE|');
    filters.push('simpleFilter=outcome.name:notEquals:UNNAMED 2nd FAVOURITE');
    filters.push('simpleFilter=outcome.name:notEquals:|UNNAMED 2nd FAVOURITE|');
  }

  // means exclude resulted Outcomes with names - Unnamed Favorite & Unnamed 2nd Favorite
  if (filtersObj.resultedOutcomesExcludeUnnamedFavourites) {
    filters.push('simpleFilter=resultedOutcome.name:notEquals:UNNAMED FAVOURITE');
    filters.push('simpleFilter=resultedOutcome.name:notEquals:|UNNAMED FAVOURITE|');
    filters.push('simpleFilter=resultedOutcome.name:notEquals:UNNAMED 2nd FAVOURITE');
    filters.push('simpleFilter=resultedOutcome.name:notEquals:|UNNAMED 2nd FAVOURITE|');
  }

  // means get only events with markets within outcomes count (for example - next races)
  if (filtersObj.limitOutcomesCount) {
    filters.push(`limitRecords=outcome:${filtersObj.limitOutcomesCount}`);
  }

  // means get only events with markets count
  if (filtersObj.limitMarketCount) {
    filters.push(`limitRecords=market:${filtersObj.limitMarketCount}`);
  }

  // only for racing next races and horseracing event (silks, jockeys)
  if (filtersObj.racingFormOutcome) {
    filters.push('racingForm=outcome');
  }

  // only for racing events (race overview, title, number, distance, etc.)
  if (filtersObj.racingFormEvent) {
    filters.push('racingForm=event');
  }

  if (filtersObj.prune) {
    if (!_.isArray(filtersObj.prune)) {
      filtersObj.prune = [filtersObj.prune];
    }
    _.each(filtersObj.prune, param => {
      filters.push(`prune=${param}`);
    });
  }

  if (filtersObj.translationLang) {
    filters.push(`translationLang=${filtersObj.translationLang}`);
  }

  if (filtersObj.count) {
    filters.push(`count=${filtersObj.count}`);
  }

  if (filtersObj.eventIdNotIn) {
    filters.push(`simpleFilter=event.id:notIn:${filtersObj.eventIdNotIn}`);
  }

  return filters.join('&');
};
