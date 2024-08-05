import { from as observableFrom, of as observableOf, Subscription } from 'rxjs';

import { mergeMap, map } from 'rxjs/operators';
import {
  Component, Input, Output, OnInit, EventEmitter, OnDestroy, ChangeDetectorRef,ViewChild, ElementRef
} from '@angular/core';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UserService } from '@core/services/user/user.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { QuickbetService } from '@app/quickbet/services/quickbetService/quickbet.service';
import { QuickbetUpdateService } from '@app/quickbet/services/quickbetUpdateService/quickbet-update.service';
import { QuickbetDepositService } from '@quickbetModule/services/quickbetDepositService/quickbet-deposit.service';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { QuickbetNotificationService } from '@app/quickbet/services/quickbetNotificationService/quickbet-notification.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { IQuickbetDepositModel } from '@app/quickbet/models/quickbet-deposit.model';
import { IFreebetToken, ITokenPossibleBet, IBppRequest } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { IPrice } from '@oddsBoost/components/oddsBoostPrice/odds-boost-price.model';
import { GtmService } from '@core/services/gtm/gtm.service';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { TimeService } from '@app/core/services/time/time.service';
import { ICountDownTimer } from '@app/core/services/time/time-service.model';
import { BppProvidersService } from '@app/bpp/services/bppProviders/bpp-providers.service';
import { IFreebetsPopupDetails, ISystemConfig } from '@app/core/services/cms/models/system-config';
import { FiveASideContestSelectionService } from '@app/fiveASideShowDown/services/fiveASide-ContestSelection.service';
import { SELECTED_CONTEST_CHANGE } from '@app/fiveASideShowDown/constants/constants';

import { ServiceClosureService } from '@lazy-modules/serviceClosure/service-closure.service';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { StorageService } from '@app/core/services/storage/storage.service';
import { quickbetConstants } from '@app/quickbet/constants/quickbet.constant';
import { ILuckyDipFieldsConfig } from '@app/lazy-modules/luckyDip/models/luckyDip';
import environment from '@environment/oxygenEnvConfig';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
@Component({
  selector: 'quickbet-selection',
  templateUrl: 'quickbet-selection.component.html',
  styleUrls: ['quickbet-selection.component.scss']
})

export class QuickbetSelectionComponent implements OnInit, OnDestroy {

  @Input() selection: IQuickbetSelectionModel;
  @Input() placeBetPending: { state: boolean };
  @Input() leftBtnLocale: string;
  @Input() ycOddsValue?: Function;
  @Input() isLogAndQuickBetPending?: boolean;
  @Input() showIFrame: boolean;
  @Input() quickDepositFormExpanded: boolean;
  @Input() getFreeBetName: string;
  @Input() betType: string;
  @Input() isFiveASideBet: boolean;
  @Input() isLuckyDip?:boolean;
  @Input() luckyDipCmsData?: ILuckyDipFieldsConfig;
  @Input() luckyDipMarketName?: string;
  @Input() isWSdisabled?: boolean;
  @Input() betslipType: string;
  @Output() readonly placeBetFn: EventEmitter<void> = new EventEmitter();
  @Output() readonly closeFn: EventEmitter<void> = new EventEmitter();
  @Output() readonly addToBetslipFn: EventEmitter<void> = new EventEmitter();
  @Output() readonly openQuickDepositFn: EventEmitter<void> = new EventEmitter();
  @Output() firstBetBoostEmit: any = new EventEmitter();
  @ViewChild('qbDigitKeyboard',{ static: false }) qbDigitKeyboard:ElementRef
  countDownTimer: ICountDownTimer;
  quickDeposit: IQuickbetDepositModel;
  selectedFreeBet: IFreebetToken;
  leftBtnText: string;
  freebetsConfig: IFreebetsPopupDetails;
  freebetsList: IFreebetToken[];
  betPackList : IFreebetToken[];
  fanzoneList: IFreebetToken[];

  isBoostEnabled: boolean; // True, if odds boost enabled in cms
  boostOldPrice: IPrice;
  boostNewPrice: IPrice;
  quickStakeVisible: boolean = true;
  body: IBppRequest;
  isUserLogIn: boolean;
  isWinorEachWay:boolean
  maxPayOutValue: string;
  maxPayedOut: boolean;
  maxPayFlag: boolean;
  maxPayMsg: string;
  link: string;
  click: string;
  infoMessage: string = 'Values have been capped or maxpayedout';
  gtmInfo: string[] = ['link click','rendered'];
  disableEachWayTooltip:boolean;
  delay:number;
  toolTipArgs: {[key: string]: string};
  Tooltip_Enable:boolean;
  private notifyTimeout: number;
  EachWay_Tooltip: string = 'TooltipEachWay';
  toolTipMessage:string;
  eachWayGaTracking:boolean = false;
  eachWayGaTraking: boolean = false;
  readonly promoLabelsFlagsExcluded = 'EVFLAG_EPR,MKTFLAG_EPR';
  readonly stakePattern: string = '^(\\d{0,12}((\\.|,)\\d{0,2})?)?$';

  protected QB_SELECTION_NAME = 'QuickbetSelectionController';
  protected LOCK_PLACE_BET_TIMEOUT: number = 1500;
  protected hasBeenReloaded: boolean = true;

  private freebetsSubscription: Subscription;
  private betPackSubscription: Subscription;
  extraPlaceData: any;
  extraPlaceName: string;
  isBrandLadbrokes:boolean;
  private fanzoneSubscription: Subscription;


  constructor(protected pubsub: PubSubService,
              protected user: UserService,
              protected locale: LocaleService,
              protected filtersService: FiltersService,
              protected quickbetDepositService: QuickbetDepositService,
              protected quickbetService: QuickbetService,
              protected quickbetUpdateService: QuickbetUpdateService,
              protected freeBetsFactory: FreeBetsService,
              protected quickbetNotificationService: QuickbetNotificationService,
              protected commandService: CommandService,
              protected cmsService: CmsService,
              protected gtmService: GtmService,
              protected cdr: ChangeDetectorRef,
              protected windowRef: WindowRefService,
              protected timeService: TimeService,
              protected bppProviderService: BppProvidersService,
              protected fiveASideContestSelectionService: FiveASideContestSelectionService,
              public serviceClosureService: ServiceClosureService,
              protected sessionStorageService: SessionStorageService,
              private storageService: StorageService,
              protected bonusSuppressionService: BonusSuppressionService
              ) {
    this.onlineListener = this.onlineListener.bind(this);
    this.offlineListener = this.offlineListener.bind(this);
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
  }

  ngOnInit(): void {
    this.formBodyParamforBuildBet();
    this.buildBetCall();
    this.leftBtnText = this.locale.getString(this.leftBtnLocale || 'quickbet.buttons.addToBetslip');
    this.quickDeposit = this.quickbetDepositService.quickDepositModel;
    this.cmsService.getSystemConfig().subscribe((data: ISystemConfig) => {
      if (data && data.maxPayOut) {
      this.maxPayFlag = data.maxPayOut.maxPayoutFlag;
      this.maxPayMsg = data.maxPayOut.maxPayoutMsg;
      this.link = data.maxPayOut.link;
      this.click = data.maxPayOut.click;
      }
      this.freebetsConfig = data.FreeBets;
    });

    this.addEventListeners();
    if(this.selection.isEachWayAvailable){
    this.showEachWay(this.selection);
    }

    this.pubsub.subscribe(this.QB_SELECTION_NAME, this.pubsub.API.SUCCESSFUL_LOGIN, () => {
      if (this.selection.isEachWayAvailable) {
        this.showEachWay(this.selection);
      }
      this.initOddsBoost();
      !this.isLuckyDip && this.bppProviderService.quickBet(this.body, true).subscribe((res) => {
       this.selection.freebetList = res && res.bets && res.bets[0] && res.bets[0].freebet && res.bets[0].freebet.filter(singleFreebet => singleFreebet.type === "SPORTS") as IFreebetToken[] || [];
        this.getFreebetsList();  
      });
    });

    this.pubsub.subscribe(this.QB_SELECTION_NAME, this.pubsub.API.GET_QUICKBET_SELECTION_STATUS, (...args) => {
      if (!args[0] && this.canBoostSelection) {
        this.initOddsBoost();
      }
    });

    this.pubsub.subscribe(this.QB_SELECTION_NAME, this.pubsub.API.QUICKBET_OPENED, (selectionData: IQuickbetSelectionModel) => {
      if (selectionData && selectionData.freebet) {
        this.onFreebetChange({ output: 'selectedChange', value: selectionData.freebet });
      }
    });

    this.pubsub.subscribe(this.selection.eventId, this.pubsub.API.SET_ODDS_FORMAT, () => this.changeOddsFormat());
    this.getFreebetsList();
    this.quickbetDepositService.update(this.selection.stake, this.selection.isEachWay);

    const disabledMap = {
      event: false,
      market: false,
      selection: false
    };

    if (this.selection.disabled) {
      const placeMap = {
          eventStatusCode: 'event',
          marketStatusCode: 'market',
          outcomeStatusCode: 'selection'
        },
        suspensionMap = [];

      for (const key in this.selection) {
        if (this.selection[key] === 'S') {
          suspensionMap.push(placeMap[key]);
          disabledMap[placeMap[key]] = true;
        }
      }
      const suspensionPlace = (suspensionMap.length > 1 ? 'selection' : suspensionMap[0]);

      this.quickbetNotificationService.saveErrorMessage(
        this.filtersService.getComplexTranslation('quickbet.singleDisabled', '%1', suspensionPlace),
        'warning',
        'bet-status'
      );
    }

    this.quickbetUpdateService.fillDisableMap(disabledMap);
    this.initOddsBoost();
    this.updateEachWayAvailable();
  }

  changeOddsFormat(): void {
    if (this.ycOddsValue) {
      this.selection.price = {
        ...this.selection.price,
        isPriceUp: false,
        isPriceChanged: false,
        isPriceDown: false
      };

      this.selection.oldOddsValue = this.ycOddsValue();
    }
  }

  ngOnDestroy(): void {
    this.pubsub.unsubscribe(this.QB_SELECTION_NAME);
    this.pubsub.unsubscribe(this.selection.eventId);
    this.windowRef.nativeWindow.removeEventListener('online', this.onlineListener);
    this.windowRef.nativeWindow.removeEventListener('offline', this.offlineListener);
    this.countDownTimer && this.countDownTimer.stop && this.countDownTimer.stop();
    this.freebetsSubscription && this.freebetsSubscription.unsubscribe();
    this.betPackSubscription && this.betPackSubscription.unsubscribe();
    this.fanzoneSubscription && this.fanzoneSubscription.unsubscribe();
    this.windowRef.nativeWindow.clearTimeout(this.notifyTimeout);
  }

  placeBetFnHandler(): void {
    this.hasBeenReloaded && this.placeBetFn.emit();
  }

  iniTimer(): void {
    this.pubsub.subscribe(this.QB_SELECTION_NAME,
      this.pubsub.API.QUICKBET_COUNTDOWN_TIMER, time => {
        this.countDownTimer = this.timeService.countDownTimer(time);
      });
  }

  closeFnHandler(): void {
    this.closeFn.emit();
  }
  addToBetslipFnHandler(): void {
    this.addToBetslipFn.emit();
  }
  openQuickDepositFnHandler(): void {
    this.openQuickDepositFn.emit();
  }

  priceTypeChange(event: { output: string, value: string }): void {
    this.selection.isLP = event.value === 'LP';
    this.onStakeChange();
  }

  /**
   * Handler for stake model change.
   */
  onStakeChange(): void {
    this.selection.onStakeChange();
    this.selection.stake = this.selection.stake?.replace(",",".");
    this.quickbetDepositService.update(this.selection.stake, this.selection.isEachWay);

    if (this.quickbetService.selectionData) {
      this.quickbetService.saveQBStateInStorage({
        userStake: this.selection.stake,
        userEachWay: this.selection.isEachWay,
        isLP: this.selection.isLP,
        freebet: this.selection.freebet,
        isBoostActive: this.selection.isBoostActive,
        isLuckyDip:this.isLuckyDip
      });
    }

    this.handleOddsBoostSP();
    this.isMaxStakeExceeded();

    // GA tracking for free bet each way signposting
    if (this.selectedFreeBet && !this.selection.hasSP && this.selection.isLP){
      this.setFreeBetGtmData(this.selection);
    }

    // GA tracking for each way checkbox
    if (this.selection && this.selection.categoryId === '21' && !this.eachWayGaTraking) {
      this.gaTrackingOnEachWayCheckBox(this.selection);
    }
    this.disableEachWayTooltip = false;
    this.cdr.detectChanges();
  }

  onFreebetChange(event: ILazyComponentOutput): void {
    if (event.output === 'selectedChange') {
      const cat = event.value?.freebetOfferCategories?.freebetOfferCategory;
      this.selectedFreeBet = event.value;
      //User enters stack value before opting Free bet then stack value will be removed after opting Free Bet,
      event.value && (this.selection.stake = null);
      this.setFreebet(event.value, cat);
      this.handleOddsBoostFreeBet();
      this.onStakeChange();
      this.quickbetDepositService.update(this.selection.stake, this.selection.isEachWay);
    }
  }

  /**
   * Set frebet model
   * @param {string} freebetValue
   */
  setFreebet(freebetValue: IFreebetToken, freebetCat?: string): void {
    const list = this.freeBetsFactory.isBetPack(freebetCat) ? this.betPackList :this.freeBetsFactory.isFanzone(freebetCat)? this.fanzoneList : this.freebetsList;
    const freebetObj: IFreebetToken = _.find(list, freebet => freebet.freebetTokenId  === freebetValue?.freebetTokenId);
    const value = freebetObj && freebetObj.value && freebetObj.value.match(/[0-9.]/g).join('');

    this.selection.freebetValue = parseFloat(value) || 0;
    this.selection.freebet = freebetObj;
    this.selection.freeBetOfferCategory = freebetCat;
    this.selection.onStakeChange();
  }

  /**
   * checks if spinner on quick deposit button should be displayed
   */
  showSpinnerOnQuickDeposit(): boolean {
    return this.isIFrameLoadingInProgress() || this.placeBetPending.state;
  }

  /**
   * Check if can click the button
   * @returns {boolean}
   */
  isSelectionDisabled(): boolean {
    return !this.selection.stake || this.selection.disabled || this.placeBetPending.state
      || this.isIFrameLoadingInProgress();
  }

  /**
   * Used in view to check if stake is typed
   * @returns {boolean}
   */
  isMakeQuickDeposit(): boolean {
    if (this.placeBetPending.state) {
      return false;
    }
    return this.user.status && (!!this.quickDeposit.neededAmountForPlaceBet ||
      (!Number(this.user.sportBalance) && !this.selection.freebetValue));
  }

  /**
   * Used in view to check if stake is typed
   * @returns {boolean}
   */
  isInputFilled(): boolean {
    return !_.isNaN(parseFloat(this.selection.stake));
  }

  /**
   * Show spinner when place bet process is in progress
   * @returns {boolean}
   */
  showPendingSpinner(): boolean {
    this.iniTimer();
    return this.placeBetPending.state;
  }

  /**
   * Filter outcome names
   * @param {string} name
   * @returns {string}
   */
  filterPlayerName(name: string): string {
    return name && this.filtersService.filterPlayerName(name);
  }

  /**
   * Filter market names
   * @param {string} name
   * @returns {string}
   */
  filterAddScore(selection: any) {
   if (selection && (selection.categoryId === '21' || selection.categoryName === 'HORSE_RACING')) {
      const checkMarketName = this.filtersService.filterAddScore(selection.marketName, selection.outcomeName);
      return checkMarketName === 'Win or Each Way' ? 'To Win' : checkMarketName;
    }
    else {
      return this.filtersService.filterAddScore(selection.marketName, selection.outcomeName);
    }
  }

  onBoostClick(): void {
    if (this.placeBetPending.state) {
      return;
    }

    if (!this.selection.isLP) {
      this.commandService.execute(this.commandService.API.ODDS_BOOST_SHOW_SP_DIALOG);
      return;
    }

    if (this.selection.freebet) {
      this.commandService.execute(this.commandService.API.ODDS_BOOST_SHOW_FB_DIALOG, [false, 'quickbet'] );
      return;
    }

    if (this.selection.reboost) {
      this.reboostSelection();
    } else {
      const isActive = !this.selection.isBoostActive;
      this.pubsub.publish(this.pubsub.API.ODDS_BOOST_CHANGE, isActive);
      this.pubsub.publish(this.pubsub.API.ODDS_BOOST_SEND_GTM, { origin: 'quickbet', state: isActive });
    }
  }
  
  onQuickStakeSelect(value: string): void {
    const intVal = Number(value)
    const intStake = parseFloat(this.selection.stake) || 0;
    const locationEvent={
      betslip_stakes:'betslip stakes',
      byb_stakes:'build your bet stakes',
      fiveaside_stakes:'fiveaside stakes',
      totepool_stakes:'totepool stakes',
      global_stakes:'global stakes',
      quickbet_stakes:'quickbet stakes'
    };
    this.selection.stake = (intStake + intVal).toFixed(2);
    this.cdr.detectChanges();
    this.onStakeChange();
    this.pubsub.publish(this.pubsub.API.QB_QUICKSTAKE_PRESSED, [this.selection.stake]);
    this.pubsub.publish(this.pubsub.API.QB_QUICKSTAKE_PRESSED_DIGIT_KEYBOARD, [this.selection.stake]);
    this.gtmService.push('trackEvent', {
      event: 'trackEvent',
      eventCategory: 'quickbet',
      eventAction: 'click',
      eventLabel:this.qbDigitKeyboard['isKeyboardShown']?'keypad predefined stake': 'predefined stake',
      locationEvent:locationEvent[this.betslipType],
      positionEvent:this.isBrandLadbrokes?'top':'bottom',
      eventDetails:value
    });
  }

  onKeyboardToggle(status: boolean): void {
    this.quickStakeVisible = status;
    this.pubsub.publish(this.pubsub.API.LUCKY_DIP_KEYPAD_PRESSED, status);
    this.cdr.detectChanges();
  }

  /**
   * @param  {boolean} newItem
   * @returns void
   */
  addItem(newItem: boolean): void {
    this.maxPayedOut = newItem;
  }

  /**
   * sends the Selected Contest information to betReceipt Service
   * @param event will contain all the details related to a particular event
   * @returns void
   */
   public handleSelectedContestChangeOutput(event: ILazyComponentOutput): void {
    if (event.output === SELECTED_CONTEST_CHANGE) {
        this.fiveASideContestSelectionService.defaultSelectedContest = event.value.id;
        this.contestSelectionGATrack(event);
    }
  }

  /**
   * ContestSelection Button GA Tracking
   * @returns void
   */
   contestSelectionGATrack(event: ILazyComponentOutput): void {
    this.gtmService.push('contestSelectionEventTrack', {
      eventLabel: event.value.name,
      eventID: event.value.id
    });
  }

  get canBoostSelection(): boolean {
    return (
      !this.isLuckyDip && 
      this.isBoostEnabled &&
      !this.selection.disabled &&
      !this.selection.hasSP &&
      !!this.selection.oddsBoost

    );
  }
set canBoostSelection(value:boolean){}
  get selectionAmountClasses(): {[key: string]: boolean} {
    return {'filled-input': this.isInputFilled(), [`currency-${this.selection.currency}`]: true};
  }
  set selectionAmountClasses(value:{[key: string]: boolean}){}
  /**
   * Check if user is logged in
   * @returns {boolean}
   */
  get isUserLoggedIn(): boolean {
    return this.user.status;
  }
  set isUserLoggedIn(value:boolean){}
  /**
   * Disable Place Bet button when stake or freebet value are empty or event is suspended
   * @returns {boolean}
   */
  get disablePlaceBet(): boolean {
    return (!parseFloat(this.selection.stake) && !this.selection.freebet) || this.selection.disabled;
  }
  set disablePlaceBet(value:boolean){}
  get getPlaceBetText(): string {
    const placeBetText = this.getPlaceBetCTAText();
   
      return this.selection.price && this.selection.price.isPriceChanged && !this.showPendingSpinner()
      || this.quickbetUpdateService.isHandicapChanged(this.selection) ?
        'quickbet.buttons.acceptPlaceBet' :
        placeBetText;

  }
  set getPlaceBetText(value:string){}

  /**
   * Retrieves freebets list.
   * @protected
   */
  protected getFreebetsList(): void {
    // Free bets should not be visible for anonymous user or for Connect app
    const freeBets = this.locale.getString('bs.freeBets');
    const betPacks = this.locale.getString('bs.betPacks');
    const fanzone = this.locale.getString('bs.fanZone');

    this.freebetsList = this.user.status ? this.mapFreebets(this.selection): [];
    this.freebetsList.sort((a, b) => Number(a.freebetTokenValue) -  Number(b.freebetTokenValue));
    const freeBetBetPackList =   this.freebetsList.reduce((pv, cv) => {
      const key = this.freeBetsFactory.isBetPack(cv.freebetOfferCategories?.freebetOfferCategory) ? betPacks : this.freeBetsFactory.isFanzone(cv.freebetOfferCategories?.freebetOfferCategory) ? fanzone : freeBets;
      if (!this.selection.isYourCallBet) {
        cv.expireAt = new Date(cv.expiry);
        cv.name = cv.offerName;
        cv.freebetTokenId = cv.id;
      }
      else{
        cv.value = cv.freebetTokenValue;
      }
      pv[key] = [...pv[key] || [], cv];
      return pv;
   }, {});

   this.freebetsList = !this.isLuckyDip && freeBetBetPackList[freeBets] || [];
   this.betPackList= freeBetBetPackList[betPacks] || [];
   this.fanzoneList = freeBetBetPackList[fanzone] || [];
  }

  /**
   * checks if iframe loading is in progress
   */
  private isIFrameLoadingInProgress(): boolean {
    return !this.showIFrame && this.quickDepositFormExpanded;
  }

  private initOddsBoost(): void {
    if (!this.user.status) { return; }

    this.cmsService.getOddsBoost().pipe(
      map(config => config.enabled),
      mergeMap(enabled => {
        if (!enabled) {
          return observableOf([false, false]);
        } else {
          return observableFrom(
            this.commandService.executeAsync(this.commandService.API.GET_ODDS_BOOST_ACTIVE_FROM_STORAGE)
          ).pipe(map(active => [enabled, active]));
        }
      }))
      .subscribe((data: [boolean, boolean]) => {
        [this.isBoostEnabled, this.selection.isBoostActive] = data;

        if (!this.isBoostEnabled) {
          return;
        }

        this.selection.onStakeChange();
        if (this.selection.oddsBoost) {
          this.commandService.execute(this.commandService.API.ODDS_BOOST_SET_MAX_VAL, [this.selection.oddsBoost.betBoostMaxStake]);
        }

        if (this.canBoostSelection) {
          this.boostOldPrice = this.commandService.execute(this.commandService.API.ODDS_BOOST_OLD_QB_PRICE, [this.selection]);
          this.boostNewPrice = this.commandService.execute(this.commandService.API.ODDS_BOOST_NEW_QB_PRICE, [this.selection]);
        }

        this.pubsub.subscribe(this.QB_SELECTION_NAME, this.pubsub.API.ODDS_BOOST_CHANGE, (active: boolean) => {
          this.selection.isBoostActive = active;
          this.selection.reboost = false;
          this.eachWayGaTraking = true;
          if (this.selection.isBoostActive && this.selection.price && this.selection.price.isPriceChanged) {
            this.reboostSelection();
          }
          if (!this.selection.disabled) {
            this.onStakeChange();
          }
        });

        this.pubsub.subscribe(this.QB_SELECTION_NAME, this.pubsub.API.ODDS_BOOST_UNSET_FREEBETS, () => {
          this.selectedFreeBet = null;
          this.setFreebet(null);
        });

        if(this.canBoostSelection && !this.sessionStorageService.get("betPlaced")) {
            this.firstBetBoostEmit.emit({step:'placeYourBet', tutorialEnabled: true, type: 'boost'});
        }
      });
  }

  private isMaxStakeExceeded(): void {
    if (this.selection.isBoostActive) {
      const stake = +this.selection.stake;
      const totalStake = this.selection.isEachWay ? stake * 2 : stake;
      this.commandService.execute(this.commandService.API.ODDS_BOOST_MAX_STAKE_EXCEEDED, [totalStake]);
    }
  }

  private handleOddsBoostSP(): void {
    if (
      this.isBoostEnabled && this.selection.isBoostActive && !this.selection.isLP
    ) {
      this.commandService.execute(this.commandService.API.ODDS_BOOST_SHOW_SP_DIALOG);
    }
  }

  private handleOddsBoostFreeBet(): void {
    if (
      this.isBoostEnabled && this.selection.isBoostActive && this.selection.freebet
    ) {
      this.commandService.execute(this.commandService.API.ODDS_BOOST_SHOW_FB_DIALOG, [true, 'quickbet'] );
    }
  }

  /**
   * Form list of freebets which are available for selection
   * @param {IQuickbetSelectionModel} selection
   * @return {Array}
   * @private
   */
  private mapFreebets(selection: IQuickbetSelectionModel): IFreebetToken[] {
    if (!this.selection.isYourCallBet) {
      return selection.freebetList || [];
    }
    const freeBetsState = this.freeBetsFactory.getFreeBetsState();
    return _.filter([...freeBetsState.data, ...freeBetsState.betTokens, ...freeBetsState.fanZone], freebet => {
      const tokenPossibleBets = freebet.tokenPossibleBets ||
        (freebet.tokenPossibleBet ? [freebet.tokenPossibleBet] : []);

      freebet.name = freebet.freebetOfferName;
      freebet.value = freebet.freebetTokenValue;
      //Date format issue in iOS
      freebet.expireAt = new Date(freebet.freebetTokenExpiryDate.replace(/-/g, '/'));
      return this.isQualifiedFreebet(selection, tokenPossibleBets);
    });
  }

  /**
   * Checks if freebet has different redemptions and at least one of them matches selection channel.
   * @param {Object} selection
   * @param {Array} tokenPossibleBets
   * @return {boolean}
   * @private
   */
  private isQualifiedFreebet(selection: IQuickbetSelectionModel, tokenPossibleBets: ITokenPossibleBet[]): boolean {
    return _.some(tokenPossibleBets, tokenPossibleBet => {
      if (!(!selection['channel'] && tokenPossibleBet.name === this.getFreeBetName)) {
        return Number({
          SELECTION: selection.outcomeId,
          MARKET: selection.marketId,
          EVENT: selection.eventId,
          TYPE: selection.typeId,
          CLASS: selection.classId,
          CATEGORY: selection.categoryId,
          ANY: tokenPossibleBet.betId
        }[tokenPossibleBet.betLevel]) === Number(tokenPossibleBet.betId);
      }
    });
  }

  private addEventListeners(): void {
    this.windowRef.nativeWindow.addEventListener('online', this.onlineListener);
    this.windowRef.nativeWindow.addEventListener('offline', this.offlineListener);
  }

  private onlineListener(): void {
    this.windowRef.nativeWindow.setTimeout(() => {
      this.hasBeenReloaded = true;
    }, this.LOCK_PLACE_BET_TIMEOUT);
  }

  private offlineListener(): void {
    this.hasBeenReloaded = false;
  }

  private reboostSelection() {
    this.pubsub.publish(this.pubsub.API.REUSE_QUICKBET_SELECTION, this.selection.requestData);
    this.pubsub.publish(this.pubsub.API.ODDS_BOOST_SEND_GTM, { origin: 'quickbet', state: true });
  }

  /**
   * @returns IBppRequest
   */
  private formBodyParamforBuildBet(): IBppRequest {

    this.body = {
      'channelRef': {
          'id': 'I'
      },
      'leg': [
          {
              'documentId': 1,
              'sportsLeg': {
                  'price': {
                      'num': this.selection.price && this.selection.price.priceNum,
                      'den': this.selection.price && this.selection.price.priceDen,
                      'priceTypeRef': {
                          'id': ''
                      }
                  },
                  'legPart': [
                      {
                          'outcomeRef': {
                              'id': this.selection.outcomeId
                          }
                      }
                  ],
                  'winPlaceRef': {
                      'id': ''
                  }
              }
          }
      ],
      'legGroup': [
          {
              'legRef': [
                  {
                      'documentId': 1
                  }
              ]
          }
      ],
      'returnOffers': 'N'
  } as IBppRequest;
    return this.body;
  }
  /**
   * @returns string
   */
  private buildBetCall(): void  {
    this.isUserLogIn = this.user.bppToken ? true : false;
    !this.isLuckyDip && this.bppProviderService.quickBet(this.body, this.isUserLogIn).subscribe((res) => {
      this.selection.markets && this.selection.markets.forEach(element => {
        if (element.name === "Win or Each Way" || element.name === "Outright") {
          this.isWinorEachWay = true;
          element.eachWayPlaces = res['outcomeDetails'][0].eachWayPlaces;
          element.previousOfferedPlaces = res['outcomeDetails'][0].previousOfferedPlaces;
          if (this.selection.markets[0].hasOwnProperty('eachWayPlaces') && this.selection.markets[0].hasOwnProperty('previousOfferedPlaces') && this.selection.markets[0].eachWayPlaces && this.selection.markets[0].previousOfferedPlaces) {
            this.extraPlaceName = this.selection.markets[0].eachWayPlaces + ' ' + 'places instead of' + ' ' + this.selection.markets[0].previousOfferedPlaces;
          }
        }
      });
      this.cdr.detectChanges();
    });
  }
  /**
   * 
   * updates the is isEachWayAvailable to dynamically display each way checkbox
   */
  private updateEachWayAvailable(): void {
    this.pubsub.subscribe(this.QB_SELECTION_NAME, this.pubsub.API.EACHWAY_FLAG_UPDATED, (eachWayAvailable: string) => {
      this.selection.isEachWay = false;
      this.selection.isEachWayAvailable = eachWayAvailable === 'Y';
    });
  }

  /**
   * sets GA tracking for eachway check box changes
   * @param selection: betslipstake
   */
   private setFreeBetGtmData(selection: any): void {
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'promotions',
      'component.LabelEvent': 'each way free bet',
      'component.ActionEvent': 'click',
      'component.PositionEvent': selection.isEachWay ? 'checked' : 'unchecked',
      'component.LocationEvent': 'quick bet',
      'component.EventDetails': selection.eventName,
      'component.URLclicked': 'not applicable',
      'sportID': selection.categoryId
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

  /**
   * To Show Tooltip for eachway checkbox
   * @param eachWay: betslipstake
   */
  public showEachWay(eachWay: any): void {
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      if (config.eachWayTooltip && config.eachWayTooltip.Enable) {
        this.delay = config.eachWayTooltip.Delay;
        this.toolTipMessage = config.eachWayTooltip.Message;
        this.Tooltip_Enable = config.eachWayTooltip.Enable;
      }
    });
    this.toolTipArgs = {
      eachWayTooltip: this.toolTipMessage
    };
    if (this.Tooltip_Enable) {
      if (eachWay && (eachWay.categoryId === '21' || eachWay.categoryName === 'HORSE_RACING') && !eachWay.disabled) {
        if (this.user.username && !(this.storageService.get(this.EachWay_Tooltip) && this.user.username === this.storageService.get(this.EachWay_Tooltip).user)) {
          this.storageService.set(this.EachWay_Tooltip, { user: this.user.username, displayed: true });
          this.disableEachWayTooltip = true;
          this.eachWayGaTracking = true;
          this.notifyTimeout = this.windowRef.nativeWindow.setTimeout(() => {
            this.disableEachWayTooltip = false;
          }, this.delay * quickbetConstants.IN_MS);
        }
      }
    }
  }

  /**
   * sets GA tracking for eachway check box
   * @param selection: betslipstake
   */
  public gaTrackingOnEachWayCheckBox(eachWay) {
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'betslip',
      'component.LabelEvent': eachWay.categoryName,
      'component.ActionEvent': eachWay.isEachWay ? 'checked' : 'unchecked',
      'component.PositionEvent': eachWay.outcomeName,
      'component.LocationEvent': 'quickbet',
      'component.EventDetails': (this.eachWayGaTracking && (eachWay.categoryName === "Horse Racing")) ? 'each way alert' : 'each way regular',
      'component.URLclicked': 'not applicable',
      'sportID': eachWay.sportID
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

  /**
   * Check if extra places offered for Horse racing and Golf to shown extra place sign posting
   * @returns boolean
   */
  extraPlaceCheck(): boolean {
    const extraPlaceOfferCheck = this.selection && this.selection.markets && this.selection.markets.length && this.selection.markets[0].hasOwnProperty('drilldownTagNames') && this.selection.markets[0].drilldownTagNames && this.selection.markets[0].drilldownTagNames.includes('MKTFLAG_EPR') && (this.selection.markets[0].name === "Win or Each Way" || this.selection.markets[0].name === "Outright");
    if (extraPlaceOfferCheck) {
      if (this.sessionStorageService.get('ExtraplaceSelection')) {
        this.extraPlaceData = this.sessionStorageService.get('ExtraplaceSelection');
      }
      this.extraPlaceData && this.selection.markets && this.extraPlaceData.markets && this.extraPlaceData.markets.forEach(element => {
        if (element.id === this.selection.markets[0].id) {
          this.selection.markets[0].eachWayPlaces = element.eachWayPlaces;
          this.selection.markets[0].previousOfferedPlaces =  element.referenceEachWayTerms && element.referenceEachWayTerms.places;
        }
      });
      if (this.extraPlaceData && this.selection.markets[0].hasOwnProperty('eachWayPlaces') && this.selection.markets[0].hasOwnProperty('previousOfferedPlaces')) {
        this.extraPlaceName =  this.selection.markets[0].eachWayPlaces + ' ' + 'places instead of' + ' ' + this.selection.markets[0].previousOfferedPlaces;
      }
    }
    return extraPlaceOfferCheck;
  }
/**
 * Get CMS configured place bet cta text for ld only
 * @returns {string}  */ 
  private getPlaceBetCTAText():string {
    return this.isLuckyDip && this.luckyDipCmsData && this.luckyDipCmsData.placebetCTAButton ?  this.luckyDipCmsData.placebetCTAButton :'quickbet.buttons.placeBet'
  }

  /**
 * Get CMS configured back btn cta text for ld only
 * @returns {string}  */ 
  getbackBtnCTAText():string {
    return this.isLuckyDip && this.luckyDipCmsData && this.luckyDipCmsData.backCTAButton ?  this.luckyDipCmsData.backCTAButton :'quickbet.buttons.back';
  }
}

