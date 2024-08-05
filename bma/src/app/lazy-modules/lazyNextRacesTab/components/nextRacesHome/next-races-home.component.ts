import { Component, Input, OnDestroy, OnInit, Output, EventEmitter } from '@angular/core';
import * as _ from 'underscore';
import { Subscription, from } from 'rxjs';
import { concatMap } from 'rxjs/operators';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { NextRacesHomeService } from '@lazy-modules-module/lazyNextRacesTab/components/nextRacesHome/next-races-home.service';
import { EventService } from '@sb/services/event/event.service';
import { ICombinedRacingConfig, ISystemConfig } from '@core/services/cms/models/system-config';
import { ISportEvent } from '@core/models/sport-event.model';
import { RacingPostService } from '@core/services/racing/racingPost/racing-post.service';
import { UpdateEventService } from '@core/services/updateEvent/update-event.service';
import environment from '@environment/oxygenEnvConfig';
import { DeviceService } from '@core/services/device/device.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { Router } from '@angular/router';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service'; 
import { GreyhoundService } from '@coreModule/services/racing/greyhound/greyhound.service'; 
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'next-races-home',
  templateUrl: 'next-races-home.component.html'
})
export class NextRacesHomeComponent implements OnInit, OnDestroy {
  @Input() moduleType: string;
  @Input() moduleAllLink: boolean;
  @Input() maxSelections?: number;
  @Input() trackGa?: boolean;
  @Input() compName: string;
  @Output() readonly dataLoaded: EventEmitter<boolean> = new EventEmitter<boolean>();
  showLoader: boolean =  true;

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

  // Show More Link
  raceEvent: string;

  leftTitleText: string;

  headerClass: string;

  private subscribedChannelsId: string = '';

  nextRacesGroupedData: any = {};

  selectedFilter :any = "All";

  filterAccess: any;
  
  showFilter = false;

  isNxtTabEnabled = false;

  private eventsSubscription: Subscription;
  protected schemaUrl : string;
  private readonly LADBROKES: string = 'ladbrokes';
  protected readonly GREYHOUNDS: string = 'Greyhounds';
  lastSuspendedEventTime: Date;

  constructor(
    public pubSubService: PubSubService,
    public cmsService: CmsService,
    public nextRacesHomeService: NextRacesHomeService,
    public eventService: EventService,
    public racingPostService: RacingPostService,
    protected deviceService: DeviceService,
    protected routingHelperService: RoutingHelperService,
    protected router: Router,
    // eslint-disable-next-line
    protected updateEventService: UpdateEventService, // for events subscription (done in service init)
    public horseRacingService: HorseracingService,
    public greyhoundService: GreyhoundService,
    public routingState: RoutingState,
    protected windowRefService: WindowRefService) {
  }
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
  /**
   * Init function for(callbacks, watchers, scope destroying)
   * @private
   */
  ngOnInit(): void {
    this.raceModule = 'NEXT_RACE';
    this.cmsService.triggerSystemConfigUpdate();
    this.registerEvents();
    this.getCmsConfigs();
    this.className = `next-races-${this.moduleType}`;
    this.showTimer = this.moduleType === 'horseracing';
    this.raceEvent = this.moduleType === 'horseracing' ? 'Horse Racing' : 'Greyhounds';
    this.windowRefService.document.addEventListener('LIVE_SERVE_UPDATE', (data: CustomEvent) => {
      const update = data.detail.liveUpdate;
      if (update.channel_type == "sEVENT" && update.payload.status == "S") {
        let storedEventsData = this.nextRacesModule.storedEvents && [...this.nextRacesModule.storedEvents];
        storedEventsData = storedEventsData || [];
        const index = storedEventsData.findIndex(res => res.id == update.channel_number);// channel_number is eventId
        if (storedEventsData && storedEventsData.length && index > -1) {
            const eventLocalTime = new Date(storedEventsData[index].startTime);
            this.lastSuspendedEventTime = eventLocalTime;
            storedEventsData = storedEventsData.filter(res => new Date(res.startTime) > eventLocalTime);
            this.nextRacesModule.storedEvents = storedEventsData;
            if( !storedEventsData.length) {
              this.getNextEvents(false);
            } 
        } else {
          this.getNextEvents(false);
        }
      }
    });
  }

  ngOnDestroy(): void {
    // unSubscribe LS Updates via PUSH
    this.nextRacesHomeService.unSubscribeForUpdates(this.subscribedChannelsId);
    this.pubSubService.unsubscribe(this.MODULE_NAME);
    this.eventsSubscription && this.eventsSubscription.unsubscribe();
    this.removeSchemaForGHNextRaces(); 
    
  }

  /**
   * Get data from Cms config
   */
  getCmsConfigs(): void {
    let storedConfig: ICombinedRacingConfig;

    this.pubSubService.subscribe(this.MODULE_NAME, this.pubSubService.API.SYSTEM_CONFIG_UPDATED, (data: ISystemConfig) => {
      this.showFilter = false;
      if (this.moduleType === 'horseracing') {
        this.filterAccess = data.NextRacesFiltersHorseRacing || {};
      } else if (this.moduleType !== 'horseracing') {
        this.filterAccess = data.NextRacesFiltersGreyHounds || {};
        this.isNxtTabEnabled = data.GreyhoundNextRacesToggle && data.GreyhoundNextRacesToggle.nextRacesTabEnabled;
      }
     this.showFilter = this.filterAccess['EnableFilters'] || false;
      const updatedConfig: ICombinedRacingConfig = {
        RacingDataHub: data.RacingDataHub,
        NextRaces: data.NextRaces,
        GreyhoundNextRaces: data.GreyhoundNextRaces
      };

      if (updatedConfig.NextRaces && !_.isEqual(updatedConfig, storedConfig)) {
        storedConfig = updatedConfig;
        this.moduleTitle = updatedConfig.NextRaces.title;
        // All nextRacesModule configuration
        this.nextRacesModule = this.nextRacesHomeService.getNextRacesModuleConfig(this.moduleType, updatedConfig);
        this.leftTitleText = this.moduleTitle;
        this.getNextEvents();
      }
    });
  }

  /**
   * tracking for vial link on home page
   */
  sendToGTM(): void {
    this.nextRacesHomeService.sendGTM('view all', 'home');
  }

  /**
   * Get Next Races Events
   */
  getNextEvents(showLoader: boolean = true): void {
    
    this.showLoader = showLoader;
    // unSubscribe LS Updates via PUSH
    this.nextRacesHomeService.unSubscribeForUpdates(this.subscribedChannelsId);
    this.eventsSubscription && this.eventsSubscription.unsubscribe();
    this.eventsSubscription = from(this.eventService.getNextEvents(this.nextRacesModule))
      .pipe(
        concatMap((eventsData: ISportEvent[]) => {
          return this.racingPostService.updateRacingEventsList(eventsData, this.moduleType === 'horseracing');
        })
      ).subscribe((eventsData: ISportEvent[]) => {
        let tempEventsData = this.nextRacesHomeService.getUpdatedEvents(eventsData, this.moduleType);
        tempEventsData = this.lastSuspendedEventTime ?  tempEventsData.filter(res => new Date(res.startTime) > this.lastSuspendedEventTime) : eventsData;
        _.extend(this.nextRacesModule, {storedEvents: tempEventsData});
        this.groupDataByFlags();
        // subscribe LS Updates via PUSH
        this.subscribedChannelsId = this.nextRacesHomeService.subscribeForUpdates(this.nextRacesModule.storedEvents);
        this.dataLoaded.emit(true);
        this.showLoader = false;
        this.deviceService.isRobot() && this.nextRacesModule && this.pubSubService.publish(this.pubSubService.API.NEXT_RACES_DATA,[this.nextRacesModule.storedEvents]);
      }, () => {
        this.dataLoaded.emit(true);
        this.showLoader = false;
        console.warn('Error while getting next events');
      });
  }

  /**
   * Sync events
   */
  registerEvents(): void {
    this.pubSubService.subscribe(this.MODULE_NAME, this.pubSubService.API.RELOAD_COMPONENTS, () => this.getCmsConfigs());
  }
  
  /**
  * to remove the schemaScript
  */
  private removeSchemaForGHNextRaces(): void {
    this.deviceService.isRobot() && this.raceEvent === this.GREYHOUNDS && environment.brand === this.LADBROKES && this.schemaUrl && this.pubSubService.publish(this.pubSubService.API.SCHEMA_DATA_REMOVED, this.schemaUrl);
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
  
}
