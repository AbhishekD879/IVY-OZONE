import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { NextRacesToBetslipRoutingModule } from './nextraces-to-betslip-routing.module';
import { NextRacesToBetslipComponent } from './components/nextraces-to-betslip.component';

@NgModule({
  imports: [
    SharedModule,
    NextRacesToBetslipRoutingModule
  ],
  declarations: [
    NextRacesToBetslipComponent
  ],
  providers: [],
  exports: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class NextRacesToBetslipModule {
  static entry = NextRacesToBetslipComponent;
}
