import { catchError, finalize, concatMap } from 'rxjs/operators';
import { forkJoin as observableForkJoin, Observer, Observable, of as observableOf } from 'rxjs';
import { Component, OnDestroy, OnInit, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import * as _ from 'underscore';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { inplayConfig } from '@app/inPlay/constants/config';
import { InplayMainService } from '@inplayModule/services/inplayMain/inplay-main.service';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';

@Component({
  selector: 'inplay-all-sports-page',
  templateUrl: 'inplay-all-sports-page.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class InplayAllSportsPageComponent extends AbstractOutletComponent implements OnInit, OnDestroy {

  expandedLeaguesCount: number;
  data: ISportSegment;

  /**
   * Name for Connect.sync fileName
   */
  cSyncName: string = `inplayAllSportsPage`;
  ssError: boolean;

  /**
   * Expanded Sports Count for SPORTS SECTIONS
   * @member {Number}
   */
  expandedSportsCount: number = inplayConfig.expandedSportsCount;

  /**
   * View Filters used for clearDeletedEventFromSport functionality.
   */
  viewByFilters: string[] = inplayConfig.viewByFilters;

  constructor(
    protected pubsubService: PubSubService,
    protected inplayMainService: InplayMainService,
    protected cms: CmsService,
    protected inPlayConnectionService: InplayConnectionService,
    protected changeDetector: ChangeDetectorRef
  ) {
    super();
  }

  ngOnInit(): void {
    const systemConfigObservable = this.cms.getSystemConfig(false);
    const structureDataObservable = Observable.create((observer: Observer<void>) => {
      const isValid = this.inplayMainService.getSportUri();
      if (isValid) {
        observer.error(null);
        observer.complete();
      }
      observer.next(null);
      observer.complete();
    }).pipe(concatMap(() => {
      return this.inplayMainService.getStructureData().pipe(
        catchError(() => {
          return observableOf([]);
        })
      );
    }));

    observableForkJoin([systemConfigObservable, structureDataObservable])
      .pipe(
        finalize(() => {
          this.addEventListeners();
          this.hideSpinner();
          this.changeDetector.detectChanges();
        }))
      .subscribe((data:any) => {
        const systemConfig = data[0];
        const structureData = data[1];

        this.expandedLeaguesCount = systemConfig.InPlayCompetitionsExpanded.competitionsCount;

        /**
         * Data for sport sections
         */
        this.data = structureData;

        /**
         * Error on SiteServer error
         * @type {boolean}
         */
        this.ssError = !structureData || _.isEmpty(structureData) || _.has(structureData, 'error');
      }, () => {
        this.data = {} as ISportSegment;
        this.ssError = true;
      });
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe(this.cSyncName);
  }

  reloadComponent(): void {
    this.inPlayConnectionService.setConnectionErrorState(false);
    super.reloadComponent();
  }

  protected addEventListeners(): void {
    /**
     * Adding callback for update section removing on LiveUpdate displayed - N
     */
    this.pubsubService.subscribe(this.cSyncName, this.pubsubService.API.DELETE_EVENT_FROM_CACHE, (eventId: number) => {
      this.inplayMainService.clearDeletedEventFromSport(this.data, eventId, this.viewByFilters);
      this.changeDetector.detectChanges();
    });

    this.pubsubService.subscribe(this.cSyncName, this.pubsubService.API.RELOAD_IN_PLAY, () => {
      this.reloadComponent();
      this.changeDetector.detectChanges();
    });
  }
}
