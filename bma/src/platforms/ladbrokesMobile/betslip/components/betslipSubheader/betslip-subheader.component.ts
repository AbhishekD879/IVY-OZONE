import { ChangeDetectionStrategy, Component } from '@angular/core';

import { BetslipSubheaderComponent } from '@betslip/components/betslipSubheader/betslip-subheader.component';

@Component({
  selector: 'betslip-subheader',
  templateUrl: './betslip-subheader.component.html',
  styleUrls: ['./betslip-subheader.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LadbrokesBetslipSubheaderComponent extends BetslipSubheaderComponent {

}
