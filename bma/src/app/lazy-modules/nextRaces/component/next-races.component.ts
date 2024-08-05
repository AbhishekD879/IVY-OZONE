import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import * as _ from 'underscore';
import { from, Subscription } from 'rxjs';
import { concatMap } from 'rxjs/operators';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { Location } from '@angular/common';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { EventService } from '@sb/services/event/event.service';
import { ICombinedRacingConfig, ISystemConfig } from '@core/services/cms/models/system-config';
import { ISportEvent } from '@core/models/sport-event.model';
import { CommandService } from '@core/services/communication/command/command.service';
import { NextRacesService } from '@core/services/racing/nextRaces/next-races.service';
import { RacingGaService } from '@racing/services/racing-ga.service';
import { RacingPostService } from '@core/services/racing/racingPost/racing-post.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { ISportConfigTab } from '@app/core/services/cms/models/sport-config-tab.model';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';
import { HorseracingService } from '@core/services/racing/horseracing/horseracing.service';
import { GreyhoundService } from '@app/core/services/racing/greyhound/greyhound.service';
import { RoutingState } from '@app/shared/services/routingState/routing-state.service';

@Component({
  selector: 'next-races-module',
  templateUrl: 'next-races.component.html'
})
export class NextRacesModuleComponent implements OnInit, OnDestroy {
  @Input() moduleType: string;
  @Input() moduleAllLink: boolean;
  @Input() fluid: boolean;
  @Input() showLoader: boolean;
  @Input() widget: boolean;
  @Input() trackGa: boolean;
  @Input() trackGaDesktop: boolean;
  @Input() headerVisible: boolean;
  @Input() raceIndex: number | string = 'next-races';
  @Input() hostContext: string = 'next-races';
  @Input() isRacingFeatured?:boolean;
  @Input() sportName?: string;
  @Input() compName: string = '';
  @Input() isLadsSideWidget: boolean = false;

  @Input() hideLoader: boolean = false;
  @Output() readonly eventsLoaded: EventEmitter<void> = new EventEmitter();
  @Input() isEventOverlay?:boolean;

  /** @member {boolean} */
  isExpanded: boolean = true;

  /** @member {object} config return from nextRacesfactory */
  nextRacesModule;

  /** @member {number} number to show amount of selection in one row */
  numberOfSelections: number = 3; // default value

  /** @member {String} Module title */
  moduleTitle: string = '';

  /** that represent connect callback for page reload on SS Error */
  raceModule: string;

  /** @member {boolean} */
  ssDown: boolean = false;

  /** @member {boolean} */
  className: string;

  /** @member {boolean} */
  showTimer: boolean;

  showBriefHeader: boolean = true;

  // Show More Link
  raceEvent: string;

  leftTitleText: string;

  headerClass: string;

  showMoreLink: {link: string; title: string};

  private subscriptionId: string = '';
  private loadDataSubscription: Subscription;
  lastSuspendedEventTime: Date;
  bannerBeforeAccorditionHeader :string = '';
  targetTab: ISportConfigTab | null = null;
  selectedFilter :any = "All";
  nextRacesGroupedData: any = {};
  filterAccess: any;
  showFilter:boolean;
  channel_number :any
  isNxtTabEnabled = false;
  constructor(
    protected pubSubService: PubSubService,
    protected cmsService: CmsService,
    protected location: Location,
    protected routingHelperService: RoutingHelperService,
    protected nextRacesService: NextRacesService,
    protected eventService: EventService,
    protected commandService: CommandService,
    protected racingPostService: RacingPostService,
    protected windowRefService: WindowRefService,
    public horseRacingService: HorseracingService,
    public greyhoundService: GreyhoundService,
    public routingState: RoutingState,
    protected vEPService : VirtualEntryPointsService
  ) { }
  get racingService(): HorseracingService | GreyhoundService {
    const segment = this.routingState.getCurrentSegment();
    return segment.indexOf("horseracing") >= 0 ? this.horseRacingService : this.greyhoundService;
  }
  set racingService(_value: HorseracingService | GreyhoundService) {}


  // Module Name
  get MODULE_NAME(): string {
    return `MODULE_${this.raceModule}`;
  }
  set MODULE_NAME(value:string){}

  trackCollapse(isCollapsed?: boolean): void {
    this.commandService.executeAsync(this.commandService.API.RACING_GA_SERVICE).then((racingGaService: RacingGaService) => {
      if (this.trackGaDesktop && !racingGaService.flag[racingGaService.CONST.WIDGET]) {
        const eventCategory = this.location.path() === '/' ? 'home' : 'widget';
        racingGaService.sendGTM('collapse', eventCategory);
        racingGaService.flag[racingGaService.CONST.WIDGET] = true;
      }

      if (this.trackGa && !this.trackGaDesktop) {
        racingGaService.trackNextRacesCollapse(this.moduleType);
      }
    });
    if (isCollapsed === false) {
      this.selectedFilter = 'All';
      this.onFilterChange({ value: { flag: 'All', data: this.nextRacesModule.storedEvents } });
    }
  }

  /**
   * Init function for(callbacks, watchers, scope destroying)
   * @private
   */
  ngOnInit(): void {
    this.raceModule = this.widget ? 'W_NEXT_RACE' : 'NEXT_RACE';
    this.showLoader = true;
    this.cmsService.triggerSystemConfigUpdate();
    this.registerEvents();
    this.getCmsConfigs();
    this.className = `${this.hostContext} next-races-${this.moduleType}`;
    this.showTimer = this.moduleType === 'horseracing';
    this.raceEvent = this.moduleType === 'horseracing' ? 'Horse Racing' : 'Greyhounds';

    this.routingHelperService.formSportUrl(this.moduleType).subscribe((url: string) => {
      this.showMoreLink = {
        link: url,
        title: `View All ${this.raceEvent} Events`
      };
    });

    this.headerClass = !this.widget || this.headerVisible ? 'secondary-header' : '';

    // show brief header by default
    this.showBriefHeader = this.hostContext === 'next-races';

    this.windowRefService.document.addEventListener('LIVE_SERVE_UPDATE', (data: CustomEvent) => {
      const update = data.detail.liveUpdate;
      if (update.channel_type == "sEVENT" && update.payload.status == "S") {
        let storedEventsData = this.nextRacesModule.storedEvents && [...this.nextRacesModule.storedEvents];
        if (storedEventsData && storedEventsData.length) {
          const index = storedEventsData.findIndex(res => res.id == update.channel_number);// channel_number is eventId
          if (index > -1) {
            const eventLocalTime = new Date(storedEventsData[index].startTime);
            this.lastSuspendedEventTime = eventLocalTime;
            storedEventsData = storedEventsData.filter(res => new Date(res.startTime) > eventLocalTime);
            this.nextRacesModule.storedEvents = storedEventsData;
            if( !this.isEventOverlay || !storedEventsData.length) {
              this.getNextEvents(false);
            } 
          }
        } else {
          this.getNextEvents();
        }
      }
    });

    this.vEPService.bannerBeforeAccorditionHeader.subscribe((header: string) => {
      this.bannerBeforeAccorditionHeader = header;
    });

    this.vEPService.targetTab.subscribe((tab: ISportConfigTab | null) => {
      this.targetTab = tab;
    });

  }

  ngOnDestroy(): void {
    this.unsubscribeFromUpdates();
    this.pubSubService.unsubscribe(this.MODULE_NAME);
  }

  /**
   * Get data from Cms config
   */
  getCmsConfigs(): void {
    let previousConfig: ICombinedRacingConfig;

    this.pubSubService.subscribe(this.MODULE_NAME, this.pubSubService.API.SYSTEM_CONFIG_UPDATED, (data: ISystemConfig) => {
      this.showFilter = false;
      if (this.moduleType === 'horseracing') {
        this.filterAccess = data.NextRacesFiltersHorseRacing || {};
      } else if (this.moduleType !== 'horseracing') {
        this.filterAccess = data.NextRacesFiltersGreyHounds || {};
        this.isNxtTabEnabled = data.GreyhoundNextRacesToggle && data.GreyhoundNextRacesToggle.nextRacesTabEnabled;
      }
     this.showFilter = this.filterAccess['EnableFilters'] || false;
      const currentConfig: ICombinedRacingConfig = {
        RacingDataHub: data.RacingDataHub,
        NextRaces: data.NextRaces,
        GreyhoundNextRaces: data.GreyhoundNextRaces
      };
      if (currentConfig.NextRaces && !_.isEqual(previousConfig, currentConfig)) {
        previousConfig = currentConfig;
        this.moduleTitle = currentConfig.NextRaces.title;
        this.numberOfSelections = parseInt(currentConfig.NextRaces.numberOfSelections, 10) || this.numberOfSelections;
        this.nextRacesModule = this.nextRacesService.getNextRacesModuleConfig(this.moduleType, currentConfig);
        this.leftTitleText = this.headerVisible || !this.widget ? this.moduleTitle : '';
        this.getNextEvents();
      } else {
        this.eventsLoaded.emit();
      }
    });
  }

  /**
   * tracking for vial link on home page
   */
  sendToGTM(): void {
    this.commandService.executeAsync(this.commandService.API.RACING_GA_SERVICE).then((racingGaService: RacingGaService) => {
      racingGaService.sendGTM('view all', 'home');
    });
  }

  /**
   * Get Next Races Events
   */
  getNextEvents(displayLoader : boolean = true ): void {
    this.unsubscribeFromUpdates();

    this.showLoader = displayLoader;
    this.loadDataSubscription = from(this.eventService.getNextEvents(this.nextRacesModule, this.nextRacesService.cacheKey, this.isEventOverlay))
      .pipe(concatMap((eventsData: ISportEvent[]) =>
        this.racingPostService.updateRacingEventsList(eventsData, this.moduleType === 'horseracing')
      ))
      .subscribe((data: ISportEvent[]) => {
        let eventsData = this.nextRacesService.getUpdatedEvents(data, this.moduleType);
        eventsData = this.lastSuspendedEventTime ?  eventsData.filter(res => new Date(res.startTime) > this.lastSuspendedEventTime) : eventsData;
        _.extend(this.nextRacesModule, {storedEvents: eventsData});
        _.extend(this.nextRacesGroupedData, {storedEvents: eventsData});
        this.groupDataByFlags();
        this.showLoader = false;
        if (this.widget) {
          this.pubSubService.publish(this.pubSubService.API.SHOW_WIDGET, {
            name: 'next-races',
            data: this.nextRacesModule.storedEvents
          });
        }
        if(this.isEventOverlay) {
          this.eventsLoaded.emit();
        }
        // Subscription from liveServe PUSH updates
        this.subscriptionId = this.nextRacesService.subscribeForUpdates(this.nextRacesModule.storedEvents);
      }, () => {
        this.showLoader = false;
        this.ssDown = true;
        this.eventsLoaded.emit();
      }, () => {
        this.eventsLoaded.emit();
      });
  }
  public groupDataByFlags(): void {
    this.nextRacesGroupedData = { ...this.nextRacesModule };
    if (this.nextRacesModule && this.nextRacesModule.storedEvents && this.showFilter) {
        let hasSelected = [];
        this.nextRacesGroupedData = this.racingService.getNextRacesData(this.filterAccess, this.nextRacesModule);
        hasSelected = this.nextRacesGroupedData.groupedRacing.filter((data: any) => data.flag === this.selectedFilter);
      if (hasSelected.length && hasSelected[0].data) {
        this.nextRacesGroupedData.storedEvents = [...hasSelected[0].data];
      } else {
        this.selectedFilter = 'All';
        this.nextRacesGroupedData.storedEvents = [...this.nextRacesModule.storedEvents];
      }
    }
  }
 
   onFilterChange(filter: any) {
    if (filter.value) {
      this.selectedFilter = filter.value.flag;
      this.nextRacesGroupedData['storedEvents'] = [...filter.value.data];
    }
  }
  /**
   * Reload current directive
   */
  reloadComponent(): void {
    this.ssDown = false;
    this.getNextEvents();
  }

  /**
   * Sync events
   */
  registerEvents(): void {
    this.pubSubService.subscribe(this.MODULE_NAME, this.pubSubService.API.RELOAD_COMPONENTS, () => this.getCmsConfigs());
  }

  private unsubscribeFromUpdates(): void {
    // unSubscription from liveServe PUSH updates
    this.nextRacesService.unSubscribeForUpdates(this.subscriptionId);
    if (this.loadDataSubscription) {
      this.loadDataSubscription.unsubscribe();
    }
  }


  isDisplayBanner(name) {
    return this.bannerBeforeAccorditionHeader?.toLowerCase() === name?.toLowerCase();
  }

}
