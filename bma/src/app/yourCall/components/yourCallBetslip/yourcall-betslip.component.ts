import {
  Component, ElementRef, Input, OnDestroy, OnInit, ChangeDetectorRef, Output, EventEmitter
} from '@angular/core';
import { of, Subscription } from 'rxjs';
import { catchError, switchMap } from 'rxjs/operators';
import * as _ from 'underscore';

import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UserService } from '@core/services/user/user.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { YourcallBetslipService } from '@yourcall/services/yourcallBetslip/yourcall-betslip.service';
import { IRemoteBetslipBet } from '@core/services/remoteBetslip/remote-betslip.constant';
import { QuickbetDataProviderService } from '@app/core/services/quickbetDataProviderService/quickbet-data-provider.service';
import { YourcallMarketsService } from '@yourcall/services/yourCallMarketsService/yourcall-markets.service';
import { YourcallDashboardService } from '@yourcall/services/yourcallDashboard/yourcall-dashboard.service';
import { YourCallNotificationService } from '@yourcall/services/yourCallNotification/yourcall-notification.service';

import { DSBet } from '@yourcall/models/bet/ds-bet';
import { BYBBet } from '@yourcall/models/bet/byb-bet';
import { IYourcallSelectionUpdate } from '@yourcall/models/messages-data.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { IReference } from '@core/models/live-serve-update.model';
import { StorageService } from '@core/services/storage/storage.service';

@Component({
  selector: 'yourcall-betslip',
  templateUrl: 'yourcall-betslip.component.html'
})
export class YourcallBetslipComponent implements OnInit, OnDestroy {
  @Input() eventEntity: ISportEvent;
  @Input() bodyClass: string = 'yourcall-bs-opened';
  @Input() recalculatePositions: boolean = true;
  @Input() isFiveASideBet: boolean = false;
  @Input() betslipType: string;


  @Output() readonly closeBetReceipt: EventEmitter<void> = new EventEmitter();
  @Output() readonly closeQuickBet: EventEmitter<void> = new EventEmitter();
  @Output() readonly isBetReceipt: EventEmitter<void> = new EventEmitter();

  TABLET_BOTTOM_MENU_HEIGHT: number = 52;

  selectionData: DSBet | BYBBet = null;
  quickbetPlaceBetSubscriber: Subscription;
  panelTitle: string;
  leftBtnLocale: string;
  sticky: boolean;
  window: any;

  windowScrollListener: () => void;
  windowResizeListener: () => void;

  private isFixed: boolean;
  private detectListener;
  private resizeTimer: number;
  private resizeTimeout: number = 500;
  private removeEdpBybTabs: boolean;

  constructor(
    private deviceService: DeviceService,
    private windowRefService: WindowRefService,
    private elementRef: ElementRef,
    private rendererService: RendererService,
    private localeService: LocaleService,
    private pubsubService: PubSubService,
    private userService: UserService,
    private fracToDecService: FracToDecService,
    private domToolsService: DomToolsService,
    private yourcallBetslipService: YourcallBetslipService,
    private yourCallNotificationService: YourCallNotificationService,
    private yourcallDashboardService: YourcallDashboardService,
    private yourcallMarketsService: YourcallMarketsService,
    private quickbetDataProviderService: QuickbetDataProviderService,
    private changeDetectorRef: ChangeDetectorRef,
    public storageService: StorageService
  ) {
    this.window = this.windowRefService.nativeWindow;

    this.relocate = this.relocate.bind(this);
    this.ycOddsValue = this.ycOddsValue.bind(this);
    this.handlePanelRender = this.handlePanelRender.bind(this);
  }

  ngOnInit(): void {
    if (this.isFiveASideBet) {
      this.ycOddsValue = undefined;
    }
    this.changeDetectorRef.detach();
    this.detectListener = this.windowRefService.nativeWindow.setInterval(() => {
      this.changeDetectorRef.detectChanges();
    });

    if (!this.deviceService.isMobileOrigin || this.deviceService.isTablet) {
      this.windowScrollListener = this.rendererService.renderer.listen(this.window, 'scroll', this.relocate);

      this.windowResizeListener = this.rendererService.renderer.listen(this.window, 'resize', () => {
        this.isFixed = null;
        this.relocateAfter(this.resizeTimeout);
      });
    }

    this.panelTitle = this.localeService.getString(`yourCall.${this.isFiveASideBet ? 'fiveASideBetslipTitle' : 'yourCallBetslipTitle'}`);
    this.leftBtnLocale = this.localeService.getString('yourCall.back');

    this.pubsubService.subscribe('YourCallBetslip', this.pubsubService.API.ADD_TO_YC_BETSLIP, ycData => {
      Object.assign(ycData, {
        categoryId: this.eventEntity.categoryId,
        classId: this.eventEntity.classId
      });
      this.yourcallBetslipService.addSelection(ycData)
        .then((selection: DSBet | BYBBet) => {
          this.pubsubService.publish(this.pubsubService.API.YC_DASHBOARD_DISPLAYING_CHANGED, [false, true, () => {
            this.yourcallDashboardService.isBetslipLoading = false;
          }]);

          _.each(selection.selections, (sel: any) => {
            sel.betslipTitle = sel.getBetslipTitle();
          });

          selection.typeName = this.eventEntity.typeName;
          selection.categoryName = this.eventEntity.categoryName;
          this.selectionData = selection;
        })
        .catch((error: string) => {
          // TODO overall error state
          console.warn('Error in adding SGL selection', error);
        });
    });

    this.pubsubService.subscribe('YourCallBetslip', this.pubsubService.API.AFTER_PANEL_RENDER,
      this.handlePanelRender);

    this.pubsubService.subscribe('YourCallBetslip',
      this.pubsubService.API.YOURCALL_SELECTION_UPDATE,
      (updateData: IYourcallSelectionUpdate) => {
        const delta = updateData.odds - this.selectionData.betOdds;

        if (delta) {
          this.showPriceChangeWarning(updateData, delta);
        } else {
          this.clearPriceChangeWarning();
        }
      });

    this.pubsubService.subscribe('YourCallBetslip', this.pubsubService.API.MOVE_EVENT_TO_INPLAY, this.handleBybLiveEvent);

    // get bet data from quickbet panel and push sent result of place bet request
    this.placeBetListener();
  }

  ngOnDestroy(): void {
    this.windowScrollListener && this.windowScrollListener();
    this.windowResizeListener && this.windowResizeListener();

    this.pubsubService.unsubscribe('YourCallBetslip');
    this.removeSubscribers();

    this.windowRefService.nativeWindow.clearInterval(this.detectListener);
    this.windowRefService.nativeWindow.clearTimeout(this.resizeTimer);

    this.yourCallNotificationService.clear();
  }

  trackById(index, selection: IBetSelection): string {
    return `${selection.id} ${index}`;
  }

  showPriceChangeWarning(updateData: IYourcallSelectionUpdate, delta: number): void {
    const oddsFormat = this.userService.oddsFormat,
      odds = updateData.odds;

    if (!updateData.skipMessage) {
      this.yourCallNotificationService.saveErrorMessage(this.localeService.getString('yourCall.priceChangeWarning'), 'warning');
    }

    this.selectionData.price = {
      isPriceChanged: true,
      isPriceUp: delta > 0,
      isPriceDown: delta < 0
    };
    if (this.selectionData.newOddsValue) {
      this.selectionData.oldOddsValue = this.selectionData.newOddsValue;
    }
    this.selectionData.newOddsValue = oddsFormat === 'dec' ? odds : this.fracToDecService.decToFrac(odds);
    this.selectionData.onOddsChange(odds, this.fracToDecService.decToFrac(odds));
  }

  clearPriceChangeWarning(): void {
    this.yourCallNotificationService.clear();
    this.selectionData.price = {
      isPriceChanged: false,
      isPriceUp: false,
      isPriceDown: false
    };

    if (this.selectionData.newOddsValue) {
      this.selectionData.oldOddsValue = this.selectionData.newOddsValue;
    }
    this.selectionData.newOddsValue = null;
  }

  /**
   * Recalculate dashboard position and dimensions
   */
  relocate(): void {
    if (this.deviceService.isMobileOrigin && !this.deviceService.isTablet) {
      return;
    }

    const container = this.elementRef.nativeElement;
    const panel = container.querySelector('.quickbet-panel');

    if (!panel) {
      return;
    }

    const windowHeight = this.window.innerHeight || 0;
    const windowYOffset = this.window.pageYOffset || 0;
    const containerWidth = this.domToolsService.getWidth(container);
    const panelHeight = this.domToolsService.getHeight(panel) || 0;
    const panelOffset = this.domToolsService.getOffset(container).top || 0;
    const panelBottom = this.deviceService.isDesktop || this.deviceService.isMobile ? 0 : this.TABLET_BOTTOM_MENU_HEIGHT;

    this.sticky = this.deviceService.isMobile || panelOffset + panelHeight + panelBottom > windowHeight + windowYOffset;

    if (this.sticky && !this.isFixed) {
      this.domToolsService.css(panel, {
        position: 'fixed',
        left: this.recalculatePositions ? container.getBoundingClientRect().left : 0,
        bottom: this.recalculatePositions ? panelBottom : 0,
        width: containerWidth
      });

      this.isFixed = true;
    }

    if (!this.sticky) {
      this.domToolsService.css(panel, {
        position: 'relative',
        left: 'auto',
        bottom: 'auto',
        width: '100%'
      });

      this.isFixed = false;
    }
  }

  /**
   * Place bet method to pass to quickbet panel
   */
  placeBet(): void {
    this.clearPriceChangeWarning();
  }

  /**
   * Close betreceipt or bestlip but leave selections in dashboard
   */
  closePanel(isBetReceipt: boolean): void {
    this.yourcallDashboardService.clear();
    this.yourcallBetslipService.removeSelection();
    this.yourcallMarketsService.removeSelectedValues();
    this.selectionData = null;
    this.pubsubService.publish(this.pubsubService.API.YC_DASHBOARD_DISPLAYING_CHANGED, false);
    this.removeSubscribers();
    if (isBetReceipt) {
      this.closeBetReceipt && this.closeBetReceipt.emit();
    }
  }

  /**
   * Close and remove all selections
   */
  reuseSelection(): void {
    this.yourcallDashboardService.calculateOdds();
    this.yourcallBetslipService.removeSelection();
    this.selectionData = null;
    this.closeQuickBet && this.closeQuickBet.emit();
    this.pubsubService.publish(this.pubsubService.API.YC_DASHBOARD_DISPLAYING_CHANGED, true);

    // remove byb and 5aside tabs from edp when quickbet closed and event is live
    this.removeEdpBybTabs && this.pubsubService.publish(this.pubsubService.API.REMOVE_EDP_BYB_TABS);
  }

  onQuickbetEvent(event: { output: string, value: boolean }): void {
    if (event.output === 'reuseSelectionFn') {
      this.reuseSelection();
    } else if (event.output === 'closePanelFn') {
      this.closePanel(event.value);
    } else if (event.output === 'placeBetFn') {
      this.placeBet();
    }
  }

  ycOddsValue(): number | string {
    return this.yourcallDashboardService.odds;
  }

  private placeBetListener(): void {
    this.removeSubscribers();
    this.quickbetPlaceBetSubscriber = this.quickbetDataProviderService.quickbetPlaceBetListener
      .pipe(switchMap((bet: IRemoteBetslipBet) => {
        return this.yourcallBetslipService.placeBet(bet, this.eventEntity, this.selectionData);
      }),
      catchError((errorMessage: string) => {
        this.quickbetDataProviderService.quickbetReceiptListener.next([{ error: errorMessage }]);
        this.placeBetListener();
        return of(null);
      }))
      .subscribe((result: any) => {
        this.pubsubService.publish(this.pubsubService.API.BETS_COUNTER_PLACEBET);
        if (result) {
          const mybets = result.data;
          mybets.isquickbet = true;
          mybets.id = mybets.betId;
          this.pubsubService.publishSync(this.pubsubService.API.MY_BET_PLACED, mybets);
          this.isBetReceipt.emit();
          this.pubsubService.publish(this.pubsubService.API.STORE_FREEBETS);
          this.quickbetDataProviderService.quickbetReceiptListener.next({ data: result.data, selection: this.selectionData });
               /**
        * set event id to Local storage when placed a bet
        */
          let signPostData = this.storageService.get('myBetsSignPostingData');
          if (signPostData?.length > 0) {
            const eventIndex = signPostData.findIndex(data => Number(data.eventId) === Number(this.eventEntity.id));
            if(eventIndex > -1) {
              const betIndex = signPostData[eventIndex].betIds.findIndex(id => Number(id) == Number(mybets.id));
              if(betIndex < 0) {
                signPostData[eventIndex].betIds.push(mybets.id);
              }
              const eventObj = {'eventId' : this.eventEntity.id, 'betIds': [mybets.id]};
              signPostData.push(eventObj);
            }
            this.storageService.set('myBetsSignPostingData', signPostData);
          } else {
            signPostData = [{'eventId' : this.eventEntity.id, 'betIds': [mybets.id]}];
            this.storageService.set('myBetsSignPostingData', signPostData);
          }
     
        }
        this.removeSubscribers();
      });
  }

  private removeSubscribers(): void {
    this.quickbetPlaceBetSubscriber && this.quickbetPlaceBetSubscriber.unsubscribe();
  }

  private relocateAfter(delay: number = 0): void {
    this.windowRefService.nativeWindow.clearTimeout(this.resizeTimer);
    this.resizeTimer = this.windowRefService.nativeWindow.setTimeout(this.relocate, delay);
  }

  /**
   * Handles pubsub "AFTER_PANEL_RENDER" event when BYB Quickbet panel was opened.
   */
  private handlePanelRender(): void {
    this.isFixed = null;
    this.placeBetListener();
    this.relocateAfter();
  }

  private handleBybLiveEvent = (event: IReference) => {
    if (this.selectionData && this.selectionData.eventId === event.id) {
      // when event goes live - disable selection and show suspended message
      this.selectionData.disabled = true;
      this.removeEdpBybTabs = true;
      this.yourCallNotificationService.saveErrorMessage(
        this.localeService.getString('quickbet.betPlacementErrors.EVENT_SUSPENDED'), 'warning' );
      this.changeDetectorRef.detectChanges();
    }
  }
}
