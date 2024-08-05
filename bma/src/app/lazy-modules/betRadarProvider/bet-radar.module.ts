import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { BetRadarProviderComponent } from '@lazy-modules/betRadarProvider/components/bet-radar-provider.component';

@NgModule({
  imports: [
    SharedModule
  ],
  providers: [],
  exports: [],
  declarations: [
    BetRadarProviderComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class BetRadarCoralModule {
  static entry = BetRadarProviderComponent;
}
