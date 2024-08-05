import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { RacingModule } from '@racingModule/racing.module';
import { SharedModule } from '@sharedModule/shared.module';
import { RacingFullResultsComponent } from './components/racingFullResults/racing-full-results.component';

@NgModule({
  imports: [
    SharedModule,
    RacingModule
  ],
  providers: [],
  exports: [RacingFullResultsComponent],
  declarations: [
    RacingFullResultsComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RacingFullResultsModule {
  static entry = RacingFullResultsComponent;
}
