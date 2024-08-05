import { ChangeDetectionStrategy, Component } from '@angular/core';
import { BetslipMultiplesReceiptComponent } from '@app/betslip/components/betslipMultiplesReceipt/betslip-multiples-receipt.component';

@Component({
  selector: 'betslip-multiples-receipt',
  templateUrl: './betslip-multiples-receipt.component.html',
  styleUrls: ['../../../../../app/betslip/assets/styles/modules/receipt.scss',
    '../../../../../app/betslip/components/betslipMultiplesReceipt/betslip-multiples-receipt.component.scss',
    '../../assets/styles/modules/receipt.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class LadbrokesBetslipMultiplesReceiptComponent extends BetslipMultiplesReceiptComponent {}
