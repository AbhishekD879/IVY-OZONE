import { CUSTOM_ELEMENTS_SCHEMA, NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CurrencyPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@sharedModule/shared.module';
import { QuickbetRunService } from '@app/quickbet/services/quickbetRunService/quickbet-run.service';
import { LadbrokesDeskBetSummaryComponent } from '@ladbrokesDesktop/quickbet/components/betSummary/bet-summary.component';
import { LadbrokesDeskQuickbetReceiptComponent } from '@ladbrokesDesktop/quickbet/components/quickbetReceipt/quickbet-receipt.component';
import { LadbrokesDeskQuickbetPanelComponent } from '@ladbrokesDesktop/quickbet/components/quickbetPanel/quickbet-panel.component';
import { LadbrokesDeskQuickbetSelectionComponent } from '@ladbrokesDesktop/quickbet/components/quickbetSelection/quickbet-selection.component';
import { LadbrokesDeskQuickStakeComponent } from '@ladbrokesDesktop/quickbet/components/quickStake/quick-stake.component';
import { LadbrokesDeskQuickbetInfoPanelComponent } from '@ladbrokesDesktop/quickbet/components/quickbetInfoPanel/quickbet-info-panel.component';
import { QuickbetYourcallWrapperComponent } from '@app/quickbet/components/quickbetYourcallWrapper/quickbet-yourcall-wrapper.component';
import { FiveASideEntryConfirmationService } from '@app/fiveASideShowDown/services/fiveAside-Entry-confirmation.service';
import { LadbrokesDeskQuickbetComponent } from '@ladbrokesDesktop/quickbet/components/quickbet/quickbet.component';

@NgModule({
  imports: [
    SharedModule,
    FormsModule,
    CommonModule
  ],
  providers: [
    FiveASideEntryConfirmationService,
    CurrencyPipe
  ],
  declarations: [
    LadbrokesDeskQuickbetComponent,
    LadbrokesDeskBetSummaryComponent,
    LadbrokesDeskQuickbetSelectionComponent,
    LadbrokesDeskQuickbetReceiptComponent,
    LadbrokesDeskQuickStakeComponent,
    LadbrokesDeskQuickbetInfoPanelComponent,
    LadbrokesDeskQuickbetPanelComponent,
    QuickbetYourcallWrapperComponent
  ],
  exports: [],
  schemas: [ CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA ]
})
export class QuickbetModule{
  static entry = {
    LadbrokesDeskQuickbetComponent,
    LadbrokesDeskQuickbetPanelComponent,
    QuickbetYourcallWrapperComponent,
    LadbrokesDeskQuickStakeComponent
  };

  constructor(quickbetRunService: QuickbetRunService) {
    quickbetRunService.init();
  }
}
