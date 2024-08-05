import {
  forkJoin as observableForkJoin,
  Subscription, of
} from 'rxjs';

import { map, concatMap, catchError } from 'rxjs/operators';
import { ActivatedRoute, Router, Params } from '@angular/router';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { Component, OnDestroy, OnInit, ChangeDetectorRef, ChangeDetectionStrategy } from '@angular/core';
import * as _ from 'underscore';

import { CmsService } from '@core/services/cms/cms.service';
import { inplayConfig } from '@app/inPlay/constants/config';
import { InplaySubscriptionManagerService } from '@app/inPlay/services/InplaySubscriptionManager/inplay-subscription-manager.service';
import { InplayMainService } from '@app/inPlay/services/inplayMain/inplay-main.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { IRibbonCache, IRibbonItem } from '@app/inPlay/models/ribbon.model';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { ISystemConfig, ISportInstance } from '@core/services/cms/models';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';
import { IReloadDataParams } from '@app/inPlay/models/reload-data-params.model';
import { IInplayConnectionState } from '@app/inPlay/models/connection.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import environment from '@environment/oxygenEnvConfig';
import { SportsConfigService } from '@app/sb/services/sportsConfig/sports-config.service';

@Component({
  selector: 'inplay-single-sport-page',
  templateUrl: 'inplay-single-sport-page.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class InplaySingleSportPageComponent extends AbstractOutletComponent implements OnInit, OnDestroy {

  sportSectionData: ISportSegment;
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

  filter: string;
  checkLoad: boolean = true;
  switchers: ISwitcherConfig[];
  routeListener: Subscription;
  topMarkets: any;

  private sportUri: string;
  private sportId: number;
  private ribbonDataSubscription: Subscription;
  private sportsConfigSubscription: Subscription;
  readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;

  constructor(
    private inplayMainService: InplayMainService,
    private inplaySubscriptionManagerService: InplaySubscriptionManagerService,
    private pubsubService: PubSubService,
    private inPlayConnectionService: InplayConnectionService,
    private route: ActivatedRoute,
    private cms: CmsService,
    private router: Router,
    private awsService: AWSFirehoseService,
    protected changeDetectorRef: ChangeDetectorRef,
    private sportsConfigService: SportsConfigService
  ) {
    super();
    this.goToFilter = this.goToFilter.bind(this);
  }

  ngOnInit(): void {
    this.filter = this.viewByFilters[0];
    this.routeListener = this.route.params.pipe(
        concatMap((params: Params) => {
          this.showSpinner();
          const systemConfigObservable = this.cms.getSystemConfig(false);

          this.changeDetectorRef.detectChanges();

          this.sportUri = params.sport || '';
          this.sportsConfigSubscription = this.sportsConfigService.getSport(this.sportUri).subscribe((sport: ISportInstance) => {
            this.topMarkets = (sport?.sportConfig?.config?.request?.aggregatedMarkets || []);
          });
          const sportDataObservable = this.inplayMainService.getSportId(this.sportUri).pipe(concatMap((sportId: number) => {
            this.sportId = sportId;
            if (!this.sportId) {
              this.inplayMainService.addRibbonURLHandler();
              // return value to make subscribe work and route change pipe work
              return of(null);
            }
              /**
               * Set Filter by default - for SINGLE SPORT
               */
              this.inPlayConnectionService.setConnectionErrorState(false);
              this.filter = this.viewByFilters[0];
              this.checkLoad = true;
              return this.inplayMainService.getSportData({
                categoryId: this.sportId,
                isLiveNowType: true,
                topLevelType: this.inplayMainService.getTopLevelTypeParameter(this.filter)
              }, true, true, true, this.sportId === +this.HORSE_RACING_CATEGORY_ID, this.topMarkets);
            }));

          return observableForkJoin([systemConfigObservable, sportDataObservable]);
      })).pipe(
        map((routeData) => {
          const systemConfig: ISystemConfig = routeData[0];
          const sportData = routeData[1];

          if (!sportData || !systemConfig) {
            return;
          }

          this.expandedLeaguesCount = systemConfig.InPlayCompetitionsExpanded.competitionsCount;

          /**
           * Set Filter by default - for SINGLE SPORT
           */
          this.filter = this.viewByFilters[0];

          /**
           * Data for sport
           */
          this.sportSectionData = sportData;

          this.pubsubService.publish(this.pubsubService.API.SET_INPLAY_WIDGETS_TAB, this.viewByFilters[1]);
          this.changeDetectorRef.markForCheck();
          this.ribbonDataSubscription = this.inplayMainService.getRibbonData()
              .subscribe((data: IRibbonCache) => this.getSwitchers(data.data));
          /**
           * Apply data on init
           */
          this.applyData(sportData);
          this.showContent();
        }),
        catchError(() => {
          /**
           * Data for sport
           */
          this.sportSectionData = {} as ISportSegment;

          this.applyData(this.sportSectionData);
          this.showContent();
          return of();
        })
    ).subscribe();
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe(this.cSyncName);
    this.routeListener.unsubscribe();
    this.ribbonDataSubscription && this.ribbonDataSubscription.unsubscribe();
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
  }

  get wsError(): IInplayConnectionState {
    return this.inPlayConnectionService.status;
  }
  set wsError(value:IInplayConnectionState){}

  /**
   * Sports Data Handler
   * @param {ISportSegment} sportSectionData
   */
  applyData(sportSectionData: ISportSegment): void {
    const sportDataIsPresent = _.has(sportSectionData, 'eventsByTypeName') && sportSectionData.eventsByTypeName.length;

    this.ssError = !sportSectionData || _.isEmpty(sportSectionData) || _.has(sportSectionData, 'error');

    if (sportDataIsPresent) {
      this.pubsubService.publish(this.pubsubService.API.EVENT_COUNT, this.filter);
      this.changeDetectorRef.markForCheck();
    } else {
      if (this.firstLoad && !this.ssError) {
        this.goToFilter(this.viewByFilters[1]);
      }
    }
    this.sportSectionData = sportSectionData;

    this.dataReady = true;
    this.firstLoad = false;

    this.trackErrorMessage();
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Go to page filter
   * @param {string} filter
   */
  goToFilter(filter: string): void {
    this.dataReady = false;

    if (this.sportSectionData) {
      const { eventsIds } = this.sportSectionData;

      this.inplaySubscriptionManagerService.unsubscribeForLiveUpdates(eventsIds);
    }

    this.pubsubService.publish(this.pubsubService.API.SET_INPLAY_WIDGETS_TAB, this.filter);
    this.pubsubService.publish('SET_LIVE_STREAM_WIDGETS_TAB', this.viewByFilters[0]);
    this.filter = filter;
    this.changeDetectorRef.detectChanges();
    this.updateSportData();
  }

  updateSportData(options?: IReloadDataParams): void {
    const useCache = (options && options.useCache) || false;
    const additionalRequestParams = (options && options.additionalParams) || {};

    this.sportUri = this.route.snapshot.params['sport'];

    this.inplayMainService.getSportId(this.sportUri).pipe(
      concatMap((sportId: number) => {
        const useLiveNowFilter = this.filter === 'upcoming' ? null : this.isLiveNowFilter();

        const requestParams = _.extend({
          categoryId: sportId,
          isLiveNowType: useLiveNowFilter,
          topLevelType: this.inplayMainService.getTopLevelTypeParameter(this.filter)
        }, additionalRequestParams);

        if (this.sportSectionData) {
          const eventsIds = this.sportSectionData.eventsIds;

          this.inplaySubscriptionManagerService.unsubscribeForSportCompetitionChanges(
            this.sportSectionData.categoryId,
            this.sportSectionData.topLevelType,
            this.sportSectionData.marketSelector
          );

          this.inplaySubscriptionManagerService.unsubscribeForLiveUpdates(eventsIds);
        }

        return this.inplayMainService.getSportData(requestParams, useCache, true, true, sportId === +this.HORSE_RACING_CATEGORY_ID, this.topMarkets);
      }),
      map((data: ISportSegment) => {
        this.applyData(data);
        setTimeout(() => {
          this.pubsubService.publish(this.pubsubService.API.INPLAY_DATA_RELOADED);
          this.changeDetectorRef.markForCheck();
        }, 0);
        this.changeDetectorRef.detectChanges();
        return data;
      }))
      .subscribe();
  }

  /**
   * Determine is LiveNow Filter - for SINGLE SPORT
   * @returns {boolean}
   */
  isLiveNowFilter(): boolean {
    return this.filter === this.viewByFilters[0];
  }

  /**
   * Check if sport events is present and show no events section
   * @param {String} filter
   */
  showNoEventsSection(filter: string): boolean {
    return this.dataReady &&
      ((this.sportSectionData === undefined) ||
        (this.sportSectionData.eventsByTypeName &&
          !this.sportSectionData.eventsByTypeName.length)) &&
      !this.ssError &&
      (filter === this.filter);
  }

  reloadComponent(): void {
    this.inPlayConnectionService.setConnectionErrorState(false);
    super.reloadComponent();
  }

  /**
   * Switchers for SINGLE SPORT
   */
  private getSwitchers(data: IRibbonItem[]): void {
    this.switchers = this.inplayMainService.generateSwitchers(this.goToFilter, this.viewByFilters, data);
    this.changeDetectorRef.detectChanges();
  }

  private showContent(): void {
    /**
     * Adding callback for update section removing on LiveUpdate displayed - N
     */
    this.pubsubService.subscribe(this.cSyncName, this.pubsubService.API.DELETE_EVENT_FROM_CACHE, eventId => {
      this.inplayMainService.clearDeletedEventFromType(this.sportSectionData, eventId);
      this.changeDetectorRef.detectChanges();
    });


    this.pubsubService.subscribe(this.cSyncName, this.pubsubService.API.RELOAD_IN_PLAY,
      () => { this.reloadComponent(); this.changeDetectorRef.detectChanges(); });

    // Update Event Counter and run digest manually using timeout
    this.pubsubService.subscribe(this.cSyncName, this.pubsubService.API.EVENT_COUNT_UPDATE,
      (data: IRibbonItem[]) => {
        const isCurrentSportRemoved = !_.findWhere(data, { targetUriCopy: this.sportUri });
        if (isCurrentSportRemoved) {
          const firstSport = this.inplayMainService.getFirstSport(data);
          this.router.navigateByUrl(firstSport.targetUri);
        } else {
          setTimeout(() => this.getSwitchers(data), 0);
        }
        this.changeDetectorRef.detectChanges();
      });

    this.hideSpinner();
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Track UI Message Service is unavailable
   */
  private trackErrorMessage(): void {
    if (this.ssError && !this.showNoEventsSection(this.filter)) {
      this.awsService.addAction('inplay=>UI_Message=>Unavailable=>ssError');
    }
  }
}
