import { forkJoin, Observable, of, Subscription, throwError } from 'rxjs';
import { catchError, first, map, mergeMap } from 'rxjs/operators';
import {
  AfterViewInit,
  Component,
  ComponentRef,
  OnDestroy,
  OnInit,
  ViewContainerRef
} from '@angular/core';
import { ActivatedRoute, Event, NavigationEnd, Router, NavigationStart } from '@angular/router';
import { Location } from '@angular/common';
import { DomSanitizer } from '@angular/platform-browser';
import environment from '@environment/oxygenEnvConfig';
import * as _ from 'underscore';
import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { UserService } from '@core/services/user/user.service';
import { StorageService } from '@core/services/storage/storage.service';
import { AfterLoginNotificationsService } from '@coreModule/services/afterLoginNotifications/after-login-notifications.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { AuthService } from '@authModule/services/auth/auth.service';
import { InsomniaService } from '@core/services/insomnia/insomnia.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { DeviceService } from '@core/services/device/device.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { ISystemConfig } from '@core/services/cms/models/index';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { widgetsConfig } from '@app/bma/constants/widgets-config.constant';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { IDialogEvent } from '@core/services/dialogService/dialog-params.model';
import { ISportCategory, IWidget } from '@core/services/cms/models';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { SPRITE_PATH } from '@bma/constants/image-manager.constant';
import { SCRIPTS_LOADING_DELAY } from '@core/services/deferredLoader/deferred-loader.service.constant';
import { PERFORMANCE_API_MEASURE,PERFORMANCE_API_MARK } from '@app/lazy-modules/performanceMark/enums/performance-mark.enums';
import { LAZY_LOAD_ROUTE_PATHS } from '@bma/constants/lazyload-route-paths.constant';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { EzNavVanillaService } from '@app/core/services/ezNavVanilla/eznav-vanilla.service';
import { FanzoneHelperService } from '@app/core/services/fanzone/fanzone-helper.service';
import { InitNetworkIndicatorService } from '@app/core/services/networkIndicator/init-network-indicator.service';
import { GA_TRACKING } from '@app/shared/constants/channel.constant';
import { IGATrackingModel } from '@app/core/models/gtm.event.model';
import { NETWORK_CONSTANTS } from '@lazy-modules/networkIndicator/components/network-indicator/network-indicator.constants';
import { NIConfig, NIConfigMessage } from '@lazy-modules/networkIndicator/components/network-indicator/network-indicator.model';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

@Component({
  selector: 'bma-main',
  templateUrl: 'bma-main.component.html'
})
export class BmaMainComponent implements OnInit, AfterViewInit, OnDestroy {
  loginPending: boolean;
  betslipLoaded: boolean = false;
  sysConfig: ISystemConfig;
  transition: string;
  showRC: boolean;
  widgetDataStore: IWidget[];
  betSlipAnimation: string;
  menuItems: ISportCategory[];
  isHomeURL: boolean;
  isGamingOpen: boolean = false;
  isMyBetsInCasino: boolean = false;
  initialIcons: string;
  featuredIcons: string;
  additionalIcons: string;
  NW_I_Object: NIConfig;
  streamBetVideoMode: boolean = false;

  GTMTrackingObj: IGATrackingModel = {
    isHomePage: this.checkIfHomeUrl(),
    event: GA_TRACKING.event,
    GATracking: {
      eventAction: GA_TRACKING.eventAction,
      eventCategory: GA_TRACKING.sportsRibbon.eventCategory,
      eventLabel: "",
    }
  };  
  protected routeChangeSuccessHandler: Subscription;
  protected windowResizeListener: Function;
  private resizeListerner: Function;
  private slideOutBetsliContainer: ViewContainerRef;
  private slideOutBetslipRef: ComponentRef<any>;
  private readonly title = 'BmaMainComponent';
  private readonly bmaReadyClass: string = 'bma-ready';
  private readonly COOKIE_LENGTH: string = 'cookiesLength';

  private cmsConfigsSubscription: Subscription;


  constructor(
      public device: DeviceService,
      public user: UserService,
      protected windowRef: WindowRefService,
      protected route: ActivatedRoute,
      protected locale: LocaleService,
      protected nativeBridge: NativeBridgeService,
      protected pubSubService: PubSubService,
      protected cms: CmsService,
      protected storageService: StorageService,
      protected afterLoginNotifications: AfterLoginNotificationsService,
      protected navigationService: NavigationService,
      protected authService: AuthService,
      protected location: Location,
      protected insomnia: InsomniaService,
      protected gtm: GtmService,
      protected filtersService: FiltersService,
      protected coreTools: CoreToolsService,
      protected domSanitizer: DomSanitizer,
      protected rendererService: RendererService,
      protected domTools: DomToolsService,
      protected router: Router,
      protected dialogService: DialogService,
      protected routingState: RoutingState,
      protected dynamicComponentLoader: DynamicLoaderService,
      protected asyncScriptLoaderService: AsyncScriptLoaderService,
      protected awsService: AWSFirehoseService,
      protected sessionStorage: SessionStorageService,
      protected seoDataService: SeoDataService,
      protected ezNavVanillaService: EzNavVanillaService,
      protected fanzoneHelperService: FanzoneHelperService,
      protected initNetworkIndicatorService: InitNetworkIndicatorService
  ) {
    this.setConfigs = this.setConfigs.bind(this);
    this.setLogoutState = this.setLogoutState.bind(this);
    this.showUserBalance = this.showUserBalance.bind(this);
    this.handleRouteChange = this.handleRouteChange.bind(this);
    this.sessionLoginHandler = this.sessionLoginHandler.bind(this);
    if (this.ezNavVanillaService.isDeviceBrowserValidForCasino()) {
      this.ezNavVanillaService.casinoMyBetsVanillaInit();
      this.isMyBetsInCasino  = this.ezNavVanillaService.isMyBetsInCasino;
    }
  }

  ngOnInit(): void {
    const screen = this.windowRef.nativeWindow;
    // Get System Configuration
    this.cmsConfigsSubscription = this.cms.getSystemConfig().pipe(
      map(this.setConfigs)
    ).subscribe();

    // Subscribe to global Pubsub events before performing session restore.
    this.subscribeToGlobalEvents();
    this.initServices();
    this.seoDataService.organisationPageSeo();
    this.breakPoint();

    // SVG ICONS
    this.cms.extractInitialIcons().subscribe((icons: string) => this.initialIcons = icons);

    this.resizeListerner = this.rendererService.renderer.listen(screen, 'resize orientationchange', () => {
      this.breakPoint();
    });

    // Fix iOS specific issue on ngDialog
    // page scrolls up when tapping on any fields in Login prompt
    if (this.device.isIos) {
      this.nativeBridge.getBuildVersion();
      const cssClasses = this.device.isWrapper ? ['ios-modal-wrapper', 'ios-modal-opened'] : ['ios-modal-opened'];
      const body = this.windowRef.document.querySelector('html');

      this.dialogService.modalListener.subscribe((event: IDialogEvent) => {
        switch (event.type) {
          case 'open':
            const isLoginDialog = event.name === 'Login';
            // Do not apply this fix for signup page where login dialog could be opened in case if
            // user enters email from existing account.
            if (this.location.path() !== '/signup') {
              cssClasses.forEach((c: string) => this.rendererService.renderer.addClass(body, c));
              if (isLoginDialog) {
                const offset = this.windowRef.nativeWindow.pageYOffset;
                // Check if page is srolled only by user and not in case when keyboard is opened
                // and pageYOffset will be minus.
                this.domTools.css(body, { top: `${offset > 0 ? (offset * -1) : 0}px` });
              }
            }
            break;
          case 'close':
          case 'closeAll':
            if (this.location.path() !== '/signup') {
              const offset = body.offsetTop;
              cssClasses.forEach((c: string) => this.rendererService.renderer.removeClass(body, c));
              if (!this.isFootbalTutorialActive()) {
                this.windowRef.nativeWindow.scrollBy(0, `${offset * -1}`);
              }
              this.domTools.css(body, { top: '0px' });
              this.pubSubService.publish(this.pubSubService.API.IOS_CLOSE_NG_DIALOG);
            }
            break;
          default:
            break;
        }
      });
    }
    this.pubSubService.subscribe(this.title, pubSubApi.STREAM_BET_VIDEO_MODE, (streamBetVideoMode: boolean) => {
      this.streamBetVideoMode = streamBetVideoMode;
    });
    this.getMenuItems();
    this.togglePortalSwitch();
    this.intialMark();
    if(this.device.isMobile) {
      this.pubSubService.subscribe(
        this.title, [this.pubSubService.API.SESSION_LOGIN,
        this.pubSubService.API.SEGMENTED_INIT_FE_REFRESH], () => {
          this.cms.getCMSRGYconfigData().subscribe(() => {
            this.getMenuItems();
          });
        }
      );
    }
   
    this.pubSubService.subscribe(this.title, this.pubSubService.API.APP_BUILD_VERSION, (appBuildVersion: string) => {
      this.getMenuItems(appBuildVersion);
      this.fanzoneHelperService.appBuildVersion = appBuildVersion;
    });

    this.pubSubService.subscribe(this.title, this.pubSubService.API.FZ_MENUS_UPDATE, () => {
      this.getMenuItems();
    })

    this.pubSubService.subscribe(this.title ,this.pubSubService.API.QUICKBET_EXTRAPLACE_SELECTION, (selectionData) => {
      this.sessionStorage.set('ExtraplaceSelection',selectionData);
   });

    //setting storage to fix scroll-once directive issue as scrollable directive is affecting the logic.
    this.sessionStorage.set('moduleribbon', false);

    if (this.device.isMobile) {
      this.pubSubService.subscribe(NETWORK_CONSTANTS.BMA_NW_INDICATOR, NETWORK_CONSTANTS.NW_I_STATUS, (message: NIConfigMessage) => {
        const obj = { displayText: message.displayText, networkSpeed: message.networkSpeed, infoMsg: message.infoMsg };
        this.NW_I_Object = { ...obj };
      });
      this.initNetworkIndicatorService.init();
    }
    if (!this.device.isDesktop && !this.featuredIcons) {
      this.loadFeaturedIcons();
    }
  }

  ngAfterViewInit(): void {
    this.rendererService.renderer.addClass(this.windowRef.document.documentElement, this.bmaReadyClass);
    this.pubSubService.publish(this.pubSubService.API.APP_IS_LOADED);
  }

  ngOnDestroy(): void {
    this.routeChangeSuccessHandler.unsubscribe();
    this.pubSubService.unsubscribe(this.title);
    this.cmsConfigsSubscription && this.cmsConfigsSubscription.unsubscribe();

    if (this.resizeListerner) {
      this.resizeListerner();
    }

    if (this.resizeListerner) {
      this.windowResizeListener && this.windowResizeListener();
    }

    this.slideOutBetslipRef && this.slideOutBetslipRef.destroy();
    this.sessionStorage.remove('moduleribbon');
  }

  intialMark(): void {
    if (performance && performance.getEntriesByName(PERFORMANCE_API_MARK.CTI, PERFORMANCE_API_MARK.Mark).length === 0) {
      performance.mark(PERFORMANCE_API_MARK.CTI);
    }
  }
  // Scrolling to the top of the page
  scrollTop(): void {
    if (this.isFootbalTutorialActive()) {
      return;
    }

    this.domTools.scrollPageTop(0);
  }


  /**
   * Initializations and subscribers on some services during component init
   */
  public initServices(): void {
    this.authService.mainInit();
  }

  /**
   * Check if the current url is five-a-side
   * @returns {boolean}
   */
  public checkForFiveASideUrl(): boolean {
    const currentPath: string = this.location.path();
    return currentPath.includes(LAZY_LOAD_ROUTE_PATHS.fiveASideShowdownPath);
 }

  protected getMenuItems(appBuildVersion?: string): void {
    forkJoin(this.cms.getMenuItems(appBuildVersion), this.cms.getSystemConfig(false))
      .subscribe(cmsData => {
        const [cmsData1Result, cmsData2Result] = cmsData;

        this.widgetDataStore = [];
        this.betSlipAnimation = cmsData2Result.Generals.betSlipAnimation;

        this.menuItems = _.filter(cmsData1Result, item => {
          item.iconClass = this.filtersService.sportCatIcon(item.linkTitle);
          
         if(item.targetUri.includes('racingsuperseries')){
          this.filtersService.filterLinkforRSS(item.targetUri).subscribe(data =>{
            item.targetUri = data;
          })
         }
          
          return item.showInHome;
        });

        this.showSportMenu();
        this.showWidgetColumns();
      });
  }

  protected sessionLoginHandler(data): void {
    this.pubSubService.publish(this.pubSubService.API.COUNTER_UPDATE);
  }

  protected loadFeaturedIcons(): void {
    const storedContent = this.storageService.get('cmsFeaturedSprite');
    if (storedContent && storedContent.name === 'featured') {
      this.featuredIcons = storedContent.content;
      this.windowRef.nativeWindow.setTimeout(() => {
        this.storageService.remove('cmsFeaturedSprite');
        this.storageService.remove('cmsInit');
      }, 500);
    } else {
      this.asyncScriptLoaderService.getSvgSprite(SPRITE_PATH.featured).subscribe((icons: string) => this.featuredIcons = icons);
    }
  }

  protected loadAdditionalIcons(): void {
    this.asyncScriptLoaderService.getSvgSprite(SPRITE_PATH.additional).subscribe((icons: string) => this.additionalIcons = icons);
  }

  /**
   * Show Sport Menu on Home page only
   */
  protected showSportMenu(): void {
    this.isHomeURL = this.checkIfHomeUrl();
  }

  /**
   * Show Widget Columns
   * @returns {boolean} true || false
   */
  protected showWidgetColumns(): void {
    this.showRC = (!this.device.isMobile || this.device.isDesktop)
      && !widgetsConfig.rightColumnConf.pageSetup[this.routingState.getCurrentSegment()];

    // This callCallback added for widgets rendering when device is rotated
    this.pubSubService.publish(this.pubSubService.API.SHOW_HIDE_WIDGETS);
  }

  protected handleRouteChange(event: Event): void {
    const cur: string = this.routingState.getCurrentSegment() || '';
    if (event instanceof NavigationEnd) {
      const prev: string = this.routingState.getPreviousSegment() || '';
      this.showSportMenu();
      // Route change event also is emitted on initial route, so need to check previous route for
      // presence, also all deposit routes should be skipped
      if (cur && prev && prev !== cur && cur.indexOf('deposit') === -1) {
        this.storageService.removeCookie('gameBaseUrl');
      }

      // Prevent closing popup on payment method adding
      if (prev !== 'deposit.neteller' &&
        prev !== 'deposit.registered' &&
        prev !== 'addToBetSlip' &&
        cur !== 'deposit.registered' &&
        !this.checkIfHomeUrl()
      ) {

        // Check if this is an entry point of RouletteJourney  - do not close login popup
        if(!this.sessionStorage.get('LuckyDip')) {
          const { targetPage, referrerPage } = this.user.getJourneyParams(this.windowRef.nativeWindow.location.href);

          if (!(this.user.isRouletteJourney() && targetPage && referrerPage)) {
            this.dialogService.closeDialogs();
          }
        }
      }

      this.addContentViewEvent();
      this.showWidgetColumns();
      this.scrollTop();
      if(!this.isHomeURL) {
        this.sessionStorage.set('moduleribbon', false);
      }
    }
    if (event instanceof NavigationStart) {
      if (cur !== 'inPlay.firstSport') {
          if (performance.getEntriesByName(PERFORMANCE_API_MEASURE.NAV, PERFORMANCE_API_MEASURE.Measure).length > 0) {
            performance.clearMeasures(PERFORMANCE_API_MEASURE.NAV);
          }
          if (performance.getEntriesByName(PERFORMANCE_API_MARK.CTI, PERFORMANCE_API_MARK.Mark).length > 0) {
            performance.clearMarks(PERFORMANCE_API_MARK.CTI);
          }
          performance.mark(PERFORMANCE_API_MARK.CTI);
      }
    }
  }

  protected togglePortalSwitch(): void {
    if (this.device.isWrapper) {
      (this.routingState).togglePortalSwitch();
    }
  }
  /**
   * Create a subscriber to router events
   */
  protected subscribeToRouterEvents(): void {
    this.routeChangeSuccessHandler = (this.routingState).replayRouterEvents.subscribe(this.handleRouteChange);
  }

  checkIfHomeUrl(): boolean {
    const currentPath: string = this.location.path();
    return currentPath === '' || currentPath.indexOf('/home/') > -1 || currentPath.indexOf('utm_source=PWA') > -1 ||
      currentPath.startsWith('?');
  }

  /*
   * Add content-view event into a global dataLayer array for analyticsProvider
   */
  private addContentViewEvent(): void {
    this.gtm.push('content-view', { screen_name: this.location.path() });
  }

  /*
   * Subscribing to events.
   */
  private subscribeToGlobalEvents(): void {
    let gtmTimeout: number;
    // set last none cached request from system config
    this.pubSubService.subscribe(this.title, this.pubSubService.API.SYSTEM_CONFIG_UPDATED, this.setConfigs);

    // send request to update system configs after receiving reload event

    this.pubSubService.subscribe(this.title, [this.pubSubService.API.RELOAD_COMPONENTS, this.pubSubService.API.SUCCESSFUL_LOGIN], () => {
      this.cms.triggerSystemConfigUpdate();
    });

    this.pubSubService.subscribe(this.title, this.pubSubService.API.SESSION_LOGIN, this.sessionLoginHandler);

    this.pubSubService.subscribe(this.title, this.pubSubService.API.SESSION_LOGOUT, this.setLogoutState);

    this.pubSubService.subscribe(this.title, this.pubSubService.API.USER_BALANCE_SHOW, this.showUserBalance);

    this.pubSubService.subscribe(this.title, this.pubSubService.API.LOGIN_PENDING, status => {
      this.loginPending = status;
    });

    /**
     * If user is redirected to our app with "cbUrl" in query params or if "gameBaseUrl" is present
     * in cookies - user should be redirected to that URL after next actions:
     *   - User was not logged in, moved to mcasino and pressed "Join". Then user should be
     *     redirected back to mcasino after successful registration or after click on "Back" button;
     *   - User was logged in, moved to mcasino and selected one of availabled options in left menu
     *     (Deposit, Withdraw, Cancel Withdrawal, My Account, Bet History , Settings, Contact Us).
     *     User should be redirected back to mcasino after successful action (deposit,
     *     withdraw) or after click on "Back" button;
     *   - User was logged in, moved to mcasino and selected one of availabled games. Then
     *     "gameBaseUrl" was changed to URL of this game. After that user selected "+Deposit" and
     *     was redirected to "/deposit/registered" page. As result - user should be redirected back
     *     to Gaming page after successful deposit or after click on "Back" button.
     */
    this.pubSubService.subscribe(this.title, this.pubSubService.API.REDIRECT, callback => {
      const cbURLParam = this.routingState.getRouteParam('cbURL', this.route.snapshot);
      // check for "cbURL" parameter in url
      if (cbURLParam) {
        this.storageService.set('redirect', cbURLParam.replace(/[<>]/g, ''));
      }
      let redirectUrl: string = this.storageService.get('redirect') || this.storageService.getCookie('gameBaseUrl');

      if (redirectUrl) {
        if (!this.navigationService.isAbsoluteUri(redirectUrl)) {
          redirectUrl = `http://${redirectUrl}`;
        }
        this.doRedirect(redirectUrl);
      } else if (_.isFunction(callback)) {
        callback();
      }
    });
    this.pubSubService.subscribe(this.title, this.pubSubService.API.DEFERRED_MODULES_LOADED, () => {
      gtmTimeout = this.windowRef.nativeWindow.setTimeout(() => {
        this.loadAdditionalIcons();
        this.awsService.addAction(this.COOKIE_LENGTH, this.windowRef.nativeWindow.document.cookie.length);

        if (this.sysConfig && this.sysConfig.gtm && this.sysConfig.gtm.enabled) {
          const gtmScriptLoaders = this.getGtmIds().map((gtmId: string): Observable<string | void> =>
            this.asyncScriptLoaderService.loadJsFile(`https://www.googletagmanager.com/gtm.js?id=${gtmId}`)
              .pipe(first(), catchError(() => of(undefined))));

          // try to initialize all the GTM scripts, and proceed if at least one has succeeded
          forkJoin(gtmScriptLoaders).pipe(
            mergeMap((loadResult: string[]) => loadResult && loadResult.some(r => !!r) ?
              this.asyncScriptLoaderService.loadJsFile('../../../../assets/gtm/gtm-script.js') :
              throwError('No GTM scripts were loaded.')),
            first()
          )
            .subscribe(() => {
              this.gtm.pushCachedEvents();
            }, err => console.warn(err));
        }

        this.asyncScriptLoaderService
          .loadJsFile('/assets/insomnia.js')
          .pipe(first())
          .subscribe(() => {
            this.insomnia.init();
          });
        if (this.device.isMobile) {
          this.asyncScriptLoaderService
            .loadJsFile('/assets/network-indicator.js')
            .pipe(first())
            .subscribe(() => {
              this.insomnia.initNetworkIndicator();
            });
        }
        this.windowRef.nativeWindow.clearTimeout(gtmTimeout);
      }, SCRIPTS_LOADING_DELAY);
    });

    this.pubSubService.subscribe(this.title, this.pubSubService.API.GAMING_OVERLAY_OPEN, () => {
      this.isGamingOpen = true;
    });
    this.pubSubService.subscribe(this.title, this.pubSubService.API.GAMING_OVERLAY_CLOSE, () => {
      this.isGamingOpen = false;
    });
    this.subscribeToRouterEvents();
  }

  private getGtmIds(): string[] {
    const gtmIdsConfigKey = 'googleTagManagerID',
      gtmIdsData: string | string[] = environment[gtmIdsConfigKey];
    this.windowRef.nativeWindow['gtmId'] = gtmIdsData[0];
    return gtmIdsData ? [].concat(gtmIdsData) : [];
  }

  private breakPoint(): void {
    const wnd = this.windowRef.nativeWindow;
    wnd.view = {
      mobile: wnd.innerWidth < this.device.mobileWidth,
      tablet: wnd.innerWidth >= this.device.mobileWidth && wnd.innerWidth < this.device.landTabletWidth,
      landscapeTablet: wnd.innerWidth >= this.device.landTabletWidth && wnd.innerWidth < this.device.desktopWidth,
      desktop: wnd.innerWidth >= this.device.desktopWidth
    };

    const deviceViewType = _.find(_.keys(this.windowRef.nativeWindow.view), type => this.windowRef.nativeWindow.view[type]);
    this.windowRef.nativeWindow.deviceViewType = deviceViewType;

    this.windowRef.nativeWindow.deviceType = this.getDeviceType(this.windowRef.nativeWindow.view);
  }

  /*
   * Function detect device type according to given object {deviceName: true|false}
   *
   * @param {*} devices
   * @returns string
   */
  private getDeviceType(devices: string[]): string {
    let deviceType = '';

    if (!devices) {
      return deviceType;
    }

    for (const index in devices) {
      if (_.has(devices, index) && devices[index]) {
        deviceType = index === 'landscapeTablet' ? 'tablet' : index;
        break;
      }
    }

    return deviceType;
  }

  /*
   * Show/hide user balance
   * @param {boolean} arg
   */
  private showUserBalance(arg: boolean): void {
    this.user.set({ showBalance: arg });
  }

  /*
   * Set logout state
   */
  private setLogoutState(): void {
    this.gtm.pushLogoutInfo();
    this.nativeBridge.logout();
  }

  private doRedirect(url: string): void {
    this.user.set({ isRedirecting: true });
    this.storageService.remove('redirect');
    this.storageService.removeCookie('gameBaseUrl');
    this.navigationService.redirectCurrPage(url);
  }

  /*
   * Set latest system configs to main scope
   * @params {object} data - system config data
   */
  private setConfigs(data: ISystemConfig): ISystemConfig {
    if (!data) {
      console.warn('System configs missed!');
      return;
    }

    this.sysConfig = data;
    this.transition = data.Banners && data.Banners.transitionDelay;

    return data;
  }

  private isFootbalTutorialActive(): boolean {
    return !!this.windowRef.document.querySelector('#football-tutorial-overlay.active');
  }

}
