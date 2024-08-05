import { IBreadcrumb, IBreadcrumbConfig } from '@ladbrokesDesktop/shared/components/breadcrumbs/breadcrumbs.model';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { LocaleService } from '@coreModule/services/locale/locale.service';
import { Location } from '@angular/common';
import { ITab } from '@shared/components/tabsPanel/tabs-panel.model';

@Injectable()
export class BreadcrumbsService {
  private config: IBreadcrumbConfig;
  private breadcrumbsTitles: { [key: string]: any; } = {};
  // this items should be last in chain of breadcrumbs
  private urlItemsRestrictors: string[] = [
    'golf_matches', 'matches', 'lotto', 'virtual-sports', 'playerbets', 'build-your-own-race-card', 'results', 'promotions'
  ];


  // this items should be last in chain of breadcrumbs
  private greyhoungUrlItemsRestrictors: string[] = [
    'matches', 'lotto', 'virtual-sports', 'playerbets', 'build-your-own-race-card', 'results', 'promotions',
    'today', 'tomorrow', 'future'
  ];

  private urlItemsToRemove: string[] = ['event', 'sport', 'sports']; // remove this items from breadcrumbs if present in URL

  constructor(private locale: LocaleService,
              private location: Location) {
  }

  /**
   * Build and get list of breadcrumbs items
   * @param {string} sportName - name of current page
   * @param {string} event - name of current page
   * @param {Array} tabs - subtabs of the page
   * @param {string} competitionName - name of competition
   * @param {string} defaultTab - default tab name(optional)
   * @return {Promise}
   */
  getBreadcrumbsList(config: IBreadcrumbConfig, defaultTab?: string): IBreadcrumb[] {
    this.config = config;
    if(this.config.sportName === 'horseracing' && !this.config.display) {
      this.config.display = 'featured';
    }

    const pathArray: string[] = this.getPathArray();

    if(!this.config.display && defaultTab && defaultTab!=='live') {
      pathArray.push(defaultTab);
    }

    this.getPathTitles(pathArray, this.config.eventName, this.config.sportName);
    return this.initializeBreadcrumbsList(pathArray, defaultTab);
  }


  /**
   * Initialize list of breadcrumbs items
   * @param {Array} pathArray - array of parsed URL
   * @param {String} title - title of sport name or event title
   * @param {String} event - name of current page
   * @return {Promise}
   */
  private initializeBreadcrumbsList(pathArray: string[], defaultTab?: string): IBreadcrumb[] {
    const breadcrumbsList: IBreadcrumb[] = this.resetDefaultBreadcrumbsList();
    const isFootballPage: boolean = this.config.sportName === 'football';
    const isCompetitionPage: boolean = this.config.isCompetitionPage;
    _.each(pathArray, (item: string, index: number) => {
      const slicedArray: string[]  = pathArray.slice(0, index + 1);
      let breadcrumbElement: IBreadcrumb;
      if (index === 0 && isFootballPage && !isCompetitionPage) {
        breadcrumbElement = {
          targetUri: defaultTab ? `/sport/football/${defaultTab}` : `/sport/football`,
          name: this.breadcrumbsTitles[item]
        };
      } else if (index === 0 && this.config.isHorseRacingPage) {
        breadcrumbElement = {
          targetUri: `/horse-racing/featured`,
          name: this.breadcrumbsTitles[item]
        };
      } else if (index === 0 && this.config.isGreyhoundPage) {
        breadcrumbElement = {
          targetUri: `/greyhound-racing/next-races`,
          name: this.breadcrumbsTitles[item]
        };
      } else if (index === 0 && item === 'virtual-sports') {
        breadcrumbElement = {
          targetUri: `/virtual-sports`,
          name: this.breadcrumbsTitles[item]
        };
      } else if (index === 0 && defaultTab) {
        const preffix: string = this.isPrefixPresent() ? '/sport' : '';
        breadcrumbElement = {
          targetUri: `${preffix}/${slicedArray.join('/')}/${defaultTab}`,
          name: this.breadcrumbsTitles[item]
        };
      } else {
        const preffix: string = this.isPrefixPresent() ? '/sport' : '';
        breadcrumbElement = {
          targetUri: `${preffix}/${slicedArray.join('/')}`,
          name: this.breadcrumbsTitles[item]
        };
      }
      breadcrumbElement.name = breadcrumbElement && breadcrumbElement.name && breadcrumbElement.name.split('?')[0];
      breadcrumbsList.push(breadcrumbElement);
    });
    return breadcrumbsList;
  }

  private isPrefixPresent(): boolean {
    return !(this.config.isOlympicsPage
      || this.config.isGreyhoundPage
      || this.config.isHorseRacingPage
      || this.config.isVirtual);
  }
  /**
   * Resolve all promises and get valid titles
   * @param {String} pathArray - array of parsed URL
   * @param {String} sportName - name of current page
   * @param {String} event - name of current page
   * @return {Promise}
   */
  private getPathTitles(pathArray, event: string, sportName: string): string[] {
    return _.reduce(pathArray, (memo: string[], item: string) => {
      memo.push(this.getItemTitle(item, sportName, event));
      return memo;
    }, []);
  }

  /**
   * Get the path for each breadcrumb element
   * @param {Array} tabs - subtabs of the page
   * @param {string} sportName - name of current page
   * @param {string} competitionName - name of competition
   * @return {Array}
   */
  private getPathArray(defaultTab?: string): string[] {
    let pathArray: string[] = this.location.path().split('/').slice(1);
    let urlItemsRestrictors = this.urlItemsRestrictors;

    if (this.config.isGreyhoundPage) {
      urlItemsRestrictors = this.greyhoungUrlItemsRestrictors;
    }
    // Competitions page
    if (this.config.isCompetitionPage) {
      pathArray = this.buildCompetitionBreadcrumb();
    }
    // Horse racing page
    if (this.config.isHorseRacingPage && !this.config.isEDPPage && !this.config.isBuildYourRaceCardPage) {
      pathArray = this.buildHorseRacingBreadcrumb();
    }
    // EDP page
    if (this.config.isEDPPage) {
      pathArray = this.buildEDPBreadcrumb(pathArray);
    }
    // Virtual sports
    if (this.config.isVirtual) {
      urlItemsRestrictors = urlItemsRestrictors.filter(item => item !== 'virtual-sports');
      pathArray = this.buildVirtualBreadcrumb();
    }

    // Check if items from urlItemsRestrictors are present in chain. If yes, remove it.
    pathArray = this.sliceArrayToFoundElement(pathArray, urlItemsRestrictors);
    // Remove all items from urlItemsToRemove array
    pathArray = _.difference(pathArray, this.urlItemsToRemove);
    // Adding the defaultTab name when uri is empty
    if (!this.config.display && defaultTab) {
      pathArray.push(defaultTab);
    }
    // Set valid title
    pathArray = this.getValidTabsTitle(pathArray, this.config.tabs);

    return pathArray;
  }

  /**
   * Build breadcrumbs for HR page
   * @returns {string[]}
   */
  private buildHorseRacingBreadcrumb(): string[] {
    return [this.config.sportName, this.config.display];
  }

  /**
   * Build breadcrumbs for virtual page
   * @returns {string[]}
   */
  private buildVirtualBreadcrumb(): string[] {
    return [this.config.sportName, this.config.eventName];
  }

  /**
   * Build breadcrumbs for competitions page
   * @returns {string[]}
   */
  private buildCompetitionBreadcrumb(): string[] {
    const path = [this.config.sportName, 'competitions'];
    if (this.config.competitionName) {
      path.push(this.config.competitionName);
    }
    return path;
  }

  /**
   * Build breadcrumbs for EDP page
   * @returns {(string & boolean)[]}
   */
  private buildEDPBreadcrumb(pathArray: string[]): string [] {
    const sportName = this.config.isGreyhoundPage ? pathArray[0] : this.config.sportName;
    const isOlympic = this.config.isOlympicsPage;
    const eventName = this.config.eventName;
    const olympicName = isOlympic ? 'olympics' : false;
    return _.compact([olympicName, sportName, 'event', eventName]) as string[];
  }

  /**
   * Initialization and resetting of breadcrumbs' array
   * @return {Array}
   */
  private resetDefaultBreadcrumbsList(): IBreadcrumb[] {
    return [{name: 'Home', targetUri: '/'}];
  }

  /**
   * Convert 'matches' title to valid title that is set on sport subtabs
   * @param {Array} pathArray
   * @param {Array} tabs
   * @return {Array}
   */
  private getValidTabsTitle(pathArray: string[], tabs: ITab[]): string[] {
    _.each(tabs, (tab: ITab) => {
      const tabIndex = pathArray.indexOf(tab.name);
      if (tabIndex > -1) {
        pathArray[tabIndex] = this.locale.getString(tab.label);
      }
    });
    return pathArray;
  }

  /**
   * Get localized breadcrumb item's title
   * @param {String} module's name
   * @param {String} breadcrumbItemName - name of breadcrumb item (got from URL)
   * @return {string}
   */
  private getLocalizedString(module: string, breadcrumbItemName: string): string {
    if (module !== 'default') {
      const itemTranslation = this.locale.getString(`${module}.${breadcrumbItemName}`);
      this.breadcrumbsTitles[breadcrumbItemName] = itemTranslation === 'KEY_NOT_FOUND'
        ? breadcrumbItemName.replace(/-/g, ' ').replace(/\r\n|\n|\r/g, '') : itemTranslation;
    } else {
      this.breadcrumbsTitles[breadcrumbItemName] = breadcrumbItemName && breadcrumbItemName.replace(/-/g, ' ').replace(/\r\n|\n|\r/g, '');
    }

    return this.breadcrumbsTitles[breadcrumbItemName];
  }

  /**
   * Get breadcrumb item's title
   * @param {String} breadcrumbsItem's name (got from URL)
   * @param {String} sportName - name of current page
   * @param {String} event - name of current page
   * @return {string}
   */
  private getItemTitle(breadcrumbsItem: string, sportName: string = '', event: string): string {
    const isOlympicsPage = this.config.isOlympicsPage;
    const isVirtual = this.config.isVirtual;
    const isCompetitionPage = this.config.isCompetitionPage;
    const isCompetitionTypeItem = isCompetitionPage && breadcrumbsItem === sportName.replace(/\s/g, '');

    if (isCompetitionTypeItem) {
      this.breadcrumbsTitles[breadcrumbsItem] = sportName;
    }

    switch (breadcrumbsItem) {
      case sportName:
        if (isOlympicsPage) {
          return this.getLocalizedString('ol', breadcrumbsItem);
        }
        if (isVirtual) {
          return this.getLocalizedString('vsbr', breadcrumbsItem);
        }
        if (event === breadcrumbsItem) {
          return this.getLocalizedString('sb', breadcrumbsItem);
        }
        return this.getLocalizedString('sb', breadcrumbsItem);
      case 'virtual-sports':
        return this.getLocalizedString('vsbr', breadcrumbsItem);
      case 'build-your-own-race-card':
        return this.getLocalizedString('sbdesktop', breadcrumbsItem);
      case 'playerbets':
        return this.getLocalizedString('playerprops', breadcrumbsItem);
      default:
        if ((event === breadcrumbsItem) && isOlympicsPage) {
          return this.getLocalizedString('ol', breadcrumbsItem);
        } else if ((event === breadcrumbsItem) && isVirtual) {
          return this.getLocalizedString('vsbr', breadcrumbsItem);
        } else if ((event === breadcrumbsItem) && !isOlympicsPage) {
          return this.breadcrumbsTitles[breadcrumbsItem] = breadcrumbsItem;
        }
        if (!isNaN(+breadcrumbsItem)) {
          return this.getLocalizedString('default', sportName);
        }
        return this.getLocalizedString('default', breadcrumbsItem);
    }
  }

  /**
   * If any of items from urlItemsRestrictors array are found, pathArray will be sliced from 0 to the found element
   * @param {string[]} pathArray - parsed url array
   * @param {string[]} urlItemsRestrictors - restricted url params array
   * @return {string[]} modified array
   */
  private sliceArrayToFoundElement(pathArray: string[], urlItemsRestrictors: string[]): string[] {
    const intersectedElement = _.intersection(urlItemsRestrictors, pathArray).toString();

    if (intersectedElement !== '') {
      return pathArray.filter((item, index, array) => {
        return array.indexOf(intersectedElement) >= index;
      });
    }

    return pathArray;
  }
}
