import { Component, EventEmitter, Input, OnInit, Output, OnDestroy } from '@angular/core';
import { RendererService } from '@app/shared/services/renderer/renderer.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { trigger, transition, style, animate, state, keyframes } from '@angular/animations';
import { FiveASideEntryInfoService } from '@app/fiveASideShowDown/services/fiveaside-entryInfo-handler.service';
import { IEntrySummaryInfo } from '@app/fiveASideShowDown/models/entry-information';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { ITeamColor } from '@app/fiveASideShowDown/models/team-color';
import { PUBSUB_API } from '@app/fiveASideShowDown/constants/constants';

@Component({
  selector: 'fiveaside-entrylist-overlay',
  template: ``,
  animations: [trigger('overlay', [
    state('in', style({ transform: 'translateY(0)' })),
    transition('void => *', [
      animate(
        500,
        keyframes([
          style({ opacity: 1, transform: 'translateY(800px)', offset: 0 }),
          style({ opacity: 1, transform: 'translateY(400px)', offset: 0.5 }),
          style({ opacity: 1, transform: 'translateY(0)', offset: 1.0 })
        ])
      )
    ])
  ])]
})
export class FiveASideEntryListOverlayComponent implements OnInit, OnDestroy {
  @Output() readonly clearOverlay = new EventEmitter();
  @Input() myEntriesList: Array<IEntrySummaryInfo>;
  @Input() eventStatus: string;
  @Input() teamColors:ITeamColor[];
  @Input() hasTeamImage: boolean;
  public entries: Array<IEntrySummaryInfo>;
  public homeBody: Element;
  public fiveASideOverlay: Element;
  public next: number = 0;
  public componentId: string;
  public staggering: Array<IEntrySummaryInfo> = [];
  private contentOverlayClassName: string = 'fiveasideentry-content-overlay';

  constructor(protected fiveASideEntryInfoService: FiveASideEntryInfoService,
    protected rendererService: RendererService, protected coreToolsService: CoreToolsService,
    protected windowRef: WindowRefService, protected deviceService: DeviceService, protected pubsub: PubSubService) {
  }

  ngOnInit() {
    this.componentId = this.coreToolsService.uuid();
    this.initElements();
    this.entries = this.myEntriesList;
    this.doNext();
    this.pubsub.subscribe(this.componentId, PUBSUB_API.CLOSE_OVERLAY_MY_ENTRIES, this.close.bind(this));
  }

  ngOnDestroy() {
    this.pubsub.unsubscribe(this.componentId);
  }

  /**
   * doNext for animation experience
   */
  doNext(): void {
    if (this.next < this.entries.length) {
      this.staggering.push(this.entries[this.next++]);
    }
  }
  /**
   * Close Overlay
   * @returns void
   */
  close(): void {
    !this.homeBody && this.getBody();
    this.rendererService.renderer.removeClass(this.homeBody, this.contentOverlayClassName);
    !this.fiveASideOverlay && this.getfiveASideOverlay();
    this.rendererService.renderer.removeClass(this.fiveASideOverlay, 'active');
    this.clearOverlay.emit();
  }
  /**
   * getBody
   * @returns void
   */
  protected getBody(): void {
    this.homeBody = this.deviceService.isWrapper ?
      this.windowRef.document.querySelector('body') : this.windowRef.document.querySelector('html, body');
  }

  /**
   * Init Elements to start OverLay
   * @returns void
   */
  private initElements(): void {
    this.getBody();
    this.getfiveASideOverlay();
    this.rendererService.renderer.addClass(this.fiveASideOverlay, 'active');
    this.rendererService.renderer.addClass(this.homeBody, this.contentOverlayClassName);
  }

  /**
   * getfiveASideOverlay
   * @returns void
   */
  private getfiveASideOverlay(): void {
    this.fiveASideOverlay = this.windowRef.document.getElementById('fiveaside-entry-overlay');
  }
}
