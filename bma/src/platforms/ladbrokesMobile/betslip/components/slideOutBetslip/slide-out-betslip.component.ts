import { Component, ViewEncapsulation } from '@angular/core';

import { SlideOutBetslipComponent as AppSlideOutBetslipComponent } from '@betslip/components/slideOutBetslip/slide-out-betslip.component';

@Component({
  selector: 'slide-out-betslip',
  templateUrl: 'slide-out-betslip.component.html',
  styleUrls: ['../../../../../app/betslip/components/slideOutBetslip/slide-out-betslip.component.scss', 'slide-out-betslip.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})

export class SlideOutBetslipComponent extends AppSlideOutBetslipComponent {}
