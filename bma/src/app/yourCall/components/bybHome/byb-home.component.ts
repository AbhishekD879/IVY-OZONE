import { IYourcallBYBEventResponse } from '@yourcall/models/byb-events-response.model';
import { BybHomeService } from './byb-home.service';
import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import * as _ from 'underscore';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
@Component({
  selector: 'byb-home',
  templateUrl: './byb-home.component.html'
})
export class BybHomeComponent extends AbstractOutletComponent implements OnInit, OnDestroy {

  switchers: {
    name: string;
    onClick: Function;
    viewByFilters: any;
  }[];
  filter: string;
  displayData: IYourcallBYBEventResponse[];
  loaded: boolean;
  leaguesStatuses: { [key: number]: boolean; } = {};
  contentReady: boolean = false;
  initialPageLoad: boolean = true;

  private viewByFilters: string[];

  private readonly DEFAULT_OPENED_LEAGUES: number = 2;

  constructor(
    private bybHomeService: BybHomeService,
    private changeDetectorRef: ChangeDetectorRef
  ) {
    super()/* istanbul ignore next */;
    this.switchers = null;
    this.filter = null;
    this.displayData = null;
    this.loaded = false;
    this.viewByFilters = [
      'today',
      'upcoming'
    ];
  }

  ngOnInit(): void {
    this.getLeagues();
  }

  ngOnDestroy(): void {
    this.displayData && this.displayData.map((league: IYourcallBYBEventResponse) => {
      league.expaned = false;
    });
  }

  trackByLeague(index: number, league: IYourcallBYBEventResponse): string {
    return `${index}${league.status}${league.title}${league.obTypeId}`;
  }

  /**
   * Show switchers or not
   * @return {boolean}
   */
  showSwitchers(): boolean {
    return this.switchers && this.switchers.length >= 1;
  }

  /**
   * Get leagues title
   * @param league
   * @returns {string}
   */
  getTitle(league: IYourcallBYBEventResponse): string {
    if (!league.normilized) {
      return league.title;
    }
    return `${league.categoryName} - ${league.className.replace(league.categoryName, '')} - ${league.typeName}`;
  }

  trackExpandCollapse(league: IYourcallBYBEventResponse): void {
    league.initiallyExpanded = false;
    league.expaned = !league.expaned;
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Sends request to get all leagues
   * @private
   */
  private getLeagues(): void {
    this.showSpinner();
    this.bybHomeService.getLeagues()
      .then(() => {
        this.leaguesStatuses = this.bybHomeService.leaguesStatuses;
        this.createSwitchers();
        if (this.switchers && this.switchers.length > 0) {
          this.selectSwitcher(this.switchers[0].viewByFilters);
        }
        this.loaded = true;
        this.contentReady = true;
        this.hideSpinner();
      }, () => {
        this.loaded = true;
        this.contentReady = true;
        this.showError();
      });
  }

  /**
   * Created switchers for today/upcoming tabs
   * @private
   */
  private createSwitchers(): void {
    this.switchers = [];

    _.each(this.viewByFilters, (filter, index) => {
      if (this.shouldCreateSwitcher(this.bybHomeService[`${filter}Leagues`])) {
        this.switchers.push({
          name: `yourcall.${filter}`,
          onClick: () => this.onSwitcherChange(index),
          viewByFilters: this.viewByFilters[index]
        });
      }
    });
  }

  private onSwitcherChange(index: number): void {
    this.contentReady = false;
    this.initialPageLoad = false;
    this.selectSwitcher(this.viewByFilters[index]);
  }

  /**
   * If we have cms available leagues for this range we will display switcher
   * @param leagues
   * @private
   */
  private shouldCreateSwitcher(leagues: IYourcallBYBEventResponse[]) {
    return _.some(leagues, (league: IYourcallBYBEventResponse) => {
      return this.bybHomeService.leaguesStatuses[league.obTypeId];
    });
  }

  /**
   * Select switcher handler; changes data to display
   * @param index
   * @private
   */
  private selectSwitcher(index: string): void {
    this.filter = index;
    let i: number = 0;
    this.displayData = this.bybHomeService[`${index}Leagues`].map((league: IYourcallBYBEventResponse) => {
      if (this.leaguesStatuses[league.obTypeId] && i < this.DEFAULT_OPENED_LEAGUES) {
        league.expaned = true;
        league.initiallyExpanded = true;
        league.eventsLoaded = false;
        i++;
      }
      return league;
    });
    this.handleEventsLoaded();
  }

  /**
   * Updates content ready state when child component data loaded
   */
  public handleEventsLoaded(): void {
    this.contentReady = this.displayData && this.displayData.every(league => league.initiallyExpanded &&
      this.leaguesStatuses[league.obTypeId] ? league.eventsLoaded : true);
    this.changeDetectorRef.detectChanges();
  }
}
