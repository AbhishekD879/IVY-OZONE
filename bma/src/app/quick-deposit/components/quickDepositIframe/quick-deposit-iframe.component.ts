import {
  Component,
  Input,
  Output,
  OnInit,
  OnDestroy,
  OnChanges,
  EventEmitter,
  SimpleChanges,
  ViewChild,
  ElementRef,
  HostListener
} from '@angular/core';
import { SafeResourceUrl } from '@angular/platform-browser';
import { Subscription } from 'rxjs';
import { QuickDepositIframeService } from '@quickDepositModule/services/quick-deposit-iframe.service';
import { IEvent } from '@quickDepositModule/components/quickDepositIframe/quick-deposit-event.model';
import { QUICK_DEPOSIT_IFRAME_CONSTANTS } from '@quickDepositModule/constants/quick-deposit-iframe.constants';
import { ISuspendedOutcomeError } from '@betslipModule/models/suspended-outcome-error.model';
import { VanillaAuthService } from '@vanillaInitModule/services/vanillaAuth/vanilla-auth.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { DeviceService } from '@core/services/device/device.service';

@Component({
  selector: 'quick-deposit-iframe',
  styleUrls: ['./quick-deposit-iframe.component.scss'],
  templateUrl: './quick-deposit-iframe.component.html'
})

export class QuickDepositIframeComponent implements OnInit, OnDestroy, OnChanges {
  @ViewChild('iframe', {static: false}) iframe: ElementRef;
  @Input() showPriceChangeNotification = false;
  @Input() showSuspendedNotification = false;
  @Input() estimatedReturn: number;
  @Input() estimatedReturnAfterPriceChange: number;
  @Input() placeSuspendedErr: ISuspendedOutcomeError;
  @Input() priceChangeBannerMsg: string;
  @Input() isLuckyDip: boolean;
  @Output() readonly closeWindow: EventEmitter<any> = new EventEmitter();
  @Output() readonly closeIframeEmit: EventEmitter<any> = new EventEmitter();
  @Output() readonly openIframeEmit: EventEmitter<any> = new EventEmitter();
  @Output() readonly quickDepositStakeChange: EventEmitter<any> = new EventEmitter();

  showContent = false;
  frameHeight: number;
  frameMaxHeight: number;
  url: SafeResourceUrl;
  errorMsg: { type: string, msg: string };
  isQuickDepositEnabled = false;
  private originalStake: number;
  private isEnabledSubscription: Subscription;
  private eventsToSend: IEvent[] = [];

  constructor(
    private quickDepositIframeService: QuickDepositIframeService,
    private vanillaAuthService: VanillaAuthService,
    private domToolsService: DomToolsService,
    private windowRefService: WindowRefService,
    private deviceService: DeviceService
  ) {}

  ngOnInit(): void {
    this.isEnabledSubscription = this.quickDepositIframeService.isEnabled().subscribe((isEnabled) => {
      this.isQuickDepositEnabled = isEnabled;
      if (isEnabled) {
        this.url = this.quickDepositIframeService.getUrl(this.stake, this.estimatedReturn);
      } else {
        this.redirectToDepositPage();
      }
    }, () => {
      this.redirectToDepositPage();
    });
  }

  ngOnDestroy(): void {
    this.isEnabledSubscription.unsubscribe();
  }

  ngOnChanges(changes: SimpleChanges): void {
    const { stake, placeSuspendedErr, estimatedReturnAfterPriceChange } = changes;
    if (stake && stake.previousValue !== undefined && !(placeSuspendedErr && placeSuspendedErr.currentValue)) {
      this.handleStakeChange();
    }

    if (estimatedReturnAfterPriceChange && estimatedReturnAfterPriceChange.currentValue !== undefined) {
      this.handlePriceChange(this.estimatedReturnAfterPriceChange);
    }

    if (placeSuspendedErr && placeSuspendedErr.currentValue !== undefined &&
      placeSuspendedErr.currentValue.msg !== placeSuspendedErr.previousValue.msg) {
      this.handleSuspendedChange(!!changes.placeSuspendedErr.currentValue.msg);
    }
  }

  get stake(): number {
    return this.originalStake;
  }

  @Input('stake')
  set stake(value: number) {
    this.originalStake = value * 100;
  }

  /**
   * emits event in order to close quick deposit window
   */
  closeIFrameQD(): void {
    this.vanillaAuthService.refreshBalance().then(() => {
      this.showContent = false;
      this.closeWindow.emit(null);
    });
  }

  /**
   * listener for post messages from quick deposit iframe
   * @param event
   */
  @HostListener('window:message', ['$event'])
  onMessage(event: MessageEvent): void {
    this.handleMessage(event);
  }

  /**
   * defines action and calls corresponding action handler
   * @param event
   */
  handleMessage(event: MessageEvent): void {
    const action = this.getEventAction(event);
    switch (action) {
      case QUICK_DEPOSIT_IFRAME_CONSTANTS.ACTIONS.OPEN:
        this.openIFrame();
        break;
      case QUICK_DEPOSIT_IFRAME_CONSTANTS.ACTIONS.CLOSE:
        this.closeIFrame();
        break;
      case QUICK_DEPOSIT_IFRAME_CONSTANTS.ACTIONS.RESIZE:
        this.resizeIFrame(event);
        break;
      default:
        break;
    }
  }

  /**
   * redirects to deposit page
   */
  private redirectToDepositPage(): void {
    this.quickDepositIframeService.redirectToDepositPage();
  }

  /**
   * gets action from event
   * @param data
   */
  private getEventAction({ data }: MessageEvent): string {
    return unescape(data).split('&')[0].split('=')[1];
  }


  /**
   * makes iframe visible when content is loaded
   */
  private openIFrame(): void {
    this.showContent = true;
    this.sendPendingPostMessages();
    if (this.openIframeEmit.observers.length) {
      this.openIframeEmit.emit();
    }
  }

  /**
   * closes iframe after successful deposit
   */
  private closeIFrame(): void {
    this.vanillaAuthService.refreshBalance().then(() => {
      this.showContent = false;
      this.closeIframeEmit.emit();
    });
  }

  /**
   * sets correct height for iframe
   * @param data
   */
  private resizeIFrame({ data }: MessageEvent): void {
    const quickDepositHeader = this.windowRefService.document.querySelector('.quick-deposit__header');
    const heightStr = unescape(data).split('&')[2].split('=')[1];
    const bodyHeight = this.getBodyPortraitHeight();
    const appHeaderHeight = this.domToolsService.getHeight(this.domToolsService.HeaderEl);
    const quickDepositHeaderHeight = this.domToolsService.getHeight(quickDepositHeader);
    this.frameHeight = parseInt(heightStr, 10);
    this.frameMaxHeight = bodyHeight - appHeaderHeight - quickDepositHeaderHeight;
  }

  private getBodyPortraitHeight(): number {
    return this.deviceService.isPortraitOrientation ?
      this.domToolsService.getHeight(this.windowRefService.document.body) :
      this.domToolsService.getWidth(this.windowRefService.document.body);
  }

  /**
   * sends StakeChange post message with updated stake and estimated return to quick deposit iframe
   */
  private handleStakeChange(): void {
    const event = this.getEventObj(QUICK_DEPOSIT_IFRAME_CONSTANTS.EVENTS.STAKE_CHANGE);
    this.sendPostMessageToIFrame(event);
    if (this.quickDepositStakeChange.observers.length) {
      this.quickDepositStakeChange.emit(null);
    }
  }

  /**
   * sends PriceChange post message with updated stake and estimated return to quick deposit iframe
   */
  private handlePriceChange(estimatedReturn: number): void {
    const event = this.getEventObj(QUICK_DEPOSIT_IFRAME_CONSTANTS.EVENTS.PRICE_CHANGE, estimatedReturn);
    this.sendPostMessageToIFrame(event);
  }

  /**
   * sends SuspendedChange post message with updated stake and estimated return to quick deposit iframe
   * @param isSuspended
   */
  private handleSuspendedChange(isSuspended: boolean): void {
    const eventName = isSuspended ?
      QUICK_DEPOSIT_IFRAME_CONSTANTS.EVENTS.SUSPENDED :
      QUICK_DEPOSIT_IFRAME_CONSTANTS.EVENTS.UNSUSPENDED;
    const event = this.getEventObj(eventName, 0, false);
    this.sendPostMessageToIFrame(event);
  }

  /**
   * returns event object which should be sent in post message
   * @param eventName
   * @param passData
   */
  private getEventObj(eventName: string, estimatedReturn = 0, passData = true): IEvent {
    const estReturn = (estimatedReturn || this.estimatedReturn) * 100;
    return passData ? { eventName, eventData: {
        stake: this.stake,
        estimatedReturn: estReturn
      }
    } : { eventName };
  }

  /**
   * sends event to quick deposit iframe
   * @param event
   */
  private sendPostMessageToIFrame(event: IEvent): void {
    if (this.showContent) {
      this.iframe.nativeElement.contentWindow.postMessage(JSON.stringify(event), '*');
    } else {
      this.eventsToSend.push(event);
    }
  }

  private sendPendingPostMessages(): void {
    this.eventsToSend.length && this.eventsToSend.forEach((event: IEvent) => this.sendPostMessageToIFrame(event));
    this.eventsToSend.length = 0;
  }
}
