import { ChangeDetectorRef, Component, ComponentFactoryResolver, Input, OnInit, OnDestroy } from '@angular/core';
import { DialogService } from '@app/core/services/dialogService/dialog.service';
import { BetpackInfoPageComponent } from '@app/lazy-modules/betpackPage/components/betpackInfoPage/betpack-info-page.component';
import { UserService } from '@core/services/user/user.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { BetpackCmsService } from '@app/lazy-modules/betpackPage/services/betpack-cms.service';
import { SIGNPOSTING_MESSAGES, BETPACK_STATICTEXT, BETPACK_PLACEHOLDER } from '@app/betpackMarket/constants/betpack.constants';
import { RendererService } from '@app/shared/services/renderer/renderer.service';
import { IBetpackLivServe } from '@app/betpackMarket/components/betpack-liveServe.model';
import { BetPackLabels, BetPackModel, BetpackSocketStorageModel } from '@app/betpackReview/components/betpack-review.model';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { TimeService } from '@core/services/time/time.service';
import { IOffer } from '@app/bpp/services/bppProviders/bpp-providers.model';
@Component({
    selector: 'betpack-card',
    templateUrl: './betpack-card.component.html',
    styleUrls: ['./betpack-card.component.scss']
})
export class BetpackCardComponent implements OnInit, OnDestroy {

    @Input() bp: BetPackModel;
    @Input() isInCarousel?: boolean;
    @Input() isMaxPurchaseLimitOver: boolean;
    @Input() getLimitsData?: number;
    @Input() accLimitFreeBets?: IOffer[];

    clicked: boolean = false;
    betpackLabels: BetPackLabels;
    currentBP: BetPackModel;
    isBuyInfoClicked: boolean = false;
    isPending: boolean;
    reviewPage: boolean;
    isQuickDeposit: boolean;
    buttonName: string;
    errorMsg: string;
    currency: string;
    current: number | string;
    threshold: number | string;
    signPostingMsg: string;
    signPostingToolTip: string;
    currentBPsignPosting = SIGNPOSTING_MESSAGES;
    min: number;
    sec: number;
    isExpanded: string;
    show: boolean = true;
    socketData: BetpackSocketStorageModel;
    openPopUpSignPosting: string;
    buyNowbtn: string;
    loaded: boolean = false;
    timer: ReturnType<typeof setInterval>;
    expiresIntimer: number;
    inBetPackStaticText = BETPACK_STATICTEXT;
    isExpiresIn: boolean = false;
    maxClaimLimitRemaining: string | number;
    bpMaxClaimData = null;

    constructor(
        protected componentFactoryResolver: ComponentFactoryResolver,
        protected dialogService: DialogService,
        private pubSubService: PubSubService,
        public userService: UserService,
        public betpackCmsService: BetpackCmsService,
        public changedetectorRef: ChangeDetectorRef,
        protected rendererService: RendererService,
        private gtmService: GtmService,
        private timeService: TimeService
    ) {
        this.betpackLabels = this.betpackCmsService.betpackLabels;
    }

    /**
     * @returns {void}
     */
    ngOnInit(): void {
        this.isExpiresIn = false;
        this.bpMaxClaimData = null;
        if(this.accLimitFreeBets && this.accLimitFreeBets.length > 0) {
            this.bpMaxClaimData = this.accLimitFreeBets.find((bp) => (bp.freebetOfferId === this.bp.betPackId && bp.offerGroup?.offerGroupId==this.bp.offerGroupId)||(bp.freebetOfferId !== this.bp.betPackId&&bp.offerGroup?.offerGroupId==this.bp.offerGroupId)||(!bp.offerGroup?.offerGroupId&&bp.freebetOfferId === this.bp.betPackId ));
        }
        if (this.bp.expiresIntimer && this.bp.signPostingMsg !== this.betpackLabels.soldOutLabel) {
            this.bp.expireIn = this.betpackLabels.expiresInLabel;
            this.bp.disableBuyBtn = false;
            this.bp.signPostingMsg = this.betpackLabels.expiresInLabel
            this.isExpiresIn = true;
            this.expiresIntimer = this.bp.expiresIntimer
        } else if (!this.bp.signPostingMsg) {
            this.bp.disableBuyBtn = true;
        }
        // if popup is open
        if (this.betpackCmsService.getFreeBets && this.betpackCmsService.currentActiveBP && this.betpackCmsService.currentActiveBP.betPackId === this.bp.betPackId &&
            !this.betpackCmsService.userloginLoaded) {
            this.betpackCmsService.currentActiveBP.signPostingMsg = this.bp.signPostingMsg;
            this.BetpackPopUpState(this.betpackCmsService.currentActiveBP);
        }
        // Actual Live Serve Data
        this.buyNowbtn = this.betpackLabels.buyNowLabel + ' - ' + this.bp.betPackPurchaseAmount;
        this.isExpanded = 'enabled';
        this.pubSubService.subscribe(`SUBSCRIBE_BPMP-${this.bp.betPackId}-${this.isInCarousel}`, `SUBSCRIBE_BPMP`,
            (data: IBetpackLivServe) => {
                const bpResp = data.response;                
                if (bpResp && bpResp.freebetOfferId === this.bp.betPackId) {

                    if (bpResp.freebetOfferLimits && bpResp.freebetOfferLimits.limitEntry[0] &&
                        bpResp.freebetOfferLimits.limitEntry[0].limitDefinition && bpResp.freebetOfferLimits.limitEntry[0].limitDefinition.limitComponent &&
                        bpResp.freebetOfferLimits.limitEntry[0].limitDefinition.limitComponent.limitParam) {
                        const changedBpInfo = bpResp.freebetOfferLimits.limitEntry[0].limitDefinition.limitComponent.limitParam;
                        changedBpInfo.forEach(bpVal => {
                            if (bpVal.name === 'current') {
                                this.current = bpVal.value;

                            } else if (bpVal.name === 'threshold') {
                                this.threshold = bpVal.value;

                            }
                        });
                        if (this.threshold != this.current && this.bpMaxClaimData) {
                            this.getMaxClaimData(this.bp);
                            this.bp.signPostingMsg = this.maxClaimLimitRemaining === 0 ? this.betpackLabels.maxPurchasedLabel : this.bp.signPostingMsg;
                        }
                        this.socketData = { id: bpResp.freebetOfferId, betpackEndDate: bpResp.endTime, current: this.current, threshold: this.threshold, maxClaimLimitRemaining: this.maxClaimLimitRemaining, betpackStartDate: bpResp.startTime };
                        this.signPostings(this.socketData);
                    }
                    else if (this.isLogin() && !bpResp.freebetOfferLimits) {
                        this.current = this.inBetPackStaticText.UNLIMITED;
                        this.threshold = this.inBetPackStaticText.UNLIMITED;
                        if (this.bpMaxClaimData) {
                            this.getMaxClaimData(this.bp);
                            this.bp.signPostingMsg = this.maxClaimLimitRemaining === 0 ? this.betpackLabels.maxPurchasedLabel : this.bp.signPostingMsg;
                        }
                        this.socketData = { id: bpResp.freebetOfferId, betpackEndDate: bpResp.endTime, current: this.current, threshold: this.threshold, maxClaimLimitRemaining: this.maxClaimLimitRemaining, betpackStartDate: bpResp.startTime };
                        this.signPostings(this.socketData);
                    } else if (!bpResp.freebetOfferLimits) {
                        this.current = this.inBetPackStaticText.UNLIMITED;
                        this.threshold = this.inBetPackStaticText.UNLIMITED;
                        this.socketData = { id: bpResp.freebetOfferId, betpackEndDate: bpResp.endTime, current: this.current, threshold: this.threshold, maxClaimLimitRemaining: this.maxClaimLimitRemaining, betpackStartDate: bpResp.startTime };
                        this.signPostings(this.socketData);
                    }
                }
            });
        this.pubSubService.subscribe('dailog', 'CLOSE_DIALOG', (flag: boolean) => {
            this.betpackCmsService.currentActiveBP = null;
        });
    }
    /**More Info Click
    * @param  {any} bp
    * @param  {Event} event
    * @param  {} signPostingMsg
    * @returns {void}
    */
    moreInfo(bp: BetPackModel, event: Event, signPostingMsg: string, signPostingToolTip: string): void {
        this.betpackCmsService.currentActiveBP = bp;
        this.isBuyInfoClicked = false;
        this.clicked = true;

        this.openPopup(bp, event, signPostingMsg, signPostingToolTip);
        const gtmData = {
            event: 'trackEvent',
            eventAction: 'bet bundles',
            eventCategory: 'bet bundles marketplace',
            eventLabel: 'more info',
            promoType: 'bet bundles-' + bp.betPackId
        };
        this.gtmService.push(gtmData.event, gtmData);
    }

    /**
     * Pop up state on click Buy
     * @param  {BetPackModel} bp
     * @param  {Event} event
     * @param  {} signPostingMsg
     * @returns {void}
     */
    buyNow(bp: BetPackModel, event: Event, signPostingMsg?: string, signPostingToolTip?: string): void {
        this.betpackCmsService.currentActiveBP = bp;
        this.betpackCmsService.currentActiveBP.signPostingMsg = signPostingMsg;
        this.isBuyInfoClicked = true;
        this.clicked = false;
        this.openPopup(bp, event, signPostingMsg, signPostingToolTip);
    }

    /**
     * GATracking
     * @param  {BetPackModel} bp
     * @returns void
     */
    sendgmt(bp: BetPackModel): void {
        const gtmData = {
            event: 'trackEvent',
            eventAction: 'bet bundles',
            eventCategory: 'bet bundles marketplace',
            eventLabel: 'buy now',
            promoType: 'bet bundles-' + bp.betPackId
        };
        this.gtmService.push(gtmData.event, gtmData);
    }

    /**
     * @returns {void}
     */
    ngOnDestroy(): void {
        this.isExpiresIn = false;
    }
    /**
  * @returns BetpackInfoPageComponent
  */
    get dialogComponent(): typeof BetpackInfoPageComponent {
        return BetpackInfoPageComponent;
    }
    /**
     * Restoring the popup after login
     * @returns {void}
     */
    private BetpackPopUpState(bp: BetPackModel): void {
        if (this.betpackCmsService.currentActiveBP.betPackId && this.bp.betPackId) {
            this.betpackCmsService.currentActiveBP.betPackPurchaseAmount =
                this.betpackCmsService.currentActiveBP.betPackPurchaseAmount.toString().replace(/^£/, this.userService.currencySymbol);
            this.betpackCmsService.currentActiveBP.betPackFreeBetsAmount =
                this.betpackCmsService.currentActiveBP.betPackFreeBetsAmount.toString().replace(/^£/, this.userService.currencySymbol);
            this.buyNow(bp, {} as any, bp.signPostingMsg, bp.signPostingToolTip);
        }
    }

    /**Setting Background Color for Signposting
     * @param  {string} signPostingMsg
     */
    private signPostingBkg(signPostingMsg: string) {
        if (signPostingMsg === this.betpackLabels.maxPurchasedLabel || signPostingMsg === this.betpackLabels.endedLabel || signPostingMsg === this.betpackLabels.soldOutLabel) {
            this.bp.disableBuyBtn = true;
            return { 'background-color': '#DD4647', 'color': '#FFFFFF' };
        }  else if(signPostingMsg === this.betpackLabels.comingSoon){
            return { 'background-color': '#8D5BA1', 'color': this.inBetPackStaticText.COLORWHITE };
        } else if(signPostingMsg.length === 1){
            return { 'background-color': this.inBetPackStaticText.COLORWHITE, 'color': this.inBetPackStaticText.COLORWHITE };
        } else {
            return { 'background-color': '#FFF270', 'color': '#07294B' };
        }
    }


    /** Checking the threshold value for unlimited
    * @returns {boolean}
    */
    private checkThresholdValue(): boolean {
        return this.threshold === this.inBetPackStaticText.UNLIMITED;
    }

    /** Checking  max claim limit remaining is greater then 0 or not
    * @returns {boolean}
    */
    private isOBMaxClaim(bp): boolean {
        return bp.maxClaimLimitRemaining && bp.maxClaimLimitRemaining > 0;
    } 

    /** check if user logged in or not
    * @returns {boolean}
    */
    private isLogin(): boolean {
        return this.userService.username;
    } 


    /** Setting signposting for each betpack level
     * @param  {BetpackSocketStorageModel} bp
     * @returns {void}
     */
    private signPostings(bp: BetpackSocketStorageModel): void {
        const todayDate = new Date().getTime();
        const bppEndDate = !!bp && this.timeService.parseDateTime(bp.betpackEndDate).getTime(); /// ws betpack end date
        const betpackValidityPeriod = (bppEndDate - todayDate);
        const bppStartDate = !!bp && this.timeService.parseDateTime(bp.betpackStartDate).getTime();
        const cmsStartDate = this.timeService.parseDateTime(this.bp.betPackStartDate).getTime();
        if (!this.betpackLabels) {
            return;
        }
        if (this.bp.signPostingMsg !== this.betpackLabels.maxPurchasedLabel) {
            if ((bp?.threshold > bp?.current) || this.checkThresholdValue()) {
                if((todayDate < bppStartDate) && (bppStartDate > cmsStartDate)){
                    this.bp.signPostingMsg = this.betpackLabels.comingSoon;
                    this.bp.signPostingToolTip = this.betpackLabels.comingSoon;
                    this.bp.disableBuyBtn = false;
                  } else if (betpackValidityPeriod < 10800000 && betpackValidityPeriod >= 3600000) {
                    this.bp.signPostingMsg = this.betpackLabels.endingSoonLabel;
                    this.bp.signPostingToolTip = this.betpackLabels.endingSoonTooltip;
                    this.isExpiresIn = false;
                } else if (betpackValidityPeriod < 3600000 && betpackValidityPeriod > 0) {
                    this.bp.expireIn = this.betpackLabels.expiresInLabel;
                    this.bp.signPostingMsg = this.bp.expireIn;
                    this.bp.expiresIntimer = bppEndDate;
                    this.expiresIntimer = bppEndDate;
                    this.isExpiresIn = true;

                }  else if (betpackValidityPeriod > 10800000 &&  this.isLogin() && this.isOBMaxClaim(bp)) {
                    this.bp.signPostingMsg = this.betpackLabels.maxOnePurchasedLabel.replace(BETPACK_PLACEHOLDER.MAX_CLAIMS, bp.maxClaimLimitRemaining.toString());
                    this.bp.signPostingToolTip = this.betpackLabels.maxOnePurchasedTooltip.replace(BETPACK_PLACEHOLDER.MAX_CLAIMS, bp.maxClaimLimitRemaining.toString());
                    this.bp.disableBuyBtn = false;
                }  else if (betpackValidityPeriod > 10800000 && this.isLogin() && !this.isOBMaxClaim(bp)) {
                    this.bp.signPostingMsg = this.betpackLabels.maxOnePurchasedLabel.replace(BETPACK_PLACEHOLDER.MAX_CLAIMS, this.bp.maxClaims.toString());
                    this.bp.signPostingToolTip = this.betpackLabels.maxOnePurchasedTooltip.replace(BETPACK_PLACEHOLDER.MAX_CLAIMS, this.bp.maxClaims.toString());
                    this.bp.disableBuyBtn = false;
                } else if (betpackValidityPeriod > 10800000 && !this.checkThresholdValue() && Number(bp.current) > 0) {
                    this.bp.signPostingMsg = this.betpackLabels.limitedLabel;
                    this.bp.signPostingToolTip = this.betpackLabels.limitedTooltip;
                    this.bp.disableBuyBtn = false;
                } else if (betpackValidityPeriod <= 0) {
                    this.bp.signPostingMsg = this.betpackLabels.endedLabel;
                    this.bp.signPostingToolTip = this.betpackLabels.endedTooltip;
                    this.isExpiresIn = false;
                }
                else if (bp && bp.threshold === this.inBetPackStaticText.UNLIMITED || (betpackValidityPeriod > 10800000 && !this.checkThresholdValue() && bp.current == 0)) {
                    this.bp.signPostingMsg = ' ';
                    this.bp.disableBuyBtn = false;
                  }
            } else if (bp?.threshold === bp?.current) {
                this.isExpiresIn = false;
                this.bp.signPostingMsg = this.betpackLabels.soldOutLabel;
                this.bp.signPostingToolTip = this.betpackLabels.soldOutTooltip;
                this.bp.disableBuyBtn = true;
                this.bp.expireIn = null;
                this.expiresIntimer = null;
                if (betpackValidityPeriod <= 0) {
                    this.bp.signPostingMsg = this.betpackLabels.endedLabel;
                    this.bp.signPostingToolTip = this.betpackLabels.endedTooltip;
                }
            }
        }
        if (this.betpackCmsService.currentActiveBP) {
            this.pubSubService.publish('BETPACK_UPDATE', { signPost: this.bp.signPostingMsg, signPostTooltip: this.bp.signPostingToolTip, betpackId: this.bp.betPackId, expiresIntimer: this.expiresIntimer });
        }
        if (this.bp.signPostingMsg === this.betpackLabels.maxOnePurchasedLabel || this.bp.signPostingMsg === this.betpackLabels.endingSoonLabel || this.bp.expireIn) {
            this.bp.disableBuyBtn = false;
        }
    }

    /**
     * @param  {BetPackModel} bp
     * @param  {Event} event
     * @param  {} signPostingMsg
     * @returns {void}
     */
    private openPopup(bp: BetPackModel, event: Event, signPostingMsg?: string, signPostingToolTip?: string): void {
        const componentFactory = this.componentFactoryResolver.resolveComponentFactory(this.dialogComponent);
        this.dialogService.openDialog(DialogService.API.betpackInfoDialog, componentFactory, false, {
            dialogClass: DialogService.API.betpackInfoDialog,
            data: {
                bp: bp,
                betpackLabels: this.betpackLabels,
                isBuyInfoClicked: this.isBuyInfoClicked,
                clicked: this.clicked,
                reviewPage: false,
                signPostingMsg: signPostingMsg,
                signPostingToolTip: signPostingToolTip,
                expiresIntimer: this.expiresIntimer
            }
        });
    }

    /**
     * @returns {boolean}
     */
    private isUpgradeVisible(): boolean {
        if (this.userService.bppToken) {
            return this.userService.isInShopUser();
        }
    }

    /**
     * @param  {} length
     * @returns {number}
     */
    private tokenLengthCheck(length: number): number {
        return length - 4;
    }
    /**
     * @param  {boolean} event
     * @returns {void}
     */
    private ontimerEmits(event: boolean):void {
        if (!event) {
            this.isExpiresIn = false;
            this.bp.signPostingMsg = this.betpackLabels.endedLabel;
            this.bp.signPostingToolTip = this.betpackLabels.endedTooltip;
            this.bp.expireIn = null;
            this.bp.disableBuyBtn = true;
        }
    }

    /**
   * To save Max claim limit remaing value
   * @param {BetPackModel} bp - betPackId
   * @returns {void} 
   */
    getMaxClaimData(bp: BetPackModel): void {
        const bpMaxClaimData = this.accLimitFreeBets.find((accLimitFreeBet) => accLimitFreeBet.offerGroup?.offerGroupId === bp.offerGroupId);
        const offerLevelLimit = bpMaxClaimData && bpMaxClaimData.freebetOfferLimits?.limitEntry.find((offerlimitEntry) => offerlimitEntry.limitSort === 'OFFER_MAX_CLAIMS_LIMIT');
        const groupLevelLimit = bpMaxClaimData && bpMaxClaimData.freebetOfferLimits?.limitEntry.find((grouplimitEntry) => grouplimitEntry.limitSort === 'OFFER_GROUP_MAX_CLAIMS_LIMIT');
        const groupLimit = groupLevelLimit?.limitRemaining
        const bpLimit = offerLevelLimit?.limitRemaining
        if(bpMaxClaimData && bpMaxClaimData.freebetOfferId === bp.betPackId ){
            this.maxClaimLimitRemaining = groupLimit && bpLimit && (groupLimit < bpLimit) ? groupLimit : bpLimit;
        } else {
            this.maxClaimLimitRemaining = groupLimit && (groupLimit < bp.maxClaims) ? groupLimit : bp.maxClaims;
        }
    }
    checkStatus(signpost: string): boolean {
       return signpost === this.betpackLabels.comingSoon;
    }
}