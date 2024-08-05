import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { DeviceService } from '@core/services/device/device.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
    selector: 'my-bets-button',
    templateUrl: 'my-bets-button.component.html',
    styleUrls: ['my-bets-button.component.scss']
})
export class MyBetsButtonComponent {
    constructor(
        private device: DeviceService,
        private pubsub: PubSubService,
        private router: Router
    ) {}

  /**
   * Depending on device view type - opens "My bets" page or emits event to select tab in widget.
   */
  openMyBets(): void {
    const betHistoryTab = 'open-bets';
    const betHistoryTabEvent = 'LOAD_UNSETTLED_BETS';

    if (!this.device.isMobile) {
      this.pubsub.publish(betHistoryTabEvent);
    } else {
      this.router.navigate([betHistoryTab]);
    }
  }
}
