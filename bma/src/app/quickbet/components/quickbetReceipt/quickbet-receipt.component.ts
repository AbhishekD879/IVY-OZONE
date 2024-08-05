import { Component, Input, OnInit, OnDestroy, Output, EventEmitter } from '@angular/core';
import { UserService } from '@core/services/user/user.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { QuickbetService } from '@app/quickbet/services/quickbetService/quickbet.service';
import {
  IQuickbetReceiptDetailsModel,
  IQuickbetReceiptStakeModel,
  IQuickbetReceiptLegPartsModel
} from '@app/quickbet/models/quickbet-receipt.model';
import { IQuickbetSelectionPriceModel } from '@app/quickbet/models/quickbet-selection-price.model';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import environment from '@environment/oxygenEnvConfig';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import * as _ from 'underscore';
import { StorageService } from '@core/services/storage/storage.service';
import { BYBBet } from '@yourcall/models/bet/byb-bet';
import { HttpClient } from '@angular/common/http';
import { IRacingPostQuickbetReceipt } from '@app/betslip/services/betReceipt/bet-receipt.model';
import { Subscription } from 'rxjs';
import { IRecentRaceTipsData, ISportEvent } from '@app/core/models/sport-event.model';
import { RacingPostTipService } from '@app/lazy-modules/racingPostTip/service/racing-post-tip.service';
import { CmsService } from '@app/core/services/cms/cms.service';
import {
  FiveASideEntryConfirmationService
} from '@app/fiveASideShowDown/services/fiveAside-Entry-confirmation.service';
import { CHANNEL } from '@app/shared/constants/channel.constant';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { MaxPayOutErrorService } from '@app/lazy-modules/maxpayOutErrorContainer/services/maxpayout-error.service';
import { FiveASideContestSelectionService } from '@app/fiveASideShowDown/services/fiveASide-ContestSelection.service';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IFreeBetState } from '@core/services/freeBets/free-bets.model';
import { MAXPAY_OUT } from '@app/lazy-modules/maxpayOutErrorContainer/constants/maxpayout-error-container.constants';
import { LocaleService } from '@core/services/locale/locale.service';
import { FirstBetGAService } from '@app/lazy-modules/onBoardingTutorial/firstBetPlacement/services/first-bet-ga.service';
import { BetReuseService } from '@app/betslip/services/betReUse/bet-reuse.service';
import { ALERTS_GTM } from '@app/betHistory/constants/bet-leg-item.constant';
import { IConstant } from '@app/core/services/models/constant.model';
import { ISystemConfig, ISvgItem } from '@app/core/services/cms/models';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
@Component({
  selector: 'quickbet-receipt',
  templateUrl: 'quickbet-receipt.component.html',
  styleUrls: ['quickbet-receipt.component.scss']
})
export class QuickbetReceiptComponent implements OnInit, OnDestroy {
  @Input() betReceipt: IQuickbetReceiptDetailsModel;
  @Input() selection: IQuickbetSelectionModel;
  @Input() winAlertsEnabled: boolean;
  @Input() ycOddsValue?: Function;
  @Input() isMaxPayedOut: boolean = false;

  @Input() racingPostToggle: IRacingPostQuickbetReceipt;
  @Input() nextRacesToBetslipToggle: boolean;
  @Output() readonly closeQuickbetPanel: EventEmitter<boolean> = new EventEmitter();
  currencySymbol: string;
  stakePerLine: string;
  freebet: string;
  amount: string;
  payout: string;
  isEachWay: boolean;
  odds: string;
  hasFreebet: boolean;
  filteredOutcomeName: string;
  filteredMarketName: string;
  filteredEventName: string;
  winAlertsBet: string;
  winAlertsReceiptId: string;
  eachEayTerms: string;
  linesPerStake: string;
  winAlertsActive: boolean;
  finalStake: string;
  isBogEnabled: boolean;
  excludedDrillDownTagNames: string;
  bybSelectionType: string;
  bybEventName: string;
  sportIconSvgId: string;
  maxPayOutFlag: boolean= false;
  upCellSubscription: Subscription;
  racingPostData: ISportEvent[];
  isNextRacesData: boolean = true;
  isSportIconEnabled: boolean;
  public entryConfirmationdescription: string;
  public showEntryConfirmation: { showdown: boolean, ecText: string, contestId: string, termsConditionTag?: string };
  private UPCELL_ENDPOINT: string;
  private _racingPostTip: IQuickbetSelectionModel;
  private readonly BET_PLACED_ON_HR = environment.HORSE_RACING_CATEGORY_ID;
  termsConditionTag: string;
  REUSE: string = 'REUSE SELECTION';
  YOUR_BETS: string = 'Your Bets: (1)';
  showReuse: boolean = true;
  @Output() readonly reuseSelectionFn?: EventEmitter<void> = new EventEmitter();

  constructor(
    protected user: UserService,
    protected filtersService: FiltersService,
    protected quickbetService: QuickbetService,
    public nativeBridge: NativeBridgeService,
    protected window: WindowRefService,
    protected pubSubService: PubSubService,
    protected http: HttpClient,
    protected storageService: StorageService,
    protected racingPostTipService: RacingPostTipService,
    protected cmsService: CmsService,
    protected fiveASideEntryConfirmationService: FiveASideEntryConfirmationService,
    private fiveASideContestSelectionService: FiveASideContestSelectionService,
    protected freeBetsService: FreeBetsService,
    protected gtmService: GtmService,
    public maxPayOutErrorService: MaxPayOutErrorService,
    protected locale: LocaleService,
    protected firstBetGAService: FirstBetGAService,
    private betReuseService: BetReuseService,
    protected sessionStorage: SessionStorageService,
    protected bonusSuppressionService: BonusSuppressionService
  ) {
    this.UPCELL_ENDPOINT = environment.UPCELL_ENDPOINT;
  }

  ngOnInit(): void {
    this.cmsService.getSystemConfig().subscribe((config) =>{
      if(config?.FiveASideGameLauncher?.entryTermsAndConditionsTag){
        this.termsConditionTag = config.FiveASideGameLauncher.entryTermsAndConditionsTag;
      }
    });

    this.subscribeToFeatured();
    this._racingPostTip = this.quickbetService.racingPostTip;
    this.hasFreebet = Number(this.betReceipt.stake.freebet) > 0;
    this.odds = this.getOdds(this.betReceipt.price);
    this.isEachWay = this.isEachWayBet(this.betReceipt.stake);
    this.stakePerLine = this.setCurrency(this.betReceipt.stake.stakePerLine);
    this.freebet = this.setCurrency(this.betReceipt.stake.freebet);
    this.amount = this.setCurrency(this.betReceipt.stake.amount);
    this.payout =
      +this.betReceipt.payout.potential &&
      this.setCurrency(this.betReceipt.payout.potential);
    this.filteredOutcomeName = this.filterOutcomeName();
    this.filteredMarketName = this.filterMarketName();
    this.filteredEventName = this.filterEventName();
    this.linesPerStake = this.getLinesPerStake(this.betReceipt.stake);
    this.finalStake = this.getStake(this.selection.stake);
    this.excludedDrillDownTagNames = this.getExcludedDrillDownTagNames();

    if (this.isEachWay) {
      this.eachEayTerms = this.getEWTerms(this.betReceipt.legParts[0]);
    }

    this.winAlertsActive = this.storageService.get('winAlertsEnabled');
    if (this.winAlertsActive) {
      this.toggleWinAlerts(this.betReceipt, true);
    }

    this.isBogEnabled = this.isBogFromPriceType();
    this.checkEntryConfirmationLegs();
    this.setBybData();
    this.checkMaxPayOut();
    this.initRacingPostTip();
    this.freeBetsStoreUpdate(this.betReceipt);
    this.setSportIcon();
  }

  ngOnDestroy(): void {
    if (this.winAlertsBet) {
      this.nativeBridge.onActivateWinAlerts(this.winAlertsReceiptId, [this.winAlertsBet]);
    }
    this.upCellSubscription && this.upCellSubscription.unsubscribe();
  }

  subscribeToFeatured() {
      this.pubSubService.subscribe('quickbet-receipt', this.pubSubService.API.WS_EVENT_UPDATE, (data) => {
        if (data && data.update && data.update.event.eventId.toString() === this.selection.eventId.toString()) {
          const update = data.update;
          const outcome = update.type === "SELCN" ? update.event.market.outcome : undefined;
          this.showReuse = (update.type === "SELCN" &&  outcome.outcomeId.toString() === this.selection.markets[0].outcomes[0].id.toString())? (outcome.displayed === 'Y' && outcome.status === 'A') :
          (update.type === "EVENT" ? (update.event.displayed === 'Y' && update.event.status === 'A') : true)
        }
      });
  }

  onQuickbetEvent() {
    this.closeQuickbetPanel.emit(true);
  }

  setCurrency(val: string): string {
    return this.filtersService.setCurrency(val, this.user.currencySymbol);
  }

  getStake(val: string): string {
    if (!val) {
      return '';
    }

    const stake = this.isEachWay ? parseFloat(val) * 2 : parseFloat(val);
    return this.setCurrency(stake.toString());
  }

  /**
   * Get Each Way terms - Each Way Odds 1/5 Places 1-2-3
   * @param price {object}
   * @returns {string}
   */
  getEWTerms(legPart: IQuickbetReceiptLegPartsModel): string {
    return this.quickbetService.getEWTerms(legPart);
  }

  /**
   * Get Lines per stake - 2 Lines at £1 per line
   * @param receipt {object}
   * @returns {string}
   */
  getLinesPerStake(stake: IQuickbetReceiptStakeModel): string {
    return this.quickbetService.getLinesPerStake(stake);
  }

  /**
   * Get odds in correct format
   * @param price {object}
   * @returns {string}
   */
  getOdds(price: IQuickbetSelectionPriceModel): string {
    return this.quickbetService.getOdds(price);
  }

  /**
 * Handler for click on football bell icon.
 */
  onFootballBellClick(): void {
    this.nativeBridge.onEventAlertsClick(
      this.selection.eventId.toString(),
      this.selection.categoryName.toLocaleLowerCase(),
      this.selection.categoryId,
      this.selection.drilldownTagNames,
      ALERTS_GTM.QUICK_BET);

    this.nativeBridge.showFootballAlerts();
    this.sendGTMMatchAlertClick();
  }

  /**
   * Check if eachway option was chosen by user
   * @param stake
   * @returns {boolean}
   */
  isEachWayBet(stake: IQuickbetReceiptStakeModel): boolean {
    return stake.stakePerLine !== stake.amount;
  }

  /**
   * Clear name(e.g. |Al Dancer| => Al Dancer)
   * @param name
   * @returns {string}
   */
  clearName(name: string): string {
    return name.replace(/[|,]/g, '');
  }

  /**
   * Filter outcome name (add handicap value to name if it is present).
   * @returns {string}
   */
  filterOutcomeName(): string {
    const names = _.map(
      this.betReceipt.legParts,
      ({ outcomeDesc, handicap }) => {
        let name = this.filtersService.filterPlayerName(outcomeDesc);
        name = this.clearName(name);
        if (handicap && this.selection.markets && this.selection.markets.length && this.selection.markets[0].outcomes.length &&
          this.selection.markets[0].outcomes[0].outcomeMeaningMajorCode === this.locale.getString('app.highLowerVal')) {
          const handiCapVal: string = String(handicap).replace(/[\+,\s\s+]/g, '');
          name += ` (${handiCapVal})`;
        } else if (handicap) {
          name += ` (${handicap})`;
        }

        return name;
      }
    );

    return names.join(', ');
  }

  /**
   * to exclude Racing unnamed favourites signposting icon from bet-receipt
   */
  getExcludedDrillDownTagNames(): string {
    const excludedArray = [];

    if (this.selection.isUnnamedFavourite) {
      excludedArray.push('MKTFLAG_EPR', 'EVFLAG_EPR');
    }

    return excludedArray.join(',');
  }

  /**
   * Filters market name.
   * @return {string}
   */
  filterMarketName(): string {
    return _.map(this.betReceipt.legParts, ({ outcomeDesc, marketDesc }) => {
      const name = this.filtersService.filterAddScore(marketDesc, outcomeDesc);
      return this.clearName(name);
    }).join(', ');
  }

  /**
   * Filters event name from bet receipt.
   * @return {string}
   */
  filterEventName(): string {
    const { eventDesc = '' } = _.isArray(this.betReceipt.legParts)
      ? this.betReceipt.legParts[0]
      : {};
    return this.selection &&
      this.quickbetService.isVirtualSport(this.selection.categoryName)
      ? this.selection.eventName
      : this.clearName(eventDesc);
  }

  /**
   * Get potential payout value
   * @param {string} payout
   * @returns {string}
   */
  getPotentialPayoutValue(payout: string): string {
    return payout || 'N/A';
  }

  showWinAlertsTooltip(): boolean {
    const MAX_VIEWS_COUNT = 1;
    const tooltipData = this.storageService.get('tooltipsSeen') || {};
    return (
      (tooltipData[`receiptViewsCounter-${this.user.username}`] || null) <=
      MAX_VIEWS_COUNT && !this.user.winAlertsToggled
    );
  }

  toggleWinAlerts(receipt: IQuickbetReceiptDetailsModel, event: boolean): void {
    if (this.window.nativeWindow.NativeBridge.pushNotificationsEnabled) {
      if (event) {
        const receiptId = receipt.receipt.id;
        if (!this.user.winAlertsToggled) {
          this.user.set({ winAlertsToggled: true });
        }
        if (!this.winAlertsReceiptId) {
          this.winAlertsReceiptId = receiptId;
        }
        this.winAlertsBet = receiptId;
        this.storageService.set('winAlertsEnabled', true);
        this.sendGTMWinAlertToggle(true);
      } else {
        this.winAlertsBet = null;
        this.storageService.set('winAlertsEnabled', false);
        this.sendGTMWinAlertToggle(false);
      }
    }
    if (this.sessionStorage.get('firstBetTutorialAvailable')) {
      this.firstBetGAService.setGtmData('Event.Tracking', 'click', 'step 3', 'toggle on/off');
    }
  }

  /**
   * Check if BogToggle is true/false from priceTypeRef.id --> 'GUARANTEED' and it is not a Greyhounds event
   * @returns <boolean>
   */
  isBogFromPriceType(): boolean {
    const betReceiptPrice = this.betReceipt.price,
      eventCategoryId = this.selection.categoryId;
    return (
      betReceiptPrice &&
      betReceiptPrice.priceTypeRef &&
      betReceiptPrice.priceTypeRef.id &&
      betReceiptPrice.priceTypeRef.id === 'GUARANTEED' &&
      !this.filtersService.isGreyhoundsEvent(eventCategoryId)
    );
  }

  /**
   * post racingpost Details by upcell if placed bet is GH/HR for mobile
   * @returns {Observable<IRacingPostHRResponse>}
   */
  sendRacingPostByUpcell(isTipEnabled): void {
    let body = {};
    if (this._racingPostTip && this._racingPostTip.categoryId === '21') {
      const url = `${this.UPCELL_ENDPOINT}/v1/api/bets`;
      body = {
        tipEnabled: isTipEnabled,
        bets: [{
          startTime: this._racingPostTip.startTime,
          eventId: this._racingPostTip.eventId
        }]
      };
      this.upCellSubscription = this.quickbetService.readUpCellBets(url, body).subscribe((racingTipData: IRecentRaceTipsData) => {
        this.isNextRacesData = racingTipData.nextRace;
        this.racingPostTipService.updateRaceData(racingTipData.races);
        this.racingPostData = racingTipData.races;
        if(this.isNextRacesData) {
          this.pubSubService.publish(this.pubSubService.API.IS_TIP_PRESENT, {
            isTipPresent: false,
            raceData: this.racingPostData
          });
        }
      });
    }
  }
    /**
* Send GA tracking on render of tooltip
*/
sendGTMData(eventAction: string): void {
  const gtmData = {
    eventAction: eventAction,
    eventCategory: MAXPAY_OUT.eventCategory,
    eventLabel: MAXPAY_OUT.eventLabel[0]
  };
  this.gtmService.push(MAXPAY_OUT.trackEvent, gtmData);
}

  /**
   * on click of win alerts info icon - GA tracking
   */
  private handleAlertInfoClick(): void {
    const gtmData = {
      'component.ActionEvent': ALERTS_GTM.CLICK,
      'component.PositionEvent': ALERTS_GTM.NA,
      'component.EventDetails': ALERTS_GTM.WIN_ALERT_ICON
    };
    this.sendGTMAlerts(gtmData);
  }

  /**
   * toggle win alerts - GA tracking
   * @param { boolean } enabled 
   * 
   */
  private sendGTMWinAlertToggle(enabled: boolean): void {
    const gtmData = {
      'component.ActionEvent': enabled ? ALERTS_GTM.TOGGLE_ON : ALERTS_GTM.TOGGLE_OFF,
      'component.PositionEvent': ALERTS_GTM.QUICK_BET,
      'component.EventDetails': ALERTS_GTM.WIN_ALERT
    };
    this.sendGTMAlerts(gtmData);
  }

  /**
  * click match alerts - GA tracking
  */
  private sendGTMMatchAlertClick(): void {
    const gtmData = {
      'component.ActionEvent': ALERTS_GTM.CLICK,
      'component.PositionEvent': ALERTS_GTM.QUICK_BET,
      'component.EventDetails': ALERTS_GTM.MATCH_ALERT_ICON
    };
    this.sendGTMAlerts(gtmData);
  }

  /**
* alerts - GA tracking
* @param { ALERTS_GTM } gtmData
*/
  private sendGTMAlerts(gtmData: IConstant): void {
    const gtmAlertsData = {
      'component.CategoryEvent': ALERTS_GTM.SPORT_ALERT,
      'component.LabelEvent': ALERTS_GTM.MATCH_ALERT,
      'component.LocationEvent': ALERTS_GTM.QUICK_BET,
      'component.URLClicked': ALERTS_GTM.NA,
      'sportID': this.selection.categoryId,
      ...gtmData
    };
    this.gtmService.push(ALERTS_GTM.EVENT_TRACKING, gtmAlertsData);
  }

/**
 * Toggle of tooltip
 */
togglemaxPayedOut(): void {
  this.isMaxPayedOut = !this.isMaxPayedOut;
  if (this.isMaxPayedOut) {
    this.sendGTMData(MAXPAY_OUT.eventAction[2]);
  }
}

  /**
   *  Get racing post tip GA tracking
   */
  onRacingPostGTMEvent(event) {
    this.racingPostTipService.racingPostGTM = event.value;
  }

  get oddsValue(): string | number {
    return this.ycOddsValue ? this.ycOddsValue() : this.betReceipt.oddsValue;
  }
  set oddsValue(value: string | number) { }

  private setBybData(): void {
    if (this.selection instanceof BYBBet) {
      const sel = this.selection as BYBBet;
      this.bybSelectionType = this.quickbetService.getBybSelectionType(
        sel.channel
      );
      this.bybEventName = this.clearName(sel.game.title);
    }
  }

  enableRacingPostTip() {
    return this.racingPostToggle && this.racingPostToggle.enabled && this.racingPostToggle.quickBetReceipt;
  }
  private initRacingPostTip() {
    if (this.selection && this.selection.categoryId === this.BET_PLACED_ON_HR) {
      const isTipEnabled = this.racingPostToggle && this.racingPostToggle.enabled && this.racingPostToggle.quickBetReceipt;
      this.sendRacingPostByUpcell(isTipEnabled);
    }
  }

  /**
   * To get the the details of entryconfirmation
   * @returns void
   */
  private getEntryConfirmationDetails(sel: BYBBet): void {
    const isFreeBet:boolean = Object.keys(sel).length>0 && sel.hasOwnProperty('freebet');
    if (sel.selections.length === 5 && sel.channel  === CHANNEL.fiveASide && this.fiveASideContestSelectionService.defaultSelectedContest?.length > 0) {
      const showdownObj = {
        receipt: this.betReceipt.receipt,
        betId: this.betReceipt.betId.toString(),
        userId: this.user.username,
        token: this.user.bppToken,
        freebet: isFreeBet,
        brand: environment.brand,
        eventId: sel.game._obEventId,
        role: this.fiveASideEntryConfirmationService.isTestOrRealUser(this.user.email),
        contestId: this.fiveASideContestSelectionService.defaultSelectedContest
      };
      this.fiveASideEntryConfirmationService
        .getShowdownConfirmationDisplay(showdownObj)
        .subscribe((response: { showdown: boolean, ecText: string, contestId: string, termsConditionTag?: string }) => {
          response.termsConditionTag = this.termsConditionTag; 
          this.showEntryConfirmation = response;
          this.fiveASideContestSelectionService.defaultSelectedContest = null;
        },(error: string) => {
          console.warn(error);
        });
    }
  }

  /**
   * TO get the legs for entry confirmation
   * @returns {void}
   */
  private checkEntryConfirmationLegs() {
    if (this.selection instanceof BYBBet) {
      const sel = this.selection as BYBBet;
      this.getEntryConfirmationDetails(sel);
    }
  }
  /**
  * check for Max Payout
  * @param receiptBets
  * @returns void
  */
  private checkMaxPayOut(): void {
    if (this.betReceipt.betTags && this.betReceipt.betTags.betTag && this.betReceipt.betTags.betTag[0].tagName === 'CAPPED') {
      this.maxPayOutFlag = true;
      this.sendGTMData(MAXPAY_OUT.eventAction[1]);
    }
  }

  /**
   * After quick bet response update freebets local storage
   * @param {IQuickbetReceiptDetailsModel} betReceipt
   * @returns void
   */
  private freeBetsStoreUpdate(betReceipt: IQuickbetReceiptDetailsModel): void {
    if (betReceipt.freebetId) {
      const freeBetsState: IFreeBetState = this.freeBetsService.getFreeBetsState();
      let freebets = [...freeBetsState.data, ...freeBetsState.betTokens, ...freeBetsState.fanZone];
      freebets = freebets.filter((freebet: IFreebetToken) => betReceipt.freebetId != Number(freebet.freebetTokenId));
      this.freeBetsService.store(this.user.username, {data: freebets});
    }
  }

  appendDrillDownTagNames (selection) {
    const twoUpMarketName: string = this.locale.getString('bma.twoUpMarketName');
    return selection.marketName === twoUpMarketName ? `${selection.marketName},` : '';
  }

  /**
   * call reuse service and add bets to bet slip
   */
  reuseBets(): void {
    this.betReuseService.reuseQuickBet(this.selection);
    this.closeQuickbetPanel.emit(true);
  }
  /**
   * Sets Sport icon svg id fetched from stored cms data
   */
  setSportIcon(): void {
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.isSportIconEnabled = config?.CelebratingSuccess?.displaySportIcon?.includes('betreceipt');
    });
    const categoryId = this.selection?.categoryId;
    if (this.bybSelectionType === "5-A-Side") this.sportIconSvgId = "5-a-side";
    else if (categoryId) {
      this.cmsService.getItemSvg('', Number(categoryId))
        .subscribe((icon: ISvgItem) => {
          this.sportIconSvgId = icon.svgId ? icon.svgId : "icon-generic";
        });
    }
  }
}
