import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Event, NavigationEnd, Router } from '@angular/router';
import { Location } from '@angular/common';
import { filter, concatMap } from 'rxjs/operators';
import * as _ from 'underscore';

import { GamingService } from '@core/services/sport/gaming.service';
import { ISportConfigSubTab } from '@app/olympics/models/olympics.model';
import { SportMatchesPageComponent } from '@sb/components/sportMatchesPage/sport-matches-page.component';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { UpdateEventService } from '@core/services/updateEvent/update-event.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { CompetitionFiltersService } from '@lazy-modules/competitionFilters/services/competitionFilters/competition-filters.service';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISportTabs } from '@app/core/services/cms/models';
import { Subscription } from 'rxjs';

@Component({
  selector: 'sport-matches-page',
  templateUrl: 'sport-matches-page.component.html'
})

export class DesktopSportMatchesPageComponent extends SportMatchesPageComponent implements OnInit, OnDestroy {
  tab: string;
  matchesTabs: ISportConfigSubTab[];
  switchers: ISportConfigSubTab[];
  isFootball: boolean;
  locationChangeListener: Subscription;
  indexPage: number;
  categoryId: string;
  changeTabName:ISportTabs;

  constructor(location: Location,
              sportsConfigService: SportsConfigService,
              routingState: RoutingState,
              protected route: ActivatedRoute,
              protected router: Router,
              navigationService: NavigationService,
              windowRefService: WindowRefService,              
              competitionFiltersService: CompetitionFiltersService,
              // eslint-disable-next-line
              protected updateEventService: UpdateEventService, // for events subscription (done in service init)
              protected cmsService: CmsService
  ) {
    super(
      location,
      sportsConfigService,
      routingState,
      route,
      router,
      navigationService,
      windowRefService,
      competitionFiltersService,
      updateEventService,
      cmsService
    );
  }

  ngOnInit(): void {
    this.competitionFiltersService.selectedMarket = '';
    this.sportName = this.route.snapshot.paramMap.get('sport');
    this.isFootball = this.sportName === 'football';
    this.tab = this.route.children && this.route.snapshot.paramMap.get('tab');
    if(this.tab && this.tab === 'allEvents'){
      this.switchers = this.initializeMatchesSwitchers(this.sportName);
    }
    else{
      this.switchers = this.initializeSwitchers(this.sportName);
    }
    this.indexPage = this.getTabIndex(this.tab);
    this.showSpinner();
    this.getSportEventFiltersAvailability();
    this.sportsConfigSubscription = this.sportsConfigService.getSport(this.sportName)
      .pipe(
        concatMap((sportInstance: GamingService) => {
          this.sport = sportInstance;
          this.categoryId = this.sport.config.request.categoryId;
          this.sportId = (this.sport && this.sport.readonlyRequestConfig && this.sport.readonlyRequestConfig.categoryId) || '0';
          return this.cmsService.getSportTabs(this.sportId);
        })
      )
      .subscribe((sportTabs: ISportTabs) => {
        this.competitionFilters = this.competitionFiltersService.formTimeFilters(
          this.tabName, sportTabs.tabs, this.competitionFiltersService.formLeagueFilters(this.tabName, sportTabs.tabs)
        );
        this.changeTabName = sportTabs
        this.getCurrentTargetTab();
        this.loadSport(this.switchers[this.indexPage].name);
        this.addLocationChangeHandler();
        this.hideSpinner();
      }, error => {
        this.showError();
        console.warn('MatchesPage', error.error || error);
      });
  }

  ngOnDestroy(): void {
    this.locationChangeListener && this.locationChangeListener.unsubscribe();
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
    this.cmsConfigSubscription && this.cmsConfigSubscription.unsubscribe();
  }

  loadSport(tabName: string = ''): void {
    this.tab = tabName;
    super.loadSport(tabName);
  }

  private addLocationChangeHandler(): void {
    this.locationChangeListener = this.router
      .events.pipe(
        filter((event: Event) => event instanceof NavigationEnd))
      .subscribe(() => {
        const { tab } = this.route.snapshot.params;
        // TODO : Golf Imp
        if(tab && tab === 'allEvents' && this.sportId == '18'){
          this.getCurrentTargetTab();
          this.tab = tab;
          this.switchers = this.initializeMatchesSwitchers(this.sportName);
        }
        else{
          this.getCurrentTargetTab();
          this.tab = tab;
          this.switchers = this.initializeSwitchers(this.sportName);
        }
        this.selectTab(tab);
        if (tab === this.tab) { return; }
      });
  }

  /**
   * Function responsible for selecting tabs
   */
  private selectTab(switcherName: string): void {
    this.indexPage = this.getTabIndex(switcherName);
    this.switchers &&
    this.switchers[this.indexPage] &&
    this.switchers[this.indexPage].name &&
    this.loadSport(this.switchers[this.indexPage].name);
  }

  /**
   * Function return index of selected tab
   */
  private getTabIndex(name: string = ''): number {
    const index = _.findIndex(this.switchers, (tab: { name: string }) => tab.name === name);
    return index === -1 ? 0 : index;
  }


  private initializeSwitchers(sportName: string): ISportConfigSubTab[] {
    return [
      {
        id: 'tab-today',
        name: 'today',
        label: 'Today',
        url: `/sport/${sportName}/matches/today`,
        hidden: false,
        onClick: () => this.selectTab('today')
      },
      {
        id: 'tab-tomorrow',
        name: 'tomorrow',
        label: 'Tomorrow',
        url: `/sport/${sportName}/matches/tomorrow`,
        hidden: false,
        onClick: () => this.selectTab('tomorrow')
      },
      {
        id: 'tab-future',
        name: 'future',
        label: 'Future',
        url: `/sport/${sportName}/matches/future`,
        hidden: false,
        onClick: () => this.selectTab('future')
      }
    ];
  }

  private initializeMatchesSwitchers(sportName:string){
    return[      {
      id: 'tab-allEvents',
      name: 'allEvents',
      label: 'AllEvents',
      url: `/sport/${sportName}/golf_matches/allEvents`,
    }]
  }
}
