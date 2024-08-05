import { Component } from '@angular/core';
import { BetslipTabsService } from '@core/services/betslipTabs/betslip-tabs.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@core/services/gtm/gtm.service';

@Component({
    selector: 'betslip-header-icon',
    templateUrl: 'betslip-header-icon.component.html',
    styleUrls: ['betslip-header-icon.component.scss']
})

export class BetslipHeaderIconComponent {
    constructor(
        private betslipTabsService: BetslipTabsService,
        private pubSubService: PubSubService,
        private GTM: GtmService
    ) {}

    /**
     * Handles click on "Betslip" button.
     */
    openBetslip(): void {
        this.GTM.push('trackPageview', { virtualUrl: '/betslip-receipt' });

        this.betslipTabsService.redirectToBetSlipTab('Bet Slip', true);

        this.pubSubService.publish(this.pubSubService.API['show-slide-out-betslip'], true);
    }
}
