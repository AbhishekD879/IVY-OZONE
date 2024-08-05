import { Component, Input } from '@angular/core';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ToteBetslipService } from '@app/betslip/services/toteBetslip/tote-betslip.service';
import { DeviceService } from '@core/services/device/device.service';
import { IToteBet, IToteBetDetails } from '@app/betslip/services/toteBetslip/tote-betslip.model';
import { StorageService } from '@core/services/storage/storage.service';
import { ToteBetReceiptService } from '@app/betslip/services/toteBetReceipt/tote-bet-receipt.service';
import { IPoolBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { UserService } from '@core/services/user/user.service';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISvgItem, ISystemConfig } from '@app/core/services/cms/models';
import { IBsReceiptBannerImages } from '@app/betslip/models/betslip-receipt-banner-data.model';
import { GtmService } from '@core/services/gtm/gtm.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';

@Component({
  selector: 'tote-bet-receipt',
  templateUrl: './tote-bet-receipt.component.html',
  styleUrls: ['./tote-bet-receipt.component.scss'],
})
export class ToteBetReceiptComponent {
  @Input() bsReceiptBannerImages: IBsReceiptBannerImages[] = [];
  
  toteBetDetails: IToteBetDetails;
  loadComplete: boolean;
  loadFailed: boolean;
  receipts: IPoolBetDetail[];
  totalStake: number;
  totalFreebetStake?: number;
  userCurrencySymbol: string;
  poolCurrencyCode: string;
  betDate: string;
  isTablet: boolean;
  isSportIconEnabled: boolean;

  private toteBet: IToteBet;

  constructor(
    private pubSubService: PubSubService,
    private deviceService: DeviceService,
    private toteBetslip: ToteBetslipService,
    private storageService: StorageService,
    private toteBetReceiptService: ToteBetReceiptService,
    private userService: UserService,
    private cmsService: CmsService,
    protected gtmService: GtmService,
    protected window: WindowRefService
  ) {
    this.toteBet = this.getToteBet();
    this.toteBetDetails = this.toteBet.toteBetDetails;
    this.poolCurrencyCode = this.toteBet.poolCurrencyCode;
    this.userCurrencySymbol = this.userService.currencySymbol;
    this.isTablet = this.deviceService.isTablet;
    this.setSvgId();
    this.getToteBetReceipt();
  }

  /**
   * Close bet slip
   */
  done(): void {
    this.pubSubService.publish(this.pubSubService.API.HOME_BETSLIP);
    if (this.deviceService.isMobile) {
      // sync to `show-${scope.sideClass}` in sidebar.js
      this.pubSubService.publish(this.pubSubService.API['show-slide-out-betslip'], false);
    }
  }

  /**
   * Add selections one more time to betslip
   */
  reuse(): void {
    const poolData = this.toteBet;
    if(poolData.poolBet.freebetTokenId) {
      delete poolData.poolBet.freebetTokenId
    }
    if(poolData.poolBet.freebetTokenValue) {
      delete poolData.poolBet.freebetTokenValue
    }
    
    this.toteBetslip.addToteBet(this.toteBet, poolData);
    this.pubSubService.publish(this.pubSubService.API.REUSE_TOTEBET);
    this.pubSubService.publish(this.pubSubService.API.HOME_BETSLIP);
  }

  private getToteBetReceipt(): void {
    this.toteBetReceiptService.getToteBetReceipt().subscribe((data: IPoolBetDetail[]) => {
      const totePoolBetDetail: IPoolBetDetail = _.first(data);
      this.receipts = data;
      this.betDate = totePoolBetDetail.date;
      this.totalStake = Number(this.receipts[0].stake) - Number(this.toteBetslip.getTokenValue());
      this.totalFreebetStake = Number(this.toteBetslip.getTokenValue());
      // Hide spinner
      this.loadComplete = true;
      this.toteBetslip.removeToteBet(false, true);
    }, () => {
      this.loadComplete = true;
      this.loadFailed = true;
    });
  }

  /**
   * Gets tote bet
   * @return {object} - tote Bet
   */
  private getToteBet(): IToteBet | null {
    return this.storageService.get('toteBet') || null;
  }
  /**
   * Sets Sport icon svg id to leg
   */
  private setSvgId(): void {
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.isSportIconEnabled = config?.CelebratingSuccess?.displaySportIcon?.includes('betreceipt');
    });
    if(this.isSportIconEnabled) {
      this.cmsService.getItemSvg('', Number(this.toteBet?.events[0]?.categoryId))
      .subscribe((icon: ISvgItem) => {
        this.toteBetDetails.svgId = icon.svgId ? icon.svgId : "icon-generic";
      });
    }
  }

  trackSiteCoreBanners(bannerName: string){
    const vipLevel: string = this.userService.vipLevel || null;
    bannerName =  bannerName.replace(/%20/g, '');
    const GTMObject = {
      eventCategory : "betreceipt banner",
      eventAction :"click",
      eventLabel : bannerName,
      location: this.window.nativeWindow.location.pathname,
      vipLevel: vipLevel
    }
    this.gtmService.push('trackEvent', GTMObject);
  }
}
