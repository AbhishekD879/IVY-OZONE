import { Component, HostListener } from '@angular/core';
import { BetslipHeaderIconComponent as AppBetslipHeaderIconComponent
} from '@shared/components/betslipHeaderIcon/betslip-header-icon.component';

@Component({
    selector: 'betslip-header-icon',
    template: '<betslip-counter data-uat="betSlipBtn"></betslip-counter>',
    styleUrls: ['betslip-header-icon.component.scss']
})

export class BetslipHeaderIconComponent extends AppBetslipHeaderIconComponent {
  @HostListener('click') openBetSlip() {
    this.openBetslip();
  }
}
