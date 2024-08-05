import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CurrencyPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { SharedModule } from '@sharedModule/shared.module';
import { QuickbetRunService } from '@app/quickbet/services/quickbetRunService/quickbet-run.service';
import { LadbrokesBetSummaryComponent } from '@ladbrokesMobile/quickbet/components/betSummary/bet-summary.component';
import { LadbrokesQuickbetReceiptComponent } from '@ladbrokesMobile/quickbet/components/quickbetReceipt/quickbet-receipt.component';
import { LadbrokesQuickbetPanelComponent } from '@ladbrokesMobile/quickbet/components/quickbetPanel/quickbet-panel.component';
import { LadbrokesQuickbetSelectionComponent } from '@ladbrokesMobile/quickbet/components/quickbetSelection/quickbet-selection.component';
import { LadbrokesQuickStakeComponent } from '@ladbrokesMobile/quickbet/components/quickStake/quick-stake.component';
import { LadbrokesQuickbetInfoPanelComponent } from '@ladbrokesMobile/quickbet/components/quickbetInfoPanel/quickbet-info-panel.component';
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
    FiveASideEntryConfirmationService,
    CurrencyPipe
  ],
  declarations: [
    LadbrokesBetSummaryComponent,
    LadbrokesQuickbetSelectionComponent,
    LadbrokesQuickbetReceiptComponent,
    LadbrokesQuickStakeComponent,
    LadbrokesQuickbetInfoPanelComponent,
    LadbrokesQuickbetPanelComponent,
    QuickbetComponent,
    QuickbetReceiptLdComponent,
    QuickbetYourcallWrapperComponent
  ],
  exports: [],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class QuickbetModule {
  static entry = {
    QuickbetComponent,
    LadbrokesQuickbetPanelComponent,
    QuickbetYourcallWrapperComponent,
    LadbrokesQuickStakeComponent
  };

  constructor(quickbetRunService: QuickbetRunService) {
    quickbetRunService.init();
  }
}
