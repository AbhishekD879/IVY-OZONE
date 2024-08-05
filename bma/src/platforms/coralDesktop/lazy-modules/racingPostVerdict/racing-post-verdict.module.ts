import { DesktopRacingPostVerdictLabelComponent } from './racing-post-verdict-label.component';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { DesktopRacingPostVerdictComponent } from '@coralDesktop/lazy-modules/racingPostVerdict/racing-post-verdict.component';

@NgModule({
  imports: [
    SharedModule
  ],
  declarations: [
    DesktopRacingPostVerdictLabelComponent,
    DesktopRacingPostVerdictComponent,
  ],
  providers: [],
  exports: [
    DesktopRacingPostVerdictComponent,
    DesktopRacingPostVerdictLabelComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RacingPostVerdictModule {
  static entry = {DesktopRacingPostVerdictComponent, DesktopRacingPostVerdictLabelComponent};
}
