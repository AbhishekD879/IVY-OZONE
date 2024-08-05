import { ChangeDetectionStrategy, Component } from '@angular/core';
import { ToteBetReceiptItemComponent } from '@betslip/components/toteBetReceiptItem/tote-bet-receipt-item.component';

@Component({
  selector: 'tote-bet-receipt-item',
  templateUrl: 'tote-bet-receipt-item.component.html',
  styleUrls: ['../../../../../app/betslip/assets/styles/modules/receipt.scss', '../../assets/styles/modules/receipt.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LadbrokesToteBetReceiptItemComponent extends ToteBetReceiptItemComponent {}
