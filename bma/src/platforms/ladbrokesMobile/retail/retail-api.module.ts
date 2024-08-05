import { NgModule } from '@angular/core';
/* eslint-disable max-len */
import { UpgradeAccountDialogService as OxygenUpgradeAccountDialogService } from '@app/retail/services/upgradeAccountDialog/upgrade-account-dialog.service';
import { UpgradeAccountDialogService as LadbrokesUpgradeAccountDialogService  } from '@retailModule/services/upgradeAccountDialog/upgrade-account-dialog.service';
/* eslint-enable max-len */
import { RetailRunService } from '@app/retail/services/retailRun/retail-run.service';
import { BetFilterParamsService } from '@app/retail/services/betFilterParams/bet-filter-params.service';
import { RetailService } from '@app/retail/services/retail/retail.service';
import { RetailMenuService } from '@app/retail/services/retailMenu/retail-menu.service';
import { UpgradeAccountService } from '@app/retail/services/upgradeAccount/upgrade-account.service';
import { UpgradeAccountProviderService } from '@app/retail/services/upgradeAccountProvider/upgrade-account-provider.service';

@NgModule({
  declarations: [],
  providers: [
    RetailRunService,
    BetFilterParamsService,
    RetailService,
    RetailMenuService,
    UpgradeAccountService,
    OxygenUpgradeAccountDialogService,
    LadbrokesUpgradeAccountDialogService,
    UpgradeAccountProviderService
  ]
})
export class RetailApiModule {}
