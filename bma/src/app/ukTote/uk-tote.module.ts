import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { UkToteEventComponent } from '@uktote/components/ukToteEvent/uk-tote-event.component';
import { UkToteCheckBoxMatrixComponent } from '@uktote/components/ukToteCheckBoxMatrix/uk-tote-check-box-matrix.component';
import { UkToteSelectionOverwiewComponent } from '@uktote/components/ukToteSelectionOverwiew/uk-tote-selection-overwiew.component';
import { UkToteLegComponent } from '@uktote/components/ukToteLeg/uk-tote-leg.component';
import { MultipleEventsToteBetComponent } from '@uktote/components/multipleEventsToteBet/multiple-events-tote-bet.component';
import { BetBuilderComponent } from '@uktote/components/betBuilder/bet-builder.component';
import { PoolSizeComponent } from '@uktote/components/poolSize/pool-size.component';
@NgModule({
  declarations: [
    UkToteCheckBoxMatrixComponent,
    MultipleEventsToteBetComponent,
    UkToteLegComponent,
    UkToteSelectionOverwiewComponent,
    UkToteEventComponent,
    BetBuilderComponent,
    PoolSizeComponent
  ],
  imports: [ SharedModule ],
  exports: [
    UkToteCheckBoxMatrixComponent,
    UkToteLegComponent,
    UkToteSelectionOverwiewComponent,
    UkToteEventComponent,
    MultipleEventsToteBetComponent,
    BetBuilderComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class UkToteModule {
  static entry = UkToteEventComponent;
  constructor(){}
}
