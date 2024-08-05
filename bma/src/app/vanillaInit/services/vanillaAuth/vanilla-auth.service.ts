import { Injectable, NgZone } from '@angular/core';
import { Router } from '@angular/router';

import { Observable, from, of } from 'rxjs';
import { map, finalize } from 'rxjs/operators';

import {
  UserAutologoutEvent,
  UserEvent,
  UserLoggingInEvent,
  UserLoginEvent,
  UserLoginFailedEvent,
  UserLogoutEvent,
  BalanceProperties,
  UserService as VanillaUserService,
  UserUpdateEvent,
  NativeEvent,
  RememberMeService as RememberMeStatusService,
  AuthService as VanillaAuth,
  ClaimsService,
  LoginDialogService,
  LoginDialogData,
  LoginNavigationService
} from '@frontend/vanilla/core';
import { UserService } from '@coreModule/services/user/user.service';
import { NativeBridgeService } from '@coreModule/services/nativeBridge/native-bridge.service';
import { PubSubService } from '@coreModule/services/communication/pubsub/pubsub.service';
import { CoreToolsService } from '@coreModule/services/coreTools/core-tools.service';
import { FiltersService } from '@coreModule/services/filters/filters.service';
import { AfterLoginNotificationsService } from '@coreModule/services/afterLoginNotifications/after-login-notifications.service';
import { AuthService } from '@authModule/services/auth/auth.service';
import { IFreeBetState } from '@core/services/freeBets/free-bets.model';
import { VanillaFreebetsBadgeDynamicLoaderService } from '@platform/vanillaInit/services/vanillaFreeBets/vanilla-fb-badges-loader.service';
import { AccountUpgradeLinkService } from '@vanillaInitModule/services/accountUpgradeLink/account-upgrade-link.service';
import { NativeBridgeAdapter } from '@vanillaInitModule/services/NativeBridgeAdapter/nativebridge.adapter';
import { VANILLA_NATIVE_EVENTS } from '@vanillaInitModule/services/NativeBridgeAdapter/nativeEvents';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { StorageService } from '@core/services/storage/storage.service';
import { ILoginOpenDialogEvent } from '@app/auth/services/loginDialog/login-dialog.model';
import { SessionService } from '@authModule/services/session/session.service';
import { ProxyHeadersService } from '@bpp/services/proxyHeaders/proxy-headers.service';
import { DeviceService } from '@core/services/device/device.service';
import { MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog';
import environment from '@environment/oxygenEnvConfig';
import { BRAND_PREFIXES_CONSTANTS } from '@vanillaInitModule/constants/brand-prefixes.constants';
import { IFreebetToken } from '@bpp/services/bppProviders/bpp-providers.model';
import { LoginDialogComponent } from '@frontend/vanilla/features/login/src/login-dialog.component';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { BalancePropertiesService } from '@frontend/vanilla/features/balance-properties';
import { UserInterfaceClientConfig } from '@app/client-config/bma-user-interface-config';

@Injectable({
  providedIn: 'root'
})
export class VanillaAuthService {

  private readonly oxiRememberMeName: string = 'rememberMe';
  private readonly PAGE_REFRESH = 'Page Refresh';
  private readonly registrationRedirectEventName: string = 'REGISTRATION_REDIRECT';
  private nativeAppCookieName: string = 'NativeApp';
  private nativeAppCookieValue: string = 'SPORTSW';
  private loginDialogOpened: boolean = false;
  private loginWasChecked: boolean = false;
  private appsFlyerTrackerIdCookieName: string = 'trackerId';
  private appsFlyerTrackerAffiliateCookieName: string = 'trackerAffiliate';
  private appsFlyerBtagCookieName: string = 'btag';
  private appsFlyertBpehCookieName: string = 'tdpeh';
  private loginDialog: MatDialogRef<LoginDialogComponent>;
  private readonly title = 'vanillaAuthService';
  private readonly brandPrefix = BRAND_PREFIXES_CONSTANTS.PREFIX;
  private subscriberName: string = this.awsService.getUniqueSubscriberName();
  private isOSPermitted: boolean = false;

  constructor(
    protected vanillaUser: VanillaUserService,
    protected user: UserService,
    private nativeBridgeService: NativeBridgeService,
    private awsService: AWSFirehoseService,
    protected pubsub: PubSubService,
    private coreToolsService: CoreToolsService,
    private filtersService: FiltersService,
    private vanillaLoginDialogService: LoginDialogService,
    private balanceService: BalancePropertiesService,
    private afterLoginNotifications: AfterLoginNotificationsService,
    protected authService: AuthService,
    private vanillaAuth: VanillaAuth,
    private claimsService: ClaimsService,
    private freeBetsBadgeLoader: VanillaFreebetsBadgeDynamicLoaderService,
    private accountUpgradeLinkService: AccountUpgradeLinkService,
    private nativeBridgeAdapter: NativeBridgeAdapter,
    protected storage: StorageService,
    protected windowRef: WindowRefService,
    private router: Router,
    private sessionService: SessionService,
    private proxyHeadersService: ProxyHeadersService,
    private device: DeviceService,
    private rememberMeStatusService: RememberMeStatusService,
    private navigationService:LoginNavigationService,
    private userInterfaceConfig: UserInterfaceClientConfig,
    protected ngZone: NgZone,
  ) {
    this.afterLoginDialogClose = this.afterLoginDialogClose.bind(this);
  }

  init(): void {
    this.nativeBridgeService.isWrapperStream.subscribe((isWrapper: boolean) =>
      isWrapper && this.triggerNativeEvents());

    this.isOSPermitted = this.userInterfaceConfig.homeBiometric?.[this.nativeBridgeService.getMobileOperatingSystem()];

    this.vanillaUser.events.subscribe((event: UserEvent) => {
      // subscribe to Vanilla log in event
      if (event instanceof UserLoginEvent) {
        this.user.set({ loginPending: false });
        this.user.userFinishedLogin = false;
        this.loginSequence('Login Event')
          .pipe(finalize(() => {
            this.user.userFinishedLogin = true;
            if(this.isOSPermitted)
              this.user.set({isManualLogout: false});
            // eslint-disable-next-line
          })).subscribe();
        return;
      }

      // subscribe to Vanilla log out event and set log out status
      if (event instanceof UserLogoutEvent || event instanceof UserAutologoutEvent) {
        this.user.set({ loginPending: false });

        if(this.isOSPermitted && event instanceof UserLogoutEvent && event.isManualLogout)
          this.user.set({isManualLogout: event.isManualLogout});

        this.setLogoutStatus(`Logout by vanilla event: ${event instanceof UserLogoutEvent ? 'UserLogoutEvent' : 'UserAutologoutEvent'}`);
        this.nativeBridgeService.logout();
        this.nativeBridgeService.pageLoaded();
        return;
      }

      // subscribe to loggingIn event to set pending status
      if (event instanceof UserLoggingInEvent) {
        this.user.initAuthPromises();
        this.user.set({ loginPending: true });
        return;
      }

      if (event instanceof UserUpdateEvent) {
        console.warn('UserUpdateEvent', event);
      }

      if (event instanceof UserLoginFailedEvent) {
        this.pubsub.publish(this.pubsub.API.FAILED_LOGIN);
        this.user.set({ loginPending: false });
        return;
      }
    });

    this.balanceService.balanceProperties.subscribe((balanceProperties: BalanceProperties) => {
      if (balanceProperties) {
        this.setBalance(balanceProperties);
      }
    });

    this.pubsub.subscribe('authFactory', this.pubsub.API.RELOAD_COMPONENTS, () =>
      this.handleReloadComponentsEvent()
    );

    this.pubsub.subscribe(this.title, this.pubsub.API.OPEN_LOGIN_DIALOG, (event) => {
      this.triggerLoginDialog().subscribe(() => {
        this.setDialogStatus(false);
        this.pubsub.publish(this.pubsub.API.LOGIN_DIALOG_CLOSED);
        event && event.action && event.action();
      });
    });

    this.pubsub.subscribe(this.title, this.pubsub.API.FREEBETS_UPDATED,
      (freeBetState: IFreeBetState, isPageRefresh?: boolean) => {
        this.isLoggedIn() && this.freebetCounterUpdate(freeBetState, isPageRefresh);
      });

    this.pubsub.subscribe(this.title, this.pubsub.API.APP_IS_LOADED, () => {
      this.loadNative();
      this.windowRef.document.addEventListener('TOUCHID_CONFIGURED', () => {
        if(!this.isLoggedIn() && !this.user.isManualLogout && !this.loginDialogExists() && this.isOSPermitted){
          this.runBiometricLogin();
        }
      });
    });

    this.pubsub.subscribe(this.title, this.pubsub.API.IMPLICIT_BALANCE_REFRESH, () => {
      this.refreshBalance();
    });

    // check user status and map data or log out
    if (this.isLoggedIn()) {
      this.loginSequence('Page Refresh').subscribe();
    } else {
      this.setLogoutStatus('Logout on VanillaAuthService init(vanillaUser.isAuthenticated: false)');
      // prevent IOS native app to hide home page too early
      if (!this.device.isIos) { this.nativeBridgeService.logout(); }
    }
  }

  /**
   * Trigger Biometric login
   */
  private runBiometricLogin(): void {
    this.windowRef.nativeWindow.setTimeout(() => {
      if(this.user.getTouchIdLogin() === 'enabled' && ((!this.isOSPermitted && this.nativeBridgeService.touchIDConfigured) || this.isOSPermitted)){
        this.nativeBridgeService.loginWithTouchID(false, '', false);
      }
    });
  }

  handleRegistrationRedirection(): void {
    if (this.loginDialog) {
      this.loginDialog.close({ openedBy: this.registrationRedirectEventName });
    }
    this.navigationService.goToRegistration();
  }


  /**
   * Set AppsFlyer cookies on Registration_Screen_Active event
   */
  setAppsFlyerCookies(): void {
    if (this.nativeBridgeService.profileid) {
      if (!this.storage.getCookie(this.appsFlyerTrackerIdCookieName)) {
        this.storage.setCookie(this.appsFlyerTrackerIdCookieName, this.nativeBridgeService.profileid, environment.DOMAIN, 30, true);
      }
      if (!this.storage.getCookie(this.appsFlyerTrackerAffiliateCookieName)) {
        this.storage.setCookie(this.appsFlyerTrackerAffiliateCookieName, this.nativeBridgeService.profileid, environment.DOMAIN, 1, true);
      }
    }
    if (!this.storage.getCookie(this.appsFlyerBtagCookieName) && this.nativeBridgeService.creferer) {
      const creferer = this.nativeBridgeService.creferer.indexOf('BTAG:') > -1 ?
        this.nativeBridgeService.creferer.substring('BTAG:'.length) : this.nativeBridgeService.creferer;
      this.storage.setCookie(this.appsFlyerBtagCookieName, creferer, environment.DOMAIN, 30, true);
    }
    if (!this.storage.getCookie(this.appsFlyertBpehCookieName) && this.nativeBridgeService.tdpeh) {
      this.storage.setCookie(this.appsFlyertBpehCookieName, this.nativeBridgeService.tdpeh, environment.DOMAIN, 30, true);
    }
  }

  /**
   * Trigger vanilla login dialog
   * @param openedBy
   */
  triggerLoginDialog(openedBy?: string) {
    const loginDialogParam: LoginDialogData = openedBy ? { openedBy } : {};
    if (!this.loginDialogExists()) {
      this.ngZone.run(() => {
        this.loginDialog = this.vanillaLoginDialogService.open(loginDialogParam);
      });

      return this.loginDialog.afterClosed();
    }
    return of(null);
  }

  isLoggedIn(): boolean {
    return this.vanillaUser.isAuthenticated;
  }

  refreshBalance(): Promise<any> {
    return Promise.resolve(this.balanceService.refresh());
  }

  loginDialogExists(): boolean {
    return this.loginDialogOpened;
  }

  /**
   * Check if user can use oddsboosts and set badges to menu items
   * @params {freeBetState: IFreeBetState, isPageRefresh: boolean}
   */
  freebetCounterUpdate(freeBetState: IFreeBetState, isPageRefresh?: boolean): void {
    from(this.sessionService.whenProxySession())
      .subscribe(() => {
        freeBetState.data = freeBetState.data.filter(bet => {
          return (bet.tokenPossibleBetTags && bet.tokenPossibleBetTags.tagName) ? bet.tokenPossibleBetTags.tagName !== 'FRRIDE' : bet;
        });
        this.freeBetsBadgeLoader.addBadgesToVanillaElements(freeBetState);
        this.freeBetsBadgeLoader.addBetpackCounter(freeBetState);

      });
  }

  /**
   * Handle login success.
   * @param event
   */
  handleMobileAutoLogin(event: NativeEvent): void {
    if (event.parameters.type === 'Autologin') {
      this.storage.set(this.oxiRememberMeName, 1);
    }
  }

  /**
   * combine User data object and store in Storage
   * trigger method to update balance
   */
  protected mapUserData(): void {
    const vanillaTierCode = this.claimsService.get('tierCode');
    const vipLevel: string | null = +vanillaTierCode > 0 ? vanillaTierCode : null;
    this.user.set({
      // TODO check advertiser | profileId fields at Vanilla User
      // advertiser: info.advertiser || null, // used in GTM
      firstname: this.vanillaUser.firstName,
      lastname: this.vanillaUser.lastName,
      vipLevel: vipLevel,
      username: this.vanillaUser.username,
      currencyCode: this.vanillaUser.currency,
      // profileId: info.profileId || null, // used in GTM
      playerCode: `${this.brandPrefix}${this.vanillaUser.username}`,
      email: this.vanillaUser.email,
      // postCode: info.signupZip || null, // used in GTM, won't be available
      // signupDate: info.signupDate || null, // not used
      countryCode: this.vanillaUser.country,
      birthDate: this.vanillaUser.dateOfBirth,
      accountBusinessPhase: this.accountUpgradeLinkService.businessPhase,
      sseToken: this.vanillaUser.ssoToken,
      sessionToken: this.vanillaUser.ssoToken,
      firstLogin: this.vanillaUser.isFirstLogin,
      isAuthenticated: this.vanillaUser.isAuthenticated,
      title: this.vanillaUser.title,
    });

    this.storage.set('vipLevel', vipLevel);
    // AEM-727, cookie is required to show personalised content on landing pages for certain vip users
    this.storage.setCookie('lbrims', vipLevel, environment.DOMAIN, 30, false);
    this.storage.set('existingUser', true);

    this.pubsub.publish(this.pubsub.API.SET_PLAYER_INFO, this.user);
    this.pubsub.publish(this.pubsub.API.FZ_MENUS_UPDATE);
    this.setBalance();
  }

  /**
   * Login user with triggering callbacks and resolve auth Promises
   */
  protected login(): void {
    if(this.user.getPostLoginBonusSupValue()) {
      this.pubsub.publish(this.pubsub.API.INITIATE_RGY_CALL, true);
      this.pubsub.subscribe('authFactory', this.pubsub.API.RGY_DATA_LOADED, () =>
        this.loginFlow()
      );
    } else {
      this.loginFlow();
    }
  }

  protected loginFlow(): void {
    this.user.login(this.vanillaUser.ssoToken);
    this.user.resolveOpenApiAuth();
    this.authService.innerSessionLoggedIn.next(null);
    this.pubsub.publish(this.pubsub.API.LOGIN_PENDING, true);
    this.pubsub.publish(this.pubsub.API.SESSION_LOGIN, [{ User: this.user, options: {} }]);
  }

  /**
   * Set dialog status
   * @params value
   */

  private setDialogStatus(value: boolean): void {
    this.loginDialogOpened = value;
  }

  /**
   * Trigger related to logout logic
   * @param logoutReason
   */
  private setLogoutStatus(logoutReason: string): void {
    this.awsService.addAction('vanillaAuth=>logout', { logoutReason }, this.subscriberName);
    this.user.logout();
  }

  /**
   * Checking authentification on vanilla's side and logout user if
   * not authenticated
   */
  private handleReloadComponentsEvent(): void {
    this.vanillaAuth.isAuthenticated().then((isAuthenticated: boolean) => {
      this.awsService.addAction('vanillaAuth=>handleReloadComponentsEvent', { isAuthenticated }, this.subscriberName);
      // should log out User if session expired on web service and he was logged in before
      if (!isAuthenticated && this.isLoggedIn()) {
        // should log out from application and navigate to home page with app reload (vanilla requires
        // page reload to set proper state) if no remember me cookie exists
        if (!this.rememberMeStatusService.tokenExists()) {
          this.nativeBridgeService.logout();
          this.setLogoutStatus('Logout by handleReloadComponentsEvent');
          this.windowRef.nativeWindow.location.href = this.windowRef.nativeWindow.location.origin;
        }
      }
    });
  }


  /**
   * Mapping data to USER object in storage with calling login method
   * and proper callbacks
   */
  private loginSequence(loginReason: string): Observable<void> {
    this.awsService.addAction(`vanillaAuth=>loginSequence=>${loginReason}`, {}, this.subscriberName);
    // TODO remove when bpp auth implemented
    this.mapUserData();
    this.login();

    if (this.user.isRestoredBppUser()) {
      this.proxyHeadersService.generateBppAuthHeaders();
      this.user.resolveProxyAuth();
      this.pubsub.publish(this.pubsub.API.STORE_FREEBETS_ON_REFRESH);
      // Get odds preference and set it to localstorage on refresh(after login)
      this.authService.getOddspreference(this.user.bppToken);

      // load oddsBoost on page refresh and Restore auth session
      return this.authService.initOddsBoost()
        .pipe(
          map((tokens: IFreebetToken[]) => {
            this.pubsub.publishSync(this.pubsub.API.STORE_ODDS_BOOST, [tokens]);
            return null;
          })
        );
    }

    // TODO check bbpToken -> use if existed -> generate new if no
    return this.authService.bppAuthSequence()
      .pipe(map(() => {
        console.warn('BPP sequence resolved');
        this.pubsub.publish(this.pubsub.API.BETPACK_POPUP_SHOW);
        this.afterLoginNotifications.start();
        this.pubsub.publish(this.pubsub.API.LOGIN_PENDING, false);
        this.pubsub.publish(this.pubsub.API.SUCCESSFUL_LOGIN);
      }));
  }

  /**
   * Update balance attributes in User object with triggering proper callbacks
   * @param balanceProperties  wthi 'this.vanillaUser.balanceProperties' by default
   */
  private setBalance(balanceProperties: BalanceProperties = this.windowRef.nativeWindow.clientConfig.vnBalanceProperties || {}): void {
    const sportBalance = balanceProperties.availableBalance;
    const currencySymbol: string = this.coreToolsService.getCurrencySymbolFromISO(this.vanillaUser.currency);
    const oldBalance = this.user.sportBalance || 0;
    this.user.set({
      currency: this.vanillaUser.currency,
      currencySymbol,
      sportBalance: String(sportBalance),  // TODO validate this field
      sportBalanceWithSymbol: this.filtersService.currencyPosition(Number(sportBalance).toFixed(2), currencySymbol)
    });
    this.pubsub.publish(this.pubsub.API.USER_BALANCE_UPD, { sportBalance, oldBalance });
    this.nativeBridgeService.onBalanceChanged({
      amount: String(sportBalance)
    });
  }

  /**
   * Subscription to events from Vanilla's side with properly logic
   */
  // Added setSportsUserName() to solve BMAN-9025
  // RCA:  The events triggered from vanilla is in the following sequence
  //         1) VANILLA_NATIVE_EVENTS.LOGIN
  //         2) UserLoginEvent
  // here due to sequence changed first NativeEvent triggered somewhere
  // in the logic it is trying to get the cookie(sportsUserName) but it
  // is not getting it is creating a problem for faceiId
  private handleVanillaNativeEvents(): void {
    this.nativeBridgeAdapter.nativeEventObservable.subscribe((event: NativeEvent) => {
      if (!event) { return; }
      switch (event.eventName) {
        case VANILLA_NATIVE_EVENTS.OPEN_LOGIN_DIALOG:
          this.windowRef.nativeWindow.openLoginDialog();
          break;
        case VANILLA_NATIVE_EVENTS.LOGIN:
          this.user.setSportsUserName(event.parameters.userName);
          this.afterLoginHandler(event);
          break;
        case VANILLA_NATIVE_EVENTS.LOGIN_FAILED:
          this.afterLoginErrorHandler(event);
          break;
        case VANILLA_NATIVE_EVENTS.LOGIN_SCREEN_ACTIVE:
          this.setDialogStatus(true);
          if (this.loginWasChecked) { return; }
          this.checkLoginOption();
          break;
        default:
          break;
      }
    });
  }

  /**
   * call to allow user to login with touch/face Id or standard login
   */
  private checkLoginOption(): void {
    this.loginWasChecked = true;
    if (this.user.status) {
      return;
    }

    if (!this.storage.getCookie('firstTimeLogin')) {
      this.storage.setCookie('firstTimeLogin', true);
    }

    if(!this.isOSPermitted)
      this.runBiometricLogin();
  }

  /**
   * Called to touch/face Id login on Vanilla side
   *  * @params {usernameCardnumber: string, passwordPin: string, rememberName: boolean, rememberMe: boolean}
   */
  private nativeLogin(usernameCardnumber: string, passwordPin: string, rememberName: boolean = false, rememberMe: boolean = false): void {
    this.nativeBridgeAdapter.doNativeLogin(usernameCardnumber, passwordPin,
      { isTouchIDEnabled: true, isFaceIDEnabled: false, rememberMe: rememberMe });
  }

  /**
   * Bind native methods to web callbacks
   */
  private subscribeToNativeEvents(): void {
    this.windowRef.nativeWindow.doLogin = this.nativeLogin.bind(this);
    // Vanilla open login dialog by itself
    this.windowRef.nativeWindow.openLoginDialog = async (config: Partial<ILoginOpenDialogEvent> = {}, errorMessage?: string) => {
      if (errorMessage) {
        this.loginWasChecked = true;
        await this.navigationService.goToLogin({ loginMessageKey: 'autologinerrortouch' });
      }
      if (!this.loginDialogExists()) {
        this.triggerLoginDialog().subscribe((dialogOptions?: LoginDialogData) => {
          this.onLoginDialogClose(dialogOptions ?
            (dialogOptions.openedBy === this.registrationRedirectEventName) : false);
        });
      }
      this.setDialogStatus(true);
      this.nativeBridgeService.onOpenPopup('Login');
    };
  }

  /**
   * Send credentials to nativeApp do store in keychain
   * @params {userData: NativeEvent}
   */
  private afterLoginHandler(userData: NativeEvent): void {
    const lastUsername = this.storage.get('lastUsername') || userData.parameters.userName;
    // BMA-41238 - playerCode = cl_ + GVC_ACCOUNT_NAME
    const playerCode = `${this.brandPrefix}${userData.parameters.userName}`;

    this.storage.set('lastUsername', userData.parameters.userName);
    this.nativeBridgeService.loginIfExist(userData.parameters.accountId, userData.parameters.password);
    this.nativeBridgeService.loginSalesForce(playerCode);
    this.nativeBridgeService.loginSessionToken({
      username: userData.parameters.userName,
      sessionToken: userData.parameters.ssoToken,
      isFromBetSlip: userData.parameters.isFromBetslip,
      password: userData.parameters.password
    });

    // set TouchIdLogin to disable if it is different this._User
    if (this.user.getTouchIdLogin() === 'enabled' && lastUsername !== userData.parameters.userName) {
      this.user.setTouchIdLogin('disabled');
    }

  }

  /**
   * Inform nativeApp about error fail
   * @params {err: any}
   */
  private afterLoginErrorHandler(event: NativeEvent): void {
    const autologinCode = 'Autologin';
    const data = {
      errorCode: event.parameters.errorCode,
      errorMessage: 'LOGIN ERROR',
      type: event.parameters.type,
      timestamp: Date.now()
    };
    this.nativeBridgeService.appSeeTrackAction({
      action: 'login-failed', data
    });

    if (data.type === autologinCode && !data.errorCode) {
      this.nativeBridgeService.touchIDLoginFailedIfExist(data);
    }

    this.nativeBridgeService.loginError(data);
  }

  /**
   * add listener to react on menu button click on ios home-screen and redirect to vanilla menu
   */
  private changeUserMenuListener(): void {
    this.windowRef.document.addEventListener('CHANGE_RIGHT_HAND_SLIDE_STATE', () => this.router.navigate(['en/menu']));
  }

  /**
   * enable nativeWrapper mode on Vanilla side and subscribe to Vanilla nativeEvents
   */
  private triggerNativeEvents(): void {
    this.setNativeCookie();
    this.changeUserMenuListener();
    this.handleVanillaNativeEvents();
    this.subscribeToNativeEvents();
  }

  /**
   * helper method to agregate logic to execute after login popup was closed
   * @params {closedFromRegistrationRedirection: boolean}
   */
  private afterLoginDialogClose(closedFromRegistrationRedirection?: boolean): void {
    this.setDialogStatus(false);
    this.loginWasChecked = false;
    this.nativeBridgeService.onClosePopup('Login', closedFromRegistrationRedirection ? { Registration: true } : undefined);
  }

  /**
   * Native events to be triggered when app is loaded
   */
  private loadNative() {
    if ((this.device.isIos && !this.isLoggedIn()) || this.device.isAndroid) { // stream and bet pop-up issue fix - native will refresh user details
      this.nativeBridgeService.logout();
    }

    this.nativeBridgeService.hideSplashScreen();
    this.nativeBridgeService.pageLoaded();
  }

  /**
   * @params {closedFromRegistrationRedirection: boolean}
   */
  private onLoginDialogClose(closedFromRegistrationRedirection?: boolean): void {
    if (this.isLoggedIn()) {
      this.pubsub.subscribe('vanillaAuth', this.pubsub.API.LOGIN_POPUPS_END, this.afterLoginDialogClose);
    } else {
      this.afterLoginDialogClose(closedFromRegistrationRedirection);
    }
  }

  /**
   * Set native app cookie to init vanilla bridge
   */
  private setNativeCookie(): void {
    // cookie should not be set if already existed - navigation to Oxygen from Vanilla 3rd party wrapper
    if (this.storage.getCookie(this.nativeAppCookieName)) {
      return;
    }
    this.storage.setCookie(this.nativeAppCookieName, this.nativeAppCookieValue);
  }
}
