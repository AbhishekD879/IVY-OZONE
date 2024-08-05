import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { LadbrokesBetRadarProviderComponent } from '@ladbrokesMobile/lazy-modules/betRadarProvider/components/bet-radar-provider.component';
import { SharedModule } from '@sharedModule/shared.module';
import { DesktopModule } from '@desktop/desktop.module';


@NgModule({
  imports: [
    SharedModule,
    DesktopModule
  ],
  providers: [],
  exports: [],
  declarations: [
    LadbrokesBetRadarProviderComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class BetRadarLadbrokesModule {
  static entry = LadbrokesBetRadarProviderComponent;
}
