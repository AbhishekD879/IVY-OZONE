import { forkJoin, Subscription } from 'rxjs';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { Location } from '@angular/common';
import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CmsService } from '@ladbrokesMobile/core/services/cms/cms.service';
import { UserService } from '@core/services/user/user.service';
import { StorageService } from '@core/services/storage/storage.service';
import { AfterLoginNotificationsService } from '@coreModule/services/afterLoginNotifications/after-login-notifications.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { AuthService } from '@authModule/services/auth/auth.service';
import { InsomniaService } from '@core/services/insomnia/insomnia.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { DeviceService } from '@core/services/device/device.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { BmaMainComponent } from '@app/bma/components/bmaMain/bma-main.component';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { GermanSupportService } from '@core/services/germanSupport/german-support.service';
import { ISportCategory, ISystemConfig } from '@app/core/services/cms/models';
import { CommandService } from '@core/services/communication/command/command.service';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { EzNavVanillaService } from '@app/core/services/ezNavVanilla/eznav-vanilla.service';
import { bmaChannelName, FANZONE } from '@app/fanzone/constants/fanzoneconstants';
import { FanzoneHelperService } from '@app/core/services/fanzone/fanzone-helper.service';
import { FanzoneDetails } from '@app/core/services/fanzone/models/fanzone.model';
import { IGATrackingModel } from '@app/core/models/gtm.event.model';
import { GA_TRACKING } from '@app/shared/constants/channel.constant';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';
import { InitNetworkIndicatorService } from '@app/core/services/networkIndicator/init-network-indicator.service';
import { IFanzoneComingBack } from '@app/lazy-modules/fanzone/models/fanzone-cb.model';

@Component({
  selector: 'bma-main',
  templateUrl: 'bma-main.component.html'
})
export class LadbrokesBmaMainComponent extends BmaMainComponent implements OnInit, OnDestroy {
  sysConfig: ISystemConfig;
  NW_I_Object: any = {};
  showNetworkIndicator = true;
  fanzoneCbData: IFanzoneComingBack[] = [];
  protected platformPath: string = 'ladbrokesMobile';
  protected hashListener: Function;
  private _recaptchaSub: Subscription;
  private readonly RECAPTCHA_TITLE: string = 'recaptchaTitle';
  private fanzone: FanzoneDetails;
  private fanzoneChannelName: string = bmaChannelName;

  GTMTrackingObj: IGATrackingModel = {
    isHomePage: this.checkIfHomeUrl(),
    event: GA_TRACKING.event,
    GATracking: {
      eventAction: GA_TRACKING.eventAction,
      eventCategory: GA_TRACKING.sportsRibbon.eventCategory,
      eventLabel: "",
    }
  };
  constructor(
    device: DeviceService,
    user: UserService,
    windowRef: WindowRefService,
    route: ActivatedRoute,
    locale: LocaleService,
    nativeBridge: NativeBridgeService,
    pubsub: PubSubService,
    cms: CmsService,
    storageService: StorageService,
    afterLoginNotifications: AfterLoginNotificationsService,
    navigationService: NavigationService,
    authService: AuthService,
    location: Location,
    insomnia: InsomniaService,
    gtm: GtmService,
    filtersService: FiltersService,
    coreTools: CoreToolsService,
    domSanitizer: DomSanitizer,
    rendererService: RendererService,
    domTools: DomToolsService,
    router: Router,
    dialogService: DialogService,
    routingState: RoutingState,
    dynamicComponentLoader: DynamicLoaderService,
    asyncScriptLoaderService: AsyncScriptLoaderService,
    awsService: AWSFirehoseService,
    sessionStorage: SessionStorageService,
    seoDataService: SeoDataService,
    ezNavVanillaService: EzNavVanillaService,

    protected fanzoneStorageService: FanzoneStorageService,
    protected command: CommandService,
    protected germanSupportService: GermanSupportService,
    protected fanzoneHelperService: FanzoneHelperService,
    protected initNetworkIndicatorService: InitNetworkIndicatorService
  ) {
    super(
      device,
      user,
      windowRef,
      route,
      locale,
      nativeBridge,
      pubsub,
      cms,
      storageService,
      afterLoginNotifications,
      navigationService,
      authService,
      location,
      insomnia,
      gtm,
      filtersService,
      coreTools,
      domSanitizer,
      rendererService,
      domTools,
      router,
      dialogService,
      routingState,
      dynamicComponentLoader,
      asyncScriptLoaderService,
      awsService,
      sessionStorage,
      seoDataService,
      ezNavVanillaService,
      fanzoneHelperService,
      initNetworkIndicatorService
    );
  }

  ngOnInit(): void {
    super.ngOnInit();
    this.fanzoneHelperService.PublishFanzoneData();
    const screen = this.windowRef.nativeWindow;
    this.checkRemoteLink(screen.location.hash);
    this.hashListener = this.rendererService.renderer.listen(screen, 'hashchange', () => {
      this.checkRemoteLink(screen.location.hash);
    });
    this.pubSubService.subscribe('LadbrokesBmaMainComponent', [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGIN
    ], () => {
      this.pubSubService.subscribe("fanzone_coming_back", this.pubSubService.API.FANZONE_COMING_BACK, (data: IFanzoneComingBack) => {
        this.fanzoneCbData = [data];
      });
    });
  }

  ngOnDestroy(): void {
    super.ngOnDestroy();
    this.pubSubService.unsubscribe('LadbrokesBmaMainComponent');
    this.pubSubService.unsubscribe(this.fanzoneChannelName);
    this._recaptchaSub && this._recaptchaSub.unsubscribe();
    this.pubSubService.unsubscribe(this.RECAPTCHA_TITLE);
  }

  protected getMenuItems(appBuildVersion?: string, selectedTeam?: FanzoneDetails): void {
    forkJoin(
      this.cms.getMenuItems(appBuildVersion, selectedTeam),
      this.cms.getSystemConfig(false)
    ).subscribe((cmsData: Partial<ISportCategory & ISystemConfig>) => {
      const menuItems = cmsData[0];
      this.sysConfig = cmsData[1];
      this.widgetDataStore = [];
      this.betSlipAnimation = this.sysConfig.Generals.betSlipAnimation;
      this.menuItems = this.filterRibbonItems(menuItems);
      this.showSportMenu();
      this.showWidgetColumns();

      this.windowResizeListener = this.rendererService.renderer.listen(this.windowRef.nativeWindow, 'resize', () => {
        this.showWidgetColumns();
      });
      this.pubSubService.subscribe('LadbrokesBmaMainComponent',
        [this.pubSubService.API.SESSION_LOGIN, this.pubSubService.API.SESSION_LOGOUT], () => {
          this.filterRibbonItems(menuItems);
        });
    })
    this.pubSubService.subscribe(this.fanzoneChannelName, this.pubSubService.API.FANZONE_DATA, (fanzone: any) => {
      this.fanzone = fanzone;
      fanzone && this.getMenuItems();
    });
    this.fanzoneHelperService.getSelectedFzUpdate().subscribe((selectedTeam: FanzoneDetails) => {
      this.getMenuItems('', selectedTeam);
    });
  }

  /**
   * Filter menu ribbon for german users
   * @param {ISportCategory[]} menuItems
   * @returns {ISportCategory[]}
   */
  private filterRibbonItems(menuItems: ISportCategory[], fanzone?: any): ISportCategory[] {
    // Filtering Ribbon for Fanzone
    const fanzoneIndex = menuItems.findIndex(link => link.sportName.includes(FANZONE.fanzoneIndex));
    const fanzoneStorage = this.fanzoneStorageService.get('fanzone');
    if (fanzoneIndex !== -1) {
      menuItems[fanzoneIndex].selectedFanzone = this.fanzone;
      if (fanzoneStorage && fanzoneStorage.teamId && this.fanzone && this.fanzone.active && this.fanzone.fanzoneConfiguration.sportsRibbon && this.user.status) {
        menuItems[fanzoneIndex].disabled = false;
      } else {
        menuItems[fanzoneIndex].disabled = true;
        menuItems[fanzoneIndex].fzDisabled = true;
      }
    }

    return this.menuItems = menuItems.filter((item: ISportCategory) => {
      item.iconClass = this.filtersService.sportCatIcon(item.linkTitle);
      return !item.disabled && !item.hidden && item.showInHome && !this.germanSupportService.isRestrictedSport(item);
    });
  }

  /**
   * BMA-44014 Add one more format of adding selections to betslip via remote link
   *
   * #!?tab=featured&externalSelectionId=:outcomeId - mobenga
   *
   * @param location hash
   */
  private checkRemoteLink(link: string): void {
    if (link && link.indexOf('#!?') > -1 && link.indexOf('externalSelectionId=') > -1) {
      const outcomeIds: string = link.split('&').filter(x => x.indexOf('externalSelectionId=') > -1)[0].substring(20);
      this.command.executeAsync(
        this.command.API.ADD_TO_BETSLIP_BY_OUTCOME_IDS,
        [outcomeIds, true, true, true]
      );
    }
  }
}
