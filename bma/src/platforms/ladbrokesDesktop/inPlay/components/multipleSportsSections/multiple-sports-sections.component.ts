import { map, takeUntil } from 'rxjs/operators';
import { Component, Input, OnChanges, OnDestroy, OnInit, SimpleChanges, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { InplayMainService } from '@ladbrokesDesktop/inPlay/services/inplayMain/inplay-main.service';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';

import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { ISportTracking } from '@app/inPlay/models/sport-tracking.model';
import { IRibbonItem } from '@app/inPlay/models/ribbon.model';
import { IInplayConnectionState } from '@app/inPlay/models/connection.model';
import { inplayConfig } from '@app/inPlay/constants/config';
import { EVENTS } from '@core/constants/websocket-events.constant';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'multiple-sports-sections',
  templateUrl: 'multiple-sports-sections.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MultipleSportsSectionsComponent implements OnInit, OnDestroy, OnChanges {
  @Input() eventsByGroups: any;
  @Input() viewByFilters: string[];
  @Input() showExpanded: boolean;
  @Input() expandedSportsCount: number;
  @Input() expandedLeaguesCount: number;
  @Input() ssError: boolean;

  moduleName: string = 'sports-tab';
  isExpanded: boolean = false;
  filter: string;
  switchers: ISwitcherConfig[];
  limit: number;

  /**
   * Identifier of expand/collapse state.
   * @type {string}
   */
  expandedKey: string = 'expanded-sports-tab';

  private unsubscribe: Subject<void> = new Subject();
  readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;

  constructor(
    private pubsubService: PubSubService,
    private inPlayMainService: InplayMainService,
    private inPlayConnectionService: InplayConnectionService,
    private awsService: AWSFirehoseService,
    private changeDetectorRef: ChangeDetectorRef
  ) {
    this.goToFilter = this.goToFilter.bind(this);
  }

  ngOnInit(): void {
    /**
     * inPlay Sports Ribbon functionality
     */
    this.inPlayMainService.getRibbonData()
      .pipe(takeUntil(this.unsubscribe))
      .subscribe(data => this.getSwitchers(data.data));

    this.setDefaultFilter();
    this.initEventsListeners();

    this.pubsubService.subscribe(this.moduleName, `${inplayConfig.moduleName}.${EVENTS.SOCKET_RECONNECT_ERROR}`, () => {
      this.awsService.addAction('inplay=>UI_Message=>Unavailable=>wsError');
    });

    if (this.ssError) {
      this.awsService.addAction('inplay=>UI_Message=>Unavailable=>ssError');
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    // Track UI Message Service is unavailable
    if (changes.ssError && changes.ssError.currentValue) {
      this.awsService.addAction('inplay=>UI_Message=>Unavailable=>ssError');
    }
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe(this.moduleName);

    this.unsubscribe.next();
    this.unsubscribe.complete();
  }

  /**
   * Error on Web Sockets connection
   * @type {object}
   */
  get wsError(): IInplayConnectionState {
    return this.inPlayConnectionService.status;
  }
  set wsError(value:IInplayConnectionState){}

  /** Go to page filter
   * @param {string} filter
   */
  goToFilter(filter: string): void {
    if (filter !== this.filter) {
      this.pubsubService.publish(this.pubsubService.API.SET_INPLAY_WIDGETS_TAB, this.filter);
      this.pubsubService.publish(this.pubsubService.API.SET_LIVE_STREAM_WIDGETS_TAB, this.viewByFilters[0]);

      this.setFilter(filter);
      this.changeDetectorRef.markForCheck();
    }
  }

  /**
   * Check if sport events is present and show no events section
   * @param {String} filter
   */
  showNoEventsSection(filter: string): boolean {
    if (!this.ssError && this.eventsByGroups[filter]) {
      return !this.eventsByGroups[filter].eventsIds.length && (filter === this.filter);
    }
    return false;
  }

  /**
   * Prepare showMore link from categoryName
   * @param {String} categoryName
   */
  getShowMoreLink(sportUri: string): string {
    return `/in-play/${sportUri.toLowerCase().trim().replace('sport/', '')}`;
  }

  /**
   * Prepare showMore link title from categoryName
   * @param {String} categoryName
   */
  getShowMoreTitle(categoryName: string): string {
    return `view all ${categoryName.trim()} in-play events`;
  }

  /**
   * Toggle expand/collapse state of sport section.
   * @param {Object} sportSection
   */
  toggleSport(isExpanded: boolean, sportSection: ISportSegment): void {
    const categoryId = parseInt(sportSection.categoryId, 10);
    sportSection[this.expandedKey] = isExpanded;
    this.changeDetectorRef.detectChanges();

    if (sportSection[this.expandedKey]) {
      this.getSportData(categoryId).subscribe(() => {
        // if use expand and collapse section, after getting data we will check section again
        // unsubscribe if section was collapsed
        if (sportSection[this.expandedKey] === false) {
          this.inPlayMainService.unsubscribeForSportCompetitionUpdates(sportSection);
          this.inPlayMainService.unsubscribeForEventsUpdates(sportSection);
        }
        this.pubsubService.publish(this.pubsubService.API.INPLAY_DATA_RELOADED);
        this.changeDetectorRef.detectChanges();
      });
    } else {
      const sportIndex = this.eventsByGroups[this.filter].eventsBySports.indexOf(sportSection);

      if (sportIndex >= 0) {
        // clear data to triger ngOnChanges in singlesport after next section expand
        this.eventsByGroups[this.filter].eventsBySports[sportIndex].eventsByTypeName = [];
      }

      this.inPlayMainService.unsubscribeForSportCompetitionUpdates(sportSection);
      this.inPlayMainService.unsubscribeForEventsUpdates(sportSection);
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

  reloadComponent(): void {
    this.ssError = false;
    this.ngOnDestroy();
    this.ngOnInit();
  }

  private initEventsListeners(): void {
    // Update Event Counter and run digest manually using $timeout
    this.pubsubService.subscribe(this.moduleName,
      this.pubsubService.API.EVENT_COUNT_UPDATE,
        data => {
          setTimeout(() => this.getSwitchers(data), 0);
        });
  }

  /**
   * Checks if "liveNow" filter is active.
   * @private
   */
  private isLiveNowFilter(): boolean {
    return this.filter === this.viewByFilters[0];
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
  private setFilter(newFilter: string): void {
    const isValidFilter = newFilter !== this.filter && _.contains(this.viewByFilters, newFilter);

    if (isValidFilter && this.eventsByGroups && this.eventsByGroups[newFilter]) {
      this.filter = newFilter;

      _.each(this.eventsByGroups[newFilter].eventsBySports, (sportSection: ISportSegment, index) => {
        const sportId = parseInt(sportSection.categoryId, 10);

        sportSection[this.expandedKey] = this.shouldSportBeExpanded(index);

        if (sportSection[this.expandedKey]) {
          this.getSportData(sportId).subscribe(() => this.changeDetectorRef.markForCheck() );
        }
      });
    }
  }

  /**
   * Sets default filter:
   *  - switch filter to upcoming on init if no live now events available;
   *  - set "livenow" for default inplay page.
   * @private
   */
  private setDefaultFilter(): void {
    let defaultFilter = this.viewByFilters[0];
    if (this.showNoEventsSection(defaultFilter)) {
      defaultFilter = this.viewByFilters[1];
      this.goToFilter(defaultFilter);
    } else {
      this.setFilter(defaultFilter);
    }
    this.pubsubService.publish(this.pubsubService.API.EVENT_COUNT, defaultFilter);
    this.changeDetectorRef.markForCheck();
  }

  /**
   * Switchers for SPORTS SECTIONS
   * @private
   */
  private getSwitchers(data: IRibbonItem[]): void {
    this.switchers = this.inPlayMainService.generateSwitchers(
      this.goToFilter,
      this.viewByFilters,
      data
    );
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Apply single sport data
   * @param {ISportSegment} sportSection
   * @param {number} id
   * @private
   */
  private applySingleSportData(sportSection: ISportSegment, id: number): void {
    const sportDataIsPresent = _.has(sportSection, 'eventsByTypeName') && sportSection.eventsByTypeName.length;
    const eventsByGroup = this.eventsByGroups[this.filter];
    const sportIndex = this.inPlayMainService.getLevelIndex(eventsByGroup.eventsBySports, 'categoryId', id);

    if (sportDataIsPresent) {
      const sportSectionToUpdate = eventsByGroup.eventsBySports[sportIndex];
      // data is present
      if (sportSectionToUpdate) {
        // Update ids list for in-play group: "livenow" or "upcoming"
        eventsByGroup.eventsIds = _.union(eventsByGroup.eventsIds, sportSection.eventsIds);
        sportSectionToUpdate.eventsIds = sportSection.eventsIds;
        sportSectionToUpdate.eventsByTypeName = sportSection.eventsByTypeName;
      }
    } else {
      // no data were received
      eventsByGroup.eventsBySports.splice(sportIndex, 1);
    }
    this.changeDetectorRef.markForCheck();
  }

  /**
   * Get data by sport
   * @param {number} categoryId
   * @return {Observable<ISportSegment>}
   * @private
   */
  private getSportData(categoryId: number): Observable<ISportSegment> {
    return this.inPlayMainService.getSportData({
      categoryId,
      isLiveNowType: this.isLiveNowFilter(),
      topLevelType: this.inPlayMainService.getTopLevelTypeParameter(this.filter)
    }, false, true, true, categoryId === +this.HORSE_RACING_CATEGORY_ID).pipe(
      map((data: ISportSegment) => {
        // error handling
        if (!data || _.isEmpty(data) || _.has(data, 'error')) {
          this.inPlayConnectionService.setConnectionErrorState(true);
          return;
        }
        this.applySingleSportData(data, categoryId);

        return data;
      }));
  }
}
