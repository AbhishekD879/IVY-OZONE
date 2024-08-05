import { Component, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Location } from '@angular/common';

import { GamingService } from '@core/services/sport/gaming.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { UpdateEventService } from '@core/services/updateEvent/update-event.service';
import { Subscription } from 'rxjs';
import { concatMap } from 'rxjs/operators';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { FILTER_TYPES, ICompetitionFilter } from '@lazy-modules/competitionFilters/models/competition-filter';
import { CompetitionFiltersService } from '@lazy-modules/competitionFilters/services/competitionFilters/competition-filters.service';
import { ISportTabs } from '@app/core/services/cms/models';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISportConfigTab } from '@app/core/services/cms/models';

@Component({
  selector: 'sport-matches-page',
  templateUrl: 'sport-matches-page.component.html'
})
export class SportMatchesPageComponent extends AbstractOutletComponent implements OnInit, OnDestroy {

  @ViewChild('SportMatchesTab', { static: false }) SportMatchesTab;

  sport: GamingService;
  sportId: string;
  sportName: string;
  isNoModulesLoaded: boolean = true;

  isNotAllModulesLoaded: boolean = true;
  featuredEventsCount: number = 0;
  isFeaturedLoaded: boolean = false;

  timeFilter: ICompetitionFilter;
  leagueFilter: ICompetitionFilter;
  competitionFilters: ICompetitionFilter[] = [];
  isSportEventFiltersEnabled: boolean;
  displayFilters = false;
  isGolfMatchesTab: boolean = false;

  private modulesLoadStatus: boolean[] = [];
  protected sportsConfigSubscription: Subscription;
  protected cmsConfigSubscription: Subscription;
  protected tabName: string = 'matches';
  targetTab: ISportConfigTab;
  changeTabName: ISportTabs;

  constructor(private location: Location,
    protected sportsConfigService: SportsConfigService,
    private routingState: RoutingState,
    protected route: ActivatedRoute,
    protected router: Router,
    protected navigationService: NavigationService,
    protected windowRefService: WindowRefService,
    protected competitionFiltersService: CompetitionFiltersService,
    // eslint:disable-next-line
    protected updateEventService: UpdateEventService, // for events subscription (done in service init)
    protected cmsService: CmsService
  ) {
    super();
  }

  ngOnInit(): void {
    this.competitionFiltersService.selectedMarket = '';
    this.isFeaturedLoaded = false;
    this.showSpinner();
    this.getSportEventFiltersAvailability();
    this.sportName = this.route.snapshot.paramMap.get('sport');
    this.sportsConfigSubscription = this.sportsConfigService.getSport(this.sportName)
      .pipe(
        concatMap((sportInstance: GamingService) => {
          this.sport = sportInstance;
          this.sportId = (this.sport && this.sport.readonlyRequestConfig && this.sport.readonlyRequestConfig.categoryId) || '0';
          return this.cmsService.getSportTabs(this.sportId);
        })
      )
      .subscribe((sportTabs: ISportTabs) => {
        this.changeTabName = sportTabs;
        this.getCurrentTargetTab();
        this.competitionFilters = this.competitionFiltersService.formTimeFilters(
          this.tabName, sportTabs.tabs, this.competitionFiltersService.formLeagueFilters(this.tabName, sportTabs.tabs)
        );
        this.targetTab = sportTabs.tabs.find((tab: ISportConfigTab) => tab.id.includes(this.tabName));
        this.loadSport();
      }, error => {
        this.showError();
        console.warn('MatchesPage', error.error || error);
      });
  }

  ngOnDestroy(): void {
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
    this.cmsConfigSubscription && this.cmsConfigSubscription.unsubscribe();
  }

  /**
   * Update global and module-personal (by index) load statuses
   * index should correspond to specific module
   *
   * setTimeout is to avoid ExpressionChangedAfterItHasBeenCheckedError (and not to use ChangeDetectorRef)
   *
   * loadedMatch is to avoid reload cause on Sub-navigation
   * 
   * @param i
   * @param isLoaded
   */
  updateLoadStatus(i: number = 0, output: ILazyComponentOutput): void {
    const loadedMatch = this.navigationService['routingStateService']['segmentHistory'].includes("sport.display");
    this.isGolfMatchesTab = this.route.snapshot['_routerState'] && this.route.snapshot['_routerState'].url.includes('golf_matches');
    if (output.output === 'featuredEventsCount') {
      this.featuredEventsCount = output.value;
      this.isFeaturedLoaded = true;
    }

    this.windowRefService.nativeWindow.setTimeout(() => {
      if (output.output === 'isLoadedEvent') {
        loadedMatch?this.navigationService.emitChangeSource.next(true):this.navigationService.emitChangeSource.next(false);
        if (i === 0 && output.value) {
          this.isFeaturedLoaded = true;
        }
        this.modulesLoadStatus[i] = output.value;
        this.isNotAllModulesLoaded = !this.modulesLoadStatus.every(loaded => loaded);
        if (!this.isNotAllModulesLoaded) {
          this.hideSpinner();
        }
        if (this.modulesLoadStatus[0] && this.modulesLoadStatus[1]) {
          this.navigationService.emitChangeSource.next(output.value);
        }
      }
    });
  }

  reloadPage(): void {
    this.showSpinner();
    this.SportMatchesTab.ngOnDestroy();
    this.SportMatchesTab.ngOnInit();
  }

  /**
   * Updates time | league filter when user clicks on them
   * @param {ILazyComponentOutput} output
   */
  handleCompetitionFilterOutput(output: ILazyComponentOutput): void {
    if (output.output === 'filterChange') {
      const filter: ICompetitionFilter = { ...output.value };

      filter.type === FILTER_TYPES.TIME
        ? this.timeFilter = { ...this.timeFilter, ...filter }
        : this.leagueFilter = { ...this.leagueFilter, ...filter };
    }
  }

  /**
   * Load Sport Page (ex: Today, Tomorrow, Future)
   */
  protected loadSport(tabName: string = ''): void {
    const sportPath = this.route.snapshot.parent.data['segment'] === 'olympicsSport'
      ? `olympics/${this.sportName}`
      : `sport/${this.sportName}`;

    const currentURL = this.route.snapshot['_routerState'] && this.route.snapshot['_routerState'].url.includes('golf_matches');
    const display = this.route.snapshot.routeConfig.data.segment === 'sport' ? '' : `/matches${tabName && `/${tabName}`}`;
    const newURL: string = currentURL ? `${sportPath}/golf_matches${tabName && `/${tabName}`}` : `${sportPath}${display}`;
    const pathName: string = this.location.path();

    if (`/${newURL}` === pathName) { return; }

    this.location.go(newURL);
    // Needs for back button functionality as location.go doesn't trigger router events
    this.routingState.setCurrentUrl(pathName);
  }

  protected getSportEventFiltersAvailability(): void {
    this.cmsConfigSubscription = this.competitionFiltersService.getSportEventFiltersAvailability()
      .subscribe((isAvailable: boolean) => this.isSportEventFiltersEnabled = isAvailable);
  }

  /**
   * show/hide filters
   */
  updateFiltersDisplay(isDisplayFilters: boolean): void {
    this.displayFilters = isDisplayFilters;
  }


  /***
   * Function stores targetTab based on selected tab
  */
  getCurrentTargetTab(): void {
    const currentURL =  this.route.snapshot['_routerState'] && this.route.snapshot['_routerState'].url;
    this.tabName = currentURL.includes('golf_matches') ? 'golf_matches' : 'matches';
    this.targetTab = this.changeTabName?.tabs.find((tab: ISportConfigTab) => tab.id.includes(this.tabName));
  }
}
