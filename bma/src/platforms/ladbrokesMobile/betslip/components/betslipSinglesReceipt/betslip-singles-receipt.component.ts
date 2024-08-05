import { ChangeDetectionStrategy, Component } from '@angular/core';
import { BetslipSinglesReceiptComponent } from '@app/betslip/components/betslipSinglesReceipt/betslip-singles-receipt.component';

@Component({
  selector: 'betslip-singles-receipt',
  templateUrl: './betslip-singles-receipt.component.html',
  styleUrls: [
    '../../../../../app/betslip/assets/styles/modules/receipt.scss',
    '../../assets/styles/modules/receipt.scss', './betslip-singles-receipt.component.scss'
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LadbrokesBetslipSinglesReceiptComponent extends BetslipSinglesReceiptComponent {}
