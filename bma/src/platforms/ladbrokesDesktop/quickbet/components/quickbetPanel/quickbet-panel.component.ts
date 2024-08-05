import { Component, ViewEncapsulation } from '@angular/core';
import { QuickbetPanelComponent } from '@app/quickbet/components/quickbetPanel/quickbet-panel.component';

@Component({
  selector: 'quickbet-panel',
  templateUrl: './quickbet-panel.component.html',
  styleUrls: ['quickbet-panel.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class LadbrokesDeskQuickbetPanelComponent extends QuickbetPanelComponent {
  /**
   * Open Quick Deposit form for luckydip desktop 
   * @returns {void} 
   * */
  openQuickDeposit(): void {
    this.quickDepositFormExpanded = true;
    if (this.isLuckyDip) {
      this.quickDepositIframeService.isEnabled().subscribe(() => {
        this.quickDepositIframeService.redirectToDepositPage();
      }, () => {
        this.quickDepositIframeService.redirectToDepositPage();
      });
    }
  }
}
