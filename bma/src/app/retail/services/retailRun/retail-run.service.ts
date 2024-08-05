import { Injectable } from '@angular/core';
import { UpgradeAccountService } from '@app/retail/services/upgradeAccount/upgrade-account.service';
import { RetailMenuService } from '@retailModule/services/retailMenu/retail-menu.service';
import { RetailService } from '@app/retail/services/retail/retail.service';

@Injectable()
export class RetailRunService {
  constructor(
    private upgradeAccountService: UpgradeAccountService,
    private retailMenuService: RetailMenuService,
    private retailService: RetailService
  ) { }

  run() {
    this.upgradeAccountService.subscribe();
    this.retailMenuService.subscribe();
    this.retailService.subscribe();
  }
}
