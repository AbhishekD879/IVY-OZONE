import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { OnBoardingFirstBetComponent } from '@lazy-modules/onBoardingTutorial/firstBetPlacement/components/first-bet-placement.component';
import { FirstBetEntryPointComponent } from './components/first-bet-entry-point/first-bet-entry-point.component';

@NgModule({
  imports: [
    SharedModule
  ],
  providers: [],
  exports: [FirstBetEntryPointComponent],
  declarations: [
    FirstBetEntryPointComponent,
    OnBoardingFirstBetComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class OnBoardingFirstBetModule {
  static entry = { FirstBetEntryPointComponent, OnBoardingFirstBetComponent };
}
