import { Component, OnInit, ChangeDetectionStrategy, ChangeDetectorRef, ComponentFactoryResolver } from '@angular/core';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { Subscription } from 'rxjs';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { IFeaturedModel } from '@app/featured/models/featured.model';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { FanzoneAppModuleService } from '@app/fanzone/services/fanzone-module.service';
import { WsUpdateEventService } from '@core/services/wsUpdateEvent/ws-update-event.service';
import { TemplateService } from '@shared/services/template/template.service';
import { CommentsService } from '@app/core/services/comments/comments.service';
import environment from '@environment/oxygenEnvConfig';
import { IFanzoneSiteCoreBanner, FanzoneDetails, FanzoneConfig } from '@app/fanzone/models/fanzone.model';
import { ISiteCoreTeaserFromServer } from '@app/core/models/aem-banners-section.model';
import { ISportTeamColors } from '@app/sb/models/sport-configuration.model';
import { IFanzoneTab } from '@app/fanzone/models/fanzone-tab.model';
import { ISystemConfig } from '@app/core/services/cms/models';
import { IFanzoneGameTooltipConfig, IFanzoneGameTooltipArgs } from "@app/fanzone/models/fanzone.model";
import { Router, Event, NavigationEnd, ActivatedRoute } from '@angular/router';
import { FANZONE, fanzoneHeading, FanzoneHomeTagName,GTM_DATA_FZ_TAB } from '@app/fanzone/constants/fanzoneconstants';
import { FanzoneHelperService } from '@app/core/services/fanzone/fanzone-helper.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { IFanzonePreferences } from '@app/fanzone/models/fanzone-preferences.model';
import { FanzoneSharedService } from '@app/lazy-modules/fanzone/services/fanzone-shared.service';
import { DeviceService } from '@frontend/vanilla/core';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';
import { UserService } from '@core/services/user/user.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { DialogService } from '@app/core/services/dialogService/dialog.service';
import { FanzoneOptinEmailDialogComponent } from '@app/lazy-modules/fanzone/components/fanzoneOptinEmailDialog/fanzone-optin-email-dialog.component';
import { FanzoneGamesService } from '@app/fanzone/services/fanzone-games.service';
import { IFanzoneGamesSignPostingData } from "@app/fanzone/models/fanzone-games.model";
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { ICommunicationSettings } from '@app/lazy-modules/fanzone/models/fanzone-email-optin.model';
import { Default_Optin_Fields } from '@app/lazy-modules/fanzone/fanzone.constant';
import { StorageService } from '@app/core/services/storage/storage.service';

@Component({
  selector: 'app-fanzone-home',
  template: ``,
  styleUrls: ['./fanzone-home.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FanzoneAppHomeComponent extends AbstractOutletComponent implements OnInit {
  fanzoneHead = fanzoneHeading;
  fanzoneName: string;
  fanzoneDesc: string;
  fanzoneModuleData: IFeaturedModel;
  sportName: string = FANZONE.football;
  initializedFanzoneModulesMap: { [key: string]: boolean } = {};
  public fanzoneBannerImage: string = '';
  public fanzoneBannerImageDesktop: string = '';
  siteCoreFanzone: ISiteCoreTeaserFromServer[];
  readonly CMS_UPLOADS_PATH: string = environment.CMS_ROOT_URI + environment.FIVEASIDE.svgImagePath;
  teamData: ISportTeamColors;
  fanzoneTeam: any;
  isNowNextTab: boolean = false;
  isClub: boolean = false;
  isStats: boolean = false;
  isGamingTab: boolean = false;
  activeTabId = FANZONE.activeTabId;
  defaultTab = FANZONE.defaultTab;
  preferences: IFanzonePreferences;
  activeTab: IFanzoneTab;
  fanzoneTabs: IFanzoneTab[] = [];
  backgroundHeaderColor: string = '';
  headerOpacity: string = 'CC';
  gtmDataTab = {
    event: GTM_DATA_FZ_TAB.EVENT,
    eventAction: GTM_DATA_FZ_TAB.EVENT_ACTION,
    eventCategory: GTM_DATA_FZ_TAB.EVENT_CATEGORY,
    eventLabel: GTM_DATA_FZ_TAB.EVENT_LABEL
  };
  newSignPostingData: IFanzoneGamesSignPostingData;
  fanzoneGameTooltipConfig: IFanzoneGameTooltipConfig;
  private notifyTimeout: number;
  toolTipArgs: IFanzoneGameTooltipArgs;

  private tagName: string = FanzoneHomeTagName;
  protected navigationServiceSubscription: Subscription;
  protected sysConfigSubscription: Subscription;
  protected routeChangeListener: Subscription;

  constructor(
    protected cms: CmsService,
    protected navigationService: NavigationService,
    protected dynamicComponentLoader: DynamicLoaderService,
    protected routingState: RoutingState,
    protected fanzoneModuleService: FanzoneAppModuleService,
    protected pubsub: PubSubService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected wsUpdateEventService: WsUpdateEventService,
    protected templateService: TemplateService,
    protected commentsService: CommentsService,
    protected router: Router,
    protected route: ActivatedRoute,
    protected fanzoneStorageService: FanzoneStorageService,
    protected fanzoneHelperService: FanzoneHelperService,
    protected fanzoneSharedService: FanzoneSharedService,
    protected gtmService: GtmService,
    protected device: DeviceService,
    protected user: UserService,
    protected bonusSuppression: BonusSuppressionService,
    protected dialogService: DialogService,
    protected componentFactoryResolver: ComponentFactoryResolver,
    protected fanzoneGamesService: FanzoneGamesService,
    protected windowRefService: WindowRefService,
    protected storageService: StorageService
  ) {
    super();
  }

  ngOnInit(): void {
    this.pubsub.subscribe(this.tagName, this.pubsub.API.FANZONE_DATA, () => {
      this.init();
      this.changeDetectorRef.detectChanges();
    });
    this.init();
    this.pubsub.subscribe(this.tagName, this.pubsub.API.FANZONE_SHOW_GAMES_TAB, () => {
      const gamesTab = this.fanzoneTabs.find((tab) => {
        return tab.id === FANZONE.games.id;
      });
      this.activeTab = gamesTab;
      this.router.navigateByUrl(gamesTab.url);
    });
    this.pubsub.subscribe(this.tagName, this.pubsub.API.FANZONE_SHOW_GAMES_TOOLTIP, () => {
      this.showFanzoneGamesTooltip();
    });
  }

  private filterIOSAppVersion() {
    this.fanzoneSharedService.isIosBlackListedDevice().subscribe((isBlackListedDevice) => {
      if (isBlackListedDevice) {
        this.pubsub.publish(this.pubsub.API.HIDE_FANZONE_GAMES_TAB);
        this.fanzoneTabs.pop();
      }
    });
  }
  
  /**
   * Open Fanzone Optin Email Dialog
   * @param communicationTypes {Object}
   * @returns {void}
   * @private
   */
  private openFanzoneOptinEmailDialog(fanzoneDetailResponse): void {
    this.fanzoneSharedService.getUserCommunicationSettings().subscribe((data: ICommunicationSettings) => {
      const emailData = data && data.communicationTypes.filter((type) => type.name === 'Email');
      if (emailData && !(emailData[0].selected)) {
        this.dialogService.openDialog('fanzoneOptinEmail', this.componentFactoryResolver.resolveComponentFactory(FanzoneOptinEmailDialogComponent), false, { data: {email: emailData[0], fanzoneDetailResponse: fanzoneDetailResponse }});
      } else if(emailData && emailData[0].selected) {
        // Show Fanzone Games Popup 
        this.fanzoneSharedService.showFanzoneGamesPopup(fanzoneDetailResponse);
        this.fanzoneSharedService.postEmailOptinDetails(Default_Optin_Fields, true);
      }
    });
  }

  /**
  * Init function to get system config data and set active tab as per route value
  * @returns {void}
  */
  private init(): void {
    this.fanzoneTeam = this.fanzoneStorageService.get('fanzone');
    this.fanzoneHelperService.selectedFanzone && this.getFanzoneInitData(this.fanzoneHelperService.selectedFanzone);
    this.showDefaultTab();
    
    this.routeChangeListener = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd) {
        this.checkNewSignPostingIcon();
        const display = event.urlAfterRedirects.substr(event.urlAfterRedirects.lastIndexOf('/') + 1, event.urlAfterRedirects.length);
        const activeTab = this.fanzoneTabs.filter((tab) => {
            return tab.id === display;
          })
        if(activeTab && activeTab[0]) {
          this.tabsSwitcher(activeTab[0]);
        }
      }
    });
  }

  /**
   * Shows fanzone default page
   * @param {}
   * @returns { void }
   */
  private showDefaultTab(){
    const url = this.router.url.substr(this.router.url.lastIndexOf('/') + 1, this.router.url.length);
    const initTab = this.fanzoneTabs.filter((tab) => {
      return tab.id === url;
    });
    this.activeTab = initTab[0];

    if (!this.activeTab && this.fanzoneTabs && this.fanzoneTabs.length) {
      const defaultActiveTab = this.fanzoneTabs.filter((tab) => {
        return tab.id === FANZONE.nowandnext.id;
      });
      this.activeTab = defaultActiveTab[0];
      this.goToDefaultPage();
    }
    
    if (this.activeTab) {
      this.gtmDataTab.eventLabel = this.activeTab.title;
      this.gtmService.push(this.gtmDataTab.event, this.gtmDataTab);
    }
  }

  /**
   * Shows fanzone tooltip if user is visited for first time
   * @param {}
   * @returns { void }
   */
  private showFanzoneGamesTooltip(): void {
    this.fanzoneSharedService.getSystemConfig().subscribe((config: ISystemConfig) => {
      if (config.fanzoneGamesTooltip) {
        this.fanzoneGameTooltipConfig = config.fanzoneGamesTooltip;
        const showFanzoneGamesTooltip = this.fanzoneGamesService.showFanzoneGamesTooltip(this.fanzoneGameTooltipConfig);
        this.toolTipArgs = {
          show: showFanzoneGamesTooltip,
          message: this.fanzoneGameTooltipConfig.Message
        };
        this.changeDetectorRef.detectChanges();
        if (showFanzoneGamesTooltip) {
          this.positionTooltip();
          this.notifyTimeout = this.windowRefService.nativeWindow.setTimeout(() => {
            this.toolTipArgs.show = false;
            this.fanzoneGamesService.setFanzoneGamesTooltipSeen();
            this.changeDetectorRef.detectChanges();
          }, this.fanzoneGameTooltipConfig.Delay * 1000);
        }
        this.changeDetectorRef.detectChanges();
      }
    }); 
  }

  /**
   * Checks for new sign posting
   * @param {}
   * @returns { void }
   */
  private checkNewSignPostingIcon(): void {
    const gamesTab = this.fanzoneTabs.find(tab => tab.id === FANZONE.games.id);
    if (gamesTab) {
      const isNewSignPostingIconSeen = this.fanzoneGamesService.showNewSignPostingIcon(this.newSignPostingData);
      gamesTab.newSignPostingIcon = isNewSignPostingIconSeen;
    }
  }

  /**
   * Switches the active tab as per display value
   * @param {display: IFanzoneTab}
   * @returns { void }
   */
  private tabsSwitcher(display: IFanzoneTab): void {
    this.activeTab = display;
    this.gtmDataTab.eventLabel = this.activeTab.title;
    this.gtmService.push(this.gtmDataTab.event,this.gtmDataTab);
    this.changeDetectorRef.markForCheck();
  }

  /**
   * Get the fanzone tabs data from CMS
   * @param {fanzoneConfiguration: FanzoneConfig}
   * @returns { void }
   */
  getFanzoneTabsData(fanzoneConfiguration: FanzoneConfig) {
    this.fanzoneTabs = [];
    this.isNowNextTab = fanzoneConfiguration.showNowNext;
    this.isStats = fanzoneConfiguration.showStats;
    this.isClub = fanzoneConfiguration.showClubs;
    this.isGamingTab = fanzoneConfiguration.showGames;

    const nowandnextUrl = FANZONE.nowandnext.url.replace('$teamName', this.fanzoneTeam.teamName);
    const statsUrl = FANZONE.stats.url.replace('$teamName', this.fanzoneTeam.teamName);
    const clubUrl = FANZONE.club.url.replace('$teamName', this.fanzoneTeam.teamName);
    const gameUrl = FANZONE.games.url.replace('$teamName', this.fanzoneTeam.teamName);

    if (this.isNowNextTab && this.bonusSuppression.checkIfYellowFlagDisabled(this.fanzoneHead, FANZONE.nowandnext.id)) {
      this.fanzoneTabs.push(this.fanzoneModuleService.createTab(FANZONE.nowandnext.tabName, FANZONE.nowandnext.id, nowandnextUrl, this.isNowNextTab));
    }
    if (this.isStats && this.bonusSuppression.checkIfYellowFlagDisabled(this.fanzoneHead, FANZONE.stats.id)) {
      this.fanzoneTabs.push(this.fanzoneModuleService.createTab(FANZONE.stats.tabName, FANZONE.stats.id, statsUrl, this.isStats));
    }
    if (this.isClub && this.bonusSuppression.checkIfYellowFlagDisabled(this.fanzoneHead, FANZONE.club.id)) {
      this.fanzoneTabs.push(this.fanzoneModuleService.createTab(FANZONE.club.tabName, FANZONE.club.id, clubUrl, this.isClub));
    }
    if (this.isGamingTab) {
      const showNewSignPostingIcon = this.fanzoneGamesService.showNewSignPostingIcon(this.newSignPostingData);
      this.fanzoneTabs.push(this.fanzoneModuleService.createTab(FANZONE.games.tabName, FANZONE.games.id, gameUrl, this.isGamingTab, showNewSignPostingIcon));
    }
  }

  /**
   * Get FanzoneDetail data
   * @returns { void }
   */
  getFanzoneInitData(fanzoneDetailResponse: FanzoneDetails): void {
    this.showSpinner();
    this.fanzoneName = fanzoneDetailResponse.name;
    this.fanzoneDesc = fanzoneDetailResponse.location;
    const assetManagmentLink = fanzoneDetailResponse.assetManagementLink;
    // Gets fanzone new signposting data and tooltip config
    if (fanzoneDetailResponse.fanzoneConfiguration.showGames) {
      this.getFanzoneGamesData(fanzoneDetailResponse);
    } else {
      this.getFanzoneTabsData(fanzoneDetailResponse.fanzoneConfiguration);
    }
    this.openFanzoneOptinEmailDialog(fanzoneDetailResponse);

    // GetPromotions from sitecore
    const bannerUrl = this.device.isMobile && !this.device.isTablet ? fanzoneDetailResponse.fanzoneBanner : fanzoneDetailResponse.fanzoneConfiguration.fanzoneBannerDesktop;
    this.getFanzoneBanner(bannerUrl);
    this.cms.getTeamsColors([assetManagmentLink], 16).subscribe((teamData) => {
      [this.teamData] = teamData;
      this.backgroundHeaderColor = this.teamData && (this.teamData.primaryColour + this.headerOpacity);
      this.hideSpinner();
      this.changeDetectorRef.detectChanges();
    }, () => {
      this.showError();
    });
  }

  /**
   * Gets fanzone new signposting data
   * @return {void}
   */
  getFanzoneGamesData(fanzoneDetailResponse: FanzoneDetails): void {
    this.fanzoneSharedService.getFanzoneNewSignPosting()
      .subscribe((res: IFanzoneGamesSignPostingData[]) => {
        this.newSignPostingData = res[0];
        this.getFanzoneTabsData(fanzoneDetailResponse.fanzoneConfiguration);
        this.showDefaultTab();
        this.filterIOSAppVersion();
      });
  }

  /**
   * fetch fanzone page banner
   * @return {void}
   */
  getFanzoneBanner(bannerUrl: string): void {
    this.fanzoneModuleService.getFanzoneImagesFromSiteCore().subscribe((response: IFanzoneSiteCoreBanner[]) => {
      if (response.length > 0) {
        const [teaserResponse] = response;
        this.siteCoreFanzone = teaserResponse.teasers ?? [];
        this.siteCoreFanzone.forEach((siteCoreData) => {
          if (siteCoreData.itemId === bannerUrl) {
            this.fanzoneBannerImage = siteCoreData.backgroundImage.src;
            this.hideSpinner();
            this.changeDetectorRef.detectChanges();
          }
        })
      }
    }, () => {
      this.showError();
    });
  }

  /**
   * Check if  team exist
   * @returns { boolean }
   */
  checkForTeamsExist(): boolean {
    return (!!this.teamData && Object.keys(this.teamData).length > 0);
  }

  /**
   * redirect user to default page when topbar clicked
   * @returns { void }
   */
  goToDefaultPage(): void {
    this.router.navigateByUrl(`/fanzone/sport-football/${this.fanzoneTeam.teamName}/now-next`);
  }
  
  /**
   * show user notification popup / preference center
   */
  showNotification() {
    this.fanzoneSharedService.showNotifications(true);
  }

  /**
   * Places tooltip with respect to games tab
   * @returns { void }
   */
  positionTooltip() {
    const bannerHeight = this.windowRefService.document.querySelector('.fanzone-banner')['clientHeight'];
    const tooltipElement = this.windowRefService.document.querySelector('.bs-fanzone-game-tooltip .tooltip');
    const gamesTabElementWidth = this.windowRefService.document.querySelectorAll('.switch')[this.fanzoneTabs.length-1]['clientWidth'];
    const gamesTabNameElementWidth = this.windowRefService.document.querySelectorAll('.tab-name')[this.fanzoneTabs.length-1]['clientWidth'];
    const tooltipHeight = tooltipElement.clientHeight;
    if( tooltipElement && tooltipElement['style']) {
      tooltipElement['style'].top = (bannerHeight-tooltipHeight) + 'px';
      tooltipElement['style'].right = (gamesTabElementWidth - gamesTabNameElementWidth)/2 + 'px';
    }
    this.changeDetectorRef.detectChanges();
  }

  ngOnDestroy() {
    this.routeChangeListener && this.routeChangeListener.unsubscribe();
    this.pubsub.unsubscribe(this.tagName);
    this.windowRefService.nativeWindow.clearTimeout(this.notifyTimeout);
  }
}
