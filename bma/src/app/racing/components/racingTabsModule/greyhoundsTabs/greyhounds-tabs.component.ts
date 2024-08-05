import { Component, Input, OnDestroy, OnInit, OnChanges, SimpleChanges, Output, EventEmitter } from '@angular/core';
import * as _ from 'underscore';

import { RacingGaService } from '@racing/services/racing-ga.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { EventService } from '@sb/services/event/event.service';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { IRaceGridMeeting } from '@core/models/race-grid-meeting.model';
import { Router } from '@angular/router';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CmsService } from '@core/services/cms/cms.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';
import { ISportConfigTab } from '@app/core/services/cms/models';

@Component({
  selector: 'greyhounds-tabs',
  templateUrl: 'greyhounds-tabs.component.html'
})
export class GreyhoundsTabsComponent implements OnDestroy, OnInit, OnChanges {
  @Input() applyingParams: boolean;
  @Input() viewByFilters: string;
  @Input() filter: string;
  @Input() isRacingPanel;
  @Input() tabsTitle: string;
  @Input() sportName: string;
  @Input() racingPath: string;
  @Input() display: string;
  @Input() sportModule: string;
  @Input() responseError?;
  @Input() isRunnersNumber: boolean;
  @Input() racing?: IRaceGridMeeting;
  @Input() racingSpecials?;
  @Input() expanded?;
  @Input() sectionTitle: Object;
  @Input() isFavourite?;
  @Input() definePriceType: Function;
  @Input() goTo: Function;
  @Input() getDay: string;
  @Input() getDate: number;
  @Input() getMonth: string;
  @Input() eventsOrder: string[];
  @Input() categoryId: string;
  @Input() isEventOverlay?: boolean;
  @Output() readonly isLoadedEvent: EventEmitter<boolean> = new EventEmitter();

  limit: number;
  isExpanded: boolean = true;
  isDailyRacingModule: boolean;
  switchers: ISwitcherConfig[];
  orderedEvents: ISportEvent[];
  orderedEventsByTypeNames: ISportEvent[][] = [];
  filteredTypeNames;
  nextRacesWidgetVisible: boolean = true;
  nextRacesLoaded: boolean = true;
  featuredLoaded: boolean = false;

  targetTab: ISportConfigTab;
  lastBannerEnabled:boolean;
  accorditionNumber:number;

  private readonly tagName: string = 'greyhoundsTabsComponent';

  constructor(
    protected router: Router,
    protected filterService: FiltersService,
    protected racingGaService: RacingGaService,
    protected routingHelperService: RoutingHelperService,
    protected eventService: EventService,
    public pubSubService: PubSubService,
    protected cmsServise: CmsService,
    protected gtm: GtmService,
    protected vEPService : VirtualEntryPointsService
  ) {
  }

  /**
   * Check if next races component should be shown
   */
  get displayNextRaces(): boolean {
    return !this.responseError && this.display === 'today';
  }
  set displayNextRaces(value:boolean){}

  get isTodayTomorrow(): boolean {
    return this.display === 'today' || this.display === 'tomorrow';
  }

  set isTodayTomorrow(value: boolean){}

  ngOnInit(): void {
    this.isDailyRacingModule = this.display === 'today' && this.filter === 'by-meeting' && this.sportName === 'greyhound';

    this.switchers = [{
      name: 'sb.byMeetingGH',
      onClick: () => {
        this.goToFilter('by-meeting');
      },
      viewByFilters: 'by-meeting'
    }, {
      name: 'sb.byTimeGH',
      onClick: () => {
        this.goToFilter('by-time');
      },
      viewByFilters: 'by-time'
    }];
    this.filterInitData();
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.SHOW_WIDGET, widget => {
      if (widget && widget.name === 'next-races') {
        this.nextRacesWidgetVisible = widget.data && !!widget.data.length;
      }
    });
    this.handleFutureTabLoaded();

    this.vEPService.targetTab.subscribe((tab: ISportConfigTab | null) => {
      this.targetTab = tab;
    });

    this.vEPService.lastBannerEnabled.subscribe((lbe: boolean) => {
      this.lastBannerEnabled = lbe;
    });
  
    this.vEPService.accorditionNumber.subscribe((accNum: number) => {
      this.accorditionNumber = accNum;
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.viewByFilters) {
      this.filterInitData();
    }
  }

  handleFeaturedLoaded(): void {
    this.featuredLoaded = true;
    this.isLoadedEvent.emit(this.featuredLoaded);
  }

  /**
   * Handles child NextRaces component data loaded
   */
  handleNextRacesLoaded(): void {
    this.nextRacesLoaded = true;
  }

  /**
   * Handles loading of future tab
   */
  handleFutureTabLoaded(): void {
    const FUTURETABNAME: string = 'future';
    if(this.display === FUTURETABNAME && this.racing && this.racing.events.length) {
      this.handleFeaturedLoaded();
    }else if(this.display === FUTURETABNAME && this.racing){
      this.featuredLoaded =true;
    }
  }

  trackModule(module, sport) {
    this.racingGaService.trackModule(module, sport);
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.tagName);
    this.racingGaService.reset();
  }

  filterInitData(): void {
    if (this.racing && !this.isTodayTomorrow) {
      this.orderedEventsByTypeNames = [];
      this.orderedEvents = this.filterService.orderBy(this.racing.events, this.eventsOrder);
      if (this.racing.classesTypeNames) {
        this.filteredTypeNames = _.sortBy(this.racing.classesTypeNames.default, typeName => typeName.name.toString());
        _.each(this.filteredTypeNames, (typeName: { name: string }) => {
          this.orderedEventsByTypeNames.push(_.filter(this.racing.events, (event: ISportEvent) => event.typeName === typeName.name));
        });
      }
    }
  }

  trackById(index, value): number {
    return value.id ? value.id : value.groupFlag;
  }

  /**
   * Go to page filter
   * @param {string} path
   */
  goToFilter(filter: string): void {
    if (this.isEventOverlay) {
      this.filter = filter;
      this.filteredTypeNames.forEach((filterType) => {
        filterType['isExpanded'] = false;
      });
      this.isExpanded = true;
      this.filteredTypeNames[0]['isExpanded'] = true;
      this.gtm.push('trackEvent', {
        eventAction: "meetings",
        eventCategory: "greyhounds",
        eventLabel: filter.split('-').join(" ")
      });
    } else {
      this.routingHelperService.formSportUrl(this.racingPath, `${this.display}/${filter}`).subscribe((url: string) => {
        if (url !== this.router.url) {
          setTimeout(() => this.router.navigateByUrl(url));
        }
      });
    }
  }

  /**
   * Shows or hides 'no events' block
   * @param {boolean} display
   * @param {Object} responseError
   * @param {Object | Array}racing {object/array}
   * @return {boolean}
   */
  showNoEvents(display: string, responseError: Object, racing: any): boolean {
    return !responseError && ((display === 'yourcall' && !racing.length) || (racing.events && !racing.events.length));
  }

  reloadComponent(): void {
    this.ngOnDestroy();
    this.ngOnInit();
  }
}
