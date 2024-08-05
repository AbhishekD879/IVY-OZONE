import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { SharedModule } from '@sharedModule/shared.module';
import { QuickbetModule } from '@quickbetModule/quickbet.module';
import { SbBetSummaryComponent } from '@app/quickbet-stream-bet/components/betSummary/sb-bet-summary.component';
import { SbDigitKeyboardComponent } from '@app/quickbet-stream-bet/components/digitKeyboard/sb-digit-keyboard.component';
import { SbQuickbetComponent } from '@app/quickbet-stream-bet/components/quickbet/sb-quickbet.component';
import { SbQuickbetInfoPanelComponent } from '@app/quickbet-stream-bet/components/quickbetInfoPanel/sb-quickbet-info-panel.component';
import { SbQuickbetPanelComponent } from '@app/quickbet-stream-bet/components/quickbetPanel/sb-quickbet-panel.component';
import { SbQuickbetPanelWrapperComponent } from '@app/quickbet-stream-bet/components/quickbetPanelWrapper/sb-quickbet-panel-wrapper.component';
import { SbQuickbetReceiptComponent } from '@app/quickbet-stream-bet/components/quickbetReceipt/sb-quickbet-receipt.component';
import { SbQuickbetSelectionComponent } from '@app/quickbet-stream-bet/components/quickbetSelection/sb-quickbet-selection.component';

@NgModule({
  imports: [
    SharedModule,
    FormsModule,
    QuickbetModule
  ],
  providers: [
  ],
  declarations: [
    SbQuickbetPanelWrapperComponent,
    SbQuickbetPanelComponent,
    SbQuickbetComponent,
    SbQuickbetSelectionComponent,
    SbDigitKeyboardComponent,
    SbBetSummaryComponent,
    SbQuickbetReceiptComponent,
    SbQuickbetInfoPanelComponent
  ],
  exports: [],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class StreamBetQuickbetModule {
  static entry = SbQuickbetPanelWrapperComponent;

  // constructor(quickbetRunService: QuickbetRunService) {
  //   quickbetRunService.init();
  // }
}
