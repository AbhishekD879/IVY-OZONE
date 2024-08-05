import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { SharedModule } from '@sharedModule/shared.module';

import { BetslipRoutingModule } from '@app/betslip/betslip-routing.module';
import { InitBetslipService } from '@app/betslip/services/initBetslip/init-betslip.service';

import { BetslipDigitKeyboardDirective } from '@app/betslip/directives/betslip-digit-keyboard.directive';
import { BetslipLimitationDialogComponent } from '@betslipModule/components/betslipLimitationDialog/betslip-limitation-dialog.component';
import { BsNotificationComponent } from '@app/betslip/components/bsNotification/bs-notification.component';
import { MaxStakeDialogComponent } from '@betslipModule/components/maxStakeDialog/max-stake-dialog.component';
import { OverAskNotificationDialogComponent } from '@betslip/components/overaskNotificationDialog/over-ask-notification-dialog.component';
import { OveraskOfferNotificationComponent } from '@betslip/components/overaskOfferNotification/over-ask-offer-notification.component';
import { VoucherComponent } from '@app/betslip/components/voucher/voucher.component';
import { BetslipContainerComponent } from '@app/betslip/components/betslipContainer/betslip-container.component';
import { IncorrectPatternComponent } from '@app/betslip/components/incorrectPattern/incorrect-pattern.component';
import { AddToBetslipComponent } from '@app/betslip/components/addToBetslip/add-to-betslip.component';
import { BetslipFctcListComponent } from '@app/betslip/components/betslipFctcList/betslip-fctc-list.component';
import {
  LadbrokesBetslipSinglesReceiptComponent
} from '@ladbrokesMobile/betslip/components/betslipSinglesReceipt/betslip-singles-receipt.component';
import {
  LadbrokesBetslipMultiplesReceiptComponent
} from '@ladbrokesMobile/betslip/components/betslipMultiplesReceipt/betslip-multiples-receipt.component';

import { SlideOutBetslipComponent } from '@ladbrokesMobile/betslip/components/slideOutBetslip/slide-out-betslip.component';
import { LadbrokesBetslipComponent } from '@ladbrokesMobile/betslip/components/betslip/betslip.component';
import { LadbrokesBetslipReceiptComponent } from '@ladbrokesMobile/betslip/components/betslipReceipt/betslip-receipt.component';
import {
  BetslipReceiptSubheaderComponent
} from '@ladbrokesMobile/betslip/components/betslipReceiptSubheader/betslip-receipt-subheader.component';
import {
  LadbrokesBetslipTotalWrapperComponent
} from '@ladbrokesMobile/betslip/components/betslipTotalWrapper/betslip-total-wrapper.component';
import {
  LadbrokesBetslipSubheaderComponent
} from '@ladbrokesMobile/betslip/components/betslipSubheader/betslip-subheader.component';
import {
  LadbrokesEmptyBetslipComponent
} from '@ladbrokesMobile/betslip/components/emptyBetslip/empty-betslip.component';
import {
  LadbrokesSelectionInfoDialogComponent
} from '@ladbrokesMobile/betslip/components/selectionInfoDialog/selection-info-dialog.component';
import {
  LadbrokesToteBetReceiptItemComponent
} from '@ladbrokesMobile/betslip/components/toteBetReceiptItem/tote-bet-receipt-item.component';
import { OveraskHoldingDrawerComponent } from '@betslip/components/overask-holding-drawer/overask-holding-drawer.component';
import { BetslipOfferedDataComponent } from './components/betslip-offered-data/betslip-offered-data.component';
import { BetslipMultipleBetPartsComponent } from '@betslip/components/betslipMultipleBetPart/betslip-multiple-bet-parts.component';
import {
  AccaInsuranceSubtitleComponent
} from '@ladbrokesMobile/betslip/components/accaInsuranceSubtitle/acca-insurance-subtitle.component';
import {
  BetslipOverlayNotificationComponent
} from '@ladbrokesMobile/betslip/components/betslipOverlayNotification/betslip-overlay-notification.component';
import { ReceiptHeaderModule } from '@ladbrokesMobile/lazy-modules/receiptHeader/receipt-header.module';
import { DeclinedBetComponent } from '@ladbrokesMobile/betslip/components/declined-bet/declined-bet.component';
import { ToteBetReceiptComponent } from '@ladbrokesMobile/betslip/components/toteBetReceipt/tote-bet-receipt.component';
import {
  BetslipDepositErrorContainerComponent
} from '@ladbrokesMobile/betslip/components/betslipDepositErrorContainer/betslip-deposit-error-container.component';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { LottoBetslipModule } from '@ladbrokesMobile/lazy-modules/lottoBetSlip/lotto-betslip.module';

@NgModule({
  declarations: [
    BetslipDigitKeyboardDirective,
    BetslipLimitationDialogComponent,
    BetslipOverlayNotificationComponent,
    BsNotificationComponent,
    MaxStakeDialogComponent,
    OverAskNotificationDialogComponent,
    OveraskOfferNotificationComponent,
    ToteBetReceiptComponent,
    VoucherComponent,
    BetslipContainerComponent,
    SlideOutBetslipComponent,
    LadbrokesBetslipComponent,
    LadbrokesBetslipReceiptComponent,
    AddToBetslipComponent,
    IncorrectPatternComponent,
    LadbrokesBetslipTotalWrapperComponent,
    LadbrokesBetslipSubheaderComponent,
    LadbrokesEmptyBetslipComponent,
    LadbrokesBetslipSinglesReceiptComponent,
    LadbrokesBetslipMultiplesReceiptComponent,
    LadbrokesSelectionInfoDialogComponent,
    BetslipReceiptSubheaderComponent,
    BetslipFctcListComponent,
    LadbrokesToteBetReceiptItemComponent,
    OveraskHoldingDrawerComponent,
    BetslipOfferedDataComponent,
    AccaInsuranceSubtitleComponent,
    BetslipMultipleBetPartsComponent,
    DeclinedBetComponent,
    BetslipDepositErrorContainerComponent
  ],
  exports: [],
  imports: [
    SharedModule,
    FormsModule,
    BetslipRoutingModule,
    ReceiptHeaderModule,
    LottoBetslipModule
  ],
  providers: [],
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
