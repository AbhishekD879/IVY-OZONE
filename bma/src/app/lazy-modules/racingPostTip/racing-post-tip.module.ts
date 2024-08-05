import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { RacingPostTipRoutingModule } from '@lazy-modules/racingPostTip/racing-post-tip-routing.module';
import { RacingPostTipComponent } from '@lazy-modules/racingPostTip/components/racingpostTip/racing-post-tip.component';
import { RacingPostTipService } from '@lazy-modules/racingPostTip/service/racing-post-tip.service';

@NgModule({
  imports: [
    SharedModule,
    RacingPostTipRoutingModule
  ],
  declarations: [
    RacingPostTipComponent
  ],
  providers: [RacingPostTipService],
  exports: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class RacingPostTipModule {
  static entry = RacingPostTipComponent;
}
