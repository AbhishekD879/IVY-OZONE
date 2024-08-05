import { Component, OnInit, Input, Output, EventEmitter, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { Location, DecimalPipe } from '@angular/common';
import { Router } from '@angular/router';
import * as _ from 'underscore';
import { UserService } from '@core/services/user/user.service';
import { BETSLIP_VALUES } from '@betslip/constants/bet-slip.constant';
import { BetReceiptService } from '@betslip/services/betReceipt/bet-receipt.service';
import { DeviceService } from '@core/services/device/device.service';
import { SessionService } from '@authModule/services/session/session.service';
import { IBetReceiptEntity, IRacingPostQuickbetReceipt } from '@betslip/services/betReceipt/bet-receipt.model';
import { StorageService } from '@core/services/storage/storage.service';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { BetInfoDialogService } from '@betslip/services/betInfoDialog/bet-info-dialog.service';
import { IRecentRaceTipsData, ISportEvent } from '@core/models/sport-event.model';
import { GtmService } from '@core/services/gtm/gtm.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { BodyScrollLockService } from '@betslip/services/bodyScrollLock/betslip-body-scroll-lock.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { IOffer } from '@core/models/aem-banners-section.model';
import { OverAskService } from '@betslip/services/overAsk/over-ask.service';
import { LocaleService } from '@core/services/locale/locale.service';
import  Utils from '@app/core/services/aemBanners/utils';
import environment from '@environment/oxygenEnvConfig';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BppErrorService } from '@app/bpp/services/bppError/bpp-error.service';
import { RacingPostTipService } from '@app/lazy-modules/racingPostTip/service/racing-post-tip.service';
import { Subscription } from 'rxjs';
import { IGtmOrigin } from '@app/core/services/gtmTracking/models/gtm-origin.model';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { ILazyComponentOutput } from '@shared/components/lazy-component/lazy-component.model';
import { bs } from '@app/lazy-modules/locale/translations/en-US/bs.lang';
import { FreeBetsService } from '@app/core/services/freeBets/free-bets.service';
import { FirstBetGAService } from '@app/lazy-modules/onBoardingTutorial/firstBetPlacement/services/first-bet-ga.service';
import { IBsReceiptBannerImages } from '@app/betslip/models/betslip-receipt-banner-data.model';
import { STRATEGY_TYPES } from '@app/core/constants/strategy-types.constant';
import { ScorecastDataService } from '@app/core/services/scorecastData/scorecast-data.service';
@Component({
  selector: 'betslip-receipt',
  templateUrl: 'betslip-receipt.component.html',
  styleUrls: ['betslip-receipt.component.scss']
})
export class BetslipReceiptComponent implements OnInit, OnDestroy {
  @Input() winAlertsEnabled: boolean;
  @Input() racingPostToggle: IRacingPostQuickbetReceipt;
  @Input() nextRacesToBetslipToggle: boolean;
  @Input() bsMaxHeight: string = '100%';
  @Input() bsReceiptBannerImages: IBsReceiptBannerImages[] = [];

  @Output() readonly winAlertsToggleChanged = new EventEmitter<{ receipt: IBetDetail, value: boolean }>();

  readonly BET_SLIP_RECEIPT_ERROR = 'betPlacementTimeoutError';

  reusePending: boolean = false;
  currencySymbol: string;
  isAndroidBrowser: boolean;
  isOldIos: boolean;
  isDesktop: boolean;
  isTablet: boolean;
  message: { type?: string; msg?: string; };
  loadComplete: boolean = false;
  loadFailed: boolean;
  totalStake: number;
  totalEstimatedReturns: number;
  freeBetsStake: number;
  allReceipts: IBetReceiptEntity = { singles: [], multiples: [] };
  activeReceipts: IBetReceiptEntity;
  allEvents: ISportEvent[];
  isAllBetsDeclined: boolean;
  isFootballAvailable: boolean = false;
  isBPMPFreeBetToken: boolean = false;
  banner: IOffer;
  betDate: string;
  receiptsCounter: number;
  winAlertsActive: boolean;
  racingPostTipTime: string;
  racingPostData: ISportEvent[];
  upCellSubscription: Subscription;
  _racingPostGA: IGtmOrigin;
  public brand: string = '';
  private UPCELL_ENDPOINT: string;
  isNextRacesData: boolean = true;
  private readonly BET_PLACED_ON_HR = environment.HORSE_RACING_CATEGORY_ID;
  upCellBetsParams = {url: '', betsData:{}};
  public onBetReceiptOverlaySeen: boolean = false;
  public isUserLoggedIn: boolean;
  public isMobile: boolean = false;
  public storageKey: string = 'betReceipt';
  public onBoardingType: string = 'betReview';
  // we need this variable to control the flow of placed bets.
  // If user comes back to Betslip and previous bet(s) was(were) placed,
  // we don't care about them and can clean Betslip at all.
  // Otherwise they will be added to Betslip again and could be displayed by mistake
  private isBettingDone: boolean = false;
  onBoardingData: { step: string; tutorialEnabled: boolean; type?: string; };
  changeStrategy = STRATEGY_TYPES.ON_PUSH;

  get overask(): OverAskService {
    return this.overAskService;
  }
  set overask(value: OverAskService) { }
  constructor(
    protected user: UserService,
    protected betReceiptService: BetReceiptService,
    protected sessionService: SessionService,
    protected storageService: StorageService,
    protected betInfoDialogService: BetInfoDialogService,
    protected location: Location,
    protected gtmService: GtmService,
    protected router: Router,
    protected comandService: CommandService,
    protected device: DeviceService,
    protected gtmTrackingService: GtmTrackingService,
    protected bodyScrollLockService: BodyScrollLockService,
    protected nativeBridge: NativeBridgeService,
    protected window: WindowRefService,
    protected overAskService: OverAskService,
    protected localeService: LocaleService,
    protected pubSubService: PubSubService,
    protected bppErrorService: BppErrorService,
    protected racingPostTipService: RacingPostTipService,
    protected sessionStorageService: SessionStorageService,
    protected fbService: FreeBetsService,
    protected firstBetGAService: FirstBetGAService,
    private changeDetection:ChangeDetectorRef,
    protected scorecastDataService: ScorecastDataService
  ) {
    this.brand = Utils.resolveBrandOrDefault(environment.brand);
    this.message = this.betReceiptService.message;
    this.isAndroidBrowser = device.browserName === BETSLIP_VALUES.ANDROID_NATIVE;
    this.isOldIos = device.isIos && Number(device.osVersion) <= BETSLIP_VALUES.OLD_IOS;
    this.isDesktop = device.isDesktop;
    this.isTablet = this.device.isTablet;
    this.currencySymbol = this.user.currencySymbol;
    this.UPCELL_ENDPOINT = environment.UPCELL_ENDPOINT;
  }

  ngOnInit(): void {
    this.loadOnBoardingInfo();
    this.bodyScrollLockService.enableBodyScroll();
    this.winAlertsActive = this.storageService.get('winAlertsEnabled');
    this.sessionService.whenProxySession().then(() => {
      this.betReceiptService.getBetReceipts().subscribe((dataInit: IBetReceiptEntity[]) => {
                this.core(dataInit);
        this.loadComplete = true;
        this.isBPMPFreeBetToken = this.overAskService.isBPMPFreeBetTokenUsed;
        this.loadFailed = false;
        this.changeDetection.detectChanges();
      }, () => {
        this.loadComplete = true;
        this.loadFailed = true;
        this.bppErrorService.showPopup(this.BET_SLIP_RECEIPT_ERROR);
      });
    });
    if (!this.sessionStorageService.get('buttonText')) {
      this.sessionStorageService.set('betPlaced', true);
      const storedOnboardingData = this.sessionStorageService.get('firstBetTutorial');
      const stepType = this.winAlertsEnabled ? 'winAlert' : 'defaultContent';
      this.onBoardingData = { step: 'betPlaced', tutorialEnabled: storedOnboardingData && storedOnboardingData.firstBetAvailable, type: stepType };
    }
  }
  
  reloadComponent(): void {
    this.ngOnDestroy();
    this.ngOnInit();
  }

  ngOnDestroy(): void {
    this.overAskService.isInFinal && this.overAskService.setStateAndClearInStorage(this.overAskService.states.off);
    this.isBettingDone && this.pubSubService.publish(this.pubSubService.API.OVERASK_CLEAN_BETSLIP, false);
    this.betReceiptService.clearMessage();
    this.pubSubService.unsubscribe('racingposttip');
    this.upCellSubscription && this.upCellSubscription.unsubscribe();
  }

  isExternalUrl(url: string): boolean {
    const extRex = /^(http:\/\/|https:\/\/)/;
    return extRex.test(url);
  }

  goToFavourites(): void {
    this.router.navigate(['/favourites']);
  }

  done(): void {
    this.isBettingDone = true;
    this.betReceiptService.done();
    this.storageService.remove('vsm-betmanager-coralvirtuals-en-selections');
    this.storageService.remove('vsbr-selection-map');
    this.storageService.remove('lastMadeBetSport');
    this.storageService.remove('lastMadeBet');
  }

  reuse(): void {
    this.reusePending = true;
    if (this.isLottoBets()) {
      const betData = this.getAllBets(this.allReceipts).map(bet => {
        return { isLotto: true, data: bet.details, goToBetslip: true, type: 'SGL' };
      });
      this.pubSubService.publish(this.pubSubService.API.ADD_TO_BETSLIP_BY_SELECTION, [ betData ]);
    } else {
      this.betReceiptService.reuse().then(() => { // TODO: 2 Observable
        this.reusePending = false;
      });
    }

  }

  /**
   *  Get racing post tip GA tracking
   */
  onRacingPostGTMEvent(event) {
    this.racingPostTipService.racingPostGTM = event.value;
  }

  core(dataReceipts: IBetReceiptEntity[]): void {
    this._racingPostGA = this.racingPostTipService.racingPostGTM;
    this.allReceipts = dataReceipts[0];
    this.activeReceipts = dataReceipts[1];

    if (!this.allReceipts) {
      this.router.navigate(['/']);
      return;
    }
    this.sendRacingPostByUpcell(this.activeReceipts.singles);
    // double check received data - OA may think bet is accepted (isConfirmed: "Y") though bet was not placed
    this.isAllBetsDeclined = this.overAskService.isAllBetsDeclined ||
      !(this.activeReceipts.singles.length || this.activeReceipts.multiples.length);

    if (this.isAllBetsDeclined) {
      this.allEvents = [];

      if (this.message && this.message.msg === this.localeService.getString('bs.depositAndPlacebetSuccessMessage')) {
        this.message.msg = undefined;
      }

      return;
    }

    const confirmedBetsLength: number = this.activeReceipts.singles.length + this.activeReceipts.multiples.length;
    this.pubSubService.publish(this.pubSubService.API.BETS_COUNTER_PLACEBET, confirmedBetsLength);
    const decimalPipe = new DecimalPipe('en-US');
    this.freeBetsStake = Number(this.betReceiptService.freeBetStake);
    this.totalStake = this.freeBetsStake && this.freeBetsStake > 0 ?
      Number(decimalPipe.transform(Number(this.betReceiptService.totalStake)
        - this.freeBetsStake, '.2-2')) : Number(this.betReceiptService.totalStake);
    this.totalEstimatedReturns = Number(this.betReceiptService.totalEstimatedReturns);
    this.betDate = this.getBetDate();
    this.allEvents = this.betReceiptService.getActiveFootballEvents(this.activeReceipts);
    this.isFootballAvailable = this.allEvents.length > 0;
    this.receiptsCounter = this.getReceiptCounter();

    if (this.winAlertsActive) {
      const bets = this.getAllBets(this.allReceipts);
      bets.forEach((bet: IBetDetail) => this.toggleWinAlerts({ receipt: bet, state: true }));
    }

    !this.isLottoBets() && this.comandService.executeAsync(this.comandService.API.GET_LIVE_STREAM_STATUS, undefined, false).then(streamData => {
      const GTMObject = {
        eventCategory: 'betslip',
        eventAction: 'place bet',
        eventLabel: 'success',
        location: this.window.nativeWindow.location.pathname,
      };
            Object.assign(GTMObject, this.betReceiptService.getGtmObject(this.activeReceipts, this.totalStake));
      const playerData = this.scorecastDataService.getScorecastData();
      if (GTMObject['ecommerce'] && GTMObject['ecommerce'].purchase
        && Array.isArray(GTMObject['ecommerce'].purchase.products)) {
        GTMObject['ecommerce'].purchase.products.forEach((product) => {
          if (this._racingPostGA && Object.keys(this._racingPostGA).length) {
            Object.assign(product, {
              dimension64: this._racingPostGA.location,
              dimension65: this._racingPostGA.module
            });
          }
          if(playerData && playerData['eventLocation'] == 'scorecast') {
            Object.assign(product, {
              dimension180: `scorecast;${playerData.teamname};${playerData.playerName};${playerData.result}`,
              dimension64: playerData.dimension64,
              dimension65: 'edp'

            });
          }
          Object.assign(product, {
            dimension87: streamData && streamData.streamActive ? 1 : 0,
            dimension88: streamData && streamData.streamID || null,
          });
        });
      }
      this.gtmService.push('trackEvent', GTMObject);

      setTimeout(() =>{
        this.scorecastDataService.setScorecastData({});
      }, 2000)
      this.changeDetection.detectChanges();
    });
  }

  trackSiteCoreBanners(bannerName: string){
    const vipLevel: string = this.user.vipLevel || null;
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



  trackByIndex(index: number): number {
    return index;
  }

  isSingles(): boolean {
    return this.allReceipts.singles && this.allReceipts.singles.length > 0;
  }

  isMultiples(): boolean {
    return this.allReceipts.multiples && this.allReceipts.multiples.length > 0;
  }

  openSelectionMultiplesDialog(index: number): void {
    const betReceipt = this.getBetReceiptById(index, true);
    this.betInfoDialogService.multiple(betReceipt.betType, Number(betReceipt.numLines));
  }

  getBetReceiptById(index: number, isMultiple: boolean): IBetDetail {
    return isMultiple ? this.allReceipts.multiples[index] : this.allReceipts.singles[index];
  }

  getReceiptNumbers(receipts: IBetReceiptEntity): string[] {
    const bets = this.getAllBets(receipts);
    return _.pluck(bets, 'receipt');
  }

  getAllBets(receipts: IBetReceiptEntity): IBetDetail[] {
    const singles = this.isSingles() ? receipts.singles : [];
    const multiples = this.isMultiples() ? receipts.multiples : [];
    return singles.concat(multiples);
  }

  isLottoBets() {
    const betData:any = this.getAllBets(this.allReceipts);
    return betData.length && betData.some(res => res.provider && res.provider.includes('Lottery'));
  }

  hasBoostedBets(receipts: IBetReceiptEntity): boolean {
    return _.some(this.getAllBets(receipts), (bet: IBetDetail) => bet.oddsBoosted);
  }

  toggleWinAlerts(event: { receipt: IBetDetail, state: boolean }): void {
    if (this.window.nativeWindow.NativeBridge.pushNotificationsEnabled) {
      if (!this.user.winAlertsToggled) {
        this.user.set({ winAlertsToggled: true });
      }
      this.winAlertsToggleChanged.emit({ receipt: event.receipt, value: event.state });
    }
    
    if (this.sessionStorageService.get('firstBetTutorialAvailable')) {
      this.firstBetGAService.setGtmData('Event.Tracking', 'click', 'step 3', 'toggle on/off');
    }
  }

  toggleWinAlertsHandler(event) {
    if(event.output === 'winAlertsToggleChanged') {
      this.winAlertsToggleChanged.emit(event.value);
    }
  }
  /**
   * post racingpost Details by upcell if placed bet is GH/HR
   * @returns {Observable<IRacingPostHRResponse>}
   */
  sendRacingPostByUpcell(racingPostData: IBetDetail[]): void {
    let body = [];
      if (racingPostData && racingPostData.length) {
        this.racingPostTipTime = racingPostData[0].date;
        const url = `${this.UPCELL_ENDPOINT}/v1/api/bets`;
        racingPostData.forEach((bets) => {
          bets.leg && bets.leg.forEach((legs) => {
           if(legs.part){
            body = body.concat(legs.part.filter((racingData) => {
              return (racingData.eventCategoryId === this.BET_PLACED_ON_HR);
            })).map(racingData => {
              const newPropsObj = {
                eventId: racingData.eventId,
                startTime: this.createDateAsUTC(new Date(racingData.startTime.replace(" ", "T"))).toISOString()
              };
              return newPropsObj;
            });
          }
          });
        });
        if (body.length) {
          const isTipEnabled = this.racingPostToggle && this.racingPostToggle.enabled && this.racingPostToggle.mainBetReceipt;
          const bets = {
            tipEnabled: isTipEnabled,
            bets: body
          }
          this.upCellBetsParams = {url: url, betsData: bets};
          if(this.enableRacingPostTip() && this.upCellBetsParams.betsData['bets'] && this.upCellBetsParams.betsData['bets'].length) {
            this.readUpcellBets(this.upCellBetsParams.url, this.upCellBetsParams.betsData);
          }
        }
      }
  }

  readUpcellBets(url, bets) {
    this.betReceiptService.readUpCellBets(url, bets).subscribe((racingTipData: IRecentRaceTipsData) => {
      
      this.racingPostData = racingTipData.races;
      this.isNextRacesData = racingTipData.nextRace;
      this.racingPostTipService.updateRaceData(racingTipData.races);
      if(this.isNextRacesData) {
        this.pubSubService.publish(this.pubSubService.API.IS_TIP_PRESENT, {
          isTipPresent: false,
          raceData: this.racingPostData
        });
      }
    });
  }

  getFreebetLabelText(){
    
    let hasFreeBet = false;
    let hasBetToken = false;
    let hasFanzone = false;
    const singleOrMulti = this.allReceipts.singles.length > 0 ? 
    (this.allReceipts.multiples.length > 0 ? [...this.allReceipts.singles, ...this.allReceipts.multiples] : 
      this.allReceipts.singles) : this.allReceipts.multiples;
    singleOrMulti.forEach(bet => {
      if(parseFloat(bet.tokenValue)>0){
        if(this.fbService.isBetPack(bet.freebetOfferCategory)){
          hasBetToken=true;
        }else if(this.fbService.isFanzone(bet.freebetOfferCategory)){
          hasFanzone=true;
        }else{
          hasFreeBet=true;
        }
      }      
    });
    return hasFreeBet ? (hasBetToken ? bs.fbAndBT : bs.freeBet) : (hasBetToken ? bs.betToken :hasFanzone? bs.fanZone : '');
  }

  private createDateAsUTC(date) {
    return new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds()));
  }

  private getBetDate(): string {
    const bet: IBetDetail = this.getBetReceiptById(0, this.isMultiples());
    const isLotto = bet.provider && bet.provider.includes('Lottery');
    return bet.date || (isLotto ? new Date().toISOString() : null);
  }

  private getReceiptCounter(): number {
    return this.allReceipts.singles.length + this.allReceipts.multiples.length;
  }

  enableRacingPostTip() {
    return this.allReceipts.multiples && !this.allReceipts.multiples.length && this.allReceipts.singles && this.allReceipts.singles.length === 1;
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
   * Sets onBetReceiptOverlaySeen to true
   * @param  {any} event  
  */
  private onCloseOnboarding(event: any): void{
    this.onBetReceiptOverlaySeen = true;
  }

  /**
   * Initialises onboarding info on load
  */
  private loadOnBoardingInfo(): void{
    const tooltipData = this.storageService.get('onBoardingTutorial') || {};
    this.onBetReceiptOverlaySeen = !!tooltipData[`${this.storageKey}-${this.user.username}`];
    this.isUserLoggedIn = !!this.user.username;
    this.isMobile = this.device.isMobile;
  }
}
