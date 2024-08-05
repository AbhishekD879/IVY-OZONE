import { forkJoin as observableForkJoin, Observable, from, of, forkJoin, throwError } from 'rxjs';

import { map, catchError, mergeMap, share } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import environment from '@environment/oxygenEnvConfig';
import { YourcallProviderService } from '../yourcallProvider/yourcall-provider.service';
import { YOURCALL_DATA_PROVIDER } from '@yourcall/constants/yourcall-data-provider';
import { YOURCALL_OB_FLAGS } from '@yourcall/constants/yourcall-ob-flags';
import { YourCallLeague } from '@yourcall/models/yourcall-league';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { GtmService } from '@core/services/gtm/gtm.service';

import { IBybConfigModel } from '@yourcall/models/byb-config.model';
import { ISystemConfig, IYourCallLeague, IYourCallStaticBlock } from '@core/services/cms/models';
import { IYourcallServiceGtmData } from '@yourcall/models/yourcall-service-gtm-data.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import {
  IYourcallByBLeague,
  IYourcallLeaguesMap,
  ILeagueResponse
} from '@yourcall/models/leagues.model';
import { IYourcallTab } from '@yourcall/models/yourcall-tab.model';
import { IYourcallModifiedSportMarketModel } from '@yourcall/models/yourcall-modified-sport-market.model';
import { IClassModel } from '@core/models/class.model';
import {
  IYourcallBYBLeagueEventsResponse
} from '@yourcall/models/byb-events-response.model';
import { LocaleService } from '@app/core/services/locale/locale.service';

@Injectable({ providedIn: 'root' })
export class YourcallService {
  BYB_CONFIG: IBybConfigModel = environment.BYB_CONFIG;

  staticBlock = {};
  isFiveASideNewIconAvailable: boolean = false;
  isFiveASideAvailable: boolean = false;
  keys = {
    page: 'yourcall-page',
    tab: 'yourcall-tab'
  };

  /**
   * State of accordions
   * is collapsed/expanded or not
   */
  isFirstTimeClicked = [];

  /**
   * is enabled TC Tab
   * @type {boolean}
   * @private
   */
  isEnabledYCTab = false;

  /**
   * is enabled UC Icon
   * @type {boolean}
   * @private
   */
  isEnabledYCIcon = false;

  /**
   * Switch which tell if YC X-sell page should be accessible
   * @member {boolean}
   */
  isEnabledYCPage = false;

  /**
   * Array with available leagues
   * @member {Array}
   */
  leagues = [];

  /**
   * Array with events
   * @member {Array}
   */
  events = [];

  private eventsData: IYourcallBYBLeagueEventsResponse[];

  /**
   * Configuration from CMS for YC leagues (disable/enable)
   * @type {undefined}
   * @private
   */
  private leaguesConfigMap = {};

  /**
   * Map where key is  a typeId and value - index in this.leagues array
   * @member {Object}
   */
  private leaguesIndexMap = {};

  /**
   * Array with oder typeIds
   * @member {Array}
   */
  private leaguesOrdering = [];

  private leaguesData: ILeagueResponse[];

  private leaguesAndCache$: Observable<void> = forkJoin([from(
    this.yourcallProviderService.useOnce(YOURCALL_DATA_PROVIDER.BYB).getLeagues()
  )]).pipe(
    map((leaguesData: ILeagueResponse[]) => {
      this.leaguesData = leaguesData;
    })
  );



  private ycReady$: Observable<IYourcallBYBLeagueEventsResponse[]> =
    forkJoin([from(this.yourcallProviderService.useOnce(YOURCALL_DATA_PROVIDER.BYB).getLeagueEventsWithoutPeriod())])
      .pipe(
        map((eventsData: IYourcallBYBLeagueEventsResponse[]) => {
          this.eventsData = eventsData;
          return eventsData;
        }),
        catchError(error => {
          this.eventsData = [];
          console.warn('BYB:getAvailableEvents', error);
          return throwError(error);
        }),
        share()
      );

  private config$: Observable<void> = this.cmsService.getCmsYourCallLeaguesConfig().pipe(
    map((config: IYourCallLeague[]) => {
      this.leaguesOrdering = _.pluck(config, 'typeId').reverse();
      this.leaguesConfigMap = {};
      _.map(config, leagueConf => {
        this.leaguesConfigMap[leagueConf.typeId] = leagueConf;
      });
    }),
    share(),
    catchError(error => {
      console.warn('DS:getConfig', error);
      return of(error);
    })
  );

  private yourCallSwitchers$: Observable<void> = this.cmsService.getSystemConfig().pipe(
    map((config: ISystemConfig) => {
      this.setConfigs(config);
    }),
    catchError(error => {
      console.warn('DS:getGeneralSwitch error', error);
      return of(error);
    })
  );

  constructor(
    private pubsubService: PubSubService,
    private cmsService: CmsService,
    private yourcallProviderService: YourcallProviderService,
    protected routingHelperService: RoutingHelperService,
    private siteServerService: SiteServerService,
    private gtmService: GtmService,
    private localeService: LocaleService
  ) {}

  $onInit() {
    // listen to system config updates to turn on/off immediately
    this.pubsubService.subscribe('yourCall', this.pubsubService.API.SYSTEM_CONFIG_UPDATED, config => {
      this.setConfigs(config);
    });
  }

  /**
   * get list of related statick blocks
   */
  getStaticBlocks(): Promise<void> {
    return this.cmsService.getYourCallStaticBlock().pipe(
      map((data: IYourCallStaticBlock[]) => {
        _.each(data, (item: IYourCallStaticBlock) => {
          this.staticBlock[item.title] = item;
        });
      }, error => {
        console.warn('DS:getGeneralSwitch', error);
      }))
      .toPromise();
  }

  /**
   * Get specific statick block
   * @param key {string}
   * @returns {string}
   */
  getStaticBlock(key: string): IYourCallStaticBlock {
    return this.staticBlock[key] ? this.staticBlock[key] : null;
  }

  /**
   * Get data for YourCall Tab on EDP
   * @param event
   * @returns {{name: string, url: string, markets: Array}}
   */
  getYCTab(event: ISportEvent): IYourcallTab {
    const tabUrl = this.routingHelperService.formEdpUrl(event);

    return {
      name: this.localeService.getString('yourcall.buildYourBet'),
      marketName: this.localeService.getString('yourcall.pathBuildYourBet'),
      url: `/${tabUrl}/${this.localeService.getString('yourcall.pathBuildYourBet')}`,
      markets: []
    };
  }

  /**
   * Get data for YourCall Tab on EDP
   * @param event
   * @returns {{name: string, url: string, markets: Array}}
   */
  get5ASideTab(event: ISportEvent): IYourcallTab {
    const tabUrl = this.routingHelperService.formEdpUrl(event);

    return {
      name: '5-A-Side',
      marketName: '5-a-side',
      url: `/${tabUrl}/5-a-side`,
      markets: []
    };
  }

  /**
   * Check if 5 A Side league available for OB competition
   * @param competitionId
   * @param ruleToCheck can be isFiveASideAvailable value
   * @return {boolean}
   */
  isFiveASideAvailableForCompetition(competitionId: number, ruleToCheck: boolean): boolean {
    return ruleToCheck && !!this.leagues[this.leaguesIndexMap[competitionId]] &&
      this.leaguesConfigMap[competitionId] && this.leaguesConfigMap[competitionId].activeFor5aSide;
  }

  /**
   * Check if Build Your Bet league available for OB competition
   * @param competitionId
   * @param ruleToCheck can be isEnabledYCIcon or isEnabledYCTab value
   * @return {boolean}
   */
  isAvailableForCompetition(competitionId: number, ruleToCheck: boolean): boolean {
    return ruleToCheck && !!this.leagues[this.leaguesIndexMap[competitionId]] &&
      this.leaguesConfigMap[competitionId] && this.leaguesConfigMap[competitionId].enabled;
  }

  /**
   * Check if #yourCall available for OB competition
   * @param eventId
   * @param ruleToCheck can be isEnabledYCIcon
   * @return {boolean}
   */
  isEventsAvailableForCompetition(eventId: number): boolean {
    const obEventId = [];

    this.events = this.eventsData && this.eventsData[0] && this.eventsData[0].data;
    if (this.events) {
      this.events.forEach(event => {
        obEventId.push(event.obEventId);
      });
    }

    return obEventId.includes(eventId);
  }

  /**
   * Check if if to show #yourCall icon
   * @param competitionId
   * @param events in competition
   * @return {boolean}
   */
  isYCIconAvailable(events: ISportEvent[]): boolean {
    return _.some(events, this.isYCAvailableForEventByOBFlag);
  }

  /**
   * Check if if to show #yourCall icon
   * @param competitionId
   * @param events in competition
   * @return {boolean}
   */
  isBYBIconAvailable(competitionId: number): boolean {
    return this.isAvailableForCompetition(competitionId, this.isEnabledYCIcon);
  }

  isBYBIconAvailableForEvents(eventId: number): boolean {
    return this.isEventsAvailableForCompetition(eventId);
  }

  /**
   * Get observable to be resolved when all yourCall data is available
   */
  whenYCReady(ruleToCheck: string, useCache: boolean = false): Observable<boolean> {
    return this.yourCallSwitchers.pipe(
      mergeMap(() => {
        if (this[ruleToCheck]) {
          return this.getEventsAndCache(useCache).pipe(
            mergeMap(() => this.init(useCache))
          );
        }
        return of(true);
      })
    );
  }

  /**
   * Get class data per typeIds from OB
   * @param ids
   */
  getClassData(ids: number[]): Promise<ISportEvent[] | IClassModel[]> {
    if (!ids || !ids.length) {
      console.warn('DS getClassData error: No league ids specified for request');
      return Promise.resolve([]);
    }
    return this.siteServerService.getClassToSubTypeForTypeByPortions(_.uniq(ids));
  }

  /**
   * Check in CMS config whether show league or hide
   * @param {Object} league
   */
  isDisabled(league: YourCallLeague | ISportEvent): boolean {
    const leagConf = this.leaguesConfigMap[league.obTypeId];
    return !league || (leagConf ? !leagConf.enabled : false);
  }

  /**
   * Goes through array and sets required for 'show all' props
   * @param data
   * @private
   */
  prepareMarkets(data: ISportEvent[]): void {
    _.each(data, (event: ISportEvent) => {
      _.each(event.markets, (market: IYourcallModifiedSportMarketModel) => {
        market.showLimit = 3;
        market.isAllShown = false;
      });
    });
  }

  /**
   * GA logic
   * Send GTM only on first two clicks accordions
   * with different eventLabel properties accordingly to the event
   * (collapse or expand)
   * @params {object} data
   * @params {number} index
   * @params {boolean} isExpanded
   */
  sendToggleGTM(data: IYourcallServiceGtmData, index: number, isExpanded: boolean): void {
    const eventLabels = { expand: 'expand market accordion', collapse: 'collapse market accordion' };
    const accordionsState = this.isFirstTimeClicked[index];

    if (accordionsState.collapsed && accordionsState.expanded) {
      return;
    }

    if (!isExpanded) {
      this.sendGTM(data, eventLabels.collapse);
      this.changeToggleState(index, 'collapsed');
    } else {
      this.sendGTM(data, eventLabels.expand);
      this.changeToggleState(index, 'expanded');
    }
  }

  /**
   * Set initial collapse/expand states
   * @params {number} accordionsAmount
   */
  accordionsStateInit(accordionsAmount: number): void {
    this.isFirstTimeClicked = _.times(accordionsAmount, () => ({ collapsed: false, expanded: false }));
  }

  /**
   * Sort leagues by array of ordered tyeIds from CMS
   * @param {Array} leaguesData
   * @private
   */
  sortLeagues(leaguesData: YourCallLeague[]): YourCallLeague[] {
    return leaguesData.sort((leagueA: YourCallLeague, leagueB: YourCallLeague) => {
      return this.leaguesOrdering.indexOf(leagueB.obTypeId) - this.leaguesOrdering.indexOf(leagueA.obTypeId);
    });
  }

  private get ycReady(): Observable<IYourcallBYBLeagueEventsResponse[]> {
    return this.ycReady$;
  }

  private set ycReady(value: Observable<IYourcallBYBLeagueEventsResponse[]>) {}

  /**
   * Pull DS leagues and CMS configs as initial data
   * @private
   */
  private init(useCache: boolean = false): Observable<boolean> {
    return observableForkJoin(
      this.getConfig(),
      from(this.getAvailableLeagues(useCache))
    ).pipe(
      map(() => {
        this.leagues = this.sortLeagues(this.leagues);
        this.leaguesIndexMap = this.mapLeagues(this.leagues);
        return true;
      }),
      catchError(error => {
        console.warn(error);
        return of(false);
      })
    );
  }

  /**
   * Check if YC is available for SS event by drilldownTagNames
   * @param {Object} event
   * @returns {Array} array with available flags
   */
  private isYCAvailableForEventByOBFlag(event: ISportEvent): boolean {
    const flags = event && _.isString(event.drilldownTagNames) ?
      _.without(event.drilldownTagNames.split(','), '') : [];

    return _.contains(flags, YOURCALL_OB_FLAGS.EVENT);
  }

  private getLeaguesAndCache(useCache: boolean = false): Observable<any> {
    // eslint-disable-next-line
    console.log(this.leaguesData);
    if (useCache && this.leaguesData) {
      return of();
    } else {
      return this.leaguesAndCache$;
    }
  }

  private getEventsAndCache(useCache: boolean = false): Observable<IYourcallBYBLeagueEventsResponse[]> {
    if (useCache && this.eventsData) {
      return of();
    }
    return this.ycReady;
  }

  /**
   * get list of available leagues with #YouCall available from data provider
   */
  private getAvailableLeagues(useCache: boolean = false): Observable<void> {
    return this.getLeaguesAndCache(useCache)
      .pipe(
        map(() => {
          const bybLeagues = this.leaguesData && this.leaguesData[0] && this.leaguesData[0].data;

          if (!bybLeagues) {
            this.leagues = [];
            console.warn('BYB:getAvailableLeagues', 'No leagues available');
            return;
          }
          this.leagues = this.mergeLeagues(bybLeagues);
        }),
        share(),
        catchError(error => {
          this.leagues = [];
          console.warn('BYB:getAvailableLeagues', error);
          return of(error);
        }));
  }

  /**
   * Return array of merged leagues available in DS and BYB
   * @param {Array} bybData
   * @param {Array} dsData
   * @private
   */
  private mergeLeagues(bybData: IYourcallByBLeague[]): YourCallLeague[] {
    const leagues = _.map(bybData,
      league => new YourCallLeague(league.obTypeId, league.title, league.status, { byb: true })
    );
    return leagues;
  }

  /**
   * Create map with league indexes (aka position in 'leagues' array)
   * @param {Array} leagues
   * @return {object}
   * @private
   */
  private mapLeagues(leagues: YourCallLeague[]): IYourcallLeaguesMap {
    const originalMap = {};

    _.each(leagues, (league, ind) => {
      if (!_.isEmpty(league)) {
        originalMap[league.obTypeId] = ind;
      }
    });

    return originalMap;
  }

  /**
   * Get config per league for #YourCall from CMS
   * @return {Promise}
   */
  private getConfig(): Observable<void> {
    return this.config$;
  }

  /**
   * Check if yourCall is enabled across whole application
   */
  private get yourCallSwitchers(): Observable<void> {
    return this.yourCallSwitchers$;
  }
  private set yourCallSwitchers(value:Observable<void>){}

  /**
   * get fields from system configs and save configs
   * @param {Object} config
   */
  private setConfigs(config: ISystemConfig): void {
    this.isEnabledYCTab = !!(config.YourCallIconsAndTabs && config.YourCallIconsAndTabs.enableTab);
    this.isEnabledYCIcon = !!(config.YourCallIconsAndTabs && config.YourCallIconsAndTabs.enableIcon);
    this.isEnabledYCPage = !!(config.YourCallPage && config.YourCallPage.enable);
    this.isFiveASideNewIconAvailable = !!(config.FiveASide && config.FiveASide.newIcon);
    this.isFiveASideAvailable = !!(config.FiveASide && config.FiveASide.enabled);
  }

  /**
   * Send GA on expand/collapse
   */
  private sendGTM(data: IYourcallServiceGtmData, action: string): void {
    if (_.has(data, 'events') || _.has(data, 'isSpecials')) {
      // track 'league' accordions
      this.gtmService.push('trackEvent', {
        eventCategory: 'your call',
        eventAction: 'league',
        eventLabel: action,
        league: data.title
      });
    } else if ((data['type'] === 'playerBets' && data.provider === 'BYB') || _.has(data, 'markets')) {
      // track 'Player Bets' and 'BYB markets' accordions
      this.gtmService.push('trackEvent', {
        eventCategory: 'your call',
        eventAction: 'build bet',
        eventLabel: action
      });
    }

    if (_.has(data, 'dsMarket')) {
      const eventBYB = data.provider === 'BYB' && 'build bet';
      // track 'market' accordions
      this.gtmService.push('trackEvent', {
        eventCategory: 'your call',
        eventAction: eventBYB,
        eventLabel: action
      });
    }
  }

  /**
   * Change accordions collapse/expand state
   * @params {number} index
   * @params {string} state
   */
  private changeToggleState(index: number, state: string): void {
    this.isFirstTimeClicked[index][state] = true;
  }
}
