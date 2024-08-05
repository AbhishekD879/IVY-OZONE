import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { SharedModule } from '@sharedModule/shared.module';

import { BetslipRoutingModule } from '@betslipModule/betslip-routing.module';
import { InitBetslipService } from '@betslipModule/services/initBetslip/init-betslip.service';

import { BetslipDigitKeyboardDirective } from '@betslipModule/directives/betslip-digit-keyboard.directive';
import { BetslipLimitationDialogComponent } from '@betslipModule/components/betslipLimitationDialog/betslip-limitation-dialog.component';
import { BsNotificationComponent } from '@betslipModule/components/bsNotification/bs-notification.component';
import { MaxStakeDialogComponent } from '@betslipModule/components/maxStakeDialog/max-stake-dialog.component';
import {
  OverAskNotificationDialogComponent
} from '@betslipModule/components/overaskNotificationDialog/over-ask-notification-dialog.component';
import {
  OveraskOfferNotificationComponent
} from '@betslipModule/components/overaskOfferNotification/over-ask-offer-notification.component';
import { ToteBetReceiptComponent } from '@betslipModule/components/toteBetReceipt/tote-bet-receipt.component';
import { BetslipReceiptComponent } from '@betslipModule/components/betslipReceipt/betslip-receipt.component';
import { ToteBetReceiptItemComponent } from '@betslipModule/components/toteBetReceiptItem/tote-bet-receipt-item.component';
import { VoucherComponent } from '@betslipModule/components/voucher/voucher.component';
import { SlideOutBetslipComponent } from '@betslipModule/components/slideOutBetslip/slide-out-betslip.component';
import { BetslipContainerComponent } from '@betslipModule/components/betslipContainer/betslip-container.component';
import { IncorrectPatternComponent } from '@betslipModule/components/incorrectPattern/incorrect-pattern.component';
import { AddToBetslipComponent } from '@betslipModule/components/addToBetslip/add-to-betslip.component';
import { BetslipComponent } from '@betslipModule/components/betslip/betslip.component';
import { BetslipTotalWrapperComponent } from '@betslipModule/components/betslipTotalWrapper/betslip-total-wrapper.component';
import { BetslipSubheaderComponent } from '@betslipModule/components/betslipSubheader/betslip-subheader.component';
import { EmptyBetslipComponent } from '@betslipModule/components/emptyBetslip/empty-betslip.component';
import { BetslipSinglesReceiptComponent } from '@betslipModule/components/betslipSinglesReceipt/betslip-singles-receipt.component';
import { BetslipMultiplesReceiptComponent } from '@betslipModule/components/betslipMultiplesReceipt/betslip-multiples-receipt.component';
import { BetslipReceiptSubheaderComponent } from '@betslipModule/components/betslipReceiptSubheader/betslip-receipt-subheader.component';
import { BetslipFctcListComponent } from '@betslipModule/components/betslipFctcList/betslip-fctc-list.component';
import { SelectionInfoDialogComponent } from '@betslipModule/components/selectionInfoDialog/selection-info-dialog.component';
import { BetslipOfferedDataComponent } from '@betslipModule/components/betslipOfferedData/betslip-offered-data.component';
import { OveraskHoldingDrawerComponent } from '@betslipModule/components/overask-holding-drawer/overask-holding-drawer.component';
import { BetslipMultipleBetPartsComponent } from '@betslip/components/betslipMultipleBetPart/betslip-multiple-bet-parts.component';
import { DeclinedBetComponent } from '@betslip/components/declinedBet/declined-bet.component';
import { QuickDepositService } from '@betslipModule/services/quickDeposit/quick-deposit.service';

import { ReceiptHeaderModule } from '@lazy-modules/receiptHeader/receipt-header.module';
import { AsyncScriptLoaderService } from '../core/services/asyncScriptLoader/async-script-loader.service';
import { LottoBetslipModule } from '@lazy-modules/lottoBetSlip/lotto-betslip.module';

@NgModule({
  declarations: [
    BetslipDigitKeyboardDirective,
    BetslipLimitationDialogComponent,
    BsNotificationComponent,
    MaxStakeDialogComponent,
    OverAskNotificationDialogComponent,
    OveraskOfferNotificationComponent,
    SelectionInfoDialogComponent,
    ToteBetReceiptComponent,
    VoucherComponent,
    BetslipContainerComponent,
    SlideOutBetslipComponent,
    BetslipReceiptComponent,
    ToteBetReceiptItemComponent,
    BetslipComponent,
    AddToBetslipComponent,
    IncorrectPatternComponent,
    BetslipTotalWrapperComponent,
    BetslipSubheaderComponent,
    EmptyBetslipComponent,
    BetslipFctcListComponent,
    BetslipReceiptSubheaderComponent,
    BetslipSinglesReceiptComponent,
    BetslipMultiplesReceiptComponent,
    BetslipOfferedDataComponent,
    OveraskHoldingDrawerComponent,
    BetslipMultipleBetPartsComponent,
    DeclinedBetComponent
  ],
  exports: [],
  imports: [
    SharedModule,
    FormsModule,
    BetslipRoutingModule,
    ReceiptHeaderModule,
    LottoBetslipModule
  ],
  providers: [
    QuickDepositService
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class BetslipModule {
  static entry = {
    BetslipContainerComponent,
    SlideOutBetslipComponent
  };

  constructor(initBetslip: InitBetslipService,private asls: AsyncScriptLoaderService) {
    initBetslip.init();
    this.asls.loadCssFile('assets-bet-history.css',true, true).subscribe();
    this.asls.loadCssFile('assets-betslip.css', true, true).subscribe();
  }
}
