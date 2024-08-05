import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { RacingPostTipService } from '@lazy-modules/racingPostTip/service/racing-post-tip.service';
import { NextRacesToBetslipComponent } from '@ladbrokesMobile/lazy-modules/nextRacesToBetslip/components/nextraces-to-betslip.component';
import { NextRacesToBetslipRoutingModule } from '@ladbrokesMobile/lazy-modules/nextRacesToBetslip/nextraces-to-betslip-routing.module';


@NgModule({
  imports: [
    SharedModule,
    NextRacesToBetslipRoutingModule
  ],
  declarations: [
    NextRacesToBetslipComponent
  ],
  providers: [RacingPostTipService],
  exports: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class NextRacesToBetslipModule {
  static entry = NextRacesToBetslipComponent;
}
