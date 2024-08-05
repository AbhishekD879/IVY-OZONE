import { Injectable } from '@angular/core';
import { Params } from '@angular/router';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { Breadcrumb, IBreadcrubmBuildParams } from '@app/client/private/models/breadcrumb.model';
import { Observable } from 'rxjs/Observable';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';
import { forkJoin } from 'rxjs/observable/forkJoin';
import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';
import * as _ from 'lodash';
import { SportsModule } from '@app/client/private/models/homepage.model';

@Injectable()
export class SportsModulesBreadcrumbsService {
  moduleTypesUrls = {
    QUICK_LINK: 'sports-quick-links',
    INPLAY: 'inplay',
    HIGHLIGHTS_CAROUSEL: 'sports-highlight-carousels',
    SUPPER_BUTTON: '',
    SURFACE_BET: 'surface-bets',
    FEATURED: 'featured-events',
    BETS_BASED_ON_YOUR_TEAM: 'sport-fanzone',
    BETS_BASED_ON_OTHER_FANS: 'sport-fanzone',
    VIRTUAL_NEXT_EVENTS: 'next-event-carousel',
    SUPER_BUTTON :'SUPER_BUTTON'
  };

  constructor(
    private sportsModulesService: SportsModulesService
  ) {
  }

  getBreadCrumbsForSportCategory(params: Params, sportConfig: SportCategory, moduleTitle: string, route: string): Breadcrumb[] {
    let breadcrumbsData;
    const sportId = params.id;

    if (!sportId || sportId === 0) {
      breadcrumbsData = [
        {
          label: `Home page`,
          url: `/sports-pages/homepage`
        }, {
          label: `${moduleTitle}`,
          url: route
        }
      ];
    } else {
      breadcrumbsData = [
        {
          label: `Sport Categories`,
          url: '/sports-pages/sport-categories'
        },
        {
          label: `${sportConfig.imageTitle}`,
          url: `/sports-pages/sport-categories/${params.id}`
        }, {
          label: `${moduleTitle}`,
          url: route
        }
      ];
    }

    return breadcrumbsData;
  }

  loadSportData(sportConfigId): Observable<SportCategory> {
    return this.sportsModulesService.getSportCategoryData(sportConfigId);
  }

  getBreadCrumbsForSportsQuickLink(
    sportId,
    sportConfigId,
    currentTitle: string,
    currentUrl,
    currentModuleId?: string
  ): Observable<Breadcrumb[]> {
    if (sportId === 0) {
      return Observable.of([
        {
          label: `Home page`,
          url: `/sports-pages/homepage`
        },
        {
          label: 'Quick LInk Module',
          url: `/sports-pages/homepage/sports-module/sports-quick-links/${currentModuleId}`
        },
        {
          label: currentTitle,
          url: currentUrl
        }
      ]);
    } else {
      return this.loadSportData(sportConfigId)
        .map((sportConfig: SportCategory) => {
          return [
            {
              label: `Sport Categories`,
              url: '/sports-pages/sport-categories'
            },
            {
              label: `${sportConfig.imageTitle}`,
              url: `/sports-pages/sport-categories/${sportConfigId}`
            },
            {
              label: 'Quick LInk Module',
              url: `/sports-pages/sport-categories/${sportConfigId}/sports-module/sports-quick-links/${currentModuleId}`
            },
            {
              label: `${currentTitle}`,
              url: currentUrl
            }];
        });
    }
  }

  getBreadCrumbsForSportsHighlightCarousel(
    sportConfigId,
    currentTitle: string,
    currentUrl,
    currentModuleId?: string
  ): Observable<Breadcrumb[]> {
    if (!sportConfigId) {
      return Observable.of([
        {
          label: `Home page`,
          url: `/sports-pages/homepage`
        },
        {
          label: 'Highlights Carousel Module',
          url: `/sports-pages/homepage/sports-module/sports-highlight-carousels/${currentModuleId}`
        },
        {
          label: currentTitle,
          url: currentUrl
        }
      ]);
    } else {
      return this.loadSportData(sportConfigId)
        .map((sportConfig: SportCategory) => {
          return [
            {
              label: `Sport Categories`,
              url: '/sports-pages/sport-categories'
            },
            {
              label: `${sportConfig.imageTitle}`,
              url: `/sports-pages/sport-categories/${sportConfigId}`
            },
            {
              label: 'Highlights Carousel Module',
              url: `/sports-pages/sport-categories/${sportConfigId}/sports-module/sports-highlight-carousels/${currentModuleId}`
            },
            {
              label: `${currentTitle}`,
              url: currentUrl
            }];
        });
    }
  }

  getSurfaceBetsBreadCrumbs(
    sportConfigId,
    currentTitle: string,
    currentUrl
  ): Observable<Breadcrumb[]> {
    if (!sportConfigId) {
      return Observable.of([
        {
          label: `Home page`,
          url: `/sports-pages/homepage`
        },
        {
          label: 'Surface Bets Module',
          url: `/sports-pages/homepage/sports-module/surface-bets`
        },
        {
          label: currentTitle,
          url: currentUrl
        }
      ]);
    } else {
      return this.loadSportData(sportConfigId)
        .map((sportConfig: SportCategory) => {
          return [
            {
              label: `Sport Categories`,
              url: '/sports-pages/sport-categories'
            },
            {
              label: `${sportConfig.imageTitle}`,
              url: `/sports-pages/sport-categories/${sportConfigId}`
            },
            {
              label: 'Surface Bets Module',
              url: `/sports-pages/sport-categories/${sportConfigId}/sports-module/surface-bets`
            },
            {
              label: `${currentTitle}`,
              url: currentUrl
            }];
        });
    }
  }

  getBreadcrubs(routeParams: Params, data: IBreadcrubmBuildParams): Observable<Breadcrumb[]> {
    const url: string = location.pathname;
    const isHomePage = url.indexOf('/sports-pages/homepage') >= 0;
    const isSportPage = url.indexOf('/sports-pages/sport-categories') >= 0;
    const sportId = (isSportPage && routeParams.id) || 0;
    const hubId = routeParams.hubId;
    const moduleId = routeParams.moduleId;
    let breadcrumbs: Breadcrumb[] = [];

    const baseBreadcrumbs: { [key: string]: Breadcrumb } = {
      eventHubLink: {
        label: 'Event Hubs List',
        url: '/sports-pages/event-hub'
      },
      homePageLink:  {
        label: 'Home page',
        url: '/sports-pages/homepage'
      },
      sportCategoryLink: {
        label: 'Sport Categories',
        url: '/sports-pages/sport-categories'
      }
    };

    const observables = [];

    let baseUrl = '';

    // hub is is in url
    if (hubId) {
      breadcrumbs.push(baseBreadcrumbs.eventHubLink);
      baseUrl = `${baseBreadcrumbs.eventHubLink.url}/${hubId}`;

      // we on hub page with hub data
      if (data.eventhub) {
        breadcrumbs.push(this.getHubBreadcrumbByHub(data.eventhub));
      } else {
        // hub id is in url but we are on deeper page
        observables.push(this.getHubBreadcrumbById(hubId)
          .map((breadcrumb) => {
            baseUrl = breadcrumb.url;
            return breadcrumb;
          }));
      }
    }

    // sports module id is in URl
    if (moduleId) {
      // homepage in url
      if (isHomePage) {
        baseUrl = baseBreadcrumbs.homePageLink.url;
        breadcrumbs.push(baseBreadcrumbs.homePageLink);
        // sport category is in url
      } else if (isSportPage) {
        baseUrl = `${baseBreadcrumbs.sportCategoryLink.url}/${sportId}`;
        breadcrumbs.push(baseBreadcrumbs.sportCategoryLink);

        // sport config page with config data
        if (data.sportConfig) {
          observables.push(new Observable((observer) => {
            const breadcrumb = this.getSportCategoryBreadcrumbByObject(data.sportConfig);

            observer.next(breadcrumb);
            observer.complete();
          }));
        } else {
          // sport config is in url but we on deeper page
          observables.push(this.getSportCategoryBreadcrumbById(sportId)
            .map((breadcrumb: Breadcrumb) => {
              return breadcrumb;
            }));
        }
      }

      // we on module page with module data
      if (data.module) {
        observables.push(new Observable((observer) => {
          const breadcrumb = this.getModuleBreadcrumbByModule(baseUrl, data.module);

          observer.next(breadcrumb);
          observer.complete();
        }));
      } else {
        // module id is in url, but we on deeper page
        observables.push(this.getModuleBreadcrumbById(baseUrl, moduleId, sportId)
          .map((breadcrumb: Breadcrumb) => {
            return breadcrumb;
          }));
      }
    }

    if (data.customBreadcrumbs) {
      _.each(data.customBreadcrumbs, (customBreadcrumb) => {
        observables.push(new Observable((observer) => {
          const breadcrumb = this.setCustomBreadcrumb(customBreadcrumb);

          observer.next(breadcrumb);
          observer.complete();
        }));
      });
    }

    if (observables.length > 0) {
      return forkJoin(observables)
        .map((gatheredBreadcrumbs: Breadcrumb[]) => {
          breadcrumbs = breadcrumbs.concat(gatheredBreadcrumbs);

          return breadcrumbs;
        });
    }

    return Observable.of(breadcrumbs);
  }

  /**
   * Load Event Hub Data and get breadcrumb for it
   * @param hubId
   */
  getHubBreadcrumbById(hubId: string): Observable<Breadcrumb> {
    return this.sportsModulesService.getHubData(hubId)
      .map((hubData) => {
        return this.getHubBreadcrumbByHub(hubData);
      });
  }

  /**
   * Get breadcrumb for Event Hub
   * @param hubData
   */
  getHubBreadcrumbByHub(hubData: IEventHub): Breadcrumb {
    return {
      label: hubData.title,
      url: `/sports-pages/event-hub/${hubData.id}`
    };
  }

  /**
   * Load Sports Module Data and get breadcrumb
   * @param baseUrl
   * @param moduleId
   * @param sportId
   */
  getModuleBreadcrumbById(baseUrl: string, moduleId: string, sportId: string): Observable<Breadcrumb> {
    return this.sportsModulesService.getSingleModuleData(moduleId, sportId)
      .map((data: [SportsModule, SportCategory]) => {
        const moduleData = data[0];
        return this.getModuleBreadcrumbByModule(baseUrl, moduleData);
      });
  }

  /**
   * Get breadcrumb for Sports Module
   * @param baseUrl
   * @param moduleData
   */
  getModuleBreadcrumbByModule(baseUrl: string, moduleData: SportsModule): Breadcrumb {
    return {
      label: moduleData.title,
      url: `${baseUrl}/sports-module/${this.moduleTypesUrls[moduleData.moduleType]}/${moduleData.id}`
    };
  }

  getSportCategoryBreadcrumbById(sportConfigId: string): Observable<Breadcrumb> {
     return this.loadSportData(sportConfigId)
       .map((sportCategory: SportCategory) => {
         return this.getSportCategoryBreadcrumbByObject(sportCategory);
       });
  }

  getSportCategoryBreadcrumbByObject(sportConfig: SportCategory): Breadcrumb {
    return {
      label: `${sportConfig.imageTitle}`,
      url: `/sports-pages/sport-categories/${sportConfig.id}`
    };
  }

  setCustomBreadcrumb(itemData: Breadcrumb): Breadcrumb {
    return {
      label: itemData.label,
      url: itemData.url || location.pathname
    };
  }
}
