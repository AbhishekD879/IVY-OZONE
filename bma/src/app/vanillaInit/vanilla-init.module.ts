import { Inject, NgModule } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { ApiServiceFactory, MenuCountersProvider, MenuCountersService, MENU_COUNTERS_PROVIDER } from '@frontend/vanilla/core';
import { VanillaApiService } from '@vanillaInitModule/services/vanillaApi/vanilla-api.service';
import { VanillaAuthService } from '@vanillaInitModule/services/vanillaAuth/vanilla-auth.service';
import {
  VanillaSmartBannerHandlerService
} from '@vanillaInitModule/services/vanillaSmartBannerHandler/vanilla-smart-banner-handler.service';
// eslint-disable-next-line
import {
  VanillaDynamicComponentLoaderService
} from '@vanillaInitModule/services/vanillaComponentDynamicLoader/vanilla-dynamic-component-loader.service';
import { NativeBridgeAdapter } from '@vanillaInitModule/services/NativeBridgeAdapter/nativebridge.adapter';
import { PortalNativeEventNotifier } from '@vanillaInitModule/services/PortalNativeEventNotifier/portal-nativeEvent-notifier';
import { NativeBridgeBootstrapperService } from '@vanillaInitModule/services/NativeBridgeBootstrapper/native-bridge-bootstrapper.service';
import { FreeBetsBadgeService } from '@app/vanillaInit/services/vanillaFreeBets/vanilla-freebets-badge.service';

export function apiServiceFactory(service: ApiServiceFactory) {
  return service.create(VanillaApiService, { product: 'coralsports', area: 'coralsports', forwardProductApiRequestHeader: true });
}

@NgModule({
  imports: [
    SharedModule
  ],
  providers: [
    NativeBridgeAdapter,
    PortalNativeEventNotifier,
    NativeBridgeBootstrapperService,
    { provide: MENU_COUNTERS_PROVIDER, useExisting: FreeBetsBadgeService, multi: true },
    { provide: VanillaApiService, deps: [ApiServiceFactory], useFactory: apiServiceFactory }
  ],
})
export class VanillaInitModule {
  constructor(
    private vanillaDynamicComponentLoaderService: VanillaDynamicComponentLoaderService,
    private vanillaAuthService: VanillaAuthService,
    private vanillaSmartBannerHandlerService: VanillaSmartBannerHandlerService,
    private menuCountersService: MenuCountersService,
    @Inject(MENU_COUNTERS_PROVIDER) private providers: MenuCountersProvider[]
  ) {
    this.vanillaAuthService.init();
    this.vanillaDynamicComponentLoaderService.init();
    this.vanillaSmartBannerHandlerService.init();
    this.menuCountersService.registerProviders(this.providers);
  }
}
