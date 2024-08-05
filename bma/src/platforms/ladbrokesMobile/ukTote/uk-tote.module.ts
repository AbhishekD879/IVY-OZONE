import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { UkToteEventComponent } from '@uktote/components/ukToteEvent/uk-tote-event.component';
import { UkToteCheckBoxMatrixComponent } from '@uktote/components/ukToteCheckBoxMatrix/uk-tote-check-box-matrix.component';
import { UkToteSelectionOverwiewComponent } from '@uktote/components/ukToteSelectionOverwiew/uk-tote-selection-overwiew.component';
import { UkToteLegComponent } from '@uktote/components/ukToteLeg/uk-tote-leg.component';
import { MultipleEventsToteBetComponent } from '@uktote/components/multipleEventsToteBet/multiple-events-tote-bet.component';
import { PoolSizeComponent } from '@uktote/components/poolSize/pool-size.component';

// Overridden Component
import {
  LadbrokesMobileBetBuilderComponent
} from '@ladbrokesMobile/ukTote/components/betBuilder/bet-builder.component';

@NgModule({
  declarations: [
    UkToteCheckBoxMatrixComponent,
    MultipleEventsToteBetComponent,
    UkToteLegComponent,
    UkToteSelectionOverwiewComponent,
    UkToteEventComponent,
    PoolSizeComponent,
    LadbrokesMobileBetBuilderComponent
  ],
  imports: [ SharedModule ],
  exports: [
    UkToteCheckBoxMatrixComponent,
    UkToteLegComponent,
    UkToteSelectionOverwiewComponent,
    UkToteEventComponent,
    MultipleEventsToteBetComponent,
    LadbrokesMobileBetBuilderComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class UkToteModule {
  static entry = UkToteEventComponent;
  constructor(){}
}
