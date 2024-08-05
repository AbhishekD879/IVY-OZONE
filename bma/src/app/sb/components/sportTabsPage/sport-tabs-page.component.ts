import { Component, OnInit, OnDestroy, OnChanges, Input, ChangeDetectorRef, SimpleChanges } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs';

import { concatMap } from 'rxjs/operators';

import { GamingService } from '@core/services/sport/gaming.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { ISportConfigurationTabs } from '@sb/models/sport-configuration.model';
import { SlpSpinnerStateService } from '@app/core/services/slpSpinnerState/slpSpinnerState.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { UpdateEventService } from '@core/services/updateEvent/update-event.service';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { EventMethods } from '@app/core/services/cms/models/sport-config-event-methods.model';
import { ISportConfigTab, ISportTabs } from '@app/core/services/cms/models';
import { CmsService } from '@app/core/services/cms/cms.service';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'sport-tabs-page',
  templateUrl: 'sport-tabs-page.component.html'
})
export class SportTabsPageComponent extends AbstractOutletComponent implements OnInit, OnDestroy, OnChanges {
  @Input() displayTab: ISportConfigurationTabs;
  @Input() index: number;
  sport: GamingService;
  sportName: string;
  sportId: string;
  display: string;
  isTierOneOrTwoSport: boolean;
  showMatchesSection: boolean;
  isLazyComponentLoading: boolean;
  isDesktop: boolean;
  sportTabs: ISportConfigTab[];
  topMarkets: any;

  private routeChangeListener: Subscription;
  private isLoaded: boolean = false;
  private featuredSpinner: boolean = false;
  private sportsConfigSubscription: Subscription;
  private readonly LAZY_COMPONENTS = ['live', 'competitions'];

  constructor(private activatedRoute: ActivatedRoute,
              private sportsConfigService: SportsConfigService,
              private router: Router,
              private slpSpinnerStateService: SlpSpinnerStateService,
              private windowRefService: WindowRefService,
              protected navigationService: NavigationService,
              protected changeDetectorRef: ChangeDetectorRef,
              // eslint-disable-next-line
              private updateEventService: UpdateEventService, // for events subscription (done in service init)
              private cmsService: CmsService
  ) {
    super();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.displayTab) {
      this.displayTab = changes.displayTab.currentValue;
    }
  }
  ngOnInit(): void {
    this.isDesktop = environment.CURRENT_PLATFORM === "desktop";
    this.sportName = this.activatedRoute.snapshot.paramMap.get('sport');
    this.display = (this.displayTab && this.displayTab.name) || this.activatedRoute.snapshot.paramMap.get('display');
    if (!this.LAZY_COMPONENTS.includes(this.display) && this.display !== 'null') {
      this.navigationService.emitChangeSource.next(true);
    }
    this.checkDisplayingLazyComponent();

    if (!this.displayTab) {
      this.routeChangeListener = this.activatedRoute.params.subscribe((params: { display: string }) => {
        if (this.display !== params['display']) {
          this.display = params['display'];
          this.checkDisplayingLazyComponent();
        }
      });
    }
    this.showSpinner();
    this.sportsConfigSubscription = this.sportsConfigService.getSport(this.sportName)
      .pipe(
        concatMap((sport: GamingService) => {
          this.sport = sport;
          this.sportId = this.sport.readonlyRequestConfig.categoryId;
          this.isTierOneOrTwoSport = [1, 2].includes(this.sport.config.tier);
          this.topMarkets = (this.sport.sportConfig.config.request.aggregatedMarkets || []);

          return this.cmsService.getSportTabs(this.sportId);
        }),
      )
      .subscribe((sportTabs: ISportTabs) => {
        this.sportTabs = sportTabs.tabs;
        this.navigateToSportLandingPage();
        this.sportId = this.sport.readonlyRequestConfig.categoryId;
        if (this.reloadInitiated) {
          this.changeDetectorRef.detectChanges();
        }
        this.hideSpinner();
      }, error => {
        this.showError();
        console.warn('MatchesPage', error.error || error);
      });
  }

  ngOnDestroy(): void {
    this.routeChangeListener && this.routeChangeListener.unsubscribe();
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
  }

  /**
   * Show sport tab
   * @param {string} display
   * @param {boolean} isFootball - true: only for Football, false: only for other sports
   * @returns {string}
   */
  showSportTab(display: string, isFootball: boolean): string {
    const isFootballSport = isFootball && this.sportName === 'football';
    const isNotFootballSport = !isFootball && this.sportName !== 'football';
    return isFootballSport || isNotFootballSport ? display : '';
  }

  receiveSpinnerStatus($event: boolean): void {
    this.isLoaded = $event;
    this.isLoaded && this.handleMatchesLoadingStatus();
  }

  hideMatches($event: boolean): void {
    this.showMatchesSection = $event;
  }

  featuredSpinnerStatus($event: { value: boolean}): void {
    // To fix angular error: 'Expression has changed after it was checked...'
    this.windowRefService.nativeWindow.setTimeout(() => {
      this.featuredSpinner = $event.value;
      this.featuredSpinner && this.handleMatchesLoadingStatus();
    });
  }

  updateLoadStatus(output: ILazyComponentOutput): void {
    this.windowRefService.nativeWindow.setTimeout(() => {
      if (output.output === 'isLoadedEvent' && output.value) {
        this.hideSpinner();
        this.navigationService.emitChangeSource.next(output.value);
      }
    });
  }

  initLazyHandler(): void {
    if (this.display === EventMethods.live) {
      this.navigationService.emitChangeSource.next(true);
    }
    this.isLazyComponentLoading = false;
  }

  protected navigateToSportLandingPage(): void {
    const sportURL: string = this.activatedRoute.snapshot.url[0].path === 'olympics' ? `olympics/` : 'sport/',
      sportLandingPage = `${sportURL}${this.sportName}`;
    if (!this.isTierOneOrTwoSport) {
      this.router.navigateByUrl(sportLandingPage);
    }
  }

  private checkDisplayingLazyComponent(): void {
    this.isLazyComponentLoading = this.LAZY_COMPONENTS.some((lazyComponent: string) => this.display === lazyComponent);
  }

  private handleMatchesLoadingStatus(): void {
    (this.isLoaded || this.display !== 'matches') && this.featuredSpinner && this.slpSpinnerStateService.handleSpinnerState();
  }
}
