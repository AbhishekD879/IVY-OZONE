import { Injectable } from '@angular/core';

// eslint-disable-next-line max-len
import { UpgradeAccountDialogService as BaseUpgradeAccountDialogService } from '@ladbrokesMobile/retail/services/upgradeAccountDialog/upgrade-account-dialog.service';

@Injectable()
export class UpgradeAccountDialogService extends BaseUpgradeAccountDialogService {
  protected modulePath = '@retail-lazy-load/retail.module#RetailModule';
}
