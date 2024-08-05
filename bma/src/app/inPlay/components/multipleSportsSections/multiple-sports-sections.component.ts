import { map } from 'rxjs/operators';
import { Component, Input, OnChanges, OnDestroy, OnInit, SimpleChanges, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { forkJoin as observableForkJoin, Observable } from 'rxjs';
import * as _ from 'underscore';
import { InplayMainService } from '@inplayModule/services/inplayMain/inplay-main.service';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { ISportTracking } from '@app/inPlay/models/sport-tracking.model';
import { IInplayConnectionState } from '@app/inPlay/models/connection.model';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { StickyVirtualScrollerService } from '@app/shared/components/stickyVirtualScroller/sticky-virtual-scroller.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { GamingService } from '@core/services/sport/gaming.service';
import { inplayConfig } from '@app/inPlay/constants/config';
import { EVENTS } from '@core/constants/websocket-events.constant';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'multiple-sports-sections',
  templateUrl: 'multiple-sports-sections.component.html',
  styleUrls: ['./multiple-sports-sections.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  providers: [StickyVirtualScrollerService]
})
export class MultipleSportsSectionsComponent implements OnInit, OnDestroy, OnChanges {
  @Input() eventsByGroups: any;
  @Input() viewByFilters: string[];
  @Input() showExpanded: boolean;
  @Input() expandedSportsCount: number;
  @Input() expandedLeaguesCount: number;
  @Input() ssError: boolean;
  @Input() isWatchLive: boolean = false;

  limit: number;
  moduleName: string = 'sports-tab';
  isExpanded: boolean = false;
  switchers: ISwitcherConfig[];
  isDataReady: boolean = false;
  isVirtualScrollEnabled: boolean;
  contentReady: boolean = false;
  skeletonShow: { [key: string]: Array<boolean> } = {};
  /**
   * Identifier of expand/collapse state.
   * @type {string}
   */
  expandedKey: string = 'expanded-sports-tab';
  readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;

  constructor(
    private stickyVirtualScrollerService: StickyVirtualScrollerService,
    private inPlayMainService: InplayMainService,
    private inPlayConnectionService: InplayConnectionService,
    private routingHelperService: RoutingHelperService,
    private cmsService: CmsService,
    private awsService: AWSFirehoseService,
    private pubsubService: PubSubService,
    private changeDetectorRef: ChangeDetectorRef
  ) {
  }

  ngOnInit(): void {
    this.cmsService.getSystemConfig().subscribe(systemConfig => {
      this.isVirtualScrollEnabled = systemConfig && systemConfig.VirtualScrollConfig && systemConfig.VirtualScrollConfig.enabled;
      this.initAccordions();
    });

    this.pubsubService.subscribe(this.moduleName, `${inplayConfig.moduleName}.${EVENTS.SOCKET_RECONNECT_ERROR}`, () => {
      this.awsService.addAction('inplay=>UI_Message=>Unavailable=>wsError');
    });

    if (this.ssError) {
      this.awsService.addAction('inplay=>UI_Message=>Unavailable=>ssError');
    }
    this.viewByFilters.forEach((x: string) => {
      this.skeletonShow[x] = [];
    });

    this.pubsubService.subscribe(
      `EVENT_BY_SPORTS_SUBSCRIBE`,
      `${this.pubsubService.API.EVENT_BY_SPORTS_CHANNEL}_MULTIPLE`,
      (data: { [key: string]: ISportSegment }) => {
        this.eventsByGroups = data;
        this.changeDetectorRef.detectChanges();
      }
    );
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.eventsByGroups && !changes.eventsByGroups.isFirstChange() && !this.isDataReady) {
      this.initAccordions();
    }

    // Track UI Message Service is unavailable
    if (changes.ssError && changes.ssError.currentValue) {
      this.awsService.addAction('inplay=>UI_Message=>Unavailable=>ssError');
    }
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe(this.moduleName);
    this.pubsubService.unsubscribe(`EVENT_BY_SPORTS_SUBSCRIBE`);
    this.stickyVirtualScrollerService.destroyEvents();
  }

  /**
   * Error on Web Sockets connection
   * @type {object}
   */
  get wsError(): IInplayConnectionState {
    return this.inPlayConnectionService.status;
  }
  set wsError(value:IInplayConnectionState){}
  get isErrorState(): boolean {
    return this.ssError || this.wsError.reconnectFailed;
  }
  set isErrorState(value:boolean){}
  goToSportCompetitionsPage(eventsBySports: ISportSegment): string {
    return this.routingHelperService.formSportCompetitionsUrl(eventsBySports.sportUri);
  }

  /**
   * Check if sport events is present and show no events section
   * @param {String} filter
   */
  showNoEventsSection(filter: string): boolean {
    if (!this.ssError && this.eventsByGroups[filter]) {
      return !this.eventsByGroups[filter].eventsIds.length;
    }
    return false;
  }

  /**
   * Toggle expand/collapse state of sport section.
   * @param {Object} sportSection
   */
  toggleSport(isExpanded: boolean, sportSection: ISportSegment, filter: string, index: number): void {
    const categoryId = parseInt(sportSection.categoryId, 10);
    sportSection[this.expandedKey] = isExpanded;
    this.skeletonShow[filter][index] = true;
    this.changeDetectorRef.detectChanges();
    if (sportSection[this.expandedKey]) {
      this.getSportData(categoryId, filter, this.inPlayMainService.getSportName(sportSection)).subscribe(() => {
        // if use expand and collapse section, after getting data we will check section again
        // unsubscribe if section was collapsed
        if (sportSection[this.expandedKey] === false) {
          this.inPlayMainService.unsubscribeForSportCompetitionUpdates(sportSection);
          this.inPlayMainService.unsubscribeForEventsUpdates(sportSection);
        }
        this.pubsubService.publish(this.pubsubService.API.INPLAY_DATA_RELOADED);
        this.stickyVirtualScrollerService.updateScrollVisibility();
        this.skeletonShow[filter][index] = false;
        this.changeDetectorRef.detectChanges();
      }, (error) => {
        console.warn(error);
        this.skeletonShow[filter][index] = false;
      });
    } else {
      this.inPlayMainService.unsubscribeForSportCompetitionUpdates(sportSection);
      this.inPlayMainService.unsubscribeForEventsUpdates(sportSection);
      this.stickyVirtualScrollerService.updateScrollVisibility();
      this.changeDetectorRef.detectChanges();
    }
  }

  /**
   * Returns unique key for sport category in current filter view.
   * @param {number} options.categoryId
   * @param {string} options.topLevelType
   * @return {string}
   */
  getSportTrackingId(index: number, eventsBySports: ISportTracking): string {
    const categoryId = eventsBySports.categoryId;
    const topLevelType = eventsBySports.topLevelType;

    return `${categoryId}-${topLevelType}`;
  }

  isLiveNowFilter(filter: string): boolean {
    return filter === 'livenow';
  }

  isUpcomingFilter(filter: string): boolean {
    return filter === 'upcomingLiveStream' || filter === 'upcoming';
  }

  trackById(index: number, filter: string) {
    return `${index}_${filter}`;
  }

  reloadComponent(): void {
    this.ssError = false;
    this.ngOnDestroy();
    this.ngOnInit();
  }

  getNoEventsMessage(filter: string): string {
    return ['livenow', 'liveStream'].includes(filter) ? 'inplay.noLiveEventsFound' : 'inplay.noUpcomingEventsFound';
  }

  /**
   * is sport section expanded
   * @param {number} index
   * @private
   */
  private shouldSportBeExpanded(index): boolean {
    return index < this.expandedSportsCount;
  }

  /**
   * Sets view filter.
   * @param {string} newFilter
   * @private
   */
  private initAccordions(): void {
    if (this.eventsByGroups && this.eventsByGroups[this.viewByFilters[0]]) {
      _.each(this.eventsByGroups[this.viewByFilters[0]].eventsBySports, (sportSection: ISportSegment, index) => {
        const sportId = parseInt(sportSection.categoryId, 10);

        sportSection[this.expandedKey] = this.shouldSportBeExpanded(index);
        sportSection.initiallyExpanded = sportSection[this.expandedKey];

        if (sportSection[this.expandedKey]) {
          this.getSportData(sportId, this.viewByFilters[0], this.inPlayMainService.getSportName(sportSection)).subscribe(() => {},
            (error) => {
              console.warn(error);
            }, () => {
              this.handleEventsLoaded();
              this.skeletonShow[this.viewByFilters[0]][index] = false;
            });
        }
      });

      this.isDataReady = true;
    }
    this.handleEventsLoaded();
  }

  /**
   * Updates content ready state when child component data loaded
   */
  private handleEventsLoaded(): void {
    if (this.eventsByGroups && this.eventsByGroups[this.viewByFilters[0]]) {
      this.contentReady = (this.eventsByGroups[this.viewByFilters[0]].eventsBySports || [])
        .every(sportSection => sportSection.initiallyExpanded ? sportSection.eventsLoaded : true);
    } else {
      this.contentReady =  false;
    }
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Apply single sport data
   * @param {ISportSegment} sportSection
   * @param {number} id
   * @private
   */
  private applySingleSportData(sportSection: ISportSegment, id: number, filter: string,
    sportInstance: GamingService | {}): void {
    const sportDataIsPresent = _.has(sportSection, 'eventsByTypeName') && sportSection.eventsByTypeName.length;
    const eventsByGroup = this.eventsByGroups[filter];
    const sportIndex = this.inPlayMainService.getLevelIndex(eventsByGroup.eventsBySports, 'categoryId', id);

    if (sportDataIsPresent) {
      const sportSectionToUpdate = eventsByGroup.eventsBySports[sportIndex];
      // data is present
      if (sportSectionToUpdate) {
        // Update ids list for in-play group: "livenow" or "upcoming"
        eventsByGroup.eventsIds = _.union(eventsByGroup.eventsIds, sportSection.eventsIds);
        this.inPlayMainService.extendSectionWithSportInstance(sportSectionToUpdate, sportInstance);
        sportSectionToUpdate.eventsIds = sportSection.eventsIds;
        sportSectionToUpdate.eventsByTypeName = sportSection.eventsByTypeName;
        sportSectionToUpdate.eventsLoaded = true;
        this.changeDetectorRef.detectChanges();
      }
    } else {
      // no data were received
      eventsByGroup.eventsBySports.splice(sportIndex, 1);
    }
  }

  /**
   * Get data by sport
   * @param {number} categoryId
   * @return {Observable<ISportSegment>}
   * @private
   */
  private getSportData(categoryId: number, filter: string, sportName: string): Observable<ISportSegment> {
    return observableForkJoin(
      this.inPlayMainService.getSportData({
        categoryId,
        isLiveNowType: this.isLiveNowFilter(filter),
        topLevelType: this.inPlayMainService.getTopLevelTypeParameter(filter)
      }, false, !this.isVirtualScrollEnabled, true, categoryId === +this.HORSE_RACING_CATEGORY_ID),
      this.inPlayMainService.getSportConfigSafe(sportName)
    ).pipe(
      map((data: [ISportSegment, GamingService | {}]) => {
        const sportSegment = data[0],
          sportInstance = data[1];
        // error handling
        if (!sportSegment || _.isEmpty(sportSegment) || _.has(sportSegment, 'error')) {
          this.inPlayConnectionService.setConnectionErrorState(true);
          return;
        }
        this.applySingleSportData(sportSegment, categoryId, filter, sportInstance);

        return sportSegment;
      }));
  }
}
