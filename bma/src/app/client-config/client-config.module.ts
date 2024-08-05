import { NgModule, ModuleWithProviders } from '@angular/core';
import { ClientConfigService } from '@frontend/vanilla/core';

import { CasinoGamesClientConfig } from './bma-casino-games-config';
import { UserInterfaceClientConfig } from './bma-user-interface-config';
import { HtmlInjectionConfig } from './bma-html-injection-config';
import { TrackingConfig } from './bma-tracking-config';

@NgModule()
export class CoralSportsClientConfigModule {
  static forRoot(): ModuleWithProviders<CoralSportsClientConfigModule> {
    return {
      ngModule: CoralSportsClientConfigModule,
      providers: [
        { provide: UserInterfaceClientConfig, deps: [ClientConfigService], useFactory: userInterfaceConfigFactory },
        { provide: CasinoGamesClientConfig, deps: [ClientConfigService], useFactory: miniGamesConfigFactory },
        { provide: HtmlInjectionConfig, deps: [ClientConfigService], useFactory: htmlInjectionConfigFactory },
        { provide: TrackingConfig, deps: [ClientConfigService], useFactory: trackingConfigFactory }
      ]
    };
  }
}

export function userInterfaceConfigFactory(clientConfigService: ClientConfigService) {
  return clientConfigService.get(UserInterfaceClientConfig);
}

export function miniGamesConfigFactory(clientConfigService: ClientConfigService) {
  return clientConfigService.get(CasinoGamesClientConfig);
}

export function htmlInjectionConfigFactory(clientConfigService: ClientConfigService) {
  return clientConfigService.get(HtmlInjectionConfig);
}

export function trackingConfigFactory(clientConfigService: ClientConfigService) {
  return clientConfigService.get(TrackingConfig);
}
