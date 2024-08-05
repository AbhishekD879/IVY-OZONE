import {
  forkJoin as observableForkJoin,
  Observable,
  of, Subscription
} from 'rxjs';

import { map, concatMap, switchMap } from 'rxjs/operators';
import { ActivatedRoute, Router, Params } from '@angular/router';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { Component, OnDestroy, OnInit, ChangeDetectorRef, ChangeDetectionStrategy } from '@angular/core';
import * as _ from 'underscore';

import { CmsService } from '@coreModule/services/cms/cms.service';
import { inplayConfig } from '@app/inPlay/constants/config';
import { InplaySubscriptionManagerService } from '@app/inPlay/services/InplaySubscriptionManager/inplay-subscription-manager.service';
import { InplayMainService } from '@inplayModule/services/inplayMain/inplay-main.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';
import { DeviceService } from '@core/services/device/device.service';
import { IRibbonCache, IRibbonItem } from '@app/inPlay/models/ribbon.model';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { ISystemConfig, ISportInstance } from '@core/services/cms/models';
import { IReloadDataParams } from '@app/inPlay/models/reload-data-params.model';
import { IInplayConnectionState } from '@app/inPlay/models/connection.model';
import { IEventCounter, IEventCounterMap } from '@app/inPlay/models/event-counter.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import environment from '@environment/oxygenEnvConfig';
import { SportsConfigService } from '@app/sb/services/sportsConfig/sports-config.service';

@Component({
  selector: 'inplay-single-sport-page',
  templateUrl: 'inplay-single-sport-page.component.html',
  styleUrls: ['inplay-single-sport-page.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class InplaySingleSportPageComponent extends AbstractOutletComponent implements OnInit, OnDestroy {

  sportSectionData: {
    [key: string]: ISportSegment
  } = {};
  expandedLeaguesCount: number;

  /**
   * Name for Connect.sync fileName
   */
  cSyncName: string = `inplaySingleSportPage`;

  /**
   * Error on SiteServer error
   * @type {boolean}
   */
  ssError: boolean = false;

  /**
   * View Filters used for SINGLE SPORT
   * @type {Array}
   */
  viewByFilters: string[] = inplayConfig.viewByFilters;

  /**
   * Determine is directive loaded by changing sport category and not filter
   * @type {boolean}
   */
  firstLoad: boolean = true;
  dataReady: boolean = false;
  categoryId: number;
  sportId: number;
  routeListener: Subscription;

  private sportUri: string;
  private sportsConfigSubscription: Subscription;
  readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;
  isHR: boolean = false;
  checkLoad: boolean = true;
  topMarkets: any;

  constructor(
    protected inplayMainService: InplayMainService,
    protected inplaySubscriptionManagerService: InplaySubscriptionManagerService,
    protected pubsubService: PubSubService,
    protected inPlayConnectionService: InplayConnectionService,
    protected route: ActivatedRoute,
    protected cms: CmsService,
    protected router: Router,
    protected deviceService: DeviceService,
    protected awsService: AWSFirehoseService,
    protected changeDetectorRef: ChangeDetectorRef,
    private sportsConfigService: SportsConfigService
  ) {
    super();
  }

  ngOnInit(): void {
    this.routeListener = this.route.params.pipe(
      concatMap((params: Params) => {
        this.sportSectionData && this.sportSectionData[this.viewByFilters[0]]
          && this.inplayMainService.unsubscribeForEventsUpdates(this.sportSectionData[this.viewByFilters[0]]);

        this.showSpinner();
        this.inPlayConnectionService.setConnectionErrorState(false);
        this.changeDetectorRef.detectChanges();

        const systemConfigObservable = this.cms.getSystemConfig();

        this.sportUri = params.sport || '';
        this.sportsConfigSubscription = this.sportsConfigService.getSport(this.sportUri).subscribe((sport: ISportInstance) => {
          this.topMarkets = (sport?.sportConfig?.config?.request?.aggregatedMarkets || []);
        });
        const sportDataObservable = this.inplayMainService.getSportId(this.sportUri).pipe(concatMap((sportId: number) => {
          this.sportId = sportId;
          if (!this.sportId) {
            this.inplayMainService.addRibbonURLHandler();
            // return value to make subscribe work and route change pipe work
            this.showContent();
            return of(null);
          }

          this.categoryId = this.sportId;
          this.isHR = this.categoryId.toString() === this.HORSE_RACING_CATEGORY_ID;
          return observableForkJoin(
            _.map(this.viewByFilters, (filter, index) => {
              const isLiveNow = this.isLiveNowFilter(filter, index);
              this.checkLoad = true;
              return this.inplayMainService.getSportData({
                categoryId: this.sportId,
                isLiveNowType: isLiveNow,
                topLevelType: this.inplayMainService.getTopLevelTypeParameter(filter),
              }, true, filter==='livenow', isLiveNow, this.isHR, this.topMarkets);
            })
          );
        }));
        return observableForkJoin([systemConfigObservable, sportDataObservable]);
      }))
      .subscribe((routeData) => {
        const systemConfig: ISystemConfig = routeData[0];
        const sportData = routeData[1];

        if (!sportData || !systemConfig) {
          return;
        }

        this.expandedLeaguesCount = systemConfig.InPlayCompetitionsExpanded.competitionsCount;

        // Data for sport
        this.setSportData(sportData);

        this.pubsubService.publish(this.pubsubService.API.SET_INPLAY_WIDGETS_TAB, this.viewByFilters[1]);

        /**
         * Apply data on init
         */
        this.applyData(this.sportSectionData);
        this.showContent();
      }, () => {
        /**
         * Data for sport
         */
        this.sportSectionData[this.viewByFilters[0]] = this.sportSectionData[this.viewByFilters[1]] = {} as ISportSegment;
        this.applyData(this.sportSectionData);
        this.showContent();
      });

    this.pubsubService.subscribe(this.cSyncName, this.pubsubService.API.EVENT_COUNT_UPDATE, (data: IRibbonItem[]) => {
      const isCurrentSportRemoved = !_.findWhere(data, { targetUriCopy: this.sportUri });
      if (isCurrentSportRemoved) {
        const firstSport = this.inplayMainService.getFirstSport(data);
        this.router.navigateByUrl(firstSport.targetUri);
      }
      const eventsCounter: IEventCounter = this.inplayMainService.getUnformattedEventsCounter(data, this.sportId);
      const eventCountersMap: IEventCounterMap = this.inplayMainService.getEventCountersByCategory(data);
      this.inplayMainService.updateEventsCounter(this.sportSectionData, this.viewByFilters, eventsCounter,
        eventCountersMap, true, 'SINGLE');
      this.changeDetectorRef.detectChanges();
    });
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe(this.cSyncName);
    this.routeListener.unsubscribe();
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
  }

  get wsError(): IInplayConnectionState {
    return this.inPlayConnectionService.status;
  }
  set wsError(value:IInplayConnectionState){}

  trackById(index: number, filter: string) {
    return `${index}_${filter}`;
  }

  /**
   * Sports Data Handler
   * @param {ISportSegment} sportSectionData
   */
  applyData(sportSectionData: { [key: string]: ISportSegment }): void {
    this.ssError = _.some(sportSectionData, singleSportSectionData => _.has(singleSportSectionData, 'error'));

    if (this.deviceService.isOnline()) {
      this.dataReady = true;
      this.changeDetectorRef.detectChanges();
    }

    this.trackErrorMessage();
  }

  updateSportData(options?: IReloadDataParams): void {
    const useCache = (options && options.useCache) || false;
    const additionalRequestParams = (options && options.additionalParams) || {};
    this.sportUri = this.route.snapshot.params['sport'];

    if (this.sportSectionData && this.sportSectionData[this.viewByFilters[0]]) {
      const sportSegmentData: ISportSegment = this.sportSectionData[this.viewByFilters[0]];
      const eventsIds: number[] = sportSegmentData.eventsIds;
      this.inplaySubscriptionManagerService.unsubscribeForSportCompetitionChanges(
        sportSegmentData.categoryId,
        sportSegmentData.topLevelType,
        sportSegmentData.marketSelector || ''
      );
      this.inplaySubscriptionManagerService.unsubscribeForLiveUpdates(eventsIds);
    }

    this.inplayMainService.getSportId(this.sportUri).pipe(
      concatMap((sportId: number) => {
        this.sportId = sportId;
        const requestParams = _.extend({
          categoryId: this.sportId,
          isLiveNowType: true,
          topLevelType: this.inplayMainService.getTopLevelTypeParameter(this.viewByFilters[0])
        }, additionalRequestParams);

        return this.inplayMainService.getSportData(requestParams, useCache, true, true, this.isHR, this.topMarkets);
      }),
      switchMap((inplaySportData: ISportSegment): Observable<ISportSegment>  => {
        return of(this.updateEventCount(inplaySportData));
      }),
      map((data: ISportSegment) => {
        this.applyInplaySportData(data);
      }))
      .subscribe();
  }

  /**
   * Determine is LiveNow Filter - for SINGLE SPORT
   * @param {string} filter
   * @returns {boolean}
   */
  isLiveNowFilter(filter: string, filterIndex: number = 0): boolean {
    if (this.isHR && filterIndex < 2) {
      return filter === this.viewByFilters[filterIndex];
    }
    return filter === this.viewByFilters[0];
  }

  /**
   * Check if sport events is present and show no events section
   * @param {string} filter
   */
  showNoEventsSection(filter: string): boolean {
    return this.dataReady &&
      ((this.sportSectionData[filter] === undefined) ||
        (this.sportSectionData[filter].eventsByTypeName &&
          !this.sportSectionData[filter].eventsByTypeName.length)) &&
      !this.ssError[filter];
  }

  reloadComponent(): void {
    this.inPlayConnectionService.setConnectionErrorState(false);
    super.reloadComponent();
  }

  protected showContent(): void {
    /**
     * Adding callback for update section removing on LiveUpdate displayed - N
     */
    this.pubsubService.subscribe(this.cSyncName, this.pubsubService.API.DELETE_EVENT_FROM_CACHE, eventId => {
      _.each(this.viewByFilters, filter => {
        this.sportSectionData && this.inplayMainService.clearDeletedEventFromType(this.sportSectionData[filter], eventId);
        this.changeDetectorRef.detectChanges();
      });
    });

    this.pubsubService.subscribe(this.cSyncName, this.pubsubService.API.RELOAD_IN_PLAY,
      () => { this.reloadComponent(); this.changeDetectorRef.detectChanges(); });
    this.hideSpinner();
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Set in-play and upcoming sport data
   * @param {Object[]} sportDataArray
   */
  private setSportData(sportDataArray: ISportSegment[] = []) {
    const sportSectionData = {};
    sportSectionData[this.viewByFilters[0]] = sportDataArray[0];
    sportSectionData[this.viewByFilters[1]] = sportDataArray[1];
    this.sportSectionData = sportSectionData;
  }

  /**
   * Apply data according to market selector change
   * @param {Object} sportData
   */
  private applyInplaySportData(sportData: ISportSegment): void {
    const sportDataIsPresent = _.has(sportData, 'eventsByTypeName') && sportData.eventsByTypeName.length;

    this.ssError = !sportData || _.isEmpty(sportData) || _.has(sportData, 'error');

    if (sportDataIsPresent) {
      // data is present
      this.sportSectionData[this.viewByFilters[0]] = sportData;
    } else {
      // no data were received
      this.sportSectionData[this.viewByFilters[0]] = {
        categoryId: this.sportId.toString(),
        eventsByTypeName: [],
        isTierOneSport: false,
        tier: undefined,
        topLevelType: 'LIVE_EVENT'
      } as Partial<ISportSegment> as ISportSegment;
    }
    this.dataReady = true;

    this.trackErrorMessage();
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Track UI Message Service is unavailable
   */
  private trackErrorMessage(): void {
    if (this.ssError) {
      this.awsService.addAction('inplay=>UI_Message=>Unavailable=>ssError');
    }
  }

  /**
   * Update event count from ribbonData
   * @param {Object} inplaySportData
   * @returns {Object}
   */
  private updateEventCount(inplaySportData: ISportSegment): ISportSegment {
    this.inplayMainService.getRibbonData().subscribe((ribbonData: IRibbonCache) => {
      const ribbonItem: IRibbonItem = ribbonData.data.filter((sport) => {
        return this.sportId.toString() === sport.categoryId.toString();
      })[0];
      if (ribbonItem) {
        if (inplaySportData.topLevelType === 'LIVE_EVENT') {
          inplaySportData.eventCount = ribbonItem.liveEventCount;
        } else if (inplaySportData.topLevelType === 'UPCOMING_EVENT') {
          inplaySportData.eventCount = ribbonItem.upcomingEventCount;
        }
      }
      this.changeDetectorRef.detectChanges();
    });
    return inplaySportData;
  }
}
