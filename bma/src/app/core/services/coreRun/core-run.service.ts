import { Injectable, Injector } from '@angular/core';

import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { BetPlacementErrorTrackingService } from '@core/services/betPlacementErrorTracking/bet-placement-error-tracking';
import { BetslipSelectionsDataService } from '@core/services/betslipSelectionsData/betslip-selections-data';
import { CommandService } from '@core/services/communication/command/command.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { SubscribersRouteService } from '@core/services/subscribersRoute/subscribers-route.service';
import { DeferredLoaderService } from '@core/services/deferredLoader/deferred-loader.service';

@Injectable()
export class CoreRunService {

  constructor(
      private commandService: CommandService,
      private injector: Injector,
      private homePageLoaderService: DeferredLoaderService
  ) { }

  init() {
    // Register lazy load handler
    this.commandService.register(this.commandService.API.LAZY_LOAD, (modulePath: string) => {
      const isLazyInd = modulePath.indexOf(':');

      if (isLazyInd < 0) {
        return Promise.resolve();
      }

      return this.dynamicComponentLoader.loadModule(modulePath.substring(0, isLazyInd), this.injector);
    });

    this.commandService.register(this.commandService.API.BESTLIP_ERROR_TRACKING,
() => this.betPlacementErrorTrackingService.sendBetSlip);
    this.nativeBridgeService.init();

    this.betslipSelectionsDataService.subscribe();
    // Starting Google tag manager
    this.gtmService.init();

    // Starting Subscriptions Service for LiveServe Updates
    this.subscribersRouteService.init();

    // start lazy loading for home
    this.homePageLoaderService.init();
  }

  get dynamicComponentLoader(): DynamicLoaderService {
    return this.injector.get(DynamicLoaderService);
  }
  set dynamicComponentLoader(value:DynamicLoaderService){}
  get nativeBridgeService(): NativeBridgeService {
    return this.injector.get(NativeBridgeService);
  }
  set nativeBridgeService(value:NativeBridgeService){}
  get betPlacementErrorTrackingService(): BetPlacementErrorTrackingService {
    return this.injector.get(BetPlacementErrorTrackingService);
  }
  set betPlacementErrorTrackingService(value:BetPlacementErrorTrackingService){}
  get betslipSelectionsDataService(): BetslipSelectionsDataService {
    return this.injector.get(BetslipSelectionsDataService);
  }
  set betslipSelectionsDataService(value:BetslipSelectionsDataService){}
  get gtmService(): GtmService {
    return this.injector.get(GtmService);
  }
  set gtmService(value:GtmService){}
  get subscribersRouteService(): SubscribersRouteService {
    return this.injector.get(SubscribersRouteService);
  }
  set subscribersRouteService(value:SubscribersRouteService){}
  get asyncScriptLoaderService(): AsyncScriptLoaderService {
    return this.injector.get(AsyncScriptLoaderService);
  }
  set asyncScriptLoaderService(value:AsyncScriptLoaderService){}
}
