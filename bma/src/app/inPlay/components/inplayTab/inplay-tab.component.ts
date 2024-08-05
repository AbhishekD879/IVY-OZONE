import { map, switchMap } from 'rxjs/operators';
import { ChangeDetectorRef, Component, Input, OnDestroy, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { Observable, forkJoin as observableForkJoin } from 'rxjs';
import * as _ from 'underscore';

import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';
import { InplayMainService } from '@inplayModule/services/inplayMain/inplay-main.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { InPlayStorageService } from '@inplayModule/services/inplayStorage/in-play-storage.service';
import { InplaySubscriptionManagerService } from '@app/inPlay/services/InplaySubscriptionManager/inplay-subscription-manager.service';
import { ISportSegment } from '../../models/sport-segment.model';
import { IInplayConnectionState } from '@app/inPlay/models/connection.model';
import { inplayConfig } from '@app/inPlay/constants/config';
import { IRequestParams } from '@app/inPlay/models/request.model';
import { IStructureData } from '@app/inPlay/models/structure.model';
import { IReloadDataParams } from '@app/inPlay/models/reload-data-params.model';
import { IEventCounter, IEventCounterMap } from '@app/inPlay/models/event-counter.model';
import { EVENTS } from '@core/constants/websocket-events.constant';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import environment from '@environment/oxygenEnvConfig';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'inplay-tab',
  templateUrl: 'inplay-tab.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class InplayTabComponent implements OnInit, OnDestroy {
  @Input() id: number = 0;
  @Input() singleSport: boolean;
  @Input() showExpanded: boolean;
  @Input() topSport: string;
  @Input() topMarkets: any;

  data: (IStructureData | { [key: string]: ISportSegment }) = {};

  appReady: boolean = false;
  filter: string;

  expandedSportsCount: number;
  expandedLeaguesCount: number;
  viewByFilters: string[];

  /**
   * Determine is directive loaded by changing sport category and not filter for - General approach
   * @type {boolean}
   */
  firstLoad: boolean = true;

  /**
   * Error on SiteServer error
   * @type {boolean}
   */
  ssError: boolean = false;

  /**
   * Indicates that calls returned data for structure or single sport - General approach
   * @type {boolean}
   */
  dataReady: boolean;

  /**
   * Live/Upcoming events counter
   * @type {number}
   */
  allEventsCount: number;
  allUpcomingEventsCount: number;
  readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;

  constructor(
    protected inPlayConnectionService: InplayConnectionService,
    protected inplayMainService: InplayMainService,
    protected cmsService: CmsService,
    protected inplayStorageService: InPlayStorageService,
    protected inplaySubscriptionManagerService: InplaySubscriptionManagerService,
    protected pubsubService: PubSubService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected awsService: AWSFirehoseService,
    protected route: ActivatedRoute
  ) {
    /**
     * Expanded Sports Count for SPORTS SECTIONS
     * @member {Number}
     */
    this.expandedSportsCount = inplayConfig.expandedSportsCount;

    /**
     * Expanded Leagues Count for LEAGUES SECTIONS
     * @member {Number}
     */
    this.expandedLeaguesCount = inplayConfig.expandedLeaguesCount;

    /**
     * View Filters used for SINGLE SPORT
     * @type {Array}
     */
    this.viewByFilters = inplayConfig.viewByFilters;

    this.updateSportData = this.updateSportData.bind(this);
  }

  ngOnInit(): void {
    /**
     * initial connection to inplay Microservice
     * on SportPage->InplayTab and on Homepage->InplayTab
     */
    this.inPlayConnectionService.connectComponent().pipe(
      switchMap(() => {
        this.appReady = true;

        /**
         * Init Cache - General approach
         */
        this.inplayMainService.initSportsCache();
        this.pubsubService.subscribe('inplay', this.pubsubService.API.EVENT_COUNT_UPDATE, ribbonData => {
          const eventsCounter: IEventCounter = this.inplayMainService.getUnformattedEventsCounter(ribbonData, this.id);
          const eventCountersMap: IEventCounterMap = this.inplayMainService.getEventCountersByCategory(ribbonData);
          this.allEventsCount = eventsCounter ? +eventsCounter.livenow : 0;
          this.allUpcomingEventsCount = eventsCounter ? +eventsCounter.upcoming : 0;
          this.inplayMainService.updateEventsCounter(this.data, this.viewByFilters, eventsCounter, eventCountersMap,
            false, this.getEventType());
          this.changeDetectorRef.detectChanges();
        });

        return observableForkJoin(
          this.cmsService.getSystemConfig(null),
          this.inplayMainService.getRibbonData()
        );
      }),
        map((data) => {
          const systemConfigData = data[0];
          const ribbonData = data[1];

          this.expandedLeaguesCount = Number(systemConfigData.InPlayCompetitionsExpanded.competitionsCount);
          // TODO: Refactor this code. It’s too complicated for component usage. All this code should be moved in service.
          ribbonData.data.forEach((sport) => {
            if (sport.categoryId.toString() === this.id.toString()) {
              this.allEventsCount = sport.liveEventCount;
              this.allUpcomingEventsCount = sport.upcomingEventCount;
            }
          });
        }),
        switchMap(() => {
          return this.updateSportData(this.viewByFilters);
        }))
        .subscribe(() => {
          this.dataReady = true;
          this.changeDetectorRef.detectChanges();
        });
    this.addEventListeners();
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe('inplay');
    this.inplayStorageService.destroySportsCache();
    this.inplayMainService.unsubscribeForUpdates();
    this.inPlayConnectionService.disconnectComponent();
    this.pubsubService.unsubscribe('inplay');
    this.changeDetectorRef && this.changeDetectorRef.detach();
  }

  /**
   * Error on Web Sockets connection
   * @type {object}
   */
  get wsError(): IInplayConnectionState {
    return this.inPlayConnectionService.status;
  }
  set wsError(value:IInplayConnectionState){}
  trackById(index: number, filter: string) {
    return `${index}_${filter}`;
  }


  addEventListeners(): void {
    /**
     * Adding callback for update section removing on Websocket LiveUpdate displayed - N
     */
    if (this.singleSport && this.id) {
      this.pubsubService.subscribe('inplay', this.pubsubService.API.DELETE_EVENT_FROM_CACHE, eventId => {
        this.viewByFilters.forEach(filter => {
          this.inplayMainService.clearDeletedEventFromType(this.data[filter] as ISportSegment, eventId);
          this.changeDetectorRef.detectChanges();
        });
      });
    } else {
      this.pubsubService.subscribe('inplay', this.pubsubService.API.DELETE_EVENT_FROM_CACHE, eventId => {
        setTimeout(() => {
          this.inplayMainService.clearDeletedEventFromSport(this.data as IStructureData, eventId, this.viewByFilters);
          this.changeDetectorRef.detectChanges();
        });
      });
    }

    /**
     * Adding callback for reload section on error
     */
    this.pubsubService.subscribe('inplay', `${inplayConfig.moduleName}.${EVENTS.SOCKET_RECONNECT_ERROR}`, () => {
      if (this.singleSport) {
        this.awsService.addAction('inplay=>UI_Message=>Unavailable=>wsError');
      }
    });
  }

  /**
   * Get data depends on config
   * Observable<void[]>
   */
  updateSportData(filters: string[], options?: IReloadDataParams): Observable<void[]> {
    const useCache = (options && options.useCache) || false;
    const additionalRequestParams = (options && options.additionalParams) || {};
    const isSingleSport = this.singleSport && this.id;
    const singleSportObservables: Observable<void>[] = [];
    const multipleSportsObservable = [];

    if (isSingleSport) {
      filters.forEach((currentFilter: string) => {
        const requestParams: IRequestParams = _.extend({
          categoryId: this.id,                    // sportId
          isLiveNowType: this.isLiveNowFilter(currentFilter),  // isLiveNow
          topLevelType: this.inplayMainService.getTopLevelTypeParameter(currentFilter)
        }, additionalRequestParams);
        singleSportObservables.push(this.updateSingleSportData(useCache, requestParams, currentFilter));
      });
    } else {
      multipleSportsObservable.push(
        this.inplayMainService.getStructureData(useCache)
          .pipe(
            map((data: IStructureData) => { this.applyStructureData(data); })
          )
      );
    }

    const currentObservables: Observable<void>[] = isSingleSport ? singleSportObservables : multipleSportsObservable;
    return observableForkJoin(currentObservables);
  }

  /**
   * Handler for data reload event
   *
   * @param filter
   * @param options
   */
  onDataReload(filter: string, options: IReloadDataParams) {
    this.updateSportData([filter], options).subscribe(() => {
      this.dataReady = true;
      this.changeDetectorRef.detectChanges();
    });
  }

  /**
   * Check if sport events is present and show no events section for SINGLE SPORT
   * @param {String} filter
   */
  showNoEventsSection(filter: string): boolean {
    return this.dataReady &&
      !this.isSportEventsAvailable(this.data[filter]) &&
      !(this.ssError || this.wsError.reconnectFailed) &&
      !!this.singleSport && !!this.id;
  }

  /**
   * Reload current directive - General approach
   */
  reloadComponent(): void {
    this.dataReady = false;
    this.ssError = false;
    this.appReady = false;

    /**
     * Inplay miscroservice connection restart
     */
    this.ngOnDestroy();
    this.ngOnInit();
  }

  /**
   * To get event type
   * @return {string}
   */
  private getEventType(): string {
    return this.singleSport ? 'SINGLE': 'MULTIPLE';
  }

  /**
   * Determine is LiveNow Filter - for SINGLE SPORT
   * @returns {boolean}
   */
  public isLiveNowFilter(filter): boolean {
    return filter === this.viewByFilters[0];
  }

  /**
   * Is available events in sport data for SINGLE SPORT
   * @param {Object} data
   * return {Boolean}
   */
  private isSportEventsAvailable(data): boolean {
    return _.has(data, 'eventsByTypeName') && data.eventsByTypeName.length;
  }

  /**
   * Applying received data from MS if present
   * @param {Object} responseData
   */
  private applyStructureData(responseData: IStructureData): void {
    this.ssError = !responseData || _.isEmpty(responseData) || _.has(responseData, 'error');
    this.data = responseData;
    this.changeDetectorRef.detectChanges();
    this.trackErrorMessage();
  }

  /**
   * Apply single sport data
   * @param {Object} data
   */
  private applySingleSportData(data: ISportSegment, filter: string): void {
    this.data[filter] = data;
    this.ssError = !data || _.isEmpty(data) || _.has(data, 'error');
    this.firstLoad = false;
    this.changeDetectorRef.detectChanges();
    this.trackErrorMessage();
  }

  private updateSingleSportData(useCache: boolean, requestParams: IRequestParams, filter: string): Observable<void> {
    if (this.data && this.data[filter]) {
      const sportSegmentData = this.data[filter];
      const eventsIds = sportSegmentData.eventsIds;
      this.inplaySubscriptionManagerService.unsubscribeForSportCompetitionChanges(
        sportSegmentData.categoryId,
        sportSegmentData.topLevelType,
        sportSegmentData.marketSelector
      );
      this.inplaySubscriptionManagerService.unsubscribeForLiveUpdates(eventsIds);
    }
    return this.inplayMainService.getSportData(requestParams, useCache, this.isLiveNowFilter(filter), true, this.id === +this.HORSE_RACING_CATEGORY_ID, this.topMarkets).pipe(
      map((data: ISportSegment) => {
        if (data.topLevelType === 'LIVE_EVENT') {
          data.eventCount = this.allEventsCount;
        } else if (data.topLevelType === 'UPCOMING_EVENT') {
          data.eventCount = this.allUpcomingEventsCount;
        }
        this.applySingleSportData(data, filter);
        this.pubsubService.publish(this.pubsubService.API.INPLAY_DATA_RELOADED);
        this.changeDetectorRef.markForCheck();
      }));
  }

  /**
   * Track UI Message Service is unavailable
   */
  private trackErrorMessage(): void {
    if (this.ssError) {
      this.awsService.addAction('inplay=>UI_Message=>Unavailable=>ssError');
    }
  }
}
