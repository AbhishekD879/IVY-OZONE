import {
  Component, OnInit, Input, OnDestroy, OnChanges,Output,EventEmitter,
  ChangeDetectionStrategy, SimpleChanges, ChangeDetectorRef
} from '@angular/core';
import { FiveASideEntryInfoService } from '@app/fiveASideShowDown/services/fiveaside-entryInfo-handler.service';
import { IOutCome } from '@app/fiveASideShowDown/models/entry-information';
import { ENTRYINFO, GTM_EVENTS, LIVE_OVERLAY, PUBSUB_API, STATUS } from '@app/fiveASideShowDown/constants/constants';
import {
  FiveAsideLiveServeUpdatesSubscribeService
} from '@app/fiveASideShowDown/services/fiveaside-live-serve-updates-subscribe.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { ITeamColor } from '@app/fiveASideShowDown/models/team-color';
import { DeviceService } from '@app/core/services/device/device.service';

@Component({
  selector: 'fiveaside-entry-details',
  template: ``,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FiveASideEntryDetailsComponent implements OnInit, OnDestroy, OnChanges {

  @Input() outComes: Array<IOutCome>;
  @Input() isLeaderboard: boolean;
  @Input() eventStatus: string;
  @Input() entryId: string;
  @Input() isTopEntry:boolean;
  @Input() teamColors:ITeamColor[];
  @Input() hasTeamImage: boolean;
  @Output() readonly closeDetails: EventEmitter<boolean> = new EventEmitter<boolean>();
  data: Array<IOutCome>;
  outcomeIds: Array<string> = [];
  componentId: string;
  readonly status: { status: string } = ENTRYINFO.STATUS;
  readonly selectionStatus = STATUS;
  public origin: string = ENTRYINFO.DETAILS;
  constructor(public fiveASideEntryInfoService: FiveASideEntryInfoService,
    public pubsub: PubSubService, protected coreToolsService: CoreToolsService,
    public fiveAsideLiveServeUpdatesSubscribeService: FiveAsideLiveServeUpdatesSubscribeService,
    private changeDetectorRef: ChangeDetectorRef, private gtmService: GtmService,
    private windowRef:WindowRefService,private deviceService:DeviceService) { }

  ngOnInit() {
    this.componentId = this.coreToolsService.uuid();
    this.myEntryListenerForEntryExpansion();
    this.data = this.fiveASideEntryInfoService.outComesFormation(this.outComes);
    if (this.eventStatus === 'live') {
      this.pubsub.subscribe(this.componentId, PUBSUB_API.OUTCOME_CHANGES, this.outComeChangeUpdate.bind(this));
      this.getOutcomeIds();
    }
  }
  /**
   * this will get called when the outcome changes
   * @param  {{previous:Array<string>} update
   * @param  {Array<string>}} current
   */
  outComeChangeUpdate(update: { previous: Array<string>, current: Array<string> }) {
    this.outcomeIds = [];
    this.outcomeIds = update.current;
  }
  ngOnChanges(change: SimpleChanges) {
    if (change.outComes) {
      this.data = this.fiveASideEntryInfoService.outComesFormation(this.outComes);
    }
  }

  /**
   * @returns void
   */
  getOutcomeIds(): void {
    this.outComes.forEach((leg: IOutCome) => {
      this.outcomeIds.push(leg.outcomeId);
    });
  }
  
  /**
   * jumpToEntry
   * @returns void
   */
  jumpToEntry(): void {
    this.closeDetails.emit(true);
    let removepixel = 80;
    const headerElement = this.windowRef.document.querySelector('.header');
    const header = headerElement.getBoundingClientRect().height;
    if (this.isTopEntry) {
      this.hideEntryDetails();
    }
    this.pubsub.publish(PUBSUB_API.CLOSE_OVERLAY_MY_ENTRIES);
    const element: HTMLElement = this.windowRef.document.querySelector(`#entry_${this.entryId}`);
    if (this.deviceService.isDesktop) {
      this.desktopScroll(element, header);
    } else {
      removepixel = removepixel + header;
      this.windowRef.nativeWindow.scrollTo({ top: element.offsetTop - removepixel, behavior: 'smooth' });
    }
    this.trackGTMEvent(GTM_EVENTS.JUMP_TO_ENTRY.action, GTM_EVENTS.JUMP_TO_ENTRY.label, GTM_EVENTS.JUMP_TO_ENTRY.category);
  }
  /**
   * @returns void
   * Hide the entry details
   */
  hideEntryDetails(): void {
    const entryEl: HTMLElement = this.windowRef.document.querySelector('#entry-details');
    if (entryEl) {
      entryEl.style.display = 'none';
    }
  }
  /**
   * DesktopScroll
   * @param  {HTMLElement} element
   * @returns void
   */
  desktopScroll(element: HTMLElement, header: number): void {
    element && element.scrollIntoView({ block: 'start', inline: 'nearest' });
    const scrolledY = this.windowRef.nativeWindow.scrollY;
    if (scrolledY) {
      this.windowRef.nativeWindow.scrollTo({ top: (scrolledY - header), behavior: 'smooth' });
    }
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
  ngOnDestroy() {
    this.outComes = [];
    if (this.eventStatus === 'live') {
      this.pubsub.unsubscribe(this.componentId);
    }
    this.outcomeIds = [];
    this.data = [];
  }

  /**
   * Listener for My Entry expansion
   * @returns void
   */
  private myEntryListenerForEntryExpansion(): void {
    if (!this.isLeaderboard) {
      this.pubsub.publish(LIVE_OVERLAY.ENTRY_OPENED_TUTORIAL_OVERLAY, {data: true});
    }
  }
}
