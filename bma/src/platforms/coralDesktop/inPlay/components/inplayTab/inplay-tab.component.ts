import { map, takeUntil, switchMap, mergeMap } from 'rxjs/operators';
import { Component, Input, OnDestroy, OnInit, ChangeDetectorRef, ChangeDetectionStrategy } from '@angular/core';
import { Observable, Subject, Subscription } from 'rxjs';
import * as _ from 'underscore';

import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';
import { InplayMainService } from '@app/inPlay/services/inplayMain/inplay-main.service';
import { CmsService } from '@core/services/cms/cms.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { InPlayStorageService } from '@inplayModule/services/inplayStorage/in-play-storage.service';
import { InplaySubscriptionManagerService } from '@app/inPlay/services/InplaySubscriptionManager/inplay-subscription-manager.service';

import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { IInplayConnectionState } from '@app/inPlay/models/connection.model';
import { inplayConfig } from '@app/inPlay/constants/config';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { IRequestParams } from '@app/inPlay/models/request.model';
import { IStructureData } from '@app/inPlay/models/structure.model';
import { IRibbonItem } from '@app/inPlay/models/ribbon.model';
import { IReloadDataParams } from '@app/inPlay/models/reload-data-params.model';
import { EVENTS } from '@core/constants/websocket-events.constant';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { ActivatedRoute } from '@angular/router';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'inplay-tab',
  templateUrl: 'inplay-tab.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class InplayTabComponent implements OnInit, OnDestroy {
  @Input() id: number;
  @Input() singleSport: boolean;
  @Input() showExpanded: boolean;
  @Input() topSport: string;
  @Input() topMarkets: any;

  data: ISportSegment | IStructureData;

  appReady: boolean = false;
  filter: string;

  expandedSportsCount: number;
  expandedLeaguesCount: number;
  viewByFilters: string[];
  liveNowTab: string = 'livenow'; 

  /**
   * Determine is directive loaded by changing sport category and not filter for - General approach
   * @type {boolean}
   */
  firstLoad: boolean = true;
  switchers: ISwitcherConfig[];

  /**
   * Error on SiteServer error
   * @type {boolean}
   */
  ssError: boolean = false;

  /**
   * Indicates that calls returned data for structure or single sport - General approach
   * @type {boolean}
   */
  dataReady: boolean = false;
  resetDropdown: boolean = false;

  private unsubscribe: Subject<void> = new Subject();
  private connection: Subscription;
  private readonly tagName: string = 'inplayTab';
  readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;

  constructor(
    private inPlayConnectionService: InplayConnectionService,
    private inplayMainService: InplayMainService,
    private cmsService: CmsService,
    private inplayStorageService: InPlayStorageService,
    private inplaySubscriptionManagerService: InplaySubscriptionManagerService,
    private pubsubService: PubSubService,
    private awsService: AWSFirehoseService,
    private changeDetectorRef: ChangeDetectorRef,
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

    /**
     * Set Filter by default - for SINGLE SPORT
     */
    this.filter = this.viewByFilters[0];

    this.goToFilter = this.goToFilter.bind(this);
    this.updateSportData = this.updateSportData.bind(this);
  }

  ngOnInit(): void {
    /**
     * initial connection to inplay Microservice
     * on SportPage->InplayTab and on Homepage->InplayTab
     */
    this.connection = this.inPlayConnectionService.connectComponent().pipe(
      map(() => {
        this.appReady = true;
        /**
         * Init Cache - General approach
         */
        this.inplayMainService.initSportsCache();

        this.cmsService.getSystemConfig(null).pipe(
          map((data) => {
            this.expandedLeaguesCount = Number(data.InPlayCompetitionsExpanded.competitionsCount);
            return data;
          }),
          switchMap(() => {
            return this.updateSportData();
          }),
          map(() => {
            this.dataReady = true;
            this.changeDetectorRef.detectChanges();
          })
        ).subscribe(() => {
          this.addEventListeners();
        });
      }),
      mergeMap(() => {
        return this.inplayMainService.getRibbonData()
          .pipe(takeUntil(this.unsubscribe));
      })
    ).subscribe(data => this.getSwitchers(data.data));
  }

  ngOnDestroy(): void {
    this.connection && this.connection.unsubscribe && this.connection.unsubscribe();
    this.pubsubService.unsubscribe(this.tagName);
    this.inplayStorageService.destroySportsCache();
    this.inplayMainService.unsubscribeForUpdates();
    this.inPlayConnectionService.disconnectComponent();

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

  addEventListeners(): void {
    /**
     * Adding callback for update section removing on Websocket LiveUpdate displayed - N
     */
    if (this.singleSport && this.id) {
      this.pubsubService.subscribe(this.tagName, this.pubsubService.API.DELETE_EVENT_FROM_CACHE, eventId => {
        this.inplayMainService.clearDeletedEventFromType(this.data as ISportSegment, eventId);
        this.changeDetectorRef.detectChanges();
      });
      // Update Event Counter and run digest manually using $timeout
      this.pubsubService.subscribe(this.tagName, this.pubsubService.API.EVENT_COUNT_UPDATE, data => {
        setTimeout(() => this.getSwitchers(data), 0);
      });
    } else {
      this.pubsubService.subscribe(this.tagName, this.pubsubService.API.DELETE_EVENT_FROM_CACHE, eventId => {
        setTimeout(() => {
          this.inplayMainService.clearDeletedEventFromSport(this.data as ISportSegment, eventId, this.viewByFilters);
          this.changeDetectorRef.detectChanges();
        });
      });
    }

    /**
     * Adding callback for reload section on error
     */
    this.pubsubService.subscribe(this.tagName, `${inplayConfig.moduleName}.${EVENTS.SOCKET_RECONNECT_ERROR}`, () => {
      this.awsService.addAction('inplay=>UI_Message=>Unavailable=>wsError');
    });
  }

  /**
   * Go to page filter, this filter working for SINGLE SPORT switcher
   * @param {string} filter
   */
  goToFilter(filter: string): void {
    if (filter !== this.filter) {
      if (filter === this.liveNowTab) {
        this.resetDropdown = true;
      }
      this.dataReady = false;

      if (this.data) {
        const eventsIds = (this.data as ISportSegment).eventsIds;
        this.inplaySubscriptionManagerService.unsubscribeForLiveUpdates(eventsIds);
      }

      this.pubsubService.publish(this.pubsubService.API.SET_INPLAY_WIDGETS_TAB, this.filter);
      this.pubsubService.publish('SET_LIVE_STREAM_WIDGETS_TAB', this.viewByFilters[0]);

      this.filter = filter;
      this.updateSportData().subscribe(() => {
        this.changeDetectorRef.detectChanges();
      });
      this.changeDetectorRef.detectChanges();
    }
  }


  /**
   * Get data depends on config
   * @returns {promise}
   */
  updateSportData(options?: IReloadDataParams): Observable<void> {
    const useCache = (options && options.useCache) || false;
    const additionalRequestParams = (options && options.additionalParams) || {};

    if (this.singleSport && this.id) {
      const requestParams = _.extend({
        categoryId: this.id,                    // sportId
        isLiveNowType: this.isLiveNowFilter(),  // isLiveNow
        topLevelType: this.inplayMainService.getTopLevelTypeParameter(this.filter)
      }, additionalRequestParams);

      return this.updateSingleSportData(useCache, requestParams);
    }

    return this.inplayMainService.getStructureData(useCache, true).pipe(
      map((data: IStructureData) => this.applyStructureData(data))
    );
  }

  /**
   * Handler for data reload event
   *
   * @param options
   */
  onDataReload(options: IReloadDataParams): void {
    this.updateSportData(options).subscribe(() => {
      this.changeDetectorRef.detectChanges();
    });
  }

  /**
   * Check if sport events is present and show no events section for SINGLE SPORT
   * @param {String} filter
   */
  showNoEventsSection(filter: string): boolean {
    return this.dataReady &&
      !this.isSportEventsAvailable(this.data) &&
      (filter === this.filter) &&
      !(this.ssError || this.wsError.reconnectFailed) &&
      !!this.singleSport && !!this.id;
  }

  /**
   * Reload current directive - General approach
   */
  reloadComponent(): void {
    this.dataReady = false;
    this.ssError = false;

    this.ngOnDestroy();
    this.ngOnInit();
  }

  /**
   * Switchers for SINGLE SPORT
   */
  private getSwitchers(data: IRibbonItem[]): void {
    this.switchers = this.inplayMainService.generateSwitchers(this.goToFilter, this.viewByFilters, data, Number(this.id));
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Determine is LiveNow Filter - for SINGLE SPORT
   * @returns {boolean}
   */
  private isLiveNowFilter(): boolean {
    return this.filter === this.viewByFilters[0];
  }

  /**
   * Is available events in sport data for SINGLE SPORT
   * @param {Object} data
   * return {Boolean}
   */
  private isSportEventsAvailable(data): boolean {
    if(data[0] == undefined){
      return _.has(data, 'eventsByTypeName') && data.eventsByTypeName.length;
    }else{
      return _.has(data[0], 'eventsByTypeName') && data[0].eventsByTypeName.length;
    }
  }

  /**
   * Applying received data from MS if present
   * @param {Object} responseData
   */
  private applyStructureData(responseData: IStructureData): void {
    this.ssError = !responseData || _.isEmpty(responseData) || _.has(responseData, 'error');
    this.data = responseData;
    this.dataReady = true;
    this.trackErrorMessage();
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Apply single sport data
   * @param {Object} data
   */
  private applySingleSportData(data: ISportSegment): void {
    this.data = data;
    this.ssError = !data || _.isEmpty(data) || _.has(data, 'error');

    // Go to upcoming filter if no live now events
    if (!this.isSportEventsAvailable(data) && this.firstLoad && !(this.ssError || this.wsError.reconnectFailed)) {
      this.goToFilter(this.viewByFilters[1]);
    }
    this.dataReady = true;
    this.firstLoad = false;

    this.trackErrorMessage();
    this.changeDetectorRef.detectChanges();
  }

  private updateSingleSportData(useCache: boolean, requestParams: IRequestParams): Observable<void> {
    if (this.data) {
      const sportSegmentData = this.data as ISportSegment;
      const eventsIds = sportSegmentData.eventsIds;
      this.inplaySubscriptionManagerService.unsubscribeForSportCompetitionChanges(
        sportSegmentData.categoryId,
        sportSegmentData.topLevelType,
        sportSegmentData.marketSelector
      );
      this.inplaySubscriptionManagerService.unsubscribeForLiveUpdates(eventsIds);
    }

    return this.inplayMainService.getSportData(requestParams, useCache, true, true, this.id === +this.HORSE_RACING_CATEGORY_ID, this.topMarkets).pipe(
      map((data: ISportSegment) => {
        this.applySingleSportData(data);
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
