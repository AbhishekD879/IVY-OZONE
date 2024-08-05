import { ChangeDetectionStrategy, Component } from '@angular/core';
import { CashoutLabelComponent } from '@app/shared/components/cashoutLabel/cashout-label.component';

@Component({
  selector: 'cashout-label',
  templateUrl: 'cashout-label.component.html',
  styleUrls: ['cashout-label.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LadbrokesCashoutLabelComponent extends CashoutLabelComponent {}
