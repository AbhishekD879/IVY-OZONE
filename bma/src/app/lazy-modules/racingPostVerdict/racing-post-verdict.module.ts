import { RacingPostVerdictLabelComponent } from './racing-post-verdict-label.component';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { RacingPostVerdictComponent } from '@app/lazy-modules/racingPostVerdict/racing-post-verdict.component';

@NgModule({
  imports: [
    SharedModule
  ],
  declarations: [
    RacingPostVerdictLabelComponent,
    RacingPostVerdictComponent,
  ],
  providers: [],
  exports: [
    RacingPostVerdictLabelComponent,
    RacingPostVerdictComponent,
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RacingPostVerdictModule {
  static entry = { RacingPostVerdictLabelComponent, RacingPostVerdictComponent };
}
