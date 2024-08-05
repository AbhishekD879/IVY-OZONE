import { ChangeDetectorRef, Component, Inject, OnInit, ViewChild, OnDestroy } from '@angular/core';
import { DeviceService } from '@core/services/device/device.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA } from '@angular/material/legacy-dialog';
import { BetPackPromotionService } from '@app/promotions/services/promotions/bet-pack-promotion.service';
import { finalize } from 'rxjs/operators';
import { UserService } from '@core/services/user/user.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { QuickDepositIframeService } from '@app/quick-deposit/services/quick-deposit-iframe.service';
import { TimeService } from '@app/core/services/time/time.service';
import { Router } from '@angular/router';
import { ILazyComponentOutput } from '@shared/components/lazy-component/lazy-component.model';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { BetPackLabels, BetPackModel, signObject } from '@app/betpackReview/components/betpack-review.model';
import { BehaviorSubject, Observable } from 'rxjs';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { BetpackCmsService } from '../../services/betpack-cms.service';
import { DialogService } from '@app/core/services/dialogService/dialog.service';
import { PlatformLocation } from '@angular/common';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { BETPACK_STATICTEXT, BETPACK_STORAGE_KEY } from '@app/betpackMarket/constants/betpack.constants';
@Component({
  selector: 'betpack-info-page',
  templateUrl: './betpack-info-page.component.html',
  styleUrls: ['./betpack-info-page.component.scss'],
  providers: [BetPackPromotionService]
})
export class BetpackInfoPageComponent extends AbstractDialogComponent implements OnInit, OnDestroy {

  @ViewChild('betpackInfoDialog', { static: true }) dialog;
  @Inject(MAT_DIALOG_DATA) public data: any;
  bp: BetPackModel;
  betpackLabels: BetPackLabels;
  buyNowClick: boolean = false;
  moreInfoClick: boolean = false;
  moreInfoBtn: string;
  clicked: boolean = false;
  isPending: boolean;
  reviewPage: boolean;
  buyNowBtn: string;
  errorMsg: string;
  depositWarn: boolean = false;
  kycEnable: boolean;
  quickDepositPanel: boolean;
  betDate: string;
  reviewFlag: boolean = false;
  signPostingMsg: string;
  signPostingToolTip: string;
  disableBuyBtn: boolean;
  header: string;
  betTime: string;
  suspendedBanner: boolean;
  gtmInfo: string[] = ['less info', 'purchase-success', 'buy now', 'purchase-fail', 'fail - exit', 'use now', 'go to my bet pack', 'exit', 'fail- make a deposit', 'fail-close'];
  timer: NodeJS.Timeout;
  signpostingEmit = new Observable<signObject>();
  signpostingSubscribe = new BehaviorSubject({
    signPost: '',
    signPostTooltip: '', betpackId: ''
  });
  moreInfoText: SafeHtml;
  isExpiresIn: boolean = false;
  inBetPackStaticText = BETPACK_STATICTEXT;
  isQuickDepositEnabled: boolean = false;
  isBPPurchased: boolean = false;
  constructor(
    device: DeviceService,
    windowRef: WindowRefService,
    private betpromotionsService: BetPackPromotionService,
    public userService: UserService,
    private pubSubService: PubSubService,
    private quickDepositIframeService: QuickDepositIframeService,
    private timeService: TimeService,
    private router: Router,
    public changeDetectorRef: ChangeDetectorRef,
    private gtmService: GtmService,
    private domSanitizer: DomSanitizer,
    public betpackCmsService: BetpackCmsService,
    public dialogService: DialogService,
    private sessionStorage: SessionStorageService,
    private loc: PlatformLocation) {
    super(device, windowRef);
    this.signpostingEmit = this.signpostingSubscribe.asObservable();
    // closes modal when back button is clicked
    loc.onPopState(() => this.closeThisDialog());
  }

  /**
   * @returns {void}
   */
  ngOnInit(): void {
    super.ngOnInit();
    this.pubSubService.subscribe('', 'STORE_STAKE_FACTOR', (flag: boolean) => { /// login update
      this.bp.betPackTokenList.forEach((token) => {
        if (token.tokenTitle[0] === '£') {
          token.tokenTitle = this.userService.currencySymbol + token.tokenTitle.substring(1);
        }
      });
    });
    this.pubSubService.subscribe('BetPack-Login', this.pubSubService.API.SESSION_LOGIN, () => {
      this.checkKYC();
    });
    // Update popup after deposit
    this.pubSubService.subscribe('Betpack-Popup-Update', this.pubSubService.API.USER_BALANCE_UPD, () => {
      if (this.isQuickDepositEnabled) {
        this.disableBuyBtn = false;
        this.depositWarn = false;
        this.buyNowBtn = this.betpackLabels.buyButtonLabel + ' - ' + this.bp.betPackPurchaseAmount;
        this.sessionStorage.remove(BETPACK_STORAGE_KEY);
        this.isQuickDepositEnabled = null;
      }
    });
    this.pubSubService.subscribe('BetPack-Popup-Close', this.pubSubService.API.LOGIN_DIALOG_CLOSED, () => {
      this.afterBPLoginHandler();
    });
    this.pubSubService.subscribe('Betpack_Popup_Update', 'BETPACK_POPUP_UPDATE', (bp) => {
      this.params.data = bp;
      this.updateBetpackDetails();
    });
    this.scrollTodescription();
  }

  ngOnDestroy() {
    this.windowRef.document.body.classList.remove('betpack-modal-open');
    this.isExpiresIn = false;
  }
  
  /**
   * Open of Dialog popup
   * @returns {void}
   */
  public open(): void {
    this.windowRef.document.body.classList.add('betpack-modal-open');
    super.open();
    this.updateBetpackDetails();
  }

  /**
    * Sets the Betpack Popup content & Button
    * @returns {void}
    */
   private updateBetpackDetails(): void {
    this.isExpiresIn = false;
    if (this.params && this.params.data && this.params.data.bp && this.params.data.betpackLabels && this.params.data.reviewPage !== undefined) {
      this.betpackLabels = this.params.data.betpackLabels;
      if (this.params.data.bp.expiresIntimer && this.params.data.signPostingMsg.split(' ')[0] === 'EXPIRES'
      ) {
        this.isExpiresIn = true;
      }
      this.bp = this.params.data.bp;
      this.disableBuyBtn = undefined;
      this.suspendedBanner = false;
      this.signPostingMsg = this.params.data.signPostingMsg;
      this.signPostingToolTip = this.params.data.signPostingToolTip;
      this.moreInfoText = this.domSanitizer.bypassSecurityTrustHtml(this.bp.betPackMoreInfoText);
      this.pubSubService.subscribe('update', 'BETPACK_UPDATE', (obj: any) => {
        if (this.params.data.bp.betPackId === obj.betpackId) {
          if (!obj.expiresIntimer) {
            this.isExpiresIn = false;
            this.params.data.signPostingMsg = obj.signPost;
            this.params.data.signPostingToolTip = obj.signPostTooltip;
          } else if (obj.expiresIntimer) {
            this.params.data.bp.expiresIntimer = obj.expiresIntimer;
            this.isExpiresIn = true
          }
          this.buttonState();
        }
      });
      this.buttonState();

      if (!this.params.data.isBuyInfoClicked && this.buyNowBtn != this.betpackLabels.gotoMyBetPacksLabel) { ////buyNow buttons
        this.buyNowBtn = this.betpackLabels.buyNowLabel + ' - ' + this.bp.betPackPurchaseAmount;
        this.header = this.betpackLabels.betPackInfoLabel;
      } else if (this.params.data.isBuyInfoClicked && this.buyNowBtn != this.betpackLabels.gotoMyBetPacksLabel) {
        this.buyNowBtn = this.betpackLabels.buyButtonLabel + ' - ' + this.bp.betPackPurchaseAmount;
        this.header = this.betpackLabels.buyBetPackLabel;
      } else {
        this.params.data.clicked = false;
      }
      this.reviewPage = this.params.data.reviewPage;

      if (this.params.data.clicked) { //// more info buttons
        this.moreInfoBtn = this.betpackLabels.lessInfoLabel;
      } else {
        this.moreInfoBtn = this.betpackLabels.moreInfoLabel;
      }
    }
    this.dialog.closeOnOutsideClick = false;
    this.changeDetectorRef.detectChanges();
   }
  /**
    * 
    * @returns {void}
    */
   private buttonState(): void {
    if ((this.signPostingMsg === this.betpackLabels.maxPurchasedLabel
      || this.signPostingMsg === this.betpackLabels.endedLabel ||
      this.signPostingMsg === this.betpackLabels.soldOutLabel || !this.signPostingMsg) && 
      (!this.reviewFlag)) {
        this.disableBuyBtn = true;
        this.params.data.isBuyInfoClicked = undefined;
      }
    }

  /**
   * Close of Dialog
   * @returns {void}
   */
  private closeThisDialog(): void {
    if ((this.depositWarn || this.kycEnable || this.suspendedBanner) && this.buyNowBtn !== "CLOSE" && this.buyNowBtn !== 'MAKE A DEPOSIT') {
      this.sendGtmData(this.gtmInfo[4]);
    }
    this.pubSubService.publish('CLOSE_DIALOG', true);
    this.isExpiresIn = false;
    this.windowRef.document.body.classList.remove('betpack-modal-open');
    this.dialogService.closeDialog(DialogService.API.betpackInfoDialog);
    setTimeout(() => {
      this.params.data.bp = null;  //null checks
      this.params.data.betpackLabels = null; //null checks
      this.params.data.reviewPage = null;
      this.params.data.isBuyInfoClicked = null;
      this.reviewFlag = null;
      this.clicked = null;
      this.moreInfoClick = null;
      this.buyNowClick = null;
      this.depositWarn = null;
      this.disableBuyBtn = null;
      this.moreInfoBtn = this.betpackLabels.moreInfoLabel;
      this.buyNowBtn = undefined;
      this.params.data.signPostingMsg = null;
      this.signPostingMsg = null;
      this.kycEnable = false;
      this.isQuickDepositEnabled && this.sessionStorage.remove(BETPACK_STORAGE_KEY);
    }, 500);
  }

  /**
   * GA tracking for close
   * @returns {void}
   */
  private sendGMTWhileClose(): void {
    if (this.depositWarn || this.kycEnable || this.suspendedBanner) {
      this.sendGtmData(this.gtmInfo[4]);
    }
    else {
      this.sendGtmData(this.gtmInfo[7]);
    }
  }

  /**
   * More Info click on popup
   * @param  {any} event
   * @returns {void}
   */
  private moreInfoClickEvent(event: ILazyComponentOutput): void {
    this.params.data.clicked = !this.params.data.clicked;
    if (!this.params.data.clicked) {
      this.moreInfoBtn = this.betpackLabels.moreInfoLabel;
      this.sendGtmData(this.gtmInfo[0]);
    } else {
      this.moreInfoBtn = this.betpackLabels.lessInfoLabel;
    }
    this.scrollTodescription();
    this.changeDetectorRef.detectChanges();
  }

  /**
   * First buy click
   * @returns {void}
   */
  private buyNowClickEvent(): void {
    if (this.buyNowBtn !== this.betpackLabels.gotoMyBetPacksLabel && this.buyNowBtn !== 'CLOSE' && !this.params.data.isBuyInfoClicked && this.params.data.clicked) {
      this.sendGtmData(this.gtmInfo[2]);
    }
    if (!this.params.data.clicked && this.params.data.isBuyInfoClicked) {

      this.dailogButton();
    }
    else if (!this.params.data.isBuyInfoClicked) {
      this.signPostingToolTip = null;
      this.buyNowBtn = this.betpackLabels.buyButtonLabel + ' - ' + this.bp.betPackPurchaseAmount;
      this.header = this.betpackLabels.buyBetPackLabel;
      this.params.data.isBuyInfoClicked = true;
      this.params.data.clicked = false;

    }
    if (!this.params.data.clicked && this.buyNowBtn === this.betpackLabels.gotoMyBetPacksLabel) {
      this.closeThisDialog();
      this.sendGtmData(this.betpackLabels.gotoMyBetPacksLabel);
      this.router.navigateByUrl('betbundle-review');
    }

    this.changeDetectorRef.detectChanges();
  }

  /**
   * Final buy click that will trigger purchase
   * @returns {void}
   */
  private buyNowBetTrigger(): void {
    this.isPending = true;
    const betPackPurchaseAmount = this.params.data.bp.betPackPurchaseAmount.replace(/[$€£]/g, '');
    this.betpromotionsService.onBuyBetPack(this.params.data.bp.triggerID, betPackPurchaseAmount.toString()).pipe(
      finalize(() => {
        this.isPending = false;
      }))
      .subscribe(data => {
        this.isExpiresIn = false;
        this.params.data.signPostingMsg = false;
        // this.signPostingMsg = null;
        this.sendGtmData(this.gtmInfo[1]);
        this.reviewFlag = true;
        this.disableBuyBtn = false;
        this.buyNowBtn = this.betpackLabels.gotoMyBetPacksLabel;
        this.errorMsg = this.betpackLabels.betPackSuccessMessage;
        this.quickDepositPanel = false;
        this.params.data.isBuyInfoClicked = true;
        this.betPlaced(this.buyNowBtn);
        this.pubSubService.publish(this.pubSubService.API.IMPLICIT_BALANCE_REFRESH);
        this.pubSubService.publish('BETPACK_PURCHASED', true);
        this.isBPPurchased = true;
      },
        (error) => {
          if (error.msg === 'INSUFFICIENT_FUNDS') {
            this.depositWarn = true;
            this.buyNowBtn = 'MAKE A DEPOSIT';
            this.errorMsg = this.betpackLabels.depositMessage;
            this.sendGtmDataError('low funds');
          } else if (error.msg === 'FAILED_TO_AWARD_TOKEN') {
            this.suspendedBanner = true;
            this.errorMsg = this.betpackLabels.serviceError;
          }
        });
  }

  /**
   * Placement of bet
   * @returns {void}
   */
  private betPlaced(buyNowBtn: string) {
    if (buyNowBtn === this.betpackLabels.gotoMyBetPacksLabel) {
      this.betDate = new Date().toISOString();
      this.betTime = this.betDate && this.timeService.formatByPattern(new Date(this.betDate), 'dd/MM/yyyy, HH:mm');
    }
  }

  /**
   * Checks for user status and changes button state and displays the banner
   * @returns {break}
   */
  private dailogButton(): void {
    switch (this.buyNowBtn) {
      case this.betpackLabels.buyButtonLabel + ' - ' + this.bp.betPackPurchaseAmount: {
        if (!this.userService.status) {
          this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'betpack'});
        } else {
          this.checkKYC();
          if (!this.kycEnable)
            this.buyNowBetTrigger();
        }
        break;
      }
      case 'MAKE A DEPOSIT': {
        this.sessionStorage.set(BETPACK_STORAGE_KEY, this.params.data);
        this.quickDepositIframeService.isEnabled().subscribe((isEnabled)=>{
          this.isQuickDepositEnabled = isEnabled;
          if(!isEnabled) {
            this.closeThisDialog();
          }
          this.quickDepositIframeService.redirectToDepositPage();
        }, () => {
          this.closeThisDialog();
          this.quickDepositIframeService.redirectToDepositPage();
        });
        this.sendGtmData(this.gtmInfo[8]);
        break;
      }
      case 'CLOSE': {
        this.closeThisDialog();
        this.sendGtmData(this.gtmInfo[9]);
        break;
      }
      default: {
        break;
      }
    }
  }

  /**Invokes after succesful login
   * @returns void
   */
  private afterBPLoginHandler(): void {
    if(this.userService.status) {
      this.sessionStorage.set(BETPACK_STORAGE_KEY, this.params.data);
      this.closeThisDialog(); 
    }
  }

  /**Signposting Background Color
   * @param  {string} signPostingMsg
   * @returns {Object}
   */
  private signPostingBkg(signPostingMsg: string): Object {
    signPostingMsg = this.params.data.signPostingMsg;
    if (signPostingMsg === this.betpackLabels.maxPurchasedLabel
      || signPostingMsg === this.betpackLabels.endedLabel ||
      signPostingMsg === this.betpackLabels.soldOutLabel) {
      this.params.data.isBuyInfoClicked = null;
      this.disableBuyBtn = true;
      return { 'background-color': '#DD4647', 'color': '#FFFFFF' };
    } else if (signPostingMsg === this.betpackLabels.comingSoon) {
      return { 'background-color': '#8D5BA1', 'color': this.inBetPackStaticText.COLORWHITE };
    } else if (signPostingMsg.length === 1) {
      return { 'background-color': this.inBetPackStaticText.COLORWHITE, 'color': this.inBetPackStaticText.COLORWHITE };
    }
    else {
      return { 'background-color': '#FFF270', 'color': '#07294B' };
    }
  }

  /**
  * Use Now Navigation
  * @param  {string} Action
  * @param  {string} Path
  * @returns void
  */
  private useNow(action: string, path: string): void {
    path = path[0] === '/' ? path : '/' + path;
    this.closeThisDialog();
    if (path === this.router.url) {
      this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    }
    this.router.navigateByUrl(path);
    this.sendGtmData(action);
  }

  /**
  * GATracking
  * @param  {string} Action
  * @returns void
  */
  private sendGtmData(action: string): void {
    const gtmData = {
      event: 'trackEvent',
      eventAction: this.reviewPage ? 'my bet bundles' : this.reviewFlag ? 'bundle receipt':'bet bundles',
      eventCategory: 'bet bundles marketplace',
      eventLabel: action.toLowerCase(),
      promoType: 'bet bundles-' + this.bp.betPackId
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

  /**
  * GATracking
  * @param  {string} Action
  * @returns void
  */
  private sendGtmDataError(error: string): void {
    const gtmData = {
      event: 'trackEvent',
      eventAction: this.reviewPage ? 'my bet bundles' : 'bet bundles',
      eventCategory: 'bet bundles marketplace',
      eventLabel: 'purchase-fail',
      promoType: 'bet bundles-' + this.bp.betPackId,
      errorMessage: error.toLowerCase(),
      errorCode: 'bet bundles'
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

  /**
   * check for KYC
   * @returns void
   */
  private checkKYC(): void {
    if (this.userService.isInShopUser() || !this.betpackCmsService.kycVerified || this.betpackCmsService.verificationStatus === 'Pending') {
      this.kycEnable = true;
      this.errorMsg = this.betpackLabels.kycArcGenericMessage;
      this.buyNowBtn = 'CLOSE';
      this.sendGtmDataError('error message');
      this.changeDetectorRef.detectChanges();
    }
  }

  /**
   * stops expiry timer in case of betpack ended
   * 
   * @param  {boolean} event
   * @returns void
   */
  ontimerEmits(event: boolean): void {
    if (!event) {
      this.isExpiresIn = false;
      this.params.data.signPostingMsg = this.betpackLabels.endedLabel;
      this.disableBuyBtn = true;
      this.signPostingToolTip = this.betpackLabels.endedTooltip;
    }
  }

  /**
   * Scrolls to description
   * @returns void
   */
  scrollTodescription() {
    setTimeout(() => {
      if (this.params.data && this.params.data.bp) {
        
        const descriptionElement = this.windowRef.document.querySelector('.betpack-info-desc');
        const moreInfoElement=this.windowRef.document.querySelector('.betpack-more-info')
        if (this.params.data.clicked && descriptionElement) {
          moreInfoElement.scroll({
            top: descriptionElement['offsetTop']-moreInfoElement['offsetTop'],
          })

        }
        else {
          moreInfoElement.scroll({
            top: 0,
          })
        }
      }
    }, 0);
  }

  checkStatus(signpost: string): boolean {
    return signpost === this.betpackLabels.comingSoon;
 }
}