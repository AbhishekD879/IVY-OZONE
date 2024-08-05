import { forkJoin, Observable, of, throwError, interval } from 'rxjs';
import { map, concatMap, catchError, share } from 'rxjs/operators';

import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';
import {
  marketsTemplateMap, verticalTemplateName,
  VIRTUAL_ROUTE_NAME
} from './../constants/virtual-sports.constant';

import { TimeService } from '@core/services/time/time.service';
import { EventProvider } from '@app/vsbr/services/event.provider';
import { VirtualSportsMapperService } from '@app/vsbr/services/virtual-sports-mapper.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { InsomniaService } from '@core/services/insomnia/insomnia.service';

import { IMarketsTemplateMap, IMarketsMap } from './../models/virtual-sports-config.model';

import { IOutcomeEntity } from '@core/models/outcome-entity.model';
import { IMarketEntity } from '@core/models/market-entity.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { ISportEventEntity } from '@core/models/sport-event-entity.model';
import { IOutcome } from '@core/models/outcome.model';
import { IMarket } from '@core/models/market.model';
import { IEventSSResponse, ISportEventGroup, ISsResponse } from '@app/vsbr/models/virtuals-ss-respose.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import {
  ICategoryAliases,
  IVirtualCategoryStructure,
  IVirtualChildCategory
} from '@app/vsbr/models/virtual-sports-structure.model';
import { IVirtualSports } from '@core/services/cms/models/virtual-sports.model';
import { ILiveServeUpd } from '@core/models/live-serve-update.model';
import { EventService } from '@app/sb/services/event/event.service';

@Injectable()
export class VirtualSportsService {
  time: Observable<number> = interval(1000).pipe(
    map(() => Date.now()),
    share()
  );
  private TYPE_IDS_LEGENDS: string[] = [];
  private LEGENDS_SPORT_ID = '223';
  private marketsTemplateMap: IMarketsTemplateMap = marketsTemplateMap;
  private eventsBuffer: object = {};
  private deltaTimeNowUnix: number = 0;
  private chunkSize: number = 100;
  private isReloadedAfterSleep: boolean = false;
  private marketsTemplate: IMarketsMap;
  private BR_TYPE_ID: string[] = environment.BR_TYPE_ID;
  private updateEventsInterval: number;
  private horizontalDipCodes: string[] = ['HH', 'MR', 'WH', 'HL'];
  private liveServeUpdateEventListenerSubscription: Function;
  private subscribedVSBREventsIdList: string[] = [];

  constructor(
    public vsMapperService: VirtualSportsMapperService,
    private timeService: TimeService,
    private eventProvider: EventProvider,
    private pubsub: PubSubService,
    private filterService: FiltersService,
    private localeService: LocaleService,
    private windowRef: WindowRefService,
    private insomniaService: InsomniaService,
    private cmsService: CmsService,
    private eventService: EventService
  ) {
    this.marketsTemplate = this.reverseMap(this.marketsTemplateMap);
  }

  addLiveServeUpdateEventListener(): void {
    const callback = (data: CustomEvent) => {
      const update = data.detail.liveUpdate;
      this.finishEvent(update);
    };

    this.windowRef.document.addEventListener('LIVE_SERVE_UPDATE', callback);

    this.liveServeUpdateEventListenerSubscription = () => {
      this.windowRef.document.removeEventListener('LIVE_SERVE_UPDATE', callback);
    };
  }

  removeLiveServeUpdateEventListener(): void {
    if (this.liveServeUpdateEventListenerSubscription) {
      this.liveServeUpdateEventListenerSubscription();
      this.liveServeUpdateEventListenerSubscription = undefined;
    }
  }

  unsubscribeFromUpdates(): void {
    if (this.updateEventsInterval) {
      this.windowRef.nativeWindow.clearInterval(this.updateEventsInterval);
    }
  }

  subscribeForUpdates(): void {
    if (this.updateEventsInterval) {
      this.unsubscribeFromUpdates();
    }
    this.updateEventsInterval = this.windowRef.nativeWindow.setInterval(() => {
      // update classes timeFactory.refreshInterval
      this.updateEvents();
    }, this.timeService.refreshInterval);
  }

  subscribeVSBRForUpdates(events: ISportEventEntity[]): void {
    // liveServChannels
    const channel = events.map((e: ISportEventEntity) => {
      this.subscribedVSBREventsIdList.push(e.event.id.toString());
      return e.event.liveServChannels.replace(',', '');
    });

    this.pubsub.publish('SUBSCRIBE_LS', {
      channel,
      module: 'vsbr'
    });
  }

  unSubscribeVSBRForUpdates(): void {
    this.subscribedVSBREventsIdList = [];
    this.pubsub.publish('UNSUBSCRIBE_LS', 'vsbr');
  }

  /**
   * Check if event finished, and broadcast 'VS_EVENT_FINISHED' event
   * @params{array} arrResponse events array
   */
  finishEvent(event: ILiveServeUpd): void {
    const payload = event && event.payload;
    const eventId = event && event.subject_number.toString();
    const isSubscribedVSBREvent = this.subscribedVSBREventsIdList.indexOf(eventId) > -1;

    if (!isSubscribedVSBREvent) {
      return;
    }

    if (payload && payload.result_conf && payload.result_conf === 'Y') {
      this.pubsub.publish(this.pubsub.API.VS_EVENT_FINISHED, {
        eventId: eventId
      });
    }
  }

  normalizeData(eventChild: ISportEventEntity, isEventOngoing: boolean): ISportEvent {
    // normalize event structure
    eventChild.event.markets = [];
    eventChild.event.eventStatusCode = isEventOngoing ? 'S' : eventChild.event.eventStatusCode;
    eventChild.event && eventChild.event.children && eventChild.event.children.forEach((marketChild) => {
      marketChild.market.marketName = marketChild.market.name;
      if (eventChild.event.className !== 'Virtual Speedway' && this.showTerms(marketChild.market)) {
        marketChild.market.isEachWayAvailable = true;
        marketChild.market.terms = this.genTerms(marketChild.market);
      }
      marketChild.market.outcomes = [];
      marketChild.market.children.forEach((outcomeChild) => {
        const runnerNumber = outcomeChild.outcome.drawNumber || outcomeChild.outcome.runnerNumber;
        outcomeChild.outcome.runnerNumber = runnerNumber || outcomeChild.outcome.silkName;
        outcomeChild.outcome.silkName = outcomeChild.outcome.silkName || runnerNumber;
        marketChild.market.outcomes.push(outcomeChild.outcome);
      });
      eventChild.event.markets.push(marketChild.market);
      marketChild.market.outcomes.sort(outcome => outcome.displayOrder);
    });
    Object.assign(eventChild.event, this.eventService.isLiveStreamAvailable(eventChild.event));
    return eventChild.event;
  }

  /**
   * show terms
   * @params{object} market entity
   * @return {boolean}
   */
  showTerms(marketEntity: IMarket): boolean {
    if (!marketEntity || !Object.keys(marketEntity).length) {
      return false;
    }

    return Boolean(marketEntity.eachWayFactorNum &&
      marketEntity.eachWayFactorDen &&
      marketEntity.eachWayPlaces);
  }

  /**
   * Generate terms
   * @param marketEntity
   * @returns {string}
   */
  genTerms(marketEntity: IMarket): string {
    if (!marketEntity || !Object.keys(marketEntity).length) {
      return '';
    }

    let oddsString = '',
      i = 0;

    const eachWayPlaces = Number(marketEntity.eachWayPlaces);

    // 5 -> '1,2,3,4,5'
    while (i < eachWayPlaces) {
      oddsString += (++i >= eachWayPlaces) ? i : `${i}-`;
    }

    return this.localeService.getString('vsbr.oddsAPlaces', {
      num: marketEntity.eachWayFactorNum,
      den: marketEntity.eachWayFactorDen,
      arr: oddsString
    });
  }

  /**
   * Get active child category
   * @param {String} classAlias
   * @returns {IVirtualChildCategory} active child category
   */
  getActiveClass(classAlias: string): IVirtualChildCategory {
    return this.vsMapperService.getChildByAlias(classAlias);
  }

  /**
   * filter events (return events without isFinished and isResulted)
   * delete event is event next to it is started
   * @params{array} events array
   * @return{object} active class
   */
  filterEvents(events: ISportEventEntity[]) {
    const activeEvents = _.filter(events, (eventItem: ISportEventEntity) => {
      return !eventItem.event.isFinished && !eventItem.event.isResulted;
    });

    return this.deleteOutDatedEvents(activeEvents);
  }

  /**
   * get section array by market names
   * @params{object} event
   * @params{string} event id
   * @return{array} array of sections objects(contain market objects)
   */
  getMarketSectionsArray(eventItem: ISportEventEntity): IMarketEntity[] {
    const markets = [];

    eventItem.event && eventItem.event.children && eventItem.event.children.forEach((market: IMarketEntity) => {
      const arrangedMarket = this.filterOutcomes(market.market);

      arrangedMarket.name = this.filterName(arrangedMarket.name);

      if (arrangedMarket.dispSortName === 'CS' && eventItem.event.className.includes('Virtual Football')) {
        arrangedMarket.children = this.groupCorrectScoreOutcomes(arrangedMarket);
        arrangedMarket.template = 'Column';
      } else if (arrangedMarket.dispSortName && (this.horizontalDipCodes.includes(arrangedMarket.dispSortName))) {
        arrangedMarket.template = 'Horizontal';
      } else {
        arrangedMarket.template = this.marketsTemplate[arrangedMarket.name.toLowerCase()] || verticalTemplateName;
      }

      arrangedMarket.displayOrder = Number(arrangedMarket.displayOrder);
      arrangedMarket.sectionTitle = this._getMarketSectionTitle(arrangedMarket.name);

      markets.push(arrangedMarket);
    });

    return markets;
  }

  /**
   * get active class events
   * @params{string} category alias
   * @return{promise} events with racing forms
   */
  getEventsWithRacingForms(alias: string): Promise<ISportEventEntity[]> {
    return new Promise((resolve, reject) => {
      const eventClass = this.getCategoryByAlias(alias);
      if (!this.eventsBuffer[eventClass]) {
        reject();
        return;
      }

      this.eventsBuffer[eventClass] = _.filter(this.eventsBuffer[eventClass], (item: ISportEventEntity) => {
        return this.BR_TYPE_ID.indexOf(item.event.typeId) === -1;
      });

      const eventsBufferForClass = this.eventsBuffer[eventClass];
      const requestsToSiteServe = this.constructEventRequestsByChunks(eventsBufferForClass);
      forkJoin(requestsToSiteServe).subscribe((eventsFromMultipleRequests: ISsResponse[][]) => {
        // merge events from chunks requests
        const events = ([] as ISsResponse[]).concat.apply([], eventsFromMultipleRequests);

        eventsBufferForClass.forEach((eventBufferItem: ISportEventEntity, index) => {
          const suitableSiteServeEvents = events.filter(eventElem => eventElem.event.id === eventBufferItem.event.id);
          if (suitableSiteServeEvents.length > 0) {
            const eventFromSiteServe = suitableSiteServeEvents[0].event;
            if (eventFromSiteServe && index === eventsBufferForClass.length - 1) {
              resolve(this.eventsBuffer[eventClass]);
            }

            eventBufferItem.event = eventFromSiteServe;
          } else {
            reject();
            return;
          }
        });
      }, () => {
        reject();
        return;
      });
    });
  }

  /*
   This method is used for constructing requests by chunks
   because of siteserve limitation for eventIds amount passed
   */
  constructEventRequestsByChunks(eventsBufferForClass: { event: ISportEvent }[]): Observable<ISsResponse[]>[] {
    const chunks = [];
    for (let i = 0, j = eventsBufferForClass.length; i < j; i += this.chunkSize) {
      chunks.push(eventsBufferForClass.slice(i, i + this.chunkSize));
    }

    return chunks.map(chunk => {
      const eventIdsSeparatedString = chunk
        .filter(eventItem => eventItem.event && eventItem.event.id)
        .map(eventItem => eventItem.event.id.toString())
        .join(',');
      return this.eventProvider.getEventsGroup(eventIdsSeparatedString)
        .pipe(catchError(error => of([])));
    });
  }

  /**
   * get events category by Alias
   * @params{string} category alias
   * @return{number} class Id
   */
  getCategoryByAlias(alias: string): string {
    const child: IVirtualChildCategory = this.vsMapperService.getChildByAlias(alias);

    return child && child.classId;
  }

  /**
   * get parent and child categories alias by  child class id
   * @params {string} classId
   * @return {string} parent and child aliases
   */
  getAliasesByClassId(classId: string): ICategoryAliases {
    return this.vsMapperService.getAliasesByClassId(classId);
  }

  /**
   * Getter for prop that tells if was returned from sleep mode or connection lost
   * @return {Boolean}
   */
  isReloaded(): boolean {
    return this.isReloadedAfterSleep;
  }

  /**
   * Setter for prop that tells if was returned from sleep mode or connection lost
   * @param {Boolean} value
   */
  setIsReloaded(value: boolean): void {
    this.isReloadedAfterSleep = value;
  }

  /**
   * Get events data.
   * @params{array} events
   * @return{observable} eventsData: events array, categories array
   */
  eventsData(lazyLoadRun: boolean = false, timeRangeStart?: string, timeRangeEnd?: string): Observable<IVirtualCategoryStructure[]> {
    let selectTimeRangeStart: string = timeRangeStart || this.timeService.getGmtTime();
    const date = new Date(selectTimeRangeStart);
    const gmtDate = new Date((date.valueOf() - this.timeService.min * 60) + (date.getTimezoneOffset() * this.timeService.min));
    selectTimeRangeStart = `${this.timeService.formatByPattern(gmtDate.toString(),'yyyy-MM-ddTHH:mm:ss')}Z`;
    const selectTimeRangeEnd: string = timeRangeEnd || this.timeService.selectTimeRangeEnd();

    let classes: string[] = [];
    let virtualSports: IVirtualCategoryStructure[];
    this.vsMapperService.structure = [];

    return this.cmsService.getVirtualSports().pipe(
      concatMap((virtualSportsInfo: IVirtualSports[]) => {
        virtualSports = virtualSportsInfo || [];

        virtualSports.forEach((sport: IVirtualCategoryStructure) => {
          sport.title = this.filterService.removeLineSymbol(sport.title);
          sport.alias = this.generateClass(sport.title);
          sport.targetUri = `/${VIRTUAL_ROUTE_NAME}/${sport.alias}`;

          this.vsMapperService.setParentCategory(sport);

          const tracks = sport.tracks || [];

          tracks.forEach((track: IVirtualChildCategory) => {
            track.title = this.filterService.removeLineSymbol(track.title);
            track.alias = this.generateClass(track.title);

            this.vsMapperService.setChildCategory(sport.alias, track);
          });
          this.setLegendsTypeIds(sport);
        });

        classes = this.vsMapperService.getAllClasses();

        if (!classes.length) {
          return throwError('noCategories');
        }

        return this.eventProvider.getEventForClass({
          classId: classes.join(','),
          startTime: selectTimeRangeStart,
          endTime: selectTimeRangeEnd,
          brTypes: this.getBrTypesString()
        });
      }),
      map((virtualSportsClasses: IEventSSResponse): IVirtualCategoryStructure[] => {
        const arrResponse: ISportEventGroup = this.groupEventsByClass(this.configureEvents(virtualSportsClasses.SSResponse.children));

        // Filters bet radar and non-legends for Legends type.
        _.forEach(arrResponse, (categoryClass: ISportEventEntity[], key) => {
          if (key === this.LEGENDS_SPORT_ID && this.TYPE_IDS_LEGENDS) {
            arrResponse[key] = categoryClass.filter((item: ISportEventEntity) => {
              return this.BR_TYPE_ID.indexOf(item.event.typeId) === -1
                && this.TYPE_IDS_LEGENDS.indexOf(item.event.typeId) > -1;
            });
          } else {
            arrResponse[key] = categoryClass.filter((item: ISportEventEntity) => {
              return this.BR_TYPE_ID.indexOf(item.event.typeId) === -1;
            });
          }
        });

        this.pubsub.subscribe('virtualSport', 'INSOMNIA', data => {
          if (data.actionType === 'category-update') {
            // Get the closest event ETA and ID.
            if (arrResponse[data.classId]) {
              const childCategory = this.vsMapperService.getChildByClassId(data.classId);

              if (childCategory) {
                this.updateCategoryClasses(arrResponse[data.classId], childCategory);
                childCategory.events = arrResponse[childCategory.classId];
              }
            } else {
              return this.vsMapperService.structure; // if no events
            }
          }
        });

        classes.forEach((classId: string) => {
          // Initialize recursive update of the next event ID and ETA.
          if (!lazyLoadRun) {
            // Get the closest event ETA and ID.
            if (arrResponse[classId]) {
              const childCategory = this.vsMapperService.getChildByClassId(classId);

              if (childCategory) {
                this.updateCategoryClasses(arrResponse[classId], childCategory);
                childCategory.events = arrResponse[childCategory.classId];
              }
            } else {
              return this.vsMapperService.structure; // if no events
            }
            // Only first run.
            this.eventsBuffer = arrResponse;

            this.vsMapperService.structure.forEach((parentSport: IVirtualCategoryStructure) => {
              parentSport.childs.forEach((childCategory: IVirtualChildCategory) => {
                if (arrResponse[childCategory.classId]) {
                  childCategory.events = arrResponse[childCategory.classId];
                  this.vsMapperService.setChildCategory(parentSport.alias, childCategory);
                }
              });
            });
            return this.vsMapperService.structure;
          } else {
            this.updateEventsBuffer(arrResponse, classes);
          }
        });

        return this.vsMapperService.structure;
      }));
  }

  generateClass(input: string): string {
    let tempClassName = input.replace(/\|/g, '');
    tempClassName = tempClassName.replace(/\s/g, '-');
    return tempClassName.toLowerCase();
  }

  /**
   * Update child categories of parent category.
   * @params{array} category events
   * @params{IVirtualChildCategory} child category
   */
  updateCategoryClasses(categoryEvents: ISportEventEntity[], childCategory: IVirtualChildCategory): void {
    for (let i = 0; i < categoryEvents.length; i++) {
      if (categoryEvents[i].event.startTimeUnix > Date.now() - this.timeService.eventOngoingGuess) {
        childCategory.startTimeUnix = categoryEvents[i].event.startTimeUnix;
        childCategory.timeLeft = childCategory.startTimeUnix - Date.now();
        this.subscribeForClassUpdates(childCategory);
        break;
      } else if (i === (categoryEvents.length - 1)) {
        childCategory.timeLeft = 0;
        this.windowRef.nativeWindow.stopEventActual = this.windowRef.nativeWindow.useStopEventActual = () => {
          // If no any new events present.
        };
      }
    }
  }

  /**
   * Set priceDec, isUS properties for outcomes
   * @params{array} markets
   * @params{boolean} isUSSport
   * @return{array} markets
   */
  private configureOutcomes(markets: IMarketEntity[], isUSSport: boolean): IMarketEntity[] {
    _.forEach(markets, (market: IMarketEntity, marketKey) => {
      _.forEach(market.market.children, (item: IOutcomeEntity, itemKey) => {
        markets[marketKey].market.children[itemKey].outcome.isUS = isUSSport;
      });
    });
    return markets;
  }

  /**
   * Set priceDec, isUS properties for outcomes
   * @params{array} markets
   * @params{boolean} isUSSport
   * @return{array} markets
   */
  private configureEvents(eventsObject: ISportEventEntity[]): ISportEventEntity[] {
    let events: ISportEventEntity[] = _.filter(eventsObject, (eventItem: ISportEventEntity): boolean => {
      return !!eventItem.event;
    });
    _.each(events, (eventItem: ISportEventEntity) => {
      const isUSSport = _.has(eventItem.event, 'typeFlagCodes') &&
        eventItem.event.typeFlagCodes.indexOf('US') !== -1;

      eventItem.event.startTimeUnix = Date.parse(eventItem.event.startTime);
      // Time removed from title because of service timezone bug.
      eventItem.event.name = eventItem.event.name.replace(/^\d*:\d\d\s/, '');
      eventItem.event.children = this.configureOutcomes(eventItem.event.children, isUSSport);
    });
    events = this.filterService.orderBy(events, ['event.startTimeUnix']);

    return events;
  }

  /**
   * Group events by classes.
   * @params{array} events
   * @return{array} groups with events
   */
  private groupEventsByClass(array: ISportEventEntity[]): ISportEventGroup {
    const f = item => {
        return [item.event.classId];
      },
      groups = {};

    array.forEach((o: ISportEventEntity) => {
      const group = f(o)[0];
      groups[group] = groups[group] || [];
      groups[group].push(o);
    });
    return groups;
  }

  /**
   * create web worker for receiveng class updates.
   * @params{array} category
   * @params{number} categoryIndex
   * @params{number} category index
   */
  private subscribeForClassUpdates(childCategory: IVirtualChildCategory): void {
    if (typeof (this.windowRef.nativeWindow.stopEventActual) === 'undefined') {
      this.insomniaService.setTimeoutAction({
        classId: Number(childCategory.classId),
        eventName: `category-update-${childCategory.classId}`,
        actionType: 'category-update'
      }, childCategory.startTimeUnix - Date.now() + this.timeService.eventOngoingGuess);
    }
  }

  /**
   * Update events buffer.
   * @params{array} events
   * @params{array} classes
   */
  private updateEventsBuffer(events: ISportEventGroup, classes: string[]): void {
    _.forEach(classes, (classId: string) => {
      if (events[classId]) {
        // Update events buffer
        _.forEach(events[classId], (newEvent: ISportEventEntity) => {
          this.eventsBuffer[classId].push(newEvent);
        });
      }
    });
  }

  /**
   * Gets br types string event from those sports have to be excluded.
   * @return {string} - url string.
   */
  private getBrTypesString(): string {
    return _.reduce(this.BR_TYPE_ID, (res, id, i) => {
      // eslint-disable-next-line no-param-reassign
      res += `simpleFilter=event.typeId:notEquals:${id}`;
      // eslint-disable-next-line no-param-reassign
      res += (i === this.BR_TYPE_ID.length - 1) ? '' : '&';
      return res;
    }, '');
  }

  /**
   * Update events, get new events with updated time range
   * @params{array} arrResponse events array
   */
  private updateEvents(): void {
    this.deltaTimeNowUnix += this.timeService.refreshInterval;

    const selectTimeRangeStart = this.timeService.selectTimeRangeStartDelta(this.deltaTimeNowUnix),
      selectTimeRangeEnd = this.timeService.selectTimeRangeEndDelta(this.deltaTimeNowUnix);

    this.eventsData(true, selectTimeRangeStart, selectTimeRangeEnd)
      .subscribe();
  }

  /**
   * delete event if event next to it started already
   * @params{object} event
   * @return{array} array of filtered events
   */
  private deleteOutDatedEvents(events: ISportEventEntity[]): ISportEventEntity[] {
    for (let i = 1; i < events.length; i++) {
      if (events[i].event.startTimeUnix < Date.now()) {
        events.splice(i - 1, 1);
        i = i - 1;
      }
    }

    return events;
  }

  private _isWinOrEw(name: string): boolean {
    return ['To Win', 'To-Win'].indexOf(name) !== -1;
  }

  private _isMatchBetting(name: string): boolean {
    return ['Match Betting', 'Match Result', 'Win/Draw/Win', 'Head/Head (winner)'].indexOf(name) !== -1;
  }

  /**
   * Return section title based on market name
   * @param marketName
   * @returns {*}
   * @private
   */
  private _getMarketSectionTitle(marketName: string): string {
    if (this._isWinOrEw(marketName)) {
      return 'Win or E/W';
    } else if (this._isMatchBetting(marketName)) {
      return 'Match Betting';
    }

    return marketName;
  }

  /**
   * reversing map from arrays values to keys,
   * example:
   * from { asd: ['a', 's', 'd'], zxc: ['z', 'x', 'c'] }
   * to {a: 'asd', s: 'asd', d: 'asd', z: 'zxc', x: 'zxc', c: 'zxc'}
   * @param map
   */
  private reverseMap(originalMap: IMarketsTemplateMap): IMarketsMap {
    const newMap = {};

    for (const templateKey in originalMap) {
      if (Object.prototype.hasOwnProperty.call(originalMap, templateKey)) {
        originalMap[templateKey].forEach(marketName => {
          newMap[this.filterName(marketName).toLowerCase()] = templateKey;
        });
      }
    }

    return newMap;
  }

  private filterName(name: string): string {
    return name && name.replace(/\|/g, '');
  }

  /**
   * filter market outcomes
   * @params{object} market
   * @return{object} market object
   */
  private filterOutcomes(market: IMarket): IMarket {
    // sort outcomes
    market.children = this.sortOutcomes(market.children);
    // get outcomeMeaningMinorCode
    _.forEach(market.children, (entity: IOutcomeEntity) => {
      if (entity.outcome && entity.outcome.outcomeMeaningMinorCode) {
        entity.outcome.outcomeMeaningMinorCode = this.getCorrectedOutcomeMeaningMinorCode(entity.outcome);
      }
    });
    return market;
  }

  /**
   * sort outcomes
   * @params{array} outcomes array
   * @return{array} filtered outcomes array
   */
  private sortOutcomes(outcomesArray: IOutcomeEntity[]): IOutcomeEntity[] {
    return _.has(outcomesArray[0].outcome, 'isUS')
      ? this.filterService.orderBy(outcomesArray, ['outcomeMeaningMinorCode']) : outcomesArray;
  }

  /**
   * get Corrected Outcome Meaning Minor Code
   * @params{object} outcome enitity
   * @return{number} outcomeMeaningMinorCode
   */
  private getCorrectedOutcomeMeaningMinorCode(outcomeEntity: IOutcome): number {
    let outcomeMeaningMinorCode = outcomeEntity.outcomeMeaningMinorCode;
    if (_.isNaN(parseInt(outcomeMeaningMinorCode.toString(), 10))) {
      switch (outcomeMeaningMinorCode.toString()) {
        case 'H':
          outcomeMeaningMinorCode = outcomeEntity.isUS ? 3 : 1;
          break;
        case 'D':
        case 'N':
        case 'L':
          outcomeMeaningMinorCode = 2;
          break;
        case 'A':
          outcomeMeaningMinorCode = outcomeEntity.isUS ? 1 : 3;
          break;
        default:
          break;
      }
    }

    return Number(outcomeMeaningMinorCode);
  }

  /**
   * Groups market outcomes based on outcomeMeaningScores.
   * @param {Object} market Market data.
   * @return {Array}
   */
  private groupCorrectScoreOutcomes(market: IMarket): IOutcomeEntity[] {
    const outcomes: IOutcomeEntity[] = market.children,
      items: IOutcome[] = (outcomes.length && outcomes[0].outcome) ? _.pluck(outcomes, 'outcome') : outcomes;

    _.each(items, (item, index) => {
      const scores = _.isString(item.outcomeMeaningScores) && item.outcomeMeaningScores.split(',').slice(0, -1);

      if (scores && scores.length) {
        item.outcomeMeaningMinorCode = this.getCode(Number(scores[0]), Number(scores[1]));
      } else {
        // if scores are not set for the market, set MeaningMinorCode to 1, 2, 3
        item.outcomeMeaningMinorCode = (index % 3) + 1;
      }
    });

    return _.map(
      _.sortBy(items, 'name'), (outcome: IOutcome) => {
        return { outcome, outcomeMeaningMinorCode: outcome.outcomeMeaningMinorCode };
      }
    );
  }

  /**
   * Returns number code based on equality check of passed values.
   * @param {number} val1
   * @param {number} val2
   * @return {number}
   */
  private getCode(val1: number, val2: number): number {
    if (val1 > val2) {
      return 1;
    }
    if (val1 === val2) {
      return 2;
    }
    return 3;
  }

  /**
   * Retreving Type Ids defined in CMS
   * @param  {IVirtualCategoryStructure} sport
   * @returns void
   */
  private setLegendsTypeIds(sport: IVirtualCategoryStructure): void {
    if ('Legends'.indexOf(sport.title) != -1 && sport.childs && sport.childs.size) {
      const legendsChildSport = sport.childs.get(this.LEGENDS_SPORT_ID);
      if (legendsChildSport && legendsChildSport.typeIds) {
        // legendsChildSport['typeIds'] = '103153,103154'; //
        // const typeIds = legendsChildSport['typeIds'].trim().split(/\s*,\s*/);
        const typeIds = legendsChildSport.typeIds.trim().split(/\s*,\s*/);
        this.TYPE_IDS_LEGENDS = typeIds;
      }
    }
  }
}
