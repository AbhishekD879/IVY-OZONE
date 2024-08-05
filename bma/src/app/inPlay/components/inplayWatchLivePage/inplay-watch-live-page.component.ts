import { catchError, finalize, takeUntil, switchMap } from 'rxjs/operators';
import { forkJoin as observableForkJoin, of, Subject } from 'rxjs';
import { Component, OnDestroy, OnInit, ChangeDetectorRef, ChangeDetectionStrategy, Input } from '@angular/core';
import * as _ from 'underscore';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { inplayLiveStreamConfig } from '@app/inPlay/constants/config';
import { InplayMainService } from '@inplayModule/services/inplayMain/inplay-main.service';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { ISystemConfig } from '@core/services/cms/models';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IRibbonCache } from '@app/inPlay/models/ribbon.model';
import { Router } from '@angular/router';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';
import { IEventCounter, IEventCounterMap } from '../../models/event-counter.model';
import { InplaySubscriptionManagerService } from '@app/inPlay/services/InplaySubscriptionManager/inplay-subscription-manager.service';
import { InPlayStorageService } from '@app/inPlay/services/inplayStorage/in-play-storage.service';
import { WsConnector } from '@core/services/wsConnector/ws-connector';

@Component({
  selector: 'inplay-watch-live-page',
  templateUrl: 'inplay-watch-live-page.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class InplayWatchLivePageComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  @Input() isLiveStreamPage: boolean;

  expandedLeaguesCount: number;
  data: ISportSegment;

  /**
   * Name for Connect.sync fileName
   */
  cSyncName: string = `inplayWatchLivePage`;
  ssError: boolean;

  /**
   * Expanded Sports Count for SPORTS SECTIONS
   * @member {Number}
   */
  expandedSportsCount: number = inplayLiveStreamConfig.expandedSportsCount;

  /**
   * View Filters used for clearDeletedEventFromSport functionality.
   */
  viewByFilters: string[] = inplayLiveStreamConfig.viewByFilters;

  private unsubscribe: Subject<void> = new Subject();

  constructor(
    protected pubsubService: PubSubService,
    protected inplayMainService: InplayMainService,
    protected inPlayConnectionService: InplayConnectionService,
    protected cms: CmsService,
    protected router: Router,
    protected inplaySubscriptionManagerService: InplaySubscriptionManagerService,
    protected inplayStorageService: InPlayStorageService,
    protected changeDetectorRef: ChangeDetectorRef
  ) {
    super();
  }

  ngOnInit(): void {
    const connectComponent$ = this.inPlayConnectionService.connectComponent();
    const systemConfig$ = this.cms.getSystemConfig();
    const systemConfigRibbon$ = systemConfig$.pipe(
      switchMap((config: ISystemConfig) => {
        const enabled = config && config.InPlayWatchLive && config.InPlayWatchLive.enabled;
        return enabled ? of(null) : this.inplayMainService.getRibbonData().pipe(takeUntil(this.unsubscribe));
      }));
    const structureData$ = this.inplayMainService.getLiveStreamStructureData();

    this.showSpinner();
    this.changeDetectorRef.detectChanges();

    observableForkJoin([connectComponent$, systemConfig$, systemConfigRibbon$, structureData$])
      .pipe(catchError(() => {
          return of([]);
        }),
        finalize(() => {
          this.addEventListeners();
          this.hideSpinner();
          this.changeDetectorRef.detectChanges();
        }))
      .subscribe(([connection, systemConfig, systemConfigRibbon, structureData]:
                    [WsConnector, ISystemConfig, IRibbonCache, ISportSegment]) => {
        if (connection) {
          this.inplayMainService.initSportsCache();
        }
        this.expandedLeaguesCount = systemConfig &&
          systemConfig.InPlayCompetitionsExpanded &&
          systemConfig.InPlayCompetitionsExpanded.competitionsCount;

        if (!this.isLiveStreamPage && systemConfigRibbon) {
          const firstSport = this.inplayMainService.getFirstSport(systemConfigRibbon.data);
          this.router.navigateByUrl(`/in-play/${firstSport.targetUriCopy}`);
        }
        /**
         * Data for sport sections
         */
        this.data = structureData;

        /**
         * Error on SiteServer error
         * @type {boolean}
         */
        this.ssError = !structureData || _.isEmpty(structureData) || _.has(structureData, 'error');
      });

    this.pubsubService.subscribe(this.cSyncName, this.pubsubService.API.EVENT_COUNT_UPDATE, data => {
      const eventsCounter: IEventCounter = this.inplayMainService.getUnformattedEventsCounter(data);
      const eventCountersMap: IEventCounterMap = this.inplayMainService.getEventCountersByCategory(data);
      this.inplayMainService.updateEventsCounter(this.data, this.viewByFilters, eventsCounter,
        eventCountersMap, false, 'MULTIPLE');
      this.changeDetectorRef.detectChanges();
    });

    this.inplaySubscriptionManagerService.subscribe4RibbonUpdates();
  }

  ngOnDestroy(): void {
    this.unsubscribeFromMs();
    this.unsubscribe.next();
    this.unsubscribe.complete();
  }

  reloadComponent(): void {
    this.inPlayConnectionService.setConnectionErrorState(false);
    super.reloadComponent();
  }


  protected unsubscribeFromMs() {
    this.pubsubService.unsubscribe(this.cSyncName);
    this.inplaySubscriptionManagerService.unsubscribe4RibbonUpdates();
    this.inplayMainService.unsubscribeForUpdates();

    // should not disconnect component when page rendered in Inplay area
    // should disconnect component if it is rendered on Live-stream Tab
    if (this.isLiveStreamPage) {
      this.inplayStorageService.destroySportsCache();
      this.inPlayConnectionService.disconnectComponent();
    }
  }


  protected addEventListeners(): void {
    /**
     * Adding callback for update section removing on LiveUpdate displayed - N
     */
    this.pubsubService.subscribe(this.cSyncName, this.pubsubService.API.DELETE_EVENT_FROM_CACHE, (eventId: number) => {
      this.inplayMainService.clearDeletedEventFromSport(this.data, eventId, this.viewByFilters);
      this.changeDetectorRef.detectChanges();
    });

    this.pubsubService.subscribe(this.cSyncName, this.pubsubService.API.RELOAD_IN_PLAY,
      () => { this.reloadComponent(); this.changeDetectorRef.detectChanges(); });
  }
}
