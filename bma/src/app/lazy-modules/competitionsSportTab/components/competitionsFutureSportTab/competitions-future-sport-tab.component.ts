import { Component, OnInit, OnDestroy, Input, Output, EventEmitter, ViewEncapsulation } from '@angular/core';

import * as _ from 'underscore';

import { ISportEvent } from '@app/core/models/sport-event.model';
import { SportTabsService } from '@app/sb/services/sportTabs/sport-tabs.service';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { ActivatedRoute } from '@angular/router';
import { RoutingHelperService } from '@app/core/services/routingHelper/routing-helper.service';
import { ILoadingState } from '../competitionsSportTab/competitions.model';
import { GamingService } from '@app/core/services/sport/gaming.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { from, Observable, Subscription } from 'rxjs';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { concatMap } from 'rxjs/operators';
import { EventMethods } from '@app/core/services/cms/models/sport-config-event-methods.model';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISystemConfig, ISportConfigTab } from '@app/core/services/cms/models';
import { MarketSortService } from '@sb/services/marketSort/market-sort.service';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';
import { ICompetitionFilter } from '@lazy-modules/competitionFilters/models/competition-filter';
import { CompetitionFiltersService } from '@lazy-modules/competitionFilters/services/competitionFilters/competition-filters.service';

@Component({
  selector: 'competitions-future-sport-tab',
  templateUrl: 'competitions-future-sport-tab.component.html',
  styleUrls: ['./competitions-future-sport-tab.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class CompetitionsFutureSportTabComponent implements OnInit, OnDestroy {
  @Input() sport: GamingService;
  @Input() sportTabs: ISportConfigTab[];
  @Input() sportName?: string;

  @Output() readonly updateLoadingState: EventEmitter<ILoadingState> = new EventEmitter();

  isResponseError: boolean = false;
  isMarketSwitcherConfigured: boolean = false;
  isLoaded: boolean = false;
  eventsBySections: ITypeSegment[];
  eventsBySectionsCopy: ITypeSegment[] = [];
  categoryId: string;
  limitedSections: { [key: number]: boolean }[] = [];
  loadData:boolean = false;
  switchers: any;
  position: any;
  competitionFilters: ICompetitionFilter[] = [];
  isSportEventFiltersEnabled: boolean;
  timeFilter: ICompetitionFilter;
  displayFilters = false;

  private matches: ISportEvent[];
  private outrights: ISportEvent[];
  private readonly componentName: string = 'CompetitionsFutureSportTabComponent';
  private loadEventsSubscription: Subscription;
  private marketSwitcherConfigSubscription: Subscription;
  private eventsLimit: number = 3;
  private readonly filtersKey: string = 'SportEventFilters';
  protected activeMarketFilter: string;
  targetTab: ISportConfigTab;
  constructor(
    private sportTabsService: SportTabsService,
    private routingHelperService: RoutingHelperService,
    private pubSubService: PubSubService,
    private activatedRoute: ActivatedRoute,
    private deviceService: DeviceService,
    private cmsService: CmsService,
    private marketSortService: MarketSortService,
    private competitionFiltersService: CompetitionFiltersService,
  ) { }

  ngOnInit(): void {
    this.categoryId = this.sport.config.request.categoryId;

    this.competitionFilters = this.competitionFiltersService.formTimeFilters('competitions', this.sportTabs);
    if(this.sportTabs){
      this.targetTab = this.sportTabs.find((tab: ISportConfigTab) => tab.id.includes('competitions'));
    }
    this.marketSwitcherConfigSubscription = this.cmsService.getMarketSwitcherFlagValue(this.sport.config.name)
    .subscribe((flag: boolean) => { this.isMarketSwitcherConfigured = flag; });
    const eventsDataLoader$: Observable<ISystemConfig> = from(this.sport.getByTab(EventMethods.antepost))
    .pipe(
      concatMap(((matchesEvents: ISportEvent[]) => {
        this.matches = matchesEvents;
        return from(this.sport.getByTab(EventMethods.outrights));
      })),
      concatMap(((outrightEvents: ISportEvent[]) => {
        this.outrights = outrightEvents;
        return this.cmsService.getSystemConfig();
      })));
    this.loadEventsSubscription = eventsDataLoader$.subscribe((systemConfig: ISystemConfig) => {
      if (systemConfig && systemConfig.SportCompetitionsTab && systemConfig.SportCompetitionsTab.eventsLimit) {
        this.eventsLimit = systemConfig.SportCompetitionsTab.eventsLimit;
      }

      this.isSportEventFiltersEnabled = systemConfig.FeatureToggle && systemConfig.FeatureToggle[this.filtersKey];

      let preparedEvents;
      // If matches length 0 then to show outrights events in competitions tab
      if (this.isMarketSwitcherConfigured && this.matches.length) {
        preparedEvents = _.uniq([...this.matches], (event => event.id));
      } else {
        this.loadData = true;
        preparedEvents = _.uniq([...this.matches, ...this.outrights], (event => event.id));
      }
      // not to show see all on desktop
      if (!this.deviceService.isDesktop) {
        preparedEvents = this.prepareEvents(preparedEvents);
      }
      this.eventsBySections = preparedEvents && preparedEvents.length ?
        this.prepareAccordions(this.sportTabsService.eventsBySections(preparedEvents, this.sport)) : [];
      this.eventsBySectionsCopy = [...this.eventsBySections];
      this.displayFilters = this.eventsBySections.length > 0;
      this.isLoaded = true;
      this.isResponseError = false;
      this.updateLoadingState.emit({
        isLoaded: this.isLoaded,
        isResponseError: this.isResponseError,
        eventsBySectionsLength: this.eventsBySections.length
      });
      // // Subscribe LS Updates via PUSH updates! unSubscribe will be automatically invoked on next subscribe!
      this.sport.subscribeLPForUpdates(preparedEvents);
      this.pubSubService.subscribe(this.componentName, this.pubSubService.API.DELETE_EVENT_FROM_CACHE, (eventId: string) => {
        this.sportTabsService.deleteEvent(eventId, this.eventsBySections);
        this.updateLoadingState.emit({
          isLoaded: this.isLoaded,
          isResponseError: this.isResponseError,
          eventsBySectionsLength: this.eventsBySections.length
        });
      });
    }, (error => {
      this.isLoaded = true;
      this.isResponseError = true;
      this.updateLoadingState.emit({
        isLoaded: this.isLoaded,
        isResponseError: this.isResponseError,
        eventsBySectionsLength: 0
      });
      console.warn(`Competitions Data:`, error && error.error || error);
    }));
  }

  ngOnDestroy(): void {
    this.sport.unSubscribeLPForUpdates();
    this.pubSubService.unsubscribe(this.componentName);
    this.loadEventsSubscription && this.loadEventsSubscription.unsubscribe();
    this.marketSwitcherConfigSubscription && this.marketSwitcherConfigSubscription.unsubscribe();
  }

  trackByTypeId(index: number, sportSection: ITypeSegment): string {
    return sportSection.typeId;
  }

  goToCompetition(competitionSection: ITypeSegment): string {
    const competitionPageUrl: string = this.routingHelperService.formCompetitionUrl({
      sport: this.activatedRoute.snapshot.paramMap.get('sport'),
      typeName: competitionSection.typeName,
      className: competitionSection.className
    });

    return competitionPageUrl;
  }

  updateState(state: boolean, section: ITypeSegment): void {
    section.isExpanded = state;
  }

  filterEvents(marketFilter: ILazyComponentOutput): void {
    if (!this.activeMarketFilter || this.activeMarketFilter !== marketFilter.value) {
      this.initMarketSelector(marketFilter.value);
    }
  }

  /**
   * Updates time filter when user clicks on it
   * @param {ILazyComponentOutput} output
   */
  handleCompetitionFilterOutput(output: ILazyComponentOutput): void {
    if (output.output === 'filterChange') {
      this.timeFilter = { ...this.timeFilter, ...output.value as ICompetitionFilter };

      this.filterEventsByCompetitionFilter(this.timeFilter);
    }
  }

  protected initMarketSelector(marketFilter: string): void {
    this.activeMarketFilter = marketFilter;
    this.loadData = true;
    this.isSportEventFiltersEnabled && (this.competitionFiltersService.selectedMarket = marketFilter);
    this.marketSortService.setMarketFilterForMultipleSections(this.eventsBySections, marketFilter);
    this.isSportEventFiltersEnabled && this.marketSortService.setMarketFilterForMultipleSections(this.eventsBySectionsCopy, marketFilter);

    if (this.isSportEventFiltersEnabled) {
      this.filterEventsByCompetitionFilter(this.timeFilter);
    }

    this.eventsBySections = [...this.prepareAccordions(this.eventsBySections)];
  }

  /**
   * Filters current events by selected | deselected league | time filter
   * @param {ICompetitionFilter} time
   * @private
   */
  private filterEventsByCompetitionFilter(time: ICompetitionFilter): void {
    this.eventsBySections = this.prepareAccordions(
      this.competitionFiltersService.filterEvents(null, time, this.eventsBySectionsCopy) as ITypeSegment[]
    );
  }

  private prepareEvents(events: ISportEvent[]): ISportEvent[] {
    const eventsBySection = this.sport.arrangeEventsBySection(events, true);
    return this.getEventsFromSections(this.limitSections(eventsBySection));
  }

  private getEventsFromSections(sections: ITypeSegment[]): ISportEvent[] {
    return _.reduce(sections, (events: ISportEvent[], section: ITypeSegment): ISportEvent[] => _.union(events, section.events), []);
  }

  private limitSections(sections: ITypeSegment[]): ITypeSegment[] {
    _.each(sections, (section: ITypeSegment) => {
      if (section.events.length > this.eventsLimit) {
        section.events.splice(this.eventsLimit);
        this.limitedSections[section.typeId] = true;
      }
    });
    return sections;
  }

  private prepareAccordions(sections: ITypeSegment[]): ITypeSegment[] {
    let j: number = 0;
    _.each(sections, (section: ITypeSegment) => {
      if (!section.deactivated && j < 3) {
        section.isExpanded = true;
        j++;
      } else {
        section.isExpanded = false;
      }
    });
    return sections;
  }

  activeIndex(currIndex): number {
    let activeInd = 0;
    this.eventsBySections.forEach((eventsBySection, index) => {
      if(!eventsBySection.deactivated && index < currIndex) {
        activeInd++;
      }
    })
    return activeInd;
  }
}
