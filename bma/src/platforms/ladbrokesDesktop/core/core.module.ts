import {
  CurrencyPipe,
  DatePipe,
  SlicePipe
} from '@angular/common';
import { APP_INITIALIZER, NgModule, NO_ERRORS_SCHEMA, Optional, SkipSelf } from '@angular/core';

import { InplayApiModule } from '@app/inPlay/inplay-api.module';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { BetHistoryApiModule } from '@app/betHistory/bet-history-api.module';

import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { DeferredLoaderService } from '@coreModule/services/deferredLoader/deferred-loader.service';

import { CoreRunService } from '@core/services/coreRun/core-run.service';
import { QuickbetDataProviderService } from '@core/services/quickbetDataProviderService/quickbet-data-provider.service';
import { BetFinderModule } from '@betFinderModule/betfinder.module';
import { AuthModule } from '@authModule/auth.module';
import { OlympicsModule } from '@olympicsModule/olympics.module';
import { BmaModule } from '@bmaModule/bma.module';
import { BppModule } from '@app/bpp/bpp.module';
import { SbModule } from '@sbModule/sb.module';
import { RetailApiModule } from '@platform/retail/retail-api.module';

import { RacingModule } from '@racingModule/racing.module';
import { ladbrokesGreyhoundConfig } from '@ladbrokesMobile/core/services/racing/config/greyhound.config';
import { ladbrokesHorseracingConfig } from '@ladbrokesDesktop/core/services/racing/config/horseracing.config';
import { GreyhoundService } from '@coreModule/services/racing/greyhound/greyhound.service';
import { HorseracingService } from '@ladbrokesMobile/core/services/racing/horseracing/horseracing.service';
import { RacingYourCallService } from '@core/services/racing/racingYourCall/racing-your-call.service';
import { NextRacesService } from '@core/services/racing/nextRaces/next-races.service';
import { DailyRacingService } from '@core/services/racing/dailyRacing/daily-racing.service';
import { TimeFormService } from '@core/services/racing/timeForm/time-form.service';
import { TimeFormApiService } from '@core/services/racing/timeForm/time-form-api.service';

import { GamingService } from '@core/services/sport/gaming.service';
import { RacingService } from '@ladbrokesMobile/core/services/sport/racing.service';
import { SportService } from '@core/services/sport/sport.service';
import { DigitalSportBetsService } from '@core/services/digitalSportBets/digital-sport-bets.service';
import { BackButtonService } from '@core/services/backButton/back-button.service';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { VisEventService } from '@core/services/visEvent/vis-event.service';
import { BuildUtilityService } from '@core/services/buildUtility/build-utility.service';
import { CommentsService } from '@core/services/comments/comments.service';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { SiteServerUtilityService } from '@core/services/siteServerUtility/site-server-utility.service';
import { SsModule } from '@ss/ss.module';
import { moduleImportGuard } from '@core/module-import.guard';
import { BetPlacementErrorTrackingService } from '@core/services/betPlacementErrorTracking/bet-placement-error-tracking';
import { BetslipSelectionsDataService } from '@core/services/betslipSelectionsData/betslip-selections-data';
import { BetslipTabsService } from '@core/services/betslipTabs/betslip-tabs.service';
import { brandConfig, brandConfigToken } from '@core/services/brand/brand.config';
import { CasinoLinkService } from '@core/services/casinoLink/casino-link.service';
import { CmsToolsService } from '@core/services/cms/cms.tools';
import { SubscriptionsManagerService } from '@core/services/subscriptionsManager/subscriptions-manager.service';
import { DeviceService } from '@core/services/device/device.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { ExistNewUserService } from '@core/services/existNewUser/exist-new-user.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { InsomniaService } from '@core/services/insomnia/insomnia.service';
import { PrivateMarketsService } from '@core/services/privateMarkets/private-markets.service';
import { LiveServConnectionService } from '@core/services/liveServ/live-serv-connection.service';
import { LiveUpdatesWSService } from '@core/services/liveUpdatesWS/liveUpdatesWS.service';
import { LiveServIframeService } from '@core/services/liveServ/live-serv-iframe.service';
import { WsConnectorService } from '@core/services/wsConnector/ws-connector.service';
import { RemoteBetslipService } from '@core/services/remoteBetslip/remote-betslip.service';
import { LpAvailabilityService } from '@core/services/lpAvailability/lp-availability.service';
import { ModuleExtensionsStorageService } from '@core/services/moduleExtensionsStorage/module-extensions-storage.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { UpdateEventService } from '@core/services/updateEvent/update-event.service';
import { WsUpdateEventService } from '@core/services/wsUpdateEvent/ws-update-event.service';
import { LStoSSDataStructureConverterService } from '@core/services/lStoSSDataConverter/ls-ss-data-converter.service';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { ReloadService } from '@core/services/reload/reload.service';
import { ResolveService } from '@core/services/resolve/resolve.service';
import { ServingService } from '@core/services/serving/serving.service';
import { ModuleRibbonService } from '@core/services/moduleRibbon/module-ribbon.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { StorageService } from '@core/services/storage/storage.service';
import { TempStorageService } from '@core/services/storage/temp-storage.service';
import { SubscribersRouteService } from '@core/services/subscribersRoute/subscribers-route.service';
import { TimeService } from '@core/services/time/time.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { UserService } from '@core/services/user/user.service';
import { CashOutLabelService } from '@core/services/cashOutLabel/cash-out-label.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { DynamicComponentsService } from '@core/services/dynamicComponents/dynamic-components.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { IteratorService } from '@core/services/iterator/iterator.service';
import { httpInterceptorProviders } from '@core/httpInterceptors';
import { MaintenanceService } from '@core/services/maintenance/maintenance.service';
import { VisDataHandlerService } from '@core/services/visDataHandler/vis-data-handler.service';
import { UkToteLiveUpdatesService } from '@core/services/ukTote/uktote-live-update.service';
import { UkToteEventsLinkingService } from '@core/services/ukTote/uktote-events-linking.service';
import { AfterLoginNotificationsService } from '@coreModule/services/afterLoginNotifications/after-login-notifications.service';
import { ClientUserAgentService } from '@core/services/clientUserAgent/client-user-agent.service';
import { CurrencyCalculatorService } from '@core/services/currencyCalculatorService/currency-calculator.service';
import { ExtraPlaceService } from '@core/services/racing/extraPlace/extra-place.service';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';

import { FavouritesModule } from '@favouritesModule/favourites.module';

// Overrided modules
import { SharedModule } from '@sharedModule/shared.module';
import { BreadcrumbsService } from '@ladbrokesDesktop/core/services/breadcrumbs/breadcrumbs.service';
import { GermanSupportService } from '@app/core/services/germanSupport/german-support.service';
import { GermanSupportFeaturedService } from '@ladbrokesMobile/core/services/germanSupportFeatured/german-support-featured.service';
import { GermanSupportInPlayService } from '@ladbrokesMobile/core/services/germanSupportInPlay/german-support-inplay.service';
import { BonusSuppressionService } from '@coreModule/services/BonusSuppression/bonus-suppression.service';
import { InitNetworkIndicatorService } from '@coreModule/services/networkIndicator/init-network-indicator.service';
import { ScorecastDataService } from '@coreModule/services/scorecastData/scorecast-data.service';

@NgModule({
  // define all feature modules + shared module
  imports: [
    BetslipApiModule,
    BetHistoryApiModule,
    InplayApiModule,
    SharedModule,
    BppModule,
    AuthModule,
    SsModule,
    RetailApiModule,
    BetFinderModule,
    SbModule,
    RacingModule,
    OlympicsModule,
    BmaModule,
    FavouritesModule
  ],

  // define app level services/providers
  providers: [
    GermanSupportService,
    GermanSupportFeaturedService,
    GermanSupportInPlayService,
    BackButtonService,
    WindowRefService,
    ReloadService,
    DialogService,
    TimeSyncService,
    NativeBridgeService,
    CmsToolsService,
    UpdateEventService,
    WsUpdateEventService,
    LStoSSDataStructureConverterService,
    CacheEventsService,
    GtmService,
    GtmTrackingService,
    ModuleRibbonService,
    FreeBetsService,
    { provide: brandConfigToken, useValue: brandConfig },
    SubscriptionsManagerService,
    RaceOutcomeDetailsService,
    StorageService,
    SessionStorageService,
    TempStorageService,
    UserService,
    DatePipe,
    SlicePipe,
    CurrencyPipe,
    DeviceService,
    TimeService,
    FiltersService,
    CasinoLinkService,
    FracToDecService,
    InfoDialogService,
    WsConnectorService,
    RemoteBetslipService,
    LpAvailabilityService,
    ExistNewUserService,
    InsomniaService,
    BetslipSelectionsDataService,
    BetPlacementErrorTrackingService,
    ResolveService,
    ServingService,
    ModuleExtensionsStorageService,
    BetslipTabsService,
    LiveServConnectionService,
    LiveUpdatesWSService,
    LiveServIframeService,
    VisEventService,
    VisDataHandlerService,
    SubscribersRouteService,
    RoutingHelperService,
    NavigationService,
    DomToolsService,
    DynamicComponentsService,
    RendererService,
    ChannelService,
    SeoDataService,
    IteratorService,
    PrivateMarketsService,
    httpInterceptorProviders,
    MaintenanceService,
    CoreToolsService,
    CommentsService,
    BuildUtilityService,
    SiteServerRequestHelperService,
    SiteServerUtilityService,
    SiteServerService,
    CashOutLabelService,
    SportEventHelperService,
    UkToteLiveUpdatesService,
    UkToteEventsLinkingService,
    AfterLoginNotificationsService,
    SportService,
    GamingService,
    RacingService,
    DigitalSportBetsService,
    CoreRunService,
    QuickbetDataProviderService,
    ClientUserAgentService,
    CurrencyCalculatorService,
    DynamicLoaderService,
    DeferredLoaderService,
    BreadcrumbsService,
    RacingYourCallService,
    DailyRacingService,
    NextRacesService,
    HorseracingService,
    GreyhoundService,
    TimeFormService,
    TimeFormApiService,
    ExtraPlaceService,
    BonusSuppressionService,
    InitNetworkIndicatorService,
    { provide: 'HORSERACING_CONFIG', useValue: ladbrokesHorseracingConfig },
    { provide: 'GREYHOUND_CONFIG', useValue: ladbrokesGreyhoundConfig },
    {
      provide: APP_INITIALIZER,
      useFactory: function (coreRunService: CoreRunService) {
        return function () {
          coreRunService.init();
        };
      },
      deps: [CoreRunService],
      multi: true
    },
    ScorecastDataService
  ],

  // avoid declarations, shared ui components should be in shared module,
  schemas: [NO_ERRORS_SCHEMA]
})
export class CoreModule {
  constructor(@Optional() @SkipSelf() parentModule: CoreModule) {
    moduleImportGuard(parentModule, 'CoreModule');
  }
}
