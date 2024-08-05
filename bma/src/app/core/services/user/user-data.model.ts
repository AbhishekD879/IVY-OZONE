import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { StorageService } from '../storage/storage.service';
import { ROULETTE_JOURNEY_KEY } from '@bma/constants/roulette-journey.constant';

const defaultData = {
  // main
  bppToken: null,
  sessionToken: null,
  username: null,
  // balances
  sportBalance: null,
  sportBalanceWithSymbol: null,
  pendingWithdrawals: null,
  // user info
  advertiser: null,
  address: null,
  accountBusinessPhase: null,
  accountClosed: false,
  maxStakeScale: null,
  ageVerificationStatus: null,
  birthDate: '',
  cardNumber: '',
  city: '',
  countryCode: null,
  currencySymbol: '£',
  currency: 'GBP',
  custId: '',
  email: null,
  firstname: null,
  firstNews: null,
  lastname: null,
  loginPending: false,
  logoutPending: false,
  oddsFormat: 'frac',
  pin: null,
  playerCode: null,
  playerDepositLimits: null,
  postCode: null,
  previousLoginTime: null,
  profileId: null,
  sessionLimit: 0,
  signupDate: '',
  tcVersion: null,
  vipLevel: null,
  vipInfo: null,
  contactPreferences: null,
  payPalBA: '',
  payPalDepositFraudNetScriptsLoaded: false,

  // states
  firstLogin: false,
  isTemporaryCard: false,
  passwordResetLogin: false,
  previouslyLogged: false,
  quickDepositTriggered: false,
  showBalance: true,
  isRedirecting: false,
  isSignUpPending: false,
  showLogoutPopup: true,
  status: false,
  quickBetNotification: true,
  timeline: true,
  logInMessage: [],
  winAlertsToggled: false,
  lastBet: '',
  bonusSuppression: false
};

@Injectable()
export class IUserDataModel {

  public data: any = (_.clone(defaultData));

  constructor(
    public storage: StorageService
  ) {}

  set(...x) {
    _.extend(this.data, ...x);

    this.storage.set('USER', this.data);
  }

  get bonusSuppression() {
    return this.data.bonusSuppression;
  }
  set bonusSuppression(value:any){}

  get bppToken() {
    return this.data.bppToken;
  }
  set bppToken(value:any){}
  get sessionToken() {
    return this.data.sessionToken;
  }
  set sessionToken(value:any){}
  get username() {
    return this.data.username;
  }
  set username(value:any){}
  get sportBalance(): string | number {
    return this.data.sportBalance;
  }
  set sportBalance(value: string | number){}
  get sportBalanceWithSymbol() {
    return this.data.sportBalanceWithSymbol;
  }
  set sportBalanceWithSymbol(value:any){}
  get pendingWithdrawals() {
    return this.data.pendingWithdrawals;
  }
  set pendingWithdrawals(value:any){}
  get advertiser() {
    return this.data.advertiser;
  }
  set advertiser(value:any){}
  get accountBusinessPhase() {
    return this.data.accountBusinessPhase;
  }
  set accountBusinessPhase(value:any){}
  get ageVerificationStatus() {
    return this.data.ageVerificationStatus;
  }
  set ageVerificationStatus(value:any){}
  get accountClosed() {
    return this.data.accountClosed;
  }
  set accountClosed(value:any){}
  get cardNumber() {
    return this.data.cardNumber;
  }
  set cardNumber(value:any){}
  get countryCode() {
    return this.data.countryCode;
  }
  set countryCode(value:any){}
  get currency(): string {
    return this.data.currency;
  }
  set currency(value:string){}
  get currencySymbol(): string {
    return this.data.currencySymbol;
  }
  set currencySymbol(value:string){}
  get custId(): string {
    return this.data.custId;
  }
  set custId(value:string){}
  get email() {
    return this.data.email;
  }
  set email(value:any){}
  get firstname() {
    return this.data.firstname;
  }
  set firstname(value:any){}
  get firstNews() {
    return this.data.firstNews;
  }
  set firstNews(value:any){}
  get lastname() {
    return this.data.lastname;
  }
  set lastname(value:any){}
  get loginPending() {
    return this.data.loginPending;
  }
  set loginPending(value:any){}
  get logoutPending() {
    return this.data.logoutPending;
  }
  set logoutPending(value:any){}
  set isManualLogout(value: boolean){}
  get isManualLogout() {
    return this.data.isManualLogout;
  }
  get LCCP() {
    return this.data.LCCP;
  }
  set LCCP(value:any){}
  get oddsFormat() {
    return this.data.oddsFormat;
  }
  set oddsFormat(value:any){}
  get timeline() {
    return this.data.timeline;
  }
  set timeline(value:any){}
  get previouslyLogged() {
    return this.data.previouslyLogged;
  }
  set previouslyLogged(value:any){}
  get quickDepositTriggered() {
    return this.data.quickDepositTriggered;
  }
  set quickDepositTriggered(value:any){}
  get previousLoginTime() {
    return this.data.previousLoginTime;
  }
  set previousLoginTime(value:any){}
  get playerCode() {
    return this.data.playerCode;
  }
  set playerCode(value:any){}
  get playerDepositLimits() {
    return this.data.playerDepositLimits;
  }
  set playerDepositLimits(value:any){}
  get postCode() {
    return this.data.postCode;
  }
  set postCode(value:string){}
  get profileId() {
    return this.data.profileId;
  }
  set profileId(value:any){}
  get signupDate() {
    return this.data.signupDate;
  }
  set signupDate(value:any){}
  get sessionLimit() {
    return this.data.sessionLimit;
  }
  set sessionLimit(value:any){}
  get tcVersion() {
    return this.data.tcVersion;
  }
  set tcVersion(value:any){}
  get vipLevel() {
    return this.data.vipLevel;
  }
  set vipLevel(value:any){}
  get vipInfo() {
    return this.data.vipInfo;
  }
  set vipInfo(value:any){}
  get firstLogin() {
    return this.data.firstLogin;
  }
  set firstLogin(value:any){}
  get isTemporaryCard() {
    return this.data.isTemporaryCard;
  }
  set isTemporaryCard(value:any){}
  get passwordResetLogin() {
    return this.data.passwordResetLogin;
  }
  set passwordResetLogin(value:any){}
  get isRedirecting() {
    return this.data.isRedirecting;
  }
  set isRedirecting(value:string){}
  get showBalance() {
    return this.data.showBalance;
  }
  set showBalance(value:any){}
  get showLogoutPopup() {
    return this.data.showLogoutPopup;
  }
  set showLogoutPopup(value:any){}
  get status(): boolean {
    return this.data.status;
  }
  set status(value:boolean){}
  get maxStakeScale(): string {
    return this.data.maxStakeScale;
  }
  set maxStakeScale(value:string){}
  get quickBetNotification() {
    return this.data.quickBetNotification;
  }
  set quickBetNotification(value:any){}
  get contactPreferences() {
    return this.data.contactPreferences;
  }
  set contactPreferences(value:any){}
  get payPalBA() {
    return this.data.payPalBA;
  }
  set payPalBA(value:any){}
  get payPalDepositFraudNetScriptsLoaded() {
    return this.data.payPalDepositFraudNetScriptsLoaded;
  }
  set payPalDepositFraudNetScriptsLoaded(value:any){}
  get isSignUpPending() {
    return this.data.isSignUpPending;
  }
  set isSignUpPending(value:any){}
  get logInMessage(): string[] {
    return this.data.logInMessage;
  }
  set logInMessage(value:string[]){}
  get winAlertsToggled(): boolean {
    return this.data.winAlertsToggled;
  }
  set winAlertsToggled(value:boolean){}
  get lastBet(): string {
    return this.data.lastBet;
  }
  set lastBet(value:string){}

  isRouletteJourney(): boolean {
    return !!this.storage.get(ROULETTE_JOURNEY_KEY);
  }

  isInShopUser(): boolean {
    return this.data.accountBusinessPhase === 'in-shop';
  }

  isMultiChannelUser(): boolean {
    return this.data.accountBusinessPhase === 'multi-channel';
  }

  isRetailUser(): boolean {
    return this.isInShopUser() || this.isMultiChannelUser();
  }

  resetData() {
    const changelessKeys = ['oddsFormat', 'timeline', 'quickBetNotification', 'logoutPending'];

    this.set(_.omit(defaultData, changelessKeys));
  }
}
