import {Injectable} from '@angular/core';
import {Breadcrumb} from '../../../client/private/models/breadcrumb.model';
import * as _ from 'lodash';
import {StatsCenterGroups, StatsCenterSeason} from '../../../client/private/models';
import {ParsedCompetitionGroups} from '../../../client/private/models/parsedCompetitionGroups.model';

@Injectable()
export class BigCompetitionService {
  private breadcrumbs: Breadcrumb[] = [];
  private surfaceBets: any;
  private tabType: any;
  private highlightsCarousel: any;
  constructor() {}

  /**
   * Parse competition data to show breadcrumb correctly
   * @param data - competition tree(competition/tab/sub tab/module)
   * @param {string} state
   * @returns {Breadcrumb[]}
   */
  public breadcrumbParser(data: any, state: string): Breadcrumb[] {
    const bigCompetitionPath = '/sports-pages/big-competition',
      competitionTree = this.parseCompetitionsData(data);
    this.breadcrumbs = [];
    this.breadcrumbs.push({ label: 'Competitions', url: bigCompetitionPath});

    switch (state) {
      case 'competitionId':
        this.pushBreadcrumbData(['competition'], competitionTree);
        break;
      case 'tabId':
        this.pushBreadcrumbData(['competition', 'tab'], competitionTree);
        break;
      case 'subTabId':
        this.pushBreadcrumbData(['competition', 'tab', 'subtab'], competitionTree);
        break;
      case 'moduleId':
        this.pushBreadcrumbData(['competition', 'tab', 'module'], competitionTree);
        break;
      case 'subTabAndModuleId':
        this.pushBreadcrumbData(['competition', 'tab', 'subtab', 'module'], competitionTree);
        break;
    }

    return this.breadcrumbs;
  }

  /**
   * Update competition when some of the childes(tab/subtab/module) was updated
   * @param competition
   * @param updatedObj
   */
  public updateCompetition(competition: any, updatedObj: any): void {
    const competitionTree = this.parseCompetitionsData(competition),
      states = Object.keys(competitionTree);

    _.forEach(states, state => {
      if (competitionTree[state] && competitionTree[state].id === updatedObj.id) {
        competitionTree[state].name = updatedObj.name;
        competitionTree[state].enabled = updatedObj.enabled;
      }
    });
  }

  /**
   * Push label and url to breadcrumbs
   * @param {Array<string>} states
   * @param competitionTree
   */
  private pushBreadcrumbData(states: Array<string>, competitionTree: any): void {
    const bigCompetitionPath = '/sports-pages/big-competition';
    let url = `${bigCompetitionPath}`;

    _.forEach(states, (value, key) => {
      if (!key) {
        url += `/${competitionTree[value].id}`;
      } else if (competitionTree[value]) {
        url += `/${value}/${competitionTree[value].id}`;
      }

      if (competitionTree[value]) {
        this.breadcrumbs.push({label: competitionTree[value].name, url: url});
      }
    });
  }

  /**
   * Parse competition data
   * @param competition
   * @returns {any}
   */
  private parseCompetitionsData(competition: any): any {
    const tab = _.isArray(competition.competitionTabs) && competition.competitionTabs[0],
      subtab = tab && _.isArray(tab.competitionSubTabs) && tab.competitionSubTabs[0],
      subtabModule = subtab && _.isArray(subtab.competitionModules) && subtab.competitionModules[0],
      tabModule = tab && _.isArray(tab.competitionModules) && tab.competitionModules[0];

    return {
      competition: competition,
      tab: tab,
      subtab: subtab,
      module: subtabModule || tabModule
    };
  }

  public parseCompetitionGroupsData(groups: StatsCenterGroups): ParsedCompetitionGroups {
    let groupsNames = [];
    let seasonsNames = [];
    let groupsNotFound = false;
    if (_.has(groups, 'allCompetitions') && groups.allCompetitions.length) {
      groupsNames = _.chain(groups.allCompetitions)
        .sortBy('name')
        .map('name')
        .value();
      seasonsNames = _.chain(groups.allSeasons)
        .sortBy('name')
        .map('name')
        .value();
    } else {
      groupsNotFound = true;
    }
    return { groupsNames, seasonsNames, groupsNotFound };
  }

  /**
   * Parse competitions seasons data
   * @param {StatsCenterSeason[]} seasons
   * @returns {{seasonsNames: string[], seasonsNotFound: boolean}}
   */
  public parseCompetitionSeasonsData(seasons: StatsCenterSeason[]): { seasonsNames: string[], seasonsNotFound: boolean } {
    let seasonsNames  = [],
      seasonsNotFound = false;
    seasonsNames = _.chain(seasons)
      .sortBy('name')
      .map('name')
      .value();
    seasonsNotFound = !(seasonsNames && seasonsNames.length);

    return { seasonsNames, seasonsNotFound };
  }

  /**
   * Set current value for selections "Available Groups" & "Available Seasons"
   */

  public setSeasonCurrentValue(statsCenterGroups: StatsCenterGroups, seasonId: number) {
    const currentSeason = _.find(statsCenterGroups.allSeasons, ['id', seasonId]);
    return currentSeason ? currentSeason.name : '';
  }

  public setGroupCurrentValue(statsCenterGroups: StatsCenterGroups,  competitionId: number) {
    const currentGroup = _.find(statsCenterGroups.allCompetitions, ['id', competitionId]);
    return currentGroup ? currentGroup.name : '';
  }

  /**
   * Search all paths from BC structure
   * @param {Array} tabAr
   * @param {Array} paths
   * @returns {Array<string>} all available paths
   */
  public getAllPaths(tabAr: any[], paths: string[] = []) {
    tabAr.forEach((singleTab) => {
      if (singleTab.hasSubtabs && (singleTab.competitionSubTabs && singleTab.competitionSubTabs.length)) {
        this.getAllPaths(singleTab.competitionSubTabs, paths);
      } else {
        paths.push(singleTab.path);
      }
    });
    return paths;
  }

/**
 * Sets surfaceBets data
 * @param {Array} data
 */
 setSurfaceBetsData(data: any) : void{
  this.surfaceBets = data;
}

/**
* Gets surfaceBets data
* @returns {Array<any>} 
*/
getSurfaceBetsData() : any {
  return this.surfaceBets;
}

/**
 * Sets Highlight Carousel data
 * @param {Array} data
 */
setHighlightsCarouselData(data: any): void {
  this.highlightsCarousel = data;
 }

/**
 * Gets Highlight Carousel data
 * @returns {Array<any>} 
 */
 getHighlightsCarouselData(): any {
  return this.highlightsCarousel;
 }

 /**
 * Sets tabType data
 * @param {string} data
 */
  setTabType(data: any) : void{
    this.tabType = data;
  }

  /**
 * Gets tabType data
 * @returns {string} 
 */
  getTabType() : any {
    return this.tabType;
  }
}
