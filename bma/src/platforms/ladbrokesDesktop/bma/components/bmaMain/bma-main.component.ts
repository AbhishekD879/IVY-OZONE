import { ChangeDetectorRef, Component, OnDestroy, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { ActivatedRoute, Event, NavigationStart, Router } from '@angular/router';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { Location } from '@angular/common';
import { Subscription } from 'rxjs';
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
import { LadbrokesBmaMainComponent } from '@ladbrokesMobile/bma/components/bmaMain/bma-main.component';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { GermanSupportService } from '@core/services/germanSupport/german-support.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { EzNavVanillaService } from '@app/core/services/ezNavVanilla/eznav-vanilla.service';
import { FanzoneHelperService } from '@app/core/services/fanzone/fanzone-helper.service';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';
import { InitNetworkIndicatorService } from '@app/core/services/networkIndicator/init-network-indicator.service';

@Component({
  selector: 'bma-main',
  templateUrl: 'bma-main.component.html'
})
export class DesktopBmaMainComponent extends LadbrokesBmaMainComponent implements OnInit, OnDestroy {
  routeChangeHandler: Subscription;

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
    private changeDetectorRef: ChangeDetectorRef,
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
      fanzoneStorageService,
      command,
      germanSupportService,
      fanzoneHelperService,
      initNetworkIndicatorService
    );
  }

  ngOnInit(): void {
    super.ngOnInit();
    this.routeChangeHandler = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationStart && event.url.indexOf('?addSelection=') > -1) {
        this.checkDesktopRemoteLink(event.url);
      }
    });
    this.pubSubService.subscribe('FanzoneLeftMenu', this.pubSubService.API.FANZONE_DATA, () => {
      this.changeDetectorRef.detectChanges();
	  });
  }

  ngOnDestroy(): void {
    if (this.routeChangeHandler) {
      this.routeChangeHandler.unsubscribe();
    }
  }

  /**
   * BMA-44014 Add one more format of adding selections to betslip via remote link
   *
   * webUrl: "https://sports.ladbrokes.com/en-gb/?addSelection=926061079" - mobenga
   *
   * @param location URL
   */
  private checkDesktopRemoteLink(link: string): void {
    const outcomeIds: string = link.substring(link.indexOf('?')).split('&').filter(x => x.indexOf('?addSelection=') > -1)[0].substring(14);
    this.command.executeAsync(
      this.command.API.ADD_TO_BETSLIP_BY_OUTCOME_IDS,
      [outcomeIds, true, true, false]
    );
  }
}
