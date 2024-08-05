import { ChangeDetectionStrategy, Component } from '@angular/core';

import { BetslipTotalWrapperComponent } from '@app/betslip/components/betslipTotalWrapper/betslip-total-wrapper.component';

@Component({
  selector: 'betslip-total-wrapper',
  templateUrl: './betslip-total-wrapper.component.html',
  styleUrls: ['./betslip-total-wrapper.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LadbrokesBetslipTotalWrapperComponent extends BetslipTotalWrapperComponent {

}
