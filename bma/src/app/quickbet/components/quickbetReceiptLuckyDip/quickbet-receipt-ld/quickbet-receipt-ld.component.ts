import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { StorageService } from '@core/services/storage/storage.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { UserService } from '@core/services/user/user.service';
import { LuckyDipCMSService } from '@lazy-modules/luckyDip/services/luckyDip-cms.service';
import { quickbetConstants } from '@app/quickbet/constants/quickbet.constant';
import { IQuickbetReceiptDetailsModel } from '@app/quickbet/models/quickbet-receipt.model';
import { IBetTag } from '@app/betHistory/models/bet-history.model';
import { IConstant } from '@core/services/models/constant.model';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'quickbet-receipt-ld',
  templateUrl: './quickbet-receipt-ld.component.html',
  styleUrls: ['./quickbet-receipt-ld.component.scss']
})
export class QuickbetReceiptLdComponent implements OnInit, OnDestroy {
  @Input() winAlertsEnabledLD: boolean;
  quickbetConstants: IConstant;
  odds: string;
  amount: string;
  potential: string;
  winAlertsBet: string;
  winAlertsReceiptId: string;
  playerDescription: string;
  outcomeDescriptionText: string = quickbetConstants.LD_TO_WIN;
  winAlertsActive: boolean;
  receiptData: IQuickbetReceiptDetailsModel;

  constructor(
    private user: UserService,
    private window: WindowRefService,
    private storageService: StorageService,
    private nativeBridge: NativeBridgeService,
    private ldCmsService: LuckyDipCMSService,
    protected pubsub:PubSubService
  ) {
    this.quickbetConstants = quickbetConstants;
  }

  ngOnInit(): void {
    this.getLdReceiptData();
  }

  ngOnDestroy(): void {
    this.ldCmsService.isLuckyDipReceipt.next({} as any);
  }

  /**
   * to toggle win alerts
   * @param {boolean} event
   * @returns {void}
   */
  toggleWinAlerts(event: boolean): void {
    if (this.window.nativeWindow.NativeBridge.pushNotificationsEnabled) {
      if (event) {
        const receiptId = this.receiptData.receipt.id;
        if (!this.user.winAlertsToggled) {
          this.user.set({ winAlertsToggled: true });
        }
        if (!this.winAlertsReceiptId) {
          this.winAlertsReceiptId = receiptId;
        }
        this.winAlertsBet = receiptId;
        this.storageService.set(this.quickbetConstants.LD_WINALERTS_ENABLED, true);
      } else {
        this.winAlertsBet = null;
        this.storageService.set(this.quickbetConstants.LD_WINALERTS_ENABLED, false);
      }
    }
  }

  /**
   * to show win alerts toolTip
   * @returns {boolean}
   */
  winAlertsTooltipLD(): boolean {
    const MAX_VIEWS_COUNT = 1;
    const tooltipData = this.storageService.get(this.quickbetConstants.LD_TOOLTIPS) || {};
    return (
      (tooltipData[`receiptViewsCounter-${this.user.username}`] || null) <=
      MAX_VIEWS_COUNT && !this.user.winAlertsToggled
    );
  }

  /**
   * check if it is an app wrapper
   * @returns {boolean}
   */
  isNativeBridge(): boolean {
    return this.nativeBridge.isWrapper;
  }
  /**
   * get Initial ld receipt data
   * @returns {void}
   */
  private getLdReceiptData(): void {
    this.ldCmsService.isLuckyDipReceipt.subscribe((receiptData: any) => {
      let isLD: boolean = false;
      if (receiptData && receiptData.betTags && receiptData.betTags.betTag) {
        isLD = (receiptData.betTags.betTag.find((tag: IBetTag) => tag.tagName === this.quickbetConstants.LD_TAG)) ? true : false;
      }
      if (isLD) {
        this.receiptData = receiptData;
        this.playerDescription = this.receiptData.legParts[0].outcomeDesc + this.outcomeDescriptionText;
        this.odds = this.receiptData.price.priceNum + this.quickbetConstants.LD_ODD_SYMBOL + this.receiptData.price.priceDen;
        this.amount = this.user.currencySymbol + this.receiptData.stake.amount;
        this.potential = this.user.currencySymbol + this.receiptData.payout.potential;
        this.winAlertsActive = this.storageService.get(this.quickbetConstants.LD_WINALERTS_ENABLED);
        this.winAlertsReceiptId = this.receiptData.receipt.id;
      }
    });
  }
}
