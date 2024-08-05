import { Subscription } from 'rxjs';
import { Component, OnInit, Input, OnDestroy } from '@angular/core';

import { IBreadcrumb, IBreadcrumbConfig } from '@coralDesktop/shared/components/breadcrumbs/breadcrumbs.model';
import { BreadcrumbsService } from '@coralDesktop/core/services/breadcrumbs/breadcrumbs.service';
import { Router, Event, NavigationEnd, ActivatedRoute } from '@angular/router';
import * as _ from 'underscore';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { Location } from '@angular/common';
import { ITab } from '@shared/components/tabsPanel/tabs-panel.model';

@Component({
  selector: 'breadcrumbs',
  templateUrl: './breadcrumbs.component.html',
  styleUrls: ['./breadcrumbs.component.scss'],
})
export class BreadcrumbsComponent implements OnInit, OnDestroy {

  breadcrumbsItems: IBreadcrumb[];

  @Input() sportName: string;
  @Input() sportEvent: string;
  @Input() sportTabs: ITab[];
  @Input() competitionName: string;
  @Input() isOlympics: boolean;
  @Input() isEDPpage: boolean;
  @Input() defaultTab: string = '';

  private subscription: Subscription;

  constructor(
    private breadcrumbsService: BreadcrumbsService,
    private router: Router,
    private route: ActivatedRoute,
    private routingState: RoutingState,
    private location: Location
  ) { }

  ngOnInit(): void {
    this.resetBreadcrumbsList();
    this.registerEventHandlers();
}

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }

  trackByBreadCrumb(breadCrumb): string {
    return breadCrumb.name;
  }

  /**
   * Set $routeChangeSuccess handler
   * @private
   */
  private registerEventHandlers(): void {
    this.subscription = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd) {
        _.debounce(() => {
          this.resetBreadcrumbsList();
        }, 50)();
      }
    });
  }

  /**
   * Get list of breadcrumbs
   * @private
   */
  private resetBreadcrumbsList(): void {
    const config: IBreadcrumbConfig = this.buildConfig();
    this.breadcrumbsItems = this.breadcrumbsService.getBreadcrumbsList(config, this.defaultTab);
  }

  private buildConfig(): IBreadcrumbConfig {
    const sportName = this.sportName || this.routingState.getRouteParam('sport', this.route.snapshot);
    return {
      sportName,
      tabs: this.sportTabs,
      competitionName: this.competitionName,
      isEDPPage: this.isEDPpage || (this.sportEvent && sportName && !this.competitionName),
      isOlympicsPage: this.location.path().includes('olympics') || this.isOlympics,
      isCompetitionPage: this.location.path().includes('competitions'),
      isBuildYourRaceCardPage: this.location.path().includes('build-your-own-race-card'),
      eventName: this.sportEvent,
      className: this.routingState.getRouteParam('className', this.route.snapshot),
      display: this.routingState.getRouteParam('display', this.route.snapshot) || '',
      isFootballPage: sportName === 'football',
      isHorseRacingPage: sportName === 'horseracing',
      isGreyhoundPage: sportName === 'greyhound',
      isVirtual: sportName === 'virtual-sports'
    };
  }
  /**
   * Validates the uri allows further routing
   * @returns void
   */
  navigateUri($event: MouseEvent, routeUrl: string): void {
    this.routingState.navigateUri($event, routeUrl, this.sportName, this.defaultTab);
  }
}
