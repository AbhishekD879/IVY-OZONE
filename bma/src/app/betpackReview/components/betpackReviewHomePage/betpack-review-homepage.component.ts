import { Component, ComponentFactoryResolver, OnInit,ChangeDetectorRef } from '@angular/core';
import { BetPackLabels, BetPackModel, IReviewPage, ITokenData, IGetFreeBetOffersList, IGetGroupedToken, IGetTokens, IToken, BannerModel } from '@app/betpackReview/components/betpack-review.model';
import { CurrencyPipe, DatePipe } from '@angular/common';
import { UserService } from '@core/services/user/user.service';
import { DialogService } from '@app/core/services/dialogService/dialog.service';
import { BetpackInfoPageComponent } from '@app/lazy-modules/betpackPage/components/betpackInfoPage/betpack-info-page.component';
import { BetpackCmsService } from '@app/lazy-modules/betpackPage/services/betpack-cms.service';
import { BppProvidersService } from '@app/bpp/services/bppProviders/bpp-providers.service';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { Router } from '@angular/router';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DeviceService } from '@core/services/device/device.service';
import { StorageService } from '@core/services/storage/storage.service';
import { ILazyComponentOutput } from '@shared/components/lazy-component/lazy-component.model';
import { rgyellow } from '@app/bma/constants/rg-yellow.constant';
import { BETPACK_DETAILS, EMPTY_STRING, LONG_DATE_FORMAT, SHORT_DATE_FORMAT } from '@app/betpackReview/constants/constants';
import { TimeService } from '@core/services/time/time.service';
import { BET_PACK_CONSTANTS } from '@app/betpackMarket/constants/constants';
import { ServiceClosureService } from '@app/lazy-modules/serviceClosure/service-closure.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { BETPACK_PLACEHOLDER, PX } from '@app/betpackMarket/constants/betpack.constants';

@Component({
  selector: 'betpack-review-homepage',
  templateUrl: './betpack-review-homepage.component.html',
  styleUrls: ['./betpack-review-homepage.scss']
})
export class BetpackReviewHomepageComponent implements OnInit {

  reviewData: IReviewPage[] = [];
  totalValue: number = 0;
  accountFreeBetToken: IFreebetToken[];
  cmsData: BetPackModel[];
  isLoading: boolean = true;
  betpackLabels: BetPackLabels;
  totalPrice: string = "0.00";
  freeBetOffersList: Array<IGetFreeBetOffersList> = [] as IGetFreeBetOffersList[];
  getmSendData: string[] = ['more info', 'less info', 'use now'];
  bannerData:BannerModel;
  onBetReceiptOverlaySeen: boolean = false;
  isUserLoggedIn: boolean;
  isMobile: boolean = false;
  storageKey: string = 'betReview';
  onBoardingType: string = 'betReview';
  rgyCheck: boolean;
  disableBetPack: boolean;
  errorTitle: string;
  errorMessage: string;
  goToBettingLabel: string;
  goBettingURL: string;
  expiresIn: boolean;
  isuseNowLinkEnable: boolean = true;
  enableExpiresIn: boolean;
  signPost: string;
  icon: string;
  isExpiresIn: boolean;

  constructor(
    protected componentFactoryResolver: ComponentFactoryResolver,
    protected dialogService: DialogService,
    public datePipe: DatePipe,
    public userService: UserService,
    public betpackCmsService: BetpackCmsService,
    protected bppProviderService: BppProvidersService,
    public currencyPipe: CurrencyPipe,
    private pubSubService: PubSubService,
    private gtmService: GtmService,
    private router: Router,
    private device: DeviceService,
    public storageService: StorageService,
    private timeService: TimeService,
    public serviceClosureService: ServiceClosureService,
    private bonusSuppression: BonusSuppressionService,
    protected changeDetectorRef: ChangeDetectorRef,
    ) {
    this.disableBetPack = (this.userService.status && !!this.userService.maxStakeScale && +this.userService.maxStakeScale <= BET_PACK_CONSTANTS.stakeFactor);
  }

  /**
   * @returns {void}
   */
  ngOnInit(): void {
    this.getBetPackBanners();
    this.getBetPackLabels();
    this.rgyCheck = (this.userService.status && this.bonusSuppression.checkIfYellowFlagDisabled(rgyellow.BET_BUNDLES)) || (!this.userService.status);
    this.pubSubService.subscribe('', 'STORE_STAKE_FACTOR', () => {
      this.reviewData = [];
      this.totalValue = 0;
      this.isLoading = true;
      this.totalPrice = "0.00";
      this.freeBetOffersList = [] as IGetFreeBetOffersList[];
      this.rgyCheck = this.bonusSuppression.checkIfYellowFlagDisabled(rgyellow.BET_BUNDLES);
      this.getBetPackLabels();
    });
  }

/**
   * @returns {boolean}
   */
  gamblingControlsCheck(){
    return this.serviceClosureService.userServiceClosureOrPlayBreakCheck() && this.serviceClosureService.userServiceClosureOrPlayBreak;
  }
  /**
   * rearrage the data into valid format
   * @returns {void}
   */
  groupingBetPacks(): void {
    if (this.accountFreeBetToken) {
      this.accountFreeBetToken = this.accountFreeBetToken.filter((freeBetToken) =>
        freeBetToken.freebetOfferCategories && freeBetToken.freebetOfferCategories.freebetOfferCategory == BETPACK_DETAILS.BETPACK);
      this.getGroupedBetPacks(this.accountFreeBetToken);
      this.getBetpackDetails();
    } else {
      this.loadingScreen();
    }
  }

  /**
   * Method to segregate all betpacks as per group, based on tokens recieved from Open Bet
   * @param accountFreeBetToken - purchased & unused token from OB
   */
  getGroupedBetPacks(accountFreeBetToken: IFreebetToken[]): void {
    accountFreeBetToken.forEach((token: IFreebetToken) => {
      const expiryDate = this.timeService.parseDateTime((token.freebetTokenExpiryDate));
      const awardedDate = this.timeService.parseDateTime((token.freebetTokenAwardedDate));
      token.formatDate= token.freebetTokenExpiryDate;
      token.freebetTokenExpiryDate = this.datePipe.transform(expiryDate, LONG_DATE_FORMAT);
      token.freebetTokenAwardedDate = this.datePipe.transform(awardedDate, SHORT_DATE_FORMAT);
      token.freebetTokenAwardedLongDate = awardedDate;
      if (token && !this.freeBetOffersList.some((tokens: IGetFreeBetOffersList) => tokens.offerId === token.freebetOfferId)) {
        this.freeBetOffersList.push({
          offerId: token.freebetOfferId,
          group: [
            {
              groupNumber: token.group,
              tokensAssociatedToGroup: [{
                tokenId: token.tokenId,
                freebetTokenExpiryDate: token.freebetTokenExpiryDate,
                freebetTokenAwardedDate: token.freebetTokenAwardedDate,
                formatDate: token.formatDate,
                freebetTokenAwardedLongDate: token.freebetTokenAwardedLongDate,
                freebetTokenValue: token.freebetTokenValue
              }],
            },
          ],
        });
      } else if (token && this.freeBetOffersList.some((tokens: IGetFreeBetOffersList) => tokens.offerId === token.freebetOfferId)) {
        this.freeBetOffersList = this.freeBetOffersList.filter((freebetOffer: IGetFreeBetOffersList) => {
          if (freebetOffer && freebetOffer.offerId === token.freebetOfferId) {
            if (!freebetOffer.group.some((group: IGetGroupedToken) => group.groupNumber === token.group)) {
              freebetOffer.group.push({
                groupNumber: token.group,
                tokensAssociatedToGroup: [{
                  tokenId: token.tokenId,
                  freebetTokenExpiryDate: token.freebetTokenExpiryDate,
                  freebetTokenAwardedDate: token.freebetTokenAwardedDate,
                  formatDate: token.formatDate,
                  freebetTokenAwardedLongDate: token.freebetTokenAwardedLongDate,
                  freebetTokenValue: token.freebetTokenValue
                }
                ],
              });
            } else if (freebetOffer.group.some((group: IGetGroupedToken) => group.groupNumber === token.group)) {
              freebetOffer.group = freebetOffer.group.filter((group: IGetGroupedToken) => {
                if (group.groupNumber === token.group) {
                  if (group.tokensAssociatedToGroup.findIndex((tokens) => tokens.tokenId === token.tokenId) === -1) {
                    group.tokensAssociatedToGroup.push(
                      {
                        tokenId: token.tokenId,
                        freebetTokenExpiryDate: token.freebetTokenExpiryDate,
                        freebetTokenAwardedDate: token.freebetTokenAwardedDate,
                        formatDate: token.formatDate,
                        freebetTokenAwardedLongDate: token.freebetTokenAwardedLongDate,
                        freebetTokenValue: token.freebetTokenValue
                      });
                  }
                }
                return freebetOffer.group
              });
            }
          }
          return freebetOffer;
        });
      }
    });
  }

  /**
   * Method to map the betpacks of tokens recieved from OB to CMS
   */
  mapCmsBetPacks(): void {
    this.freeBetOffersList.forEach((offer: IGetFreeBetOffersList) => {
      const betpackCMSDATA = this.cmsData.find((bpCMSDATA: BetPackModel) => offer.offerId === bpCMSDATA.betPackId);
      offer.group.forEach((group: IGetGroupedToken) => {
        const betPackTokens: ITokenData[] = [];
        betpackCMSDATA && betpackCMSDATA.betPackTokenList.forEach((tokenCMSDATA: IToken) => {
          const obTokenInfo = group.tokensAssociatedToGroup.find((token: IGetTokens) => token.tokenId === tokenCMSDATA.tokenId);
          if (obTokenInfo && obTokenInfo.freebetTokenValue) {
            this.totalValue += parseFloat(obTokenInfo.freebetTokenValue);
          }
          betPackTokens.push(
            {
              tokenId: tokenCMSDATA.tokenId,
              tokenTitle: this.userService.currencySymbol + tokenCMSDATA.tokenValue + EMPTY_STRING + tokenCMSDATA.tokenTitle,
              deepLinkUrl: tokenCMSDATA.deepLinkUrl,
              tokenValue: tokenCMSDATA.tokenValue,
              active: obTokenInfo && Object.keys(obTokenInfo).length ? true : false,
              freebetTokenExpiryDate: obTokenInfo && obTokenInfo.freebetTokenExpiryDate,
              formatDate: obTokenInfo && obTokenInfo.formatDate,
              freebetTokenAwardedDate: obTokenInfo && obTokenInfo.freebetTokenAwardedDate,
              freebetTokenAwardedLongDate: obTokenInfo && obTokenInfo.freebetTokenAwardedLongDate
            });
        });
        betpackCMSDATA && betPackTokens.find(a => a.active) && this.reviewData.push(
          {
            betPackId: betpackCMSDATA.betPackId,
            betPackTitle: betpackCMSDATA.betPackTitle,
            betPackPurchaseAmount: String(betpackCMSDATA.betPackPurchaseAmount),
            betPackFreeBetsAmount: String(betpackCMSDATA.betPackFreeBetsAmount),
            betPackFrontDisplayDescription: betpackCMSDATA.betPackFrontDisplayDescription,
            betPackMoreInfoText: betpackCMSDATA.betPackMoreInfoText,
            sportsTag: betpackCMSDATA.sportsTag,
            betPackStartDate: betpackCMSDATA.betPackStartDate,
            betPackEndDate: betpackCMSDATA.maxTokenExpirationDate,
            betPackPurchaseDate: this.getBetpackPurchaseDate(betPackTokens),
            betPackPurchaseLongDate: this.getBetpackPurchaseLongDate(betPackTokens),
            betPackTokenList: betPackTokens
          });
        this.reviewData.forEach((x) => this.tokenTimer(x.betPackTokenList));
        
      });
    });
    this.sortReviewData();
    this.loadingScreen();
    this.loadOnBoardingInfo();
    this.expiringTokenCount();
  }

  tokenTimer(betPackTokenList: ITokenData[]): void {
    betPackTokenList.forEach((bpToken) => {
      if(bpToken.formatDate){
        bpToken.isExpiresIn = false;       
         if (this.timeService.compareDate(bpToken.formatDate)===1) {
          bpToken.expiresIntimer = this.timeService.parseDateTime(bpToken.formatDate).getTime();
          bpToken.isExpiresIn = true;
         }
      }
    })
  }

  /**
   * Method to calculate the purchase date of active token
   * @param betPackTokens - list of tokens available for the betpack
   * @returns - freebet purchase date
   */
  getBetpackPurchaseDate(betPackTokens): string {
    return betPackTokens.find(a => a.active) && betPackTokens.find(a => a.active).freebetTokenAwardedDate;
  }

  /**
   * Method to calculate the purchase date of active token
   * @param betPackTokens - list of tokens available for the betpack
   * @returns - freebet purchase long date
   */
  getBetpackPurchaseLongDate(betPackTokens): string {
    return betPackTokens.find(a => a.active) && betPackTokens.find(a => a.active).freebetTokenAwardedLongDate;
  }

  /**
   * Method to sort the reviewData betpacks
   */
  sortReviewData(): void {
    this.reviewData.sort((a,b) => {
      const firstBetpackLongDate = Date.parse(a.betPackPurchaseLongDate),
      secondBetpackLongDate = Date.parse(b.betPackPurchaseLongDate);
      return firstBetpackLongDate - secondBetpackLongDate;
    });
  }

  /**
   * Open pop up clicking on more info
   * @param  {any} bet
   * @returns {void}
   */
  openPopup(bet: any): void {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(BetpackInfoPageComponent);
    this.dialogService.openDialog(DialogService.API.betpackInfoDialog, componentFactory, true, {
      dialogClass: DialogService.API.betpackInfoDialog,
      data: {
        bp: bet,
        betpackLabels: this.betpackLabels,
        isBuyInfoClicked: false,
        clicked: true,
        reviewPage: true
      }
    });
  }

  /**
   * To disable loading
   * @returns {void}
   */
  loadingScreen(): void {
    this.totalPrice = this.currencyPipe.transform(this.totalValue, this.userService.currencySymbol, 'code');
    this.isLoading = false;
  }

  /**
   * Get Betpack details from cms
   * @returns {void}
   */
  getBetpackDetails(): void {
    this.betpackCmsService.getBetPackDetails().subscribe((data: BetPackModel[]) => {
      if (data) {
        this.cmsData = data.filter((bet: BetPackModel) => this.freeBetOffersList.findIndex((betpack) => betpack.offerId === bet.betPackId) > -1);
        this.cmsData.forEach((bp) => {
          const startDate = new Date(bp.betPackStartDate);
          const endDate = new Date(bp.maxTokenExpirationDate);
          bp.betPackPurchaseAmount = this.currencyPipe.transform(bp.betPackPurchaseAmount.toString(), this.userService.currencySymbol, 'code', '1.0');
          bp.betPackFreeBetsAmount = this.currencyPipe.transform(bp.betPackFreeBetsAmount.toString(), this.userService.currencySymbol, 'code', '1.0');
          bp.betPackStartDate = this.datePipe.transform(startDate, 'dd/MM/yyyy');
          bp.maxTokenExpirationDate = this.datePipe.transform(endDate, 'dd/MM/yyyy HH:mm:ss');
        });
        this.mapCmsBetPacks();
      } else {
        this.loadingScreen();
      }
    });
  }

  /**
   * Get betpack labels data from cms
   * @returns {void}
   */
  getBetPackLabels(): void {
    this.betpackCmsService.getBetPackLabels().subscribe((data: BetPackLabels) => {
      this.betpackLabels = data;
      this.getFreeBetTokens();
    });
  }

  getBetPackBanners():void{
    this.betpackCmsService.getBetPackBanners().subscribe((bannerData: BannerModel) => {
      if (bannerData) {
        this.bannerData=bannerData
        this.enableExpiresIn = bannerData.expiresInActive;
        this.signPost = bannerData.expiresInText;
        this.icon = bannerData.expiresInIconImage;
        this.changeDetectorRef.detectChanges();
      }
    });
  }

  /**
   * Get tokens form accountFreeBet api call
   * @returns {void}
   */
  getFreeBetTokens(): void {
    this.bppProviderService.accountFreebets().subscribe((data) => {
      this.accountFreeBetToken = data.response.model.freebetToken;
      this.groupingBetPacks();
    });
  }

  /**
   * onboarding event handler
   * @param  {ILazyComponentOutput} event
  */
  handleOnBoardingEvents(event: ILazyComponentOutput): void {
    if (event.output === 'closeOnboardingEmitter') {
      this.onCloseOnboarding(event);
    }
  }
  /**
  * GATracking
  * @param  {string} Action
  * @returns void
  */
   sendGtmData(data: string, promotion:boolean,betPackId?: number): void {
    const gtmData = {
      event: 'trackEvent',
      eventAction: 'my bet bundles',
      eventCategory: 'bet bundles marketplace',
      eventLabel: data,
    };
    if(promotion)gtmData['promoType'] = `bet bundles-${betPackId} `;    
    this.gtmService.push(gtmData.event, gtmData);
  }

  /**
   * Sets onBetReceiptOverlaySeen to true
   * @param  {any} event
  */
  private onCloseOnboarding(event: any): void {
    this.onBetReceiptOverlaySeen = true;
  }

  /**
   * Initialises onboarding info on load
  */
  private loadOnBoardingInfo(): void {
    const onBoardingData = this.storageService.get('onBoardingTutorial') || {};
    this.onBetReceiptOverlaySeen = !!onBoardingData[`${this.storageKey}-${this.userService.username}`];
    this.isUserLoggedIn = !!this.userService.username;
    this.isMobile = this.device.isMobile;
  }
   /**
   * Sets onBetReceiptOverlaySeen to true
   * @param  {any} event
  */

  private ontimerEmits(event: boolean,token):void {
    if (!event) {
      token.isExpiresIn = false;
      this.changeDetectorRef.detectChanges();
    }
}
 /**
   * use to close the review page banner
   * @param  {any} event
  */
closeBaner(container){
  container.remove()
  this.storageService.set('betPackReviewBanner',false)
}
/**
   * replace the toket count with place holder
   * @param  {any} event
  */
expiringTokenCount(){ 
   return  this.bannerData.bannerTextDescInReviewPage.replace(BETPACK_PLACEHOLDER.TOKEN_COUNT,this.calculateExpirinTokens());
}
 /**
   * calculate the expiring tokents in less than 25 hrs
   * @param  {any} event
  */
calculateExpirinTokens(){
  let count=0;
  this.reviewData?.forEach(x=>{
    count+= x.betPackTokenList.filter(token=>token.isExpiresIn).length;  
  })
  this.isExpiresIn=count>0?true:false;
 return count.toString()
}
 /**
   * retrun the height of the element in px
   * @param  {any} event
  */
getheightFromChild(element,offset){
  return (element.offsetHeight-offset)+PX;
}
getSvgWidth(element){
  return (element.offsetWidth)+PX;
}


}
