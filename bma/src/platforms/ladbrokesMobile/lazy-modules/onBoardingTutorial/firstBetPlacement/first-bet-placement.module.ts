import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { LadbrokesOnBoardingFirstBetComponent } from '@ladbrokesMobile/lazy-modules/onBoardingTutorial/firstBetPlacement/components/first-bet-placement.component';
import { LadbrokesFirstBetEntryPointComponent } from '@ladbrokesMobile/lazy-modules/onBoardingTutorial/firstBetPlacement/components/first-bet-entry-point/first-bet-entry-point.component';

@NgModule({
  imports: [
    SharedModule
  ],
  providers: [],
  exports: [],
  declarations: [
    LadbrokesFirstBetEntryPointComponent,
    LadbrokesOnBoardingFirstBetComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class LadbrokesOnBoardingFirstBetModule {
  static entry = { LadbrokesFirstBetEntryPointComponent, LadbrokesOnBoardingFirstBetComponent };
}
