import {
  Component,
  Input,
  Output,
  OnInit,
  OnDestroy,
  EventEmitter,
  AfterContentInit,
  ViewEncapsulation,
  ChangeDetectorRef
} from '@angular/core';
import { Subscription } from 'rxjs';
import { Router } from '@angular/router';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { UserService } from '@core/services/user/user.service';
import { DeviceService } from '@core/services/device/device.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { QuickbetService } from '@app/quickbet/services/quickbetService/quickbet.service';
import { QuickbetDepositService } from '@quickbetModule/services/quickbetDepositService/quickbet-deposit.service';
import { QuickbetDataProviderService } from '@app/core/services/quickbetDataProviderService/quickbet-data-provider.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';

import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { IQuickbetReceiptDetailsModel, IYCBetReceiptModel } from '@app/quickbet/models/quickbet-receipt.model';
import { QuickbetNotificationService } from '@app/quickbet/services/quickbetNotificationService/quickbet-notification.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { ISuspendedOutcomeError } from '@betslip/models/suspended-outcome-error.model';
import { QuickbetUpdateService } from '@app/quickbet/services/quickbetUpdateService/quickbet-update.service';
import { ArcUserService } from '@app/lazy-modules/arcUser/service/arcUser.service';
import { ServiceClosureService } from '@lazy-modules/serviceClosure/service-closure.service';
import { YourcallMarketsService } from '@app/yourCall/services/yourCallMarketsService/yourcall-markets.service';
import { NativeBridgeService } from '@app/core/services/nativeBridge/native-bridge.service';
import environment from '@environment/oxygenEnvConfig';
import { IConstant } from '@core/services/models/constant.model';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { UserService as User } from '@core/services/user/user.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { ILuckyDipFieldsConfig } from '@app/lazy-modules/luckyDip/models/luckyDip';
import { LUCKY_DIP_CONSTANTS } from '@app/lazy-modules/luckyDip/constants/lucky-dip-constants';
import { QuickDepositIframeService } from '@app/quick-deposit/services/quick-deposit-iframe.service';

@Component({
  selector: 'quickbet-panel',
  templateUrl: 'quickbet-panel.component.html',
  styleUrls: ['quickbet-panel.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class QuickbetPanelComponent implements OnInit, OnDestroy, AfterContentInit {
  @Input() title: string;
  @Input() showCloseIcon: boolean;
  @Input() isFiveASideBet: boolean;
  @Input() selection: IQuickbetSelectionModel;
  @Input() leftBtnLocale?: string;
  @Input() bodyClass: string;
  @Input() ycOddsValue?: Function;
  @Input() isLuckyDip?: boolean;
  @Input() luckyDipCmsData?: ILuckyDipFieldsConfig;
  @Input() luckyDipMarketName?: string;
  @Input() isWSdisabled?: boolean;
  @Input() betslipType: string;
  @Output() readonly placeBetFn: EventEmitter<void> = new EventEmitter();
  @Output() readonly reuseSelectionFn?: EventEmitter<void> = new EventEmitter();
  @Output() readonly closeFn: EventEmitter<boolean> = new EventEmitter();
  @Output() readonly addToBetslipFn: EventEmitter<void> = new EventEmitter();
  @Output() readonly quickDepositFormExpandedFn: EventEmitter<boolean> = new EventEmitter();
  quickDepositFormExpanded: boolean;
  viewState: string;
  initialTitle: string;
  placeBetPending: { state: boolean };
  betReceipt: IQuickbetReceiptDetailsModel;
  loginAndPlaceBets: boolean;
  sysConfig: ISystemConfig;
  slideUpAnimation: boolean;
  showIFrame = false;
  showPriceChangeMessage = false;
  showSuspendedNotification = false;
  iframeLoaded = false;
  placeSuspendedErr: ISuspendedOutcomeError = { multipleWithDisableSingle: false, disableBet: false, msg: '' };
  priceChangeText: string;
  estimatedReturnAfterPriceChange: number;

  protected QB_PANEL_NAME = 'QuickbetPanel';

  private eventSuspensionSubscription: Subscription;
  private priceChangeSubscription: Subscription;

  protected QB_PANEL_CLOSE = 'QuickBetPanelClose';

  private BODY_CLASS: string;
  private quickbeReceiptSubscriber: Subscription;
  private windowScrollY: number;
  private werePopupsShown = false;
  onBoardingData;

  constructor(protected rendererService: RendererService,
    protected pubsub: PubSubService,
    protected userService: UserService,
    protected locale: LocaleService,
    protected quickbetDepositService: QuickbetDepositService,
    public device: DeviceService,
    protected infoDialog: InfoDialogService,
    protected quickbetService: QuickbetService,
    protected quickbetDataProviderService: QuickbetDataProviderService,
    protected quickbetNotificationService: QuickbetNotificationService,
    protected cmsService: CmsService,
    protected windowRefService: WindowRefService,
    protected domToolsService: DomToolsService,
    protected router: Router,
    protected quickbetUpdateService: QuickbetUpdateService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected arcUserService: ArcUserService,
    protected nativeBridgeService: NativeBridgeService,
    public serviceClosureService: ServiceClosureService,
    public yourCallMarketService: YourcallMarketsService,
    public dialogService: DialogService,
    protected sessionStorageService: SessionStorageService,
    protected user: User,
    protected quickDepositIframeService: QuickDepositIframeService
  ) {
    this.viewState = 'initial';
    this.placeBetPending = { state: false };
    this.betReceipt = null;
    this.loginAndPlaceBets = false;
    this.handleFootballAlerts = this.handleFootballAlerts.bind(this);
  }

  ngOnInit(): void {
    this.initialTitle = this.title;
    this.BODY_CLASS = this.bodyClass || 'quickbet-opened';

    if (!this.sessionStorageService.get('betPlaced')) {
      const storedOnboardingData = this.sessionStorageService.get('firstBetTutorial');
      this.onBoardingData = { step: 'placeYourBet', tutorialEnabled: storedOnboardingData && storedOnboardingData.firstBetAvailable, type: 'defaultContent' };
    }

    this.pubsub.subscribe(this.QB_PANEL_NAME, this.pubsub.API.MY_BET_PLACED_LD, (placedBet: any) => {
      this.isLuckyDip && this.setReceiptStateforLd();
    });
    // close quickbet on selection of price button in racing post tip shown
    this.pubsub.subscribe(this.QB_PANEL_CLOSE, this.pubsub.API.QUICKBET_PANEL_CLOSE, () => this.closePanel());

    // Allow place bet on 'login and place bets' action

    this.pubsub.subscribe(this.QB_PANEL_NAME, [this.pubsub.API.SUCCESSFUL_LOGIN, this.pubsub.API.SESSION_LOGOUT], placeBet => {
      if (this.isState('receipt') || this.userService.isInShopUser()) {
        this.closePanel();
        return;
      }

      if (!this.werePopupsShown) {
        this.loginAndPlaceBets = true;
        this.selection.updateCurrency();
        this.checkArcUserOnLogIn();
        this.quickbetDepositService.init(true);
      } else {
        this.goToState('initial');
        this.quickbetNotificationService.clear();
        this.reuseSelection();
      }
    });

    // stop placing bet if notification popup is displayed after used has logged in
    this.pubsub.subscribe(this.QB_PANEL_NAME, this.pubsub.API.USER_INTERACTION_REQUIRED, () => {
      this.werePopupsShown = true;
      this.loginAndPlaceBets = false;
      // update quick deposit model to show insufficient funds message
      this.checkArcNotify();
    });

    // Place bets on 'login and place bets' action after all popup will be shown
    this.pubsub.subscribe(this.QB_PANEL_NAME, this.pubsub.API.LOGIN_POPUPS_END, () => {
      this.werePopupsShown = false;
      if (this.loginAndPlaceBets) {
        this.loginAndPlaceBets = false;
        this.pubsub.subscribe(this.QB_PANEL_NAME, this.pubsub.API.PAYMENT_ACCOUNTS_PASSED, () => {
          this.checkArcUser();
        });
        this.quickbetDepositService.init(true);
      }
    });

    this.pubsub.subscribe(this.QB_PANEL_NAME, this.pubsub.API.UPDATE_QUICKBET_NOTIFICATION, message => {
      if (message && message.msg) {
        this.checkArcError(message);
      }
    });

    this.pubsub.subscribe(this.QB_PANEL_NAME, this.pubsub.API.QUICKBET_CARD_CHANGE, () => {
      this.quickbetNotificationService.clear();

      if (this.selection && this.selection.stake) {
        this.quickbetDepositService.update(this.selection.stake, this.selection.isEachWay);
      }
    });

    this.pubsub.subscribe(this.QB_PANEL_NAME, `SELECTION_PRICE_UPDATE_${this.selection.outcomeId}`, () => {
      this.changeDetectorRef.detectChanges();
    });

    this.toggleBodyScroll(true);
    // Quickbet Receipt Subscriber(get receipt data from quickbet/yourcall components)
    this.placeBetListener();

    if (this.quickbetService.acceptChangedBoost()) {
      this.selection.isBoostActive = true;
      this.placeBet();
    }

    this.cmsService.getSystemConfig().subscribe((config) => this.sysConfig = config);

    // Slide up(animation) quickbet panel
    this.windowRefService.nativeWindow.setTimeout(() => {
      this.slideUpAnimation = true;
      this.changeDetectorRef.detectChanges();
    }, 0);

    this.eventSuspensionSubscription = this.quickbetUpdateService.getEventSuspension().subscribe((status: ISuspendedOutcomeError) => {
      this.placeSuspendedErr = status;
      this.showSuspendedNotification = status.disableBet;
      this.showPriceChangeMessage = false;
    });
    this.priceChangeSubscription = this.quickbetUpdateService.getPriceChange().subscribe((msg: string) => {
      if (!this.showSuspendedNotification) {
        this.selection.onStakeChange();
        this.estimatedReturnAfterPriceChange = parseFloat(this.selection.potentialPayout);
        this.showPriceChangeMessage = true;
        this.priceChangeText = msg;
      }
    });

    this.setupModificationWatchDogForLogInAndQuickBetPending();
    this.windowRefService.document.addEventListener('eventAlertsEnabled', this.handleFootballAlerts);
  }

  ngOnDestroy(): void {
    this.toggleBodyScroll(false);
    this.pubsub.unsubscribe(this.QB_PANEL_NAME);

    // remove from storage data if not a qucikbet
    if (!this.isQuickbet()) {
      this.quickbetService.removeQBStateFromStorage();
    }
    this.eventSuspensionSubscription.unsubscribe();
    this.priceChangeSubscription.unsubscribe();
    this.pubsub.unsubscribe(this.QB_PANEL_CLOSE);
    this.windowRefService.document.removeEventListener('eventAlertsEnabled', this.handleFootballAlerts);
  }

  ngAfterContentInit(): void {
    this.pubsub.publishSync(this.pubsub.API.AFTER_PANEL_RENDER);
  }

  /**
   * Required to check weather is betslip or quickbet
   * @return {boolean}
   */
  isQuickbet(): boolean {
    return this.BODY_CLASS === 'quickbet-opened';
  }

  /**
   * Checks if passed state is active.
   * @param {string} state
   * @return {boolean}
   */
  isState(state: string): boolean {
    if (this.selection && !this.selection.error && this.viewState === 'receipt')
      this.yourCallMarketService.removeAllMarkets = true;
    return this.selection && !this.selection.error && this.viewState === state;
  }

  /**
   * Changes active state
   * @param {string} state
   */
  goToState(state: string): void {
    this.viewState = state;
  }

  /**
   * Closes panel.
   */
  closePanel(event?: Event): void {
    !!event && event.stopPropagation();
    this.quickbetDepositService.clearQuickDepositModel();
    this.pubsub.publishSync(this.pubsub.API.ODDS_BOOST_CHANGE);
    this.closeFnHandler();
    this.quickbetNotificationService.clear();
    this.closeAnimationDialog();
    if (this.isState('receipt') && this.sessionStorageService.get('betPlaced')) {
      const currentType = this.selection.markets.find(market => market.isCashoutAvailable === 'Y') ? 'cashOut' : 'defaultContent';
      this.pubsub.publish(this.pubsub.API.FIRST_BET_PLACEMENT_TUTORIAL,
        { step: 'betDetails', tutorialEnabled: true, type: currentType });
    }
  } 

  firstBetBoostEmit(event) {
    if (!this.sessionStorageService.get('betPlaced')) {
      this.onBoardingData = event;
    }
  }
  /**
   * Places bet from active selection.
   */
  placeBet(): void {
    if (this.serviceClosureService.userServiceClosureOrPlayBreak) {
      this.selection.stake = null;
      return;
    }
    const bet = this.selection.formatBet(),
      quickDepositModel = this.quickbetDepositService.quickDepositModel;
    this.quickbetDepositService.update(this.selection.stake);

    if (!this.device.isOnline()) {
      this.infoDialog.openConnectionLostPopup();
    } else if (!this.userService.status) {
      this.pubsub.publish(this.pubsub.API.OPEN_LOGIN_DIALOG, {
        placeBet: 'quickbet',
        moduleName: 'quickbet'
      });
    } else {
      if (!quickDepositModel.neededAmountForPlaceBet && !this.placeBetPending.state && this.userService.bppToken) {
        // Show Place bet spinner
        this.placeBetPending.state = true;

        if (this.selection.reboost) {
          this.quickbetService.activateReboost();
          this.selection.reboost = false;
          this.reuseSelection();
          return;
        }

        this.placeBetFnHandler();
        this.quickbetDataProviderService.quickbetPlaceBetListener.next(bet);
      }
    }
  }

  /**
   * Reuse selection handler.
   */
  reuseSelection(): void {
    if (this.isQuickbet()) {
      this.pubsub.publish(this.pubsub.API.REUSE_QUICKBET_SELECTION, this.selection.requestData);
      this.pubsub.publish(this.pubsub.API.ODDS_BOOST_CHANGE, this.selection.isBoostActive);
    } else {
      this.reuseSelectionFnHandler();
    }
  }

  placeBetFnHandler(): void {
    this.placeBetFn.emit();
  }

  closeFnHandler(): void {
    if (this.viewState === 'receipt' && !this.isQuickbet()) {
      this.closeFn.emit(this.isState('receipt'));
    } else if (this.isQuickbet()) {
      this.closeFn.emit(this.isState('receipt'));
      if (this.quickbetNotificationService.config.type && this.quickbetNotificationService.config.type === 'warning') {
        this.quickbetNotificationService.clear();
      }
    } else {
      this.reuseSelectionFnHandler();
    }
  }

  reuseSelectionFnHandler(): void {
    this.reuseSelectionFn.emit();
  }

  addToBetslipFnHandler(): void {
    if (this.serviceClosureService.userServiceClosureOrPlayBreak) {
      return;
    }
    if (!this.sessionStorageService.get('betPlaced')) {
      this.pubsub.publish(this.pubsub.API.FIRST_BET_PLACEMENT_TUTORIAL,
        { step: 'addSelection', tutorialEnabled: true, type: 'defaultContent' });
    }
    this.addToBetslipFn.emit();
  }

  /**
   * closes quick deposit window
   */
  onCloseQuickDepositWindow(): void {
    this.quickbetDepositService.update(this.selection.stake);
    this.showIFrame = false;
    this.quickDepositFormExpanded = false;
    this.showPriceChangeMessage = false;
    this.quickDepositFormExpandedFn.emit(false);
  }

  closeIFrame(): void {
    this.showIFrame = false;
    this.quickDepositFormExpanded = false;
    this.quickDepositFormExpandedFn.emit(false);
    this.placeBet();
  }

  onOpenIframe(): void {
    this.showIFrame = true;
    this.iframeLoaded = true;
    this.showPriceChangeMessage = false;
  }

  getTotalStake(): number {
    return this.selection.isEachWay ? +this.selection.stake * 2 : +this.selection.stake;
  }

  onQuickDepositEvents({ output }): void {
    if (output === 'openIframeEmit') {
      this.onOpenIframe();
    } else if (output === 'closeWindow') {
      this.onCloseQuickDepositWindow();
    } else if (output === 'closeIframeEmit') {
      this.closeIFrame();
    }
  }

  /**
   * Subscribe on login dialog and login events to prevent QuickBet stake update
   * through QuickBetPanel - by setting _loginAndPlaceBets_ variable to true.
   */
  private setupModificationWatchDogForLogInAndQuickBetPending() {
    this.pubsub.subscribe(this.QB_PANEL_NAME, this.pubsub.API.SESSION_LOGIN, () => {
      this.loginAndPlaceBets = true;
    });
    this.pubsub.subscribe(this.QB_PANEL_NAME, this.pubsub.API.LOGIN_DIALOG_CLOSED, () => {
      if (this.userService.loginPending) {
        this.loginAndPlaceBets = true;
        this.pubsub.subscribe(this.QB_PANEL_NAME, this.pubsub.API.FAILED_LOGIN, () => {
          this.loginAndPlaceBets = false;
        });
      }
    });
  }

  private placeBetListener() {
    this.quickbeReceiptSubscriber = this.quickbetDataProviderService.quickbetReceiptListener
      .subscribe(betReceipt => {
        this.placeBetPending.state = false;
        if (_.isArray(betReceipt) && betReceipt[0].error) {
          console.warn('Error while placing quickbet', betReceipt[0].error);
          this.quickbetNotificationService.saveErrorMessageWithCode(betReceipt[0].error, 'warning', '', betReceipt[0].errorCode);
        } else {
          // Go to bet receipt state
          if (this.isQuickbet()) {
            this.betReceipt = _.isArray(betReceipt) && betReceipt.length && betReceipt[0];
            this.betReceipt.categoryId = this.selection.categoryId;
            this.title = this.locale.getString(`quickbet.betReceiptTitle`);
            if (!this.sessionStorageService.get('firstBetTutorial') && this.betReceipt.receipt.id) {
              this.sessionStorageService.set('firstBetTutorial', { user: this.user.username, firstBetAvailable: false });
              this.pubsub.publish(this.pubsub.API.FIRST_BET);
            }
            this.sessionStorageService.set('betPlaced', true);
            const storedOnboardingData = this.sessionStorageService.get('firstBetTutorial');
            const stepType = this.sysConfig.winAlerts && this.sysConfig.winAlerts.enabled && this.device.isWrapper ? 'winAlert' : 'defaultContent';
            this.onBoardingData = { step: 'betPlaced', tutorialEnabled: storedOnboardingData && storedOnboardingData.firstBetAvailable, type: stepType };
          } else {
            this.setYCBetReceiptProps(<IYCBetReceiptModel>betReceipt);
            this.title = this.locale.getString(`quickbet.${this.isFiveASideBet ? 'fiveASideBetreceipt' : 'yourCallBetreceipt'}`);
          }

          this.checkFootballAlerts();
          // Go to bet receipt state
          this.goToState('receipt');
          this.nativeBridgeService.betPlaceSuccessful(this.betReceipt.receipt.id, this.selection.categoryName, 'Single');
          this.quickbeReceiptSubscriber.unsubscribe();
        }
      });
  }

  /**
   * set the footballAlertsVisible property based on config
   */
  checkFootballAlerts(): void {
    const alertsEnabled = this.nativeBridgeService.hasOnEventAlertsClick() || this.nativeBridgeService.hasShowFootballAlerts();
    if (alertsEnabled && this.selection.categoryId === environment.CATEGORIES_DATA.footballId && !this.selection.isOutright) {
      (this.cmsService.getFeatureConfig('NativeConfig', false)).subscribe((data: ISystemConfig) => {
        if (data && (data.visibleNotificationIconsFootball || data.visibleNotificationIcons)) {
          const { value = '' } = data.visibleNotificationIconsFootball || data.visibleNotificationIcons;
          const isOSPermitted = this.checkDeviceOS(data.displayOnBetReceipt);
          if (isOSPermitted) {
            const allowedLeaguesList = typeof value === 'string' ? value.split(/\s*,\s*/) : [];
            this.betReceipt.footballAlertsVisible = allowedLeaguesList.includes(this.selection.typeName);
            this.betReceipt.footballAlertsVisible && this.nativeBridgeService.eventPageLoaded(this.selection.eventId.toString(), this.selection.categoryName.toLocaleLowerCase());
          }
        }
      });
    } else {
      this.betReceipt.footballAlertsVisible = false;
    }
  }

  /**
  * sets the footballBellActive status
  * @param {IConstant} data
  */
  private handleFootballAlerts(data: IConstant): void {
    this.betReceipt.footballBellActive = data.detail.isEnabled;
  }

  /**
   * check for device OS
   * @param {string[]} osList
   * @return {boolean}
   */
  private checkDeviceOS(osList: string[]): boolean {
    return Object.values(osList).includes(this.nativeBridgeService.getMobileOperatingSystem());
  }

  /**
   * Toggles class to body element to enable/disable scrolling depending on passed state.
   * @param {boolean} state
   * @private
   */
  private toggleBodyScroll(state: boolean): void {
    if (this.windowRefService.document.body) {
      state ? this.rendererService.renderer.addClass(this.windowRefService.document.body, this.BODY_CLASS) :
        this.rendererService.renderer.removeClass(this.windowRefService.document.body, this.BODY_CLASS);
      this.handleScroll(state);
    }
  }

  /**
   * Handle background scrolling for android wrappers
   */
  private handleScroll(state: boolean): void {
    if (this.device.isWrapper && this.device.isAndroid) {
      const htmlElement = this.windowRefService.document.querySelector('html');

      if (state) {
        this.windowScrollY = this.windowRefService.nativeWindow.pageYOffset;
        this.rendererService.renderer.addClass(htmlElement, this.BODY_CLASS);
      } else {
        this.rendererService.renderer.removeClass(htmlElement, this.BODY_CLASS);
        this.domToolsService.scrollPageTop(this.windowScrollY);
      }
    }
  }

  /**
   * Sets YC bet receipt properties
   * @param betReceipt {object}
   * @private
   */
  private setYCBetReceiptProps(betReceipt: IYCBetReceiptModel): void {
    this.betReceipt = {
      selections: true,
      date: betReceipt.data.date,
      payout: { potential: betReceipt.selection.potentialPayout },
      oddsValue: betReceipt.selection.oldOddsValue,
      receipt: betReceipt.data.receipt,
      betId: betReceipt.data.betId,
      stake: { stakePerLine: betReceipt.data.totalStake, amount: betReceipt.data.totalStake }
    };
    if (betReceipt.selection.freeBetOfferCategory) {
      this.betReceipt.stake.freebetOfferCategory = betReceipt.selection.freeBetOfferCategory;
    }
    this.betReceipt.stake.freebet = betReceipt.selection.freebet ? betReceipt.selection.freebet.freebetTokenValue : '0';
  }

  /**
   * Check for Arc user and disable quickbet
   */
  private checkArcUser(): void {
    if (this.arcUserService.quickbet) {
      this.addToBetslipFn.emit();
    } else {
      this.placeBet();
    }
  }
  /**
   * Check for Arc user and send the selection to betslip
   */
  private checkArcUserOnLogIn(): void {
    if (this.arcUserService.quickbet) {
      this.pubsub.subscribe(this.QB_PANEL_NAME, this.pubsub.API.QUICKBET_PANEL_CLOSE, () => {
        this.closePanel();
      });
    }
  }
  /**
  * Check for Arc user and check for notification with popup
  */
  private checkArcNotify(): void {
    if (this.arcUserService.quickbet) {
      this.addToBetslipFn.emit();
    } else {
      this.quickbetDepositService.update(this.selection.stake, this.selection.isEachWay);
    }
  }
  /**
   * Check for Arc user for error
   */
  private checkArcError(message): void {
    if (this.arcUserService.quickbet) {
      this.pubsub.subscribe(this.QB_PANEL_NAME, this.pubsub.API.QUICKBET_PANEL_CLOSE, () => {
        this.closePanel();
      });
    } else {
      this.quickbetNotificationService.saveErrorMessage(message.msg, message.type);
    }
  }

  /**
   * Navigating to betreceipt for luckydip
   * @returns {void} 
   * */
  private setReceiptStateforLd() {
    if (this.isLuckyDip) {
      this.title = this.locale.getString(LUCKY_DIP_CONSTANTS.QB_BET_RECEIPT_TITLE);
      this.goToState(LUCKY_DIP_CONSTANTS.RECEIPT);
    }
  }

  /**
   * Close dialog for animation for lucky dip
   * @returns {void} 
   * */
  private closeAnimationDialog(): void {
    if (this.isState('receipt') && this.isLuckyDip) {
      this.dialogService.closeDialog(DialogService.API.animationModal, true);
    }
  }

  /**
   * Open Quick Deposit form 
   * @returns {void} 
   * */
  openQuickDeposit() {
    this.quickDepositFormExpanded = true;
  }

}
