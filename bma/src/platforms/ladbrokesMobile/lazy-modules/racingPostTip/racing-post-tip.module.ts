import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
// eslint-disable-next-line max-len
import { LadbrokesRacingPostTipComponent } from '@ladbrokesMobile/lazy-modules/racingPostTip/components/racingPostTip/racing-post-tip.component';
import { SharedModule } from '@sharedModule/shared.module';
import { LadbrokesRacingTipRoutingModule } from '@ladbrokesMobile/lazy-modules/racingPostTip/racing-post-routing.module';
import { RacingPostTipService } from '@app/lazy-modules/racingPostTip/service/racing-post-tip.service';

@NgModule({
  imports: [
    SharedModule,
    LadbrokesRacingTipRoutingModule
  ],
  declarations: [
    LadbrokesRacingPostTipComponent
  ],
  providers: [RacingPostTipService],
  exports: [
    LadbrokesRacingPostTipComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RacingPostTipModule {
  static entry = LadbrokesRacingPostTipComponent;
}
