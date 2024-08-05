import { of as observableOf, Observable, Subject } from 'rxjs';
import { shareReplay, map, concatMap } from 'rxjs/operators';

import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import * as _ from 'underscore';

import { BetslipDataService } from '@betslip/services/betslip/betslip-data.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { StorageService } from '@core/services/storage/storage.service';
import { UserService } from '@core/services/user/user.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { GtmService } from '@core/services/gtm/gtm.service';

import { IBppResponse, IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IOddsBoost, IBetInfo } from '@betslip/services/bet/bet.model';
import { Bet } from '@betslip/services/bet/bet';
import { InformationDialogComponent } from '@sharedModule/components/informationDialog/information-dialog.component';
import { IPrice } from '../components/oddsBoostPrice/odds-boost-price.model';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { IDialogButton } from '@core/services/dialogService/dialog-params.model';

import { dialogIdentifierDictionary } from '@core/constants/dialog-identifier-dictionary.constant';
import { OddsBoostInfoDialogComponent } from '@shared/components/oddsBoostInfoDialog/odds-boost-info-dialog.component';
import { VanillaFreebetsBadgeDynamicLoaderService } from '@app/vanillaInit/services/vanillaFreeBets/vanilla-fb-badges-loader.service';
import { ISystemConfig , IOddsBoostMsgConfigDetails} from '@app/core/services/cms/models';

enum POPUP_CAPTIONS {
    YESPLEASE = 'yes please',
    NOTHANKS = 'no thanks',
    OKTHANKS = 'ok thanks'
  }
@Injectable()
export class OddsBoostService {
  static readonly BET_TYPES = ['', 'ANY', 'SGL', 'DBL', 'TBL', 'ACCA'];
  static readonly BET_LEVELS = ['SELECTION', 'MARKET', 'EVENT', 'TYPE', 'CLASS', 'CATEGORY', 'ANY', ''];
  static oddsBoostSeen: boolean;
  static maxBoostValue: string;
  private static oddsBoostCount: Subject<number> = new Subject();

  private boostTokens: IFreebetToken[] = [];
  private boostActive: boolean;
  private doNotUnsetFreeBets: boolean;
  private title: string = 'OddsBoostService';
  private betslipDialog : IOddsBoostMsgConfigDetails;

  constructor(
    private cmsService: CmsService,
    private coreToolsService: CoreToolsService,
    private dialogService: DialogService,
    private bppService: BppService,
    private storageService: StorageService,
    private userService: UserService,
    private infoDialogService: InfoDialogService,
    private localeService: LocaleService,
    private pubSubService: PubSubService,
    private betslipDataService: BetslipDataService,
    private fracToDecService: FracToDecService,
    private gtmService: GtmService,
    private router: Router,
    private freeBetsBadgeLoader: VanillaFreebetsBadgeDynamicLoaderService,
  ) {
    this.subscribeToEvents();
    this.getBoostActiveFromStorage();
    OddsBoostService.oddsBoostSeen = this.storageService.get('oddsBoostSeen');

    this.pubSubService.subscribe(this.title, this.pubSubService.API['show-slide-out-betslip-true'], () => this.openFirstTimeDialog());

    this.pubSubService.subscribe(this.title, pubSubService.API.ODDS_BOOST_INFO_DIALOG, () => this.openFirstTimeDialog());

    // store oddsboost tokens after page refresh
    this.pubSubService.subscribe(this.title, pubSubService.API.STORE_ODDS_BOOST, (tokens: IFreebetToken[]) => {
      this.storeTokens(tokens);
    });
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
        this.betslipDialog = config.OddsBoostMsgConfig;
      });
  }

  get updateCountListeners(): string {
    return 'show-sidebar-right-menu-true';
  }
 set updateCountListeners(value:string){}
  get dialogComponent(): typeof OddsBoostInfoDialogComponent {
    return OddsBoostInfoDialogComponent;
  }
  set dialogComponent(value:typeof OddsBoostInfoDialogComponent){}

  get informationDialog(): typeof InformationDialogComponent {
    return InformationDialogComponent;
  }
set informationDialog(value:typeof InformationDialogComponent){}
  get tokens(): IFreebetToken[] {
    return this.boostTokens;
  }
set tokens(value:IFreebetToken[]){}
  get oddsBoostsCountListener(): Observable<number> {
    return OddsBoostService.oddsBoostCount.asObservable();
  }
set oddsBoostsCountListener(value:Observable<number>){}
  init(tokens: IFreebetToken[]): Observable<void> {
    this.boostTokens = tokens;
    this.freeBetsBadgeLoader.addOddsBoostCounter(tokens);
    return observableOf(null);
  }

  isBoostActive(): boolean {
    return this.boostActive;
  }

  showTokensInfoDialog(): Observable<null> {
    const tokens = this.boostTokens;
    const storageTokens = this.getStorageTokens();
    const isNewTokensAvailable = this.isNewTokensAvailable(tokens, storageTokens);
    const keepPopupHidden = this.keepPopupHidden();

    // store actual tokens
    this.storeTokens(tokens);

    // compare tokens with tokens from storage
    // if there is no available (new tokens) - don't show dialog
    if (!isNewTokensAvailable || keepPopupHidden) {
      return observableOf(null);
    }

    this.pubSubService.publish(this.pubSubService.API.USER_INTERACTION_REQUIRED);

    return Observable.create(observer => {
      this.dialogService.openDialog(DialogService.API.oddsBoostInfo, this.dialogComponent, false, {
        oddsBoostTokens: tokens,
        oddsBoostConfig: this.cmsService.initialData.oddsBoost,
        onBeforeClose: () => {
          observer.next();
          observer.complete();
        }
      });
    });
  }

  showInfoDialog(): void {
    const buttons: IDialogButton[] = [{
      caption: 'Ok',
      cssClass: 'btn-style2',
    }];

    const moreLink = this.cmsService.initialData.oddsBoost.moreLink;
    if (moreLink) {
      buttons.unshift({
        caption: 'More',
        cssClass: 'btn-style4',
        handler: () => {
          this.router.navigateByUrl(moreLink);
          this.pubSubService.publish('show-slide-out-betslip', false);
        }
      });
    }

    this.infoDialogService.openInfoDialog(
      this.localeService.getString('oddsboost.infoDialog.title'),
      this.localeService.getString('oddsboost.infoDialog.text', [OddsBoostService.maxBoostValue, this.userService.currencySymbol]),
      'bs-odds-boost-info-dialog', undefined, undefined, buttons
    );
  }

  setMaxBoostValue(value: string): void {
    OddsBoostService.maxBoostValue = value;
  }

  isOddsBoostEnabled(): boolean {
    return !!this.coreToolsService.getOwnDeepProperty(this.cmsService.initialData, 'oddsBoost.enabled');
  }

  isOddsBoostBetslipHeaderAvailable(): boolean {
    return (
      this.userService.status &&
      this.isOddsBoostEnabled() &&
      this.hasSelectionsWithBoost()
    );
  }

  hasSelectionsWithBoost(): boolean {
    return _.some(this.betslipDataService.bets, bet => {
      return (bet.oddsBoost && !bet.info().disabled);
    });
  }

  canBoostSelections(): boolean {
    return (
      this.hasSelectionsWithBoost() &&
      !_.some(this.betslipDataService.bets, bet => {
        const betInfo = bet.info();
        return (
          betInfo.isSPLP && betInfo.pricesAvailable && bet.price.type === 'SP'
        );
      })
    );
  }

  hasSelectionsWithFreeBet(): boolean {
    return this.betslipDataService.bets.some((bet: Bet) =>  bet.freeBet && !!bet.freeBet.id);
  }

  getOddsBoostTokens(isPageRefresh?: boolean): Observable<IFreebetToken[]> {
    // different methods for direct freebets load and on page refresh when we load all freebets in one call
    const method = isPageRefresh ? 'allAccountFreebets' : 'accountOddsBoost';
    // BETBOOST param passed to get correct filtered freebets in response
    return this.userService.isInShopUser() ? observableOf([]) :
      this.bppService.send(method, 'BETBOOST').pipe(
        shareReplay(1),
        map((res: IBppResponse) => {
          const tokens = this.coreToolsService.getOwnDeepProperty((res), 'response.model.freebetToken', []);
          this.boostTokens = tokens;
          this.freeBetsBadgeLoader.addOddsBoostCounter(tokens);
          return tokens;
        })
      );
  }

  getOddsBoostTokensCount(): Observable<number>  {
    return this.getOddsBoostTokens().pipe(concatMap(data => {
      const oddsBoostsCount = data ? data.length : 0;
      return observableOf(oddsBoostsCount);
    }));
  }

  storeTokens(tokens: IFreebetToken[]): void {
    this.boostTokens = tokens;
    this.storageService.set(`oddsBoostTokens-${this.userService.username}`, tokens);
  }

  getStorageTokens(): IFreebetToken[] {
    return this.storageService.get(`oddsBoostTokens-${this.userService.username}`) || [];
  }

  isNewTokensAvailable(tokens: IFreebetToken[], storageTokens: IFreebetToken[]): boolean {
    return _.difference(
      tokens.map(t => t.freebetTokenId),
      storageTokens.map(t => t.freebetTokenId)
    ).length > 0;
  }

  showOddsBoostSpDialog(): void {
    this.infoDialogService.openInfoDialog(
      this.localeService.getString('oddsboost.spDialog.title'),
      this.localeService.getString('oddsboost.spDialog.text'),
      null,
      dialogIdentifierDictionary.informationDialog,
      null,
      [{caption: this.localeService.getString('oddsboost.spDialog.ok')}]
    );
    this.pubSubService.publish(this.pubSubService.API.ODDS_BOOST_CHANGE, false);
  }

  getOldPriceFromBetslipStake(betslipStake: IBetInfo, type: string): IPrice {
    if (type === 'single') {
      return {
        decimal: betslipStake.price.priceDec,
        num: betslipStake.price.priceNum,
        den: betslipStake.price.priceDen
      };
    }

    if (type === 'multiple' || type === 'acca') {
      return this.convertPotentialPayoutToPrice(betslipStake.potentialPayout);
    }
  }

  getNewPriceFromBetslipStake(betslipStake: IBetInfo, type: string): IPrice {
    if (type === 'single') {
      return {
        decimal: betslipStake.Bet.oddsBoost.enhancedOddsPrice,
        num: betslipStake.Bet.oddsBoost.enhancedOddsPriceNum,
        den: betslipStake.Bet.oddsBoost.enhancedOddsPriceDen
      };
    }

    if (type === 'multiple' || type === 'acca') {
      return this.convertPotentialPayoutToPrice(+betslipStake.Bet.oddsBoost.enhancedOddsPrice);
    }
  }

  getOldPriceFromQuickBet(selection: IQuickbetSelectionModel): IPrice {
    return {
      decimal: selection.price.priceDec,
      num: selection.price.priceNum,
      den: selection.price.priceDen
    };
  }

  getNewPriceFromQuickBet(selection: IQuickbetSelectionModel): IPrice {
    if (selection.oddsBoost) {
      return {
        decimal: selection.oddsBoost.enhancedOddsPrice,
        num: selection.oddsBoost.enhancedOddsPriceNum,
        den: selection.oddsBoost.enhancedOddsPriceDen
      };
    } else {
      return { decimal: 0, num: 0, den: 0 };
    }
  }

  showOddsBoostFreeBetDialog(selectOddsBoostFirst: boolean, type: string): void {
    let params;
    const betType = (type === 'betslip'? 'betslip' : 'quickbet');
    if (selectOddsBoostFirst) {
      this.sendGTM(betType, 'not opted free bet', 'load', 'contentView');
      params = {
        caption: this.localeService.getString(this.betslipDialog.continueWith),
        text: this.localeService.getString(this.betslipDialog.cancelBoostPriceMessage),
        buttons: [
          {
            caption: this.localeService.getString(this.betslipDialog.noThanks),
            cssClass: 'btn-style4',
            handler: this.closeOddsBoostFreeBetDialog.bind(this, POPUP_CAPTIONS.NOTHANKS, type)
          },
          {
            caption: this.localeService.getString(this.betslipDialog.yesPlease),
            handler: this.continueWithFreeBet.bind(this, POPUP_CAPTIONS.YESPLEASE, type)
          }
        ],
        onBeforeClose: this.continueWithOddsBoost.bind(this)
      };
    } else {
      this.sendGTM(betType, 'opted free bet', 'load', 'contentView');
      params = {
        caption: this.localeService.getString(this.betslipDialog.continueWith),
        text: this.localeService.getString(this.betslipDialog.cantBoostMessage),
        buttons: [
          {
            caption: this.localeService.getString(this.betslipDialog.okThanks),
            handler: this.closeOddsBoostFreeBetDialog.bind(this, POPUP_CAPTIONS.OKTHANKS, type)
          }
        ]
      };
    }

    this.dialogService.openDialog(DialogService.API.informationDialog, this.informationDialog, true, params);
  }

  getBoostActiveFromStorage(): boolean {
    this.boostActive = !!this.storageService.get('oddsBoostActive');
    return this.boostActive;
  }

  isMaxStakeExceeded(stake: number): boolean {
    if (stake > +OddsBoostService.maxBoostValue) {
      this.infoDialogService.openInfoDialog(
        this.localeService.getString('oddsboost.maxStakeExceeded.title'),
        this.localeService.getString('oddsboost.maxStakeExceeded.text', [OddsBoostService.maxBoostValue, this.userService.currencySymbol]),
        null,
        dialogIdentifierDictionary.informationDialog,
        null,
        [{
          caption: this.localeService.getString('oddsboost.spDialog.ok'),
          cssClass: 'btn-style2 btn-medium'
        }]
      );
      this.pubSubService.publish(this.pubSubService.API.ODDS_BOOST_CHANGE, false);
      return true;
    }
  }

  settleOddsBoostTokens(bets: Bet[]): Observable<Bet[]> {
    bets.forEach((bet: Bet) => this.sortBetTokens(bet));
    this.removeIneligibleBoosts(bets);
    this.useDailyBoost(bets);
    this.checkBetslipSelections();
    return observableOf(bets);
  }

  sortPageTokens(tokens: IFreebetToken[]): IFreebetToken[] {
    return tokens.sort((a: IFreebetToken, b: IFreebetToken) =>
      this.betTypeSort(a.freebetOfferType, b.freebetOfferType) ||
      this.betLevelSort(this.getBetLevel(a), this.getBetLevel(b)) ||
      this.betExpirySort(a.freebetTokenExpiryDate, b.freebetTokenExpiryDate) ||
      this.betNameSort(a.freebetOfferName, b.freebetOfferName)
    );
  }

  sendEventToGTM(eventCategory: string, isActive: boolean): void {
    this.gtmService.push('trackEvent',   {
      event: 'trackEvent',
      eventCategory: eventCategory,
      eventAction: 'odds boost',
      eventLabel: isActive ? 'toggle on' : 'toggle off'
    });
  }

  private getBetLevel(token: IOddsBoost | IFreebetToken): string {
    return token.tokenPossibleBets && token.tokenPossibleBets.length ? token.tokenPossibleBets[0].betLevel : '';
  }

  private sortBetTokens(bet: Bet): void {
    const tokens = bet.params.oddsBoosts || [];

    _.each(tokens, (oddsBoostToken: IOddsBoost) => {
      const betLevel = this.getBetLevel(oddsBoostToken);
      const freebetOfferType = oddsBoostToken.freebetOfferType;
      oddsBoostToken.sorting = !betLevel && !freebetOfferType ? {} : {
        level: betLevel,
        type: freebetOfferType
      };
    });

    this.sortingFlow(tokens);
    bet.oddsBoost = tokens[0];
  }

  private removeIneligibleBoosts(bets: Bet[]): void {
    const sgls = _.filter(bets, (bet: Bet) => bet.type === 'SGL' && !!bet.oddsBoost);
    const accaBet = _.find(bets, (bet: Bet) => bet.type !== 'SGL' && bet.lines === 1 && !!bet.oddsBoost);

    if (accaBet && accaBet.oddsBoost && !_.contains(['', 'SGL', 'ANY'], accaBet.oddsBoost.sorting.type)) {
      _.each(sgls, (bet: Bet) => {
        bet.oddsBoost = null;
      });

      return;
    }

    const boostedBets = _.union(sgls, accaBet ? [accaBet] : []);
    this.removeDifferentTokens(boostedBets);
  }

  private removeDifferentTokens(bets: Bet[]): void {
    const tokens = _.pluck(bets, 'oddsBoost');

    this.sortingFlow(tokens);

    _.each(bets, (bet: Bet) => {
      if (bet.oddsBoost.id !== tokens[0].id) {
        bet.oddsBoost = null;
      }
    });
  }

  private sortingFlow(tokens: IOddsBoost[]): IOddsBoost[] {
    return tokens.sort((a: IOddsBoost, b: IOddsBoost) =>
      this.betTypeSort(a.sorting.type, b.sorting.type) ||
      this.betLevelSort(a.sorting.level, b.sorting.level) ||
      this.betExpirySort(a.expiry, b.expiry) ||
      this.betNameSort(a.offerName, b.offerName)
    );
  }

  private betTypeSort(a: string, b: string): number {
    const aType = this.betTypeIndex(a);
    const bType = this.betTypeIndex(b);

    if (aType > bType) { return -1; }
    if (aType < bType) { return 1; }
    return 0;
  }

  private betLevelSort(a: string, b: string): number {
    const aLevel = _.indexOf(OddsBoostService.BET_LEVELS, a);
    const bLevel = _.indexOf(OddsBoostService.BET_LEVELS, b);

    if (aLevel > bLevel) { return 1; }
    if (aLevel < bLevel) { return -1; }
    return 0;
  }

  private betExpirySort(a: string, b: string): number {
    const aExpiry = new Date(a).getTime();
    const bExpiry = new Date(b).getTime();

    if (aExpiry > bExpiry) { return 1; }
    if (aExpiry < bExpiry) { return -1; }
    return 0;
  }

  private betNameSort(a: string, b: string): number {
    return a.toLowerCase() > b.toLowerCase() ? 1 : -1;
  }

  private betTypeIndex(type: string): number {
    switch (type) {
      case '':
      case 'ANY':
      case 'SGL':
        return 1;
      case 'DBL':
        return 2;
      case 'TBL':
        return 3;
      default :
        const index = /(\d+)$/.exec(type);
        return index ? +index[0] : 1;
    }
  }

  private openFirstTimeDialog(): void {
    if (
      this.isOddsBoostBetslipHeaderAvailable() &&
      !OddsBoostService.oddsBoostSeen &&
      OddsBoostService.maxBoostValue
    ) {
      OddsBoostService.oddsBoostSeen = true;
      this.storageService.set('oddsBoostSeen', true);
      this.showInfoDialog();
    }
  }

  private closeOddsBoostFreeBetDialog(message: string, type: string): void {
    this.sendGTM((type === 'betslip'? 'betslip' : 'quickbet'), message, 'click', 'trackEvent');
    this.dialogService.closeDialog(DialogService.API.informationDialog);
  }

  private continueWithOddsBoost() {
    if (!this.doNotUnsetFreeBets) {
      this.pubSubService.publish('ODDS_BOOST_UNSET_FREEBETS');
    } else {
      this.doNotUnsetFreeBets = false;
    }
  }

  private continueWithFreeBet(message: string, type: string) {
    this.pubSubService.publish(this.pubSubService.API.ODDS_BOOST_CHANGE, false);
    this.doNotUnsetFreeBets = true;
    this.closeOddsBoostFreeBetDialog(message, type);
  }

  private subscribeToEvents(): void {
    // odds boost change
    this.pubSubService.subscribe(this.title, this.pubSubService.API.ODDS_BOOST_CHANGE, (active: boolean) => {
      this.boostActive = active;
      this.storageService.set('oddsBoostActive', active);
    });

    // handle sp
    this.pubSubService.subscribe(this.title, this.pubSubService.API.ODDS_BOOST_HANDLE_SP, () => {
      if (this.isOddsBoostEnabled() && this.isBoostActive()) {
        this.showOddsBoostSpDialog();
      }
    });

    this.pubSubService.subscribe(this.title, this.pubSubService.API.ODDS_BOOST_SEND_GTM, (data: { origin: string, state: boolean }) => {
      this.sendEventToGTM(data.origin, data.state);
    });

    this.pubSubService.subscribe(this.title, this.pubSubService.API.ODDS_BOOST_CHECK_BS_SELECTIONS, () => {
      this.checkBetslipSelections();
    });

    this.pubSubService.subscribe(`oddsBoostCountNotification`, this.updateCountListeners, this.updateOddsBoostCount.bind(this));

    this.pubSubService.subscribe(this.title, this.pubSubService.API.ODDS_BOOST_DECREMENT_COUNTER, () => {
      this.decrementBoostsCount();
    });
  }

  private convertPotentialPayoutToPrice(value: number): IPrice {
    const format = this.userService.oddsFormat;

    if (format === 'dec') {
      return { decimal: value.toFixed(2) };
    } else {
      const price = this.fracToDecService.decToFrac(value , true).split('/');
      return { num: price[0], den: price[1] };
    }
  }

  private updateOddsBoostCount(): void {
    if (this.userService.status) {
      this.getOddsBoostTokensCount().subscribe((oddsBoostsCount: number)  => {
        OddsBoostService.oddsBoostCount.next(oddsBoostsCount);
      });
    }
  }

  private decrementBoostsCount(): void {
    if (this.userService.status) {
      this.boostTokens && this.boostTokens.pop();

      const tokens = this.boostTokens || [];
      this.freeBetsBadgeLoader.addOddsBoostCounter(tokens);
    }
  }

  /**
   * Check betslip selections and disable boost if odds boost is not possible
   */
  private checkBetslipSelections(): void {
    if (
      this.betslipDataService.bets.length &&
      this.isOddsBoostEnabled() &&
      this.isBoostActive() &&
      !this.canBoostSelections()
    ) {
      this.pubSubService.publish(this.pubSubService.API.ODDS_BOOST_CHANGE, false);
    }
  }

  private getDailyBoosts(bet: Bet): IOddsBoost[] {
    const dailyBoosts = bet.params.oddsBoosts.filter((token: IOddsBoost) => {
      return (
        !token.freebetOfferType &&
        this.getBetLevel(token) === 'ANY'
      );
    });

    dailyBoosts.sort((token1: IOddsBoost, token2: IOddsBoost) => {
      return new Date(token1.expiry).getTime() - new Date(token2.expiry).getTime();
    });

    return dailyBoosts;
  }

  private useDailyBoost(bets: Bet[]): void {
    // don't use daily boost if Acca token selected
    const accaBet = bets.find((bet: Bet) => {
      const type = bet.oddsBoost && bet.oddsBoost.sorting.type;
      return type && type !== 'SGL';
    });
    if (accaBet) {
      return;
    }

    const boostableBets = bets.filter((bet: Bet) => {
      return !bet.disabled && bet.params.oddsBoosts && bet.params.oddsBoosts.length;
    });

    // don't use daily boost if all bets boosted
    if (!boostableBets.some((bet: Bet) => !bet.oddsBoost)) {
      return;
    }

    boostableBets.forEach((bet: Bet) => {
      const dailyBoosts = this.getDailyBoosts(bet);
      if (!dailyBoosts.length) {
        return;
      }
      bet.oddsBoost = dailyBoosts[0];
    });
  }

  private keepPopupHidden(): boolean {
    let keepPopupHidden = false;
    let { allowUserToToggleVisibility, daysToKeepPopupHidden } = this.cmsService.initialData.oddsBoost;

    allowUserToToggleVisibility = allowUserToToggleVisibility || false;
    daysToKeepPopupHidden = daysToKeepPopupHidden || 0;
    const popupData = this.storageService.get('keepOddsBoostPopupHidden') || {};
    const hideOddsBoostDateForUser = Date.parse(popupData[`setDate-${this.userService.username}`] || null);

    let daysPassed = 0;
    if (allowUserToToggleVisibility && hideOddsBoostDateForUser && daysToKeepPopupHidden > 0) {
      const currentDate = Date.now();
      daysPassed = Math.round((currentDate - hideOddsBoostDateForUser) / 86400000); // 1000[ms] * 60[s] * 60[s] * 24[h]
      if (daysPassed < daysToKeepPopupHidden) {
        keepPopupHidden = true;
      }
    }
    return keepPopupHidden;
  }
  sendGTM(eventPosition: string, eventDetails: string, eventAction: string, type?: string): void {
    this.gtmService.push('trackEvent',   {
      'event': (type === 'trackEvent') ? 'Event.Tracking' : 'contentView',
      'component.CategoryEvent': 'bets boost',
      'component.LabelEvent': 'free bet alert',
      'component.ActionEvent': eventAction,
      'component.PositionEvent': eventPosition,
      'component.LocationEvent': 'free bet alert',
      'component.EventDetails': eventDetails,
      'component.URLClicked': 'not applicable'
    });
  }
}
