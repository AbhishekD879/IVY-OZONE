import { ActivatedRoute, Router, Params } from '@angular/router';
import * as _ from 'underscore';
import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { RoutesDataSharingService } from '@racing/services/routesDataSharing/routes-data-sharing.service';
import { TimeService } from '@core/services/time/time.service';
import { IInitialSportConfig } from '@core/services/sport/config/initial-sport-config.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { TemplateService } from '@shared/services/template/template.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';
import { GreyhoundService } from '@coreModule/services/racing/greyhound/greyhound.service';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { from, Observable, Subscription, zip } from 'rxjs';
import { filter } from 'rxjs/operators';
import { IRaceGridMeeting } from '@core/models/race-grid-meeting.model';
import environment from '@environment/oxygenEnvConfig';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';

@Component({
  selector: 'racing-tabs-main-component',
  templateUrl: './racing-tabs-main.component.html'
})
export class RacingTabsMainComponent extends AbstractOutletComponent implements OnInit, OnDestroy {

  @Input() isEventOverlay?: boolean = false;
  @Input() sportName?: string;
  racingName: string;
  racingPath: string;
  sportModule: string;
  eventsData: IRaceGridMeeting;
  racing: IRaceGridMeeting;
  racingYourCallSpecials: any = [];
  responseError: boolean = false;
  filter: string;
  display: string;
  eventsOrder: Array<string>;
  sectionTitle: any;
  isRunnersNumber: boolean;
  applyingParams: boolean;
  outcomesLimit: any;
  isRacingPanel: boolean;
  expanded: boolean;
  viewByFilters: Array<string>;
  tabsTitle: { [key: string]: string };

  getDate: number;
  getDay: string;
  getMonth: string;
  racingResultsFilters: Array<string>;
  categoryId: string;

  private readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;
  private filters: Array<string>;
  private racingFilters: Array<string>;
  private getDataSubscription: Subscription;
  private routeSubscription: Subscription;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private templateService: TemplateService,
    private timeService: TimeService,
    private routesDataSharingService: RoutesDataSharingService,
    private horseRacingService: HorseracingService,
    private greyhoundService: GreyhoundService,
    private routingState: RoutingState,
    private navigationService: NavigationService,
    public sessionStorageService: SessionStorageService
  ) {
    super();
  }

  ngOnInit(): void {
    this.routeSubscription = this.route.params
      .subscribe(
        (params: Params) => {
          this.display = params.display || params.tab;
          const segment = this.routingState.getCurrentSegment();
          if(!this.display) {
            this.display = this.isEventOverlay ? "future" : segment.indexOf('horseracing') >= 0 ? "featured" : "today";
          }
          this.getData();
        }
      );

    if(this.isEventOverlay) {
      this.display = 'future';
      this.getData();
    }
    this.categoryId = this.racingService.config.request.categoryId;
  }

  ngOnDestroy(): void {
    this.getDataSubscription && this.getDataSubscription.unsubscribe();
    this.routeSubscription && this.routeSubscription.unsubscribe();
  }

  goTo(path: string): void {
    this.router.navigateByUrl(path);
  }

  isFavourite(outcomeEntity: IOutcome): boolean {
    return +outcomeEntity.outcomeMeaningMinorCode > 0 || outcomeEntity.name.toLowerCase() === 'unnamed favourite' ||
      outcomeEntity.name.toLowerCase() === 'unnamed 2nd favourite';
  }

  definePriceType(marketEntity: IMarket, outcomeEntity: IOutcome): string {
    return (marketEntity.isSpAvailable &&
      (!marketEntity.isLpAvailable ||
        (marketEntity.isLpAvailable && !outcomeEntity.prices.length))) ||
    this.isFavourite(outcomeEntity) ? 'SP' : 'LP';
  }

  updateLoadStatus(output: boolean): void {
    if (output) {
      this.hideSpinner();
      this.navigationService.emitChangeSource.next(output);
    }
  }

  protected concatDataRequests(racingInstance: HorseracingService | GreyhoundService): Observable<[ISportEvent[], ISportEvent[]]> {
    const racingYourCallSpecials = this.display === 'featured' ? racingInstance.getYourCallSpecials() : Promise.resolve([]);

    return zip(from(racingInstance.getByTab(this.display, true)), from(racingYourCallSpecials));
  }

  private getData(): Subscription {
    if (!this.racingService.getConfig()) {
      return;
    }

    this.applyingParams = true;

    return this.getDataSubscription = this.concatDataRequests(this.racingService)
      .pipe(
        filter(([eventsData, racingYourCallSpecialsData]) => !!eventsData && !!racingYourCallSpecialsData)
      )
      .subscribe(
        ([eventsData, racingYourCallSpecialsData]) => this.processDataSuccess([eventsData, racingYourCallSpecialsData]),
        (err) => this.processDataError(err)
      );
  }

  private get racingService(): HorseracingService | GreyhoundService {
    const segment = this.isEventOverlay ? this.sportName : this.routingState.getCurrentSegment();

    return segment.indexOf('horseracing') >= 0 ? this.horseRacingService : this.greyhoundService;
  }
  private set racingService(value: HorseracingService | GreyhoundService){}
  private initModel(): void {
    const racingConfiguration: IInitialSportConfig = this.racingService.getGeneralConfig();

    this.racingName = this.racingService.getConfig().name;

    this.racingPath = this.racingService.getConfig().path;

    this.sportModule = racingConfiguration.config.sportModule;

    // Events ordering
    this.eventsOrder = racingConfiguration.order.EVENTS_ORDER;

    this.sectionTitle = racingConfiguration.sectionTitle;

    this.isRunnersNumber = racingConfiguration.isRunnerNumber;

    // Racing filters information
    this.racingFilters = racingConfiguration.filters.RACING_FILTERS;

    // Racing filters information for Results tab
    this.racingResultsFilters = racingConfiguration.filters.RESULTS_FILTERS;

    this.applyParams();

    this.filters = this.racingFilters;

    // Racing tabs information
    const racingTabs = this.routesDataSharingService.getRacingTabs(this.racingName);
    const isCorrectParams = this.racingService.isDisplayAndFilterCorrect(racingTabs, this.display, this.filters, this.filter);

    if (!this.isEventOverlay && !isCorrectParams) {
      this.router.navigateByUrl('/');
      return;
    }

    // Selecting active tab
    this.routesDataSharingService.updatedActiveTabId(`tab-${this.display}`);

    this.outcomesLimit = {};

    this.isRacingPanel = this.display !== 'results' && this.display !== 'specials';

    this.expanded = true;

    // Get racing grouped events
    this.racing = this.eventsData;
    if (this.racingService.config.request.categoryId === this.HORSE_RACING_CATEGORY_ID &&
      this.display === 'featured') {
      const currentDay = this.timeService.getDayI18nValue(new Date().toString()).split('.');
      this.racing = this.racingService.sortRaceGroup(this.eventsData, `racing.${currentDay[1]}`);
    }

    // TODO: Refactor this method, when sort and group logic will be moved from template
    this.racingService.addFirstActiveEventProp(this.racing);

    this.viewByFilters = [
      'by-meeting',
      'by-time'
    ];

    this.tabsTitle = {
      'by-meeting': 'sb.byMeeting',
      'by-time': 'sb.byTime'
    };

    _.each(this.racing.events, (event: ISportEvent) => {
      _.each(event.markets, market => {
        market.terms = this.templateService.genTerms(market);
      });
    });

  }

  /**
   * Get active tab and sorting criteria from route
   */
  private applyParams() {
    let display = this.isEventOverlay ? this.display : this.route.snapshot.params['display'];
    let _filter = this.route.snapshot.params['filter'];
    if(this.isEventOverlay) {
      display = this.display;
      _filter = this.sessionStorageService.get('gh-overlay-filterBy');
    }
    if (this.racingName === 'horseracing') {
      this.display = display || 'featured';
    } else {
      this.display = display || 'today';
      if (this.display !== 'results') {
        this.filter = _filter || 'by-meeting';
        this.sessionStorageService.set('gh-overlay-filterBy', this.filter);
      }
    }

    // Get Full Date (timestamp)
    this.getDate = this.timeService.incrementDateDay(this.display);

    // Get Day (example: Wednesday)
    this.getDay = this.timeService.getDayI18nValue(this.getDate.toString());

    // Get short Month (example: Apr)
    this.getMonth = this.timeService.getMonthI18nValue(new Date(this.getDate), false);

    if (this.display === 'results') {
      this.filter = this.route.snapshot.params['filter'] || 'by-latest-results';
    }
  }

  private processDataSuccess([eventsData, racingYourCallSpecials]) {
    this.racingYourCallSpecials = this.racingService.prepareYourCallSpecialsForFeaturedTab(racingYourCallSpecials);
    this.eventsData = eventsData;

    this.initModel();
    this.applyingParams = false;
    this.responseError = false;
    this.hideSpinner();
  }

  private processDataError(err) {
    this.showError();
    console.warn(err);
    this.state.error = true;
    this.applyingParams = false;
  }
}
