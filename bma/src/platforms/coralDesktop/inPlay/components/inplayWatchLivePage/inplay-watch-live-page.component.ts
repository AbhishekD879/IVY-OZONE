import { Subject, of, forkJoin as observableForkJoin } from 'rxjs';
import { Component, OnDestroy, OnInit, ChangeDetectorRef, Input, ChangeDetectionStrategy } from '@angular/core';
import * as _ from 'underscore';
import { takeUntil, map, switchMap, catchError, finalize } from 'rxjs/operators';
import { CmsService } from '@core/services/cms/cms.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { inplayLiveStreamConfig } from '@app/inPlay/constants/config';
import { InplayMainService } from '@app/inPlay/services/inplayMain/inplay-main.service';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { ISystemConfig } from '@core/services/cms/models';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IRibbonCache } from '@app/inPlay/models/ribbon.model';
import { Router } from '@angular/router';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';
import { InPlayStorageService } from '@coralDesktop/inPlay/services/inplayStorage/in-play-storage.service';

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

  isWatchLiveEnabled: boolean = true;

  private unsubscribe: Subject<void> = new Subject();

  constructor(
    private pubsubService: PubSubService,
    private inplayMainService: InplayMainService,
    private cms: CmsService,
    private router: Router,
    private inplayConnectionService: InplayConnectionService,
    private inplayStorageService: InPlayStorageService,
    protected changeDetectorRef: ChangeDetectorRef
  ) {
    super();
  }

  ngOnInit(): void {
    const systemConfigRibbon$ = this.cms.getSystemConfig().pipe(
      map((config: ISystemConfig) => {
        this.expandedLeaguesCount = config.InPlayCompetitionsExpanded.competitionsCount;
        return config && config.InPlayWatchLive && config.InPlayWatchLive.enabled;
      }),
      switchMap((enabled: boolean) => {
        this.isWatchLiveEnabled = enabled;
        return enabled ? of(null) : this.inplayMainService.getRibbonData().pipe(takeUntil(this.unsubscribe));
      }));
    const structureData$ = this.inplayMainService.getLiveStreamStructureData();

    this.showSpinner();
    this.changeDetectorRef.detectChanges();

    observableForkJoin([systemConfigRibbon$, structureData$])
      .pipe(catchError(() => {
          this.showError();
          return of([]);
        }),
        finalize(() => {
          this.hideSpinner();
          this.changeDetectorRef.detectChanges();
        }))

      .subscribe(([systemConfigRibbon, structureData]: [IRibbonCache, ISportSegment]) => {
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

        /**
         * Adding callback for update section removing on LiveUpdate displayed - N
         */
        this.pubsubService.subscribe(this.cSyncName, this.pubsubService.API.DELETE_EVENT_FROM_CACHE, (eventId: number) => {
          this.inplayMainService.clearDeletedEventFromSport(this.data, eventId, this.viewByFilters);
          this.changeDetectorRef.detectChanges();
        });

        /**
         * Adding callback for update section removing on LiveUpdate displayed - N
         */
        this.pubsubService.subscribe(this.cSyncName, this.pubsubService.API.RELOAD_IN_PLAY, () => {
          this.reloadComponent();
          this.changeDetectorRef.detectChanges();
        });
        this.changeDetectorRef.detectChanges();
      });
  }

  ngOnDestroy(): void {
    this.unsubscribeFromMs();
    this.unsubscribe.next();
    this.unsubscribe.complete();
  }

  private unsubscribeFromMs() {
    this.pubsubService.unsubscribe(this.cSyncName);
    this.inplayMainService.unsubscribeForUpdates();

    if (this.isLiveStreamPage) {
      this.inplayStorageService.destroySportsCache();
      this.inplayConnectionService.disconnectComponent();
    }
  }
}
