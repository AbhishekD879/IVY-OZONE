import { of, Observable, ReplaySubject, forkJoin, throwError } from 'rxjs';
import { map, catchError, concatMap, finalize } from 'rxjs/operators';
import { Injectable } from '@angular/core';

import { GamingService } from '@core/services/sport/gaming.service';
import { OlympicsService } from '@app/sb/services/olympics/olympics.service';
import { ISportCMSConfig } from '@app/olympics/models/olympics.model';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISportConfig, ISportCategory, ISportInstanceStorage } from '@app/core/services/cms/models';
import { footballEventMethods, tier1EventMethods,
  tier2EventMethods, outrightsEventMethods } from '@sb/services/sportsConfig/event-methods.constant';
  import { defaultRequestTabs, footballRequestTabs } from './sport-config-tabs.constant';
import { SportsConfigStorageService } from '@sb/services/sportsConfig/sport-config-storage.service';
import { SportsConfigHelperService } from '@sb/services/sportsConfig/sport-config-helper.service';
import environment from '@environment/oxygenEnvConfig';
import { ISportInstanceMap, ISportInstance } from '@app/core/services/cms/models/sport-instance.model';
import { ISportTeamColors } from '@app/sb/models/sport-configuration.model';

@Injectable({
  providedIn: 'root'
})
export class SportsConfigService {
  private cachedSportNamesBuffer: string[] = [];
  constructor(
    private olympicsService: OlympicsService,
    private gamingService: GamingService,
    private cmsService: CmsService,
    private sportsConfigStorageService: SportsConfigStorageService,
    private sportsConfigHelperService: SportsConfigHelperService
  ) { }


  /**
   * Should get sports data for the team Names
   * @param teamNames { Array<string> }
   * @param sportId { string | number }
   * @returns Observable<ISportTeamColors[] | any>
   */
  getTeamColorsForSports(teamNames: Array<string>, sportId: string | number): Observable<ISportTeamColors[] | any> {
    return this.cmsService.getTeamsColors(teamNames, sportId);
  }

  /**
   * Get sports config instance either from CMS or from Cache
   *
   * @param {string[]} sportName
   * @param {boolean} useCache
   * @return {Observable<ISportInstanceMap>}
   */
  getSport(sportName: string, useCache: boolean = true): Observable<ISportInstance> {
    const sportConfigName: string = this.sportsConfigHelperService.getSportConfigName(sportName);
    return this.getSports([sportName], useCache)
      .pipe(
        map((sportInstanceMap: ISportInstanceMap): ISportInstance => {
          return sportInstanceMap && Object.keys(sportInstanceMap).length && sportInstanceMap[sportConfigName] || null;
        })
      );
  }

  /**
   * Get sports config instances either from CMS or from Cache
   *
   * @param {string[]} sportNames
   * @param {boolean} useCache
   * @return {Observable<ISportInstanceMap>}
   */
  getSports(sportNames: string[], useCache: boolean = true): Observable<ISportInstanceMap> {
    sportNames = this.filterOutRacingSportNames(sportNames);
    const isHR: boolean = sportNames.includes('horseracing') || sportNames.includes('horse racing');

    if (!sportNames.length) { return of(null); }

    const requestSportNames: string[] = [];
    let sportsByRequest$: Observable<ISportInstanceMap> = of({});
    let sportsByCache$: Observable<ISportInstanceMap> = of({});

    sportNames.forEach(sport => {
      const sportConfigName: string = this.sportsConfigHelperService.getSportConfigName(sport);
      const sportInstance$ = useCache && this.sportsConfigStorageService.getSport(sportConfigName);
      const isSportToRequest: boolean = !sportInstance$ && !requestSportNames.includes(sportConfigName)
        && !this.cachedSportNamesBuffer.includes(sportConfigName);

      if (isSportToRequest) {
        // store in buffer sport names, where configs should be requested from CMS
        requestSportNames.push(sportConfigName);
        // initiate store for caching and tracking multiple requests.
        const sportConfigLoader$ = new ReplaySubject<ISportInstance>(1);
        this.sportsConfigStorageService.storeSport(sportConfigName, sportConfigLoader$);
      } else if (!this.cachedSportNamesBuffer.includes(sportConfigName)) {
        // store in buffer sport names which are already requested, or exists in cache.
        this.cachedSportNamesBuffer.push(sportConfigName);
      }
    });

    if (this.cachedSportNamesBuffer.length > 0) {
      const cachedSportsMap$: ISportInstanceStorage = this.sportsConfigStorageService.getSports(this.cachedSportNamesBuffer);
      sportsByCache$ = this.getSportsByCache(Object.values(cachedSportsMap$));
    }

    if (requestSportNames.length > 0) {
      sportsByRequest$ = this.getSportsByRequest(requestSportNames, isHR);
    }

    // get sport instances from cms and cache
    return forkJoin(sportsByRequest$, sportsByCache$)
      .pipe(
        map((sportInstanceMaps: ISportInstanceMap[]): ISportInstanceMap => {
          if (sportInstanceMaps.length === 0
            || (Object.keys(sportInstanceMaps[0]).length === 0
              && Object.keys(sportInstanceMaps[1]).length === 0)) {
            throw new Error('No sport configs received.');
          }
          return { ...sportInstanceMaps[0], ...sportInstanceMaps[1] };
        }),
        catchError((error) => {
          console.warn('Error in getting sport instances. ', error);
          return of({});
        }),
        finalize(() => {
          this.cachedSportNamesBuffer = [];
        }),
      );
  }

  getSportByCategoryId(categoryId: number): Observable<ISportInstance> {
    return this.cmsService.getSportCategoryById(categoryId)
      .pipe(
        concatMap((sportCategory: ISportCategory) => {
          return this.getSport(sportCategory.sportName && sportCategory.sportName.split('/').pop());
        }));
  }

  /**
   * Get sport configs from CMS.
   * Flow:
   *  1. Get sport categories Ids by sport names.
   *  2. Get sport configs by categories Ids.
   *  3. (Legacy) If sport config is missing in CMS, tries to get config from olympic sport configs.
   *  4. When config is received, stores in cache,to avoid multiple requests.
   *
   * @param {string[]} sportNamesBuffer
   * @return {Observable<ISportInstanceMap>}
   */
  private getSportsByRequest(sportNamesBuffer: string[], isHR: boolean = false): Observable<ISportInstanceMap> {
    return this.cmsService.getSportCategoriesByName(sportNamesBuffer)
      .pipe(
        catchError((error) => {
          console.warn(`Can't get ${sportNamesBuffer.join(', ')} categories. `, error);
          return of([]);
        }),
        concatMap((sportCategories: ISportCategory[]) => {
          if (sportCategories.length) {
            if (sportCategories.length < sportNamesBuffer.length) {
              console.warn(`${sportCategories.length} sport categories are received. Expected ${sportNamesBuffer.length}`);
            }
            return sportCategories.length === 1 ? this.cmsService.getSportConfig(sportCategories[0].categoryId)
              : this.cmsService.getSportConfigs(sportCategories.map(sportCategory => sportCategory.categoryId));
          } else {
            return throwError('Sport categories are not received.');
          }
        }),
        catchError((error) => {
          console.warn(`Can't get ${sportNamesBuffer.join(', ')} configs. `, error);
          return of([]);
        }),
        concatMap((sportConfigs: ISportConfig[]) => {
          if (sportConfigs.length < sportNamesBuffer.length) {
            const missingSports: string[] = this.getMissingSportNames(sportConfigs, sportNamesBuffer);
            return this.getOlympicSports(missingSports);
          } else {
            return of(sportConfigs);
          }
        }),
        map((sportConfigs: ISportConfig[]): ISportInstanceMap => {
          const sportsMap: ISportInstanceMap = {};
          sportConfigs.forEach((sportConfig: ISportConfig) => {
            if(!sportConfig.config.name && isHR) {
              sportConfig.config.name = environment.CATEGORIES_DATA.racing.horseracing.name;
            }
            const sportConfigLoader$ = this.sportsConfigStorageService.getSport(sportConfig.config.name);
            const sportInstance: ISportInstance = this.setupSportInstance(sportConfig);
            sportConfigLoader$.next(sportInstance);
            sportConfigLoader$.complete();
            this.sportsConfigStorageService.storeSport(sportConfig.config.name, sportConfigLoader$);
            sportsMap[sportConfig.config.name] = sportInstance;
          });
          return sportsMap;
        }),
        catchError((error) => {
          console.warn(`Failed to request ${sportNamesBuffer.join(', ')} configs. `, error);
          return of({});
        }));
  }

  /**
   * Get sport configs from store or process multiple requests to get configs.
   * It tracks whether ReplaySubject for sport was intitiated on initial request.
   * Any next requests to get sport will wait until ReplaySubject completes from initial request
   * or get stored config if it already completed.
   *
   * @param {ReplaySubject<ISportInstance>[]} cachedSports$
   * @return {Observable<ISportInstanceMap>}
   */
  private getSportsByCache(cachedSports$: ReplaySubject<ISportInstance>[]): Observable<ISportInstanceMap> {
    return forkJoin([...cachedSports$])
      .pipe(
        map((sportInstances: ISportInstance[]): ISportInstanceMap => {
          const sportsMap: ISportInstanceMap = {};
          sportInstances.forEach((sportInstance: ISportInstance) => {
            sportsMap[sportInstance.sportConfig.config.name] = sportInstance;
          });
          return sportsMap;
        }),
        catchError((error) => {
          console.warn(`Failed to get sport instances from cache.`, error);
          return of({});
        }));
  }

  /**
   * In case sport config not received, get legacy olympic sport config.
   *
   * @param {ReplaySubject<ISportInstance>[]} recievedSportConfigs$
   * @param {string[]} sportNamesBuffer
   * @return {Observable<ISportConfig[]>}
   */
  private getOlympicSports(sportNamesBuffer: string[]): Observable<ISportConfig[]> {
    return this.olympicsService.getCMSConfig()
      .pipe(
        map((cmsConfigs: ISportCMSConfig[]): ISportConfig[] => {
          return sportNamesBuffer.map((sportName: string): ISportConfig => {
            try {
              const olympicSportConfig: ISportConfig = this.olympicsService.generateSportConfig(sportName, cmsConfigs);
              const sportInstance = this.olympicsService.olympicsService(olympicSportConfig) as ISportInstance;
              return sportInstance.sportConfig;
            } catch (error) {
              console.warn(`Missing ${sportName} olympic config. `, error);
              return null;
            }
          }).filter(sportConfig => !!sportConfig);
        }),
        catchError((error) => {
          console.warn(`Can't get olympic sports: ${sportNamesBuffer.join(', ')}. `, error);
          return of([]);
        }));
  }

  private filterOutRacingSportNames(sportNames: string[]): string[] {
    return sportNames.filter((sportName: string) => {
      sportName = this.sportsConfigHelperService.getSportConfigName(sportName);
      return sportName 
        && sportName !== environment.CATEGORIES_DATA.racing.greyhound.name;
    });
  }

  private getMissingSportNames(sportConfigs: ISportConfig[], sportNames: string[]): string[] {
    return sportNames.reduce<string[]>(((currentMissingSports: string[], sportName: string): string[] => {
      if (sportConfigs.every(sportConfig => sportConfig.config.name !== sportName)) {
        currentMissingSports.push(sportName);
      }
      return currentMissingSports;
    }), []);
  }

  private setupSportInstance(sportConfig: ISportConfig): ISportInstance {
    this.extendSportConfig(sportConfig);
    const sportInstance: ISportInstance = this.gamingService.createNewInstance();
    sportInstance.sportConfig = sportConfig;
    sportInstance.setConfig(sportConfig.config);
    return sportInstance;
  }

  private extendSportConfig(sportConfig: ISportConfig): void {
    const isFootball = sportConfig.config.request.categoryId === environment.CATEGORIES_DATA.footballId;
    sportConfig.config.tabs = defaultRequestTabs;

    if (sportConfig.config.tier === 1) {
      if (isFootball) {
        sportConfig.config.eventMethods = footballEventMethods;
        sportConfig.config.tabs = footballRequestTabs;
      } else {
        sportConfig.config.eventMethods = tier1EventMethods;
        sportConfig.config.tabs = defaultRequestTabs;
      }
    } else if (sportConfig.config.isOutrightSport && sportConfig.config.name !== environment.CATEGORIES_DATA.golfSport) {
      sportConfig.config.eventMethods = outrightsEventMethods;
    } else {
      sportConfig.config.eventMethods = tier2EventMethods;
    }

    this.addLegacyConfig(sportConfig);
  }

  private addLegacyConfig(sportConfig: ISportConfig): void {
    switch (sportConfig.config.request.categoryId) {
      case '16': {
        sportConfig.isFootball = sportConfig.config.request.categoryId === environment.CATEGORIES_DATA.footballId;
        sportConfig.specialsTypeIds = [2297, 2562];
        sportConfig.config.eventRequest = {
          scorecast: true
        };
        delete sportConfig.config.request.dispSortName;
        delete sportConfig.config.request.dispSortNameIncludeOnly;
        delete sportConfig.config.request.marketTemplateMarketNameIntersects;
        break;
      }
      case '51': {
        sportConfig.config.scoreboardConfig = {
          config: {
            type: 'double',
            label: 'G'
          }
        };
        break;
      }
      case '6': {
        sportConfig.config.scoreboardConfig = {
          config: {
            type: 'betGenius'
          }
        };
        break;
      }
      case '36':
      case '52': {
        sportConfig.config.scoreboardConfig = {
          config: {
            type: 'double',
            label: 'S'
          }
        };
        break;
      }
      case '20': {
        sportConfig.config.scoreboardConfig = {
          config: {
            type: 'single'
          }
        };
        break;
      }
    }
  }
}
