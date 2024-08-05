import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Injectable({providedIn: 'root'})
export class UpgradeAccountService {

  private isUpgradeFromBetslip: boolean = false;

  constructor(
    private pubSubService: PubSubService,
    private router: Router
  ) { }

  subscribe(): void {
    this.pubSubService.subscribe('upgradeFromBetslip', this.pubSubService.API.UPGRADE_FROM_BETSLIP, () => {
      this.isUpgradeFromBetslip = true;
    });
  }

  afterReloginRedirection(): void {
    if (this.isUpgradeFromBetslip) {
      setTimeout(() => {
        this.router.navigate(['/']);
      });

      setTimeout(() => {
        this.pubSubService.publish(this.pubSubService.API['show-slide-out-betslip'], true);
      }, 1000);

      this.isUpgradeFromBetslip = false;
    } else {
      this.router.navigate(['/deposit', 'addcard']);
    }
  }
}
