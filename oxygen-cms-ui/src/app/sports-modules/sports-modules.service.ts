import { Injectable } from '@angular/core';
import { SportsModule } from '../client/private/models/homepage.model';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';

import {HttpErrorResponse, HttpResponse } from '@angular/common/http';

import { IInplayConfig } from '../client/private/models/homeInplayConfig.model';
import { ApiClientService } from '../client/private/services/http';
import { GlobalLoaderService } from '../shared/globalLoader/loader.service';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { Order } from '@app/client/private/models/order.model';
import { forkJoin } from 'rxjs/observable/forkJoin';
import { concatMap } from 'rxjs/operators/concatMap';
import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';

import * as _ from 'lodash';
import { IRpgConfigModel } from '@app/client/private/models/rpgConfig.model';
import { IAemBannersConfig } from '@app/client/private/models/sport-modules/aem-banners-config.modul';
import { IPrePlayPopularBets } from '@app/client/private/models/prePlaypopularBets.model';
import { HomeInplayModule, InplaySports } from '../client/private/models/inplaySportModule.model';

@Injectable()
export class SportsModulesService {
  defaultSportId: number = 0;
  defaultPageType: string = 'sport';

  inplayConfig: IInplayConfig = {
    maxEventCount: 10,
    homeInplaySports: []
  };

  popularBetConfig: IPrePlayPopularBets = {
    displayName:'Popular Bets - Upcoming Matches',
    redirectionUrl: 'https://beta-sports.ladbrokes.com/sport/football/popularbets/popular-bets' ,
     mostBackedIn: '48',
     eventStartsIn: '48',
     maxSelections:  5,
     priceRange: '1/10-10/1',
     enableBackedInTimes: false
    };

  /**
   * Default config for recently played games module
   */
  rpgConfig: IRpgConfigModel = {
    title: 'Recently Played Games',
    seeMoreLink: 'https://gaming.coral.co.uk',
    gamesAmount: 3,
    bundleUrl: 'https://apk.coral.co.uk/XBC/bundler-coral-sports-react-bundler/2.1.2',
    loaderUrl: 'https://apk.coral.co.uk/XBC/xbc/1.0.4/loader.js'
  };

  moduleConfig: IAemBannersConfig = {
    maxOffers: 7,
    timePerSlide: 7,
    displayFrom: '2019-10-10T00:00:00.000Z',
    displayTo: '2019-12-12T23:59:59.999Z'
  };


  defaultModulesList: SportsModule[] = [
    new SportsModule(this.defaultSportId, this.defaultPageType, 'AEM_BANNERS', 'AEM banners carousel #1', true, 0,
      null, null, this.moduleConfig),
    new SportsModule(this.defaultSportId, this.defaultPageType, 'QUICK_LINK', 'Quick Links Module', false, 1),
    new SportsModule(this.defaultSportId, this.defaultPageType, 'INPLAY', 'In play module', false, 2, this.inplayConfig),
    new SportsModule(this.defaultSportId, this.defaultPageType, 'AEM_BANNERS', 'AEM banners carousel #2', true, 3,
      null, null, this.moduleConfig),
    new SportsModule(this.defaultSportId, this.defaultPageType, 'HIGHLIGHTS_CAROUSEL', 'Highlights Carousel', false, 4),
    new SportsModule(this.defaultSportId, this.defaultPageType, 'SUPPER_BUTTON', 'Super Button', false, 5),
    new SportsModule(this.defaultSportId, this.defaultPageType, 'AEM_BANNERS', 'AEM banners carousel #3', true, 6,
      null, null, this.moduleConfig),
    new SportsModule(this.defaultSportId, this.defaultPageType, 'FEATURED', 'Featured events', true, 7),
    new SportsModule(this.defaultSportId, this.defaultPageType, 'SURFACE_BET', 'Surface Bet Module', true, 8),
    new SportsModule(this.defaultSportId, this.defaultPageType, 'AEM_BANNERS', 'AEM banners carousel #4', true, 9,
      null, null, this.moduleConfig)
  ];

  rpgModule: SportsModule = new SportsModule(
    this.defaultSportId,
    this.defaultPageType,
    'RECENTLY_PLAYED_GAMES',
    'Recently Played Games',
    false,
    6,
    null,
    this.rpgConfig,
    null
  );
popularbetModule: SportsModule = new SportsModule(
this.defaultSportId, 
this.defaultPageType,
'POPULAR_BETS', 
'Popular Bets Module',
false, 
2,
null,
null,
null,
null,
this.popularBetConfig
);
  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService
  ) {}

  updateModulesOrder(newHomepageOrder: Order) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.homepages().reorder(newHomepageOrder);
    return this.wrappedObservable(getData);
  }

  updateModule(sportsModule: SportsModule): Observable<SportsModule> {
    this.globalLoaderService.showLoader();

    return this.apiClientService.homepages()
      .updateModule(sportsModule)
      .map((updatedSportModule: SportsModule) => {
        this.globalLoaderService.hideLoader();
        return updatedSportModule;
      });
  }

  getSingleModuleData(moduleId: string, sportId: string): Observable<[SportsModule, SportCategory]> {
    this.globalLoaderService.showLoader();
    return forkJoin([
      this.apiClientService.homepages().getModuleById(moduleId)
        .map((data: HttpResponse<SportsModule>) => data.body)
        .map((module: SportsModule) => {
          this.globalLoaderService.hideLoader();
          return module;
        }),
      (() => {
        if (sportId) {
          return this.getSportCategoryData(sportId);
        }

        return Observable.of(null);
      })()
    ]) as Observable<[SportsModule, SportCategory]>;
  }

  /**
   * retrieve the list of sports quick links items based on segment selection
   * @param segment value seelcted via dropdown selection
   * @returns 
   */
  public getInplaySportsBySegment(segment: string, brand: string): Observable<HomeInplayModule[]> {
    return this.apiClientService.homepages().getInplaySportsBySegment(segment, brand);
  }

  public getAllSportNames(): Observable<InplaySports[]> {
    return this.apiClientService.homepages().getAllSportNames();
  }

  public getInplaySportById(id: string): Observable<HomeInplayModule> {
    return this.apiClientService.homepages().getInplaySportById(id);
  }

  public saveNewInplaySport(newInplaySport: HomeInplayModule): Observable<HomeInplayModule> {
    return this.apiClientService.homepages().saveNewInplaySport(newInplaySport);
  }

  public updateNewInplaySport(newInplaySport: HomeInplayModule): Observable<HomeInplayModule> {
    return this.apiClientService.homepages().updateNewInplaySport(newInplaySport);
  }

  public deleteSportById(id: string): Observable<HomeInplayModule> {
    return this.apiClientService.homepages().deleteSportById(id);
  }

  inplaySportsReorder(newSportsOrder: Order) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.homepages().inplaySportsReorder(newSportsOrder);
    return this.wrappedObservable(getData);
  }

  /**
   * Do not remove, Use it to cleanUp sport modules from code.
   * No UI for this functionality. only for internal usage for now.
   * @param sportsModules
   */
  removeModules(sportsModules: SportsModule[]): Observable<SportsModule[]> {
    const requestQueue = [];

    sportsModules.forEach((module: SportsModule) => {
      requestQueue.push((() => {
        return this.apiClientService.homepages().removeModule(module.id);
      })());
    });

    // @ts-ignore
    return forkJoin(requestQueue);
  }

  removeModule(module: SportsModule): Observable<SportsModule> {
    return this.apiClientService.homepages().removeModule(module.id);
  }

  isRpgModulePresent(modulesList: SportsModule[]): SportsModule {
    return _.find(modulesList, (module: SportsModule) => module.moduleType === 'RECENTLY_PLAYED_GAMES');
  }
  isPopularBetsModulePresent(modulesList: SportsModule[]): SportsModule {
    return _.find(modulesList, (module: SportsModule) => module.moduleType === 'POPULAR_BETS');
  }
  /**
   * @param pageType - 'sport' or 'eventhub'
   * @param pageId - sport id or eventhub index
   */
  getModulesData(pageType: string, pageId: number): Observable<SportsModule[]> {
    this.globalLoaderService.showLoader();

    return this.apiClientService.homepages().getAllModulesBySport(pageType, pageId)
      .map((res) => res.body)
      .pipe(concatMap((modulesList: SportsModule[]) => {
        // check and create rpg module for homepage.
        if (pageType === 'sport' && pageId === 0 && !this.isRpgModulePresent(modulesList)) {
          return this.apiClientService.homepages().postNewModule(this.rpgModule)
            .map((rpgModule: SportsModule) => {
              modulesList.push(rpgModule);

              return modulesList;
            });
        }
        return Observable.of(modulesList);
      }))
      .pipe(concatMap((modulesList: SportsModule[]) => {
        this.globalLoaderService.hideLoader();
        if (modulesList.length >= this.defaultModulesList.length) {
          return Observable.of(this.addModulesHref(modulesList));
        } else if (pageType === 'eventhub') {
          return Observable.of(modulesList);
        }

        return this.createDefaultModulesList(pageId, pageType, modulesList)
          .map((defaultModulesList: SportsModule[]) => {
            return this.addModulesHref(defaultModulesList);
          });
      }));
  }

  createHubModule(module: SportsModule, hubIndex: string): Observable<SportsModule> {
    module.pageType = 'eventhub';
    module.pageId = hubIndex;
    module.sportId = null;

    if (module) {
      return this.apiClientService.homepages().postNewModule(module);
    }

    return Observable.throw('No module fount for this type');
  }

  createHubModuleByName(moduleName: string, hubIndex: string): Observable<SportsModule> {
    return this.createHubModule(this.getSportModuleByName(moduleName), hubIndex);
  }

  createHubModuleByType(moduleType: string, hubIndex: string): Observable<SportsModule> {
    return this.createHubModule(this.getSportModuleByType(moduleType), hubIndex);
  }

  getSportModuleByType(moduleType: string): SportsModule {
    return _.find(this.defaultModulesList, {moduleType: moduleType});
  }

  getSportModuleByName(moduleName: string): SportsModule {
    return _.find(this.defaultModulesList, {title: moduleName});
  }

  createDefaultModulesList(sportId: number, pageType: string, modulesList: SportsModule[]): Observable<SportsModule[]> {
    const requestQueue = [];

    this.globalLoaderService.showLoader();
    this.defaultModulesList.forEach((module: SportsModule) => {
      module.sportId = sportId;
      module.pageType = pageType;
      module.pageId = sportId.toString();

      if (module.moduleType === 'RECENTLY_PLAYED_GAMES' && sportId !== 0) {
         return;
      }

      requestQueue.push((() => {
        const existingModule = _.find(modulesList, { moduleType: module.moduleType });
        if (existingModule) {
          // if module exist return this module
          return of(existingModule);
        } else {
          // create module by moduleType
          return this.apiClientService.homepages().postNewModule(module);
        }
      })());
    });

    return forkJoin(requestQueue)
      .map((modulesData: SportsModule[]) => {
        this.globalLoaderService.hideLoader();
        return modulesData;
      });
  }

  /**
   * Wrap request to handle success/error.
   * @param observableDate
   */
  wrappedObservable(observableDate): Observable<any> {
    return observableDate
      .map(res => {
        this.globalLoaderService.hideLoader();
        return res;
      })
      .catch(response => {
        if (response instanceof HttpErrorResponse && response.status !== 400) {
          this.handleRequestError(response.error);
        }

        this.globalLoaderService.hideLoader();
        return Observable.throw(response);
      });
  }

  /**
   * Handle networking error.
   * Notify user.
   */
  handleRequestError(error): void {
    this.globalLoaderService.hideLoader();
  }

  /**
   * Add navigation urls (hrefs for its links) for modules.
   * @param modules
   */
  addModulesHref(modules: SportsModule[]): SportsModule[] {
    const updatedModulesData = [];

    modules.forEach((module: SportsModule) => {
      let moduleHref = '';

      switch (module.moduleType) {
        case('QUICK_LINK'):
          moduleHref = `sports-module/sports-quick-links/${module.id}`;
          break;
        case('FEATURED'):
        case('UNGROUPED_FEATURED'):
          moduleHref = `sports-module/featured-events/${module.id}`;
          break;
        case('INPLAY'):
          moduleHref = `sports-module/inplay/${module.id}`;
          break;
        case('HIGHLIGHTS_CAROUSEL'):
          moduleHref = `sports-module/sports-highlight-carousels/${module.id}`;
          break;
        case('RECENTLY_PLAYED_GAMES'):
          moduleHref = `sports-module/recently-played-games/${module.id}`;
          break;
        case('AEM_BANNERS'):
          moduleHref = `sports-module/aem-banner/${module.id}`;
          break;
        case('RACING_MODULE'):
          moduleHref = `sports-module/racing-module/${module.id}`;
          break;
        case('BETS_BASED_ON_YOUR_TEAM'):
          moduleHref = `sports-module/sport-fanzone/${module.id}`;
          break;
        case('BETS_BASED_ON_OTHER_FANS'):
          moduleHref = `sports-module/sport-fanzone/${module.id}`;
          break;
          case('BYB_WIDGET'):
          moduleHref = `sports-module/featured-events/${module.id}`;
          break;
          case('POPULAR_BETS'):
          moduleHref = `sports-module/pre-play/${module.id}`;
          break;
          case('POPULAR_ACCA'):
          moduleHref = `sports-module/featured-events/${module.id}`;
          break;
          case('VIRTUAL_NEXT_EVENTS'):
          moduleHref = `sports-module/next-event-carousel/${module.id}`;
          break;
          case('LUCKY_DIP'):
          case('BYB_WIDGET'):
          moduleHref = `sports-module/featured-events/${module.id}`;
          case('SUPER_BUTTON'):
          moduleHref = `sports-module/featured-events/${module.id}`;
          break;
      }

      if (module.moduleType === 'SURFACE_BET') {
        moduleHref = `sports-module/surface-bets/${module.id}`;
      }

      updatedModulesData.push({
        ...module,
        href: moduleHref
      });
    });

    return updatedModulesData;
  }

  getSportCategoryData(sportId: string): Observable<SportCategory> {
    this.globalLoaderService.showLoader();
    return this.apiClientService.sportCategory()
      .findOne(sportId)
      .map((data: HttpResponse<SportCategory>) => {
        return data.body;
      })
      .map((sportCategory: SportCategory) => {
        this.globalLoaderService.hideLoader();
        return sportCategory;
      });
  }

  getHubData(hubId: string): Observable<IEventHub> {
    return this.apiClientService.eventHub().getEventHubById(hubId);
  }
}
