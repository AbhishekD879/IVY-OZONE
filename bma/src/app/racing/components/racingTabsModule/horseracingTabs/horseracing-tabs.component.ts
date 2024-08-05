import { Router } from '@angular/router';
import {
  Component,
  Input,
  OnDestroy,
  OnInit, Output, EventEmitter
} from '@angular/core';
import * as _ from 'underscore';

import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { EventService } from '@sb/services/event/event.service';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';
import { IRaceGridMeeting  } from '@core/models/race-grid-meeting.model';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';
import { ISportConfigTab } from '@app/core/services/cms/models';

@Component({
  selector: 'horseracing-tabs',
  templateUrl: 'horseracing-tabs.component.html'
})
export class HorseracingTabsComponent implements OnDestroy, OnInit {
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
  @Input() racing?;
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
  @Input() isFromOverlay?: boolean;
  @Output() readonly isLoadedEvent: EventEmitter<boolean> = new EventEmitter();

  switchers: ISwitcherConfig[];
  isExtraPlaceAvailable: boolean = false;
  offersAndFeaturedRacesTitle: string;
  nextRacesComponentEnabled: boolean = false;
  defaultAntepostTab: string;
  nextRacesLoaded: boolean = false;
  featuredLoaded: boolean = false;

  targetTab: ISportConfigTab;
  lastBannerEnabled:boolean;
  accorditionNumber:number;

  /**
   * Checks whether next-races component should be displayed
   */
  get displayNextRaces(): boolean {
    return !this.responseError && this.display === 'featured' && this.nextRacesComponentEnabled;
  }
  set displayNextRaces(value:boolean){}

  constructor(
    private router: Router,
    private routingHelperService: RoutingHelperService,
    private eventService: EventService,
    public cmsService: CmsService,
    protected vEPService : VirtualEntryPointsService
  ) {
  }

  ngOnInit(): void {
    this.switchers = [{
      name: 'sb.byMeeting',
      onClick: () => {
        this.goToFilter('by-meeting');
      },
      viewByFilters: 'by-meeting'
    }, {
      name: 'sb.byTime',
      onClick: () => {
        this.goToFilter('by-time');
      },
      viewByFilters: 'by-time'
    }];

    this.cmsService.getSystemConfig()
      .subscribe((config: ISystemConfig) => {
        if (config.featuredRaces && config.featuredRaces.enabled) {
          this.isExtraPlaceAvailable = true;
          this.offersAndFeaturedRacesTitle = config.featuredRaces.title;
        }

        this.nextRacesComponentEnabled = config && config.NextRacesToggle
          && config.NextRacesToggle.nextRacesComponentEnabled === true;
        this.defaultAntepostTab = config && config.defaultAntepostTab && config.defaultAntepostTab.tabName;
      });

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
  /**
   * Handle racing featured  data loaded
   */
  handleFeaturedLoaded(racing?: IRaceGridMeeting): void {
    this.featuredLoaded = true;
    this.racing = racing;
    this.isLoadedEvent.emit(this.featuredLoaded);
  }

  /**
   * Handle child next-races component data loaded
   */
  handleNextRacesLoaded(): void {
    this.nextRacesLoaded = true;
  }

  onFeaturedEvents(event: {output: string, value: any}): void {
    switch (event.output) {
      case 'nextRacesLoaded':
        this.handleNextRacesLoaded();
        break;
      case 'featuredLoaded':
        this.handleFeaturedLoaded(event.value);
        break;
      default:
        break;
    }
  }

  ngOnDestroy(): void {}

  trackByFlag(index: number, value: {flag: string}): string {
    return value.flag;
  }

  checkCacheOut(events: ISportEvent[], typeName: string): boolean {
    const filteredEvents = _.filter(events, (event: ISportEvent) => event.typeName === typeName);

    return this.eventService.isAnyCashoutAvailable(filteredEvents, [{ cashoutAvail: 'Y' }]);
  }

  /**
   * Go to page filter
   * @param {string} path
   */
  goToFilter(filter: string): void {
    this.routingHelperService.formSportUrl(this.racingPath, `${this.display}/${filter}`).subscribe((url: string) => {
      if (url !== this.router.url) {
        setTimeout(() => this.router.navigateByUrl(url));
      }
    });
  }

  /**
   * Shows or hides 'no events' block
   * @param display {boolean}
   * @param responseError {object}
   * @param racing {object/array}
   * @return {boolean}
   */
  showNoEvents (display: string, responseError: Object, racing: any): boolean {
    return !responseError && ((display === 'yourcall' && !racing.length) || (racing.events && !racing.events.length));
  }

  reloadComponent(): void {
    this.ngOnDestroy();
    this.ngOnInit();
  }
}
