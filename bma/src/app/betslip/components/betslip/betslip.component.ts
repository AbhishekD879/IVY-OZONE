import { DatePipe } from '@angular/common';
import {
  from as observableFrom,
  interval,
  Observable,
  of,
  Subject,
  Subscription,
  throwError
} from 'rxjs';
import { catchError, delayWhen, finalize, first, map, mergeMap, takeUntil } from 'rxjs/operators';
import {
  Component,
  ComponentFactoryResolver,
  ElementRef,
  Input,
  OnDestroy,
  OnInit,
  Type,
  ViewChild,
  ChangeDetectorRef,
  EventEmitter,
  Output
} from '@angular/core';
import * as _ from 'underscore';
import { Router } from '@angular/router';

import { BETSLIP_VALUES } from '@betslip/constants/bet-slip.constant';
import { Bet } from '@betslip/services/bet/bet';
import { SessionService } from '@authModule/services/session/session.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DeviceService, IDeviceViewType } from '@core/services/device/device.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { ResolveService } from '@core/services/resolve/resolve.service';
import { StorageService } from '@core/services/storage/storage.service';
import { UserService } from '@core/services/user/user.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { BetInfoDialogService } from '@betslip/services/betInfoDialog/bet-info-dialog.service';
import { BetReceiptService } from '@betslip/services/betReceipt/bet-receipt.service';
import { BetslipDataService } from '@betslip/services/betslip/betslip-data.service';
import { BetslipStakeService } from '@betslip/services/betslip/betslip-stake.service';
import { BetslipStorageService } from '@betslip/services/betslip/betslip-storage.service';
import { BetslipService } from '@betslip/services/betslip/betslip.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { BetslipFiltersService } from '@betslip/services/betslipFilters/betslip-filters.service';
import { BetslipLiveUpdateService } from '@betslip/services/betslipLiveUpdate/betslip-live-update.service';
import { DigitalSportBetsService } from '@core/services/digitalSportBets/digital-sport-bets.service';
import { OverAskService } from '@betslip/services/overAsk/over-ask.service';
import { QuickDepositService } from '@betslipModule/services/quickDeposit/quick-deposit.service';
import { ToteBetReceiptService } from '@betslip/services/toteBetReceipt/tote-bet-receipt.service';
import { ToteBetslipService } from '@betslip/services/toteBetslip/tote-betslip.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { TimeService } from '@core/services/time/time.service';
import { IBet, IBetError, IBetsResponse, IClaimedOffer, IRespTransGetBetsPlaced } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IBetslipConfig } from '@betslip/models/betslip-config.model';
import { IBetslipBetData } from '@betslip/models/betslip-bet-data.model';
import { IBetInfo, IBetPrice } from '@betslip/services/bet/bet.model';
import { ISuspendedOutcomeError } from '@betslip/models/suspended-outcome-error.model';
import { IFreeBet } from '@betslip/services/freeBet/free-bet.model';
import { BodyScrollLockService } from '@betslip/services/bodyScrollLock/betslip-body-scroll-lock.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { SelectionInfoDialogComponent } from '@betslip/components/selectionInfoDialog/selection-info-dialog.component';
import { ILazyComponentOutput } from '@shared/components/lazy-component/lazy-component.model';
import { BetslipBetDataUtils } from '@betslip/models/betslip-bet-data.utils';
import { IFirstMultipleInfo } from '@betslip/models/first-multiple-info';
import { AccountUpgradeLinkService } from '@vanillaInitModule/services/accountUpgradeLink/account-upgrade-link.service';
import { QuickDepositIframeService } from '@app/quick-deposit/services/quick-deposit-iframe.service';
import { IBetslipDepositData } from '@betslip/models/betslip-deposit.models';
import { IComplexBet } from '@core/models/complex-bet.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { ISystemConfig } from '@app/core/services/cms/models';
import { IFreebetsPopupDetails } from '@app/core/services/cms/models/system-config';
import { ServiceClosureService } from '@lazy-modules/serviceClosure/service-closure.service';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IFreeBetState } from '@core/services/freeBets/free-bets.model';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { SignpostingCmsService } from '@lazy-modules/signposting/services/signposting.service';
import { GetSelectionDataService } from '@betslip/services/getSelectionData/get-selection-data.service';
import { ISingleBet } from '@core/models/single-bet.model';
import { FreeBetType } from '@betslip/services/freeBet/free-bet.model';
import { ItoteFreeBets } from '@betslip/services/toteBetslip/tote-betslip.model';

import environment from '@environment/oxygenEnvConfig';
 
@Component({
  selector: 'betslip',
  templateUrl: 'betslip.component.html',
  styleUrls: ['./betslip.component.scss']
})
export class BetslipComponent implements OnInit, OnDestroy {

  @Input() hidden: boolean;
  @Output() readonly heightChanged = new EventEmitter<number>();

  currencySymbol: string;
  isAndroidBrowser: boolean;
  isOldIos: boolean;
  placeBetsPending: boolean = false;
  loginAndPlaceBets: boolean = false;
  bsButtonTitle: string;
  depositButtonTitle: string;
  betslipMessage = { type: '', msg: '' };
  oldPrice = {};
  estimatedReturnAfterPriceChange: number;
  quickDeposit: IBetslipDepositData;
  isLiveEvent: boolean = false;
  bonusValue= '£0.00';

  placeSuspendedErr: ISuspendedOutcomeError;

  betSlipSingles: any;
  betSlipMultiples: any;
  accaBets: any;
  notAccaBets: any;
  betResponseData:any;

  allStakes: { value: string | any } = { value: '' };
  isDidigitKeyboardInit: boolean = false;
  isDigitKeyboardShown: boolean;
  isBetSlipEmpty: boolean;
  loadComplete: boolean = false;
  loadFailed: boolean = false;
  multiplesShouldBeRebuilded: boolean;
  noActiveSelections: boolean;
  placeStakeErr: string;
  isBetsSelected: boolean = false;
  isOveraskCanBePlaced: boolean = false;

  multiplesSectionCount: string;
  priceChangeBannerMsg: string;
  potentialPayoutObj = null;
  debouncePlaceBets;
  toteBetGeneralError = null;
  toteBetSuspendedError = null;
  toteError = null;
  countDownClock: string;
  toteBetSlip: ToteBetslipService;
  betType: string;
  isBoostEnabled: boolean;  // True, if odds boost is enabled in CMS.
  isBoostActive: boolean;   // True, if odds boost activated via "Boost" button

  hasBetsWithTooLowStake: boolean;
  isSelectionSuspended: boolean = false;
  quickStakeVisible: boolean = true;

  overaskProcessingTitle: string;
  overaskProcessingTopMessage: string;
  overaskProcessingBottomMessage: string;
  overaskDrawerIsConfigured: boolean = false;
  freeBetAvailable: boolean;
  betTokensAvailable: boolean;
  isToteFreeBetAvailable = false;
  isToteBetTokensAvailable = false;
  fanZoneAvailable: boolean;
  hideAvailableFreeBetsMessage: boolean = false;
  hideEmptyBetslip: boolean = false;
  isTablet: boolean;

  showIFrame = false;
  quickDepositIFrameFormExpanded = false;
  iframeLoadingInProgress = false;
  errorMessage: string;
  neededAmountForPlaceBetIsChanged = false;
  totalStakeAmount: string;
  changedFromAllStakeField = false;
  isZeroBalanceWithExistingBets = false;
  amountNeededErrorMessage: string;
  maxPayFlag: boolean;
  maxPayMsg: string;
  isHeightUpdated = false;
  bsMaxHeightLimit: number;
  bsMaxHeight = '100%';
  freebetsConfig: IFreebetsPopupDetails;
  disableEachWayTooltip:boolean = false;
  toteFreeBetSelected: boolean = false;
  delay:number;
  Tooltip_Enable:boolean;
  betslipData:any;
  horseIndex:number;
  toolTipMessage:string;
  BetSlip_EachWay_Tooltip: string = 'BetSlipTooltipEachWay';
  toolTipArgs: {[key: string]: string};
  restrictedHorseTooltipData: {[key: string]: string};
  restrictedRaceCardTooltipData: {[key: string]: string};
  eachWayGaTracking:boolean = false;
  estReturn: any;
  deviceViewType:IDeviceViewType;
  availableToteFreeBets: ItoteFreeBets[];
  availableToteBetPacks: ItoteFreeBets[];
  showLuckySignPost:boolean = false;
  isLuckyAvailable: boolean = false;
  showLuckysignPostLabel: boolean = false;
  usedTotefreebetsList: any = [];
  selectedToteFreeBetObj: any;

  readonly tagName: string = 'BetSlip';  
  private readonly globalStake = 'global_stakes';
  private readonly betslipType = 'betslip_stakes';
  readonly promoLabelsFlagsExcluded = 'EVFLAG_EPR,MKTFLAG_EPR';

  readonly betProvider = 'OpenBetBir';
  readonly claimedOffers = 'claimedOffers';
  readonly claimed = 'claimed';
  readonly bsHeightStakesCount = 4;
  readonly stakePattern: string = '^(\\d{0,12}((\\.|,)\\d{0,2})?)?$';
  private readonly categoryList: any = environment.CATEGORIES_DATA.categoryIds;

  protected currentStakeWithoutDisabledBets: number;
  protected isToteBets: boolean = false;
  protected reboost: boolean;
  protected betData: any = [];
  private readonly MIN_PAYOUT_ACCA: number = 1.00099;
  private betslipErrorTracking: Function;
  private betId;
  private dsBetsCounter: number = 0;
  public isMobile: boolean;
  private popupsShown: boolean;
  private rebuildBetslip: boolean;
  private fetchedData: Bet[] = [];
  private firstRunOfBetSlip: boolean = true;
  private betSlipInitDone: boolean = false;
  private emptyStake: boolean = false;
  private suspendedOutcomesCounter: number;
  private priceChangeBets = new Set();
  public currentStake: number;
  private countDownValue;
  private isLoginAndPlaceBetsInterrupted: boolean;
  private fetchSubscription: Subscription;
  private scrollWrapperRendered$: Subject<null> = new Subject();
  private scrollWrapperSubjectClosed$: Subject<null>;
  private scrollWrapperEl: HTMLElement;
  private betslipIsOpened: boolean = false;
  private quickDepositEnabledSub: Subscription;
  private sub: Subscription;
  private isAlreadyReloaded: boolean = false;
  private bsWrapperEl: HTMLElement;
  private bsScrollWrapperEl: HTMLElement;
  private singleStakesWrapperEl: HTMLElement;
  private freeBetsData: IFreebetToken[] = [];
  private isFreeBetApplied: boolean = false;
  private notifyTimeout: number;
  public restrictedHorseMsg: string;
  public restrictedRaceCardMsg: string;
  public horseTooltipMessage: string;
  public raceCardTooltipMessage: string;
  public horseNames = [];
  public lottoErrorMsg: IBetError;
  public restrictedRaces: any = [];
  public isShowHorseRestrictedInfo: boolean = false;
  public isShowRacecardRestrictedInfo: boolean = false;
  public eventIdDetails = [];
  public isRestrictedHorsesLoaded: boolean = false;
  public isRestrictedRacecardLoaded: boolean = false;
  private selectedToteFreeBetValue: any;
  public isRestrictedData:boolean = false;
  updatedToteFreeBetValue: number;
  toteStake: string;
  stakePerLine: any;

  private errorDictionary = {
    INSUFFICIENT_FUNDS: this.handleInsufficientFunds.bind(this)
  };
  private readonly BPP_TIMEOUT_ERROR: number = 2100;
  onBoardingData: { step: string; tutorialEnabled: boolean; type: string; };
  lottobetslipData: any;
  lottoBetsContainerEl: HTMLElement;  
  quickStakeItems: string[] | number[];

  @ViewChild('scrollWrapper', { static: false }) set scrollWrapper(elementRef: ElementRef) {
    if (elementRef && elementRef.nativeElement) {
      this.scrollWrapperEl = elementRef.nativeElement;
      this.scrollWrapperRendered$.next(null);
    }
  }

  @ViewChild('bsWrapper', { static: false }) set bsWrapper(elementRef: ElementRef) {
    if (elementRef && elementRef.nativeElement) {
      this.bsWrapperEl = elementRef.nativeElement;
    }
  }

  @ViewChild('singleStakesWrapper', { static: false }) set singleStakesWrapper(elementRef: ElementRef) {
    if (elementRef && elementRef.nativeElement) {
      this.singleStakesWrapperEl = elementRef.nativeElement;
    }
  }
  
  constructor(protected overAskService: OverAskService,
    protected windowRefService: WindowRefService,
    protected betslipLiveUpdateService: BetslipLiveUpdateService,
    protected betslipService: BetslipService,
    protected toteBetslipService: ToteBetslipService,
    public userService: UserService,
    protected resolveService: ResolveService,
    protected betReceiptService: BetReceiptService,
    protected localeService: LocaleService,
    protected quickDepositService: QuickDepositService,
    protected betInfoDialogService: BetInfoDialogService,
    protected infoDialogService: InfoDialogService,
    protected storageService: StorageService,
    protected digitalSportBetsService: DigitalSportBetsService,
    protected deviceService: DeviceService,
    protected freeBetsService: FreeBetsService,
    protected sessionService: SessionService,
    protected fracToDecService: FracToDecService,
    protected gtmService: GtmService,
    protected pubSubService: PubSubService,
    protected commandService: CommandService,
    protected toteBetReceiptService: ToteBetReceiptService,
    protected bsFiltersService: BetslipFiltersService,
    protected betslipStorageService: BetslipStorageService,
    protected betslipDataService: BetslipDataService,
    protected cmsService: CmsService,
    public betslipStakeService: BetslipStakeService,
    protected datePipe: DatePipe,
    protected filterService: FiltersService,
    protected awsService: AWSFirehoseService,
    protected router: Router,
    protected routingState: RoutingState,
    protected timeService: TimeService,
    protected bodyScrollLockService: BodyScrollLockService,
    protected dialogService: DialogService,
    protected componentFactoryResolver: ComponentFactoryResolver,
    private accountUpgradeLinkService: AccountUpgradeLinkService,
    private quickDepositIframeService: QuickDepositIframeService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected serviceClosureService: ServiceClosureService,
    public siteServerRequestHelperService: SiteServerRequestHelperService,
    protected sessionStorageService: SessionStorageService,
    protected coreToolsService: CoreToolsService,
    protected signpostingCmsService: SignpostingCmsService,
    protected getSelectionDataService: GetSelectionDataService
  ) {
    this.toteBetSlip = toteBetslipService;
    this.placeBets = this.placeBets.bind(this);
    this.afterLoginHandler = this.afterLoginHandler.bind(this);
    this.selectionLiveUpdate = this.selectionLiveUpdate.bind(this);
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      if (config.maxPayOut) {
        this.maxPayFlag = config.maxPayOut.maxPayoutFlag;
        this.maxPayMsg = config.maxPayOut.maxPayoutMsg;
      }
      this.freebetsConfig = config.FreeBets;
      this.toteBetslipService.setFreeBetsConfig(this.freebetsConfig);
      if (config.restrictedHRMessages?.enabled) {
        this.restrictedHorseMsg = config['restrictedHRMessages'].restrictedHorseMsg;
        this.restrictedRaceCardMsg = config['restrictedHRMessages'].restrictedRaceCardMsg;
        this.horseTooltipMessage = config['restrictedHRMessages'].restrictedHorseTooltip;
        this.raceCardTooltipMessage = config['restrictedHRMessages'].restrictedRaceCardTooltip;
        this.restrictedHorseTooltipData = {
          restrictedHorseTooltipMessage: this.horseTooltipMessage
        }
        this.restrictedRaceCardTooltipData = {
          restrictedRaceCardTooltipMessage: this.raceCardTooltipMessage
        }
      }
      if (config.eachWayTooltip && config.eachWayTooltip.Enable) {
        this.delay = config.eachWayTooltip.Delay;
        this.toolTipMessage = config.eachWayTooltip.Message;
        this.Tooltip_Enable = config.eachWayTooltip.Enable;
      }
    });
    this.cmsService.getQuickStakes(this.betslipType).subscribe((predefinedStakes: string[]) => {
      this.quickStakeItems = predefinedStakes;
      this.formatBetslipStakes(this.quickStakeItems);
    });
    this.deviceViewType = this.deviceService.getDeviceViewType();
  }

  get countDownCurrentValue(): string {
    return this.quickDepositService.countDownCurrentValue;
  }
  set countDownCurrentValue(value: string) { }
  get overask(): OverAskService {
    return this.overAskService;
  }
  set overask(value: OverAskService) { }
  get totalStakeIsPresent(): boolean {
    const liveBetData = this.betData.filter(bet => bet.Bet && bet.Bet.legs.filter(leg => leg.selection.eventIsLive).length &&
      (bet.selectedFreeBet || bet.stake.stakePerLine));
    this.isLiveEvent = liveBetData.length > 0;
    if(this.areToteBetsInBetslip() && this.toteFreeBetSelected) {
      return this.toteFreeBetSelected;
    } else {
      const totalStake = this.areToteBetsInBetslip() ?
      this.toteBetslipService.getTotalStake() :
      this.betslipStakeService.getTotalStake(this.betData);
      return totalStake && totalStake !== '0.00';
    } 
    
   
  }
  set totalStakeIsPresent(value: boolean) { }
  get defaultQuickDepositData(): IBetslipDepositData {
    return {
      quickDepositPending: false,
      quickDepositFormAllowed: false,
      showQuickDepositForm: false,
      quickDepositFormExpanded: false,
      neededAmountForPlaceBet: undefined
    };
  }
  set defaultQuickDepositData(value: IBetslipDepositData) { }
  get infoDialogComponent(): Type<SelectionInfoDialogComponent> {
    return SelectionInfoDialogComponent;
  }
  set infoDialogComponent(value: Type<SelectionInfoDialogComponent>) { }
  ngOnInit() {
    this.fetchToteFreeBetsStorage();
    this.setQuickDepositInitialData();
    this.serviceClosureService.checkUserServiceClosureStatus();

    this.betslipErrorTracking = this.commandService.execute(this.commandService.API.BESTLIP_ERROR_TRACKING, undefined, () => {
      console.warn('betslipErrorTracking functionality not found');
    });
    
    this.toteBetslipService.reload();
    // do not remove this hack.
    this.currencySymbol = this.userService.currencySymbol;
    this.isAndroidBrowser = this.deviceService.browserName === BETSLIP_VALUES.ANDROID_NATIVE;
    this.isOldIos = this.deviceService.isIos && Number(this.deviceService.osVersion) <= BETSLIP_VALUES.OLD_IOS;
    this.isMobile = this.deviceService.isMobile;
    this.isTablet = this.deviceService.isTablet;

    this.updateBsButtonTitle();

    this.digitalSportBetsService.getDSBetslipCounter((betsNumber: number) => {
      this.dsBetsCounter = betsNumber;
    });

    // Apply calculations for events which is from cache each/way.
    _.each(this.betSlipSingles, (bet: any, i) => {
      if (bet.isEachWayAvailable) {
        this.winOrEachWay(bet);
      }
    });

    /**
     * Call placeBets fn with 1 sec debounce effect to prevent extra clicks.
     */
    this.debouncePlaceBets = _.debounce(() => {
      this.placeBets().subscribe(null, (e) => console.warn(e));
      this.awsService.addAction('betSlipComponent=>placeBetRequest=>COMMON');
    }, 1000, true);

    this.init();

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.SESSION_LOGOUT, () => {
      // this callback could be executed before init() finished - skip for first ini
      if (this.firstRunOfBetSlip && !this.loadComplete && !this.loadFailed) { return; }
      this.quickDeposit = this.defaultQuickDepositData; // rollback deposit data to default state

      this.init();

      this.updatePlaceBetsPending(false);

      this.updateBsButtonTitle();

      this.quickDeposit.quickDepositPending = false;

      if (this.betReceiptService.message
        && this.betReceiptService.message.msg === this.localeService.getString('bs.depositAndPlacebetSuccessMessage')) {
        this.betReceiptService.message.msg = undefined;
      }
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.RELOAD_COMPONENTS, () => {
      this.windowRefService.nativeWindow.setTimeout(() => {
        if (this.overask.bsMode !== 'Bet Receipt') {
          this.quickDeposit.quickDepositPending = false;
          this.betslipLiveUpdateService.reconnect();
          this.rebuildBetslip = false;
          this.isAlreadyReloaded = true;
          this.init();
        }
      }, 1000);
    });

    // //////////////////////////////////////////////////////////////////
    // /////////////////////////// Overask //////////////////////////////
    // //////////////////////////////////////////////////////////////////

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.EXECUTE_OVERASK, responseData => {
      this.placeStakeErr = null;

      const overaskData = this.betslipService.parsePlaceBetsResponse(responseData);

      this.betId = overaskData.selectionId;
      this.init(undefined, false, overaskData);

      this.changeDetectorRef.detectChanges();
    });

    // stop placing bet if notification popup is displayed after used has logged in
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.USER_INTERACTION_REQUIRED, () => {
      this.loginAndPlaceBets = false;
      this.isLoginAndPlaceBetsInterrupted = true;
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.OVERASK_CLEAN_BETSLIP, ({ closeSlideOut, isOveraskCanceled }) => {
      this.cleanBetslip(closeSlideOut, isOveraskCanceled);
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.OVERASK_BETS_DATA_UPDATED, overaskMessage => {
      if (this.fetchedData && this.fetchedData.length) { // data is empty on page refresh (not yet fetched from SS)
        this.core(this.fetchedData);

        // If overask message is shown to user - scroll to action buttons in betslip to make them
        // visible to user.
        if (overaskMessage) {
          this.scrollToActionButtons();
        }
      }
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.OVERASK_STATE_RESTORED,
      placeBetsData => {
        this.placeBetsResponseProcess(placeBetsData);
      });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.OVERASK_STATE_RESTORE_FAILED, error => {
      console.warn(error);
      this.updatePlaceBetsPending(false);
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.OVERASK_REVIEW_STARTED, this.handleOverAskProcessing.bind(this));

    // Fetch bet slip data on selection change
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.BETSLIP_UPDATED, (data) => {
      this.placeStakeErr = null;
      if(!this.deviceViewType.mobile && !this.deviceViewType.tablet){
        this.showEachWayTooltip();
      }
      if (!data || !data.selectionId) {
        this.init(data);
        return;
      }
      this.betId = data.selectionId;
      this.init();
    });

    // reload betSlip on login (unless bet should be placed after login)
    this.pubSubService.subscribe(
      this.tagName,
      [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGIN],
      placeBet => {
        this.betslipSuccessfulLogin(placeBet);
        this.serviceClosureService.checkUserServiceClosureStatus();
      });

    // Reload betslip after user presses "Reload" button after previous unsuccessful betslip load.
    this.pubSubService.subscribe(this.tagName, [this.pubSubService.API.REFRESH_BETSLIP],
      () => {
        this.rebuildBetslip = false;
        this.reloadComponent();
      });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.SET_ODDS_FORMAT, () => {
      this.accaNotificationChanged();
      this.init();
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.LOGIN_POPUPS_START, () => {
      this.popupsShown = true;
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.HOME_BETSLIP, (mode: string) => {
      this.hideEmptyBetslip = false;
    });

    // place bets on 'login and place bets' action
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.LOGIN_POPUPS_END, () => {
      const isFreebetsAvailable = this.freeBetsService.getFreeBetsState().available;
      this.popupsShown = false;
      if (this.loginAndPlaceBets && !this.serviceClosureService.userServiceClosureOrPlayBreak) {
        this.loginAndPlaceBets = false;
        this.placeBets().subscribe(null, null, () => isFreebetsAvailable && this.init());
        this.awsService.addAction('betSlipComponent=>placeBetRequest=>LOGIN_AND_PLACE_BET');
        this.onShowQuickDepositWindow();
      } else if (isFreebetsAvailable && this.isLoginAndPlaceBetsInterrupted && !this.isShowQuickDepositBtnShown()) {
        this.isLoginAndPlaceBetsInterrupted = false;
        this.init();
      }
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.SYSTEM_CONFIG_UPDATED, updatedConfig => {
      if (!updatedConfig) {
        return;
      }

      this.betslipService.getConfig().subscribe((conf: IBetslipConfig) => {
        if (!_.isEqual(conf, updatedConfig.Betslip)) {
          this.betslipService.setConfig(updatedConfig.Betslip);
          this.init();
        }
      });
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.TOTE_BETSLIP_UPDATED, toteBetSuspendedError => {
      this.toteBetSuspendedError = toteBetSuspendedError || null;
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.REUSE_TOTEBET, () => {
      this.isBetSlipEmpty = false;
    });

    // Close bet receipt when slide out betslip was closed
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API['show-slide-out-betslip-false'], () => {
      this.placeStakeErr = null;
    });

    this.activateOddsBoost();
    this.pubSubService.publish('ACCA_NOTIFICATION_ENABLE', true);

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.DIGIT_KEYBOARD_SHOWN,
      (decBtn: boolean, quickDepBtn: boolean, quickStakeItems: string[], kbId: string) => this.digitKeyboardShown(decBtn, quickDepBtn, quickStakeItems,kbId));

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.DIGIT_KEYBOARD_HIDDEN,
      (kbId: string) => this.digitKeyboardHidden(kbId));

    // Fix is needed only for mobile iOS
    if (this.deviceService.isMobile && this.deviceService.isIos) {
      this.pubSubService.subscribe(this.tagName, this.pubSubService.API.BETSLIP_SIDE_BAR_MOTION, (show: boolean) => {
        // Element exists
        this.betslipIsOpened = show;
        if (this.scrollWrapperEl && this.scrollContainerRendered()) {
          this.lockBodyScroll(show);
        } else {
          // sync trigger betslip open and view render
          if (show) {
            this.lockBodyScrollAfterRender();
          } else {
            // discard waiting of bestlip view rendering
            this.scrollWrapperSubjectClosed$.next(null);
            this.scrollWrapperSubjectClosed$.complete();
          }
        }
      });
    }

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.BETSLIP_CLEAR_STAKE, (overAskBetId: string) => {
      const clearStakeBet = this.getAllBets().find(bet => bet.id === overAskBetId);

      if (clearStakeBet) {
        this.setAmount(clearStakeBet, '');
      }
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.BS_SELECTION_LIVE_UPDATE, this.selectionLiveUpdate);

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.ODDS_BOOST_REBOOST_CLICK, () => this.priceChangeBets.clear());

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.BS_BET_NOT_ALLOWED, () => {
      this.cleanBetslip();
      this.infoDialogService.openInfoDialog(
        this.localeService.getString('bs.cantBuildBs.title'), this.localeService.getString('bs.cantBuildBs.text')
      );
    });
    // display message about restricted horses by giving betslip data on odd selection
    this.pubSubService.subscribe('BETSLIP_BET_DATA', this.pubSubService.API.BETSLIP_BET_DATA, (res) => {
      if (res && res.bets) {
        this.betResponseData = res;
        this.isShowHorseRestrictedInfo = false;
        this.isShowRacecardRestrictedInfo = false;
        this.showLuckySignPostBanner(this.betResponseData)
      }
    });

    this.pubSubService.subscribe('RestrictedRacecard', this.pubSubService.API.SET_RESTRICTED_RACECARD, (res) => {
        this.checkHRRestrictionsIfAny(res);
    });
  
    this.restoreOveraskProcess();
    this.subscribeToVanillaEvents();
    this.clearOveraskSubscription();
    this.updateEachWayAvailable();
    this.getSignpostingInfo();
   }

  fetchToteFreeBetsStorage(): void {
    this.availableToteFreeBets = this.storageService.get('toteFreeBets');
    this.availableToteBetPacks = this.storageService.get('toteBetPacks');
    const toteBet = this.storageService.get('toteBet');
    this.isToteFreeBetAvailable = this.availableToteFreeBets?.length > 0;
    this.isToteBetTokensAvailable = this.availableToteBetPacks?.length > 0;
    if(toteBet !== null && toteBet && toteBet.poolBet) {
      this.toteFreeBetSelected = toteBet.poolBet.freebetTokenId;
      if(this.toteFreeBetSelected && (this.isToteFreeBetAvailable || this.isToteBetTokensAvailable)) {
        this.reAssignSelectedToteFreeBetObj(toteBet.poolBet.freebetTokenId,  this.availableToteFreeBets, this.availableToteBetPacks)
      }
    }
  }
  
   reAssignSelectedToteFreeBetObj(freebetTokenId, toteFreeBets, toteBetPacks) : void {
      const filteredToteBet = toteFreeBets && toteFreeBets.filter(list => list.freebetTokenId === freebetTokenId);
      const filteredToteBetPack = toteBetPacks && toteBetPacks.filter(list => list.freebetTokenId === freebetTokenId);
      if(filteredToteBet.length > 0) {
        this.selectedToteFreeBetObj = filteredToteBet;
      } else if(filteredToteBetPack.length > 0) {
        this.selectedToteFreeBetObj = filteredToteBetPack;
      }
      if(this.selectedToteFreeBetObj) {
        this.selectedToteFreeBetValue = this.selectedToteFreeBetObj[0].freebetTokenValue;
        this.updatedToteFreeBetValue = this.selectedToteFreeBetObj[0].freebetTokenValue;
      }
   }
  /**
   * Gets and sets signposting configuration
  */
  private getSignpostingInfo(): void {
    if (!this.signpostingCmsService.freeBetSignpostingArray) {
      this.signpostingCmsService.getFreebetSignposting().subscribe(res => {
        if (res) {
          this.signpostingCmsService.freeBetSignpostingArray = res;
        }
      });
    }
  }

  formatBetslipStakes(quickStakeItems: string[]) {
    this.quickStakeItems = quickStakeItems.map((stake: string) => {
      const dec = stake.split('.');
      if (dec.length > 1) {
        dec[1] = dec[1].substring(0, 2);
        stake = dec.join(".");
      }
      return stake;
    });
  }

  private checkHRRestrictionsIfAny(response){
    if(Array.isArray(response) && response.length>0){
      if(response.every(outcome=>outcome.categoryId != '21')){
        this.initRestrictedSelections();
        return;
      }
    }
    this.initRestrictedSelections();
    const finalSSObj = !response ? this.getSelectionDataService.outcomeData : response.SSResponse?.children;
    if(finalSSObj){
        finalSSObj.forEach((eventObj) => {
            if (eventObj.event) {
                eventObj.event.children.forEach((marketObj) => {
                  if (marketObj.market) {
                    if (eventObj.event){
                      const restrictedHRSelections = this.getSelectionDataService.restrictedRacecardAndSelections(marketObj.market, eventObj.event,this.betResponseData?.outcomeDetails);
                      this.horseNames = [...new Set([...this.horseNames ,...restrictedHRSelections.horseNames])];
                      this.restrictedRaces = [...new Set([...this.restrictedRaces ,...restrictedHRSelections.restrictedRaces])];
                      this.eventIdDetails = [...new Set([...this.eventIdDetails ,...restrictedHRSelections.eventIdDetails])];
                      this.isRestrictedData = (this.horseNames.length>0 || this.restrictedRaces.length>0)? true:false;
                    }
                  }
                });
            
            }
          });
      }
  } 
  showLuckySignPostBanner(response:any): void {
    let otherSport = false;
    const onlyHRGHids = response && response.outcomeDetails && response.outcomeDetails.filter(outcome => {
      if(!otherSport){
        otherSport = this.categoryList.includes(outcome.categoryId);
      }
      return (outcome.categoryId === '19' || outcome.categoryId === '21');
    });
    this.showLuckySignPost = ((onlyHRGHids && onlyHRGHids.length >= 4 && !otherSport) ? true : false);
    this.isLuckyAvailable = response.bets.filter(element=>{
      return ['L15', 'L31', 'L63'].includes(element.betTypeRef.id) && element.availableBonuses && this.betReceiptService.isBonusApplicable(element.availableBonuses)
    }).length !== 0;
    this.betReceiptService.isLuckyBonusAvailable = this.isLuckyAvailable;
}

  private initRestrictedSelections(){
    this.horseNames = [];
    this.restrictedRaces = [];
    this.eventIdDetails = [];
    this.isRestrictedData = false;
  }

  reloadComponent(): void {
    if (!this.isAlreadyReloaded) {
      this.init();
    }
  }

  /**
   * Handler for the successful login event
   * @param placeBet - name of the component which initiated the login process
   */
  betslipSuccessfulLogin(placeBet) {
    if (this.userService.bppToken && this.overask.bsMode !== 'Bet Receipt') {
      this.init();
    }

    this.pubSubService.publishSync(this.pubSubService.API.BETSLIP_COUNTER_UPDATE, this.betslipService.count());

    this.activateOddsBoost();
    this.firstRunOfBetSlip = true;

    this.updateBsButtonTitle();

    if (this.userService.status && placeBet === 'betslip' && !Number(this.quickDeposit.neededAmountForPlaceBet)) {
      this.loginAndPlaceBets = true;
    }
  }

  activateOddsBoost(): void {
    if (!this.userService.status) { return; }

    this.cmsService.getOddsBoost().pipe(
      map(config => config.enabled),
      mergeMap(enabled => {
        if (!enabled) {
          return of([false, false]);
        } else {
          return observableFrom(
            this.commandService.executeAsync(this.commandService.API.GET_ODDS_BOOST_ACTIVE)
          ).pipe(map(active => [enabled, active]));
        }
      })).subscribe((data: [boolean, boolean]) => {
        [this.isBoostEnabled, this.isBoostActive] = data;

        if (this.isBoostEnabled) {
          this.subscribeToOddsBoostChange();
          this.pubSubService.subscribe(this.tagName, this.pubSubService.API.ODDS_BOOST_UNSET_FREEBETS, () => {
            this.unsetFreeBets(this.betSlipSingles);
            this.unsetFreeBets(this.betSlipMultiples);
          });
        }
      });
  }

  ngOnDestroy(): void {
    if (this.quickDeposit.quickDepositPending) {
      this.quickDepositService.quickDepositCache = this.quickDeposit;
    }
    this.pubSubService.unsubscribe(this.tagName);

    // Clear Data to prevent crash if user goes to home page with widget.
    this.resolveService.reset('betslip');

    this.overAskService.clearBetsData(); // clear betsData model in overask
    this.betslipLiveUpdateService.clearAllSubs();
    this.toteBetslipService.clear();

    this.scrollWrapperSubjectClosed$ && this.scrollWrapperSubjectClosed$.unsubscribe();
    this.scrollWrapperRendered$ && this.scrollWrapperRendered$.unsubscribe();
    this.pubSubService.publish('ACCA_NOTIFICATION_ENABLE', false);
    this.fetchSubscription && this.fetchSubscription.unsubscribe();
    this.pubSubService.unsubscribe('BetSlipVanilla');
    this.quickDepositEnabledSub && this.quickDepositEnabledSub.unsubscribe();
    this.sub && this.sub.unsubscribe();
    this.windowRefService.nativeWindow.clearTimeout(this.notifyTimeout);
  }

  get isNoSelections(): boolean {
    return this.loadComplete && this.isBetSlipEmpty && !(this.betSlipSingles && this.betSlipSingles.length);
  }
  set isNoSelections(value: boolean) { }
  setFocusIndex(betType: string): void {
    this.changedFromAllStakeField = false;
    this.betType = betType;
  }

  getAccatype(betslipStake: IBetPrice): string {
    return this.localeService.getString(`bs.${betslipStake.type}`);
  }

  areToteBetsInBetslip(): boolean {
    this.fetchToteFreeBetsStorage()
    return !this.betslipDataService.containsRegularBets() && this.toteBetslipService.isToteBetPresent();
  }

  accaTemplate(potentialPayout: number, numberOfSelections: number): string {
    let template;

    if (this.betSlipSingles.length > 2 && numberOfSelections > 0) {
      template = 1;
    } else if (numberOfSelections < 1 && potentialPayout < 4) {
      template = 2;
    } else {
      template = 3;
    }

    return `acca-notification-${template}`;
  }

  isSuccess(potentialPayout: number, numberOfSelections: number): boolean {
    return potentialPayout > 4 && numberOfSelections < 1;
  }

  /**
   * Returns true if any bet has an error
   * and removes this error in case of live serve updates for not blinking
   * @return {boolean}
   */
  hasErrors(): boolean {
    const betsErr = _.some(this.betData, (bet: any) => {
      return bet.errorMsg || bet.error > 0;
    }),
      handicapBetsErr = _.some(this.betData, (bet: any) => {
        return bet.handicapErrorMsg || bet.handicapError > 0;
      });

    // if there are any other error message in the betslip(but just in case if suspended error is present
    // and all stakes are empty show placeBetAlertMessage)
    if (((this.placeSuspendedErr && this.placeSuspendedErr.msg) || betsErr || handicapBetsErr) && !this.emptyStake) {
      // remove placeStakeErr (it has lower priority)
      this.placeStakeErr = null;
      this.emptyStake = false;
      return true;
    }

    return false;
  }


  /**
   * W/E checkbox state defines type of stake and calculate related estimate amount
   * @param bet
   * @param $event
   */
  winOrEachWay(bet: any, $event?: MouseEvent): void {
    this.placeStakeErr = null;
    bet.Bet.isEachWay = !bet.Bet.isEachWay;
    // Do not check checkbox if freebetValue / lines < 0.01 and show popup;
    if (bet.Bet.isEachWay && bet.selectedFreeBet && !this.betslipService.isFreeBetValid(bet.selectedFreeBet.value, bet)) {
      bet.Bet.isEachWay = !bet.Bet.isEachWay;
      this.showUnvalidFreeBetPopup();
      $event.preventDefault();
      return;
    }
    this.betslipService.winOrEachWay(bet);
    if (bet.selectedFreeBet) {
      bet.stake.freeBetAmount = Math.floor(bet.selectedFreeBet.value / (bet.stakeMultiplier * (bet.Bet.isEachWay ? 2 : 1)) * 100) / 100;
    }
    if (this.isBoostActive) {
      this.maxStakeExceeded();
    }
    // GA tracking for freebet eachway signposting 
    this.gaTrackingOnEachWayChange(bet);

    // GA tracking for eachway checkbox
    if (bet && bet.sportId === "21") {
      this.gaTrackingOnEachWayCheckBox(bet);
    }
  }

  /**
   * Clear input values and selected free bet for disabled selections
   */
  clearUserValueForDisabledBets(): void {
    _.each(this.betSlipSingles, (bet: any) => {
      if (bet.disabled) {
        bet.stake.perLine = '';
        if (bet.selectedFreeBet) {
          bet.selectedFreeBet = null;
          this.setFreebet(bet);
        }
      }
    });
  }

  handleFreebetOutput(event: ILazyComponentOutput, bet: IBetslipBetData): void {
    if (event.output === 'selectedChange') {

      //When a free bet is selected, hide the free bet notificaiton and make the stake per line 0.
      this.hideFreeBetNotification();
      if (event.value && bet.stake.perLine && Number(bet.stake.perLine) > 0) {
        this.setAmount(bet, '');
      }

      if (event.value && !this.betslipService.isFreeBetValid(event.value.value, bet)) {
        this.showUnvalidFreeBetPopup();

        return;
      }

      bet.selectedFreeBet = event.value;
      this.setFreebet(bet);
      this.checkStakeStatus();
    } else if(event.output === 'toteBet') {
      this.selectedToteFreeBetObj = event.value;
      this.toteBetSlip.toteBet.poolBet.stakePerLine = '';
      this.hideFreeBetNotification();
      const x = this.storageService.get('toteBet');
      let numOfLines;
      if(x.poolBet.poolType === 'UTRI') {
        numOfLines = Number(x.toteBetDetails.betName.split(' ')[0]);
      } else if(x.poolBet.poolType === 'UEXA') {
        if(x.toteBetDetails.betName.split(' ')[0] === '1' && x.toteBetDetails.betName.split(' ')[1] === 'REVERSE') {
          numOfLines = 2;
        } else {
          numOfLines = Number(x.toteBetDetails.betName.split(' ')[0]);
        }
      } else {
        numOfLines = 0;
        if(x.toteBetDetails){
          const orderedOutcomes = x.toteBetDetails.orderedOutcomes ? x.toteBetDetails.orderedOutcomes.length : 0;
          numOfLines = x.toteBetDetails.numberOfLines ? x.toteBetDetails.numberOfLines: orderedOutcomes;
        }
      }
      const freeBetPerLine = (Number(event.value.freebetTokenValue)/numOfLines);
      this.updatedToteFreeBetValue = this.toteBetslipService.getRoundedValue(freeBetPerLine) * numOfLines;
      this.selectedToteFreeBetValue = Number(event.value.freebetTokenValue);
      this.toteFreeBetSelected = true;
    } else if(event.output === 'removetoteFreeBet') {
      this.selectedToteFreeBetValue = null;
      this.updatedToteFreeBetValue = null;
      this.toteFreeBetSelected = false;
      this.selectedToteFreeBetObj = null;
      this.deleteFromToteBetStorage();
      
    }
  }

  deleteFromToteBetStorage(): void {
    const toteBet = this.storageService.get('toteBet');
    if (toteBet && toteBet.poolBet) {
      if (toteBet.poolBet.freebetTokenId) {
        delete toteBet.poolBet.freebetTokenId;
      }
      if (toteBet.poolBet.freebetTokenValue) {
        delete toteBet.poolBet.freebetTokenValue;
      }
    }
    this.storageService.set('toteBet', toteBet);
  }

  fetchStakePerLine() {
    //const stakePerLine = this.toteBetSlip?.toteBet?.poolBet?.stakePerLine?.replace(",",".");
    const stakePerLine = this.toteBetSlip && this.toteBetSlip.toteBet && this.toteBetSlip.toteBet.poolBet && 
    this.toteBetSlip.toteBet.poolBet.stakePerLine;
    if(stakePerLine === '' || stakePerLine === null || stakePerLine === undefined) {
      return this.updatedToteFreeBetValue;
    } else if(stakePerLine && this.selectedToteFreeBetValue) {
      return this.selectedToteFreeBetValue;
    } else {
      return this.selectedToteFreeBetValue;
    }
  }
  /**
   * Sets free bet for stake.
   * @param bet
   */
  setFreebet(bet): void {
    this.placeStakeErr = null;
    bet.errorMsg = null;
    bet.handicapErrorMsg = null;

    bet.Bet.freeBet = bet.selectedFreeBet;
    this.betslipService.updateAvailableFreeBets(this.betData);

    if (bet.error === BETSLIP_VALUES.ERRORS.PRICE_CHANGED) {
      this.clearSingleBetPriceChangeErr(bet);
    }

    // check if to show and then set multiple suspended error
    this.setMultipleSuspendedErrMsg(bet);

    if (bet.selectedFreeBet) {
      this.pubSubService.publish(this.pubSubService.API.SET_FREE_BET);
      bet.stake.freeBetAmount = Math.floor(bet.selectedFreeBet.value * 100 / (bet.stakeMultiplier * (bet.Bet.isEachWay ? 2 : 1))) / 100;
    } else {
      bet.stake.freeBetAmount = undefined;
    }

    // Set free bet to be remembered for auto refresh
    this.betslipStorageService.setFreeBet(bet);

    if (this.isBoostActive && bet.selectedFreeBet) {
      this.commandService.execute(this.commandService.API.ODDS_BOOST_SHOW_FB_DIALOG, [true, 'betslip']);
    }

    this.priceChangeBets.delete(bet.id);
    this.detectBetsWithTooLowStake();
  }

  /**
   * Returns odds in correct format
   * @param betslipStake {object}
   * @return {string}
   */
  odds(betslipStake): string {
    let price;
    if (betslipStake.price) {
      price = (betslipStake.price.oldPrice && this.userService.status && betslipStake.isStarted)
        ? betslipStake.price.oldPrice : betslipStake.price;
      return this.userService.oddsFormat === 'frac'
        ? (`${price.priceNum}/${price.priceDen}`) : Number(price.priceDec).toFixed(2);
    }
    return betslipStake.priceDec && betslipStake.priceDec.toFixed(2);
  }

  showPriceChangeNotification(): boolean {
    const shouldShowReboostNotification = this.isPriceUpdate() && this.reboost;
    return (this.priceChangeBets.size > 0 && !this.placeBetsPending && !this.placeSuspendedErr.msg && !this.countDownClock)
      || shouldShowReboostNotification;
  }

  /**
   * Should check if Deposit & Place Bet button title should be shown
   * @return {boolean}
   */
  isDepositAndPlaceBets(): boolean {
    return (!this.placeBetsPending && !this.overask.isNotInProcess || !this.quickDeposit.quickDepositPending);
  }

  /**
   *  Set and update button title depends on state (Hcap changes, price updates etc.)
   */
  setDepositBtnTitle(): boolean {
    if (this.isPriceOrHcapUpdate()) {
      this.depositButtonTitle = 'bs.acceptPlaceBetDeposit';
    } else {
      this.depositButtonTitle = 'bs.betslipDepositBtn';
    }
    return true;
  }

  openSelectionInfoDialog(betslipStake): void {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(this.infoDialogComponent);
    this.dialogService.openDialog(
      DialogService.API.selectionInfoDialog,
      componentFactory,
      true,
      {
        stake: betslipStake,
        odds: this.odds(betslipStake)
      }
    );
  }

  /**
   * Returns odds for ACCA and Double in correct format
   * @param betslipStake {object}
   * @return {string}
   */
  oddsACCA(betslipStake) {
    const userOddsFormat = this.userService.oddsFormat;
    // Recalculate potentialPayout
    let newPotentialPayout = <any>this.betslipService.getMultiplePotentialPayout(betslipStake);
    // Find if singles has old prices(price was changed)
    const singlesHasOldPrice = this.betslipService.isSinglesHasOldPrice(betslipStake);
    // Check if current price is different from previous
    const currentPriceIsValid = this.potentialPayoutObj
      ? (this.potentialPayoutObj.newPriceDec === newPotentialPayout)
      : false;
    // Check if potentialPayoutObj should be updated
    if (singlesHasOldPrice && !currentPriceIsValid) {
      // Update old price
      const oldPriceDec = this.potentialPayoutObj ? this.potentialPayoutObj.newPriceDec : betslipStake.potentialPayout;
      this.potentialPayoutObj =
        this.betslipService.buildPotentialPayoutObj(oldPriceDec, userOddsFormat, newPotentialPayout);
    } else if (!singlesHasOldPrice) {
      this.potentialPayoutObj = null;
    }

    const isBetValid = this.isAccaBetValid(newPotentialPayout);
    // Update new potentialPayout in multiple(Double) bet
    _.each(this.betSlipMultiples, (bet: any) => {
      if (bet.stakeMultiplier === 1 && !bet.isTraderChanged) {
        bet.potentialPayout = Number(newPotentialPayout);
      }
    });
    if (!isNaN(newPotentialPayout)) {
      newPotentialPayout = this.getFormattedPrice(newPotentialPayout);
      newPotentialPayout = this.fracToDecService.getAccumulatorPrice(newPotentialPayout);
    }
    return isBetValid ? newPotentialPayout : null;
  }


  /**
   * Returns changed odds in correct format
   * @param time {string}
   * @return {string}
   */
  getStakeTime(time): string {
    return this.timeService.getEventTime(time);
  }

  /**
   * Counts stake
   * @return {number}
   */
  stake(): number {
    return this.betslipStakeService.getStake(this.betData);
  }

  /**
   * Counts free bet stake
   * @return {number}
   */
  freeBetStake(): number {
    return +this.betslipStakeService.getFreeBetStake(this.betData);
  }

  getFreeBetLabelText(flag: boolean = false): string {
    if (((this.availableToteBetPacks && this.availableToteBetPacks.length > 0) || (this.availableToteFreeBets && this.availableToteFreeBets.length > 0)) && this.areToteBetsInBetslip()) {
      const x = this.storageService.get('toteBet');
      if(x && x.poolBet) {
        return (x.poolBet.betType ? this.localeService.getString('bs.betToken') : this.localeService.getString('bs.freeBet'));
      }
    } else {
      return this.betslipStakeService.getFreeBetLabelText(this.betData, flag);
    }
  }
  /**
   * Counts total stake
   * @return {string}
   */
  totalStake(): string {
    if (!this.areRegularBetsInBetslip() && this.areToteBetsInBetslip()) {
      this.isToteBets = true;
      return this.toteBetslipService.getTotalStake();
    }
    this.isToteBets = false;
    // Add second parameter to getStake method to allow taking into consideration suspended bets for quick deposit
    // Quick deposit should be opened and allow user to deposit even selected bet(s) will be suspended
    this.currentStake = this.betslipStakeService.getStake(this.betData, true);
    this.currentStakeWithoutDisabledBets = this.betslipStakeService.getStake(this.betData);
    const isShowQuickDeposit = this.currentStake > Number(this.userService.sportBalance);
    Object.assign(this.quickDeposit,
      this.quickDepositService.checkQuickDeposit(
        this.currentStakeWithoutDisabledBets,
        this.betslipStakeService.getFreeBetStake(this.betData, true),
        this.userService.sportBalance,
        (this.betSlipSingles && this.betSlipSingles.length),
        this.placeBetsPending,
        this.isSelectionSuspended,
        isShowQuickDeposit ? this.quickDeposit.showQuickDepositForm : false
      )
    );
    this.handleQuickDepositState();

    return this.betslipStakeService.getTotalStake(this.betData);
  }

  totalStakeWithOutFreeBets(): number | string {
    if(this.areToteBetsInBetslip()) {
      this.isToteBets = true;
      //const stakePerLine = this.toteBetSlip?.toteBet?.poolBet?.stakePerLine?.replace(",",".");
      const stakePerLine = this.toteBetSlip && this.toteBetSlip.toteBet && this.toteBetSlip.toteBet.poolBet && this.toteBetSlip.toteBet.poolBet.stakePerLine;
      if(stakePerLine === '' || stakePerLine === null || stakePerLine === undefined) {
        return this.toteBetslipService.getTotalStake();
      } else {
        const x = Number(this.selectedToteFreeBetValue - this.updatedToteFreeBetValue);
        if(this.updatedToteFreeBetValue && this.selectedToteFreeBetValue) {
          return this.toteBetslipService.getTotalStake(this.toteBetslipService.getRoundedValue(x));
        } else {
          return this.toteBetslipService.getTotalStake();
        }
      }
    }

    const result = this.betslipStakeService.getStake(this.betData, false);
    return this.totalFreeBetsStake() && !result ? null : result.toFixed(2);
  }

  totalFreeBetsStake(): string | null {
    if(this.areToteBetsInBetslip()) {
      return this.fetchStakePerLine();
    }
    const result = this.betslipStakeService.getFreeBetStake(this.betData, false);
    return result === '0.00' ? null : result;
  }

  /**
   * Counts total estimated returns for singles bets
   * @return {number||string}
   */
  totalEstReturns(): number | string {
    const estReturns = this.betslipStakeService.getTotalEstReturns(this.betData, this.areToteBetsInBetslip());
    this.betReceiptService.isbetSlipHaveEst = estReturns !== 'N/A';
    return estReturns === 'N/A' ? undefined : estReturns;
  }

  /**
   * Calculate Estimated Returns for Singles
   * @param {number} index
   * @return {string}
   */
  calculateEstReturns(index): number | string {
    const estReturn = this.betslipStakeService.calculateEstReturns(this.betSlipSingles[index], index);
    return _.isNumber(estReturn) ? this.filterService.setCurrency(estReturn, this.currencySymbol) : estReturn;
  }

  /**
   * Calculate Estimated Returns for Multiples
   * @param {number} index
   * @return {string}
   */
  calculateEstReturnsMultiples(index, bets): string | number {
     this.estReturn = this.betslipStakeService.calculateEstReturnsMultiples(bets[index], index);
    return _.isNumber(this.estReturn) ? this.filterService.setCurrency(this.estReturn, this.currencySymbol) : this.estReturn;
  }
 
  calculateAllWinnerBonus(): string {
    if(this.showLuckySignPost && this.betResponseData.bets && !this.betReceiptService.isSP(this.betResponseData)){
      return this.betReceiptService.luckyAllWinnersBonus(this.betResponseData, this.estReturn); 
    }
  }

  isShownAllWinner(): string | number {
    const luckbonus = this.betResponseData.bets.filter(element=>{
      return (['L15', 'L31', 'L63'].includes(element.betTypeRef && element.betTypeRef.id) || ['L15', 'L31', 'L63'].includes(element.betType)) && element.availableBonuses;
    });
    const isLuckyAll = this.betReceiptService.isAllWinnerOnlyApplicable(luckbonus[0]);
    if(isLuckyAll){
      if(!this.estReturn){
        this.bonusValue= '£0.00'
        return 1;
      }
      this.bonusValue = this.calculateAllWinnerBonus();
      return this.betReceiptService.returnAllWinner(this.bonusValue);
    }
  }

  // isSPOnly(): boolean {
  //   return !!this.betResponseData?.legs.some(item => item.sportsLeg.price.priceTypeRef.id === 'SP');
  // }
  /**
   * Set amount on change
   * @params {object} bet
   * @params {number} amount
   */
  setAmount(bet, amount): void {
    const minStake = 2;
    bet.Bet.stake.perLine = this.changedFromAllStakeField ? this.allStakes.value.replace(",",".") : amount.replace(",",".");

    this.placeStakeErr = null;
    this.emptyStake = false;
    bet.errorMsg = null;
    bet.handicapErrorMsg = null;
    bet.Bet.errorMsg = null;
    bet.Bet.handicapErrorMsg = null;

    if (
      bet.error === BETSLIP_VALUES.ERRORS.PRICE_CHANGED ||
      bet.handicapError === BETSLIP_VALUES.ERRORS.HANDICAP_CHANGED
    ) {
      this.clearSingleBetPriceChangeErr(bet);
    }

    if (bet.Bet.betOffer.offer) {
      bet.Bet.betOffer.isAccaValid = !amount || amount >= minStake;
    }

    // check if to show and then set multiple suspended error
    this.setMultipleSuspendedErrMsg(bet);

    this.betslipService.setAmount(bet);
    this.checkStake(bet);

    if (this.isBoostActive) {
      this.maxStakeExceeded();
    }

    this.detectBetsWithTooLowStake();

    this.priceChangeBets.delete(bet.id);

    this.checkStakeStatus();
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Set price type on change
   * @param event
   * @param index
   */
  setPriceType(event: { output: string, value: string }, index: number): void {
    this.betSlipSingles[index].price.priceType = event.value;
    this.betslipService.setPriceType(this.betSlipSingles[index]);
  }

/**
 * @memberof BetslipComponent
 */
removeAllSuspended(): void {

    const gtmData = {
      event: 'trackEvent',
      eventCategory: 'betslip',
      eventAction: 'click',
      eventLabel: 'remove suspended'
    };
    this.gtmService.push(gtmData.event, [gtmData]);

   const  suspendedSingles: ISingleBet[] = this.betslipService.suspendedIndexFromSelection(this.betSlipSingles);
    this.placeStakeErr = null;
    this.betslipService.removeByOutcomeIds(suspendedSingles);
    _.each(suspendedSingles, suspendedSingle => {
      const index = this.betSlipSingles.indexOf(suspendedSingle);
      this.storageService.set('betId', this.betSlipSingles[index].outcomeId);
      this.betSlipSingles.splice(index, 1)
    });
    this.afterRemoveSelections();
    this.betslipService['_betKeyboardData'] = [];
    this.storageService.remove('betKeyboardData');
  }

/**
 * @memberof BetslipComponent
 */
afterRemoveSelections():void {
    this.init();
    if (this.windowRefService.nativeWindow.view.mobile && !this.betSlipSingles.length && !this.dsBetsCounter) {
      this.pubSubService.publish(this.pubSubService.API['show-slide-out-betslip'], false);
    }
    this.pubSubService.publishSync(this.pubSubService.API.BETSLIP_COUNTER_UPDATE, this.betslipService.count());
    // clear overask message
    this.overAskService.clearStateMessage();
    if (this.betSlipSingles.length < 2) {
      this.clearAllStakesHolder();
    }
    this.quickDeposit.quickDepositFormExpanded = false;
    this.checkOddsBoostStatus();
    this.priceChangeBets.clear();
    this.isSelectionSuspended = false;
    this.onCloseQuickDepositWindow();
  }


  /**
   * Delete one bet from betSlipSingles
   * @param index
   */
  removeFromBetslip(index:number): void {
    let singleBet = this.betSlipSingles[index];
    if(singleBet.Bet.params.lottoData?.isLotto) {
      singleBet = singleBet.Bet.params.lottoData;
    }
    this.placeStakeErr = null;
    this.storageService.set('betId', this.betSlipSingles[index].outcomeId);

    this.betslipService.removeByOutcomeId(singleBet);
    this.betSlipSingles.splice(index, 1);
    this.afterRemoveSelections();

  }
  
  /**
   * Delete betSlipSingles array
   */
  cleanBetslip = (isCloseSlideOut = true, isOveraskCanceled = false) => {
    this.betSlipSingles = [];
    this.betSlipMultiples = [];
    this.accaBets = [];
    this.placeStakeErr = null;
    this.placeSuspendedErr = null;
    this.rebuildBetslip = false;
    this.lottoErrorMsg = null;
    this.horseNames=[];
    this.restrictedRaces=[];
    this.eventIdDetails=[];
    // Don't show "noSelections" message when user REJECT trader's offer
    this.isBetSlipEmpty = isOveraskCanceled;
    this.emptyStake = false;
    this.betslipStorageService.clean();
    this.removeToteBet(true, isOveraskCanceled);

    this.quickDeposit.showQuickDepositForm = false;

    const betslipContentLayout: any = this.windowRefService.document.querySelectorAll('.bs-content');
    if (betslipContentLayout[0]) {
      betslipContentLayout[0].style.paddingBottom = '0px';
    }

    if (this.windowRefService.nativeWindow.vsmobile && this.windowRefService.nativeWindow.vsmobile.instance) {
      const bets = this.windowRefService.nativeWindow.vsmobile.instance.getAllSelectedBets();
      _.each(bets, (bet: any) => {
        this.windowRefService.nativeWindow.vsmobile.instance.deselectBet(bet.selectionKey);
      });
    }

    this.pubSubService.publish(this.pubSubService.API.ODDS_BOOST_CHANGE, false);

    this.pubSubService.publishSync(this.pubSubService.API.BETSLIP_COUNTER_UPDATE, this.betslipService.count());

    if (!this.dsBetsCounter && isCloseSlideOut) {
      this.pubSubService.publish(this.pubSubService.API['show-slide-out-betslip'], false);
    }
    this.storageService.remove('vsbr-selection-map');
    this.storageService.remove('vsm-betmanager-coralvirtuals-en-selections');

    this.storageService.remove('lastMadeBet');
    this.storageService.remove('lastMadeBetSport');

    this.storageService.remove('reuseBetSelections');

    // clear overask message
    this.overAskService.clearStateMessage();
    this.clearAllStakesHolder();

    // remove all live updates for bets in bet slip because they are deleted
    this.betslipLiveUpdateService.clearAllSubs();
    this.quickDeposit.quickDepositFormExpanded = false;

    this.priceChangeBets.clear();
    this.isSelectionSuspended = false;
  }

  removeToteBet(withRefresh: boolean = true, receipt?: boolean) {
    this.toteBetslipService.removeToteBet(withRefresh, receipt);
    this.toteBetGeneralError = null;
    this.toteError = null;
    this.onCloseQuickDepositWindow();
    this.selectedToteFreeBetValue = null;
    this.updatedToteFreeBetValue = null;
    this.toteFreeBetSelected = false;
    this.totalFreeBetsStake();
  }

  openSelectionMultiplesDialog(index, isLuckySignPost, isAcca = false, label:string = ""): void {
    if(this.betReceiptService.isBetSlipShown && isLuckySignPost){
    this.sendGtmDataoninfoicon(label)
    }
    const bet = isAcca ? this.accaBets[index] : this.notAccaBets[index];
    const luckbonus = this.betResponseData.bets.filter(element=>{
      return (element.betTypeRef.id === "L15" || element.betTypeRef.id === "L31" || element.betTypeRef.id === "L63")
    })
    const luckytype = luckbonus[0] && luckbonus[0].availableBonuses && luckbonus[0].availableBonuses.availableBonus;
    this.betInfoDialogService.multiple(bet.type, bet.stakeMultiplier, luckytype, isLuckySignPost,"betslip", label);
  }

  getTime(betslipStake): string {
    return this.betInfoDialogService.isRacing(betslipStake.sportId)
      ? betslipStake.localTime : `${this.datePipe.transform(betslipStake.time, 'h:mm a')},`;
  }

  isBetCheckboxDisabled(): boolean {
    return this.overAskService.hasTraderMadeDecision && this.overAskService.isNoBetsOffered;
  }

  showMultipleRemoveLink(bet): boolean {
    return bet.isTraderDeclined;
  }

  /**
   * Check if entered stake passes through maxAllowed and minAllowed rules.
   *
   * @param {object} bet
   * @return {bool}
   */
  checkStake(bet): boolean {
    let validStake = true;
   if(bet && !bet.isLotto){
    const perLine = Number(bet.stake.perLine);
    const freeBetAndStake = perLine + this.freeBetStake();

    if (freeBetAndStake && freeBetAndStake < bet.stake.min) {
      const minStake = Number(bet.stake.min).toFixed(2);
      bet.errorMsg = this.localeService.getString('bs.minStake', [minStake, this.userService.currencySymbol]);
      validStake = false;
    }
   }
    return validStake;
  }

  /**
   * Check whether price validation rules are passed.
   *
   * - There should be stake placed on at least one bet.
   * - User needs to have enough money to place the bet.
   * - Stakes should be valid
   * - Free bets cannot be used twice.
   *
   * @return {Boolean}
   */
  checkAmount(): boolean {
    const bets = this.betData;
    let hasPrice = true,
      isValidStake = true;
    let isAccaStakeAvailable = false;
    hasPrice = this.betslipService.areBetsWithStakes(bets);

    _.each(bets, (bet: any) => {
      if(bet.isLotto) {
        isAccaStakeAvailable = bet.accaBets.some(acca => acca.stake);
      }
     if (!Number((bet.stake && bet.stake.perLine) || (bet.details && bet.details.stake) || isAccaStakeAvailable) && !bet.disabled && !hasPrice && !bet.selectedFreeBet) {
        this.placeStakeErr = this.localeService.getString('bs.placeBetAlertMessage');
        this.pubSubService.publish(this.pubSubService.API.BS_SHOW_OVERLAY, this.placeStakeErr);
        this.emptyStake = true;
        hasPrice = false;
      } else if (!this.checkStake(bet)) {
        isValidStake = false;
      }
    });

    return hasPrice && isValidStake;
  }

  isMultiplesEachWay(): boolean {
    const isEachWay = _.every(this.betSlipSingles, (bet: any) => {
      return bet.isEachWayAvailable === true;
    });

    return isEachWay;
  }

  templatePlaceBet(): void {
    this.placeStakeErr = null;
    this.eachWayGaTracking = false;
    this.debouncePlaceBets();
  }

  setStake(): void {
      this.toteBetSlip.toteBet.poolBet.stakePerLine = this.toteBetSlip.toteBet.poolBet.stakePerLine.replace(",",".");
  }

  setSingleStake(): void {
    this.allStakes.value = this.allStakes.value.replace(",",".");
  }
  /**
   * BS main bet placement flow
   *
   * @param onQuickDeposit - bet placement performed after quick deposit
   */
  placeBets(onQuickDeposit = false): Observable<IBetsResponse> {
    if (!this.deviceService.isOnline()) {
      this.infoDialogService.openConnectionLostPopup();
      return throwError('Betslip cannot proceed with bet placement: Device is not online');
    }

    // octal number fix, to remove '0' before the entered stake
    if (!!this.toteBetSlip && !!this.toteBetSlip.toteBet && !!this.toteBetSlip.toteBet.poolBet
      && !!this.toteBetSlip.toteBet.poolBet.stakePerLine) {
      this.toteBetSlip.toteBet.poolBet.stakePerLine = +this.toteBetSlip.toteBet.poolBet.stakePerLine;
    }

    this.lottoErrorMsg = null;
    // clear price change errors
    this.clearSingleBetsPriceChangeErr();
    // clear overask message
    this.overAskService.clearStateMessage();

    this.pubSubService.subscribe(this.tagName,
      this.pubSubService.API.SET_BIR_COUNTDOWN_TIMER, time => this.birCountDownTimer(time));

    if (!this.userService.status) {
      const isStake = this.betslipService.areBetsWithStakes(this.betData) || this.toteBetslipService.isToteBetWithProperStake();
      this.callCallbackOpenLoginDialog(isStake);
      return throwError('Betslip cannot proceed with bet placement: Unauthorized access');
    }

    if (this.toteBetCanBePlaced()) {
      this.toteBetGeneralError = null;
      this.toteError = null;
      this.updatePlaceBetsPending(true);
      
      return this.toteBetslipService.placeBet(this.totalStakeWithOutFreeBets()).pipe(
        mergeMap(res => {
          this.toteBetGeneralError = { msg: this.toteBetslipService.toteError };
          this.updatePlaceBetsPending(false);
          if (res.betPlacement) {
            this.hideEmptyBetslip = true;
            this.toteBetReceiptService.id = res.betPlacement[0].betId;
            this.toteBetslipService.setTokenValue(res.betPlacement[0].tokenValue);
            this.scrollTop(0);
            this.pubSubService.publish(this.pubSubService.API.HOME_BETSLIP, this.localeService.getString('app.betslipTabs.toteBetReceipt'));
            this.isBetSlipEmpty = !this.betSlipSingles.length && this.areToteBetsInBetslip();
            if(this.storageService.get('toteFreeBets').filter(toteBets => toteBets.freebetTokenId === this.storageService.get('toteBet').poolBet.freebetTokenId).length > 0) {
              this.storageService.set('toteFreeBets', this.storageService.get('toteFreeBets').filter(x=> x.freebetTokenId !== this.storageService.get('toteBet').poolBet.freebetTokenId));
              const usedTote = this.storageService.get('toteBet').poolBet.freebetTokenId;
              this.usedTotefreebetsList.push(usedTote);
              this.storageService.set('usedToteFreebets', this.usedTotefreebetsList);
            } else if(this.storageService.get('toteBetPacks').filter(betPacks => betPacks.freebetTokenId === this.storageService.get('toteBet').poolBet.freebetTokenId).length > 0) {
              this.storageService.set('toteBetPacks', this.storageService.get('toteBetPacks').filter(x=> x.freebetTokenId !== this.storageService.get('toteBet').poolBet.freebetTokenId));
            }
            this.toteBetslipService.setToteFreeBetText(this.storageService.get('toteBet').poolBet.betType ? this.storageService.get('toteBet').poolBet.betType : undefined)
            this.selectedToteFreeBetValue = null;
            this.totalFreeBetsStake();
            this.availableToteFreeBets = this.storageService.get('toteFreeBets');
            this.availableToteBetPacks = this.storageService.get('toteBetPacks');
            const toteBetStorage = this.storageService.get('toteBet');
            if (toteBetStorage && toteBetStorage.poolBet && toteBetStorage.poolBet.freebetTokenId) {
              this.freeBetsData = this.freeBetsStoreUpdate([], this.storageService.get('toteBet').poolBet.freebetTokenId);
              if (this.isFreeBetApplied) {
                this.freeBetsService.store(this.userService.username, { data: this.freeBetsData });
              }
            }
          } else {
            this.toteError = res && res.betError ? null : this.localeService.getString(`bs.BET_NOT_FOUND`);
          }
          return of(null);
        }),
        catchError(err => {
          this.updatePlaceBetsPending(false);
          this.awsService.addAction('betSlipComponent=>totePlaceBetRequest=>Error', { err });

          return throwError(err);
        })
      );
    } else if (this.checkAmount()) {               // ToDo: fix inconsistency in return point, no default return value.
      this.clearUserValueForDisabledBets();

      this.updatePlaceBetsPending(true);
      this.quickDeposit.quickDepositPending = true;

      // rebuild betslip in case when user press "accep & place bet" instead of "re-boost"
      if (this.rebuildBetslip && this.isBoostActive && this.showPriceChangeNotification()) {
        this.init();
        return of(null);
      }
      const lottoObj = this.isLottoBet(this.lottobetslipData) ? {
        isLotto: this.lottobetslipData && this.lottobetslipData.length && this.isLottoBet(this.lottobetslipData),
        lottoData : [...this.lottobetslipData]
      } : null;

      return this.betslipService.placeBets(lottoObj).pipe(
        delayWhen((result) => {
          
          if (result.errs && result.errs.length > 0) {
            return interval(this.BPP_TIMEOUT_ERROR);
          }
          return of(result);
        }),
        map(result => {
          this.quickDeposit.quickDepositPending = false;
          this.quickDeposit = this.defaultQuickDepositData;
          // Set flag to true after place bet to execute initQuickDeposit
          // when oncoming bets will be added to empty betslip next time(as quick deposit resets to default after place bet)
          this.firstRunOfBetSlip = true;

          this.placeBetsResponseProcess(result, onQuickDeposit);
          result.errs && result.errs.length === 0 && this.clearAllStakesHolder();
          this.awsService.addAction('betSlipComponent=>placeBetResponse=>Success', { result });
          this.pubSubService.publish('PRIVATE_MARKETS_TAB');
          if(lottoObj && lottoObj.isLotto) {
          this.pubSubService.publish('LOTTO_BET_PLACED');
          this.getLottoMessage(result);
          }
          this.freeBetsData = this.freeBetsStoreUpdate(result.bets || []);
          if (this.isFreeBetApplied) {
            this.freeBetsService.store(this.userService.username, { data: this.freeBetsData });
          }
          return result;
        }),
        catchError(err => {
          this.quickDeposit.quickDepositPending = false;

          this.handleError(err);

          this.updatePlaceBetsPending(false);
          this.scrollTop(0);
          this.awsService.addAction('betSlipComponent=>placeBetResponse=>Error', { err });
          return throwError(err);
        })
      );
    } else {
      this.quickDeposit.quickDepositPending = false;
      this.updatePlaceBetsPending(false);
      return throwError('Betslip cannot proceed with bet placement');
    }
  }

  getLottoMessage(result) {
    if(result.errs && result.errs.length) {
      this.lottoErrorMsg = result.errs[0];
    }
  }
  afterLoginHandler(): void {
    this.betslipSuccessfulLogin('betslip');
  }

  getStakeOptions(price) {
    return this.getDefaultStakeOptions().map(item => {
      if (item.name === 'LP') {
        item.value = this.odds(price);
      }
      return item;
    });
  }

  /**
   * Checks if the bet is for ACCA
   * @param bet
   * @return {boolean|Number}
   */
  isACCABetslip(bet): boolean {
    return this.isBetForACCA(bet);
  }

  /**
   * Checks and toggle only one stake per time
   * @param bet
   */
  toggle(bet): void {
    bet.expanded = !bet.expanded;

    if (!bet.expanded) {
      return;
    }

    _.each(this.betSlipSingles, (value: any) => {
      if (value !== bet) {
        value.expanded = false;
      }
    });
  }

  trackByIndex(index): number {
    return index;
  }

  /**
   * Check price data and get price-change message
   *
   * @param betslipStake
   */
  getPriceChangeMessage(betslipStake: IBetInfo): string {
    const oldPrice = this.getOldPrice(betslipStake);
    if (!oldPrice || betslipStake.price.priceType === 'SP') { return ''; }

    const oldOdds = this.odds({ price: oldPrice });
    const currOdds = this.odds(betslipStake);
    if (oldOdds === currOdds) { return ''; }

    return this.localeService.getString('bs.stakePriceChangeMsg', [oldOdds, currOdds]);
  }

  /**
   * Check if use auto scroll to specific kind of notification
   * @params {String} error
   * @return {Boolean}
   */
  autoScrollOff(error): boolean {
    return error === BETSLIP_VALUES.ERRORS.PRICE_CHANGED || this.betslipService.isSuspended(error);
  }

  /**
   * on DidigitKeyboardInput initialized
   */
  onDidigitKeyboardInit(): void {
    this.isDidigitKeyboardInit = true;
  }

  /**
   * Sets value to all single stake fields
   */
  setStakes(): void {
    if (this.deviceService.isMobileOnly && !this.isDidigitKeyboardInit) {
      return;
    }
    const allStakesAmount = this.allStakes.value && this.allStakes.value.match(/^[0]+[.]*[0]*$/) ? '' : this.allStakes.value;
    this.changedFromAllStakeField = true;

    this.storageService.set('all-stakes', allStakesAmount);
    this.betSlipSingles.forEach(betslipStake => {
      if (!betslipStake.disabled) {
        this.setAmount(betslipStake, allStakesAmount);
      }
    });
  }
  getAllSingleStakeOutcomeIds(){
    return this.betSlipSingles?.map(singleStake=>singleStake.outcomeId).join(',')
  }
  isPlaceButtonShown(): boolean {
    return (
      !this.placeBetsPending &&
      !this.overAskService.isInProcess &&
      !this.quickDeposit.quickDepositPending
    );
  }

  isUpgradeVisible(): boolean {
    // TODO: change string to 'retail' when login is implemented;
    // TODO: add condition for upgraded user when retail auth is implemented
    return this.userService.isInShopUser();
  }

  getRemovedLineSymbol(value: string): string {
    return this.filterService.removeLineSymbol(value);
  }

  getErrorMsgLocale(betslipStake): string {
    return betslipStake && this.localeService.getString(`bs.${betslipStake.error}`);
  }

  getTypeLocale(betslipStake): string {
    return betslipStake && this.localeService.getString(`bs.${betslipStake.type}`);
  }

  SSDSType(type: string): boolean {
    return type && (type.indexOf('SS') > -1 || type.indexOf('DS') > -1);
  }

  getOldPrice(betslipStake) {
    return betslipStake.Bet?.legs[0]?.parts[0]?.outcome?.oldModifiedPrice || '';
  }

  getStakeOddClass(betslipStake) {
    return {
      'offered': betslipStake.traderChangedOdds || betslipStake.traderChangedPriceType,
      'boosted': this.isStakeBoostAvailable(betslipStake)
    };
  }

  getFooterWarningMsg(): string {
    return (this.placeSuspendedErr && this.placeSuspendedErr.msg) || this.toteBetslipService.toteSuspensionError;
  }

  getStakeId(prefix: string, id: string): string {
    return `${prefix}-${id}`;
  }

  isStakeBoostAvailable(betslipStake: IBetInfo): boolean {
    const available = (
      this.userService.status &&
      this.isBoostEnabled &&
      this.isBoostActive &&
      !betslipStake.disabled &&
      !!betslipStake.Bet.oddsBoost &&
      !betslipStake.isSP
    );
    if (betslipStake.isSPLP) {
      return (
        available &&
        betslipStake.price.priceType !== 'SP' &&
        betslipStake.pricesAvailable
      );
    }
    return available;
  }

   /**
   * Returns true if selection odds can be boosted
   * @param betslipStake {IBetInfo}
   * @returns {boolean}
   */
  canBoostSelection(betslipStake: IBetInfo): boolean {
    const  available = (
      this.userService.status &&
      this.isBoostEnabled &&
      !betslipStake.disabled &&
      !!betslipStake.Bet.oddsBoost &&
      !betslipStake.isSP
    );
    if (betslipStake.isSPLP) {
      return (
        available &&
        betslipStake.price.priceType !== 'SP' &&
        betslipStake.pricesAvailable
      );
    }

    return available;
  }

  getBoostedOldPrice(betslipStake: IBetInfo, type: string): IBetPrice {
    return this.commandService.execute(this.commandService.API.ODDS_BOOST_OLD_PRICE, [betslipStake, type]);
  }

  getBoostedNewPrice(betslipStake: IBetInfo, type: string): IBetPrice {
    return this.commandService.execute(this.commandService.API.ODDS_BOOST_NEW_PRICE, [betslipStake, type]);
  }

  acceptOffer() {
    this.overask.acceptOffer();
  }

  /**
   * Show confirmation popup for "reject traders offer" action
   */
  rejectOffer(): void {
    this.infoDialogService.openInfoDialog(
      this.localeService.getString('bs.overaskElements.confirmCancelDialogTitle'),
      this.localeService.getString('bs.overaskElements.confirmCancelDialogMessage'),
      'bs-overask-dialog',
      undefined,
      undefined,
      [{
        cssClass: 'btn-style4',
        caption: this.localeService.getString('bs.overaskElements.cancelCancelTradersOffer')
      }, {
        caption: this.localeService.getString('bs.overaskElements.confirmCancelTradersOffer'),
        cssClass: 'btn-style2',
        handler: () => {
          this.betslipService.closeNativeBetslipAndWaitAnimation(() => {
            this.overask.rejectOffer(false).subscribe();
            this.infoDialogService.closePopUp();
          });
        }
      }]
    );
  }

  showBetNowBtn(): boolean {
    const isOveraskInProcess = this.overask.isInProcess;
    const qDeposit = this.quickDeposit;
    const isDepositPending = qDeposit.quickDepositPending && !qDeposit.quickDepositFormExpanded;
    const isAnyDepositFormActive =
      !!this.totalStakeAmount && !qDeposit.quickDepositFormExpanded
      || !qDeposit.showQuickDepositForm
      || !qDeposit.quickDepositFormAllowed;

    return !isOveraskInProcess
      && !this.quickDepositIFrameFormExpanded
      && (!this.allowQuickDeposit() && isAnyDepositFormActive || isDepositPending)
      && !this.isIFrameLoadingInProgress()
      && (!this.isZeroBalanceWithExistingBets || !!Number(this.totalFreeBetsStake()));
  }

  disableBetNowBtn(): boolean {
    return this.toteBetSuspendedError || !this.totalStakeIsPresent || this.placeBetsPending ||
      this.quickDeposit.quickDepositPending || this.loginAndPlaceBets || this.noActiveSelections ||
      this.overask.isOnTradersReview || this.multiplesShouldBeRebuilded || this.totalStakeAmount === '0.00' ||
      this.hasBetsWithTooLowStake || this.serviceClosureService.userServiceClosureOrPlayBreak;
  }

  /**
   * Check if showQuickDepositBtn should be disabled
   * (ignore placeBetsPending and quickDepositPending for overask phase 2)
   * TODO: refactor during BMA-46323
   */
  isShowQuickDepositBtnDisabled(): boolean {
    return this.overask.isOnTradersReview ||
      !this.overask.userHasChoice && (this.placeBetsPending || this.quickDeposit.quickDepositPending);
  }

  restoreOveraskProcess() {
    if (this.overask.isInProcess && this.overask.isOnTradersReview) {
      this.getOveraskDrawerConfig();
    }
  }

  isRacingOrVirtual(betslipStake): boolean {
    return betslipStake.isRacingSport || betslipStake.sport === 'Virtual Sports' || betslipStake.sportId === '39';
  }

  getEventTime(betslipStake): string {
    if (betslipStake.isRacingSport) {
      return `${betslipStake.localTime} `;
    } else {
      return `${this.timeService.formatByPattern(betslipStake.time, 'HH:mm')} `;
    }
  }

  onQuickStakeSelect(value: string): void {
    this.pubSubService.publish(this.pubSubService.API.QB_QUICKSTAKE_PRESSED, [value]);
  }

  onKeyboardToggle(status: boolean): void {
    this.quickStakeVisible = status;
  }

  isFreebetButtonShown(stake: IBetslipBetData): boolean {
    return BetslipBetDataUtils.areFreeBetsAvailable(stake) && !(this.overask.isInProcess && !this.overask.isNoBetsOffered);
  }

  hideFreeBetNotification(): void {
    this.hideAvailableFreeBetsMessage = true;
    this.storageService.set(`hideAvailableFreeBetsMessage-${this.userService.username}`, true);
  }

  /**
   * Remove bet from offer list (make disable)
   *
   * @param id
   */
  removeFromOffer(id: string) {
    this.calculateIsBetsSelected();
    this.overask.collectDeletedBetID(id);
  }

  /**
   * Undo remove bet from offer list (make active)
   *
   * @param bet
   */
  undoOveraskBetRemove(bet: any): void {
    bet.isSelected = true;
    this.calculateIsBetsSelected();
    this.overask.removeDeletedBetID(bet.id);
  }

  onOpenIframe(): void {
    this.showIFrame = true;
    this.iframeLoadingInProgress = this.isIFrameLoadingInProgress();
    this.pubSubService.publish(this.pubSubService.API.TOGGLE_QUICK_DEPOSIT_IFRAME, true);
  }

  /**
   * checks if quick deposit should be opened after stake change
   * or updating number of selections in betslip
   */
  handleBetslipUpdate(): void {
    if (!this.isAmountNeeded() && (this.showIFrame || this.iframeLoadingInProgress)) {
      this.onCloseQuickDepositWindow();
    }
  }

  /**
   * checks if needed amount error message should be shown
   */
  isAmountNeeded(): boolean {
    return Number(this.quickDeposit.neededAmountForPlaceBet) > 0;
  }

  /**
   * returns error message for needed amount property
   */
  getErrorMsg(): string {
    const arg = this.userService.currencySymbol + this.userService.getUserDepositNeededAmount(
      this.quickDeposit.neededAmountForPlaceBet, true
    );
    return `${this.localeService.getString('bs.betslipDepositNotification', [arg])}`;
  }

  /**
   * closes quick deposit window
   */
  onCloseQuickDepositWindow(fromDigitShown = false): void {
    this.estimatedReturnAfterPriceChange = undefined;
    this.showIFrame = false;
    this.quickDepositIFrameFormExpanded = false;
    this.iframeLoadingInProgress = this.isIFrameLoadingInProgress();
    this.pubSubService.publish(this.pubSubService.API.TOGGLE_QUICK_DEPOSIT_IFRAME, false);
    if (!fromDigitShown && !this.sessionStorageService.get('buttonText') && !this.sessionStorageService.get('betPlaced')) {
      const betsPlaced = this.storageService.get("betSelections");
      const stepSelection = betsPlaced && betsPlaced.length ? 'addSelection' : 'pickYourBet';

      this.pubSubService.publish(this.pubSubService.API.FIRST_BET_PLACEMENT_TUTORIAL,
        { step: stepSelection, tutorialEnabled: true, type: 'defaultContent' });
    }
  }

  /**
   * sends event with modified object (an object with an addition action)
   * @param isStake if true has any stakes
   */
  callCallbackOpenLoginDialog(isStake: boolean): void {
    this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, {
      placeBet: isStake ? 'betslip' : false,
      moduleName: 'betslip',
      action: this.afterLoginHandler
    });
  }

  allowQuickDeposit(): boolean {
    const isLessStakeCurrBal = this.currentStakeWithoutDisabledBets <= Number(this.userService.sportBalance);
    return this.isToteBets ? false :
      this.userService.status && isLessStakeCurrBal === false;
  }

  // TODO slice and reuse isShowQuickDepositBtnShown Fn from core
  isShowQuickDepositBtnShown(): boolean {
    return (!this.overask.isInProcess
      && this.quickDeposit.showQuickDepositForm
      && !this.placeBetsPending
      && this.quickDeposit.quickDepositFormAllowed
      && this.totalStake() !== '0.00'
      && this.allowQuickDeposit())
      || this.quickDepositIFrameFormExpanded
      || this.isZeroBalanceWithExistingBets && !Number(this.totalFreeBetsStake());
  }

  /**
   * closes iframe after successful deposit and automatically places bet
   */
  closeIFrame(): void {
    this.onCloseQuickDepositWindow();
    this.templatePlaceBet();
  }

  /**
   * check if show suspended message
   */
  isShowSuspendedNotification(): boolean {
    return (this.placeSuspendedErr.msg && this.overask.isNotInProcess) || this.toteBetSuspendedError;
  }

  /**
   * check if in-shop/online user and navigate to upgrade to MC
   */
  navigateToUpgrade(): void {
    const gtmData = {
      event: 'trackEvent',
      eventCategory: 'cta',
      eventAction: 'upgrade account',
      eventLabel: 'yes - upgrade Account'
    };
    this.pubSubService.publish(this.pubSubService.API.UPGRADE_FROM_BETSLIP);

    this.gtmService.push(gtmData.event, gtmData);

    this.windowRefService.nativeWindow.location.href = this.userService.isInShopUser()
      ? this.accountUpgradeLinkService.inShopToMultiChannelLink
      : this.accountUpgradeLinkService.onlineToMultiChannelLink;
  }

  loadQuickDepositIFrame(): void {
    this.isZeroBalanceWithExistingBets = false;
    this.quickDepositIFrameFormExpanded = true;
    this.iframeLoadingInProgress = this.isIFrameLoadingInProgress();
  }

  onQuickDepositEvents({ output }): void {
    switch (output) {
      case 'openIframeEmit':
        this.onOpenIframe();
        break;
      case 'quickDepositStakeChange':
        this.handleBetslipUpdate();
        break;
      case 'closeWindow':
        this.onCloseQuickDepositWindow();
        break;
      case 'closeIframeEmit':
        this.closeIFrame();
        break;
      default:
        break;
    }
  }

  /*
  catches the emitted stake input details from lotto betslip
  **/
  onstakeInputChangeEvents( event: ILazyComponentOutput){
    if(event.output == 'removeErrorMsg') {
      this.lottoErrorMsg = null;
    } else if (event.output == 'removeFrombetList') {
      this.lottoErrorMsg = null;
      this.removeFromBetslip(event.value);
    } else if(event.output === 'lottoBetsEmitter') { 
      this.updateBetSlipHeight(event.value);
    } else if (event.value.lottoData) {
      this.betData = event.value.lottoData;
      this.checkStakeStatus();
    }
  }

  /**
   * checks if iframe loading is in progress
   */
  isIFrameLoadingInProgress(): boolean {
    return !this.showIFrame && this.quickDepositIFrameFormExpanded;
  }

  /**
   * Handle quick deposit state(amount needed message and isQuickDeposit panel is onened - needed for ladbrokes brand)
   */
  protected handleQuickDepositState(): void {
    this.amountNeededErrorMessage = this.userService.getUserDepositMessage(this.quickDeposit.neededAmountForPlaceBet, true);
  }

  /**
   * Clear overlay message(needed for ladbrokes brand)
   */
  protected clearOverlayMessage(type?: string): void { }

  protected selectionLiveUpdate(bet: Bet): void {
    if (
      bet.history.isPriceChanged() ||
      bet.history.isPriceChangedAndMarketUnsuspended()
    ) {
      const info = bet.info();
      this.priceChangeBets.add(info.id);
      this.priceChangeBannerMsg = this.localeService.getString(
        this.reboost ? 'bs.reboostPriceChangeBannerMsg' : 'bs.priceChangeBannerMsg'
      );
    }
  }

  protected handleDefaultError(result: IBetsResponse): boolean {
    const KEY_NOT_FOUND = 'KEY_NOT_FOUND',
      errors = _.groupBy(result.errs, (err: any) => err.outcomeRef && err.outcomeRef.id),
      error = result.errs[0].subCode ? result.errs[0].subCode : result.errs[0].code,
      outcomeError = this.outcomesErrorParser(errors, result.bets, result.legs),
      noCodeError = this.localeService.getString(`bs.${result.errs[0].errorDesc}`);
    let errorMessage = '';

    if (error && error !== BETSLIP_VALUES.ERRORS.PRICE_CHANGED && !outcomeError) {
      errorMessage = this.localeService.getString(`bs.${error}`);
    } else if (!error && noCodeError !== KEY_NOT_FOUND) {
      errorMessage = noCodeError;
    }

    if (this.isBoostActive && error === BETSLIP_VALUES.ERRORS.BAD_FREEBET_TOKEN) {
      errorMessage = this.localeService.getString('bs.oddsBoostExpiredOrRedeemed');
    }

    if (errorMessage === KEY_NOT_FOUND) {
      this.awsService.addAction('betSlipComponent=>placeBetResponse=>undefined_errors', {
        response: JSON.stringify(result),
        errors: JSON.stringify(errors),
        errorCode: error || noCodeError
      });
      this.placeStakeErr = this.localeService.getString('bs.DEFAULT_PLACEBET_ERROR');
    } else if (errorMessage) {
      this.placeStakeErr = errorMessage;
    }

    if (this.betslipService.isBetNotPermittedError(result)) {
      this.placeStakeErr = this.betslipService.getBetNotPermittedError();
    }

    this.updatePlaceBetsPending(false);
    return outcomeError;
  }

  /**
   * Returns object with params ready for acca notification message
   * @param multipleBet
   * @private {*}
   */
  protected getFirstMultipleInfoForAccaNotification(multipleBet: Partial<IBetInfo>): IFirstMultipleInfo {
    const isValidMultiple = multipleBet && multipleBet.stakeMultiplier === 1;

    if (isValidMultiple) {
      this.oddsACCA(multipleBet); // only called to update payout after LS TODO: how it worked before?
      const stake = !multipleBet.stake.perLine || this.overask.hasCustomerActionTimeExpired ? 0 : multipleBet.stake.perLine;
      return {
        translatedType: multipleBet.type,
        potentialPayout: multipleBet.potentialPayout,
        stake
      };
    } else {
      return {};
    }
  }

  private loadQuickDepositIfEnabled(): void {
    this.quickDepositEnabledSub = this.quickDepositIframeService.isEnabled().subscribe((isEnabled: boolean) => {
      if (isEnabled) {
        this.loadQuickDepositIFrame();
      }
    });
  }
 private haveFBandBT( allBets:IBetInfo[],tokenType:number):boolean{
  return allBets.some((bet: IBetInfo) => !!bet.Bet.freeBets && bet.Bet.freeBets.length > 0 && this.checkForFreebetsAndBetTokens(bet.Bet.freeBets, tokenType));
 }

  private checkForAvailableFreebets(): void {
    const allBets = this.getAllBets() || [];
    if (allBets.length) {
      this.freeBetAvailable = this.haveFBandBT(allBets, FreeBetType.FREEBET);
      this.betTokensAvailable = this.haveFBandBT(allBets, FreeBetType.BETPACK);
      this.fanZoneAvailable = this.haveFBandBT(allBets, FreeBetType.FANZONE);
      this.hideAvailableFreeBetsMessage = this.storageService.get(`hideAvailableFreeBetsMessage-${this.userService.username}`);
    } else {
      const freebetData=this.freeBetsService.getFreeBetsData();
      this.freeBetAvailable = this.checkForFreebetsAndBetTokens(freebetData, FreeBetType.FREEBET);
      this.betTokensAvailable = this.checkForFreebetsAndBetTokens(freebetData, FreeBetType.BETPACK);
      this.fanZoneAvailable = this.checkForFreebetsAndBetTokens(freebetData, FreeBetType.FANZONE);
      this.hideAvailableFreeBetsMessage = false;
      this.storageService.remove(`hideAvailableFreeBetsMessage-${this.userService.username}`);
    }
  }

  /**
   *
   * @param freeBets {FreeBet[] | IFreebetToken[]}
   */
  private checkForFreebetsAndBetTokens(freeBets: any, freebetType: number) {
    const freebetdata = !!freeBets && freeBets.length ;
    if (freebetType == FreeBetType.FREEBET) {
      return freebetdata> 0 && freeBets.some((freebet) =>
       (!freebet.freebetOfferCategories ||
        (!this.freeBetsService.isBetPack(freebet && freebet.freebetOfferCategories && freebet.freebetOfferCategories.freebetOfferCategory) 
        && !this.freeBetsService.isFanzone(freebet && freebet.freebetOfferCategories && freebet.freebetOfferCategories.freebetOfferCategory)
        )));
    }
    if (freebetType == FreeBetType.FANZONE) {
      return freebetdata > 0 && freeBets.some((freebet) => this.freeBetsService.isFanzone(freebet.freebetOfferCategories?.freebetOfferCategory));
    } 
      return freebetdata > 0 && freeBets.some((freebet) => this.freeBetsService.isBetPack(freebet.freebetOfferCategories?.freebetOfferCategory));
  }

  private isPriceOrHcapUpdate(): boolean {
    return this.betSlipSingles && this.betSlipSingles.some((bet: IBetInfo) => {
      return bet.error === BETSLIP_VALUES.ERRORS.PRICE_CHANGED
        || bet.handicapError === BETSLIP_VALUES.ERRORS.HANDICAP_CHANGED;
    });
  }

  /**
   * Check if some of selections has price changed(checked by price not by error code)
   */
  private isPriceUpdate(): boolean {
    return this.betSlipSingles && this.betSlipSingles.some((bet: IBetInfo) => {
      return !!(!bet.disabled && this.getPriceChangeMessage(bet));
    });
  }

  private handleOverAskProcessing(): void {
    this.getOveraskDrawerConfig();
  }

  private getOveraskDrawerConfig(): void {
    if (!this.overaskDrawerIsConfigured) {
      this.cmsService.getFeatureConfig('Overask')
        .subscribe(config => {
          this.overaskProcessingTitle = config.title;
          this.overaskProcessingTopMessage = config.topMessage;
          this.overaskProcessingBottomMessage = config.bottomMessage;
          this.overaskDrawerIsConfigured = true;
        }, (error) => {
          console.error('Overask drawer can not be shown', error);
        });
    }
  }

  private isFreeBetSelected() {
    return this.betSlipSingles.some(betSingle => {
      return betSingle.selectedFreeBet;
    }) && this.betSlipMultiples.some(betMultiple => {
      return betMultiple.selectedFreeBet;
    });
  }

  private unsetFreeBets(bets): void {
    bets.forEach(bet => {
      bet.selectedFreeBet = null;
      this.setFreebet(bet);
    });
  }

  /**
   * Update placeBetsPending value
   * @param  {Boolean} value
   */
  private updatePlaceBetsPending(value: boolean): void {
    this.placeBetsPending = value;
    this.betslipService.setPlaceBetPending(value);
  }

  // //////////////////////////////////////////////////////////////////
  // //////////////////////////// Tote Betslip ////////////////////////
  // //////////////////////////////////////////////////////////////////

  private areRegularBetsInBetslip(): boolean {
    return this.betslipDataService.containsRegularBets();
  }

  private noActiveToteBets(): boolean {
    return !this.toteBetslipService.isToteBetPresent();
  }

  private toteBetCanBePlaced(): boolean {
    let canPlaceToteBets = false;
    if(this.toteBetslipService.isToteBetWithProperStake()) {
      canPlaceToteBets = true;
    } else if(!this.toteBetslipService.isToteBetWithProperStake() && !this.toteFreeBetSelected) {
      canPlaceToteBets = false;
    } else if(!this.toteBetslipService.isToteBetWithProperStake() && this.toteFreeBetSelected) {
      canPlaceToteBets = true;
    }
    return !this.noActiveToteBets() && canPlaceToteBets;
  }

  private handleSuspensionOnDeposit(): void {
    this.isSelectionSuspended = true;
  }

  // //////////////////////////////////////////////////////////////////
  // //////////////////////////// Betslip /////////////////////////////
  // //////////////////////////////////////////////////////////////////

  /**
   * Init bet slip data
   * (process if first attempt or load is completed/failed)
   *
   * @param {object} initialData
   * @param {boolean} preventSystemCache - not use cache for get system request
   * @param {Object} overaskData - data ready to execute overask on demand
   */
  private init(initialData?, preventSystemCache?: boolean, overaskData?): void {
    this.loadComplete = false;
    this.loadFailed = false;
    this.currencySymbol = this.userService.currencySymbol;
    const data = initialData;
    const betIds = this.storageService.get('betIds');
    this.lockBodyScrollAfterReinit();

    if (this.storageService.get('betId')) {
      this.betId = this.storageService.get('betId');
    }

    if (this.allStakes && this.allStakes.value && this.betSlipSingles.length < 2) {
      this.clearAllStakesHolder();
    }

    this.placeBetsPending = this.betslipService.getPlaceBetPending || this.toteBetslipService.isPlaceBetPending;
    this.isBetSlipEmpty = !data && !this.areToteBetsInBetslip();

    if (!data) {
      if (this.fetchSubscription && !this.fetchSubscription.closed) {
        this.fetchSubscription.unsubscribe();
        this.fetchSubscription = null;
        this.loadComplete = false;
      }
      const fetch$ = this.betslipService.fetch(preventSystemCache).pipe(
        map(bsData => {
          if(this.isLottoBet(bsData)) {
            return bsData;
          }
          return this.betslipLiveUpdateService.subscribe(bsData);
        }),
        map(bsData => {
          this.fetchedData = bsData;
          this.core(bsData, overaskData);
        }),
        catchError(error => {
          if (error.message === 'no events') {
            this.loadComplete = true;
            this.cleanBetslip();
          } else {
            this.loadFailed = true;
            const isOnline = this.windowRefService.nativeWindow.navigator.onLine
            this.awsService.addAction('betslip=>UI_Message=>Unavailable=>init', error);
            this.awsService.addAction('betslip=>IsOnline', isOnline);
            return of(null);
          }

          return of(null);
        }),
        finalize(() => {
          // update array of betsingles with competition from betSelections
          this.updateBetSingles();

          if (!this.betSlipInitDone) {
            const betsCount = this.betslipService.count(),
              selections = this.betslipService.getSelections;

            this.betSlipInitDone = true;
            this.betslipService.betSlipReady.next({
              betsCount,
              selections
            });
            this.betslipService.betSlipReady.complete();
            this.pubSubService.publish(this.pubSubService.API.BETSLIP_COUNTER_UPDATE, betsCount);
          }

          if (this.betId) {
            // remove from localStorage
            this.storageService.remove('betId');
          }

          if (betIds) {
            this.storageService.remove('betIds');
          }

          this.loadComplete = true;
          this.changeDetectorRef.detectChanges();

          if (this.rebuildBetslip && this.placeBetsPending && overaskData === undefined) {
            this.rebuildBetslip = false;
            this.placeBets().subscribe();
            this.awsService.addAction('betSlipComponent=>placeBetRequest=>RE_BOOST_PLACE_BET');
          }

          this.checkForAvailableFreebets();
          if (this.deviceService.isDesktop) {
            this.onShowQuickDepositWindow();
          }
          this.isAlreadyReloaded = false;
        })
      );

      this.fetchSubscription = fetch$.subscribe();

      this.priceChangeBets.clear();
    } else { // update via LS
      this.isAlreadyReloaded = false;
      this.loadComplete = true;
      this.isBetSlipEmpty = !this.areToteBetsInBetslip();
      this.fetchedData = data;
      this.core(data);

      if (this.placeSuspendedErr && this.placeSuspendedErr.msg) {
        this.handleSuspensionOnDeposit();
      } else {
        this.isSelectionSuspended = false;
      }
    }

    /**
     * All Stakes
     */
    this.allStakes = { value: '' };
    const allStakesValue = <string>this.storageService.get('all-stakes');
    if (allStakesValue) {
      this.allStakes.value = allStakesValue;
    }

    // clearOverlayMessage - will be overwritten for ladbrokes
    this.clearOverlayMessage('ACCA');
  }

  isLottoBet(betslipData): boolean {
    if(Array.isArray(betslipData)) {
      betslipData = betslipData[0];
    }
    return betslipData && (betslipData.isLotto || betslipData.params?.lottoData?.isLotto);
  }

  private core(data, overaskData?): void {
    this.betData = data.map(bet => {
      if (bet.params?.lottoData?.isLotto) {
        return bet.info();
       }
      // update bet if handicap value was changed(remove this code when live handicap update will be implemented in sb module)
      const outcome = bet.legs[0].parts[0].outcome;
      const shouldHandicapBeUpdated = outcome.prices && outcome.prices[0] && outcome.prices[0].handicapValueDec;

      if (shouldHandicapBeUpdated) {
        const handicap = outcome.prices[0].handicapValueDec.replace(/,/g, '');
        bet.updateHandicap(bet.legs[0], outcome, bet, handicap);
      }

      return bet.info(); // eslint-disable-line no-useless-call
    });
    this.betslipService.betData = this.betData;
    // find all the groups of bets
    const groupedBets = _.groupBy(this.betData, (bet: any) => {
      return bet.type;
    });
    // find duplicated multiples selection, set EW est returns to the win selection and delete EW selection
    _.each(groupedBets, (bets, type) => {
      if (type !== 'SGL' && bets.length > 1) {
        // remove each way bet, because bets[0] is exactly the same, but it is formed from the EW parts
        this.betData = _.without(this.betData, bets[1]);
      }
    });

    // Handles freeBets when chosen freeBet on quickBet is not available anymore in buildBet request
    if (overaskData && overaskData.bets[0].freebet) {
      const freeBet = <IFreeBet>this.freeBetsService.getFreeBetInBetSlipFormat(overaskData.bets[0].freebet[0].id);

      if (freeBet) {
        this.betData[0].Bet.freeBets.push(this.betslipService.constructFreeBet(freeBet));
      }
    }

    this.betslipStorageService.restoreUserStakeData(this.betData);
      if (!this.isLottoBet(this.betData.map(bet => bet.Bet))) {
      this.overAskService.setBetsData(this.betData); // set betData model to overask
    }

    this.betSlipSingles = _.filter(this.betData, (bet: any) => {
      return bet.outcomeId || bet.combiName === 'SCORECAST' || bet.isFCTC || this.isLottoBet(bet.Bet);
    });

    this.lottobetslipData = this.betSlipSingles.filter(res => res.Bet.params.lottoData)
                                                .map(res =>res.Bet.params.lottoData);

    this.betSlipMultiples = _.reject(this.betData, (bet: any) => {
      return bet.type === 'SGL';
    });

    this.betSlipMultiples = this.bsFiltersService.multiplesSort(this.betSlipMultiples, this.betSlipSingles.length);

    this.accaNotificationChanged();

    // Show declined bets on top
    this.betSlipSingles = this.overAskService.sortDeclinedBetsOnTop(this.betSlipSingles);
    this.betSlipMultiples = this.overAskService.sortDeclinedBetsOnTop(this.betSlipMultiples);

    // Show child linked bet after parent
    this.betSlipSingles = this.overAskService.sortLinkedBets(this.betSlipSingles);
    this.betSlipMultiples = this.overAskService.sortLinkedBets(this.betSlipMultiples);

    // clear price change error if suspended outcomes is present
    if (this.suspendedOutcomesCounter) {
      this.clearSingleBetsPriceChangeErr();
    }

    if (this.isBoostEnabled) {
      this.subscribeToOddsBoostChange();
    }

    this.checkStakeStatus();

    this.accaBets = _.filter(this.betSlipMultiples, (bet) => this.isACCABetslip(bet));
    this.notAccaBets = _.filter(this.betSlipMultiples, (bet) => !this.isACCABetslip(bet));

    this.placeSuspendedErr = this.betslipService.showSuspendedOutcomeErr(this.betSlipSingles, this.betSlipMultiples);
    this.suspendedOutcomesCounter = this.betslipService.countSuspendedOutcomes(this.betSlipSingles);
    this.multiplesShouldBeRebuilded = this.placeSuspendedErr.disableBet && (this.suspendedOutcomesCounter > 0);
    this.noActiveSelections = this.noActiveSelectionsAction() && this.noActiveToteBets();

    this.calculateIsBetsSelected();

    // to show correct count in multiples section header
    this.multiplesSectionCount = `(${this.betSlipMultiples.length})`;

    if (overaskData) {
      this.updatePlaceBetsPending(true);
      this.quickDeposit.quickDepositPending = true;
      this.betslipService.exucuteOverask(overaskData).subscribe((result: IRespTransGetBetsPlaced) => {
        this.quickDeposit.quickDepositPending = false;
        this.placeBetsResponseProcess(result);
        this.clearAllStakesHolder();
      }, err => {
        this.quickDeposit.quickDepositPending = false;

        this.handleError(err);

        this.updatePlaceBetsPending(false);
        this.scrollTop(0);
      });
    }

    _.each(this.betData, (betslipItem: IBetslipBetData) => {
      betslipItem.selectedFreeBet = betslipItem.selectedFreeBet || null;
    });

    if (!this.isLottoBet(this.betData.map(res=>res.Bet))) {
      this.betslipService.updateAvailableFreeBets(this.betData);
      this.betslipService.findBetForFreeBetTooltip(this.betSlipSingles, this.accaBets, this.betSlipMultiples);

      // Check min stake value
      this.betData.forEach((bet: IBetInfo) => this.checkStake(bet));

      this.detectBetsWithTooLowStake();
    }

    this.updateBsButtonTitle();

    this.checkMaxStakeError();

    this.checkOddsBoostStatus();

    this.checkAllSingleStakesForBetslipSingles();
    if (this.deviceService.isDesktop) {
      this.isHeightUpdated = true;
    }
    if(!this.deviceViewType.mobile && !this.deviceViewType.tablet){
      this.showEachWayTooltip();
    }
  }

  ngAfterViewChecked() {
    if (this.isHeightUpdated) {
      this.updateBetSlipHeight();
    }
  }

  appendDrillDownTagNames(betSlip) {
    if (betSlip.sportId == '16' && betSlip.marketName === this.get2UpMarketName()) {
      return betSlip.drilldownTagNames ? betSlip.drilldownTagNames + `${betSlip.marketName},` : `${betSlip.marketName},`;
    }
    return '';
  }

  get2UpMarketName() {
    return this.localeService.getString('bma.twoUpMarketName');
  }

  /**
   * display scroll for betslip based on no. of single betslips
   */
  private updateBetSlipHeight(lottoStakeWrapperEl?): void {
    this.bsScrollWrapperEl = this.bsWrapperEl || this.scrollWrapperEl;
    if (this.loadComplete && this.bsScrollWrapperEl?.scrollHeight > 0 && this.betSlipSingles) {
      if ((this.deviceService.isMobile && lottoStakeWrapperEl) || this.betSlipSingles.length < this.bsHeightStakesCount) {
        this.bsMaxHeight = '100%';
        this.heightChanged.emit(0);
      } else if (this.betSlipSingles.length === this.bsHeightStakesCount) {
        this.windowRefService.nativeWindow.setTimeout(() => { this.setBsNotificationHeight(lottoStakeWrapperEl); });
        this.bsMaxHeight = '100%';
        this.heightChanged.emit(0);
      } else {
        this.setBsNotificationHeight(lottoStakeWrapperEl);
        this.bsMaxHeight = `${this.bsMaxHeightLimit}px`;
        this.heightChanged.emit(this.bsMaxHeightLimit);
      }
      this.isHeightUpdated = false;
    }
  }

  /**
   * sets the max height upto first 4 single stakes 
   */
  private setBsNotificationHeight(lottoStakeWrapperEl?): void {
    let stakeMaxHeight = 0;
    const queryClassName = lottoStakeWrapperEl ? '.lotto-text' : '.single-stake';
    [...this.windowRefService.document.querySelectorAll(queryClassName)].slice(0, this.bsHeightStakesCount).forEach((element: Element) => {
      stakeMaxHeight += element.clientHeight;
    });
    const singleStakeWrapperHeight = lottoStakeWrapperEl ? lottoStakeWrapperEl.clientHeight : this.singleStakesWrapperEl?.clientHeight || 0;
    this.bsMaxHeightLimit = this.bsScrollWrapperEl.scrollHeight - singleStakeWrapperHeight + stakeMaxHeight;
  }

  /**
   * Check if there is value in all single stakes input and apply it to all betslip items without a ammount
   */
  private checkAllSingleStakesForBetslipSingles(): void {
    if (this.allStakes && this.allStakes.value) {
      const allStakesAmount = (this.allStakes.value.match(/^[0]+[.]*[0]*$/)) ? '' : this.allStakes.value;
      this.betSlipSingles.forEach((betslipStake: IComplexBet) => {
        if (!betslipStake.Bet.stake.perLine && !betslipStake.disabled) {
          this.setAmount(betslipStake, allStakesAmount);
        }
      });
    }
  }

  private checkOddsBoostStatus(): void {
    // Disable odds boost if betslip is empty
    if (this.isBoostEnabled && this.isBoostActive && _.isEmpty(this.betSlipSingles) && !this.isLottoBet(this.betSlipSingles)) {
      this.pubSubService.publish(this.pubSubService.API.ODDS_BOOST_CHANGE, false);
    }
  }

  private checkMaxStakeError(): void {
    this.betData.forEach(item => {
      const stake = item.stake;
      const didStakeErrorOccur = (item.error === BETSLIP_VALUES.ERRORS.STAKE_TOO_HIGH ||
        item.Bet && item.Bet.error === BETSLIP_VALUES.ERRORS.STAKE_TOO_HIGH);
      const isStakeCorrect = ((Number(stake.stakePerLine) || 0) + (stake.freeBetAmount || 0)) <=
        stake.max && didStakeErrorOccur;

      if (isStakeCorrect) {
        item.error = null;
        item.errorMsg = null;
        item.Bet.error = null;
        item.Bet.errorMsg = null;
      }
    });
  }

  /**
   * Scroll to position
   * @param {number} position
   */
  private scrollTop(position): void {
    const scrollDiv = this.windowRefService.document.querySelector('.w-content-scroll');
    if (scrollDiv) {
      scrollDiv.scrollTop = position;
    }
  }

  /**
   * Scrolls to the bottom of betslip to make action buttons visible for user.
   */
  private scrollToActionButtons(): void {
    const scrollDiv = this.windowRefService.document.querySelector('.w-content-scroll');

    if (scrollDiv) {
      scrollDiv.scrollTop = scrollDiv.scrollHeight;
    }
  }

  private updateBetSingles() {
    return this.betSlipSingles && this.betSlipSingles
      .map(ev => {
        ev.competition = this.findCompetition(ev.outcomeId);
        return ev;
      });
  }

  private findCompetition(id): string {
    const selection = this.betslipStorageService.restore()
      .find(ev => ev.id === `SGL|${id}`);

    return selection ? selection.typeName : undefined;
  }

  private placeBetsResponseProcess(result, onQuickDeposit = false) {
    const error = result && result.errs && result.errs[0];

    this.quickDeposit.quickDepositPending = false;
    this.updatePlaceBetsPending(false);
    this.rebuildBetslip = false;
    // Find and then store ids of suspended outcomes
    this.betslipService.findSuspendedBetsId(this.betSlipSingles);

    if (error) {
      const { code, subCode, errorDesc } = error,
        customHandler = this.errorDictionary[subCode || code],
        errorTypeChecker = customHandler || this.handleDefaultError.bind(this),
        isOutcomeError = errorTypeChecker(result);

      this.quickDeposit.showQuickDepositForm = subCode === 'INSUFFICIENT_FUNDS';

      // sending errors to betslipErrorTracking service
      const singles = _.filter(result.bets, (bet: any) => bet.betTypeRef && bet.betTypeRef.id === 'SGL'),
        multiples = _.filter(result.bets, (bet: any) => bet.betTypeRef && bet.betTypeRef.id !== 'SGL'),
        errorsType = {
          isOnlyMultiples: multiples.length && !singles.length,
          bothTypesError: multiples.length && singles.length
        };
      let errorCode = false,
        errorMessage = false;

      if (customHandler || !isOutcomeError) {
        errorCode = subCode || code || false;
        errorMessage = errorDesc || subCode || false;
      }

      this.betslipErrorTracking(
        this.betSlipSingles,
        this.betSlipMultiples,
        result.errs,
        errorCode,
        errorMessage,
        errorsType);
    } else {
      if (Array.isArray(result.bets) &&
        (result.bets.some((bet: IBet) => bet.provider === this.betProvider) || this.hasClaimedOffersForBIRBets(result.bets))) {
        this.freeBetsService.getFreeBets().subscribe(); // Get Free Bets
      }

      this.betSlipSingles = [];
      this.betSlipMultiples = [];
      this.accaBets = [];

      this.betslipStorageService.clean();
      this.betslipLiveUpdateService.clearAllSubs(); // remove subscription for live serve update after place bet is success
      this.quickDeposit.showQuickDepositForm = false;

      if (this.windowRefService.nativeWindow.vsmobile && this.windowRefService.nativeWindow.vsmobile.instance) {
        const bets = this.windowRefService.nativeWindow.vsmobile.instance.getAllSelectedBets();
        _.each(bets, (bet: any) => {
          this.windowRefService.nativeWindow.vsmobile.instance.deselectBet(bet.selectionKey);
        });
      }

      this.pubSubService.publishSync(this.pubSubService.API.BET_PLACED, result);
      this.pubSubService.publishSync(this.pubSubService.API.MY_BET_PLACED, result);
      this.pubSubService.publish(this.pubSubService.API.BET_RECEIPT);
      this.pubSubService.publishSync(this.pubSubService.API.BETSLIP_COUNTER_UPDATE, this.betslipService.count());
      this.pubSubService.publish(this.pubSubService.API.ODDS_BOOST_CHANGE, false);


      /**
    * set event id to Local storage when placed a bet
    */
      let signPostingData = this.storageService.get('myBetsSignPostingData');
      if (result.bets) {
        result.bets.forEach((bet: IBet) => {
          bet.leg.forEach((leg: any) => {
            if(leg.part) {
              if (signPostingData?.length > 0) {
                const eventIndex = signPostingData.findIndex(data => Number(data.eventId) === Number(leg.part[0].eventId));
                if(eventIndex > -1) {
                  const betIndex = signPostingData[eventIndex].betIds.findIndex(id => Number(id) == Number(bet.id));
                  if(betIndex < 0) {
                    signPostingData[eventIndex].betIds.push(bet.id);
                  }
                } else {
                  const eventObj = {'eventId' : leg.part[0].eventId, 'betIds': [bet.id]};
                  signPostingData.push(eventObj);
                }
              } else {
                signPostingData = [{'eventId' : leg.part[0].eventId, 'betIds': [bet.id]}];
              }
              this.storageService.set('myBetsSignPostingData', signPostingData);
            }
          });
        });
      }
        
      // set successful message to betReceipt for "Deposit&Place Bet" flow (paycardDepositForm fired placeBets after successful deposit)
      if (onQuickDeposit) {
        this.betReceiptService.message = { type: 'success', msg: this.localeService.getString('bs.depositAndPlacebetSuccessMessage') };
        this.quickDeposit.showQuickDepositForm = true;
      } else {
        this.quickDeposit.showQuickDepositForm = false;
      }
      this.hideEmptyBetslip = true;
      this.betReceiptService.ids = result.ids;
      this.betslipDataService.readBets.bets = result.bets;
      this.scrollTop(0);
      this.pubSubService.publish(this.pubSubService.API.HOME_BETSLIP, this.localeService.getString('app.betslipTabs.betReceipt'));
      this.betData = [];
      this.hideAvailableFreeBetsMessage = true;

      this.priceChangeBets.clear();
    }
  }

  /**
   * Launches the countdown timer for inplay (BIR)
   * TODO this and related methods could be suppressed by timeService.countDownTimer
   *
   * @param {number} time
   */
  private birCountDownTimer(time: number): void {
    if (time) {
      this.countDownValue = time;
    }
    if (this.countDownValue !== undefined) {
      const min = `0${(this.countDownValue / 60).toString().slice(0, 1)}`;
      const sec = `0${parseInt(((this.countDownValue % 3600) % 60).toFixed(), 10)}`.slice(-2);
      this.countDownClock = `${min}:${sec}`;
      this.quickDepositService.countDownCurrentValue = this.countDownClock;

      if (this.countDownValue > 0) {
        this.countDownValue--;
        this.windowRefService.nativeWindow.setTimeout(this.birCountDownTimer.bind(this), 1000);
      } else {
        this.quickDepositService.countDownCurrentValue = null;
        this.countDownClock = null;
      }
    }
  }

  /**
   * clears price change errors for all singlesBets
   */
  private clearSingleBetsPriceChangeErr(): void {
    _.each(this.betSlipSingles, bet => this.clearSingleBetPriceChangeErr(bet));
  }

  /**
   * clears price change errors for ONE Bet
   * @param bet
   */
  private clearSingleBetPriceChangeErr(bet): void {
    if (!bet.disabled && (bet.errorMsg || bet.handicapErrorMsg || bet.handicapError || bet.error)) {
      bet.error = null;
      bet.errorMsg = '';
      bet.handicapError = null;
      bet.handicapErrorMsg = '';
      bet.Bet.clearErr();
    }
  }

  /**
   * Returns true if there are no active selections in the betslip
   *
   * @return {bool}
   */
  private noActiveSelectionsAction() {
    return !_.some(this.betData, (bet: any) => {
      return !bet.disabled;
    });
  }

  // BetSlip stake selection options
  private getDefaultStakeOptions() {
    return [
      { name: 'SP', value: 'SP' },
      { name: 'LP', value: 'LP' }
    ];
  }

  /**
   * Checks bet for "Triple" or "Accumulator" type
   * @param bet
   * @return {boolean}
   */
  private isBetForACCA(bet): boolean {
    // Acca is any bet which has line equal to 1 and legs is more then 1
    return bet.Bet.lines === 1 &&
      bet.Bet.legs.length > 1;
  }

  /**
   * Clears placeholder for All Stakes
   */
  private clearAllStakesHolder(): void {
    this.allStakes = { value: '' };
    this.storageService.remove('all-stakes');
  }

  /**
   * Check if Multiples stake boxes has amount entered
   */
  private checkMultipleStakeBox() {
    return _.find(this.betSlipMultiples, (bet: any) => bet.stake && bet.stake.amount > 0);
  }

  /**
   * Check which kind of suspended msg should be shown and set it
   * @params {object} bet
   */
  private setMultipleSuspendedErrMsg(bet) {
    // 'BET NOW' btn should be disabled if any amount entered in Multiples outcome stake box
    // or free bet is set && when suspended single outcome is present
    if ((bet.type !== 'SGL' || (bet.combiType !== undefined))) {
      const multipleWithDisableSingle = this.placeSuspendedErr.multipleWithDisableSingle;
      this.multiplesShouldBeRebuilded =
        ((this.checkMultipleStakeBox() && multipleWithDisableSingle) ||
          (this.betslipService.isMultipleFreeBetSelected(this.betSlipMultiples) && multipleWithDisableSingle)) &&
        (this.suspendedOutcomesCounter > 0);

      const placeSinglesSuspendErr = this.suspendedOutcomesCounter > 0
        ? this.betslipService.getSuspendedMessage(this.suspendedOutcomesCounter)
        : null;

      this.placeSuspendedErr = {
        multipleWithDisableSingle,
        disableBet: this.multiplesShouldBeRebuilded,
        msg: placeSinglesSuspendErr
      };
    }
  }

  /**
   * Get all bets
   * @returns {Array}
   */
  private getAllBets(): IBetInfo[] {
    return this.betSlipSingles && this.betSlipSingles.length ?
      this.betSlipSingles.concat(this.betSlipMultiples && this.betSlipMultiples.length ? this.betSlipMultiples : []) : [];
  }

  /**
   * Publish acca notification changed events
   */
  private accaNotificationChanged(): void {
    if (this.betSlipMultiples) {
      const bet = this.getFirstMultipleInfoForAccaNotification(this.betSlipMultiples[0]);
      this.pubSubService.publishSync(this.pubSubService.API.ACCA_NOTIFICATION_CHANGED, bet);
    }
  }

  /**
   * Check if acca bet valid
   * @returns {Boolean}
   */
  private isAccaBetValid(potentialPayout): boolean {
    return potentialPayout > this.MIN_PAYOUT_ACCA;
  }

  /**
   * Make price format according to User settings
   * @returns {String}
   */
  private getFormattedPrice(potentialPayout): string {
    if (this.userService.oddsFormat === 'frac') {
      return this.fracToDecService.decToFrac(potentialPayout, true);
    }
    return this.fracToDecService.getNumberWith2Decimals(potentialPayout);
  }

  private handleInsufficientFunds(): void {
    // show "make deposit" button if user has insufficient funds
    this.quickDeposit.quickDepositFormAllowed = true;
    this.quickDeposit.showQuickDepositForm = true;
  }

  /**
   * Parse errors recieved after betplacement and return if ones exist.
   * @param {object} outcomesErrors
   * @returns {Boolean}
   */
  private outcomesErrorParser(outcomesErrors, bets, legs) {
    let areErrors = [];

    // process errors with no outcomeRef.id
    if (outcomesErrors.undefined) {
      areErrors = outcomesErrors.undefined.map(err => this.stakeErrorParser(err, bets, legs));
    }
    // process outcome errors
    areErrors = areErrors.concat(Object.keys(_.omit(outcomesErrors, 'undefined'))
      .map(outcomeId => this.outcomeErrorParser(outcomesErrors[outcomeId])));

    const isError = areErrors.some(err => err);

    if (isError) {
      this.pubSubService.publishSync(this.pubSubService.API.BETSLIP_UPDATED, [this.fetchedData]);
    }

    return isError;
  }

  /**
   * Parse errors errors with no outcomeRef.id
   * @param {Object} stakeError
   * @param {Array} bets - response bets
   * @param {Array} legs - response legs
   * @returns {Boolean}
   */
  private stakeErrorParser(stakeError, bets, legs) {
    const payload: any = {};
    const bet = _.find(bets, (b: any) => b.documentId === stakeError.betRef);
    payload.bet = this.betslipService.getBetslipBetByResponseBet(bet, legs, this.getAllBets());

    switch (stakeError.subCode) {
      case BETSLIP_VALUES.ERRORS.STAKE_TOO_HIGH:
        if (payload.bet) {
          payload.bet.stake.max = bet.stake.maxAllowed;
        }
        payload.type = 'max';
        payload.placeBet = true;
        this.addStakeError(stakeError, payload);
        return true;
      case BETSLIP_VALUES.ERRORS.STAKE_TOO_LOW:
        if (payload.bet) {
          payload.bet.stake.min = bet.stake.minAllowed;
        }
        payload.type = 'min';
        payload.placeBet = true;
        this.addStakeError(stakeError, payload);
        return true;
      default:
        return false;
    }
  }

  /**
   * Parse particular outcome errors
   * @param {Array} outcomeErrors
   * @returns {Boolean}
   */
  private outcomeErrorParser(outcomeErrors) {
    let isError = false;
    const suspended = _.find(outcomeErrors, { subCode: BETSLIP_VALUES.ERRORS.OUTCOME_SUSPENDED }),
      evSuspended = _.find(outcomeErrors, { subCode: BETSLIP_VALUES.ERRORS.EVENT_STARTED }),
      priceChange: any = _.find(outcomeErrors, { subCode: BETSLIP_VALUES.ERRORS.PRICE_CHANGED }),
      handicapChange: any = _.find(outcomeErrors, { subCode: BETSLIP_VALUES.ERRORS.HANDICAP_CHANGED }),
      payload: any = {};

    if (priceChange) {
      payload.lp_num = priceChange.price[0].priceNum;
      payload.lp_den = priceChange.price[0].priceDen;
      payload.status = 'A';
      payload.placeBet = true;
      this.updateBetError(priceChange, payload, 'outcome');
      this.addOutcomeError(priceChange, payload);
      // Update all legs that contain selection ID with new prices (e.g. "EACH_WAY")
      this.betslipService.updateLegsWithPriceChange(payload, priceChange.outcomeRef.id);

      isError = true;
    }

    if (handicapChange) {
      payload.raw_hcap = handicapChange.handicap;
      payload.hcap_values = {
        A: (handicapChange.handicap * (-1)).toFixed(1),
        H: handicapChange.handicap.toFixed(1),
        L: handicapChange.handicap.toFixed(1)
      };
      payload.status = 'A';
      payload.placeBet = true;
      this.updateBetError(handicapChange, payload, 'outcome');
      isError = true;
    }

    if (suspended) {
      payload.status = 'S';
      this.updateBetError(suspended, payload, 'outcome');
      isError = true;
    }

    if (evSuspended) {
      payload.started = 'Y';
      this.updateBetError(evSuspended, payload, 'event');
      isError = true;
    }

    return isError;
  }

  /**
   * Show error for particular bet or general error.
   * @param {object} err
   * @param {object} payload
   */
  private addStakeError(err, payload) {
    if (payload.bet) {
      payload.bet.Bet.update(payload, 'stakeError');
    } else {
      this.placeStakeErr = this.localeService.getString(`bs.${err.subCode}`);
    }
  }

  /**
   * Update outcome or Event
   * For 'outcome' => Add 'OUTCOME_SUSPENDED' or 'PRICE_CHANGED' error messages
   */
  private updateBetError(err, payload, betItemName: string) {
    _.each(this.betSlipSingles, (bet: any) => {
      if (bet.outcomeId === err.outcomeRef.id) {
        bet.Bet.update(payload, betItemName);
      }
    });
  }

  private subscribeToOddsBoostChange(): void {
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.ODDS_BOOST_REBOOST, () => {
      this.rebuildBetslip = true;
      this.reboost = this.isBoostActive;
      if (this.reboost) {
        this.priceChangeBannerMsg = this.localeService.getString('bs.reboostPriceChangeBannerMsg');
      }
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.ADDTOBETSLIP_PROCESS_FINISHED, () => {
      const value: IBetInfo = _.find(_.union(this.betSlipSingles, this.betSlipMultiples), (bet: IBetInfo) => bet.Bet.oddsBoost);

      this.commandService.execute(this.commandService.API.ODDS_BOOST_SET_MAX_VAL, [value && value.Bet.oddsBoost.betBoostMaxStake]);
      if (value && !this.isMobile && !this.popupsShown) {
        this.pubSubService.publish(this.pubSubService.API.ODDS_BOOST_INFO_DIALOG);
      }
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.ODDS_BOOST_CHANGE, (active: boolean) => {
      if (active && this.maxStakeExceeded()) {
        return;
      }

      this.placeStakeErr = null;
      this.isBoostActive = active;
      this.reboost = active ? this.reboost : false;

      if (this.isBoostActive && this.isFreeBetSelected()) {
        this.commandService.execute(this.commandService.API.ODDS_BOOST_SHOW_FB_DIALOG, [false, 'betslip']);
      }
    });

    // update oddsboost after bet placed and update oddsboost counter in sidebar menu.
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.BETS_COUNTER_PLACEBET, () => {
      if (this.isBoostActive) {
        this.pubSubService.publish(this.pubSubService.API.ODDS_BOOST_DECREMENT_COUNTER);
      }
    });
  }

  private maxStakeExceeded(): boolean {
    return this.commandService.execute(this.commandService.API.ODDS_BOOST_MAX_STAKE_EXCEEDED, [+this.totalStake()]);
  }

  // Add 'OUTCOME_SUSPENDED' or 'PRICE_CHANGED' error messages to outcome.
  private addOutcomeError(err, payload) {
    _.each(this.betSlipSingles, this.updatePayLoadByType('outcome', payload, err));
  }

  private updatePayLoadByType(type: string, payload, err) {
    return function (bet: any) {
      if (bet.outcomeId === err.outcomeRef.id) {
        bet.Bet.update(payload, type);
      }
    };
  }

  private digitKeyboardShown(decBtn: boolean, quickDepBtn: boolean, quickStakeItems: string[], kbId: string): void {
    if (kbId === 'slide-out-betslip') {
      this.isDigitKeyboardShown = true;
      this.changeDetectorRef.detectChanges();
    } 
  }

  private digitKeyboardHidden(kbId: string): void {
    if (kbId === 'slide-out-betslip') {
      this.isDigitKeyboardShown = false;
    }
  }

  /**
   * After any changes affected by calling init() ref to HTML element lost
   * so needed to lock again for new container
   */
  private lockBodyScrollAfterReinit(): void {
    if (!this.betslipIsOpened || !(this.deviceService.isMobile && this.deviceService.isIos)) {
      return;
    }

    if (this.scrollContainerRendered()) {
      this.lockBodyScroll(true);
    } else {
      this.lockBodyScrollAfterRender();
    }
  }

  /**
   * Wait view rendering HTML element
   */
  private lockBodyScrollAfterRender(): void {
    // Stop when betslip closes
    this.scrollWrapperSubjectClosed$ = new Subject();
    this.scrollWrapperRendered$.pipe(
      first(),
      takeUntil(this.scrollWrapperSubjectClosed$)
    ).subscribe(() => {
      this.scrollWrapperSubjectClosed$.complete();
      this.lockBodyScroll(true);
    });
  }

  /**
   * Lock lock touchmove scroll for iOS
   * @param {boolean} showSide
   */
  private lockBodyScroll(showSide: boolean): void {
    if (showSide) {
      this.bodyScrollLockService.disableBodyScroll(this.scrollWrapperEl);
    } else {
      this.bodyScrollLockService.enableBodyScroll();
    }
  }

  /**
   * <div class="bs-wrapper-block" *ngIf="loadComplete && !loadFailed && !hidden">
   */
  private scrollContainerRendered(): boolean {
    return this.loadComplete && !this.loadFailed && !this.hidden;
  }

  private detectBetsWithTooLowStake(): void {
    this.hasBetsWithTooLowStake = this.betData.some((_bet: IBetInfo) => !this.checkStake(_bet));
  }

  private updateBsButtonTitle(): void {
    if (this.userService.status) {
      const priceOrHcapUpdate = this.isPriceOrHcapUpdate();
      // There is case when error code is not changed to PRICE_CHANGED but price is actually
      // changed(when price is changed for suspended bet)
      this.bsButtonTitle = priceOrHcapUpdate || this.isPriceUpdate() ? 'bs.acceptBet' : 'bs.betNow';
    } else {
      this.bsButtonTitle = 'bs.betNowLogIn';
    }
  }

  /**
   * Handle error for overask or placeBets
   * @params {any} error
   */
  private handleError(error: any): void {
    if (error) {
      // set stake empty if overask offer expired - business flow
      if (error.data && (error.data.offerTimeExpired || error.data.status === 'PT_ERR_AUTH' || error.data.status === 'LOW_FUNDS')) {
        if (error.data.status !== 'LOW_FUNDS') {
          this.clearStakes();
        }
        this.init();
      } else {
        // sending errors to betslipErrorTracking service
        const errorCode = error.status || false,
          errorMessage = error.statusText || error.message || false;

        this.betslipErrorTracking(
          this.betSlipSingles,
          this.betSlipMultiples,
          [error],
          errorCode,
          errorMessage);
      }
    }
  }

  /**
   * Empty stake field and unset freebet
   * @params {any} bets
   */
  private clearStakes(): void {
    this.clearAllStakesHolder();
    if (this.betData) {
      this.unsetFreeBets(this.betData);
      this.betData.forEach((bet: any) => {
        this.setAmount(bet, '');
      });
    }
  }

  /**
   * Calculates is any bet checkbox selected
   * Used in overask process
   */
  private calculateIsBetsSelected(): void {
    const allBets = this.getAllBets();
    this.isBetsSelected = _.some(allBets, (betDataEntity: IBetInfo) => betDataEntity.isSelected && !betDataEntity.disabled);
    this.isOveraskCanBePlaced = this.overAskService.isOveraskCanBePlaced();
  }

  private setQuickDepositInitialData(): void {
    const { quickDepositCache } = this.quickDepositService;

    this.quickDeposit = this.defaultQuickDepositData;

    if (quickDepositCache) {
      this.quickDeposit = quickDepositCache;
    }
  }

  /**
   * Show unvalid free Bet popup
   */
  private showUnvalidFreeBetPopup(): void {
    this.infoDialogService.openInfoDialog(
      this.localeService.getString('bs.freeBetNotEligible'),
      this.localeService.getString('bs.freeBetCanNotBeAdded'),
      undefined,
      undefined,
      undefined,
      [{
        caption: this.localeService.getString('bs.ok'),
        cssClass: 'btn-style2',
        handler: () => {
          this.infoDialogService.closePopUp();
        }
      }]);
  }

  private subscribeToVanillaEvents(): void {
    this.sub = this.betslipLiveUpdateService.getPriceUpdate().subscribe(() => {
      this.estimatedReturnAfterPriceChange = this.totalEstReturns() as number;
    });
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API['show-slide-out-betslip-true'], () => {
      this.showEachWayTooltip();
      this.onShowQuickDepositWindow();
    });
    this.pubSubService.subscribe('BetSlipVanilla', [
      this.pubSubService.API.DIGIT_KEYBOARD_SHOWN,
      this.pubSubService.API['show-slide-out-betslip-false']
    ], () => {
      this.onCloseQuickDepositWindow(true);
    });
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.BETSLIP_COUNTER_UPDATE, () => {
      this.handleBetslipUpdate();
    });
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.SET_FREE_BET, () => {
      this.onCloseQuickDepositWindow();
    });
  }
  /**
   * shows quick deposit window in case of nullable balance and existing bets
   */
  private onShowQuickDepositWindow(): void {
    this.onBoardingData = null;
    if (!this.sessionStorageService.get('buttonText') && !this.sessionStorageService.get('betPlaced')) {
      const storedOnboardingData = this.sessionStorageService.get('firstBetTutorial');
      const stepType = this.isBoostEnabled && !this.placeBetsPending &&
        this.isOddsBoostEnabled() && this.hasSelectionsWithBoost() ? 'boost' : 'defaultContent';
      this.onBoardingData = { step: 'betSlip', tutorialEnabled: storedOnboardingData && storedOnboardingData.firstBetAvailable, type: stepType };
    }
    this.isZeroBalanceWithExistingBets =
      this.userService.status && this.betData.length && !Number(this.userService.sportBalance);
    if (this.isZeroBalanceWithExistingBets) {
      this.loadQuickDepositIfEnabled();
    }
  }

  private checkStakeStatus(): void {
    this.totalStakeAmount = this.totalStake();
    this.errorMessage = this.getErrorMsg();
    this.neededAmountForPlaceBetIsChanged = this.isAmountNeeded();
  }

  /**
   * clear betslip and overask if has active overask and user is logged out
   */
  private clearOveraskSubscription(): void {
    this.sessionService.whenProxySession().catch(() => {
      if (this.storageService.get('overaskIsInProcess')) {
        this.betslipStorageService.cleanBetslip(false, false);
        this.betslipStorageService.clearStateInStorage();
      }
    });
  }

  /**
   * Check the claimedOffer status is equal 'claimed' if a bet is BIR
   * @param {IBet[]} bets
   * @returns {boolean} true if bets have at least one claimedOffer status equals 'claimed' for non BIR bet
   */
  private hasClaimedOffersForBIRBets(bets: IBet[]): boolean {
    return bets.some((bet: IBet) => {
      if (bet.provider !== this.betProvider && bet.hasOwnProperty(this.claimedOffers)) {
        return bet.claimedOffers.some((claimedOffer: IClaimedOffer) => claimedOffer.status === this.claimed);
      }
      return false;
    });
  }

  /**
  * After quick bet response update freebets local storage 
  * @param betReceipt 
  */
  private freeBetsStoreUpdate(bets: IBet[], toteBetId?): IFreebetToken[] {
    if(toteBetId){
      const freeBetsState: IFreeBetState = this.freeBetsService.getFreeBetsState();
      this.freeBetsData = [...freeBetsState.data, ...freeBetsState.betTokens, ...freeBetsState.fanZone];
      this.isFreeBetApplied = true;
      this.freeBetsData = this.freeBetsData.filter((freebet: IFreebetToken) => Number(toteBetId) != Number(freebet.freebetTokenId));
    }
    if (bets.length) {
      const freeBetsState: IFreeBetState = this.freeBetsService.getFreeBetsState();
      this.freeBetsData = [...freeBetsState.data, ...freeBetsState.betTokens, ...freeBetsState.fanZone];
      bets.forEach((bet: IBet) => {
        if (bet.freebet && bet.freebet.length) {
          this.isFreeBetApplied = true;
          this.freeBetsData = this.freeBetsData.filter((freebet: IFreebetToken) => Number(bet.freebet[0].id) != Number(freebet.freebetTokenId));
          if (this.storageService.get('toteFreeBets') && this.storageService.get('toteFreeBets').length > 0) {
            this.storageService.set('toteFreeBets', this.storageService.get('toteFreeBets').filter(x => Number(bet.freebet[0].id) !== Number(x.freebetTokenId)));
          }
          if (this.storageService.get('toteBetPacks') && this.storageService.get('toteBetPacks').length > 0) {
            this.storageService.set('toteBetPacks', this.storageService.get('toteBetPacks').filter(x => Number(bet.freebet[0].id) !== Number(x.freebetTokenId)));
          }
        }
      })
    }
    return this.freeBetsData;
  }
  public showRestrictedHRInfoTooltip(restrictionMsg, position) {
    this.isShowHorseRestrictedInfo = !this.isShowHorseRestrictedInfo;
    if (this.isShowHorseRestrictedInfo) {
      this.isShowRacecardRestrictedInfo = false;
      this.sendGTMData(restrictionMsg, position);
    }
  }
  public showRaceCardInfoTooltip(restrictionMsg, position) {
    this.isShowRacecardRestrictedInfo = !this.isShowRacecardRestrictedInfo;
    if (this.isShowRacecardRestrictedInfo) {
      this.isShowHorseRestrictedInfo = false;
      this.sendGTMData(restrictionMsg, position);
    }
  }
  /**
 * Send GA tracking on render of tooltip
 */
  sendGTMData(LocationEvent: string, positionEvent: string): void {
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'betslip',
      'component.LabelEvent': 'restriction messages',
      'component.ActionEvent': 'click',
      'component.PositionEvent': positionEvent,
      'component.LocationEvent': LocationEvent,
      'component.EventDetails': 'info icon',
      'component.URLClicked': 'not applicable'
    }
    this.gtmService.push(gtmData.event, gtmData);
  }
  /**
 * Send GA tracking on render of of resticted horse messages
 */
  private sendGTMDataOnLoad(message: string, positionEvent: string): void {
    const gtmData = {
      event: 'contentView',
      'component.CategoryEvent': 'betslip',
      'component.LabelEvent': 'restriction messages',
      'component.ActionEvent': 'load',
      'component.PositionEvent': positionEvent,
      'component.LocationEvent': 'betslip',
      'component.EventDetails': message,
      'component.URLClicked': 'not applicable'
    }
    this.gtmService.push(gtmData.event, gtmData);
  }

  private isOddsBoostEnabled(): boolean {
    return !!this.coreToolsService.getOwnDeepProperty(this.cmsService.initialData, 'oddsBoost.enabled');
  }

  private hasSelectionsWithBoost(): boolean {
    return _.some(this.betslipDataService.bets, bet => {
      return (bet.oddsBoost && !bet.info().disabled);
    })
  }
  // Lucky 15/31/63 sign posting 
     sendGtmDataoninfoicon(label){
    const gtmData={
      event: 'Event.Tracking',
     'component.CategoryEvent': 'betslip',
     'component.LabelEvent': 'lucky bonus',
     'component.ActionEvent': 'click',
     'component.PositionEvent': label,
     'component.LocationEvent': 'betslip',
     'component.EventDetails': 'info icon',
     'component.URLClicked':  'not applicable',
  }
  this.gtmService.push(gtmData.event, gtmData);
}


  /**
   * updates the is isEachWayAvailable to dynamically display each way checkbox
   */
  private updateEachWayAvailable(): void {
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.EACHWAY_FLAG_UPDATED, (payloadDetail: any, betInfo: IBetInfo) => {
      this.betSlipSingles.forEach((bet: IBetInfo) => {
        if (betInfo && bet && bet.Bet && bet.id.toString() == betInfo.id) {
          bet.Bet.params.eachWayAvailable = payloadDetail.ew_avail;
          bet.isEachWayAvailable = payloadDetail.ew_avail == 'Y';
        }
      });

      if (!this.isMultiplesEachWay()) {
        this.betSlipMultiples.forEach((bet: IBetInfo) => {
          this.winOrEachWay(bet);
        });
      }
    });
  }

  /**
   * Get betslip stake price for multiple bets
   * @param betslipStake : betslip info 
   * @returns betInfo
   */
   public getBetInfoPrice(betslipStake: any): any {
    const betInfo: any = {
      price: {
        priceNum: null,
        priceDen: null
      },
      sportId: betslipStake ? betslipStake.sportId : undefined
    }
    const potentialPayout: any = betslipStake ? this.oddsACCA(betslipStake) : null;
    const splitItems: string[] = potentialPayout ? potentialPayout.split('/') : [];

    // Assigning a denominator 1 for potentialPayout having decimal odds
    // to have a common calc logic for both deci and fractional odds for multiples
    if(splitItems && splitItems[0] && this.userService.oddsFormat === 'dec'){
      splitItems[1] = '1';
    }

    if (splitItems && splitItems.length === 2) {
      betInfo.price.priceNum = splitItems[0];
      betInfo.price.priceDen = splitItems[1];
    }

    return betInfo;
  }
  
  /**
   * trigger GA tracking for single and multiple bets
   * @param bet : betslipstake
   */
  private gaTrackingOnEachWayChange(bet: any): void {
    // single bet
    if (bet && bet.selectedFreeBet && bet.isSPLP && bet.price?.priceType !== 'SP') {
      this.setFreeBetGtmData(bet, true);
    } // multiple bet
    else if (bet && bet.selectedFreeBet && !bet.isSPLP && !bet.isSP) {
      this.setFreeBetGtmData(bet, false);
    }
  }

  /**
   * sets gtm data for eachway checkbox
   * @param betslipStake : bet info
   */
  private setFreeBetGtmData(betslipStake: any, isSingleBet: boolean): void {
    let eventName: string = 'not applicable';
    if(betslipStake.localTime && betslipStake.eventName){
      eventName = betslipStake.localTime + ' ' + betslipStake.eventName;
    }
    
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'promotions',
      'component.LabelEvent': 'each way free bet',
      'component.ActionEvent': 'click',
      'component.PositionEvent': betslipStake.Bet.isEachWay ? 'checked' : 'unchecked',
      'component.LocationEvent': 'betslip',
      'component.EventDetails': isSingleBet ? eventName : 'not applicable',
      'component.URLclicked': 'not applicable',
      'sportID': isSingleBet ? betslipStake.sportId : 'not applicable'
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

  /**
   * Filter market names
   * @param {string} name
   * @returns {string}
   */
  findWinOrEachWay(betslipStake: any){
    if (betslipStake && (betslipStake.sportId === '21'|| betslipStake.sport === 'HORSE_RACING')) {
      const checkMarketName = betslipStake.isFCTC ? betslipStake.Bet.betComplexName : betslipStake.marketName;
      return checkMarketName === 'Win or Each Way' ? 'To Win' : checkMarketName;
    }
    else {
      return betslipStake.isFCTC ? betslipStake.Bet.betComplexName : betslipStake.marketName;
    }
  }

  /**
   * To Show Tooltip for eachway checkbox
   * @param betSlipSingles
   */
  public showEachWayTooltip() {
  
    this.toolTipArgs = {
      eachWayTooltip: this.toolTipMessage
    }

    if (this.Tooltip_Enable && this.betSlipSingles?.length>0) {
      for (const [index, betslipData] of this.betSlipSingles.entries()) {
        if (betslipData && (betslipData.sportId === '21' || betslipData.sport === 'HORSE_RACING') && !betslipData.disabled && betslipData.isEachWayAvailable) {
          if (this.userService.username && !(this.storageService.get(this.BetSlip_EachWay_Tooltip)
            && this.userService.username === this.storageService.get(this.BetSlip_EachWay_Tooltip).user)) {
            this.horseIndex = index;
            this.disableEachWayTooltip = true;
            this.eachWayGaTracking = true;
            this.storageService.set(this.BetSlip_EachWay_Tooltip, { user: this.userService.username, displayed: true });
            this.notifyTimeout = this.windowRefService.nativeWindow.setTimeout(() => {
              this.disableEachWayTooltip = false;
            }, this.delay * BETSLIP_VALUES.IN_MS);
          }
          break;
        }
      }
    }
  }

  /**
   * sets GA tracking for eachway check box
   * @param bet: betslipstake
   */
  public gaTrackingOnEachWayCheckBox(bet: any) {
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'betslip',
      'component.LabelEvent': bet.sport,
      'component.ActionEvent': bet.Bet.isEachWay ? 'checked' : 'unchecked',
      'component.PositionEvent': bet.outcomeName,
      'component.LocationEvent': 'betslip',
      'component.EventDetails': (this.eachWayGaTracking && (bet.sport === "HORSE_RACING")) ? 'each way alert' : 'each way regular',
      'component.URLclicked': 'not applicable',
      'sportID': bet.sportId
    };
    this.gtmService.push(gtmData.event, gtmData);
  }
  
/**
* Send GA tracking on render of of resticted horse messages
*/
  public validateRestrictedHRs() {
    if (!this.isRestrictedHorsesLoaded) {
      this.sendGTMDataOnLoad(this.restrictedHorseMsg, 'restricted Horses');
      this.isRestrictedHorsesLoaded = true;
    }
    return true;
  }

/**
* Send GA tracking on render of of resticted racecard messages
*/
  public validateRestrictedRacecards() {
    if (!this.isRestrictedRacecardLoaded) {
      this.sendGTMDataOnLoad(this.restrictedRaceCardMsg, 'restricted Racecards');
      this.isRestrictedRacecardLoaded = true;
    }
    return true;
  }

  checkSP(betData): boolean {
    const isAvailable = !!betData.outcomes.some((item: any) => item.price.priceType === 'SP');
    return (['L15', 'L31', 'L63'].includes(betData.type) && isAvailable);
  }

  showLuckySignPostInfoLable(value): boolean {
    return ['L15', 'L31', 'L63'].includes(value);
  }
}
