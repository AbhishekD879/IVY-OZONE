import { ChangeDetectorRef, Component, ComponentFactoryResolver, OnDestroy, OnInit } from '@angular/core';
import { ServiceClosureService } from '@lazy-modules/serviceClosure/service-closure.service';
import { UserService } from '@core/services/user/user.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BET_PACK_CONSTANTS, EMPTY_STRING } from '@app/betpackMarket/constants/constants';
import { CurrencyPipe } from '@angular/common';
import { BetPackLabels, BetPackModel, API_GETLIMITS, BetPackDialogModel, BannerModel } from '@app/betpackReview/components/betpack-review.model';
import { FreeBetsService } from '@app/core/services/freeBets/free-bets.service';
import { StorageService } from '@app/core/services/storage/storage.service';
import { BetpackCmsService } from '@app/lazy-modules/betpackPage/services/betpack-cms.service';
import { DeviceService } from '@core/services/device/device.service';
import { ILazyComponentOutput } from '@shared/components/lazy-component/lazy-component.model';
import { BETPACK_PLACEHOLDER, BETPACK_STATICTEXT, BETPACK_STORAGE_KEY, BetPack, PX } from '@app/betpackMarket/constants/betpack.constants';
import { IAccGetLimitsResponse, IApiGetLimitsResponse, IFreebetToken, ILimitEntry, IOffer } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { rgyellow } from '@app/bma/constants/rg-yellow.constant';
import { BonusSuppressionService } from '@core/services/BonusSuppression/bonus-suppression.service';
import { BppProvidersService } from '@app/bpp/services/bppProviders/bpp-providers.service';
import { LiveServConnectionService } from '@app/core/services/liveServ/live-serv-connection.service';
import { ISocketIO } from '@app/core/services/liveServ/live-serv-connection.model';
import { TimeService } from '@core/services/time/time.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { BetpackInfoPageComponent } from '@app/lazy-modules/betpackPage/components/betpackInfoPage/betpack-info-page.component';
import { DialogService } from '@app/core/services/dialogService/dialog.service';
import { forkJoin } from 'rxjs';
import { GtmService } from '@app/core/services/gtm/gtm.service';
@Component({
  selector: 'betpack-homepage',
  templateUrl: './betpack-homepage.component.html',
  styleUrls: ['./betpack-homepage.component.scss', './betpack-homepage.scss']
})

export class BetpackHomepageComponent implements OnInit, OnDestroy {
  disableBetPack: boolean;
  isUserLogIn: boolean;
  isQuickDeposit: boolean = false;
  gamblingControlsCheck: boolean;
  sportTitle: string;
  sportIconId: string;
  sportIconSvg: string;
  betpackPrice: string | number = '21';
  privateSportName: string = 'BET BUNDLES';
  topBarInnerContent: boolean;
  sportName: string;
  messageIdentifier?: string;
  cmsMessages: { errorTitle: string; errorMessage: string; goToBettingLabel: string; goBettingURL: string; };
  betpackDetails: BetPackModel[];
  betpackLabels: BetPackLabels;
  filteredBetPack: BetPackModel[] = [];
  filterValues: any = new Set([]);
  filterDisplay: boolean = true;
  isPromptDisplay: boolean = false;
  userLimits: number;
  message: string;
  filteredBetPacksList: BetPackModel[] = [];
  isMaxPurchaseLimitOver: boolean = false;
  getLimitsData: number | string;
  getFreeBets: IFreebetToken[];
  accLimitFreeBets: IOffer[];
  betpackDetailsMaster: BetPackModel[] = [];
  filteredBetPackEnable: Map<string, boolean>;
  filtered: BetPackModel[];
  isLoaded: boolean = false;
  public onBoardingOverlaySeen: boolean = false;
  public isUserLoggedIn: boolean;
  public isMobile: boolean = false;
  thresholdLimit: number;
  localStorage: boolean;
  OBgetLimitsData: number;
  showLoader: boolean;
  list: string[];
  current: string | number;
  threshold: string | number;
  signPostingMsg: string;
  bpData: { id: any; betpackEndDate: any; current: any; threshold: any; expiry: string; betpackStartDate: any };
  initialSignPostData: any;
  signPostingToolTip: string;
  expireIn: string;
  loader: boolean;
  private moduleName = rgyellow.BET_BUNDLES;
  betpackIdFromBuyNowClicked: string;
  inBetPackStaticText = BETPACK_STATICTEXT;
  maxClaimLimitRemaining: string | number = '';
  betpackDetailsFromBuyNowClicked: BetPackDialogModel;
  isKYCVerified: boolean = true;
  bannerData: BannerModel;
  enableMarketBanner: boolean = false;
  freeBetToken: IFreebetToken[];

  constructor(
    private pubSubService: PubSubService,
    public userService: UserService,
    public currencyPipe: CurrencyPipe,
    public serviceClosureService: ServiceClosureService,
    public betpackCmsService: BetpackCmsService,
    private changeDetectorRef: ChangeDetectorRef,
    private freeBetsService: FreeBetsService,
    protected storage: StorageService,
    private device: DeviceService,
    private bonusSuppression: BonusSuppressionService,
    protected bppProviderService: BppProvidersService,
    private liveServConnectionService: LiveServConnectionService,
    private timeService: TimeService,
    private sessionStorage: SessionStorageService,
    protected dialogService: DialogService,
    protected componentFactoryResolver: ComponentFactoryResolver,
    private gtmService: GtmService
  ) {
    this.initialCall();
  }

  /**
   * @returns {void}
   */
  initialCall(): void {
    this.updateHandler = this.updateHandler.bind(this);
    this.pubSubService.subscribe('Betpack-Login', [this.pubSubService.API.SESSION_LOGIN, this.pubSubService.API.SESSION_LOGOUT], () => {
      this.showLoader = true; // stake factor Loader
      this.betpackCmsService.userloginLoaded = true; /// loader for betpacks after login
      this.pubSubService.subscribe('Betpack-Successful-Login', this.pubSubService.API.SUCCESSFUL_LOGIN, () => {
        this.init();
        if (!this.bonusSuppression.checkIfYellowFlagDisabled(this.moduleName)) {
          this.bonusSuppression.navigateAwayForRGYellowCustomer();
        }
      });
    });
    this.disableBetPack = (this.userService.status && !!this.userService.maxStakeScale && +this.userService.maxStakeScale <= BET_PACK_CONSTANTS.stakeFactor);
    this.gamblingControlsCheck = this.serviceClosureService.userServiceClosureOrPlayBreakCheck() && this.serviceClosureService.userServiceClosureOrPlayBreak;
    this.pubSubService.subscribe('Betpack-StakeFactor', 'STORE_STAKE_FACTOR', () => {
      this.disableBetPack = (this.userService.status && !!this.userService.maxStakeScale && +this.userService.maxStakeScale <= BET_PACK_CONSTANTS.stakeFactor);
      this.showLoader = false;
    });
    this.pubSubService.subscribe('Betpack-Logout', 'SESSION_LOGOUT', () => {
      this.userService.maxStakeScale = null;
      this.disableBetPack = false;
      this.isPromptDisplay = false;
      this.gamblingControlsCheck = false;
    });
  }

  /**
   * @returns {void}
   */
  ngOnInit(): void {
    this.getBannerData()
    this.betpackCmsService.userloginLoaded = true;
    this.loadBetPackInfo(); /// onboarding betpacks
    this.betpackLabels = this.betpackCmsService.betpackLabels;
    this.getCmsBetpackDetails();
    this.pubSubService.subscribe('xyz', 'BETPACK_PURCHASED', () => {
      this.getBppCalls(); //Called for purchased bet pack subscriptions
    });
    this.topBarInnerContent = this.privateSportName === this.betpackLabels?.betPackMarketplacePageTitle;
    this.sportName = this.privateSportName;
    this.sportTitle = this.privateSportName;
    this.showLoader = false;
    this.openPopup();

    //Shows betpack popup
    this.pubSubService.subscribe('Betpack-Popup-Show', this.pubSubService.API.BETPACK_POPUP_SHOW, () => {
      this.openPopup(true);
    });
    this.pubSubService.subscribe('PLAY_BREAK_UPDATE', this.pubSubService.API.USER_CLOSURE_PLAY_BREAK, (flag: boolean) => {
      this.gamblingControlsCheck = flag;
      if (flag) {
        this.sessionStorage.remove(BETPACK_STORAGE_KEY);
        this.dialogService.closeDialog(DialogService.API.betpackInfoDialog);
      }
    });
    this.pubSubService.subscribe('Betpack-Reload', this.pubSubService.API.RELOAD_COMPONENTS, () => {
      this.reloadComponent();
    });
  }
  updateHandler(response): void {
    this.pubSubService.publish('SUBSCRIBE_BPMP', {
      response
    });
  }

  ngOnDestroy(): void {
    const betpackIds = this.betpackDetailsMaster.map(el => el.betPackId);
    this.liveServConnectionService.unsubscribeBP(betpackIds, this.updateHandler);
  }

  /**
   * reloads component
   * @returns {void}
   */
  reloadComponent(): void {
    this.ngOnDestroy();
    this.initialCall();
    this.ngOnInit();
  }

  /**
   * opens popup when navigating back from cashier portal
   * @returns {void}
   */
  openPopup(fromLogin?: boolean): void {
    if (!this.disableBetPack && !this.gamblingControlsCheck) {
      const betpackData = this.sessionStorage.get(BETPACK_STORAGE_KEY);
      if (!!betpackData) {
        this.betpackDetailsFromBuyNowClicked = betpackData;
        this.sessionStorage.remove(BETPACK_STORAGE_KEY);
        const componentFactory = this.componentFactoryResolver.resolveComponentFactory(BetpackInfoPageComponent);
        this.dialogService.openDialog(DialogService.API.betpackInfoDialog, componentFactory, false, {
          dialogClass: DialogService.API.betpackInfoDialog,
          data: fromLogin ? null : betpackData
        });
      }
    } else {
      this.sessionStorage.remove(BETPACK_STORAGE_KEY);
    }
  }

  subscribeForBetpacks(channels: string[], updateHandler: Function): void {
    this.liveServConnectionService.connect().subscribe((connection: ISocketIO) => {
      const handler = (msg: any) => {
        if (updateHandler) {
          updateHandler(msg);
        }
      };

      this.liveServConnectionService.subscribeBP(channels, handler);
    });
  }

  /**
   * to getLimitsCheck
   * @returns {void}
   */
  private init(): void {
    if (this.userService.status) {
      forkJoin(this.betpackCmsService.getAccountLevelLimits(), this.freeBetsService.getAccLimitFreeBetReq())
        .subscribe((res: any) => {
          const [accLevelLimits, accLimitFreeBets] = res;

          this.accLimitFreeBets = accLimitFreeBets?.freebetOffer;
          this.freeBetToken = accLimitFreeBets?.freebetToken;
          this.expiringTokenCount()
          if (this.checkLimitAvailable(accLevelLimits)) {
            this.userLimitsCheck(accLevelLimits.response.model.activeLimits.limitEntry);
            this.OBgetLimitsData = accLevelLimits.response.model.activeLimits.limitEntry.limitRemaining;
          } else {
            this.getLimitsData = this.inBetPackStaticText.UNLIMITED;
          }
          this.betpackDetailsFormat();
        });
    } else {
      this.betpackDetailsFormat();
    }
  }

  /**
   * To check limits availability 
   * @param  {IAccGetLimitsResponse} res
   * @returns {boolean}
   */
  private checkLimitAvailable(res: IAccGetLimitsResponse): boolean {
    return res.response.model.hasOwnProperty(this.inBetPackStaticText.LIMITPARAMS_ACTIVELIMITS);
  }
  /**
   * to set userslimts and thresholdLimit
   * @returns {void}
   */
  private userLimitsCheck(res: ILimitEntry): void {
    this.thresholdLimit = res.limitDefinition.limitComponent.limitParam[1].value;
    this.userLimits = res.limitRemaining;
    this.getLimitsCheck(res.limitRemaining);
  }

  /** Once user purchased calling reqfreebets which updates freebets in local storage
   * @returns void
   */
  private getBppCalls(): void {
    this.freeBetsService.getFreeBets(false).subscribe((data) => {
      this.betpackCmsService.getFreeBets = data;
      this.init();
    });
  }

  /**
   * to get the prompt flag when user login
   * @returns {void}
   */
  private getPrompt(): void {
    if (this.betpackCmsService.betpackLabels.isDailyLimitBannerEnabled && (this.filteredBetPacksList?.length || this.filteredBetPack?.length)) {
      if (this.userService.status && this.userLimits > 0) {
        this.isPromptDisplay = true;
        this.message = this.betpackLabels.maxBetPackPerDayBannerLabel.replace(BETPACK_PLACEHOLDER.LIMIT, this.userLimits.toString());
      } else if (this.userService.status && this.userLimits === 0) {
        this.isPromptDisplay = true;
        this.message = this.betpackLabels.betPackAlreadyPurchasedPerDayBannerLabel.replace(BETPACK_PLACEHOLDER.LIMIT, this.thresholdLimit.toString());
      }
    }
  }

  /**
   * to get the user limits
   * @param  {number} getlimits
   * @returns {void}
   */
  private getLimitsCheck(getlimits: number): void {
    if (this.userService.status) {
      if (getlimits === 0) {
        this.isMaxPurchaseLimitOver = true;
      } else {
        this.getLimitsData = getlimits;
      }
    }
  }

  /**
  * @returns {void}
  */
  private closeNotification(): void {
    this.isPromptDisplay = false;
  }

  getBannerData() {
    this.betpackCmsService.getBetPackBanners().subscribe((bannerData: BannerModel) => {
      if (bannerData) this.bannerData = bannerData

    });
  }
  closeBaner(container) {
    container.remove();
    this.storage.set('betPackMarketBanner', false)
  }

  expiringTokenCount() {
    return this.bannerData && this.bannerData.bannerTextDescInMarketPlacePage.replace(BETPACK_PLACEHOLDER.TOKEN_COUNT, this.calculateExpirinTokens());
  }

  calculateExpirinTokens() {  
    const freeBetTokens = this.freeBetToken?.filter((bp) => this.timeService.compareDate(bp.freebetTokenExpiryDate)==1  && bp.freebetOfferCategories?.freebetOfferCategory == BetPack);
    this.enableMarketBanner = freeBetTokens?.length > 0 ? true : false;
    return freeBetTokens?.length.toString()
  }

  getheightFromChild(element,offset) {
    return (element.offsetHeight-offset) + PX;
  }
  getSvgWidth(element) {
    return element.offsetWidth+ PX;
  }
  /**
   * to validate the betpack Cms enddate
   * @param  {} betpackDetails
   * @returns {boolean}
   */
  private isValidOBBetpack(betpackDetails): boolean {
    return (new Date().getTime() <= new Date(betpackDetails.betPackEndDate).getTime());
  }

  /**
   * to get filters in betpacks
   * @param  {BetPackModel} betpackDetails
   * @returns {void}
   */
  private filteredBetPacks(betpackDetails: BetPackModel[]): void {
    const filteredSet = new Set();
    betpackDetails.forEach(element => {
      element.filterList.forEach(ele => {
        filteredSet.add(ele);
      });
    });
    this.filterValues = filteredSet;
    if ((this.filterValues.length === 0) || (betpackDetails.length === 0)) {
      this.filterDisplay = false;
    }
    this.filteredBetPack = betpackDetails;
    this.showLoader = false;
    this.betpackCmsService.userloginLoaded = false;
    this.betpackDetails.forEach(element => {
      this.filteredBetPackEnable?.set(element.betPackId, true);
    });
  }

  /**
   * @param  {} event
   * @returns void
   */
  onFilterTabChange(event): void {
    if (event.filterName != 'All') {
      this.filteredBetPackEnable = new Map();
      this.betpackDetails.forEach(element => {
        if (element.filterList.includes(event.filterName)) {
          this.filteredBetPackEnable.set(element.betPackId, true);
        } else {
          this.filteredBetPackEnable.set(element.betPackId, false);
        }
      });
    } else {
      this.betpackDetails.forEach(element => {
        this.filteredBetPackEnable?.set(element.betPackId, true);
      });
    }
    this.changeDetectorRef.detectChanges();
  }

  /**
   * to get betpack details for cms
   * @returns {void}
   */
  private getCmsBetpackDetails(): void {
    this.betpackCmsService.getBetPackDetails().subscribe((data: BetPackModel[]) => {
      this.betpackDetailsMaster = data.filter(betpack => betpack.betPackActive && this.isValidOBBetpack(betpack));
      if (this.betpackDetailsMaster.length == 0) {
        this.betpackCmsService.userloginLoaded = false;
      } else {
        this.betpackDetailsMaster.sort((a, b) => a.sortOrder < b.sortOrder ? -1 : a.sortOrder > b.sortOrder ? 1 : 0);
        const betpackIds = this.betpackDetailsMaster.map(el => el.betPackId);
        this.subscribeForBetpacks(betpackIds, this.updateHandler);
        this.init();
      }
    });
  }
  /**
   * to rearrange the betpack details into valid format
   * @returns {void}
   */
  private betpackDetailsFormat(): void {
    this.betpackDetails = JSON.parse(JSON.stringify(this.betpackDetailsMaster));
    this.list = this.betpackDetails.map(a => a.betPackId);
    const Obj = { 'freebetOfferIds': this.list, 'returnLimits': 'Y', 'freeBetTriggerType': 'PURCHASE', 'ignoreStartDate': 'Y' };
    // API call to fetch initial websocket data
    this.bppProviderService.initialWSGetLimits(Obj).subscribe((res: IApiGetLimitsResponse) => {
      this.initialSignPostData = res?.response?.respFreebetGetOffers?.freebetOffer;
      this.cmsBetpackWithGroupIds(); ///assigning group Id from OB to CMS betpacks
      ////////////mock creation
      this.betpackDetails.forEach((bp) => {
        bp.betPackPurchaseAmount = this.currencyPipe.transform(bp.betPackPurchaseAmount.toString(), this.userService.currencySymbol, 'code', '1.0');
        bp.betPackFreeBetsAmount = this.currencyPipe.transform(bp.betPackFreeBetsAmount.toString(), this.userService.currencySymbol, 'code', '1.0');
        bp.showSignPost = false;
        bp.betPackTokenList.forEach((token) => {
          token.tokenTitle = this.userService.currencySymbol + token.tokenValue + EMPTY_STRING + token.tokenTitle;
        });
      });
      this.filtered = this.betpackDetails.filter(betpack => betpack.filterBetPack);
      this.filteredBetPacksList = this.betpackDetails.filter(betpack => betpack.futureBetPack);
      this.getPrompt();
      //for logged in users only
      this.userService.status && this.UserLevelvalidation(this.betpackDetails);
      //for all users
      !this.isMaxPurchaseLimitOver && this.initialSignPostData && this.computeInitialNonLoggedInSignPostings(this.initialSignPostData);
      this.initialSignPostData && this.filteredBetPacks(this.betpackDetails);
      if (!!this.betpackDetailsFromBuyNowClicked) {
        const bp = this.betpackDetails.find(betpack => betpack.betPackId === this.betpackDetailsFromBuyNowClicked.bp.betPackId);
        this.betpackDetailsFromBuyNowClicked.bp = bp;
        this.betpackDetailsFromBuyNowClicked.signPostingMsg = bp.expiresIntimer ? this.betpackLabels.expiresInLabel : bp.signPostingMsg;
        this.betpackDetailsFromBuyNowClicked.signPostingToolTip = bp.expiresIntimer ? this.betpackLabels.expiresInTooltip : bp.signPostingToolTip;
        this.pubSubService.publish('BETPACK_POPUP_UPDATE', this.betpackDetailsFromBuyNowClicked);
      }
      this.changeDetectorRef.detectChanges();
    });
  }
  /**
   * Setting threshold value for betpack id for setting the signpostings
   * @param signPostingData
   * @returns void
   */

  private computeInitialNonLoggedInSignPostings(signPostingData): void {
    this.betpackDetails.forEach((betpack) => {
      if (betpack) {
        let bpMaxClaimData = null;
        this.maxClaimLimitRemaining = null;
        if (this.accLimitFreeBets) {
          bpMaxClaimData = this.accLimitFreeBets.find((bp) => bp.freebetOfferId === betpack.betPackId);
        }

        const bpLimitsData = signPostingData.find((c) => c?.freebetOfferId === betpack.betPackId);
        // this.maxClaimLimitRemaining = bpMaxClaimData?bpLimitsData?.freebetOfferLimits?.limitEntry[0]?.limitRemaining: betpack.maxClaims;
        if (this.userService.status && bpMaxClaimData) {
          this.maxClaimLimitRemaining = this.getMaxClaimData(bpMaxClaimData);
        } else if (!bpMaxClaimData && bpLimitsData && betpack.showSignPost && betpack.offerGroupId) {
          this.maxClaimLimitRemaining = this.getMaxClaimData(bpLimitsData);
        }
        const limits = bpLimitsData?.freebetOfferLimits?.limitEntry[0]?.limitDefinition?.limitComponent.limitParam;
        if (limits) {
          limits.forEach(bpVal => {
            if (bpVal.name === 'current') {
              this.current = bpVal.value;
            } else if (bpVal.name === 'threshold') {
              this.threshold = bpVal.value;
            }
          });
        } else {
          this.current = this.inBetPackStaticText.UNLIMITED;
          this.threshold = this.inBetPackStaticText.UNLIMITED;
        }
        if (bpLimitsData) {
          const bpData = {
            id: bpLimitsData.freebetOfferId, betpackEndDate: bpLimitsData.endTime, current: this.current, threshold: this.threshold,
            expiry: betpack.betPackEndDate, maxClaimLimitRemaining: this.maxClaimLimitRemaining, betpackStartDate: bpLimitsData.startTime
          };
          betpack.signPostingMsg !== this.betpackLabels.maxPurchasedLabel && this.signPostings(bpData, betpack); /// websocket signpostings(betpack level signpostings)
        }
      }
    });
    this.changeDetectorRef.detectChanges();
  }

  /** Checking the threshold value for unlimited
  * @returns {boolean}
  */
  private checkThresholdValue(): boolean {
    return this.threshold === this.inBetPackStaticText.UNLIMITED;
  }

  /**
   * To get Max claim limit remaing value
   * @param {IOffer} bpMaxClaimData - freebetoffer data
   * @returns {string} max claim limit remaining
   */
  getMaxClaimData(bpMaxClaimData: IOffer): string | number {
    const maxClaimLimitRemaining = bpMaxClaimData?.freebetOfferLimits?.limitEntry[0]?.limitRemaining;

    return maxClaimLimitRemaining;
  }

  /** returns true if max claim data is present and limit remaining is greater then 0
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

  /**
   * Assigning signposting for each betpack
   * @param bp
   * @param betpack
   * @returns void
   */
  private signPostings(bp: API_GETLIMITS, betpack: BetPackModel): void {
    const todayDate = new Date().getTime();
    const bppEndDate = !!bp && this.timeService.parseDateTime(bp.betpackEndDate).getTime(); /// ws betpack end date
    const betpackValidityPeriod = (bppEndDate - todayDate);
    const bppStartDate = !!bp && this.timeService.parseDateTime(bp.betpackStartDate).getTime();
    const cmsStartDate = this.timeService.parseDateTime(betpack.betPackStartDate).getTime();
    if (!this.betpackLabels) {
      return;
    }
    if ((bp?.threshold > bp?.current) || this.checkThresholdValue()) {
      if ((todayDate < bppStartDate) && (bppStartDate > cmsStartDate)) {
        betpack.signPostingMsg = this.betpackLabels.comingSoon;
        betpack.signPostingToolTip = this.betpackLabels.comingSoon;
        betpack.disableBuyBtn = false;
      } else if (betpackValidityPeriod < 10800000 && betpackValidityPeriod > 3600000) {
        betpack.signPostingMsg = this.betpackLabels.endingSoonLabel;
        betpack.signPostingToolTip = this.betpackLabels.endingSoonTooltip;
        betpack.disableBuyBtn = false;
      } else if (betpackValidityPeriod < 3600000 && betpackValidityPeriod > 0) {
        betpack.expiresIntimer = bppEndDate;
      } else if (betpackValidityPeriod > 10800000 && this.isLogin() && this.isOBMaxClaim(bp)) {
        betpack.signPostingMsg = this.betpackLabels.maxOnePurchasedLabel.replace(BETPACK_PLACEHOLDER.MAX_CLAIMS, bp.maxClaimLimitRemaining.toString());
        betpack.signPostingToolTip = this.betpackLabels.maxOnePurchasedTooltip.replace(BETPACK_PLACEHOLDER.MAX_CLAIMS, bp.maxClaimLimitRemaining.toString());
        betpack.disableBuyBtn = false;
      } else if (betpackValidityPeriod > 10800000 && this.isLogin() && !this.isOBMaxClaim(bp)) {
        betpack.signPostingMsg = this.betpackLabels.maxOnePurchasedLabel.replace(BETPACK_PLACEHOLDER.MAX_CLAIMS, betpack.maxClaims.toString());
        betpack.signPostingToolTip = this.betpackLabels.maxOnePurchasedTooltip.replace(BETPACK_PLACEHOLDER.MAX_CLAIMS, betpack.maxClaims.toString());
        betpack.disableBuyBtn = false;
      } else if (betpackValidityPeriod > 10800000 && !this.checkThresholdValue() && Number(bp.current) > 0) {
        betpack.signPostingMsg = this.betpackLabels.limitedLabel;
        betpack.signPostingToolTip = this.betpackLabels.limitedTooltip;
        betpack.disableBuyBtn = false;
      } else if (betpackValidityPeriod <= 0) {
        betpack.signPostingMsg = this.betpackLabels.endedLabel;
        betpack.signPostingToolTip = this.betpackLabels.endedTooltip;
        betpack.disableBuyBtn = true;
      } else if (bp && bp.threshold === this.inBetPackStaticText.UNLIMITED || (betpackValidityPeriod > 10800000 && !this.checkThresholdValue() && bp.current == 0)) {
        betpack.disableBuyBtn = false;
        betpack.signPostingMsg = " ";
      }
    } else if (bp?.threshold === bp?.current) {
      betpack.signPostingMsg = this.betpackLabels.soldOutLabel;
      betpack.signPostingToolTip = this.betpackLabels.soldOutTooltip;
      betpack.disableBuyBtn = true;
      if (betpackValidityPeriod <= 0) {
        betpack.signPostingMsg = this.betpackLabels.endedLabel;
        betpack.signPostingToolTip = this.betpackLabels.endedTooltip;
      }
    }
  }
  /**
   * User level signpostings assignment to each betpack
   * @param BetPackModel[]
   * @returns void
   */
  private UserLevelvalidation(betpackDetails: BetPackModel[]): void {
    if (this.isMaxPurchaseLimitOver) {
      betpackDetails.forEach((obj) => {
        this.updateComingSoonSignPost(obj)
      })
    } else if (this.getLimitsData) {
      this.userLevelPurchase(betpackDetails);
    }
  }

  /**
   * Call this method when user has limits left
   * @param BetPackModel[]
   * @returns void
   */
  private userLevelPurchase(betpackDetails: BetPackModel[]): void {
    if (this.accLimitFreeBets) {
      betpackDetails.forEach((bp) => {
        const obj = this.accLimitFreeBets.find(ele => ele.freebetOfferId === bp.betPackId && this.checkForMaxLimits(ele, bp)
        )
        if (obj) {
          bp.signPostingMsg = this.betpackLabels.maxPurchasedLabel;
          bp.signPostingToolTip = this.betpackLabels.maxPurchasedTooltip;
          bp.disableBuyBtn = true;
        }
      });
    }
  }

  /**
   * returns true if limit remaing for offer is 0
   * @param freeBetOffer
   * @returns boolean
   */
  // check for offer level limit
  private checkForMaxLimits(freeBetOffer: IOffer, bp:BetPackModel): boolean {
    const offerLevelLimit = freeBetOffer.freebetOfferLimits?.limitEntry.find((oferLimitEntry: ILimitEntry) => oferLimitEntry.limitSort === 'OFFER_MAX_CLAIMS_LIMIT');
    return freeBetOffer.offerGroup?.offerGroupId ? this.groupLevelCheck(freeBetOffer, bp) : offerLevelLimit?.limitRemaining === 0;
  }

  /**
 * returns true if limit remaing for offer is 0
 * @param freeBetOffer
 * @returns boolean
 */
  //check for group level limit
  private groupLevelCheck(freeBetOffer: IOffer, bp: BetPackModel): boolean {
    const groupLevelLimit = freeBetOffer.freebetOfferLimits?.limitEntry.find((groupLimitEntry: ILimitEntry) => groupLimitEntry.limitSort === 'OFFER_GROUP_MAX_CLAIMS_LIMIT');
    return groupLevelLimit?.limitRemaining === 0 ? true && this.updateGroupedBps(freeBetOffer, bp, true) : this.updateGroupedBps(freeBetOffer, bp, false) && false;

  }
  /**
 * returns update signpostings only when group level limit exhausted for grouped bet bundles
 * @param freeBetOffer
 * @param limit
 */
  private updateGroupedBps(freeBetOffer: IOffer, bp: BetPackModel, limit: boolean): any {
    if (limit) {
      this.betpackDetails.forEach((betpack) => {
        if (bp.offerGroupId && bp.offerGroupId === betpack.offerGroupId && betpack.signPostingMsg !== this.betpackLabels.maxPurchasedLabel) {
          this.updateComingSoonSignPost(betpack);
        }
      })
    } else {
      this.OfferLimitUpdate(freeBetOffer, bp);
    }
  }

  updateComingSoonSignPost(betpack:BetPackModel): void {
    this.initialSignPostData.forEach((obData) => {
      if (betpack.betPackId === obData.freebetOfferId) {
        const todayDate = new Date().getTime();
        const bppStartDate = !!obData && this.timeService.parseDateTime(obData.startTime).getTime();
        const cmsStartDate = this.timeService.parseDateTime(betpack.betPackStartDate).getTime();
        if ((todayDate < bppStartDate) && (bppStartDate > cmsStartDate)) {
          betpack.signPostingMsg = this.betpackLabels.comingSoon;
          betpack.signPostingToolTip = this.betpackLabels.comingSoon;
          betpack.disableBuyBtn = false;
        } else {
          betpack.signPostingMsg = this.betpackLabels.maxPurchasedLabel;
          betpack.signPostingToolTip = this.betpackLabels.maxPurchasedTooltip;
          betpack.disableBuyBtn = true;
        }
      }
    })
  }
  /**
 * returns update the grouped bet bundles max signpostings 
 * @param freeBetOffer
 */

  private OfferLimitUpdate(freeBetOffer: any, betpack: BetPackModel): void {
    const limitUpdate = { limitDetails: freeBetOffer?.freebetOfferLimits?.limitEntry, OfferId: freeBetOffer?.freebetOfferId, offerGropuId: freeBetOffer?.offerGroup?.offerGroupId }
    this.limitEntryUpdatewithlimits(limitUpdate, freeBetOffer, betpack)
    this.checkMaxPurchase(freeBetOffer, 0, betpack);
    this.updateAllGroupedBPswithLimits(freeBetOffer,limitUpdate)
  }


  private updateAllGroupedBPswithLimits(freeBetOffer: any, limitUpdate: any) {
    this.initialSignPostData.forEach((obOffer) => {
      this.betpackDetails.forEach((bp) => {
        if (obOffer.offerGroup && obOffer.offerGroup.offerGroupId && obOffer.offerGroup.offerGroupId === freeBetOffer.offerGroup.offerGroupId && bp.betPackId === obOffer.freebetOfferId && !bp.showSignPost) {
          const todayDate = new Date().getTime();
          const bppStartDate = !!obOffer && this.timeService.parseDateTime(obOffer.startTime).getTime();
          const cmsStartDate = this.timeService.parseDateTime(bp.betPackStartDate).getTime();
          if ((todayDate < bppStartDate) && (bppStartDate > cmsStartDate)) {
            bp.signPostingMsg = this.betpackLabels.comingSoon;
            bp.signPostingToolTip = this.betpackLabels.comingSoon;
            bp.disableBuyBtn = false;
          }
          if (obOffer.freebetOfferLimits && obOffer.freebetOfferLimits.limitEntry[0].limitRemaining != 0) {
            this.limitEntryUpdatewithlimits(limitUpdate, obOffer, bp)
          } else if (!obOffer.freebetOfferLimits) {
            obOffer.freebetOfferLimits = { limitEntry: [] };
            this.limitEntryUpdatewithlimits(limitUpdate, obOffer, bp)
          }
          this.checkMaxPurchase(obOffer, 0, bp)
        }
      })

    })
  }

  private limitEntryUpdatewithlimits(limitUpdate: any, freeBetOffer: any, betpack: BetPackModel): void {
    const sorted = this.CheckGropuLimitAndUpdateEventService(limitUpdate, freeBetOffer, betpack);
    const index = freeBetOffer.freebetOfferLimits.limitEntry.findIndex((limitEntry) => limitEntry.limitSort === sorted?.limitSort);
    if (index != -1) {
      freeBetOffer.freebetOfferLimits.limitEntry.splice(index, 1, sorted);
      freeBetOffer.freebetOfferLimits.limitEntry.sort((a, b) => a.limitRemaining - b.limitRemaining);
    } else {
      sorted && freeBetOffer.freebetOfferLimits.limitEntry.push(sorted);
      freeBetOffer.freebetOfferLimits.limitEntry.sort((a, b) => a.limitRemaining - b.limitRemaining);
    }
    betpack.showSignPost = true;
  }

  private CheckGropuLimitAndUpdateEventService(limitUpdate: any, initSignPostBp: any, cmsBp: BetPackModel): any {
    if (cmsBp) {
      const groupLimit = limitUpdate.limitDetails?.find(limit => limit.limitSort == 'OFFER_GROUP_MAX_CLAIMS_LIMIT')
      const bpLimit = limitUpdate.limitDetails?.find(limit => limit.limitSort == 'OFFER_MAX_CLAIMS_LIMIT')
      return initSignPostBp.freebetOfferId == limitUpdate.OfferId ?
        groupLimit?.limitRemaining <= bpLimit?.limitRemaining ? groupLimit : bpLimit :
        groupLimit?.limitRemaining <= cmsBp.maxClaims ? groupLimit : this.updateLimitDataWithCmsMaxClaims(initSignPostBp, cmsBp)
    }
  }
  /**
    * returns compare and update the cms limit and ob limits and return which ever is less
    * @param freeBetOffer
    * @param BetPackModel
    * @returns ILimitEntry
    */
  private updateLimitDataWithCmsMaxClaims(initSignPostBp: any, cmsBp: BetPackModel): void {
    if (initSignPostBp.freebetOfferLimits.limitEntry.length && initSignPostBp.freebetOfferLimits.limitEntry[0].limitRemaining) {
      initSignPostBp.freebetOfferLimits.limitEntry[0].limitRemaining = cmsBp.maxClaims
    } else {
      initSignPostBp.freebetOfferLimits.limitEntry[0] = { limitRemaining: cmsBp.maxClaims }
    }

    return initSignPostBp.freebetOfferLimits.limitEntry[0]
  }
  /**
   * to handle onboarding events
   * @returns {void}
   */
  private handleOnBoardingEvents(event: ILazyComponentOutput): void {
    if (event.output === 'closeOnboardingEmitter') {
      this.onCloseOnboarding(event.value);
    }
  }

  /**
  * to close onboarding events
  * @returns {void}
  */
  private onCloseOnboarding(event: string): void {
    this.onBoardingOverlaySeen = true;
    this.changeDetectorRef.detectChanges();
  }

  /**
   * to load betpack info
   * @returns {void}
   */
  private loadBetPackInfo(): void {
    const onBoardingData = this.storage.get('onBoardingTutorial') || {};
    this.onBoardingOverlaySeen = !!onBoardingData[`betPack-${this.userService.username}`];
    this.isUserLoggedIn = !!this.userService.username;
    this.isMobile = this.device.isMobile;
    this.checkKYC();
  }

  /**
   * check for KYC
   * @returns void
   */
  private checkKYC(): void {
    if (this.userService.isInShopUser() || !this.betpackCmsService.kycVerified || this.betpackCmsService.verificationStatus === 'Pending') {
      this.isKYCVerified = false;
    }
  }

  /**
   * GATracking for bet bundles event
   * @param  {Carousel} value
   * @returns void
   */
  private sendGtmData(eventLabel: string): void {
    const gtmData = {
      event: 'trackEvent',
      eventAction: 'bet bundles',
      eventCategory: 'bet bundles marketplace',
      eventLabel: eventLabel
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

  private cmsBetpackWithGroupIds(): void {
    this.betpackDetails.forEach((bp:BetPackModel) => {
      this.initialSignPostData.forEach((obOffer) => {
        if (bp.betPackId === obOffer.freebetOfferId && obOffer.offerGroup?.offerGroupId) {
          bp.offerGroupId = obOffer.offerGroup.offerGroupId;
        }
      })
    })
  }

  private checkMaxPurchase(accLimitFreeBet: any, index: number, betpack: BetPackModel): void {
    if (accLimitFreeBet.freebetOfferLimits.limitEntry[index].limitRemaining === 0 && betpack.signPostingMsg !== this.betpackLabels.comingSoon
    ) {
      betpack.signPostingMsg = this.betpackLabels.maxPurchasedLabel;
      betpack.signPostingToolTip = this.betpackLabels.maxPurchasedTooltip;
      betpack.disableBuyBtn = true;
    }
  }
}