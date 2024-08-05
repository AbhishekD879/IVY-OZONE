import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { from as observableFrom,  Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import environment from '@environment/oxygenEnvConfig';
import { OUTRIGHTS_CONFIG } from '@core/constants/outrights-config.constant';
import { IOutrightsConfig } from '@shared/models/outrights-config.model';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { EventService } from '@sb/services/event/event.service';
import { TimeService } from '@core/services/time/time.service';
import { TemplateService } from '@shared/services/template/template.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { IClassModel, IClassResultModel } from '@core/models/class.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { NAME_TO_GOALS } from '@sb/services/currentMatches/current-matches.constant';
import { ICompetitionPage } from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitions-page.model';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ISportConfig } from '@app/core/services/cms/models';

@Injectable()
export class CurrentMatchesService {
  classCache: IClassModel[];
  OUTRIGHTS_CONFIG: IOutrightsConfig;

  constructor(
    private cacheEventsService: CacheEventsService,
    private siteServerService: SiteServerService,
    private filterService: FiltersService,
    private eventService: EventService,
    private timeService: TimeService,
    private templateService: TemplateService,
    private routingHelperService: RoutingHelperService,
    private channelService: ChannelService,
    private pubSubService: PubSubService) {
    this.OUTRIGHTS_CONFIG = OUTRIGHTS_CONFIG;
  }

  /**
   * Get type by typeName and events by typeId
   * @param {string} typeName
   * @param {string} className
   * @return {Promise<T>} type, events by type id
   */
  getTypeEventsByClassName(typeName: string, className: string, sportConfig: ISportConfig, eventQuickSwitch?: boolean):
    Promise<ICompetitionPage> {
    return this.getTypesForClasses(className, sportConfig.config.request.categoryId)
      .then((types: IClassModel[]) => {
        const typeObj = _.find(types, (type: IClassModel) => this.checkIfEqual(type.type.name, typeName));

        if (!typeObj) {
          throw { noEventsFound: true };
        }

        return typeObj.type;
      })
      .then((type: IClassModel) => this.getEventsByTypeWithMarketCounts(type.id, sportConfig, eventQuickSwitch).then(events => ({ type, events })))
      .then((data: { type: IClassModel; events: ISportEvent[] }) => this.getOutrights(data.type.id, sportConfig.config.request.categoryId)
      .then(outrights => ({ data, outrights })));
  }

  /**
   * Get all Classes that containe active events
   */
  getAllClasses(categoryId: string = environment.CATEGORIES_DATA.footballId): Promise<IClassModel[]> {
    return this.siteServerService.getClasses(categoryId)
      .then(data => this.filterClasses(data))
      .then(data => this.storeClasses(data));
  }

  /**
   * Get Class typeIds by Class name
   * @param {string} name
   * @return {Promise<IClassModel[]>} typeIds
   */
  getClassIdsByName(name: string, categoryId: string = environment.CATEGORIES_DATA.footballId): Promise<IClassModel[]> {
    return this.siteServerService.getClasses(categoryId)
      .then(data => this.filterClasses(data))
      .then(data => this.storeClasses(data))
      .then(_.partial(this.getTypeIdFromClasses, name).bind(this));
  }

  /**
   * Get outrights events by typeId
   *
   * @param {string} typeId
   * @return { Promise<ISportEvent[]>} outrights events
   */
  getOutrights(typeId: string, categoryId: string = environment.CATEGORIES_DATA.footballId): Promise<ISportEvent[]> {
    return this.eventService.eventsByTypeIds({
      eventSortCode: this.OUTRIGHTS_CONFIG.sportSortCode,
      typeId,
      categoryId,
      siteChannels: 'M',
      suspendAtTime: this.timeService.getSuspendAtTime()
    })
      .then(data => this.templateService.filterBetInRunMarkets(data))
      .then(data => this.templateService.filterMultiplesEvents(data));
  }

  /**
   * Get Class typeIds by Class name
   * @param{string} className
   * @param{string} categoryId
   * @return {Promise<IClassModel[]>} typeIds
   */
  getTypesForClasses(className: string, categoryId: string): Promise<IClassModel[]> {
    return this.getClassIdsByName(className, categoryId)
      .then(data => {
        if (!data) {
          throw { noEventsFound: true };
        }
        return this.siteServerService.getTypesByClasses.call(this.siteServerService, data);
      })
      .then(data => this.filterTypes(data));
  }

  /**
   * Get Class typeIds by Class name
   * @param {number} classId
   * @return {Promise<IClassModel[]>} typeIds
   */
  getClassToSubTypeForClass(classId: string): Observable<IClassModel[]> {
    const ids = [Number(classId)];
    return observableFrom(this.siteServerService.getTypesByClasses(ids)).pipe(map((data: IClassModel[]) => {
      return this.filterTypes(data);
    }));
  }

  /**
   * Return sub-categories(Class ID) for football only
   * @params{array} Class Ids from CMS
   * return {Promise<IClassModel[] | any[]>} Filtered sub-categories
   */
  getFootballClasses(ids: string[]): Promise<IClassModel[] | any[]> {
    return this.getAllClasses()
      .then((result: IClassModel[]) => ({ allClasses: true, result }))
      .then((classes: IClassResultModel) => this.filterInitialClasses(classes, ids));
  }

  /**
   * Return sub-categories(Class ID) for football only
   * @params{array} Class Ids from CMS
   * return {Promise<IClassModel[] | any[]>} Filtered sub-categories
   */
  getOtherClasses(ids: string[], categoryId: string): Promise<IClassModel[] | any[]> {
    return this.getAllClasses(categoryId)
      .then((result: IClassModel[]) => ({ allClasses: true, result }))
      .then((classes: IClassResultModel) => this.filterInitialClasses(classes, ids));
  }

  /**
   * Filter Classes Array
   * Return classes by ids from CMS
   * @params {array} classes
   * @params {array} classes Ids from CMS
   * return {Array<IClassModel[] | any[]>} Filtered classes
   */
  filterInitialClasses(classes: IClassResultModel, CmsClassIds: string[]): Array<IClassModel[] | any[]> {
    const subCategories: IClassModel[] | any[] = [];
    _.each(CmsClassIds, (classId: string) => {
      const filterdId = this.filterService.initialClassIds(classes, classId);

      if (filterdId) {
        // @ts-ignore
        subCategories.push(filterdId);
      }
    });
    // @ts-ignore
    return subCategories;
  }

  /**
   * Get Events by typeId with market counts
   * @params {string} typeId
   * @return {Promise<ISportEvent[]>} eventsArray
   */
  getEventsByTypeWithMarketCounts(typeIds: string, sportConfig: ISportConfig, eventQuickSwitch?: boolean): Promise<ISportEvent[]> {
    // clear current Matches cache before getting new data
    this.cacheEventsService.clearByName('currentMatches');

    const requestParams = {
      noEventSortCodes: this.OUTRIGHTS_CONFIG.sportSortCode,
      typeId: typeIds,
      marketsCount: true,
      childCount: true
    } as any;

    if (sportConfig.config.request.categoryId !== environment.CATEGORIES_DATA.footballId) {
      requestParams.dispSortName = sportConfig.config.request.dispSortName;
      requestParams.dispSortNameIncludeOnly = sportConfig.config.request.dispSortNameIncludeOnly;
      requestParams.marketTemplateMarketNameIntersects = sportConfig.config.request.marketTemplateMarketNameIntersects;
    } else if(eventQuickSwitch) {
      requestParams.competitionTemplateMarketName = true;
    } else {
      requestParams.competitionTemplateMarketNameOnlyIntersects = true;
    }

    return this.eventService.eventsByTypeWithMarketCounts(requestParams)
      .then((events: ISportEvent[]) => this.applyTemplateProperties(events));
  }

  /**
   * applying Template Properties to events
   *
   * @param eventsArray
   * @returns {ISportEvent[]}
   */
  applyTemplateProperties(eventsArray: ISportEvent[]): ISportEvent[] {
    this.templateService.addIconsToEvents(eventsArray);
    _.each(eventsArray, (eventEntity: ISportEvent) => {
      _.each(eventEntity.markets, (market: IMarket) => {
        _.each(market.outcomes, (outcomeEntity: IOutcome) => {
          outcomeEntity.isUS = eventEntity.isUS;
          outcomeEntity.correctedOutcomeMeaningMinorCode = this.templateService.getCorrectedOutcomeMeaningMinorCode(outcomeEntity);
        });
        market.outcomes = _.sortBy(market.outcomes, 'correctedOutcomeMeaningMinorCode');
      });

      eventEntity.eventCorectedDay = this.templateService.getEventCorectedDay(eventEntity.startTime);

      this.parseTemplateMarketNames(eventEntity);
    });
    return eventsArray;
  }

  /**
   * Parse market Name property to set market Next Score property
   * @param eventEntity
   */
  parseTemplateMarketNames(eventEntity: ISportEvent): void {
    _.each(eventEntity.markets, (market: IMarket) => {
      if (market.templateMarketName === 'Next Team to Score') {
        market.nextScore = this.getMatchNextGoalsAmount(market.name);
      }
    });
  }

  /**
   * Parse templateMarketName to get next score for market view.
   * @param marketName - {string}
   * @returns {Number} - returns 1,2,3 number of next goal
   */
  getMatchNextGoalsAmount(marketName: string): number {
    let numberOfGoals: number;
    const goalsMatch = marketName.match(/\d+$/);
    const goalsTextMatch = marketName.match(/^[^\s]+/);

    const goalsCount = goalsMatch && goalsMatch[0];
    const goalsTextFromName = goalsTextMatch && goalsTextMatch[0];

    const parsedCount = parseInt(goalsCount, 10);

    // when goals number at the end of templateMarketName
    if (goalsCount) {
      numberOfGoals = !isNaN(parsedCount) ? parsedCount : 0;
    }

    // when goals number should be compared to text at the beginning of templateMarketName
    if (!goalsCount && goalsTextFromName && NAME_TO_GOALS[goalsTextFromName]) {
      numberOfGoals = NAME_TO_GOALS[goalsTextFromName];
    }

    return numberOfGoals;
  }

  /**
   * Sort types and get Type objects only
   * @param {Array} typesByClasses
   * @return {IClassModel[]} types
   */
  filterTypes(typesByClasses: IClassModel[]): IClassModel[] {
    let types = [];

    _.each(typesByClasses, (classObj: IClassModel) => {
      _.each(classObj.class.children, (type: IClassModel) => {
        type.type.displayOrder = Number(type.type.displayOrder);
        types.push(type);
      });
    });

    // Filter types to remove Enhanced and Specials
    types = _.filter(types, (type: IClassModel) => {
      return type.type.id !== '12301' && type.type.id !== '34829';
    });

    return _.chain(types)
      .sortBy(item => item.type.name)
      .sortBy(item => item.type.displayOrder)
      .value();
  }

  /**
   * Filter Classes Array
   * Remove Sport Name from Class name (currently only Football)
   * Only Football support Favourite Matches at the moment
   * @params {array} Classes
   * @params {string} Sport Name
   * @return {IClassModel[]} Filtered matches
   */
  filterClasses(classes: IClassModel[], sportName = 'Football'): IClassModel[] {
    _.each(classes, (classItem: IClassModel) => {
      classItem.class.originalName = classItem.class.name;
      classItem.class.name = this.filterService.clearSportClassName(classItem.class.name, sportName);
    });
    return _.sortBy(classes, 'class.name');
  }

  /**
   * Store Classes got from SS
   * @param {IClassModel[]} classes to store
   */
  storeClasses(classes: IClassModel[]): IClassModel[] {
    this.classCache = classes;
    return classes;
  }

  /**
   * Get Type ids from Class
   * try to get id from Classes on main Current Matches page
   * if id was not found, it means that user wants to see Types from Classes on A-Z page
   * @params {string} class name where to search
   * @params {array} default array of classes
   * @return {string} TypeId for selected Class
   */
  getTypeIdFromClasses(name: string, classes: IClassModel[]): string {
    let id: string;

    try {
      id = _.find(classes, (classObj: IClassModel) => this.checkIfEqual(classObj.name, name)).id;
    } catch (err) {
      const classItem = _.find(this.classCache, (classObj: IClassModel) => this.checkIfEqual(classObj.class.originalName, name));

      id = classItem ? classItem.class.id : id;
    }

    return id;
  }

  /**
   * Checks if passed string are eqaul after encoding to url part.
   * @param {string} nameA
   * @param {string} nameB
   * @return {boolean}
   */
  checkIfEqual(nameA: string, nameB: string): boolean {
    return this.routingHelperService.encodeUrlPart(nameA) === this.routingHelperService.encodeUrlPart(nameB);
  }

  /**
   * subscribe for updates via liveServe PUSH updates (iFrame)!
   * @param {ISportEvent[]} events
   */
  subscribeForUpdates(events: ISportEvent[]): void {
    const channel = this.channelService.getLSChannelsFromArray(events, true, true);

    this.pubSubService.publish('SUBSCRIBE_LS', {
      channel,
      module: 'current-matches'
    });
  }

  /**
   * UnSubscribe from updates via liveServe PUSH updates (iFrame)!
   */
  unSubscribeForUpdates(): void {
    this.pubSubService.publish('UNSUBSCRIBE_LS', 'current-matches');
  }
}
