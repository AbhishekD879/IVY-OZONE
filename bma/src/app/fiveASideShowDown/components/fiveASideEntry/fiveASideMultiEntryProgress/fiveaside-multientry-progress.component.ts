import { trigger, transition, style, animate } from '@angular/animations';
import { Component, ViewChild, ElementRef, AfterViewInit,
  Input, OnChanges, OnInit, SimpleChanges, ChangeDetectorRef } from '@angular/core';
import { IEntrySummaryInfo } from '@app/fiveASideShowDown/models/entry-information';
import { IShowDown } from '@app/fiveASideShowDown/models/show-down';
import { GTM_EVENTS, MULTI_PROGRESS_COLOURS, PUBSUB_API } from '@app/fiveASideShowDown/constants/constants';
import { IPrize } from '@app/fiveASideShowDown/models/IPrize';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { ITeamColor } from '@app/fiveASideShowDown/models/team-color';
@Component({
  selector: 'fiveaside-multientry-progress',
  templateUrl: './fiveaside-multientry-progress.component.html',
  styleUrls: ['./fiveaside-multientry-progress.component.scss'],
  animations: [trigger('myInsertMultiRemoveTrigger', [
    transition(':enter', [style({ marginLeft: '0%' }), animate(1000)])
  ])]
})
export class FiveASideMultiEntryProgressComponent implements AfterViewInit, OnInit, OnChanges {
  @ViewChild('inputElement') inputElement: ElementRef;
  @Input() myEntriesList: Array<IEntrySummaryInfo>;
  @Input() contestInfo: IShowDown;
  @Input() prize: IPrize;
  @Input() eventStatus: string;
  @Input() teamColors:ITeamColor[];
  @Input() hasTeamImage: boolean;
  public openAllMyEntries: boolean;
  public winningPercentage: number;
  public losingpercentage: number;
  componentId: string;
  isDisabled: boolean = false;
  entriesList: Array<IEntrySummaryInfo>;
  constructor(private pubsub: PubSubService, protected coreToolsService: CoreToolsService,
    private gtmService: GtmService, private changeDetectorRef: ChangeDetectorRef) {
  }

  ngOnInit() {
    this.componentId = this.coreToolsService.uuid();
    this.updateRankEntryProgress(this.myEntriesList);
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.myEntriesList && !changes.myEntriesList.isFirstChange()) {
      this.updateRankEntryProgress(this.myEntriesList);
    }
  }
  /**
   * @param  {Array<IEntrySummaryInfo>} myEntryList
   * @returns void
   */
  updateRankEntryProgress(myEntryList: Array<IEntrySummaryInfo>): void {
    myEntryList.forEach((entrySummary: IEntrySummaryInfo) => {
      entrySummary.rankProgress = 100 -
        (Number((Math.floor((Number(this.parserank((entrySummary.rank as string).toString())) / Number(this.contestInfo.contestSize)) * 100))));
        entrySummary.rankProgress = entrySummary.rankProgress > 99 ? 99 : entrySummary.rankProgress;
    });
    this.entriesList = myEntryList;
    this.changeDetectorRef.markForCheck();
  }

  /**
   * @param  {any} rank
   * Changes the '1=' to '1'
   * @returns string
   */
  parserank(rank: string): string {
    return rank.split('=')[0];
  }
  ngAfterViewInit() {
    const totalCount = this.contestInfo.contestSize;
    const totalWinnings = Number(this.prize.totalPrizes);
    const totalpercentage = 100;
    this.winningPercentage = Math.floor((totalWinnings / totalCount) * totalpercentage);
    this.winningPercentage = this.winningPercentage > 100 ? 100 : this.winningPercentage;
    this.losingpercentage = (totalpercentage - this.winningPercentage);
    this.inputElement.nativeElement.style.background =
      `linear-gradient(to right,${MULTI_PROGRESS_COLOURS.lostcolor} 0%,
        ${MULTI_PROGRESS_COLOURS.lostcolor} ${this.losingpercentage}%,
        ${MULTI_PROGRESS_COLOURS.winnigcolor} ${this.losingpercentage}%,
        ${MULTI_PROGRESS_COLOURS.winnigcolor} ${totalpercentage}%)`;
    this.isDisabled = true;
  }
  /**
   * Widget Click
   * @returns void
   */
  widgetClick(): void {
    if (this.myEntriesList && this.myEntriesList.length > 1) {
      window.scroll(0, 0);
      this.openAllMyEntries = true;
      this.pubsub.publish(PUBSUB_API.CLOSE_EVERY_ENTRY_DETAILS);
      this.trackGTMEvent(GTM_EVENTS.POSITION_SUMMARY_WIDGET.action,
        GTM_EVENTS.POSITION_SUMMARY_WIDGET.label, GTM_EVENTS.POSITION_SUMMARY_WIDGET.category);
    }
  }
  /**
   * Clear Overlay
   * @returns void
   */
  overlayClear(): void {
    this.openAllMyEntries = false;
  }
  /**
   * @param  {string} eventAction
   * @param  {string} eventLabel
   * @param  {string} eventCategory
   * @returns void
   */
  trackGTMEvent(eventAction: string, eventLabel: string, eventCategory: string): void {
    this.gtmService.push('trackEvent', { eventCategory, eventAction, eventLabel });
  }
}
