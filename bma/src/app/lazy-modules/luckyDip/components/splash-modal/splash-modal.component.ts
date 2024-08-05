import { ChangeDetectorRef, Component, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { DeviceService } from '@core/services/device/device.service';
import { DomSanitizer } from '@angular/platform-browser';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { BetslipBetDataUtils } from '@app/betslip/models/betslip-bet-data.utils';
import { QuickbetService } from '@app/quickbet/services/quickbetService/quickbet.service';
import { IOutcomeDetails } from '@core/models/outcome.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DomToolsService } from '@core/services/domTools/dom.tools.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { LuckyDipBetSelectionComponent } from '@lazy-modules/luckyDip/components/luckyDip-quick-bet/luckyDip-quick-bet.component';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { LuckyDipCMSService } from '@lazy-modules/luckyDip/services/luckyDip-cms.service';
import { ServiceClosureService } from '@lazy-modules/serviceClosure/service-closure.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { ILuckyDip, ILuckyDipRemoteBetSlipSelection } from '@lazy-modules/luckyDip/models/luckyDip';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { AnimationDataConfig } from '@lazy-modules/luckyDip/models/luckyDip';
import { LUCKY_DIP_CONSTANTS } from '@lazy-modules/luckyDip/constants/lucky-dip-constants';
import * as _ from 'underscore';


@Component({
  selector: 'splash-modal',
  templateUrl: './splash-modal.component.html',
  styleUrls: ['splash-modal.component.scss']
})

export class SplashModalComponent extends AbstractDialogComponent implements OnInit,OnDestroy{
  @ViewChild(LUCKY_DIP_CONSTANTS.DIALOG, { static: true }) dialog: any;
  @ViewChild(LUCKY_DIP_CONSTANTS.LDIP_CHILD, { static: true }) ldipChild: LuckyDipBetSelectionComponent;
  eventEntity: ISportEvent;
  market: IMarket;
  outcome: IOutcome;
  odds: string;
  marketName: string;
  cmsConfig: ILuckyDip;
  animationData: AnimationDataConfig;
  remoteBetslipObj: ILuckyDipRemoteBetSlipSelection;
  bannerImage: string;
  overlayBannerImage: string;
  selectionDataQb: IQuickbetSelectionModel;
  svg: any;
  isKeyPadClosed: boolean = true;
  heightLuckyDipSplash: string = this.getModalHeight();
  MAX_HEIGHT = '477px';
  SCREEN_HEIGHT = 770;
  constructor(
    public device: DeviceService,
    public windowRef: WindowRefService,
    public storage: SessionStorageService,
    public pubsub: PubSubService,
    public gtmTrackingService: GtmTrackingService,
    public domToolsService: DomToolsService,
    public quickBetService: QuickbetService,
    public ldCmsService: LuckyDipCMSService,
    public serviceClosureService: ServiceClosureService,
    private changeDetectorRef: ChangeDetectorRef,
    private sanitizer: DomSanitizer
  ) {
    super(device, windowRef);
  }
  
  ngOnInit(): void {
    this.pubsub.publish(this.pubsub.API.TOGGLE_LOADING_OVERLAY, { overlay: false });
    this.pubsub.subscribe(LUCKY_DIP_CONSTANTS.LUCKY_DIP_KEYPAD, this.pubsub.API.LUCKY_DIP_KEYPAD_PRESSED, (status: boolean) => {
      if ((this.windowRef.nativeWindow.screen.height < this.SCREEN_HEIGHT)) {
        this.isKeyPadClosed = status;
      } else {
        this.isKeyPadClosed = true;
      }

    });
    this.ldCmsService.getLuckyDipCMSAnimationData(this.cmsConfig.playerPageBoxImgPath).subscribe(svg => {
      this.svg = svg;
    });
  }
  /** 
  Add to remote bet slip object creation for selection handler in remote betslip
  @returns {void}
   */
  createMarketObj(): void {
    const tracking = this.gtmTrackingService.detectTracking('gtmModule', 'segment', this.eventEntity, this.market);
    const GTMObject = {
      categoryID: this.eventEntity && String(this.eventEntity.categoryId),
      typeID: this.eventEntity && String(this.eventEntity.typeId),
      eventID: this.eventEntity && String(this.eventEntity.id),
      selectionID: this.outcome && String(this.outcome.id)
    };
    GTMObject['tracking'] = tracking;
    const priceType = this.outcome.prices && this.outcome.prices[0] ? this.outcome.prices[0].priceType : 'SP';
    const price = _.extend({}, this.outcome.prices[0], priceType && { priceType });
    const handicap = this.market.rawHandicapValue && {
      type: this.outcome.outcomeMeaningMajorCode,
      raw: this.outcome.prices[0]?.handicapValueDec.replace(/,/g, '')
    };
    const details: Partial<IOutcomeDetails> = BetslipBetDataUtils.outcomeDetails(this.eventEntity, this.market, this.outcome);
    this.remoteBetslipObj = {
      eventIsLive: this.eventEntity.eventIsLive,
      outcomes: [this.outcome],
      typeName: this.eventEntity.typeName,
      price, handicap,
      goToBetslip: false,
      modifiedPrice: this.outcome.modifiedPrice,
      eventId: this.eventEntity.id,
      isOutright: true,
      isSpecial: true,
      GTMObject,
      details,
      templateMarketName: this.market.templateMarketName,
      selectionInfo: {
        marketName: this.marketName,
        eventName: this.eventEntity.name,
        outcomeName: this.marketName,
        newOdds: this.odds,
        potentialOdds: '0.00'
      }
    };
  }
  /**
   * to open splash popup
   * @returns {void}
   */
  public open(): void {
    super.open();
    this.dialog.closeOnOutsideClick = false;
    this.storage.set(LUCKY_DIP_CONSTANTS.LUCKY_DIP_STORAGE_KEY, true);
    this.storage.remove(LUCKY_DIP_CONSTANTS.QUICK_BET_SELECTION);
    ({
      eventEntity: this.eventEntity,
      outcome: this.outcome,
      market: this.market,
      odds: this.odds,
      cmsConfig: this.cmsConfig,
      overlayBannerImage: this.overlayBannerImage,
      bannerImage: this.bannerImage,
      marketName: this.marketName
    } = this.params.data);
    this.params.data && this.createMarketObj();
    this.changeDetectorRef.detectChanges();
  }

  /** 
  Method to initiate the animation post place bet
   * @returns {void}
   */
  startAnimation(value): void {
    this.animationData = {
      cmsConfig: {
        gotItCTAButton: this.cmsConfig.luckyDipFieldsConfig.gotItCTAButton,
        playerPageBoxImgPath: this.cmsConfig.playerPageBoxImgPath,
        playerCardDesc: this.cmsConfig.luckyDipFieldsConfig.playerCardDesc,
        potentialReturnsDesc: this.cmsConfig.luckyDipFieldsConfig.potentialReturnsDesc
      },
      playerData: {
        playerName: value.legParts[0].outcomeDesc,
        amount: value.payout.potential,
        odds: value.price.priceNum + '/' + value.price.priceDen
      },
      svg: this.sanitizer.bypassSecurityTrustHtml(this.svg)
    };
    this.params.data.callConfirm(this.animationData);
    setTimeout(() => this.ldCmsService.isLuckyDipReceipt.next(value), 1000);
  }

  /**
   * to close splash popup
   * @returns {void}
   */
  public closeSplashDialog(): void {
    const dialogBox = this.windowRef.document.getElementsByClassName('modal-dialog') as HTMLCollectionOf<HTMLElement>;
    if (dialogBox.length) {
      dialogBox[0].style['display'] = 'none';
      this.changeDetectorRef.detectChanges();
    }

    if (this.selectionDataQb && this.outcome) {
      Object.assign(this.selectionDataQb, {
        requestData: {
          outcomeIds: [this.outcome.id]
        }
      });
      this.quickBetService.removeSelection(this.selectionDataQb, false);
    }
    this.pubsub.publish(this.pubsub.API.QUICKBET_PANEL_CLOSE, false);
    this.storage.remove(LUCKY_DIP_CONSTANTS.LUCKY_DIP_STORAGE_KEY);
    this.storage.remove(LUCKY_DIP_CONSTANTS.QUICK_BET_SELECTION);
    if (this.device.isIos) {
      this.windowRef.document.body.classList.remove('ios-modal-opened');
      this.device.isWrapper && this.windowRef.document.body.classList.remove('ios-modal-wrapper');
    }
    super.closeDialog();
    setTimeout(() => {
      this.changeDetectorRef.detectChanges();
    }, 250)
  }

  /**
  Event after bet place
  @returns {void}
   */
  betPlaced(value: any): void {
    this.startAnimation(value);
    this.dialog.closeOnOutsideClick = false;
    const modalBody = this.windowRef.document.querySelector(LUCKY_DIP_CONSTANTS.MODAL_BODY);
    modalBody.classList.add(LUCKY_DIP_CONSTANTS.HIDE_MODAL);
    const mainContainer = this.windowRef.document.querySelector(LUCKY_DIP_CONSTANTS.SPLASH_MODAL_CONTAINER);
    mainContainer.classList.add(LUCKY_DIP_CONSTANTS.HIDE_CONTAINER);
    const mainModal: HTMLElement = this.windowRef.document.querySelector(LUCKY_DIP_CONSTANTS.SPLASH_MODAL_CSS);
    mainModal.style.cssText = LUCKY_DIP_CONSTANTS.BACKGROUND_CSS;
    const quickbetHeader = this.windowRef.document.querySelector(LUCKY_DIP_CONSTANTS.QUICKBET_HEADER);
    this.domToolsService.toggleVisibility(quickbetHeader as HTMLElement);
    this.storage.remove(LUCKY_DIP_CONSTANTS.LUCKY_DIP_STORAGE_KEY);
  }

  /** 
  Calculate the splash modal height based on device heights
   * @returns {string}
   */
  private getModalHeight(): string {
    return `calc(100vh - ${this.MAX_HEIGHT})`;
  }

  ngOnDestroy(){
    this.pubsub.unsubscribe(LUCKY_DIP_CONSTANTS.LUCKY_DIP_KEYPAD);
  }
}


