import { of as observableOf, Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { TimeService } from '@core/services/time/time.service';
import { IStoredData, IIndexConfig, ILevel2Deepness, IPathToData, IEventsIndex, INumberIndex, ICached } from './cache-events.model';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IFeaturedModel } from '@featured/models/featured.model';
import { IOutputModule } from '@featured/models/output-module.model';
import { Cached } from './cached';

@Injectable()
export class CacheEventsService {
  storedData: IStoredData = {
    event: {},
    nextRacesHome: {},
    liveEventsStream: {}, // stream widget event to stream
    multiplesEvents: {},
    inPlayWidget: {},
    inplaySection: {},
    LSWidget: {},
    coupons: {},
    ribbonEvents: {},
    privateMarkets: {},
    index: {},
    marketsIndex: {}, // Additional hashes for outcomes and markets to events. Need for liveserve updates.
    outcomesIndex: {}, // It is useful to use sSELCN and sEVMKT separately without subscribing or aggregator SEVENT.
    currentMatches: {},
    favouritesMatches: {},
    toteEvents: {},
    surfaceBetEvents: {},
    nextRaces: {}
  };

  indexConfig: IIndexConfig = {
    addToIndexCounter: 0, // cleans counter - updating each time cleaner is called
    addToIndexLimit: 5 // Earlier count: 20 - every 5th call cleaner will clean outdated indexes
  };

  level2Deepness: ILevel2Deepness = {
    multiplesEvents: 'events',
    ribbonEvents: 'data'
  };

  pathToData: IPathToData = {
    ribbonEvents: 'modules'
  };

  constructor(private timeService: TimeService, private pubsub: PubSubService) {
    this.store = this.store.bind(this);
  }

  /**
   * Caches the data passed in the last argument to the
   * runtime cache structure in two steps:
   * 1. Create a nested data structure with data inside,
   * 2. Merges it to stored data.
   * If the data already exists by this path, it should be
   * overwritten.
   * @return {[type]} [description]
   */
  store(...args: any[]): any {
    const path = args.slice(0, -1);
    const source = this.pack(args);

    this.addToIndex(this.storedData, source);
    this.merge(this.storedData, source);

    return this.stored(...path);
  }

  /**
   * Clear cached data by Name
   *
   * @param cacheName
   */
  clearByName(cacheName: string): void {
    this.storedData[cacheName] = undefined;
  }

  /**
   * Wraps the plain data into promise
   * @param  {Object}       data Any data
   * @param {boolean}       isPromise
   * @return {Observable}   Observable data
   */
  async(data: IFeaturedModel, isPromise: boolean = true): Promise<any> | Observable<any> {
    const result: Observable<IFeaturedModel> = observableOf(data);
    return isPromise ? result.toPromise() : result;
  }

  /**
   * Stores new market data or outcome to cash object
   * @param  {Object}       update Market or Outcome data
   * @return {number}       updated market index
   */
  storeNewMarketOrOutcome(update: any): IMarket | boolean {
    return update.eventId ? this.storeNewMarket(update) : this.storeNewOutcome(update);
  }

  /**
   * Store new multiple outcomes that are received from response for markets (BWIN markets) to event cache
   * @param outcomes
   */
  storeNewOutcomes(outcomes: IOutcome[], skipCheck: boolean = false): void {
    const event = this.storedData.event.data[0],
      index = event && _.findIndex(event.markets, (market: IMarket) => (`${market.id}` === `${outcomes[0].marketId}`));
    let filteredOutcomes = outcomes;
    if (event && index >= 0) {
      if (event.markets[index].outcomes && !skipCheck) {
        event.markets[index].outcomes = this.removeFakeOutcomes(event.markets[index].outcomes);
        /*
        Checking existing outcomes as we might receive them also during live updates while request to SS in progress
        in order not to have duplicated outcomes.
        */
        const existingOutcomesIds = event.markets[index].outcomes.map(o => o.id);
        filteredOutcomes = outcomes.filter(outcome => !existingOutcomesIds.includes(outcome.id));
        event.markets[index].outcomes = event.markets[index].outcomes.concat(filteredOutcomes);
      } else {
        event.markets[index].outcomes = outcomes;
      }

      filteredOutcomes.forEach(outcome => {
        this.storedData.outcomesIndex[outcome.id] = event.id;
      });

      this.pubsub.publish('UPDATE_OUTCOMES_FOR_MARKET', event.markets[index]);
    }
  }
  /**
   * A facade method of `dive` function, also checks
   * the existance of cached data
   * @return {[type]} [description]
   */
  stored(...args: string[]): IFeaturedModel {
    const cached = this.dive(args, this.storedData);
    return cached && cached instanceof Cached ? this.isDataOutdated(cached, this.interval(args[0])) : undefined;
  }

  /**
   * Adds sourceData to Index in storedData
   *
   * @param {object} data
   * @param {object} sourceData
   */
  addToIndex(data: IStoredData, sourceData: Cached): void {
    const storedDataKey = _.keys(sourceData)[0];
    const dataPath = this.pathToData[storedDataKey] ? ['data'].concat(this.pathToData[storedDataKey]) : ['data'];
    const storedDataPath = this.getStoredDataPath(sourceData);
    const path = [...storedDataPath, ...dataPath];
    let expireTimestamp = storedDataPath.reduce((obj, i) => obj[i], sourceData).updated
      + this.timeService.apiDataCacheInterval[storedDataKey];
    const reference = path.reduce((obj, i) => obj[i], sourceData);
    const fn = this.level2Deepness[storedDataKey]
      ? this.addToIndexWithDeepnessLevel2.bind({ key: this.level2Deepness[storedDataKey], fn: this.addToIndexWithDeepnessLevel1 })
      : this.addToIndexWithDeepnessLevel1;

    if (reference && reference.length) {
      this.cleanIndex(data.index, data.marketsIndex, data.outcomesIndex);

      // Sets past time when expireTimestamp is NaN
      if (isNaN(expireTimestamp)) {
        const MS_PER_MINUTE = 60 * 1000; //1 min
        expireTimestamp = Date.now() - (30 * MS_PER_MINUTE);
      }

      fn(data.index, data.marketsIndex, data.outcomesIndex, path, reference, expireTimestamp);
    }
  }

  /**
   * cleans index from outdated data - using indexConfig
   *
   * @param {Object} eventsIndex
   * @param {Object} marketsIndex
   * @param {Object} outcomesIndex
   */
  private cleanIndex(eventsIndex: IEventsIndex,
    marketsIndex: INumberIndex,
    outcomesIndex: INumberIndex): void {
    this.indexConfig.addToIndexCounter++;
    if (this.indexConfig.addToIndexCounter >= this.indexConfig.addToIndexLimit) {
      this.indexConfig.addToIndexCounter = 0;
      const currentTimestamp = this.timeService.getCurrentTime();

      for (const eventProp in eventsIndex) {
        if (eventsIndex.hasOwnProperty(eventProp)) {
          for (const eventRef in eventsIndex[eventProp]) {
            if (eventsIndex[eventProp].hasOwnProperty(eventRef)) {
              if (eventsIndex[eventProp][eventRef].expire < currentTimestamp) {
                delete eventsIndex[eventProp][eventRef];
              }
            }
          }

          if (Object.keys(eventsIndex[eventProp]).length === 0 && eventsIndex[eventProp].constructor === Object) {
            delete eventsIndex[eventProp];
          }
        }
      }

      // delete markets indexes
      for (const key of Object.keys(marketsIndex)) {
        const result: boolean = eventsIndex.hasOwnProperty(marketsIndex[key]);
        if (!result) {
          delete marketsIndex[key];
        }
      }

      // delete outcomes indexes
      for (const key of Object.keys(outcomesIndex)) {
        const result: boolean = eventsIndex.hasOwnProperty(outcomesIndex[key]);
        if (!result) {
          delete outcomesIndex[key];
        }
      }
    }
  }

  /**
   * Returns path till meet 2 objects (data, updated) - it means the end of the path
   *
   * @param obj
   * @returns {Array}
   */
  private getStoredDataPath(obj: Cached | IPathToData): string[] {
    const keys = _.keys(obj);
    let keysArray = [];
    if (keys.length === 1) {
      keysArray = [keys[0], ...this.getStoredDataPath(obj[keys[0]])];
    }

    return keysArray;
  }

  /**
   * Adds to index ordinary events with common structure - deepness level 1.
   *
   * @param eventsIndex
   * @param marketsIndex
   * @param outcomesIndex
   * @param path
   * @param reference
   * @param expireTimestamp
   */
  private addToIndexWithDeepnessLevel1(eventsIndex: IEventsIndex,
    marketsIndex: INumberIndex,
    outcomesIndex: INumberIndex,
    path: Array<string | number>,
    reference: ISportEvent[],
    expireTimestamp: number): void {
    const stringPath = path.join('');
    _.forEach(reference, (eventEntity: ISportEvent, i: number) => {
      if (!eventsIndex[eventEntity.id]) {
        eventsIndex[eventEntity.id] = {};
      }
      // extend markets and outcomes indexes with attached events ids
      if (_.has(eventEntity, 'markets')) {
        _.forEach(eventEntity.markets, (m: IMarket) => {
          marketsIndex[m.id] = eventEntity.id.toString();
          _.forEach(m.outcomes, (o: IOutcome) => {
            outcomesIndex[o.id] = eventEntity.id.toString();
          });
        });
      }

      eventsIndex[eventEntity.id][stringPath] = {
        path: path.concat(i),
        expire: expireTimestamp,
        reference: reference[i]
      };
    });
  }

  /**
   * Adds to index ordinary events with level structure - deepness level 2.
   *
   * @param eventsIndex
   * @param marketsIndex
   * @param outcomesIndex
   * @param path
   * @param reference
   * @param expireTimestamp
   * @this level2Deepness object property
   */
  private addToIndexWithDeepnessLevel2(eventsIndex: IEventsIndex,
    marketsIndex: INumberIndex,
    outcomesIndex: INumberIndex,
    path: Array<string | number>,
    reference: IOutputModule[],
    expireTimestamp: number): void {
    _.forEach(reference, (levelEntity: IOutputModule, levelIndex: number) => {
      const level2Path = path.concat(levelIndex, this['key']);
      const level2Reference = reference[levelIndex][this['key']];

      this['fn'](eventsIndex, marketsIndex, outcomesIndex, level2Path, level2Reference, expireTimestamp);
    });
  }

  /**
   * Creates a hierarchical object from provided array,
   * each element of it defines a folding level,
   * and the last one gets stored in the structure.
   * @param  {Array} fullPath   Mixed array, last element is the data
   * @return {Object}       Packed object
   */
  private pack(fullPath: any[]) {
    const path = fullPath.slice(0);
    const obj = {};
    const arg = path.splice(0, 1)[0];

    obj[arg] = path.length > 0 ? this.pack(path) : undefined;

    return obj[arg] ? obj : new Cached(arg, this.timeService);
  }

  /**
   * Recursively merges source objects into target,
   * by modifying the first one.
   * It overwrites existing data endpoint.
   * @param  {Object} target target object
   * @param  {Object} source source object
   * @return {undefined}
   */
  private merge(target: IStoredData, source: Cached | { ribbonEvents: ICached }): void {
    _.each(_.keys(source), key => {
      const isInstanceOfCache = source[key] instanceof Cached;
      target[key] = isInstanceOfCache ? source[key] : target[key] || source[key];
      // Check if merge source has reached to Cached object,
      // avoid multiple recursion of deep merge and decrease time to merge
      if (!isInstanceOfCache) {
        this.merge(target[key], source[key]);
      }
    });
  }

  /**
   * checks cache data is they are outdated
   *
   * @param cached
   * @param intervalValue
   * @returns {*}
   */
  private isDataOutdated(cached: ICached, intervalValue: number): IFeaturedModel {
    return (this.timeService.getCurrentTime() - cached.updated) > intervalValue ? undefined : cached.data;
  }

  /**
   * Recursively following the path in the deep
   * of the object and returns the remainder.
   * @param  {[type]} fullPath [description]
   * @param  {[type]} obj  [description]
   * @return {[type]}      [description]
   */
  private dive(fullPath: string[], obj: IStoredData): ICached {
    const path = fullPath.slice(0);
    const key = path.shift();

    if (!obj) {
      return undefined;
    }

    if (path.length > 0) {
      return this.dive(path, obj[key]);
    }

    return obj[key];
  }

  private interval(date: string): number {
    return this.timeService.apiDataCacheInterval[date];
  }

  /**
   * Stores new market
   * @param  {Object}   market
   */
  private storeNewMarket(market: IMarket): boolean | IMarket {
    market.new = true;
    const event = !_.isEmpty(this.storedData.event) && this.storedData.event.data[0];
    if (event && (Number(event.id) === Number(market.eventId)) && !(event.eventIsLive && market.isMarketBetInRun === 'N')) {
      this.storedData.marketsIndex[market.id] = event.id;
      event.markets.push(market);

      return event.markets[event.markets.length - 1];
    }

    return false;
  }

  /**
   * Stores new outcome
   * @param  {Object}  outcome
   */
  private storeNewOutcome(outcome: IOutcome): boolean | IMarket {
    const event = !_.isEmpty(this.storedData.event) && this.storedData.event.data[0];
    const index = event && _.findIndex(event.markets, (market: IMarket) =>
      (!_.isUndefined(market.id) && `${market.id}` === `${outcome.marketId}`));

    if (event && index >= 0) {
      this.extendHandicapOutcome(event.markets[index], outcome);
      if (event.markets[index].outcomes) {
        event.markets[index].outcomes = this.removeFakeOutcomes(event.markets[index].outcomes);
        event.markets[index].outcomes.push(outcome);
      } else {
        event.markets[index].outcomes = [outcome];
      }
      this.storedData.outcomesIndex[outcome.id] = event.id;
      this.pubsub.publish('UPDATE_OUTCOMES_FOR_MARKET', event.markets[index]);

      return event.markets[index];
    }

    return false;
  }

  /**
   * [Remove fake outcomes which were added at footballExtension for proper displaying
   *  of outcomes ]
   * @param  { Array } outcomes [Array of outcoms]
   * @return { Array }          [Filtered array of outcoms (without fake outcomes)]
   */
  private removeFakeOutcomes(outcomes: IOutcome[]): IOutcome[] {
    return _.filter(outcomes, (outcome: IOutcome) => !outcome.fakeOutcome);
  }

  private extendHandicapOutcome(handicapMarket: IMarket, handicapOutcome: IOutcome): void {
    const index = typeof (handicapOutcome.outcomeMeaningMinorCode) === 'string' ?
      handicapOutcome.outcomeMeaningMinorCode : +handicapOutcome.outcomeMeaningMinorCode;
    if (handicapMarket.handicapValues && handicapMarket.handicapValues[index]) {
      handicapOutcome.prices[0].handicapValueDec = `${handicapMarket.handicapValues[index]},`;
      handicapOutcome.outcomeMeaningMajorCode = handicapMarket.marketMeaningMinorCode;
    }
  }
}
