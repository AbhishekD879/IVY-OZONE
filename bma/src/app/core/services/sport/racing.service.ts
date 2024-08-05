import { Observable, from, forkJoin, throwError, of } from 'rxjs';
import { map, concatMap, catchError, mergeMap } from 'rxjs/operators';

import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import environment from '@environment/oxygenEnvConfig';
import { IMarket } from '@core/models/market.model';
import { ICombinedSportEvents, ISportEvent } from '@core/models/sport-event.model';
import { ISportServiceConfig } from '@core/models/sport-service-config.model';
import { ISportServiceRequestConfig } from '@core/models/sport-service-request-config.model';
import { CommandService } from '@core/services/communication/command/command.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { LiveUpdatesWSService } from '@core/services/liveUpdatesWS/liveUpdatesWS.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { LpAvailabilityService } from '@core/services/lpAvailability/lp-availability.service';
import { SportService } from '@core/services/sport/sport.service';
import { TimeService } from '@core/services/time/time.service';
import { EventService } from '@sb/services/event/event.service';
import { TemplateService } from '@shared/services/template/template.service';
import { IInitialSportConfig, IInitialSportTab } from '@core/services/sport/config/initial-sport-config.model';
import { RacingYourCallService } from '@core/services/racing/racingYourCall/racing-your-call.service';
import { UkToteService } from '@uktote/services/ukTote/uk-tote.service';
import { DailyRacingService } from '@core/services/racing/dailyRacing/daily-racing.service';
import { TimeFormService } from '@core/services/racing/timeForm/time-form.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { RACING_CONFIG } from '@platform/core/services/sport/config/racing.constant';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models/system-config';
import { RacingPostService } from '@coreModule/services/racing/racingPost/racing-post.service';
import {
  IRacingDataHubConfig,
  IRacingPostGHResponse,
  IRacingPostHRResponse
} from '@coreModule/services/racing/racingPost/racing-post.model';
import { ITimeFormData } from '@core/models/time-form-data.model';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { IRaceGridMeeting, IGroupedRacingItem } from '@core/models/race-grid-meeting.model';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { IRacingEdpMarket } from '@core/services/cms/models/racing-edp-market.model';

@Injectable()
export class RacingService extends SportService {

  ANTEPOST_SWITCHER_KEYS: string[];

  private readonly BYBConfig;
  private readonly racingConfig = RACING_CONFIG;
  private countryFlags = RACING_CONFIG.COUNTRY_FLAGS;
  private readonly TIME_INTERVAL = 600000; // 10 Minutes time interval
  private readonly GREYHOUND_ID: string = environment.CATEGORIES_DATA.racing.greyhound.id;
  private readonly featuredTabs: string[] = RACING_CONFIG.FEATURED_TABS;
  private birMarketsEnabled: string[];

  constructor(
    protected timeformService: TimeFormService,
    protected ukToteService: UkToteService,
    protected dailyRacingService: DailyRacingService,
    protected eventFactory: EventService,
    protected templateService: TemplateService,
    protected timeService: TimeService,
    protected filtersService: FiltersService,
    protected liveUpdatesWSService: LiveUpdatesWSService,
    protected channelService: ChannelService,
    protected lpAvailabilityService: LpAvailabilityService,
    protected commandService: CommandService,
    protected localeService: LocaleService,
    protected racingYourcallService: RacingYourCallService,
    protected pubSubService: PubSubService,
    protected cmsService: CmsService,
    protected racingPostService: RacingPostService,
    protected routingHelperService: RoutingHelperService
  ) {
    super(eventFactory, templateService, timeService, liveUpdatesWSService, channelService, filtersService, pubSubService);
    this.BYBConfig = environment.BYB_CONFIG;
    this.ANTEPOST_SWITCHER_KEYS = RACING_CONFIG.ANTEPOST_SWITCHER_KEYS;
  }

  /**
   * setConfig()
   * @param {IInitialSportConfig} generalConfig
   * @returns {this}
   */
  setConfig(generalConfig: IInitialSportConfig): this {
    this.generalConfig = generalConfig;
    this.config = this.extendConfig(generalConfig.config);
    this.readonlyRequestConfig = Object.assign({}, generalConfig.config.request);

    return this;
  }

  /**
   * getConfig()
   * @returns {ISportServiceConfig}
   */
  getConfig(): ISportServiceConfig {
    return this.config;
  }

  getGeneralConfig(): IInitialSportConfig {
    return this.generalConfig;
  }

  /**
   * getEvents()
   * @param {string} selectedTab
   * @param {boolean} isGrouped
   * @returns {Promise<ISportEvent[]>}
   */
  getEvents(selectedTab: string, isGrouped: boolean): Promise<ISportEvent[]> {
    const eventMethod: string = (this.featuredTabs.includes(selectedTab) && isGrouped) ? RACING_CONFIG.FEATURED_MS : selectedTab;
    return this[this.getConfig().eventMethods[eventMethod]](isGrouped)
      .then(result => {
          if (!this.getConfig().inConnectApp) {
            const groupObj = eventMethod === 'ms'  ? {groupedRacing: [], classesTypeNames: []} : {};
            _.extend(result, {selectedTab, modules: this.getConfig().request.modules, ...groupObj});
          }
          return this.getConfig().name === 'horseracing'
            ? Promise.resolve(result) : this.dailyRacingService.addEvents(result).then(() => result);
        }
      );
  }

  /**
   * getByTab()
   * @param {string} tabName
   * @param {boolean} isGrouped
   * @returns {Promise<ISportEvent[]>}
   */
  getByTab(tabName: string, isGrouped: boolean): Promise<ISportEvent[]> {
    this.getConfig().request = this.getRequestConfigByTab(tabName);
    return this.getEvents(tabName, isGrouped);
  }

  /**
   * getById()
   * @param {string} eventId
   * @param {boolean} useCache
   * @returns {Promise<{}>}
   */
  getById(eventId: string, useCache: boolean): Observable<ISportEvent[]> {
    return this.cmsService.getSystemConfig().pipe(
      map((data: ISystemConfig) => {
        return data.RacingDataHub;
      }),
      concatMap((raceInfoConfig: IRacingDataHubConfig) => {
        const res = [from(this.getEvent.call(this, eventId, useCache, raceInfoConfig.isEnabledForHorseRacing))];
        if (raceInfoConfig.isEnabledForHorseRacing) {
          res.push(this.racingPostService.getHorseRacingPostById(eventId));
        }
        return forkJoin(res);
      }),
      map(([eventData, raceData]: [ISportEvent[], IRacingPostHRResponse]) => {
        return this.racingPostService.mergeHorseRaceData(eventData, raceData);
      }),
      catchError((error) => {
        console.error(`Error loading horse data for OB event ${eventId}`, error);
        return throwError(error);
      })
    );
  }

  /**
   * OZONE-5816 jira story
   * OZONE-9566
   * Group markets by Country((UK, IE) comes under UK&IRE, Virtuals as VR, Other countries as INT)
   * @param1 { filterAccess } cms system configuration (enable or disable flags to show in filter)
   * @param2 { nextRacesModule } all combined data
   * @returns grouped filter data
   */
  getNextRacesData(filterAccess, nextRacesModule) {
    if (nextRacesModule && nextRacesModule.storedEvents) {
      const nextRacesGroupedData: any = { ...nextRacesModule };
      const countryFlags = ['UK', 'IE', 'INT', 'VR'];
      const filterData = this.groupByFlagCodesAndClassesTypeNames(nextRacesModule.storedEvents, countryFlags);
      _.extend(nextRacesGroupedData, filterData);
      nextRacesGroupedData.showFilter = false;
      if (nextRacesGroupedData.groupedRacing && !_.isEmpty(filterAccess)) {
          nextRacesGroupedData.groupedRacing.forEach((item: any) => {
          if (item.flag !== 'All') {
            item.flag = item.flag === 'UK' ? 'UK&IRE' : item.flag;
            item.access = filterAccess[item.flag] || false;
            if (item.access) {
              nextRacesGroupedData['showFilter'] = true;
            }
          }
        });
        if (nextRacesGroupedData.showFilter) {
          nextRacesGroupedData.groupedRacing.unshift({ flag: "All", country: 'All', access: true, data: nextRacesGroupedData.storedEvents });
        }
      }
      return nextRacesGroupedData;
    }
  }

  /**
   * isSpecialsAvailable()
   * @returns {boolean}
   */
  isSpecialsAvailable(url: string, isCheckSpecial: boolean = false): Observable<boolean> {
    if (isCheckSpecial && this.config.request.categoryId === this.GREYHOUND_ID) {
      return of(false);
    }

    const tab = 'specials',
      request = {},
      tabs = this.getConfig().tabs[tab] || {};

    _.extend(request, this.readonlyRequestConfig, {
      date: tab,
      limitOutcomesCount: 1,
      limitMarketCount: 1,
      externalKeysEvent: false,
      suspendAtTime: this.timeService.getSuspendAtTime()
    }, tabs);
    const isSpecialsTab = this.routingHelperService.getLastUriSegment(url) === tab;

    return isSpecialsTab ? of(true) : from(this.eventFactory.isSpecialsAvailable(request));
  }

  /**
   * getEvent()
   * @param {number} eventId
   * @param {boolean} useCache
   * @param {boolean} racingPostEnabled
   * @returns {ISportEvent[]}
   */
  getEvent(eventId: number | string, useCache?: boolean, racingPostEnabled = false): Promise<ISportEvent[]> {
    const filters = {
      priceHistory: this.getConfig().request.priceHistory,
      externalKeysEvent: true
    };
    if (!racingPostEnabled) {
      Object.assign(filters, {
        racingFormOutcome: this.getConfig().request.racingFormOutcome,
        racingFormEvent: this.getConfig().request.racingFormEvent,
      });
    }
    return this.eventFactory.getEvent(eventId, filters, false, useCache);
  }

  /**
   * extendConfig()
   * @param {ISportServiceConfig} config
   * returns {ISportServiceConfig}
   */
  extendConfig(config: ISportServiceConfig): ISportServiceConfig {
    const specialsClassIds = this.categoriesData.racing[config.sportModule].specialsClassIds;

    if (specialsClassIds && specialsClassIds.length) {
      _.extend(config.request, { excludeEventsClassIds: specialsClassIds });
      _.extend(config.request.modules.dailyRacing, { classIds: specialsClassIds });
    }

    return Object.assign({}, config);
  }

  /**
   * getYourCallSpecials()
   * @returns {Promise<ISportEvent[]>}
   */
  getYourCallSpecials(): Promise<ISportEvent[]> {
    return this.eventFactory.eventsByTypeIds({
      typeId: this.BYBConfig.HR_YC_EVENT_TYPE_ID,
      suspendAtTime: this.timeService.getSuspendAtTime()
    });
  }

  /**
   * get event and greyhound race by id
   *
   * @param {string} eventId
   * @param useCache
   *
   * @returns {Promise<any[]>}
   */
  getGreyhoundEvent(eventId: string, useCache = false): Observable<any[]> {
    return this.cmsService.getSystemConfig().pipe(
      map((data: ISystemConfig) => {
        return Object.assign({}, data.raceInfo, data.RacingDataHub);
      }),
      concatMap((raceInfoConfig: IRacingDataHubConfig) => {
        const res = [of(raceInfoConfig), from(this.getEvent.call(this, eventId, useCache, raceInfoConfig.isEnabledForGreyhound))];
        if (raceInfoConfig && raceInfoConfig.isEnabledForGreyhound) {
          res.push(this.racingPostService.getGreyhoundRacingPostById(eventId));
        } else if (raceInfoConfig && raceInfoConfig.timeFormEnabled) {
          res.push(this.timeformService.getGreyhoundRaceById(eventId));
        }
        return forkJoin(res);
      }),
      map(([conf, eventData, raceData]: [IRacingDataHubConfig, ISportEvent[], IRacingPostGHResponse | ITimeFormData]) => {
        if (conf && conf.isEnabledForGreyhound) {
          return this.racingPostService.mergeGreyhoundRaceData(eventData, raceData as IRacingPostGHResponse);
        } else {
          const obData = [].concat(eventData)[0];
          const timeFormData = [].concat(raceData)[0];
          return this.timeformService.mergeGreyhoundRaceData([obData, timeFormData as ITimeFormData]);
        }
      }),
      catchError((error) => {
        console.error(`Error loading greyhound data for OB event ${eventId}`, error);
        return throwError(error);
      })
    );
  }

  arrangeEvents(eventsArray, selectedTab, eventsGroupingByTab) {
    let groupingResult;

    if (typeof eventsArray === 'object' && selectedTab) {
      groupingResult = eventsGroupingByTab.call(this, eventsArray);
      return Promise.resolve(_.extend({}, { events: eventsArray }, groupingResult));
    } else {
      return Promise.reject('Error in params');
    }
  }

  addLpAvailableProp(eventsArray) {
    return eventsArray.map(event => {
      event.lpAvailable = this.lpAvailabilityService.check(event);
      return event;
    });
  }

  getAntepostEvents() {
    const config = this.getConfig().request;

    return this.eventFactory.eventsByClasses(config)
      .then(events => ({ events }));
  }

  getAntepostEventsByFlag({ drilldownTagNames }) {
    const request = this.getRequestConfigByTab('future'),
      flag = _.intersection(request.eventDrilldownTagNamesIntersects.split(','), drilldownTagNames.split(','));

    return this.eventFactory.eventsByClasses(request)
      .then(events => events.filter(event => flag && flag[0] && event.drilldownTagNames.indexOf(flag[0].toString()) !== -1))
      .then(events => this.navMenuGroupEventsByCountryCodes(events), error => error);
  }

  /**
   * todayEventsByClasses()
   * @param {boolean} isGrouped
   * @returns {Promise<any>}
   */
  todayEventsByClasses(isGrouped: boolean): Promise<any> {
    const config: ISportServiceRequestConfig = this.getConfig().request;

    return this.eventFactory.eventsByClasses(config)
      .then(data => this.templateService.filterEventsWithoutMarketsAndOutcomes(data))
      .then(data => this.addLpAvailableProp(data))
      .then(data => this.addPersistentInCacheProp(data, config.date))
      // todo: uktote should be checked whether its loaded or not (Lazy loading)
      .then(data => this.addAvailablePoolTypes(data).toPromise())
      .then(data => {
          if (isGrouped) {
            return this.arrangeEvents(data, config.date, this.getEventsGroupingByTabs(config.date))
              .then(result => {
                  result.events = _.reject(result.events, event => (event as any).isStarted === 'true');
                  return Promise.resolve(result);
                }, error => Promise.reject(error)
              );
          } else {
            return Promise.resolve({ events: data });
          }
        }, error => Promise.reject(error)
      );
  }

  prepareEventsObj(data) {
    const eventsByTypeName = this.templateService.groupEventsByTypeName(data);

    return {
      events: data,
      eventsByTypeName,
      typeNamesArray: _.keys(eventsByTypeName)
    };
  }

  results() {
    return Promise.resolve([]);
  }

  getEventsGroupingByTabs(method) {
    const groupingMethod = _.pick({
      featured: this.groupByFlagCodesAndClassesTypeNames,
      today: this.groupByFlagCodesAndClassesTypeNames,
      tomorrow: this.groupByFlagCodesAndClassesTypeNames,
      future: this.getClassesTypeNames,
      antepost: this.getClassesTypeNames,
      specials: this.getClassesTypeNames
    }, method);

    return groupingMethod[method];
  }

  getClassesTypeNames(eventsArray) {
    const list = [];

    _.forEach(eventsArray, ({ typeName, typeDisplayOrder }) => {
      if (!_.find(list, ({ name }) => name === typeName)) {
        list.push({ name: typeName, typeDisplayOrder });
      }
    });

    list.sort((a, b) => {
      if (a.typeDisplayOrder > b.typeDisplayOrder) { return 1; }
      if (a.typeDisplayOrder < b.typeDisplayOrder) { return -1; }

      if (a.name > b.name) { return 1; }
      if (a.name < b.name) { return -1; }

      return 1;
    });

    return {
      classesTypeNames: {
        default: list
      }
    };
  }

  groupByFlagCodesAndClassesTypeNames(eventsArray, countryFlags?: string[]) {
    const config = this.getConfig().request,
      groupedRacing = this.groupByFlagCodes(eventsArray, config.groupByFlagCodesSortOrder, countryFlags);
    let classesTypeNames = this.getClassesTypeNamesByFlagCodes(eventsArray, groupedRacing);

    if (classesTypeNames && groupedRacing) {
      classesTypeNames = this.getLiveStreamGroups(classesTypeNames, (groupedRacing as any));
    }

    return {
      classesTypeNames,
      groupedRacing
    };
  }

  getRacingEventTypeFlagCodeKey(event, countryFlags?: string[]): string | null {
    if (!_.has(event, 'typeFlagCodes')) {
      return null;
    }

    const country = _.intersection(event.typeFlagCodes.split(','), (countryFlags || this.countryFlags));
    if (event.typeFlagCodes.indexOf('IE') !== -1) {
      return 'UK';
    }
    if (country.length) {
      return country[0];
    }

    return 'INT';
  }

  groupByFlagCodes(eventsArray, sortOrderArray: string[], countryFlags?: string []) {
    const groups = {};
    const grouped = [];

    let eventTypeFlagCodeKey;

    eventsArray.forEach(eventEntity => {
      eventTypeFlagCodeKey = this.getRacingEventTypeFlagCodeKey(eventEntity,countryFlags);
      if (!_.has(groups, eventTypeFlagCodeKey)) {
        groups[eventTypeFlagCodeKey] = [];
      }

      if (eventEntity.typeFlagCodes && !eventEntity.typeFlagCodes.toLowerCase().includes('sp')) {
        groups[eventTypeFlagCodeKey].push(eventEntity);
      }
    });

    sortOrderArray.forEach(currentValue => {
      if (groups[currentValue]) {
        grouped.push({ flag: currentValue, data: groups[currentValue] });
      }
    });

    return grouped;
  }

  getClassesTypeNamesByFlagCodes(eventsArray, groupedRacing) {
    const classesTypeNames = {};

    _.forEach(groupedRacing, event => {
      classesTypeNames[(event as any).flag] = [];
      _.forEach((event as any).data, data => {
        if (!_.find(classesTypeNames[(event as any).flag], num => {
          return (num as any).name === (data as any).typeName;
        })) {
          classesTypeNames[(event as any).flag].push({ name: (data as any).typeName });
        }
      });
    });

    return this.getCashoutAvailGroups((classesTypeNames as any), groupedRacing);
  }

  arrangeOutcomesWithResults(eventsArray) {
    _.forEach(eventsArray, (eventEntity: ISportEvent) => {
      _.forEach(eventEntity.markets, marketEntity => {
        marketEntity.correctedEachWayPlaces = this.templateService.genEachWayPlaces(marketEntity);
        if (marketEntity.outcomes.length) {
          const outcomesArray = this.addFavouriteLabelToOutcomesWithResults((marketEntity as any).outcomes)
            .filter(o => o.results.outcomeResultCode !== 'L');

          marketEntity.outcomes = this.filtersService.orderBy(outcomesArray, ['results.outcomePosition']);

          eventEntity.atLeastOneWinnerIsPresent = !!marketEntity.outcomes.length;
        }
      }, this);
    }, this);

    return Promise.resolve(eventsArray.filter(eventEntity => {
      return eventEntity.atLeastOneWinnerIsPresent;
    }));
  }

  groupedPricesArray(outcomesArray) {
    const groupedArray = [],
      arrayOfPrices = outcomesArray.map(returnArrayOfPrices),
      uniqPrices = _.uniq(arrayOfPrices),
      groupByPrices = _.groupBy(arrayOfPrices, _.identity);

    function returnArrayOfPrices(item) {
      return Number(item.results.priceDec);
    }

    _.forEach(uniqPrices, e => {
      groupedArray.push(groupByPrices[(e as any)]);
    });

    return groupedArray;
  }

  updateOucomesArray(flags, outcomes) {
    _.forEach(flags, (item, index) => {
      if (item) {
        outcomes[index].favourite = item;
      }
    });

    return outcomes;
  }

  sortOutcomesByLowestPrice(outcomesArray) {
    return outcomesArray.sort((a, b) => {
      return Number(a.results.priceDec) - Number(b.results.priceDec);
    });
  }

  addFavouriteLabelToOutcomesWithResults(outcomesArray) {
    const outcomes = this.sortOutcomesByLowestPrice(outcomesArray),
      prices = this.groupedPricesArray(outcomes),
      pattern = ((prices[0] && prices[0].length && prices[0].length.toString()) || '')
        .concat((prices[1] && prices[1].length) || '');

    return this.updateOucomesArray(this.racingConfig.FLAGS_MAP[pattern], outcomes);
  }

  sortMarketsName(eventEntity: ISportEvent, sortOrderArray) {
    if (!sortOrderArray) { return eventEntity; }

    _.forEach(eventEntity.markets, market => {
      for (let j = 0; j < sortOrderArray.length; j++) {
        if (market.name === sortOrderArray[j]) {
          market.customOrder = j;
          break;
        }
      }
      market.displayOrder = Number((market as any).displayOrder);
      market.terms = this.templateService.genTerms(market);
    });

    eventEntity.uiClass = this.templateService.genClass(eventEntity);

    return eventEntity;
  }

  getTypeNamesEvents({ selectedTab, filterByDate, additionalEventsFromModules }) {
    const dateFilter = timeStamp => data => {
      if (timeStamp) {
        const { timeStampFrom, timeStampTo } = this.timeService.determineCurrentAndNextDayRange(timeStamp);
        data.events = data.events.filter(event => event.startTime >= timeStampFrom && event.startTime < timeStampTo);
      }
      return data;
    };
    this.getConfig().
      request = this.getRequestConfigByTab(selectedTab);
    return this.getEvents(selectedTab, false)
      .then(this.addEventsFromModules(additionalEventsFromModules))
      .then(dateFilter(filterByDate))
      .then(data => this.navMenuGroupEventsByCountryCodes(data.events), error => error);
  }

  navMenuGroupEventsByCountryCodes(sportEvents: ISportEvent[]): ICombinedSportEvents {
    const groupedByFlagKey = {},
      groupedByFlagAndData = [],
      config = this.getConfig().request,
      groupedEvents = this.templateService.groupEventsByTypeName(sportEvents || []);

    let eventTypeFlagCodeKey, filteredEvent;
    _.each(groupedEvents, (eventEntity, key) => {
      eventTypeFlagCodeKey = this.getRacingEventTypeFlagCodeKey(eventEntity[0]);

      if (eventTypeFlagCodeKey !== null) {

        if (!_.has(groupedByFlagKey, eventTypeFlagCodeKey)) {
          groupedByFlagKey[eventTypeFlagCodeKey] = [];
        }

        filteredEvent = this.filteredEventsByStatusANDTime(eventEntity, true);

        if (!eventEntity[0].typeFlagCodes.toLowerCase().includes('sp')) {
          groupedByFlagKey[eventTypeFlagCodeKey].push({meeting: key, events: filteredEvent});
        }
      }
    });

    config.breadcrumbsNavMenuFlags.forEach(currentValue => {
      if (groupedByFlagKey[currentValue]) {
        groupedByFlagAndData.push({ flag: currentValue, data: groupedByFlagKey[currentValue]});
      }
    });

    return { sportEventsData: sportEvents, groupedByMeetings: groupedEvents, groupedByFlagAndData: groupedByFlagAndData };
  }

  navMenuGroupEnhancedRaces(enhancedEvents: ISportEvent[]): ICombinedSportEvents {
    const groupedEventsByMeetings = [],
      groupedEvents = this.templateService.groupEventsByTypeName(enhancedEvents);

    const filteredEvent = this.filteredEventsByStatusANDTime(enhancedEvents);

    const title = this.localeService.getString('sb.extraPlaceTitle');
    if (filteredEvent && filteredEvent.eventStatusCode === 'A') {
      filteredEvent.isExtraPlaceOffer = true;
      groupedEventsByMeetings.push({meeting: title, events: filteredEvent});
    }

    return { sportEventsData: enhancedEvents, groupedByMeetings: groupedEvents,  groupedByFlagAndData: [{ flag: 'ENHRCS', data: groupedEventsByMeetings }]};
  }

  isRaceOff(event: ISportEvent): boolean {
    return !event.isResulted && !event.isLiveNowEvent && event.isStarted;
  }

  filteredEventsByStatusANDTime(eventEntity: ISportEvent[], noRaceOff: boolean = false): ISportEvent {
    const filterEventByStatus = eventEntity.filter((value: ISportEvent) => {
      return value.eventStatusCode === 'A' && (noRaceOff ? !this.isRaceOff(value) : true);
    });
    const activeEventsByTime = this.filtersService.orderBy(filterEventByStatus, ['startTime']);

    return filterEventByStatus.length ? activeEventsByTime[0] : eventEntity[0];
  }

  addEventsFromModules(additionalEventsFromModules: any): any {
    if (additionalEventsFromModules) {
      const promisesArray = additionalEventsFromModules.filter(e => e !== undefined)
        .map(module => this.commandService.executeAsync(module, undefined, []));

      return data => {
        return Promise.all(promisesArray)
          .then(events => _.flatten(events))
          .then(eventsArray => {
            data.events = data.events ? data.events.concat(eventsArray) : [].concat(eventsArray);
            return data;
          });
      };
    }

    return Promise.resolve([]);
  }

  /**
   * getRequestConfigByTab()
   * @param {string} tabName
   * @returns {ISportServiceRequestConfig}
   */
  getRequestConfigByTab(tabName: string): ISportServiceRequestConfig {
    const request = {},
      tabConfig = this.getConfig().tabs[tabName] || {};

    _.extend(request, this.readonlyRequestConfig, {
      date: tabName,
      suspendAtTime: this.timeService.getSuspendAtTime()
    }, tabConfig);

    return request;
  }

  /**
   * initRaceMarketsObj()
   * @returns {Object}
   */
  initRaceMarketsObj(): Object {
    return {
      mainMarkets: this.racingConfig.MAIN_RACING_MARKETS,
      woMarkets: {
        name: this.localeService.getString('sb.bettingWithout'),
        label: this.localeService.getString('sb.bettingWithout'),
        path: this.racingConfig.WO_MARKET.PATH,
        customOrder: this.racingConfig.WO_MARKET.CUSTOM_ORDER,
        displayOrder: 0,
        subMarkets: this.racingConfig.WO_MARKET.SUB_MARKETS,
        markets: []
      },
      toFinishMarkets: {
        name: this.localeService.getString('sb.toFinishMarkets'),
        label: this.localeService.getString('sb.toFinishMarkets'),
        path: this.racingConfig.TO_FINISH_MARKET.PATH,
        customOrder: this.racingConfig.TO_FINISH_MARKET.CUSTOM_ORDER,
        displayOrder: 0,
        subMarkets: this.racingConfig.TO_FINISH_MARKET.SUB_MARKETS,
        markets: [],
        header: []
      },
      topFinishMarkets: {
        name: this.localeService.getString('sb.topFinishMarkets'),
        label: this.localeService.getString('sb.topFinishMarkets'),
        path: this.racingConfig.TOP_FINISH_MARKET.PATH,
        customOrder: this.racingConfig.TOP_FINISH_MARKET.CUSTOM_ORDER,
        displayOrder: 0,
        subMarkets: this.racingConfig.TOP_FINISH_MARKET.SUB_MARKETS,
        markets: [],
        header: []
      },
      insuranceMarkets: {
        name: this.localeService.getString('sb.insuranceMarkets'),
        label: this.localeService.getString('sb.insuranceMarkets'),
        path: this.racingConfig.INSURANCE_MARKETS.PATH,
        customOrder: this.racingConfig.INSURANCE_MARKETS.CUSTOM_ORDER,
        displayOrder: 0,
        subMarkets: this.racingConfig.INSURANCE_MARKETS.SUB_MARKETS,
        markets: [],
        header: []
      },
      otherMarkets: {
        name: this.localeService.getString('sb.otherMarkets'),
        label: this.localeService.getString('sb.otherMarkets'),
        path: this.racingConfig.OTHER_MARKETS.PATH,
        markets: []
      }
    };
  }

  sortRacingMarketsByTabs(markets: IMarket[], eventId: string) {
    const raceMarkets: any = this.initRaceMarketsObj(),
      marketsArray = [];

    _.forEach(markets, (market: IMarket) => {
      if (market.eventId === eventId) {
        market.label = market.templateMarketName === 'Win or Each Way' ?
          this.localeService.getString('sb.winOrEachWay') : market.name;
        if (raceMarkets.mainMarkets.hasOwnProperty(market.templateMarketName)) {
          market.path = raceMarkets.mainMarkets[market.templateMarketName].path;
          marketsArray.push(market);
        } else if (this.checkTemplateMarketName(raceMarkets.topFinishMarkets, market)) {
          this.setupMarket(market, raceMarkets, 'topFinishMarkets', 'isTopFinish');
          this.setGroupedMarketHeader(raceMarkets.topFinishMarkets, market);
        } else if (this.checkTemplateMarketName(raceMarkets.toFinishMarkets, market)) {
          this.setupMarket(market, raceMarkets, 'toFinishMarkets', 'isToFinish');
          this.setGroupedMarketHeader(raceMarkets.toFinishMarkets, market);
        } else if (this.checkTemplateMarketName(raceMarkets.insuranceMarkets, market)) {
          this.setupMarket(market, raceMarkets, 'insuranceMarkets', 'insuranceMarkets');
          this.setGroupedMarketHeader(raceMarkets.insuranceMarkets, market);
        } else if (this.checkTemplateMarketName(raceMarkets.woMarkets, market)) {
          this.setupMarket(market, raceMarkets, 'woMarkets', 'isWO');
        } else {
          market.path = this.routingHelperService.encodeUrlPart(market.name);
          marketsArray.push(market);
        }
      }
    });

    this.collectSubMarkets(raceMarkets, marketsArray);

    return marketsArray;
  }

  collectSubMarkets(raceMarkets, marketsArray) {
    _.forEach(raceMarkets, marketsType => {
      if (_.has(marketsType, 'markets') && (marketsType as any).markets.length) {
        marketsArray.push(marketsType);
      }
    });
  }

  setupMarket(market, raceMarkets, marketType, isType) {
    market[isType] = true;
    raceMarkets[marketType].displayOrder = market.displayOrder;
    raceMarkets[marketType].markets.push(market);
  }

  checkTemplateMarketName(groupedType, market) {
    return groupedType.subMarkets.join('').indexOf(market.templateMarketName) !== -1;
  }

  /**
   * Sort Racing EDP markets based on cms response
   * @param {IMarket[]} collections
   * @param {IRacingEdpMarket[]} RACING_EDP_MARKETS
   * @param {boolean} isGreyHoundEdp
   * @returns {IMarket[]}
   */
  getSortingFromCms(collections: IMarket[], racingEdpMarkets: IRacingEdpMarket[],
    isGreyHoundEdp: boolean): IMarket[] {
    const racingMarkets = racingEdpMarkets.length ? racingEdpMarkets.filter((market) => {
      return isGreyHoundEdp ? market.isGH : market.isHR;
    }): [];
    if (racingMarkets && racingMarkets.length && collections && collections.length) {
      const arrayLength = (racingMarkets.length > collections.length) ? racingMarkets.length : collections.length;
      this.cmsService.getSystemConfig().subscribe((sysConfig: ISystemConfig) => {
        if (sysConfig?.HorseRacingBIR && sysConfig.HorseRacingBIR.marketsEnabled) {
          this.birMarketsEnabled = sysConfig.HorseRacingBIR.marketsEnabled;
        }
      });
      let indexedCollection = collections.map((collection: IMarket) => {
        const racingEdpMarket = racingMarkets.find((market) => {
          return market.name === (collection.name || collection.label);
        });
        if (!racingEdpMarket) {
          return {
            index: arrayLength,
            ...collection
          };
        }  else {
          return {
            index: racingMarkets.indexOf(racingEdpMarket),
            isGH: racingEdpMarket.isGH,
            isHR: racingEdpMarket.isHR,
            isNew: racingEdpMarket.isNew,
            description: racingEdpMarket.description,
            birDescription: racingEdpMarket.birDescription && this.birMarketsEnabled && this.birMarketsEnabled.includes(racingEdpMarket.name) ? racingEdpMarket.birDescription : null,
            ...collection
          };
        }
      });
      indexedCollection = this.filtersService.orderBy(indexedCollection, ['index']);
      return indexedCollection;
    } else {
      return collections;
    }
  }

  setGroupedMarketHeader(groupedMarkets, market) {
    if (market.isTopFinish) {
      _.forEach(this.racingConfig.TOP_FINISH_MARKET.HEADERS, header => {
        if (market.templateMarketName.indexOf(header) !== -1) {
          groupedMarkets.header.push(header);
        }
      });
    } else if (market.isToFinish || market.insuranceMarkets) {
      const marketType = market.isToFinish ? 'TO_FINISH_MARKET' : 'INSURANCE_MARKETS';
      switch (market.templateMarketName) {
        case this.racingConfig[marketType].SUB_MARKETS[0]:
        case this.racingConfig[marketType].SUB_MARKETS[3]:
        case this.racingConfig[marketType].SUB_MARKETS[6]:
          groupedMarkets.header.push('2nd');
          break;
        case this.racingConfig[marketType].SUB_MARKETS[1]:
        case this.racingConfig[marketType].SUB_MARKETS[4]:
        case this.racingConfig[marketType].SUB_MARKETS[7]:
          groupedMarkets.header.push('3rd');
          break;
        case this.racingConfig[marketType].SUB_MARKETS[2]:
        case this.racingConfig[marketType].SUB_MARKETS[5]:
        case this.racingConfig[marketType].SUB_MARKETS[8]:
          groupedMarkets.header.push('4th');
          break;
        default:
          break;
      }
    }
  }

  addFirstActiveEventProp(racingEvents) {
    // Group all racing events by event name
    const allEvents = _.chain(racingEvents.groupedRacing)
        .pluck('data')
        .flatten()
        .value(),
      groupedEvents = _.groupBy(allEvents, event => event.name);

    _.forEach(groupedEvents, events => {
      // Sort grouped events by event startTime(sort like on racing grid)
      const sortedEvents = _.sortBy(events, event => event.startTime);

      _.forEach(sortedEvents, (event, i) => {
        if (event.isResulted && sortedEvents[i + 1] && sortedEvents[i + 1].isOpenEvent) {
          // It needs for moving first active events to the left on ribbon
          if (sortedEvents[i + 2]) {
            sortedEvents[i + 2].firstActiveEvent = true;
          } else {
            sortedEvents[i + 1].firstActiveEvent = true;
          }
        }
      });
    });
  }

  /**
   * For HR events on FEATURED TAB and with market name 'Featured'
   */
  prepareYourCallSpecialsForFeaturedTab(yourCallSpecials: ISportEvent[]): ISportEvent[] {
    const yourCallSpecialsEvents = this.racingYourcallService.prepareData([], yourCallSpecials);

    return _.where(yourCallSpecialsEvents, {name: this.racingConfig.YC_WIDGET_FILTER});
  }

  configureTabs(name: string, tabs: IInitialSportTab[],
                isSpecialsPresent: boolean,
                isNextRacesEnabled: boolean = false): IInitialSportTab[] {
    return name === 'horseracing' || name === 'greyhound' ? this.filterTabs(tabs, isSpecialsPresent, isNextRacesEnabled) : tabs;
  }

  filterTabs(tabsArray: IInitialSportTab[], isSpecialsPresent, isNextRacesEnabled) {
    tabsArray.forEach(item => {
      if (item.id === 'tab-specials') {
        item.hidden = !isSpecialsPresent;
      } else if (item.id === 'tab-races') {
        item.hidden = !isNextRacesEnabled;
      }
    });
    return tabsArray;
  }

  /**
   * check if it is racing specials edp
   * @return {boolean}
   */
  isRacingSpecials(eventEntity: ISportEvent): boolean {
    const drillDownTagNames = eventEntity.drilldownTagNames;
    const typeFlagCodes = eventEntity.typeFlagCodes;
    if ((drillDownTagNames && drillDownTagNames.indexOf('EVFLAG_SP') !== -1)
      || (typeFlagCodes && typeFlagCodes.indexOf('SP') !== -1)) {
      return true;
    }
    return false;
  }

  /**
   * Sort Countries based on time and Open Bet Ranking
   * @param {IRaceGridMeeting} eventsData
   * @return {IRaceGridMeeting}
   */
  sortRaceGroup(eventsData: IRaceGridMeeting, currentDay: string): IRaceGridMeeting {
    const sortOrder: { flag: string, displayOrder: number }[] = [];
    let sortedCountries = [];
    let activeCountries = [];
    const raceGrid: IRaceGridMeeting = eventsData;
    const isUSWithinRange: boolean = this.isTimeWithinRange(new Date().getTime());

    eventsData.groupedRacing.forEach((racing: IGroupedRacingItem, index: number) => {
      sortOrder.push({ flag: racing.flag, displayOrder: index });
      const obRank = sortOrder.find((country: { flag: string, displayOrder: number }) => country.flag === racing.flag);
      const sortedRaces = [...racing.data].sort((a: ISportEvent, b: ISportEvent) => {
        return (a.startTime > b.startTime) ? 1 : ((b.startTime > a.startTime) ? -1 : 0);
      });
      const activeCountry = this.getActiveCountry(racing, sortedRaces, currentDay, isUSWithinRange);
      const groupedRace = {
        flag: racing.flag,
        data: racing.data,
        displayOrder: obRank.displayOrder
      };
      if (!!activeCountry) {
        activeCountries.push(groupedRace);
      } else {
        sortedCountries.push(groupedRace);
      }
    });
    raceGrid.groupedRacing = [];
    activeCountries = this.sortCountries(activeCountries);
    sortedCountries = this.sortCountries(sortedCountries);
    raceGrid.groupedRacing = [...activeCountries, ...sortedCountries];
    return raceGrid;
  }

  /**
   * Fetches first active event from the group which has been started
   * @param {ISportEvent[]} racingGroup
   * @param {string} racingGroupFlag
   * @returns {ISportEvent}
   */
  getFirstActiveEventFromGroup(racingGroup: ISportEvent[], racingGroupFlag: string): ISportEvent {
    if (this.isActiveGroup(racingGroup, null, racingGroupFlag, true)) {
      return racingGroup[0];
    } else {
      return null;
    }
  }

  addPersistentInCacheProp(eventsArray: ISportEvent[], tabName: string): ISportEvent[] {
    return tabName === 'featured' || tabName === 'today' ? eventsArray.map(event => {
      event.persistentInCache = true;
      return event;
    }) : eventsArray;
  }

  /**
   * Check races and assign filter accordingly
   * @param {ISportEvent[]} racingGroup
   * @param {string} filter
   * @param {ISwitcherConfig[]} switchers
   * @returns {string}
   */
  validateRacesForToday(racingGroup: ISportEvent[], filter: string,
    switchers: ISwitcherConfig[]): string {
   const unFinishedRaces = racingGroup.filter((race: ISportEvent) => {
     return (race.correctedDayValue === filter) && !race.isResulted;
   });

   if (unFinishedRaces.length) {
     return filter;
   } else {
     return switchers.length > 1 ? switchers[1].viewByFilters : filter;
   }
  }

  /*
   * To check if it is tote, forecast or tricast market
   * @returns {boolean}
   */
  isToteForecastTricasMarket(market: string): boolean {
    return (market === this.localeService.getString('sb.tricast')) ||
      (market === this.localeService.getString('sb.forecast')) ||
      (market === this.localeService.getString('uktote.totepool'));
  }

  /**
   * To filter racing group based on today date
   * @param {ISportEvent[]} racing
   * @returns {ISportEvent[]}
   */
  filterRacingGroup(racing: ISportEvent[]): ISportEvent[] {
    if (racing && racing.length) {
      return racing.filter((race: ISportEvent) => {
        const today = new Date();
        const todayTime = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 0, 0, 0, 0).getTime();
        const eventDate = new Date(race.startTime);
        const eventTime = new Date(eventDate.getUTCFullYear(),
        eventDate.getUTCMonth(), eventDate.getUTCDate(),
        eventDate.getUTCHours(), eventDate.getUTCMinutes(), eventDate.getUTCSeconds(),
        eventDate.getUTCMilliseconds()).getTime();
        if (eventTime >= todayTime) {
          return race;
        }
      });
    }
    return racing;
  }

  /**
   * Fetches Active Countries where races are happnening
   * @param {IGroupedRacingItem} racing
   * @param {ISportEvent[]} racingGroup
   * @param {string} currentDay
   * @returns {IGroupedRacingItem}
   */
  private getActiveCountry(racing: IGroupedRacingItem, racingGroup: ISportEvent[],
    currentDay: string, isUSWithinRange?: boolean): IGroupedRacingItem {
    if (this.isActiveGroup(racingGroup, currentDay, racing.flag, isUSWithinRange)) {
      return racing;
    } else {
      return null;
    }
  }

  /**
   * Veifies if the give event is active or not
   * @param {ISportEvent[]} acingGroup
   * @param {string} currentDay
   * @param {string} racingGroupFlag
   * @param {boolean} isUSWithinRange
   * @returns {boolean}
   */
  private isActiveGroup(racingGroup: ISportEvent[], currentDay: string,
    racingGroupFlag?: string, isUSWithinRange?: boolean): boolean {
    let unFinishedRace: ISportEvent;
    if (currentDay) {
      unFinishedRace = racingGroup.find((race: ISportEvent) => {
        return !race.isFinished && race.correctedDay === currentDay;
      });
    } else {
      unFinishedRace = racingGroup.find((race: ISportEvent) => {
        return !race.isFinished;
      });
    }
    const eventStartTime = new Date(racingGroup[0] && racingGroup[0].startTime).getTime();
    const isSuspended = this.isRacingSuspended(racingGroup[0]);
    const isStarted = racingGroup[0] && racingGroup[0].isStarted;
    const isNotVR = racingGroupFlag !== 'VR';
    const currentTime = new Date().getTime();
    const isWithinTimeRange: boolean = racingGroupFlag === 'US' ? isUSWithinRange : true;
    const isActiveEvent = (isStarted ||
      ((eventStartTime <= (currentTime + this.TIME_INTERVAL)) && !isSuspended))
       && isNotVR && isWithinTimeRange;
    return (!!unFinishedRace && isActiveEvent);
  }

  /**
   * Method to check if a race is suspended
   * @param racingGroup - racing data
   * @returns true/false
   */
  isRacingSuspended(racingGroup: ISportEvent): boolean {
    return Object.keys(racingGroup).length && racingGroup.eventStatusCode === 'S' && !racingGroup.isFinished;
  }

  /**
   * To verify if current time within start time and end time
   * @param {number} time
   * @returns {boolean}
   */
  private isTimeWithinRange(time: number): boolean {
    const startTime: number = new Date().setHours(this.racingConfig.US_IGNORE_TIME.START_TIME, 0, 0, 0);
    const endTime: number = new Date().setHours(this.racingConfig.US_IGNORE_TIME.END_TIME, 0, 0, 0);
    return this.validateTimeRange(time, startTime, endTime);
  }

  /**
   * To verify if time is not within range
   * @param {number} currentTime
   * @param {number} startTime
   * @param {number} endTime
   * @returns {boolean}
   */
  private validateTimeRange(currentTime: number, startTime: number, endTime: number): boolean {
    return currentTime < startTime || currentTime > endTime;
  }

  /**
   * Sort Countries and remove display order
   * @param {IGroupedRacingItem[]} sportEvents
   */
  private sortCountries(sportEvents: IGroupedRacingItem[]): IGroupedRacingItem[] {
    const sortedCountries = [...sportEvents].sort((a: IGroupedRacingItem, b: IGroupedRacingItem) => {
      return (a.displayOrder > b.displayOrder) ? 1 : ((b.displayOrder > a.displayOrder) ? -1 : 0);
    });
    return sortedCountries.map((country: IGroupedRacingItem) => {
      delete country.displayOrder;
      return country;
    });
  }

  private addAvailablePoolTypes(events: ISportEvent[]): Observable<ISportEvent[]> {
    return this.cmsService.getSystemConfig(false)
      .pipe(
        mergeMap((config: ISystemConfig) => {
          const UKToteEnabled: boolean = config.TotePools && config.TotePools.Enable_UK_Totepools;
          if (UKToteEnabled) {
            return from(this.ukToteService.addAvailablePoolTypes(events));
          }

          return of(events);
        })
      );
  }

  // eslint-disable-next-line
  private getFeatured(isGrouped: boolean): Promise<Object> {
    return Promise.resolve({});
  }
}
