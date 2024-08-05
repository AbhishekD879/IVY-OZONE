import { ChangeDetectionStrategy, Component } from '@angular/core';
import {
  BetslipReceiptSubheaderComponent as BaseBetslipReceiptSubheaderComponent
} from '@app/betslip/components/betslipReceiptSubheader/betslip-receipt-subheader.component';

@Component({
  selector: 'betslip-receipt-subheader',
  templateUrl: './betslip-receipt-subheader.component.html',
  styleUrls: [
    '../../../../../app/betslip/components/betslipReceiptSubheader/betslip-receipt-subheader.component.scss',
    'betslip-receipt-subheader.component.scss'
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class BetslipReceiptSubheaderComponent extends BaseBetslipReceiptSubheaderComponent {}
