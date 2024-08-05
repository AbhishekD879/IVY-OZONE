import * as _ from 'underscore';
import { IMarketEntity } from '@core/models/market-entity.model';
import { IMarket } from '@core/models/market.model';
import { IOutcomeEntity } from '@core/models/outcome-entity.model';
import { IPriceEntity } from '@core/models/price-entity.model';
import { IPrice } from '@core/models/price.model';
import { ISportEventEntity } from '@core/models/sport-event-entity.model';
import { Injectable } from '@angular/core';
import { FiltersService } from '@core/services/filters/filters.service';
import { TimeService } from '@core/services/time/time.service';
import { CommentsService } from '@core/services/comments/comments.service';
import { IOutcome } from '@core/models/outcome.model';
import { IAggregation } from '@core/models/aggregation.model';
import { IPoolModel } from '@shared/models/pool.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { ScoreParserService } from '@core/services/scoreParser/score-parser.service';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { IConstant } from '../models/constant.model';
import environment from '@environment/oxygenEnvConfig';

@Injectable()
export class BuildUtilityService {
  private readonly HORSE_RACING_CATEGORY_ID: string = '21';
  private readonly GREY_HOUND_CATEGORY_ID: string = '19';
  private readonly VIRTUAL_SPORT_CATEGORY_ID: string = '39';
  constructor(
    private filter: FiltersService,
    private time: TimeService,
    private comments: CommentsService,
    private ssRequestHelper: SiteServerRequestHelperService,
    private scoreParserService: ScoreParserService,
    private sportEventHelperService: SportEventHelperService,
  ) {
    /**
     * Context bindings
     * It's needed here because context losses in such functions, like "_.partial(Fn1, Fn2, ...)"
     */
    this.buildMapper = this.buildMapper.bind(this);
    this.outcomeBuilder = this.outcomeBuilder.bind(this);
    this.priceBuilder = this.priceBuilder.bind(this);
    this.eventBuilder = this.eventBuilder.bind(this);
    this.marketBuilder = this.marketBuilder.bind(this);
    this.addScorecastMarkets = this.addScorecastMarkets.bind(this);
    this.buildEvents = this.buildEvents.bind(this);
    this.buildEventsWithRacingForm = this.buildEventsWithRacingForm.bind(this);
    this.buildEventsWithOutMarketCounts = this.buildEventsWithOutMarketCounts.bind(this);
    this.buildEventsWithMarketCounts = this.buildEventsWithMarketCounts.bind(this);
    this.buildCouponEventsWithMarketCounts = this.buildCouponEventsWithMarketCounts.bind(this);
    this.buildEventsWithScorecasts = this.buildEventsWithScorecasts.bind(this);
    this.msEventBuilder = this.msEventBuilder.bind(this);
  }

  /**
   * marketBuilder()
   * @param {IMarketEntity} marketEntity
   * @returns {IMarket}
   */
  marketBuilder(marketEntity: IMarketEntity): IMarket {
    const buildOutcomes = _.partial(this.buildMapper, this.outcomeBuilder);
    this.referenceEachWayTermsBuilder(marketEntity);
    return _.extend(marketEntity.market, {
      outcomes: marketEntity.market.children ? buildOutcomes(marketEntity.market.children) : [],
      displayOrder: Number(marketEntity.market.displayOrder)
    });
  }

  /**
   * referenceEachWayTermsBuilder()
   * @param {IMarketEntity} marketEntity
   */
  referenceEachWayTermsBuilder(marketEntity: IMarketEntity) {
    let referenceEachWayTerms, referenceEachWayTermsIndex;
    marketEntity.market && marketEntity.market.children && marketEntity.market.children.forEach((element, index)=>{
      if (element.referenceEachWayTerms) {
        referenceEachWayTerms = element.referenceEachWayTerms;
        referenceEachWayTermsIndex = index;
      }
    });
    if (referenceEachWayTerms) {
      marketEntity.market.referenceEachWayTerms = referenceEachWayTerms;
      marketEntity.market.children.splice(referenceEachWayTermsIndex, 1);
    }
  }

  /**
   * outcomeBuilder()
   * @param {IOutcomeEntity} outcomeEntity
   * @returns {IOutcome}
   */
  outcomeBuilder(outcomeEntity: IOutcomeEntity): IOutcome {
    outcomeEntity.outcome = this.setTrapNumber(outcomeEntity.outcome);
    const buildPrices = _.partial(this.buildMapper, this.priceBuilder);

    return _.extend(outcomeEntity.outcome, {
      name: this.createOutcomeName(outcomeEntity.outcome),
      prices: buildPrices(outcomeEntity.outcome.children),
      displayOrder: Number(outcomeEntity.outcome.displayOrder)
    });
  }

  /**
   * buildEvents()
   * @param {ISportEventEntity[]} sportEventEntities
   * @returns {ISportEvent[]}
   */
  buildEvents(sportEventEntities: ISportEventEntity[]): ISportEvent[] {
    return _.partial(this.buildMapper, this.eventBuilder)(sportEventEntities);
  }

  /**
   * buildEventsWithRacingForm()
   * @param {ISportEventEntity[]} sportEventEntities
   * @returns {ISportEvent[]}
   */
  buildEventsWithRacingForm(sportEventEntities: ISportEventEntity[]): ISportEvent[] {
    const racingFormEvent = 'racingFormEvent',
      racingFormOutcome = 'racingFormOutcome',
      events = _.filter(filterElements('event'), eventObj => !!(eventObj as any).event.children),
      formEvents = _.pluck(filterElements(racingFormEvent), racingFormEvent),
      formOutcomes = _.pluck(filterElements(racingFormOutcome), racingFormOutcome);

    function filterElements(property) {
      return _.filter(sportEventEntities, el => el[property]);
    }

    function setRacingForm(forms, el, racingForm, event) {
      const firstMarketSelection = _.findWhere(event.markets[0].outcomes, { runnerNumber: String(el.runnerNumber) }),
        form = _.findWhere(forms, { refRecordId: String(el.id) })
          || (firstMarketSelection && (firstMarketSelection as any).racingFormOutcome);

      if (form) {
        el[racingForm] = form;
      }
    }

    function addRacingForm(eventsData) {
      _.each(eventsData, event => {
        setRacingForm(formEvents, event, racingFormEvent, event);
        _.each((event as any).markets, market =>
          _.each((market as any).outcomes, outcome =>
            setRacingForm(formOutcomes, outcome, racingFormOutcome, event)));
      });

      return eventsData;
    }

    return _.compose(addRacingForm, this.buildEvents)(events);
  }

  /**
 * build Event With RacingFormOutcomes
 * @param {ISportEventEntity[]} sportEventEntities
 * @returns {ISportEvent[]}
 */
  buildEventWithRacingFormOutcomes(sportEventEntities: ISportEvent[], racingFormOutcomeArray: IOutcome[]): ISportEvent[] {
    for (const event of sportEventEntities) {
      if (event.categoryId === this.VIRTUAL_SPORT_CATEGORY_ID) {
        const markets = event.markets;
        if (markets && markets.length) {
          markets.forEach((elem, index) => {
            const outcomes = markets[index].outcomes
            if (outcomes && outcomes.length) {
              outcomes.forEach(outcome => {
                const suitableOutcomesElements = racingFormOutcomeArray.filter(racingFormOutcomeElement => racingFormOutcomeElement.racingFormOutcome.refRecordId === outcome.id),
                  racingFormOutcome = suitableOutcomesElements && suitableOutcomesElements[0] && suitableOutcomesElements[0].racingFormOutcome;
                if (racingFormOutcome) {
                  outcome.silkName = racingFormOutcome.silkName;
                  outcome.racerId = racingFormOutcome.id;
                  outcome.drawNumber = racingFormOutcome.draw;
                  outcome.jockey = racingFormOutcome.jockey || racingFormOutcome.trainer;
                }
                if(!outcome.silkName )
                  outcome.silkName = outcome.runnerNumber;
              });
            }
          });
        }
      }
    }
    return sportEventEntities;
  }
  /**
   * eventBuilder()
   * @param {ISportEventEntity} sportEventEntity
   * @returns {ISportEvent}
   */
  eventBuilder(sportEventEntity: ISportEventEntity): ISportEvent {
    const buildMarkets = _.partial(this.buildMapper, this.marketBuilder),
      isUSSport = _.has(sportEventEntity.event, 'typeFlagCodes') && sportEventEntity.event.typeFlagCodes.indexOf('US') !== -1,
      unpipe = this.filter.removeLineSymbol,
      clearName = this.filter.clearEventName.bind(this.filter);
    const filteredMarkets = sportEventEntity.event.children && sportEventEntity.event.children.filter(market => market.market);
    return _.extend({}, sportEventEntity.event, {
      startTime: Date.parse(sportEventEntity.event.startTime),
      localTime: this.getLocalTime(sportEventEntity.event),
      className: unpipe(sportEventEntity.event.className),
      categoryName: unpipe(sportEventEntity.event.categoryName),
      name: clearName(unpipe(sportEventEntity.event.name), sportEventEntity.event.categoryCode),
      originalName: sportEventEntity.event.originalName || sportEventEntity.event.name,
      typeName: unpipe(sportEventEntity.event.typeName),
      classId: Number(sportEventEntity.event.classId),
      typeId: Number(sportEventEntity.event.typeId),
      id: Number(sportEventEntity.event.id),
      isUS: isUSSport,
      displayOrder: Number(sportEventEntity.event.displayOrder),
      classDisplayOrder: Number(sportEventEntity.event.classDisplayOrder),
      typeDisplayOrder: Number(sportEventEntity.event.typeDisplayOrder),
      markets: buildMarkets(filteredMarkets),
      correctedDay: this.getCorrectedDay(sportEventEntity.event),
      correctedDayValue: this.getDayValue(sportEventEntity.event),
      eventIsLive: this.isLiveEvent(sportEventEntity.event),
      liveEventOrder: this.isLiveEvent(sportEventEntity.event) ? 0 : 1
    });
  }

  msEventBuilder(event: ISportEvent): ISportEvent {
    const isUSSport = _.has(event, 'typeFlagCodes') && event.typeFlagCodes.indexOf('US') !== -1,
      unpipe = this.filter.removeLineSymbol,
      clearName = this.filter.clearEventName.bind(this.filter);
    return Object.assign({}, event, {
      startTime:  Date.parse(event.startTime) || event.startTime,
      localTime: this.getLocalTime(event, true),
      className: unpipe(event.className),
      categoryName: unpipe(event.categoryName),
      originalName: event.originalName || event.name,
      name: clearName(unpipe(event.name), event.categoryCode),
      typeName: unpipe(event.typeName),
      classId: Number(event.classId),
      typeId: Number(event.typeId),
      id: Number(event.id),
      isUS: isUSSport,
      displayOrder: Number(event.displayOrder),
      classDisplayOrder: Number(event.classDisplayOrder),
      typeDisplayOrder: Number(event.typeDisplayOrder),
      correctedDay: this.getCorrectedDay(event),
      correctedDayValue: this.getDayValue(event),
      eventIsLive: this.isLiveEvent(event),
      liveEventOrder: this.isLiveEvent(event) ? 0 : 1
    });
  }

  /**
   * poolsBuilder()
   * @param {IPoolModel[]} pools
   * @returns {IPoolModel[]}
   */
  poolsBuilder(pools: IPoolModel[]): IPoolModel[] {
    return pools.filter((poolEntity: IPoolModel) => poolEntity.pool.marketIds).map((poolEntity: IPoolModel) => {
      return _.extend({}, poolEntity.pool,
        {
          id: Number(poolEntity.pool.id),
          marketIds: poolEntity.pool.marketIds.split(',').filter(mId => mId.length),
          poolType: poolEntity.pool.type,
          guides: poolEntity.pool.children
        });
    });
  }

  /**
   * buildMarketCounts()
   * @param {ISportEventEntity[]} marketCounts
   * @returns {Object}
   */
  buildMarketCounts(marketCounts: IAggregation[]): Object {
    const mappedValues = _.map(marketCounts, agr => [agr.refRecordId, Number(agr.count)]);

    return _.object(mappedValues);
  }

  /**
   * buildEventsIds()
   * @param {ISportEventEntity[]} eventEntities
   * @returns {any[]}
   */
  buildEventsIds(eventEntities: ISportEventEntity[]): number[] {
    return eventEntities.map(eventEntity => eventEntity.event.id);
  }

  /**
   * buildEventsWithMarketCounts()
   * @param {any[]} data
   * @returns {ISportEvent[]}
   */
  buildEventsWithMarketCounts(data: any[]): ISportEvent[] {
    if ((data.length && !_.isEmpty(data[0])) || (this.checkPresentOf(data, 0) || this.checkPresentOf(data, 1))) {
      // сonvert a flat array to nested
      // if we use loadEventsWithOutMarketCounts() we get a flat array
      // if we use loadEventsWithMarketCounts() we get a nested array
      data = data[0].length ? data : [data];

      const events = data[0].filter(event => event.event);
      const countData = data[1] || data[0];
      const marketCounts = countData.filter(count => count.aggregation || count.childCount)
        .map(count => count.aggregation || count.childCount);
      const counts =  this.buildMarketCounts(marketCounts);
      const eventsBuilt = this.buildEvents(events);

      return _.map(eventsBuilt, event => _.extend({}, event, { marketsCount: counts[event.id] }));
    } else {
      return [];
    }
  }

  /**
   * buildCouponEventsWithMarketCounts()
   * @param {ISportEventEntity[]} eventEntities
   * @returns {ISportEvent[]}
   */
  buildCouponEventsWithMarketCounts(eventEntities: ISportEventEntity[]): ISportEvent[] {
    eventEntities.forEach((eventEntity: ISportEventEntity) => {
      const childCountObj = eventEntity.event.children.find(child => child.childCount);
      if (childCountObj) { eventEntity.event.marketsCount = Number(childCountObj.childCount.count); }
    });
    return this.buildEvents(eventEntities).map((event: ISportEvent) => Object.assign({}, event));
  }

  /**
   * buildEventsWithOutMarketCounts()
   * @param {ISportEventEntity[]} eventEntities
   * @returns {ISportEvent[]}
   */
  buildEventsWithOutMarketCounts(eventEntities: ISportEventEntity[]): ISportEvent[] {
    const eventsBuilt = this.buildEvents(eventEntities);

    return _.map(eventsBuilt, event => _.extend({}, event));
  }

  /**
   * buildEventsWithScorecasts()
   * @param {ISportEventEntity} eventEntity
   * @returns {any | any[]}
   */
  buildEventsWithScorecasts(eventEntity: ISportEventEntity): any | any[] {
    return _.partial(this.buildMapper, this.addScorecastMarkets)(eventEntity);
  }

  buildEventsWithScoresAndClock(data) {
    let results = data.events;

    results = this.addComments(results, data.comments);
    results = this.addClock(results, data.comments);

    return results;
  }

  /**
   * buildEventWithScores()
   * @param {ISportEvent[]} events
   * @returns {Promise<ISportEvent[]> | Promise<any>}
   */
  buildEventWithScores(events: ISportEvent[]): Promise<ISportEvent[]>|Promise<any> {
    const scoresByAdditionalRequestSports = ['BADMINTON', 'FOOTBALL'],
      scoresInNamesSports = ['VOLLEYBALL', 'HANDBALL', 'BEACH_VOLLEYBALL', 'DARTS'];

    return this.contains(events, scoresByAdditionalRequestSports.concat(scoresInNamesSports))
      ? this.handler(events, scoresByAdditionalRequestSports) : Promise.resolve(events);
  }

  buildInPlayEventsWithMarketsCount(data) {
    const liveNowEvents = _.union(data.nowEvents, data.outrightNowEvents, data.outrightSpecificNowEvents);

    _.forEach(liveNowEvents, nowEvent => {
      (nowEvent as any).isLiveNow = true;
    });

    const upcomingEvents = _.union(data.laterEvents, data.outrightLaterEvents, data.outrightSpecificLaterEvents);

    const eventsArray = data.correction === 'cashout'
      ? _.uniq(_.union(liveNowEvents, upcomingEvents, data.nonLiveServedEvents), ev => (ev as any).id)
      : _.uniq(_.union(liveNowEvents, upcomingEvents), ev => (ev as any).id);

    return this.extendEvents((eventsArray as any), _.defaults(data.laterMarkets, data.nowMarkets), 'marketsCount');
  }

  buildEventsWithExternalKeys(elements) {
    const externalKeys = _.pluck(_.filter(elements, element => (element as any).externalKeys), 'externalKeys');

    if (!externalKeys.length) {
      return elements;
    }

    const events = _.pluck(_.filter(elements, element => (element as any).event), 'event'),
      externalKeysMap = this.getExternalKeysMap(externalKeys);

    _.each(events, event => {
      const eventKeys = externalKeysMap[event.id];

      if (eventKeys) {
        event.externalKeys = eventKeys;
      }
    });

    return _.reject(elements, element => (element as any).externalKeys);
  }

  getLocalTime(event: ISportEvent, isHHformat: boolean = false): string {
    const startTime = Date.parse(event.startTime) || event.startTime;
    let raceLocalTime: string = this.filter.getTimeFromName(event.name);

    if (event.originalName) {
      raceLocalTime = this.filter.getTimeFromName(event.originalName);
    }
    const userLocalTime = (event.categoryCode === 'INTL_TOTE' || isHHformat) ?
        this.time.getLocalHourMinInMilitary(startTime as any) :
        this.time.getLocalHourMin(startTime);
    return raceLocalTime.length > 0 ? raceLocalTime : userLocalTime;
  }

  private checkPresentOf(data: IConstant[], index: number): number {
    return data[index] && data[index].length;
  }

  private isLiveEvent(event: ISportEvent): boolean {
    return event.rawIsOffCode === 'Y' || (event.rawIsOffCode === '-' && event.isStarted);
  }

  private getCorrectedDay(event: ISportEvent): string {
    return (environment.EVENT_CATEGORIES_WITH_WATCH_RULES.indexOf(event.categoryCode) !== -1 ||
            environment.EVENT_CATEGORIES_WITH_WATCH_RULES.indexOf(event.categoryId) !== -1) && event.categoryId !== '19'
      ? this.time.getUTCDay((event.startTime as any)).replace(/sb/i, 'racing')
      : this.time.getUTCDayValue(new Date(event.startTime).getTime());
  }

  private getExternalKeysMap(keys) {
    const requiredKeyTypeCodes = ['OBEvLinkTote', 'OBEvLinkNonTote', 'OBEvLinkScoop6', 'OBEvLinkPlacepot7'],
      keysMap = {};

    _.map(keys, key => {
      if ((key as any).refRecordType && (key as any).refRecordType === 'event'
        && _.contains(requiredKeyTypeCodes, (key as any).externalKeyTypeCode)) {
        const mappings = this.parseKeyString((key as any).mappings, 'event');
        _.map(mappings, ids => {
          const [mainId, linkedId] = ids;

          if (!keysMap[mainId]) {
            keysMap[mainId] = {};
          }

          keysMap[mainId][(key as any).externalKeyTypeCode] = Number(linkedId);
        });
      }
    });

    return keysMap;
  }

  private parseKeyString(keyStr, record) {
    if (!keyStr || !_.isString(keyStr)) {
      return [];
    }

    return _.reduce(keyStr.toLowerCase().split(`,${record},`), (memo, mapStr) => {
      if (mapStr.length > 0) {
        memo.push(mapStr.split(','));
      }
      return memo;
    }, []);
  }

  /**
   * childFree()
   * @param {Object} entity
   * @returns {Object}
   */
  private childFree(entity: Object): Object {
    return _.omit(entity, 'children');
  }

  /**
   * createOutcomeName()
   * @param {IOutcome} outcome
   * @returns {string}
   */
  private createOutcomeName(outcome: IOutcome): string {
    if (this.isHandicapAvailable(outcome)) {
      return outcome.name + this.filter.makeHandicapValue(outcome.children[0].price.handicapValueDec, outcome);
    }

    return outcome.name;
  }

  /**
   * Check outcome for handicap, returns false for Draw or Tie handicap outcomes
   * @param {IOutcome} outcome
   * @returns {boolean}
   */
  private isHandicapAvailable(outcome: IOutcome) {
    const isTieHandicap = outcome.name && outcome.name.toLowerCase().includes('tie');
    return outcome.children && outcome.children[0].price.handicapValueDec && !isTieHandicap;
  }

  /**
   * addComments()
   * @param {ISportEvent[]} events
   * @param rawComments
   * @returns {ISportEvent[]}
   */
  private addComments(events: ISportEvent[], rawComments): ISportEvent[] {
    _.each(events, event => {
      const scoreType = this.scoreParserService.getScoreType(event.categoryId);
      if (rawComments[event.id]) {
        const parser = this.comments[`${event.categoryCode.toLowerCase()}InitParse`];

        if (parser) {
          event.comments = parser(rawComments[event.id]);
        }
      } else if (scoreType) {
        // try to parse score from name and include in comments if success
        const scores = this.scoreParserService.parseScores(event.originalName, scoreType);
        if (scores) {
          if (scores.type === 'SetsGamesPoints') {
            // convert score to tennis comments
            event.comments = this.comments.tennisTransformFallback(scores);
          } else {
            event.comments = {
              teams: scores
            };
          }
          // override event name, since clearEventName from filters.service
          // would not correctly filter scores in all cases
          event.name = `${scores.home.name} v ${scores.away.name}`;
        }
      }
    });

    return events;
  }

  /**
   * addClock()
   * @param {ISportEvent[]} events
   * @param {Object} rawComments
   * @returns {ISportEvent[]}
   */
  private addClock(events: ISportEvent[], rawComments: Object): ISportEvent[] {
    _.each(events, event => {
      if (rawComments[event.id]) {
        const parser = this.comments[`${event.categoryCode.toLowerCase()}ClockInitParse`];

        if (parser) {
          _.extend(event, parser(rawComments[event.id], event.categoryCode.toLowerCase(),
            event.startTime, event.responseCreationTime));
        }
      }
    });

    return events;
  }

  /**
   * addScorecastMarkets()
   * @param {ISportEventEntity} eventEntity
   * @returns {ISportEvent}
   */
  private addScorecastMarkets(eventEntity: ISportEventEntity): ISportEvent {
    this.modifyScorecastMarkets(eventEntity.event);
    return this.eventBuilder(eventEntity);
  }

  /**
   * handler()
   * @param {ISportEvent[]} events
   * @param {string[]} additionalRequest
   * @returns {Promise<ISportEvent[]> | Promise<any>}
   */
  private handler(events: ISportEvent[], additionalRequest: string[]) {
    return this.contains(events, additionalRequest) ? this.scoresExtension(events) : this.scoresInNames(events);
  }

  private scoresInNames(data) {
    data[0].comments = {
      teams: this.comments.parseScoresFromName(data[0].originalName)
    };
    return Promise.resolve(data);
  }

  /**
   * scoresExtension()
   * @param {ISportEvent[]} events
   * @returns {Promise<ISportEvent[]>}
   */
  private scoresExtension(events: ISportEvent[]): Promise<ISportEvent[]> {
    return this.ssRequestHelper.getCommentsByEventsIds({ eventsIds: events[0].id }).then(res => {
      const comments = res.SSResponse.children[0].event.children;

      if (_.isArray(comments) && comments.length) {
        if (this.sportEventHelperService.isFootball(events[0])) {
          events[0].comments = this.comments.footballInitParse(comments);
        } else {
          const periods = _.filter(comments[0].eventPeriod.children, el => (el as any).eventPeriod);
          let lastPeriod = _.max(periods, el => (el as any).eventPeriod.periodIndex);
          lastPeriod = (lastPeriod as any).eventPeriod.children;
          const current = _.sortBy(
            _.filter(
              (lastPeriod as any), el => (el as any).eventFact),
            el => (el as any).eventFact.eventParticipantId);
          const scores = _.sortBy(
            _.filter(
              comments[0].eventPeriod.children, el => (el as any).eventFact),
            el => (el as any).eventFact.eventParticipantId);
          const participants = _.filter(comments, el => el.eventParticipant);

          (events[0] as any).comments = {
            teams: {
              home: {
                currentPoints: (current[0] as any).eventFact.fact,
                score: (scores[0] as any).eventFact.fact,
                name: this.filter.removeLineSymbol(participants[0].eventParticipant.name)
              },
              away: {
                currentPoints: (current[1] as any).eventFact.fact,
                score: (scores[1] as any).eventFact.fact,
                name: this.filter.removeLineSymbol(participants[1].eventParticipant.name)
              }
            }
          };
        }
      }

      return events;
    });
  }

  private extendEvents(eventsList: ISportEvent[], extendingObject: Object, key: string) {
    _.each(eventsList, event => {
      if (extendingObject[event.id]) {
        event[key] = extendingObject[event.id];
      }
    });
    return eventsList;
  }

  /**
   * modifyScorecastMarkets()
   * @param {ISportEvent} event
   */
  private modifyScorecastMarkets(event: ISportEvent): void {
    if (event.children) {
      let i = event.children.length - 1;

      for (i; i >= 0; i--) {
        const marketEntity = event.children[i],
          children = marketEntity.market.children;

        if (children && children.length && children[0].scorecast) {
          marketEntity.market.children = children.map(s => ({ outcome: s.scorecast }));
        }
      }
    }
  }

  /**
   * contains()
   * @param {any | any[]} data
   * @param {any[]} sportsArray
   * @returns {boolean}
   */
  private contains(data: any|any[], sportsArray: any[]): boolean {
    return _.contains(sportsArray, data && data[0] && data[0].categoryCode);
  }

  /**
   * priceBuilder()
   * @param {IPriceEntity} priceEntity
   * @returns {IPrice}
   */
  private priceBuilder(priceEntity: IPriceEntity): IPrice {
    if (priceEntity.hasOwnProperty('historicPrice') && priceEntity.historicPrice.hasOwnProperty('livePriceDec')) {
      priceEntity.historicPrice.livePriceDec = Number(priceEntity.historicPrice.livePriceDec);
      return priceEntity.historicPrice;
    }

    if (priceEntity.price.priceDec) {
      priceEntity.price.priceDec = Number(priceEntity.price.priceDec);
    }

    if (priceEntity.price.priceDen) {
      priceEntity.price.priceDen = Number(priceEntity.price.priceDen);
    }

    if (priceEntity.price.priceNum) {
      priceEntity.price.priceNum = Number(priceEntity.price.priceNum);
    }

    return priceEntity.price;
  }

  /**
   * buildMapper()
   * @param {Function} builderFn
   * @param {any | any[]} elements
   * @returns {any | any[]}
   */
  private buildMapper(builderFn: Function, elements: any|any[]): any|any[] {
    return _.map(elements, _.compose(this.childFree, builderFn));
  }

  private setTrapNumber(outcome: IOutcome): IOutcome {
    if (outcome.runnerNumber) {
      const index = outcome.name.search(/(\(RES\))/);
      outcome.trapNumber = index !== -1 ? outcome.displayOrder : Number(outcome.runnerNumber);
    }

    return outcome;
  }

  /**
   * To fetch correct day value
   * @param {string} sportEventEntity
   * @returns {string}
   */
  private getDayValue(sportEvent: ISportEvent): string {
    if (sportEvent.categoryId === this.GREY_HOUND_CATEGORY_ID || sportEvent.categoryId === this.HORSE_RACING_CATEGORY_ID) {
      if (sportEvent.categoryId === this.GREY_HOUND_CATEGORY_ID) {
        return this.time.getUTCDay(new Date(sportEvent.startTime)).replace(/sb/i, 'racing');
      } else {
        return this.time.getUTCDayValue((new Date(sportEvent.startTime).getTime() as any)).replace(/sb/i, 'racing');
      }
    } else {
      return this.time.getCorrectDay(sportEvent.startTime);
    }
  }
}
