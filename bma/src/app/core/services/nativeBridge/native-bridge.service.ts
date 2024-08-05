import { DOCUMENT } from '@angular/common';
import { Inject, Injectable } from '@angular/core';
import { Router, Event, NavigationEnd } from '@angular/router';
import * as _ from 'underscore';

import { DeviceService } from '@core/services/device/device.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { UserService } from '@core/services/user/user.service';
import { INaviveBridgeDetails } from './native-bridge.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { LIVE_STREAM_CONFIG } from '@sb/sb.constant';
import { Observable, ReplaySubject } from 'rxjs';

@Injectable()
export class NativeBridgeService {

  isWrapper: boolean;
  private isWrapperSubject: ReplaySubject<boolean> = new ReplaySubject();
  private bridge: any;

  constructor(
    private command: CommandService,
    @Inject(DOCUMENT) private document: any,
    private windowRef: WindowRefService,
    private pubsub: PubSubService,
    private user: UserService,
    private router: Router,
    private deviceService: DeviceService
  ) {
    this.bridge = this.windowRef.nativeWindow.NativeBridge;
    this.isWrapper = !!this.bridge;
    this.isWrapperSubject.next(this.isWrapper);
  }

  /**
   * initialise app listeners to use native bridge
   */
  init(): void {
    if (this.isWrapper) {
      this.pubsub.subscribe('nativeBridgeFactory', this.pubsub.API.SET_ODDS_FORMAT,
        (oddsFormatData: any) => this.onOddsSettingsChanged(oddsFormatData));
      this.pubsub.subscribe('nativeBridgeFactory', this.pubsub.API.SYNC_BETSLIP_TO_NATIVE,
        (outcomes: Array<string>) => this.syncBetSlipToNative(outcomes));
      this.command.executeAsync(this.command.API.BETSLIP_READY)
        .then(() => this.syncBetSlipFromNative());
      this.pubsub.subscribe('nativeBridgeFactory', this.pubsub.API.USER_BALANCE_SHOW,
          (settingValue: any) => this.showUserBalance(settingValue));
      this.pubsub.subscribe('nativeBridgeFactory', this.pubsub.API.SYNC_FAVOURITES_TO_NATIVE,
        (event: ISportEvent[]) => this.syncFavouritesToNative(event));

      if (_.isFunction(this.bridge.hideSplashScreen)) {
        this.pubsub.subscribe('nativeBridgeFactory', this.pubsub.API.APP_IS_LOADED, () => this.hideSplashScreen());
      }

      this.document.addEventListener('CURRENT_WATCH_LIVE_STATE_CHANGED', e => {
        this.playerStatus = e.detail.settingValue;
      });
      this.document.addEventListener('syncBetSlip', () => this.syncBetSlipFromNative());
      this.document.addEventListener('CHANGE_BET_SLIP_SLIDE_STATE', (event: CustomEvent) => this.openSlideOutBetSlip(event));
      this.document.addEventListener('syncFavourites', () => this.syncFavouritesFromNative());
      this.document.addEventListener('openPromotionWithType', e => {
        this.command.executeAsync(this.command.API.PROMOTIONS_SHOW_OVERLAY, [e.detail.settingValue], 'defaultResult');
      });
      this.document.addEventListener('showOptInSplashScreen', () => this.showOptInSplashScreen());
      this.document.addEventListener('showMarketingPreferencePage', () => this.showMarketingPreferencePage());
      this.document.addEventListener('ADD_TO_QUICKBET', e => {
        this.pubsub.publish(this.pubsub.API.SYNC_NATIVE_QUICKBET_SELECTION, e.detail.selectionId);
      });

      this.document.addEventListener('virtualSportSelected', e => {
        this.pubsub.publish(this.pubsub.API.VIRTUAL_ORIENTATION_CHANGED, `${e.detail}`);
      });

      this.document.addEventListener('streamAndBetPlaced', e => {
        this.pubsub.publish(this.pubsub.API.BETS_COUNTER_PLACEBET, e.detail && e.detail.placedBetsCount || 0);
      });

      this.document.addEventListener('onCookieBannerAccept', e => {
        if (e.detail) {
          this.pubsub.publish(this.pubsub.API.NATIVE_COOKIE_BANNER_CLOSED, e.detail);
        }
      });

      this.document.addEventListener('onCheckConnectReceived', e => { // TODO: rename to retail after changes in native.
        this.pubsub.publish(this.pubsub.API.CHECK_RETAIL_NATIVE, e.detail);
      });

      this.document.addEventListener('onCheckGridReceived', isAppStatus => {
        this.pubsub.publish(this.pubsub.API.CHECK_RETAIL_NATIVE, isAppStatus.detail);
      });

      this.document.addEventListener('onOrientationChanged', e => {
        this.pubsub.publish(this.pubsub.API.ORIENTATION_CHANGED, e.detail);
      });

      /**
       * @description Add event listener on event TOUCH_ID_CHANGED
       * this event dispatched when user changed Touch Id Login setting on native wrapper app
       * it could be on the native login dialogue, or if fail touch id login ...
       */
      this.document.addEventListener('TOUCH_ID_CHANGED', (data: INaviveBridgeDetails) => {
        this.user.setTouchIdLogin(data.detail.settingValue);
      });

      this.document.addEventListener('videoPlayerCollapsed', e => {
        this.pubsub.publish(this.pubsub.API.IS_NATIVE_VIDEO_STICKED, !e.detail.state);
      });

      this.document.addEventListener('updateBalance', () => {
        this.pubsub.publish(this.pubsub.API.IMPLICIT_BALANCE_REFRESH);
      });

      this.document.addEventListener('onBuildVersionReceived', (appBuildVersion: INaviveBridgeDetails) => {
        this.pubsub.publish(this.pubsub.API.APP_BUILD_VERSION, appBuildVersion.detail.versionValue);
      });

      this.document.addEventListener('onBetSharingCompleted', data => {
        this.pubsub.publish(this.pubsub.API.BET_SHARING_COMPLETED, data);
      });

      this.router.events.subscribe((event: Event) => {
        if (event instanceof NavigationEnd) {
          this.onUrlChanged(this.windowRef.nativeWindow.location.href);
        }
      });
    }
  }

  /**
   * returns observable which emits isWrapper value
   */
  get isWrapperStream(): Observable<boolean> {
    return this.isWrapperSubject.asObservable();
  }
  set isWrapperStream(value:Observable<boolean>){}
  /**
   * returns duration for close betslip sidebar animation
   * @returns {number}
   */
  get betSlipCloseAnimationDuration(): number {
    return this.isWrapper && this.bridge.betSlipCloseAnimationDuration ? this.bridge.betSlipCloseAnimationDuration : 500;
  }
  set betSlipCloseAnimationDuration(value:number){}
  /**
   * Return TouchIDConfigured value
   * @return {boolean}
   */
  get touchIDConfigured(): boolean {
    return this.isWrapper && (this.bridge.touchIDConfigured === 'true' || this.bridge.touchIDConfigured === true);
  }
  set touchIDConfigured(value:boolean){}
  /**
   * Return betslip selections
   * @return {string[]}
   */
  get betSelections(): Array<string> {
    return this.isWrapper && this.bridge.betSelections ? this.bridge.betSelections : null;
  }
  set betSelections(value:Array<string>){}
  /**
   * Return favorites
   * @return {*}
   */
  get favourites(): Array<any> {
    return this.isWrapper && this.bridge.favourites ? this.bridge.favourites : null;
  }
  set favourites(value:Array<any>){}
  /**
   * Return NativeBridge.creferer value
   */
  get creferer(): any {
    return this.isWrapper && this.bridge.creferer ? this.bridge.creferer : null;
  }
  set creferer(value:any){}
  /**
   * Return NativeBridge.tdpeh value
   */
  get tdpeh(): string {
    return this.isWrapper && this.bridge.tdpeh || null;
  }
  set tdpeh(value:string){}

  get profileid(): any {
    return this.isWrapper && this.bridge.profileid ? this.bridge.profileid : null;
  }
  set profileid(value:any){}
  /**
   * get NativeBridge.eventStartTime
   */
  get eventStartTime(): string {
    return this.isWrapper && this.bridge.eventStartTime ? this.bridge.eventStartTime : null;
  }
  
  /**
   * Set NativeBridge.startTime value
   * @params {string} startTime
   */
  set eventStartTime(startTime: string) {
    if (this.isWrapper) {
      this.bridge.eventStartTime = startTime;
    }
  }

  /**
   * get NativeBridge.playerStatus
   */
  get playerStatus(): boolean {
    return this.isWrapper && this.bridge.playerStatus ? this.bridge.playerStatus : false;
  }

  /**
   * Set NativeBridge.playerStatus value
   * @params {boolean} value
   */
  set playerStatus(value: boolean) {
    if (this.isWrapper) {
      this.bridge.playerStatus = value;
    }
  }

  /**
   * get NativeBridge.getNativeDialogOpened
   */
  get isNativePage() {
    return this.isWrapper && this.bridge.isNativePage ? this.bridge.isNativePage : false;
  }
 set isNativePage(value:any){}
  /**
   * Check is Mobenga wrapper
   * @returns {boolean}
   */
  get isMobengaWrapper() {
    return !!this.windowRef.nativeWindow.CoralAndroid || this.windowRef.document['Native'];
  }
  set isMobengaWrapper(value:string){}
  get pushNotificationsEnabled(): boolean {
    return this.isWrapper && this.bridge.pushNotificationsEnabled;
  }
  set pushNotificationsEnabled(value:boolean){}
  get isRemovingGamingEnabled(): boolean {
    return this.isWrapper && this.bridge.isRemovingGamingEnabled ? this.bridge.isRemovingGamingEnabled : false;
  }
  set isRemovingGamingEnabled(value:boolean){}
  /**
   * Check for deviceType and calls for buildVersion
   */
  getBuildVersion(): void {
    if (this.isWrapper && this.deviceService.isIos && typeof this.bridge.getBuildVersion === 'function') {
      this.bridge.getBuildVersion();
    }
  }

  /**
   * Check for deviceType and calls for betPlaceSuccessful
   */
   betPlaceSuccessful(receiptId: string, categoryName?: string, betType?: string): void {
    if (this.isWrapper && typeof this.bridge.betPlaceSuccessful === 'function') {
      this.bridge.betPlaceSuccessful(receiptId, categoryName, betType);
    }
  }

  /**
   * Determine the mobile operating system.
   * This function returns one of 'ios', 'android', 'wp', or 'unknown'.
   *
   * @returns {String}
   */
  getMobileOperatingSystem(): string {
    const userAgent = this.windowRef.nativeWindow.navigator.userAgent || this.windowRef.nativeWindow.navigator.vendor
      || this.windowRef.nativeWindow.opera;

    // Windows Phone must come first because its UA also contains 'Android'
    if (/windows phone/i.test(userAgent)) {
      return 'wp';
    }

    if (/android/i.test(userAgent)) {
      return 'android';
    }

    // iOS detection from: http://stackoverflow.com/a/9039885/177710
    // iOS 13 iPad user agent string do not contain 'iPad' word
    if ((/iPad|iPhone|iPod/.test(userAgent) || this.isWrapper && userAgent.indexOf('Macintosh') > -1)
      && !this.windowRef.nativeWindow.MSStream) {
      return 'ios';
    }

    return 'unknown';
  }

  /**
   * Login Native Bridge method
   * @params {string} playerCode
   * @params {string} pass
   */
  loginIfExist(playerCode: string, pass: string) {
    if (this.isWrapper && _.isFunction(this.bridge.login)) {
      if (this.touchIDConfigured) {
        // add pass as second parameter if touch ID Login
        this.bridge.login(playerCode, pass);
      } else {
        this.bridge.login(playerCode);
      }
    }
  }

  loginSalesForce(accountId: string): void {
    if (this.isWrapper && _.isFunction(this.bridge.loginSalesForce)) {
      this.bridge.loginSalesForce(accountId);
    }
  }

  /**
   * Login with Touch ID Native Bridge method
   * @params {bool} placeBet
   * @params {string} msg
   * @params {bool} disable
   */
  loginWithTouchID(placeBet: boolean, msg: string, disable: boolean) {
    this.bridge.loginWithTouchID(placeBet, msg, disable);
  }

  /**
   * Return TouchIDConfigured value
   * @return {boolean}
   */
  isLoginDialog(): boolean {
    return this.isWrapper && _.isFunction(this.bridge.openNativeLoginDialog);
  }

  /**
   * Open Login Dialog with Native Bridge method
   */
  openLoginDialog(...args: Array<any>) {
    this.bridge.openNativeLoginDialog.apply(this, args);
  }

  /**
   * Touch ID Login Failed Native bridge method
   * @params {string|object} error
   */
  touchIDLoginFailedIfExist(error: any) {
    // iOS error handler
    if (this.isWrapper && this.touchIDConfigured && _.isFunction(this.bridge.touchIDLoginFailed)) {
      this.bridge.touchIDLoginFailed(error);
    }

    // Android error handler
    if (this.isWrapper && this.touchIDConfigured && _.isFunction(this.bridge.onFingerPrintLoginFailed)) {
      this.bridge.onFingerPrintLoginFailed(error.code, error.msg);
    }
  }

  /**
   * Touch ID Settings Update Native bridge method
   * @params {boolean} settings value
   */
  touchIDSettingsUpdate(value: boolean) {
    if (this.isWrapper && this.touchIDConfigured && _.isFunction(this.bridge.touchIDSettingsUpdate)) {
      this.bridge.touchIDSettingsUpdate(value);
    }
  }

  /**
   * Get player bets Native bridge method
   * @params {number} count
   */
  syncPlayerBetSlip(count: number) {
    if (this.isWrapper && _.isFunction(this.bridge.syncPlayerBetSlip)) {
      this.bridge.syncPlayerBetSlip(count);
    }
  }

  /**
   * Call acca notification Native bridge method
   * @param {Object} obj
   * @param {string} obj.title
   * @param {string} obj.price
   */
  accaNotificationChanged({ title, price }: { [key: string]: string } = {}): void {
    if (this.isWrapper && _.isFunction(this.bridge.accaNotificationChanged)) {
      this.bridge.accaNotificationChanged(title || '', price || '');
    }
  }

  /**
   * Logout Native bridge method
   */
  logout(): void {
    if (this.isWrapper) {
      if (_.isFunction(this.bridge.logout)) {
        this.bridge.logout();
      }
      if (_.isFunction(this.bridge.showUserBalance)) {
        this.bridge.showUserBalance(true);
      }
    }
  }

  /**
   * Deposit Native bridge method
   * @params {string} currency
   * @params {number} amount
   */
  depositIfExist(currency: string, amount: number) {
    if (this.isWrapper && _.isFunction(this.bridge.deposit)) {
      this.bridge.deposit(currency, amount);
    }
  }

  /**
   * Create temporary js-frame for disable native splash
   */
  createMobengaIframe(): void {
    const ifrm = this.document.createElement('iframe');
    ifrm.setAttribute('src', 'js-frame:data;animationAction=execute;');
    ifrm.style.width = '0px';
    ifrm.style.height = '0px';
    this.document.body.appendChild(ifrm);
    this.document.body.removeChild(ifrm);
  }

  /**
   * Show video Native bridge method
   * @param {string} videoUrl
   * @param {number} eventId
   * @param {string} categoryCode
   */
  showVideoIfExist(videoUrl: string, eventId: number, categoryCode: string, streamProvider: string): void {
    if (this.isWrapper) {
      if (_.isFunction(this.bridge.showVideoStreamV2)) {
        // BMA-53678
        // Android wrapper v6.3 bridge.showVideoStreamV2 method accepts only 3 parameters.
        // version >= 6.4 will accept 4 parameters
        // window.NativeBridge.id will be defined in Android app versions >= 6.4
        if (!!this.bridge.id) {
          this.bridge.showVideoStreamV2(videoUrl, eventId, categoryCode, streamProvider);
        } else {
          this.bridge.showVideoStreamV2(videoUrl, eventId, categoryCode);
        }
      } else if (_.isFunction(this.bridge.showVideoStream)) {
        this.bridge.showVideoStream(videoUrl);
      }
      this.playerStatus = true;
    }
  }

  /**
   * Hide video Native bridge method
   */
  hideVideoStream(): void {
    if (this.isWrapper && _.isFunction(this.bridge.pauseVideo)) {
      this.bridge.pauseVideo();
    }
  }

  /**
   * Check if wrapper supports video
   *
   * returns {boolean}
   */
  supportsVideo(): boolean {
    return this.isWrapper && (this.bridge.showVideoStream || this.bridge.showVideoStreamV2);
  }

  /**
   * Registration started Native bridge method
   */
  registrationStartedIfExist(): void {
    if (this.isWrapper && _.isFunction(this.bridge.registrationStarted)) {
      this.bridge.registrationStarted();
    }
  }

  /**
   * Registration finished Native bridge method
   * @params {string} playerCode
   * @params {string} pass
   */
  registrationFinishedIfExist(playerCode: string = '', pass: string = ''): void {
    if (this.isWrapper && _.isFunction(this.bridge.registrationFinished)) {
      if (this.touchIDConfigured) {
        // add pass as second parameter if touch ID Login
        this.bridge.registrationFinished(playerCode, pass);
      } else {
        this.bridge.registrationFinished(playerCode);
      }
    }
  }

  registrationFinishedSalesForce(accountId: string = ''): void {
    if (this.isWrapper && _.isFunction(this.bridge.registrationFinishedSalesForce)) {
      this.bridge.registrationFinishedSalesForce(accountId);
    }
  }

  /**
   * PasswordChanged Native bridge method
   * @params {string} newPass
   * @params {string} username
   */
  passwordChangedIfExist(newPassword: string, username: string): void {
    if (this.isWrapper && this.touchIDConfigured && _.isFunction(this.bridge.passwordChanged)) {
      this.bridge.passwordChanged(newPassword, username);
    }
  }

  /**
   * Check if wrapper shows football alerts
   * returns {boolean}
   */

  hasOnEventAlertsClick(): boolean {
    return this.isWrapper && _.isFunction(this.bridge.onEventAlertsClick);
  }

  // TODO: Reverted changes from BMA-37049. Will be removed after new approach implementation.
  hasShowFootballAlerts(): boolean {
    return this.isWrapper && _.isFunction(this.bridge.showFootballAlerts);
  }
  // TODO END

  onEventAlertsClick(eventId: string, eventType: string, categoryId: string, drilldownTagNames: string, location: string): void {
    if (this.hasOnEventAlertsClick()) {
      let streamProvider;
      LIVE_STREAM_CONFIG.forEach(provider => {
        if (drilldownTagNames && drilldownTagNames.indexOf(provider.drilldownTagNames) >= 0) {
          streamProvider = provider.type;
        }
      });
      this.bridge.onEventAlertsClick(eventId, eventType, categoryId, streamProvider);
      if (typeof this.bridge.onMatchAlertsClick === 'function') {
        this.bridge.onMatchAlertsClick(JSON.stringify({ location }));
      }
    }
  }

  // TODO: Reverted changes from BMA-37049. Will be removed after new approach implementation.
  showFootballAlerts(): void {
    if (this.hasShowFootballAlerts()) {
      this.bridge.showFootballAlerts();
    }
  }
  // TODO END

  /**
   * Trigger on close Slide Out BetSlip
   */
  onCloseBetSlip(): void {
    if (this.isWrapper && _.isFunction(this.bridge.onCloseBetSlip)) {
      this.bridge.onCloseBetSlip();
    }
  }

  /**
   * Trigger on open Slide Out BetSlip
   */
  onOpenBetSlip(): void {
    if (this.isWrapper && _.isFunction(this.bridge.onOpenBetSlip)) {
      this.bridge.onOpenBetSlip();
    }
  }

  /**
   * Trigger on open Gaming
   */
  onGaming(): void {
    if (this.isWrapper && typeof this.bridge.onGaming === 'function') {
      this.bridge.onGaming();
    }
  }

  /**
   * Trigger on match alerts loaded
   * @params {number[]} eventIds
   * @params {string} categoryName
   */
   multipleEventPageLoaded(eventIds: string[], categoryName: string): void {
    if (this.isWrapper && typeof this.bridge.multipleEventPageLoaded === 'function') {
      const data = {
        eventIds,
        categoryName
      };
      this.bridge.multipleEventPageLoaded(JSON.stringify(data));
    }
  }
  
  /**
   * Trigger on close login dialog
   */
  onCloseLoginDialog(): void {
    if (this.isWrapper && _.isFunction(this.bridge.onCloseLoginDialog)) {
      this.bridge.onCloseLoginDialog();
    }
  }

  /**
   * Trigger on open dialog
   * @identifier {string} dialog identifier
   */
  onOpenPopup(identifier: string): void {
    if (this.isWrapper && _.isFunction(this.bridge.onOpenPopup)) {
      this.bridge.onOpenPopup(identifier);
    }
  }

  /**
   * Trigger on close dialog
   * @identifier {string} dialog identifier
   * @openedDialogs {object} remaining dialogs
   */
  onClosePopup(identifier: string, openedDialogs?: { [name: string]: any }) {
    if (this.isWrapper && _.isFunction(this.bridge.onClosePopup)) {
      this.bridge.onClosePopup(identifier, JSON.stringify(openedDialogs));
    }
  }

  /**
   * get NativeBridge.getNativeDialogOpened
   */
  getNativePageOpened(): boolean {
    return this.isWrapper && this.bridge.isNativePage ? this.bridge.isNativePage : false;
  }

  /**
   * Check if wrapper supports onFeaturedTabClicked function
   */
  hasOnFeaturedTabClicked(): boolean {
    return this.isWrapper && _.isFunction(this.bridge.onFeaturedTabClicked);
  }

  /**
   * Trigger on login popups end
   */
  onLoginPopupsEnd(): void {
    if (this.isWrapper && _.isFunction(this.bridge.onLoginPopupsEnd)) {
      this.bridge.onLoginPopupsEnd();
    }
  }

  /**
   * Launch content of Featured tab for native
   */
  onFeaturedTabClicked(): void {
    this.bridge.onFeaturedTabClicked();
  }

  /**
   * trigger on right menu click
   */
  onRightMenuClick(): void {
    if (this.isWrapper && _.isFunction(this.bridge.onRightMenuClick)) {
      this.bridge.onRightMenuClick();
    }
  }

  /**
   * trigger on coookie banner close
   */
  onCookieBannerClosed(): void {
    if (this.isWrapper && _.isFunction(this.bridge.onCookieBannerClosed)) {
      this.bridge.onCookieBannerClosed();
    }
  }

  /**
   * trigger Freebets status
   * @params {boolean} Free Bets status
   */
  onFreeBetUpdated(freeBetsStatus: boolean, data = []): void {
    if (this.isWrapper && _.isFunction(this.bridge.onFreeBetUpdatedV2)) {
      this.bridge.onFreeBetUpdatedV2(freeBetsStatus, JSON.stringify(data));
    } else if (this.isWrapper && _.isFunction(this.bridge.onFreeBetUpdated)) {
      this.bridge.onFreeBetUpdated(freeBetsStatus);
    }
  }

  /**
   * trigger Private Markets state
   * @params {boolean} Private Markets status
   */
  arePrivateMarketsAvailable(privateMarkets: boolean): void {
    if (this.isWrapper && _.isFunction(this.bridge.arePrivateMarketsAvailable)) {
      this.bridge.arePrivateMarketsAvailable(privateMarkets);
    }
  }

  /**
   * trigger Balance change
   * @params {Object} params
   *   - params pendingWithdrawals
   *   - params sportsbookGamingBalance
   */
  onBalanceChanged(balance: { [name: string]: any }): void {
    const amount = balance.amount;
    if (balance && this.isWrapper && _.isFunction(this.bridge.onBalanceChanged)) {
      this.bridge.onBalanceChanged(amount);
    }
  }

  /**
   * Send stream error for native devices
   * @params {string} error type
   */
  showErrorForNative(reason: string): void {
    if (this.isWrapper && _.isFunction(this.bridge.showErrorForNative)) {
      this.bridge.showErrorForNative(reason);
    }
  }

  /**
   * Tells to wrapper when page is ready
   */
  pageLoaded(): void {
    if (this.isWrapper && _.isFunction(this.bridge.pageLoaded)) {
      this.deviceService.isIos ? this.bridge.pageLoaded(this.user.sessionToken) : this.bridge.pageLoaded();
    }
  }

  /**
   * Tells to wrapper when football event detail page is ready
   */
  eventPageLoaded(eventId: string, eventType: string): void {
    if (this.isWrapper && _.isFunction(this.bridge.eventPageLoaded)) {
      this.bridge.eventPageLoaded(eventId, eventType);
    }
  }

  // TODO: Reverted changes from BMA-37049. Will be removed after new approach implementation.
  footballEventPageLoaded(): void {
    if (this.isWrapper && _.isFunction(this.bridge.footballEventPageLoaded)) {
      this.bridge.footballEventPageLoaded();
    }
  }
  // TODO END

  /**
   * Send new abs URL on route change success
   */
  onUrlChanged(url: string): void {
    if (this.isWrapper && _.isFunction(this.bridge.onUrlChanged)) {
      this.bridge.onUrlChanged(url);
    }
  }

  /**
   * Check if wrapper supports Diagnostics function
   */
  isDiagnostics(): boolean {
    return this.isWrapper && _.isFunction(this.bridge.wrapperSendDiagnostics);
  }

  /**
   * Send report
   */
  sendReport(): void {
    this.bridge.wrapperSendDiagnostics();
  }

  /**
   * Pass session token to native bridge
   *
   * @param {Object} params
   *   - params.username - OpenaApi user name;
   *   - params.sessionToken - OpenApi sessionToken;
   *   - params.isFromBetSlip - Indicates if login was made from betslip.
   */
  loginSessionToken(params: { username: string, sessionToken: string, isFromBetSlip: boolean, password: string }): void {
    if (this.isWrapper && _.isFunction(this.bridge.loginSessionToken)) {
      this.bridge.loginSessionToken(JSON.stringify(params));
    }
  }

  /**
   * Login error handler
   */
  loginError(err: any): void {
    if (this.isWrapper && _.isFunction(this.bridge.loginError)) {
      this.bridge.loginError(err);
    }
  }

  /**
   * Callback When user changes session limit
   * @params {Number} sessionLimit
   */
  onSessionLimitChanged(sessionLimit: number): void {
    if (this.isWrapper && _.isFunction(this.bridge.onSessionLimitChanged)) {
      this.bridge.onSessionLimitChanged(sessionLimit);
    }
  }

  /**
   * Callback on toggle balance visibility
   * @params {boolean} settingValue
   */
  showUserBalance(settingValue: any): void {
    if (this.isWrapper && _.isFunction(this.bridge.showUserBalance)) {
      this.bridge.showUserBalance(settingValue);
    }
  }

  /**
   * Synchronize favourites with wrapper
   * @params {*} favourites
   */
  syncFavouritesToNative(data: any): void {
    if (this.isWrapper && _.isFunction(this.bridge.syncFavourites)) {
      this.bridge.syncFavourites(JSON.stringify(data));
    }
  }

  /**
   * Load favourites from native wrapper
   */
  syncFavouritesFromNative(): void {
    const favourites = this.favourites;
    if (_.keys(favourites).length) {
      this.command.execute(this.command.API.SYNC_FAVOURITES_FROM_NATIVE, [favourites]);
    }
  }

  /**
   * Open slide out bet slip from native wrapper
   * @param {Object} data
   */
  openSlideOutBetSlip(data: CustomEvent): void {
    // set $timeout to ensure that all betslip data were loaded
    setTimeout(() => this.pubsub.publish(this.pubsub.API['show-slide-out-betslip'], data.detail.isOpen));
  }

  /**
   * Show Policy banner
   * @param type
   */
  showPolicyBanner(type: any): void {
    if (this.isWrapper && _.isFunction(this.bridge.showPolicyBanner)) {
      console.warn('NativeBridge: showPolicyBanner');
      this.bridge.showPolicyBanner(type);
    }
  }

  /**
   * Event handles if "watch live" button is shown for the event
   */
  onEventDetailsStreamAvailable(eventDetails: {
    categoryId: number;
    classId: number;
    typeId: number;
    eventId: number;
  }): void {
    if (this.isWrapper && _.isFunction(this.bridge.onEventDetailsStreamAvailable) && this.user.status) { //display native stream and bet poup only for logged-in user
      this.bridge.onEventDetailsStreamAvailable(JSON.stringify(eventDetails));
    }
  }

  /**
   * Check if connect native app was used previously
   *
   * @memberof NativeBridgeService
   */
  checkConnect(): void {
    if (this.isWrapper && _.isFunction(this.bridge.checkConnect)) { // TODO: rename to retail after changes in native
      this.bridge.checkConnect();
    }
  }

  /**
   * Check if grid native app was used previously
   * @memberof NativeBridgeService
   * @return {void}
   */
  checkGrid(): void {
    if (this.isWrapper && typeof this.bridge.checkGrid === 'function') {
      this.bridge.checkGrid();
    }
  }

  appSeeTrackAction(actionData: { action: string, data: { [key: string]: any } }): void {
    // eslint-disable-next-line no-console
    console.warn('NativeBridge.onUserAction call:', JSON.stringify(actionData)); //  ToDo: remove after verification of BMA-34374
    if (this.isWrapper && _.isFunction(this.bridge.onUserAction)) {
      this.bridge.onUserAction(JSON.stringify(actionData));
    }
  }

  /**
   * Send virtual sport string to native app
   * @params {string} eventId
   */
  onVirtualsSelected(sportId: string, eventId: string): void {
    if (this.isWrapper && _.isFunction(this.bridge.onVirtualsSelected)) {
      this.bridge.onVirtualsSelected(sportId, eventId);
    }
  }

  onActivateWinAlerts(receiptId: string, betIds: string[]): void {
    if (this.isWrapper && _.isFunction(this.bridge.onActivateWinAlerts)) {
      this.bridge.onActivateWinAlerts(receiptId, betIds);
    }
  }

  /**
   * method to get all the status of winalerts for bet receipt ids
   */
  winAlertsStatus(): void {
    if (this.isWrapper && typeof this.bridge.winAlertsStatus === 'function') {
      this.bridge.winAlertsStatus();
    }
  }

  /**
   * method to deactivate the status of winalerts for a bet receipt id
   * @params {string} betId
   */
  disableWinAlertsStatus(betId: string): void {
    if (this.isWrapper && typeof this.bridge.disableWinAlertsStatus === 'function') {
      this.bridge.disableWinAlertsStatus(betId);
    }
  }

    /**
   * method to clear cache of pagination mybets data
   */
    onClearCache(): void {
      if (this.isWrapper && typeof this.bridge.onClearCache === 'function') {
        this.bridge.onClearCache();
      }
    }

  showNotificationSettings(): void {
    if (this.isWrapper && _.isFunction(this.bridge.showNotificationSettings)) {
      this.bridge.showNotificationSettings();
    }
  }

  /**
   * Hide native splash screen
   */
  hideSplashScreen(): void {
    if (this.isWrapper && _.isFunction(this.bridge.hideSplashScreen)) {
      this.bridge.hideSplashScreen();
    }
  }

  /*
   * Handler to send initial info to the native devices
   */
  handleNativeVideoPlayer(nativeVideoPlayerPlaceholder: HTMLElement) {
    if (nativeVideoPlayerPlaceholder && this.isWrapper && _.isFunction(this.bridge.onVideoPlayerExpanded)) {
      const elOffset = el => el ? el.offsetTop + elOffset(el.offsetParent) : 0;
      this.bridge.onVideoPlayerExpanded(elOffset(nativeVideoPlayerPlaceholder));
    }
  }

  /**
   * Handler for native video player placeholder
   * @param isVideoSticked: boolean
   * @param element: ElementRef
   */
  handleNativeVideoPlaceholder(isVideoSticked: boolean, element: HTMLElement): void {
    if (element) {
      element.style.height = `${isVideoSticked ? this.bridge.nativeVideoPlayerHeight : 0}px`;
    }
  }

  /**
   * Passing network indicator enabled information to native
   * @param  {boolean} enabled
   * @returns void
   */
  networkIndicatorEnabled(enabled: boolean): void {
    if (this.isWrapper && _.isFunction(this.bridge.networkIndicatorEnabled)) {
      this.bridge.networkIndicatorEnabled(enabled);
    }
  }

  /**
   * sharing the bet image to invoke android native
   * @param imageString 
   * @param sportsUrl 
   */
  shareContentOnSocialMediaGroups(data: any): void {
    if (this.isWrapper && _.isFunction(this.bridge.shareContentOnSocialMediaGroups)) {
      this.bridge.shareContentOnSocialMediaGroups(JSON.stringify(data));
    }
  }

  /**
   * Open Opt In splash screen from native app
   */
  private showOptInSplashScreen(): void {
    console.warn('NativeBridge: showOptInSplashScreen');
    this.command.execute(this.command.API.OPT_IN_SPLASH_UPDATE_STATE,
      [{ visibility: true, type: 'optIn' }]);
  }

  /**
   * open marketing preferences page when click on opt in checkbox on native policy banner
   */
  private showMarketingPreferencePage(): void {
    console.warn('NativeBridge: showMarketingPreferencePage');
    this.command.execute(this.command.API.OPT_IN_INACTIVE_USER);
  }

  /**
   * Synchronize betslip with wrapper
   * @params {string[]} outcomes
   */
  private syncBetSlipToNative(outcomes: Array<string>): void {
    if (this.isWrapper && _.isFunction(this.bridge.syncBetSlip)) {
      this.bridge.syncBetSlip(JSON.stringify(outcomes));
    }
  }

  /**
   * Load betslip from native wrapper
   */
  private syncBetSlipFromNative(): void {
    const selections = this.betSelections;
    if (_.isArray(selections)) {
      this.pubsub.publish(this.pubsub.API.SYNC_BETSLIP_FROM_NATIVE, selections);
    }
  }

  /**
   * Callback When user changes odds format
   * @params {boolean} settingValue
   */
  private onOddsSettingsChanged(settingValue: any): void {
    if (this.isWrapper && _.isFunction(this.bridge.onOddsSettingsChanged)) {
      this.bridge.onOddsSettingsChanged(settingValue);
    }
  }

  /**
   * Display streaming in Full screen-Landscape mode
   */
   displayInLandscapeMode(): void {
    if (this.isWrapper && _.isFunction(this.bridge.displayInLandscapeMode)) {
      this.bridge.displayInLandscapeMode();
    }
  }
}
