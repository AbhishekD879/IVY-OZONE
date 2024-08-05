import { ChangeDetectionStrategy, Component } from '@angular/core';

import { EmptyBetslipComponent } from '@app/betslip/components/emptyBetslip/empty-betslip.component';

@Component({
  selector: 'empty-betslip',
  templateUrl: './empty-betslip.component.html',
  styleUrls: ['./empty-betslip.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LadbrokesEmptyBetslipComponent extends EmptyBetslipComponent {

}
