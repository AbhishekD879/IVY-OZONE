import { of, Subject } from 'rxjs';
import { Component, OnDestroy, OnInit, ChangeDetectorRef, ChangeDetectionStrategy, Input } from '@angular/core';
import * as _ from 'underscore';
import { takeUntil, map, switchMap } from 'rxjs/operators';

import { CmsService } from '@coreModule/services/cms/cms.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { inplayLiveStreamConfig } from '@app/inPlay/constants/config';
import { InplayMainService } from '@ladbrokesDesktop/inPlay/services/inplayMain/inplay-main.service';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { ISystemConfig } from '@core/services/cms/models';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IRibbonCache } from '@app/inPlay/models/ribbon.model';
import { Router } from '@angular/router';
import { InPlayStorageService } from '@ladbrokesDesktop/inPlay/services/inplayStorage/in-play-storage.service';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';


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
    this.cms.getSystemConfig(false).pipe(
      map((config: ISystemConfig) => {
        this.expandedLeaguesCount = config.InPlayCompetitionsExpanded.competitionsCount;
        return config && config.InPlayWatchLive && config.InPlayWatchLive.enabled;
      }),
      switchMap((enabled: boolean) => {
        this.isWatchLiveEnabled = enabled;
        return enabled ? of(null) : this.inplayMainService.getRibbonData().pipe(takeUntil(this.unsubscribe));
      })
    ).subscribe((data: IRibbonCache) => {
      if (!this.isLiveStreamPage && data) {
        const firstSport = this.inplayMainService.getFirstSport(data.data);
        this.router.navigateByUrl(`/in-play/${firstSport.targetUriCopy}`);
        this.changeDetectorRef.detectChanges();
      }
    });

    this.showSpinner();
    this.changeDetectorRef.detectChanges();

    this.inplayMainService.getLiveStreamStructureData().subscribe((structureData) => {

      /**
       * Data for sport sections
       */
      this.data = <ISportSegment>structureData;

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

      this.pubsubService.subscribe(this.cSyncName, this.pubsubService.API.SESSION_LOGIN, () => {
        if (this.inplayMainService.isNewUserFromOtherCountry()) {
          this.reloadComponent();
          this.changeDetectorRef.detectChanges();
        }
      });

      this.hideSpinner();
      this.changeDetectorRef.detectChanges();
    }, () => {
      this.showError();
      this.changeDetectorRef.detectChanges();
    });
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe(this.cSyncName);
    this.inplayMainService.unsubscribeForUpdates();

    if (this.isLiveStreamPage) {
      this.inplayStorageService.destroySportsCache();
      this.inplayConnectionService.disconnectComponent();
    }

    this.unsubscribe.next();
    this.unsubscribe.complete();
  }
}
