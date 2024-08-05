import { Component, OnDestroy, OnInit, Output, EventEmitter,ChangeDetectorRef } from '@angular/core';
import { LocaleService } from '@core/services/locale/locale.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SessionService } from '@authModule/services/session/session.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { DeviceService } from '@core/services/device/device.service';
import { OverAskService } from '@betslip/services/overAsk/over-ask.service';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { StorageService } from '@core/services/storage/storage.service';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { IBetslipReceiptBanner, IBsReceiptBannerImages } from '@app/betslip/models/betslip-receipt-banner-data.model';
import { BetReceiptService } from '@app/betslip/services/betReceipt/bet-receipt.service';
import { LUCKY_DIP_CONSTANTS } from '@app/lazy-modules/luckyDip/constants/lucky-dip-constants';

@Component({
  selector: 'betslip-container',
  templateUrl: 'betslip-container.component.html'
})
export class BetslipContainerComponent implements OnInit, OnDestroy {
  @Output() readonly heightChanged = new EventEmitter<number>();

  sessionStateDefined: boolean = false;
  tag: string = 'wBetslip';
  sysConfig: ISystemConfig;
  winAlertsBets: string[] = [];
  winAlertsReceiptId: string;
  bsMaxHeight: string;
  bsReceiptBannerImages: IBsReceiptBannerImages[] = [];
  bannersLoaded: boolean = false;
  private bsMode: string;
  private modes: { [key: string]: string; };
  isLuckyDip: boolean = false;
  constructor(
    locale: LocaleService,
    private cmsService: CmsService,
    private pubSubService: PubSubService,
    private sessionService: SessionService,
    private nativeBridge: NativeBridgeService,
    public device: DeviceService,
    private overAskService: OverAskService,
    private storageService: StorageService,
    private sessionStorageService: SessionStorageService,
    private betReceiptService: BetReceiptService,
    protected changeDetector: ChangeDetectorRef
  ) {
    this.modes = {
      betslip: locale.getString('app.betslipTabs.betslip'),
      cashout: locale.getString('app.betslipTabs.cashout'),
      openbets: locale.getString('app.betslipTabs.openbets'),
      betReceipt: locale.getString('app.betslipTabs.betReceipt'),
      toteBetReceipt: locale.getString('app.betslipTabs.toteBetReceipt'),
      betHistory: locale.getString('app.betslipTabs.betHistory')
    };
  }

  get MODES() {
    return this.modes;
  }
  set MODES(value: any) {
    this.modes = value;
  }
  get mode() {
    return this.bsMode;
  }

  set mode(value) {
    this.bsMode = value;
    this.overAskService.bsMode = value;
    this.getBetslipReceiptBanners();
  }

  selectBetSlipTab(name: string, preventSystemUpdate: boolean = false): void {
    const updateSystemConf = name === this.MODES.betslip && !preventSystemUpdate;

    if (this.mode === 'Bet Receipt' && this.winAlertsBets.length) {
      this.nativeBridge.onActivateWinAlerts(this.winAlertsReceiptId, this.winAlertsBets);
      this.winAlertsBets = [];
      this.winAlertsReceiptId = null;
    }

    this.mode = name;
    if (updateSystemConf) {
      this.cmsService.triggerSystemConfigUpdate();
    }
    this.pubSubService.publish(this.pubSubService.API.BETSLIP_LABEL, name);
  }


  ngOnInit(): void {
    this.selectBetSlipTab(this.MODES.betslip);
    this.pubSubService.subscribe(this.tag, [LUCKY_DIP_CONSTANTS.LD_BET_PLACED], (data) => {
      this.mode = data ? 'Bet Receipt' : 'Bet Slip';
      this.isLuckyDip = data;
      this.changeDetector.detectChanges();
    });
    
    this.pubSubService.subscribe(this.tag, [this.pubSubService.API.SUCCESSFUL_LOGIN], placeBet => {
      if (placeBet !== 'betslip') {
        this.selectBetSlipTab(this.mode || this.MODES.betslip);
      }
    });

    this.sessionService.whenSession().then(() => {
      this.sessionStateDefined = true;
      this.selectBetSlipTab(this.mode || this.MODES.betslip);
    }).catch(error => error && console.warn(error));

    this.pubSubService.subscribe(this.tag, this.pubSubService.API.SESSION_LOGOUT, () => {
      if (this.sessionStateDefined) {
        this.selectBetSlipTab(this.MODES.betslip, true);
      }
    });

    this.pubSubService.subscribe(this.tag, this.pubSubService.API.HOME_BETSLIP,
      name => this.selectBetSlipTab(name || this.MODES.betslip));

    this.cmsService.getSystemConfig().subscribe((config) => this.sysConfig = config);

    this.pubSubService.subscribe(this.tag, this.pubSubService.API.BETSLIP_UPDATED, () => {
      if (!this.sessionStorageService.get('betPlaced')) {
        const betsPlaced = this.storageService.get("betSelections");
        this.sessionStorageService.set('cashOutAvail', betsPlaced && betsPlaced.some((bet) => bet.details && bet.details.cashoutAvail === 'Y' && bet.details.marketCashoutAvail === 'Y'))
        const stepSelection = betsPlaced && betsPlaced.length ? 'addSelection' : 'pickYourBet';

        this.pubSubService.publish(this.pubSubService.API.FIRST_BET_PLACEMENT_TUTORIAL,
          { step: stepSelection, tutorialEnabled: true, type: 'defaultContent' });
      }

      if (this.mode !== this.MODES.betslip) {
        this.selectBetSlipTab(this.MODES.betslip);
      }
    });
  }

  ngOnDestroy(): void {
    this.isLuckyDip = false;
    this.pubSubService.unsubscribe(this.tag);
  }

  setWinAlertsBets(event: { receipt: IBetDetail, value: boolean }): void {
    const receipt = event.receipt;

    if (event.value) {
      if (!this.winAlertsReceiptId) { this.winAlertsReceiptId = receipt.receipt; }
      this.winAlertsBets.push(receipt.receipt);
      this.storageService.set('winAlertsEnabled', true);
    } else {
      this.winAlertsBets.splice(this.winAlertsBets.indexOf(receipt.receipt), 1);

      if (!this.winAlertsBets.length) {
        this.storageService.set('winAlertsEnabled', false);
      }
    }
  }

  /**
   * sets the betslip max height
   */
  handleHeightUpdate(bsMaxHeight: number): void {
    this.bsMaxHeight = bsMaxHeight ? `${bsMaxHeight}px` : '100%';
  }

  /**
   * Method to load bet receipt banners from sitecore
   */
  private getBetslipReceiptBanners(): void {
    this.bsReceiptBannerImages = [];
    if ((this.bsMode === this.MODES.betReceipt || this.bsMode === this.MODES.toteBetReceipt) && this.device.isMobileOnly) {
      this.betReceiptService.getBetReceiptSiteCoreBanners()
        .subscribe((teasers: IBetslipReceiptBanner[]) => {
          this.bannersLoaded = true;
          const [teaserResponse] = teasers;
          const siteCoreFanzone = teaserResponse.teasers ?? [];
          siteCoreFanzone && siteCoreFanzone.forEach((siteCoreData) => {
            if (siteCoreData && siteCoreData.backgroundImage && siteCoreData.backgroundImage.src) {
              this.bsReceiptBannerImages.push({ imageSrc: siteCoreData.backgroundImage.src, imageHref: siteCoreData.bannerLink.url, bannerName: siteCoreData.itemName });
            }
          });
        });
    }
  }

  checkIfBannersLoaded(): boolean {
    if (this.device.isMobileOnly) {
      if (this.bannersLoaded) {
        return true;
      }
    } else {
      return true;
    }
  }

}
