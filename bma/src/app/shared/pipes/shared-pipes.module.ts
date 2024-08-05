import { CommonModule } from '@angular/common';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { NumberNormalizerPipe } from '@shared/pipes/number-normalizer/number-normalizer.pipe';
import { SafePipe } from '@shared/pipes/safe/safe.pipe';
import { EventNamePipe } from '@shared/pipes/event-name/event-name.pipe';
import { OddsFormatPipe } from '@shared/pipes/odds-format/odds-format.pipe';
import { EventMorePipe } from '@shared/pipes/event-more/event-more.pipe';
import { CallBackPipe } from '@shared/pipes/call-back/call-back.pipe';
import { NameWithoutPipesPipe } from '@core/pipes/filters/name-without-pipes.pipe';
import { DateAgoPipe } from '@lazy-modules/timeline/pipes/dateAgo/date-ago.pipe';

@NgModule({
  imports: [
    CommonModule
  ],
  declarations: [
    NumberNormalizerPipe,
    EventNamePipe,
    SafePipe,
    OddsFormatPipe,
    EventMorePipe,
    CallBackPipe,
    NameWithoutPipesPipe,
    DateAgoPipe
  ],
  providers: [
    EventNamePipe,
    OddsFormatPipe
  ],
  exports: [
    NumberNormalizerPipe,
    SafePipe,
    EventNamePipe,
    OddsFormatPipe,
    EventMorePipe,
    CallBackPipe,
    NameWithoutPipesPipe,
    DateAgoPipe
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class SharedPipesModule {
}
