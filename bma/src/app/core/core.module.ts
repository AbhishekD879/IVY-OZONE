import { CurrencyPipe, DatePipe, SlicePipe } from '@angular/common';
import { APP_INITIALIZER, NgModule, NO_ERRORS_SCHEMA, Optional, SkipSelf } from '@angular/core';

import { InplayApiModule } from '@app/inPlay/inplay-api.module';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { BetHistoryApiModule } from '@app/betHistory/bet-history-api.module';

import { BmaModule } from '@bmaModule/bma.module';
import { BppModule } from '@app/bpp/bpp.module';
import { SbModule } from '@sbModule/sb.module';
import { RetailApiModule } from '@retailModule/retail-api.module';
import { SharedModule } from '@sharedModule/shared.module';
import { SsModule } from '@ss/ss.module';
import { FavouritesModule } from '@favouritesModule/favourites.module';

import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { DeferredLoaderService } from '@coreModule/services/deferredLoader/deferred-loader.service';
import { DynamicComponentsService } from '@coreModule/services/dynamicComponents/dynamic-components.service';
import { CoreRunService } from '@coreModule/services/coreRun/core-run.service';
import { QuickbetDataProviderService } from '@coreModule/services/quickbetDataProviderService/quickbet-data-provider.service';

import { greyhoundConfig } from '@coreModule/services/racing/config/greyhound.config';
import { horseracingConfig } from '@coreModule/services/racing/config/horseracing.config';
import { GreyhoundService } from '@coreModule/services/racing/greyhound/greyhound.service';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';

import { RacingYourCallService } from '@coreModule/services/racing/racingYourCall/racing-your-call.service';
import { NextRacesService } from '@coreModule/services/racing/nextRaces/next-races.service';
import { DailyRacingService } from '@coreModule/services/racing/dailyRacing/daily-racing.service';
import { TimeFormService } from '@coreModule/services/racing/timeForm/time-form.service';
import { TimeFormApiService } from '@coreModule/services/racing/timeForm/time-form-api.service';

import { GamingService } from '@coreModule/services/sport/gaming.service';
import { RacingService } from '@coreModule/services/sport/racing.service';
import { SportService } from '@coreModule/services/sport/sport.service';
import { DigitalSportBetsService } from '@coreModule/services/digitalSportBets/digital-sport-bets.service';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { SportEventHelperService } from '@coreModule/services/sportEventHelper/sport-event-helper.service';
import { VisEventService } from '@coreModule/services/visEvent/vis-event.service';
import { BuildUtilityService } from '@coreModule/services/buildUtility/build-utility.service';
import { CommentsService } from '@coreModule/services/comments/comments.service';
import { SiteServerService } from '@coreModule/services/siteServer/site-server.service';
import { SiteServerRequestHelperService } from '@coreModule/services/siteServerRequestHelper/site-server-request-helper.service';
import { SiteServerUtilityService } from '@coreModule/services/siteServerUtility/site-server-utility.service';
import { moduleImportGuard } from '@coreModule/module-import.guard';
import { BetPlacementErrorTrackingService } from '@coreModule/services/betPlacementErrorTracking/bet-placement-error-tracking';
import { BetslipSelectionsDataService } from '@coreModule/services/betslipSelectionsData/betslip-selections-data';
import { BetslipTabsService } from '@coreModule/services/betslipTabs/betslip-tabs.service';
import { brandConfig, brandConfigToken } from '@coreModule/services/brand/brand.config';
import { CasinoLinkService } from '@coreModule/services/casinoLink/casino-link.service';
import { CmsToolsService } from '@coreModule/services/cms/cms.tools';
import { SubscriptionsManagerService } from '@coreModule/services/subscriptionsManager/subscriptions-manager.service';
import { DeviceService } from '@coreModule/services/device/device.service';
import { DialogService } from '@coreModule/services/dialogService/dialog.service';
import { ExistNewUserService } from '@core/services/existNewUser/exist-new-user.service';
import { FiltersService } from '@coreModule/services/filters/filters.service';
import { FracToDecService } from '@coreModule/services/fracToDec/frac-to-dec.service';
import { GtmService } from '@coreModule/services/gtm/gtm.service';
import { GtmTrackingService } from '@coreModule/services/gtmTracking/gtm-tracking.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { InsomniaService } from '@coreModule/services/insomnia/insomnia.service';
import { PrivateMarketsService } from '@coreModule/services/privateMarkets/private-markets.service';
import { LiveServConnectionService } from '@coreModule/services/liveServ/live-serv-connection.service';
import { LiveUpdatesWSService } from '@coreModule/services/liveUpdatesWS/liveUpdatesWS.service';
import { LiveServIframeService } from '@coreModule/services/liveServ/live-serv-iframe.service';
import { WsConnectorService } from '@coreModule/services/wsConnector/ws-connector.service';
import { RemoteBetslipService } from '@coreModule/services/remoteBetslip/remote-betslip.service';
import { LpAvailabilityService } from '@coreModule/services/lpAvailability/lp-availability.service';
import { ModuleExtensionsStorageService } from '@coreModule/services/moduleExtensionsStorage/module-extensions-storage.service';
import { NativeBridgeService } from '@coreModule/services/nativeBridge/native-bridge.service';
import { UpdateEventService } from '@coreModule/services/updateEvent/update-event.service';
import { WsUpdateEventService } from '@coreModule/services/wsUpdateEvent/ws-update-event.service';
import { LStoSSDataStructureConverterService } from '@coreModule/services/lStoSSDataConverter/ls-ss-data-converter.service';
import { CacheEventsService } from '@coreModule/services/cacheEvents/cache-events.service';
import { RaceOutcomeDetailsService } from '@coreModule/services/raceOutcomeDetails/race-outcome-details.service';
import { ReloadService } from '@coreModule/services/reload/reload.service';
import { ResolveService } from '@coreModule/services/resolve/resolve.service';
import { ServingService } from '@coreModule/services/serving/serving.service';
import { ModuleRibbonService } from '@coreModule/services/moduleRibbon/module-ribbon.service';
import { SessionStorageService } from '@coreModule/services/storage/session-storage.service';
import { TempStorageService } from '@coreModule/services/storage/temp-storage.service';
import { SubscribersRouteService } from '@coreModule/services/subscribersRoute/subscribers-route.service';
import { TimeService } from '@coreModule/services/time/time.service';
import { TimeSyncService } from '@coreModule/services/timeSync/time-sync.service';
import { UserService } from '@core/services/user/user.service';
import { CashOutLabelService } from '@coreModule/services/cashOutLabel/cash-out-label.service';
import { CoreToolsService } from '@coreModule/services/coreTools/core-tools.service';
import { RoutingHelperService } from '@coreModule/services/routingHelper/routing-helper.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { ChannelService } from '@coreModule/services/liveServ/channel.service';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';
import { IteratorService } from '@coreModule/services/iterator/iterator.service';
import { httpInterceptorProviders } from '@coreModule/httpInterceptors';
import { MaintenanceService } from '@coreModule/services/maintenance/maintenance.service';
import { VisDataHandlerService } from '@coreModule/services/visDataHandler/vis-data-handler.service';
import { UkToteLiveUpdatesService } from '@coreModule/services/ukTote/uktote-live-update.service';
import { UkToteEventsLinkingService } from '@coreModule/services/ukTote/uktote-events-linking.service';
import { AfterLoginNotificationsService } from '@coreModule/services/afterLoginNotifications/after-login-notifications.service';
import { BackButtonService } from '@coreModule/services/backButton/back-button.service';
import { ClientUserAgentService } from '@coreModule/services/clientUserAgent/client-user-agent.service';
import { CurrencyCalculatorService } from '@coreModule/services/currencyCalculatorService/currency-calculator.service';
import { ExtraPlaceService } from '@coreModule/services/racing/extraPlace/extra-place.service';
import { GermanSupportService } from '@coreModule/services/germanSupport/german-support.service';
// Vanilla overrides
import { AuthModule } from '@authModule/auth.module';
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
    SbModule,
    BmaModule,
    FavouritesModule
  ],

  // define app level services/providers
  providers: [
    DynamicLoaderService,
    DeferredLoaderService,
    DynamicComponentsService,
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
    LiveServIframeService,
    LiveServConnectionService,
    LiveUpdatesWSService,
    VisEventService,
    VisDataHandlerService,
    SubscribersRouteService,
    RoutingHelperService,
    NavigationService,
    DomToolsService,
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
    BackButtonService,
    ClientUserAgentService,
    CurrencyCalculatorService,
    RacingYourCallService,
    DailyRacingService,
    NextRacesService,
    HorseracingService,
    GreyhoundService,
    GermanSupportService,
    TimeFormService,
    TimeFormApiService,
    ExtraPlaceService,
    BonusSuppressionService,
    InitNetworkIndicatorService,
    { provide: 'HORSERACING_CONFIG', useValue: horseracingConfig },
    { provide: 'GREYHOUND_CONFIG', useValue: greyhoundConfig },
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
