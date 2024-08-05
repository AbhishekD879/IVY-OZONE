import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CurrencyPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { SharedModule } from '@sharedModule/shared.module';
import { QuickbetRunService } from './services/quickbetRunService/quickbet-run.service';
import { BetSummaryComponent } from './components/betSummary/bet-summary.component';
import { QuickStakeComponent } from './components/quickStake/quick-stake.component';
import { QuickbetSelectionComponent } from './components/quickbetSelection/quickbet-selection.component';
import { QuickbetReceiptComponent } from './components/quickbetReceipt/quickbet-receipt.component';
import { QuickbetInfoPanelComponent } from './components/quickbetInfoPanel/quickbet-info-panel.component';
import { QuickbetPanelComponent } from './components/quickbetPanel/quickbet-panel.component';
import { QuickbetComponent } from '@app/quickbet/components/quickbet/quickbet.component';
import { QuickbetYourcallWrapperComponent } from '@app/quickbet/components/quickbetYourcallWrapper/quickbet-yourcall-wrapper.component';
import { FiveASideEntryConfirmationService } from '@app/fiveASideShowDown/services/fiveAside-Entry-confirmation.service';
import { QuickbetReceiptLdComponent } from '@app/quickbet/components/quickbetReceiptLuckyDip/quickbet-receipt-ld/quickbet-receipt-ld.component';

@NgModule({
  imports: [
    SharedModule,
    FormsModule
  ],
  providers: [
    CurrencyPipe,
    FiveASideEntryConfirmationService
  ],
  declarations: [
    BetSummaryComponent,
    QuickStakeComponent,
    QuickbetSelectionComponent,
    QuickbetReceiptComponent,
    QuickbetReceiptLdComponent,
    QuickbetInfoPanelComponent,
    QuickbetPanelComponent,
    QuickbetComponent,
    QuickbetYourcallWrapperComponent
  ],
  exports: [],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class QuickbetModule {
  static entry = {
    QuickbetComponent,
    QuickbetYourcallWrapperComponent,
    QuickStakeComponent,
    // QbVideoOverlayWrapper
  };

  constructor(quickbetRunService: QuickbetRunService) {
    quickbetRunService.init();
  }
}
