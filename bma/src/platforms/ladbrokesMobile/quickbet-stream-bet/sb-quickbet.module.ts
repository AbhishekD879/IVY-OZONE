import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { SharedModule } from '@sharedModule/shared.module';
import { QuickbetModule } from '@quickbetModule/quickbet.module';

import { SbQuickbetPanelWrapperComponent } from '@app/quickbet-stream-bet/components/quickbetPanelWrapper/sb-quickbet-panel-wrapper.component';
import { SbDigitKeyboardComponent } from '@app/quickbet-stream-bet/components/digitKeyboard/sb-digit-keyboard.component';
import { SbQuickbetComponent } from '@app/quickbet-stream-bet/components/quickbet/sb-quickbet.component';
import { SbBetSummaryComponent } from '@ladbrokesMobile/quickbet-stream-bet/components/betSummary/sb-bet-summary.component';
import { SbQuickbetInfoPanelComponent } from '@ladbrokesMobile/quickbet-stream-bet/components/quickbetInfoPanel/sb-quickbet-info-panel.component';
import { SbQuickbetPanelComponent } from '@ladbrokesMobile/quickbet-stream-bet/components/quickbetPanel/sb-quickbet-panel.component';
import { SbQuickbetReceiptComponent } from '@ladbrokesMobile/quickbet-stream-bet/components/quickbetReceipt/sb-quickbet-receipt.component';
import { SbQuickbetSelectionComponent } from '@ladbrokesMobile/quickbet-stream-bet/components/quickbetSelection/sb-quickbet-selection.component';

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
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class StreamBetQuickbetModule {
  static entry = {
    SbQuickbetPanelWrapperComponent
  };

  // constructor(quickbetRunService: QuickbetRunService) {
  //   quickbetRunService.init();
  // }
}
