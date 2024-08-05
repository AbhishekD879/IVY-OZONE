import { map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import * as _ from 'underscore';

import {
  EVENTS_FILTERS,
  OUTRIGHT_CONFIG, OUTRIGHTS_FILTERS,
  PROPS_CONFIG,
  SPECIALS_FILTERS,
  SPORTS_CONFIG
} from '@app/olympics/olympics.constant';
import { OUTRIGHTS_CONFIG } from '@core/constants/outrights-config.constant';
import { ISportServiceRequestConfig } from '@core/models/sport-service-request-config.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { ISportBaseConfig, ISportCMSConfig, ISportCMSConfigTab, ISportEventTab } from '@app/olympics/models/olympics.model';
import { ISSRequestParamsModel } from '@core/models/ss-request-params.model';
import { IFeaturedModel } from '@featured/models/featured.model';
import { ISportEventEntity } from '@core/models/sport-event-entity.model';
import { ISportServiceConfig } from '@core/models/sport-service-config.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { LIVE_STREAM_CONFIG } from '@sb/sb.constant';

import { SimpleFiltersService } from '@ss/services/simple-filters.service';
import { GamingService } from '@core/services/sport/gaming.service';
import { LoadByPortionsService } from '@ss/services/load-by-portions.service';
import { LiveStreamService } from '@sb/services/liveStream/live-stream.service';
import { TemplateService } from '@shared/services/template/template.service';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { TimeService } from '@core/services/time/time.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { BuildUtilityService } from '@core/services/buildUtility/build-utility.service';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { SportsConfigHelperService } from '@sb/services/sportsConfig/sport-config-helper.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { olympicsEventMethods } from '@app/sb/services/sportsConfig/event-methods.constant';
import { ISportConfig } from '@app/core/services/cms/models';

@Injectable({providedIn: 'root'})
export class OlympicsService {
  extensionName: string = 'olympics';

  private readonly outrightConfigTemplate: ISportConfig = OUTRIGHT_CONFIG;
  private readonly sportsConfigTemplate: ISportConfig = SPORTS_CONFIG;
  private confPropsList: string[] = PROPS_CONFIG;
  private specialsFilters: string[] = SPECIALS_FILTERS;
  private outrightsFilters: string[] = OUTRIGHTS_FILTERS;
  private eventsFilters: string[] = EVENTS_FILTERS;

  constructor(
    private timeService: TimeService,
    private templateService: TemplateService,
    private cacheEventsService: CacheEventsService,
    private simpleFiltersService: SimpleFiltersService,
    private coreToolsService: CoreToolsService,
    private siteServerRequestHelperService: SiteServerRequestHelperService,
    private loadByPortionsService: LoadByPortionsService,
    private buildUtilityService: BuildUtilityService,
    private liveStreamService: LiveStreamService,
    private gamingService: GamingService,
    private cmsService: CmsService,
    private sportsConfigHelperService: SportsConfigHelperService,
    private routingHelperService: RoutingHelperService
  ) { }

  /**
   * Get Sport Config
   * @returns {ISportServiceConfig}
   */
  get config(): ISportServiceConfig {
    return this.gamingService.getConfig();
  }
  set config(value:ISportServiceConfig){}

  getCMSConfig(): Observable<ISportCMSConfig[]> {
    return this.cmsService.getSports().pipe(
      map((config: ISportCMSConfig[]|any) => {
        config.forEach((sportConfig: ISportCMSConfig) => {
          if (!sportConfig.sport) {
            sportConfig.categoryId = sportConfig.categoryId.toString();
            sportConfig.sport = sportConfig.targetUriCopy || sportConfig.imageTitle.toLowerCase().replace(/\s+/g, '');
            sportConfig.targetUri = `/olympics/${sportConfig.targetUriCopy}/${this.getDefaultTab(sportConfig.defaultTab)}`;
          }
        });
        return _.reject(config, (sport: ISportCMSConfig) => sport.disabled);
      }));
  }

  /**
   * Generates Common Sport Config
   *
   * @param {ISportCMSConfig} sportCMSConfig
   * @returns {ISportConfig}
   */
  generateCommonSportConfig(sportCMSConfig: ISportCMSConfig): ISportConfig {
    const { sport, targetUri, categoryId, typeIds, imageTitle, tabs }: ISportCMSConfig = sportCMSConfig;
    const isVisible: boolean = this.isVisible(tabs);
    return {
      config: {
        extension: this.extensionName,
        name: this.sportsConfigHelperService.getSportConfigName(sport),
        title: imageTitle,
        path: sport,
        defaultTab: targetUri,
        request: {
          categoryId: categoryId,
          typeIds: typeIds
        }
      },
      tabs: [
        {
          url: `/olympics/${sport}/live`,
          hidden: isVisible ? false : !tabs['tab-live'].visible,
          label: tabs['tab-live'].tablabel || 'In-Play'
        },
        {
          url: `/olympics/${sport}/matches/today`,
          hidden: isVisible ? false : !tabs['tab-matches'].visible,
          label: tabs['tab-matches'].tablabel || 'Matches',
          subTabs: [
            {
              url: `${targetUri}/matches/today`
            }, {
              url: `${targetUri}/matches/tomorrow`
            }, {
              url: `${targetUri}/matches/future`
            }
          ]
        },
        {
          url: `/olympics/${sport}/outrights`,
          hidden: isVisible ? false : !tabs['tab-outrights'].visible,
          label: tabs['tab-outrights'].tablabel || 'Outrights'
        },
        {
          url: `/olympics/${sport}/specials`,
          hidden: isVisible ? false : !tabs['tab-specials'].visible,
          label: tabs['tab-specials'].tablabel || 'Specials'
        }
      ]
    };
  }

  /**
   * generates Outright Sport Config
   *
   * @param {ISportCMSConfig} sportCMSConfig
   * @returns {ISportConfig}
   */
  generateOutrightSportConfig(sportCMSConfig: ISportCMSConfig): ISportConfig {
    const config: ISportConfig = this.coreToolsService.merge(
      this.getConstant(this.sportsConfigTemplate),
      this.getConstant(this.outrightConfigTemplate));
    return Object.assign({}, this.coreToolsService.merge(config, this.generateCommonSportConfig(sportCMSConfig)));
  }

  /**
   * Generates PreMatch Sport Config
   *
   * @param {ISportCMSConfig} sportCMSConfig
   * @returns {ISportConfig}
   */
  generatePreMatchSportConfig(sportCMSConfig: ISportCMSConfig): ISportConfig {
    const { dispSortName, primaryMarkets }: ISportCMSConfig = sportCMSConfig;
    const prematchConfigTemplate: ISportConfig = {
        config: {
          request: {},
          tabs: {
            live: {},
            today: {
              dispSortName,
              dispSortNameIncludeOnly: dispSortName,
              marketTemplateMarketNameIntersects: primaryMarkets,
              marketDrilldownTagNamesNotContains: 'MKTFLAG_SP'
            },
            tomorrow: {
              dispSortName,
              dispSortNameIncludeOnly: dispSortName,
              marketTemplateMarketNameIntersects: primaryMarkets,
              marketDrilldownTagNamesNotContains: 'MKTFLAG_SP'
            },
            future: {
              dispSortName,
              dispSortNameIncludeOnly: dispSortName,
              marketTemplateMarketNameIntersects: primaryMarkets,
              marketDrilldownTagNamesNotContains: 'MKTFLAG_SP'
            },
            outrights: {
              isActive: true
            },
            specials: {
              marketDrilldownTagNamesContains: 'MKTFLAG_SP'
            }
          },
          eventMethods: olympicsEventMethods
        }
      };
    const config: ISportConfig = this.coreToolsService.merge(this.getConstant(this.sportsConfigTemplate), prematchConfigTemplate);
    return Object.assign({}, this.coreToolsService.merge(config, this.generateCommonSportConfig(sportCMSConfig)));
  }


  /**
   * Returns sports config like in CATEGORIES_DATA.gaming
   *
   * @param {ISportCMSConfig[]} sportCMSConfig
   * @returns {ISportConfig | {}}
   */
  getSportsConfigs(sportCMSConfig: ISportCMSConfig[]): ISportBaseConfig | {} {
    const sports: ISportBaseConfig | {} = {};
    sportCMSConfig.forEach((sportConfig: ISportCMSConfig) => {
      const sportName: string = this.sportsConfigHelperService.getSportConfigName(sportConfig.sport);
      sports[sportName] = {
        path: sportConfig.sport,
        id: sportConfig.categoryId
      };
      _.extend(sports[sportName], _.pick(sportConfig, this.confPropsList));
    });
    return sports;
  }


  /**
   * Generates sport config like sport CONSTANT with all needed settings for sport entity
   *
   * @param {string} sportPath
   * @param {ISportCMSConfig[]} CMSConfig
   * @returns {*}
   */
  generateSportConfig(sportPath: string, CMSConfig: ISportCMSConfig[]): ISportConfig {
    let sport: ISportConfig;
    const sportConfig: ISportCMSConfig = _.find(CMSConfig, (config: ISportCMSConfig) => {
      return this.sportsConfigHelperService.getSportConfigName(config.sport) === sportPath;
    });
    if (sportConfig) {
      sport = sportConfig.isOutrightSport
        ? this.generateOutrightSportConfig(sportConfig)
        : this.generatePreMatchSportConfig(sportConfig);
    }

    return sport;
  }

  /**
   * Returns config ready for menu Items
   *
   * @param {ISportCMSConfig[]} cmsConfigs
   * @returns {ISportCMSConfig[]}
   */
  getMenuConfigs(cmsConfigs: ISportCMSConfig[]): ISportCMSConfig[] {
    const sportMenu: ISportCMSConfig[] = JSON.parse(JSON.stringify(cmsConfigs));
    return _.map(sportMenu, (sport: ISportCMSConfig) => {
      _.each(this.confPropsList, prop => {
        delete sport[prop];
      });
      return sport;
    });
  }

  /**
   * Returns generated object for tabs for olympic sports
   *
   * @param {ISportEvent[]} marketsByCollection
   * @param {ISportEvent} event
   * @returns {ISportEventTab[]}
   */
   getCollectionsTabs(marketsByCollection: ISportEvent[], event: ISportEvent): ISportEventTab[] {
    const collectionsNamesArray: string[] = _.pluck((marketsByCollection.filter(m => m.markets)), 'name').sort((a, b) => a < b ? -1 : a > b ? 1 : 0);
    const tabUrl: string = this.routingHelperService.formEdpUrl(event);

    let collectionLink: string;
    return collectionsNamesArray.map((collectionName: string) => {
      collectionLink = collectionName.toLowerCase()
        .replace(/[^A-Za-z0-9 ]/g, '')
        .replace(/\s/g, '-');

      return {
        id: `tab-${collectionLink}`,
        marketName: collectionLink,
        label: collectionName,
        url: `${tabUrl}/${collectionLink}`
      };
    });
  }

  /**
   * Extends current game service to use olympics prototypes
   *
   * @param {ISportConfig} sportConfig
   * @returns {ISportServiceConfig}
   */
  olympicsService(sportConfig: ISportConfig): GamingService {
    const olympics = Object.assign(this.gamingService.setConfig(sportConfig.config), {
      extension: this.extensionName,
      outrights: this.outrightsByTypesIds.bind(this),
      specials: this.specialsByTypesIds.bind(this),
      todayEventsByTypesIds: this.todayEventsByTypesIds.bind(this),
      getCollectionsTabs: this.getCollectionsTabs.bind(this),
      sportConfig: sportConfig
    });

    return olympics;
  }

  /**
   * Extends apiDataCacheInterval and storedData params for cache
   */
  extendCacheParams(): void {
    this.timeService.apiDataCacheInterval[`${this.extensionName}Events`] = 60000; // 1000 * 60 seconds
    this.timeService.apiDataCacheInterval[`${this.extensionName}Coupons`] = 5 * 60000; // 1000 * 60 seconds
    this.cacheEventsService.storedData[`${this.extensionName}Events`] = {};
    this.cacheEventsService.storedData[`${this.extensionName}Coupons`] = {};
  }

  /**
   * Get specials events
   *
   * @returns {Promise<ISportEvent[]>}
   */
  specialsByTypesIds(): Promise<ISportEvent[]> {
    const eventFilters = this.simpleFiltersService.getFilterParams(this.config.request, this.specialsFilters);

    if (this.config.request.typeIds && this.config.request.typeIds.length > 0) {
      const cachedEvents = this.cachedEvents((config: ISportServiceRequestConfig) => {
        return this.loadByPortionsService.get((params: ISSRequestParamsModel) => {
          return this.siteServerRequestHelperService.getOutrightsByTypeIds(params);
        }, eventFilters, 'typeId', config.typeIds as number[])
          .then((data: ISportEventEntity[]) => {
            return this.buildUtilityService.buildEventsWithOutMarketCounts(data);
          })
          .then((data: ISportEvent[]) => {
            return this.liveStreamService.addLiveStreamAvailability(LIVE_STREAM_CONFIG)(data);
          });
      }, `${this.extensionName}Events`)(this.config.request);

      return cachedEvents;
    }

    return Promise.resolve([]);
  }

  /**
   * Loads events by type ids and for events that are outrights events
   *
   * @returns {Promise<ISportEvent[]>}
   */
  outrightsByTypesIds(): Promise<ISportEvent[]> {
    this.config.request.eventSortCode = this.config.request.outrightsSport
      ? OUTRIGHTS_CONFIG.outrightsSportSortCode
      : OUTRIGHTS_CONFIG.sportSortCode;

    const eventFilters = this.simpleFiltersService.getFilterParams(this.config.request, this.outrightsFilters);

    if (this.config.request.typeIds && this.config.request.typeIds.length > 0) {
      const cachedEvents = this.cachedEvents((config: ISportServiceRequestConfig) => {
        return this.loadByPortionsService.get((params: ISSRequestParamsModel) => {
          return this.siteServerRequestHelperService.getOutrightsByTypeIds(params);
          }, eventFilters, 'typeId', config.typeIds as number[])
          .then((data: ISportEventEntity[]) => {
            return this.buildUtilityService.buildEventsWithOutMarketCounts(data);
          })
          .then((data: ISportEvent[]) => {
            return this.liveStreamService.addLiveStreamAvailability(LIVE_STREAM_CONFIG)(data);
          })
          .then((data: ISportEvent[]) => {
            return this.templateService.filterBetInRunMarkets(data);
          })
          .then((data: ISportEvent[]) => {
            return this.templateService.filterMultiplesEvents(data);
          });
      }, `${this.extensionName}Events`)(this.config.request);

      return cachedEvents;
    }

    return Promise.resolve([]);
  }

  /**
   * Loads events by type ids and for events that have primary markets
   *
   * @returns {Promise<ISportEvent[]>}
   */
  todayEventsByTypesIds(): Promise<ISportEvent[]> {
    const eventFilters = this.simpleFiltersService.getFilterParams(this.config.request, this.eventsFilters);

    if (this.config.request.typeIds.length > 0) {
      const cachedEvents = this.cachedEvents((config: ISportServiceRequestConfig) => {
        return this.loadByPortionsService.get((params: ISSRequestParamsModel) => {
          return this.siteServerRequestHelperService.getOutrightsByTypeIds(params);
        }, eventFilters, 'typeId', config.typeIds as number[])
          .then((data: ISportEventEntity[]) => {
            return this.loadCounts(data).then((marketsCountData) => {
              return [data, marketsCountData[0]];
            });
          })
          .then((data: ISportEvent[]) => {
            return this.buildUtilityService.buildEventsWithMarketCounts(data);
          })
          .then((data: ISportEvent[]) => {
            return this.liveStreamService.addLiveStreamAvailability(LIVE_STREAM_CONFIG)(data);
          })
          .then((data: ISportEvent[]) => {
            return this.filterEventsWithPrices(data);
          });
      }, `${this.extensionName}Events`)(this.config.request);

      return cachedEvents;
    }

    return Promise.resolve([]);
  }

  /**
   * Load Counted Events Data
   * @param {ISportEventEntity[]} eventsData
   * @returns {Promise<ISportEvent[]>}
   */
  private loadCounts(eventsData: ISportEventEntity[]): Promise<ISportEvent[]> {
    const countFilters = this.simpleFiltersService.getFilterParams(this.config.request,
      _.without(this.eventsFilters, 'dispSortName', 'marketTemplateMarketNameIntersects', 'templateMarketNameOnlyIntersects'), true);
    const ids = eventsData.map((eventEntity: ISportEventEntity) => eventEntity.event.id);

    return ids.length ? Promise.all([this.loadByPortionsService.get((params: ISSRequestParamsModel) => {
      return this.siteServerRequestHelperService.getMarketsCountByEventsIds(params);
    }, _.extend({}, countFilters), 'eventsIds', ids)]) : Promise.resolve([]);
  }

  /**
   * Adds events to cache - wrapper
   *
   * @param loaderFn
   * @param cacheName
   * @returns {Function}
   */
  private cachedEvents(loaderFn: Function, cacheName: string): Function {
    return (params: ISportServiceRequestConfig) => {
      const stored: IFeaturedModel = this.cacheEventsService.stored(cacheName, params.date, (params.typeIds as number[]).join(''));
      const store: Function = _.partial(this.cacheEventsService.store, cacheName, params.date, (params.typeIds as number[]).join(''));
      return stored
        ? this.cacheEventsService.async(stored)
        : loaderFn(params).then((events: ISportEvent[]) => store(events));
    };
  }

  /**
   * Filters Events With Prices
   *
   * @param events
   * @returns {*}
   */
  private filterEventsWithPrices(events: ISportEvent[]): ISportEvent[]  {
    return events.filter((event: ISportEvent) => {
      return event.markets && event.markets.some((market: IMarket) => {
        return market.outcomes && market.outcomes.some((outcome: IOutcome) => {
          return outcome.prices && outcome.prices.length > 0;
        });
      });
    });
  }

  /**
   * Checking if all tabs hidden
   *
   * @param tabs
   * @returns {boolean}
   */
  private isVisible(tabs: ISportCMSConfigTab[]): boolean {
    return _.every(tabs, (tab: ISportCMSConfigTab) => {
      return !tab.visible;
    });
  }

  /**
   * Get constant
   * @param constant
   */
  private getConstant(constant: {}): {} {
    return JSON.parse(JSON.stringify(constant));
  }

  /**
   * Get default tab from config
   *
   * @param {string} defaultTab
   * @returns {string}
   */
  private getDefaultTab(defaultTab: string): string {
    return defaultTab === 'matches' ? 'matches/today' : defaultTab;
  }
}
