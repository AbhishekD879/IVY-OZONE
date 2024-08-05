import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { UkToteCheckBoxMatrixComponent } from '@app/ukTote/components/ukToteCheckBoxMatrix/uk-tote-check-box-matrix.component';
import { UkToteSelectionOverwiewComponent } from '@app/ukTote/components/ukToteSelectionOverwiew/uk-tote-selection-overwiew.component';
import { UkToteLegComponent } from '@uktote/components/ukToteLeg/uk-tote-leg.component';
import { UkToteEventComponent } from '@uktote/components/ukToteEvent/uk-tote-event.component';
import {
  MultipleEventsToteBetComponent
} from '@uktote/components/multipleEventsToteBet/multiple-events-tote-bet.component';
import { PoolSizeComponent } from '@uktote/components/poolSize/pool-size.component';

// Overridden Component
import {
  LadbrokesDesktopBetBuilderComponent
} from '@ladbrokesDesktop/ukTote/components/betBuilder/bet-builder.component';

@NgModule({
  declarations: [
    UkToteEventComponent,
    MultipleEventsToteBetComponent,
    UkToteCheckBoxMatrixComponent,
    UkToteLegComponent,
    UkToteSelectionOverwiewComponent,
    PoolSizeComponent,
    LadbrokesDesktopBetBuilderComponent
  ],
  imports: [ SharedModule ],
  exports: [
    UkToteEventComponent,
    MultipleEventsToteBetComponent,
    UkToteCheckBoxMatrixComponent,
    UkToteLegComponent,
    UkToteSelectionOverwiewComponent,
    LadbrokesDesktopBetBuilderComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class UkToteModule {
  static entry = UkToteEventComponent;
  constructor(){}
}
