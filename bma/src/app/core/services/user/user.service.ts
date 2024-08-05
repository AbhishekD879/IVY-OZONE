import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { PubSubService } from '../communication/pubsub/pubsub.service';
import { StorageService } from '../storage/storage.service';
import { IUserDataModel } from './user-data.model';
import { IRetailCard } from '@app/core/services/user/retail-card.model';
import environment from '@environment/oxygenEnvConfig';
import { ROULETTE_JOURNEY_KEY } from '@bma/constants/roulette-journey.constant';
import { Params } from '@angular/router';
import { LocaleService } from '@core/services/locale/locale.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
@Injectable()
export class UserService extends IUserDataModel {
  userFinishedLogin: boolean = true;
  removeUsernameCookie: boolean = true;
  private retailCardCreds: IRetailCard = null;
  private openApiAuthPromise: Promise<any>;
  private openApiAuthPromiseResolve: (value?: any | PromiseLike<{}>) => void;
  private openApiAuthPromiseReject: (value?: any | PromiseLike<{}>) => void;
  private openApiAuthIsPending = false;

  private proxyAuthPromise: Promise<any>;
  private proxyAuthPromiseResolve: (value?: any | PromiseLike<{}>) => void;
  private proxyAuthPromiseReject: (value?: any | PromiseLike<{}>) => void;
  private proxyAuthPromiseIsPending = false;
  private readonly DEFAULT_DEPOSIT_MINIMUM_AMOUNT: number = 5;

  constructor(
    public storage: StorageService,
    public pubsub: PubSubService,
    private localeService: LocaleService,
    private windowRef: WindowRefService) {
    super(storage);

    this.initOpenApiPromise();
    this.initproxyAuthPromise();

    this.restore();
  }

  getRetailCard() {
    return this.retailCardCreds;
  }

  /**
   * Initializes new authentication promises only in case if previous promises when resolved/rejected.
   */
  initAuthPromises(): void {
    if (!this.openApiAuthIsPending) {
        this.initOpenApiPromise();
    }
    if (!this.proxyAuthPromiseIsPending) {
        this.initproxyAuthPromise();
    }
  }

  // OPENAPI PROMISES
  getOpenApiAuth(): Promise<void> {
    return this.openApiAuthPromise;
  }
  resolveOpenApiAuth(): void {
    this.openApiAuthPromiseResolve();
    this.openApiAuthIsPending = false;
  }
  rejectOpenApiAuth(): void {
    this.openApiAuthPromiseReject('rejecting OpenApiAuth');
    this.openApiAuthIsPending = false;
  }

  // BPP PROMISES
  initProxyAuth(): void {
    if (!this.proxyAuthPromiseIsPending) {
      this.initproxyAuthPromise();
    }
  }
  getProxyAuth(): Promise<any> {
    return this.isInShopUser() ? Promise.resolve({}) : this.proxyAuthPromise;
  }
  resolveProxyAuth(): void {
    this.proxyAuthPromiseResolve();
    this.proxyAuthPromiseIsPending = false;
  }
  rejectProxyAuth(): void {
    this.proxyAuthPromiseReject();
    this.proxyAuthPromiseIsPending = false;
  }

  proxyPromiseResolved(): boolean {
    return !this.proxyAuthPromiseIsPending;
  }

  setExternalCookies(): void {
    if (Boolean(this.windowRef.nativeWindow.NativeBridge)) {
      this.storage.setCookie('X_MB_NATIVE', 'true', environment.DOMAIN, 365, true);
    } else {
      this.removeNativeCookie();
    }

    if (this.status) {
      this.storage.setCookie('userLoginTime', this.previousLoginTime, environment.DOMAIN, 365, true);
      this.setSportsUserName(this.username);
      this.storage.setCookie('sportsbookToken', this.sessionToken, environment.DOMAIN, 365, true);
    } else {
      this.removeExternalCookies();
    }
  }
  // setSportUserName
  setSportsUserName(userName: string) {
    if (!this.storage.getCookie('sportsbookUsername')) {
      this.storage.setCookie('sportsbookUsername', userName, environment.DOMAIN, 365, true);
    }
  }

  /**
   * Checks if the name of current user is the same as stored username value.
   * @return {boolean}
   */
  isRestoredBppUser(): boolean {
    const lastBppUsername: string = this.storage.get('previousBppUsername');
    return this.bppToken && _.isString(lastBppUsername) && _.isString(this.username) &&
      lastBppUsername.toLowerCase() === this.username.toLowerCase();
  }

  setTouchIdLogin(value): void {
    this.storage.setCookie('touchIdLogin', value);
  }

  getTouchIdLogin(): string {
    return this.storage.getCookie('touchIdLogin') || 'disabled';
  }

  login(sessionToken: string): void {
    this.set({
      sessionToken,
      status: true,
      loginPending: false,
      bonusSuppression: this.getPostLoginBonusSupValue()
    });
    this.storage.get('betPackMarketBanner')==null&&this.storage.set('betPackMarketBanner',true);
    this.storage.get('betPackReviewBanner')==null&&this.storage.set('betPackReviewBanner',true);
    this.setExternalCookies();
  }

  /**
   * Fetches the post login cookie values and returns bonus suppresion value
   * @returns {boolean} 
   */
  getPostLoginBonusSupValue(): boolean {
    return this.storage.getCookie('mobileLogin.PostLoginValues')?.['bonusSuppression'] || false;
  }

  /**
   * Logout
   * @param {boolean} isNotify
   */
  logout(isNotify: boolean = true): void {
    // reject previously created promises, before creating new.
    // case for logout by server, when token is not valid.
    this.rejectPromises();
    this.initAuthPromises();

    // Clear price modifiers from local storage
    this.storage.remove('priceModifiers');
    this.storage.remove('89901');
    this.storage.removeCookie('isModifiedPriceValid');
    //remove the banner details
    this.storage.remove('betPackReviewBanner');
    this.storage.remove('betPackMarketBanner');
    this.toteBetReset();
    this.removeExternalCookies();
    this.removeNativeCookie();
    this.resetData();

    if (isNotify) {
      this.pubsub.publish(this.pubsub.API.SESSION_LOGOUT);
    }

    this.retailCardCreds = null;
  }
  toteBetReset() {
    this.storage.remove('toteFreeBets');
    this.storage.remove('toteBetPacks');
    this.storage.remove('usedToteFreebets');  
    const toteBet = this.storage.get('toteBet');
    if (toteBet && toteBet.poolBet) {
      if (toteBet.poolBet.freebetTokenId) {
        delete toteBet.poolBet.freebetTokenId;
      }
      if (toteBet.poolBet.freebetTokenValue) {
        delete toteBet.poolBet.freebetTokenValue;
      }
      this.storage.set('toteBet', toteBet);
    }
  }
  rememberRetailCredentials(cardNumber: string, cardPin: number): void {
    this.retailCardCreds = { cardNumber, cardPin };
  }

  breakRouletteJourney(reason: string = 'page closed') {
    if (this.isRouletteJourney()) {
      this.storage.remove(ROULETTE_JOURNEY_KEY);
      this.pubsub.publish(this.pubsub.API.ROULETTE_JOURNEY_END);
      console.warn(`Breaking roulette journey (${reason})`);
    }
  }

  /**
   * Check possibility - query contains specific params, user is not logged in yet
   *
   * @param {Params} queryParams
   * @return boolean
   * NOTE: desirable to remove this and all calls (bma-main, featured-tab components) after Roulette User migration
   */
  canActivateJourney(queryParams: Params): boolean {
    return !!(queryParams['targetPage'] && queryParams['referrerPage'] && !this.status);
  }

  /**
   * Get params from window.location.href to detect user upgrade journey
   * Note: do not use ActivatedRouteSnapshot because sometimes it is empty
   * @param {string} href
   * @return Params
   * NOTE: desirable to remove this and all calls (bma-main, featured-tab components) after Roulette User migration
   */
  getJourneyParams(href: string): Params {
    const url = new URL(href),
      targetPage = url.searchParams && url.searchParams.get('targetPage'),
      referrerPage = url.searchParams && url.searchParams.get('referrerPage');

    return {
      targetPage,
      referrerPage
    };
  }

  get checkZeroBalance(): boolean {
    return Number(this.sportBalance) === 0;
  }
  set checkZeroBalance(value:boolean){}

  /**
   * Get amount for bet for different cases
   * @param {string | amount} amount
   * @param {boolean} isBetslip - flag not to count amount as from Betslip we already get needed amount for placing bet
   * and from quickbet we get just stake
   */
  getUserDepositNeededAmount(amount: string | number, isBetslip: boolean): string {
    let amountNumber;
    const isNeededAmountLessDefault = Number(amount) < Number(this.DEFAULT_DEPOSIT_MINIMUM_AMOUNT);
    const islessDefaultBetslip = isBetslip && isNeededAmountLessDefault;
    const isBalanceIsLessNeedAmount = Number(this.sportBalance) < Number(amount);
    const isBalanceDiffLessDefault = (Number(amount) - Number(this.sportBalance)) < Number(this.DEFAULT_DEPOSIT_MINIMUM_AMOUNT);
    // if isBetslip = true it means that amount field is already calculated and equal to neededAmountForPlaceBet
    const checkDefault = (isBalanceIsLessNeedAmount && isBalanceDiffLessDefault && !isBetslip)
      || (isNeededAmountLessDefault && this.checkZeroBalance)
      || islessDefaultBetslip;

    if (checkDefault) {
      amountNumber = this.DEFAULT_DEPOSIT_MINIMUM_AMOUNT;
    } else if (isBetslip) {
      amountNumber = Number(amount);
    } else {
      amountNumber = (Number(amount) - Number(this.sportBalance));
    }
    return amountNumber.toFixed(2);
  }

  /**
   * Get proper deposit message
   * @param {string | amount} amount
   * @param {boolean} isBetslip
   */
  getUserDepositMessage(amount: string | number, isBetslip: boolean): string {
    const amountNumber = this.getUserDepositNeededAmount(amount, isBetslip);

    return this.localeService.getString('bs.betslipDepositNotification',
      [ this.currencySymbol + amountNumber ]);
  }

  removeNativeCookie(): void {
    this.storage.removeCookie('X_MB_NATIVE');
  }

  getLoggedInUser(): string {
    return this.storage.getCookie('sportsbookUsername');
  }

  private rejectPromises() {
    if (this.openApiAuthPromiseReject && this.proxyAuthPromiseReject) {
      this.rejectOpenApiAuth();
      this.rejectProxyAuth();
    }
  }

  private initOpenApiPromise(): void {
    this.openApiAuthIsPending = true;
    const promise = new Promise((resolve, reject) => {
      this.openApiAuthPromiseResolve = resolve;
      this.openApiAuthPromiseReject = reject;
    });

    promise.catch(this.errorHandler);

    this.openApiAuthPromise = promise;
  }

  private initproxyAuthPromise(): void {
    this.proxyAuthPromiseIsPending = true;
    const promise = new Promise((resolve, reject) => {
      this.proxyAuthPromiseResolve = resolve;
      this.proxyAuthPromiseReject = reject;
    });

    promise.catch(this.errorHandler);

    this.proxyAuthPromise = promise;
  }

  private errorHandler(error: string): void {
    if (!error) { return; }
    console.warn(error);
  }

  private restore(): void {
      const sessionToken = this.storage.getCookie('sportsbookToken');
      const username = this.storage.getCookie('sportsbookUsername');

      this.set(this.storage.get('USER'), sessionToken && username ? { sessionToken, username } : {});
  }

  private removeExternalCookies(): void {
    this.storage.removeCookie('userLoginTime');
    this.storage.removeCookie('sportsbookToken');
    if (this.removeUsernameCookie) {
      this.storage.removeCookie('sportsbookUsername');
    } else {
      this.removeUsernameCookie = true;
    }
  }
}
