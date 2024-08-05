import { concatMap, finalize } from 'rxjs/operators';
import { from as observableFrom,  Observable } from 'rxjs';
import { Component, OnInit, Input, ViewEncapsulation, Output, EventEmitter } from '@angular/core';
import * as _ from 'underscore';

import { StorageService } from '@core/services/storage/storage.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ICompetitionCategory, ILoadingState } from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions.model';
import { CurrentMatchesService } from '@sb/services/currentMatches/current-matches.service';
import { ICompetitionsConfig } from '@core/services/cms/models/system-config';
import { GamingService } from '@app/core/services/sport/gaming.service';
import { ISportConfigTab } from '@app/core/services/cms/models';

@Component({
  selector: 'competitions-sport-tab',
  templateUrl: 'competitions-sport-tab.component.html',
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class CompetitionsSportTabComponent implements OnInit {
  @Input() sport: GamingService;
  @Input() sportTabs: ISportConfigTab[];
  @Output() readonly isLoadedEvent: EventEmitter<boolean> = new EventEmitter();

  isResponseError: boolean = false;
  isLoaded: boolean = false;
  isTierOne: boolean = false;
  eventsBySectionsLength: number;
  currentMatchCategories: ICompetitionCategory[] = [];
  allCategories: ICompetitionCategory[] = [];
  categoryName: string;
  categoryId: string;
  childComponentLoaded: boolean = false;
  isNoCategories: boolean;
  isLoading: boolean = true;
  targetTab:ISportConfigTab;
  allAccorditions:ICompetitionCategory[] = [];

  constructor(
    private currentMatchesService: CurrentMatchesService,
    private cmsService: CmsService,
    private storageService: StorageService
  ) {}

  ngOnInit(): void {
    this.isTierOne = this.sport.config.tier === 1;
    this.categoryName = this.sport.config.name;
    this.categoryId = this.sport.config.request.categoryId;
    if (this.isTierOne) {
      this.loadCompetitionsData(this.categoryName);
      this.isLoadedEvent.emit(true);
      if(this.sportTabs){
        this.targetTab = this.sportTabs.find((tab: ISportConfigTab) => tab.id.includes('competitions'));
      }
    }
   
  }

  checkIsLoading(): void {
    this.isLoading = !this.isLoaded
        || (this.isTierOne && !this.isResponseError && !this.isNoCategories && !this.childComponentLoaded);
  }

  updateLoadingState(event: ILoadingState): void {
    this.isResponseError = event.isResponseError;
    this.isLoaded = event.isLoaded;
    this.eventsBySectionsLength = event.eventsBySectionsLength;
    this.checkIsLoading();
    this.isLoadedEvent.emit(this.isLoaded);
  }

  childComponentLoadedHandler(): void {
    this.childComponentLoaded = true;
    this.checkIsLoading();
  }

  /**
   * Load Sport Competitions Data
   */
  public loadCompetitionsData(categoryName: string): void {
    let matchCompetitions = [], azCompetitions = [];
    this.isLoaded = false;
    this.isResponseError = false;
    this.cmsService.getCompetitions(categoryName).pipe(
      concatMap((competitionsConfig: ICompetitionsConfig) => {
        matchCompetitions = this.getIds(competitionsConfig, 'InitialClassIDs');
        azCompetitions = this.getIds(competitionsConfig, 'A-ZClassIDs');
        const allIds: string[] = _.union(matchCompetitions, azCompetitions);
        return this.getClasses(allIds, categoryName); }))
          .pipe(finalize(() => {
            this.isLoaded = true;
            this.checkIsLoading();
          }))
          .subscribe((result: ICompetitionCategory[]) => {
            this.allCategories = this.azCompetitions(result, azCompetitions, categoryName);
            this.currentMatchCategories = this.mainCompetitions(result, matchCompetitions, categoryName);
            this.isNoCategories = !this.currentMatchCategories.length && !this.allCategories.length;
            this.isResponseError = false;
            this.allAccorditions=this.currentMatchCategories.concat(this.allCategories);
          }, error => {
            console.warn('Competitions Data:', error);
            this.isResponseError = true;
          });
  }

  private getIds(competitionsConfig: ICompetitionsConfig, name: string): string[] {
    return competitionsConfig[name] ? competitionsConfig[name].split(',') : [];
  }

  private azCompetitions(competitions: ICompetitionCategory[], ids: string[], categoryName: string): ICompetitionCategory[] {
    this.storageService.set(`competitionsAZClasses_${categoryName}`, ids);
    return ids.length ? _.sortBy(this.filterCompetitions(competitions, ids), (item: ICompetitionCategory) => {
      return item.class.name.toLowerCase();
    }) : [];
  }

  private mainCompetitions(competitions: ICompetitionCategory[], ids: string[], categoryName: string): ICompetitionCategory[] {
    const result = ids.length ? this.filterCompetitions(competitions, ids) : [];
    this.storageService.set(`competitionsMainClasses_${categoryName}`, result);
    return result;
  }

  private filterCompetitions(competitions: ICompetitionCategory[], ids: string[]): ICompetitionCategory[] {
    return _.filter(competitions, (competition: ICompetitionCategory) => {
      return ids.includes(competition.class.id);
    });
  }

  /**
   * Return sub-categories(Class ID) for football only
   *
   * @params {string[]} Class Ids from CMS
   * return {Observable<ICompetitionCategory[]>} Filtered sub-categories
   */
  private getClasses(ids: string[], categoryName: string): Observable<ICompetitionCategory[] | any[]> {
    if (categoryName === 'football') {
      return observableFrom(this.currentMatchesService.getFootballClasses(ids));
    }
    return observableFrom(this.currentMatchesService.getOtherClasses(ids, this.categoryId));
  }
}
