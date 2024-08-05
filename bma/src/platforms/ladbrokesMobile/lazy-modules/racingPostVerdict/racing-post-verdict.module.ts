import {
  LadbrokesRacingPostVerdictLabelComponent
} from './racing-post-verdict-label.component';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { LadbrokesRacingPostVerdictComponent } from '@ladbrokesMobile/lazy-modules/racingPostVerdict/racing-post-verdict.component';

@NgModule({
  imports: [
    SharedModule
  ],
  declarations: [
    LadbrokesRacingPostVerdictLabelComponent,
    LadbrokesRacingPostVerdictComponent,
  ],
  providers: [],
  exports: [
    LadbrokesRacingPostVerdictLabelComponent,
    LadbrokesRacingPostVerdictComponent,
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RacingPostVerdictModule {
  static entry = { LadbrokesRacingPostVerdictLabelComponent, LadbrokesRacingPostVerdictComponent };
}
