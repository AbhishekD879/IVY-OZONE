import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
// eslint-disable-next-line max-len
import { UpgradeAccountDialogService as OxygenUpgradeAccountDialogService } from '@app/retail/services/upgradeAccountDialog/upgrade-account-dialog.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { StorageService } from '@app/core/services/storage/storage.service';
import { UserService } from '@app/core/services/user/user.service';
import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { Router } from '@angular/router';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { CmsService } from '@coreModule/services/cms/cms.service';

@Injectable()
export class UpgradeAccountDialogService extends OxygenUpgradeAccountDialogService {

  protected modulePath = '@retail-lazy-load/retail.module#RetailModule';

  constructor(
    protected dialogService: DialogService,
    protected gtmService: GtmService,
    protected storageService: StorageService,
    protected userService: UserService,
    protected router: Router,
    protected routingState: RoutingState,
    protected dynamicComponentLoader: DynamicLoaderService,
    protected deviceService: DeviceService,
    protected cmsServcie: CmsService
  ) {
    super(dialogService, gtmService, storageService, userService, router, routingState, dynamicComponentLoader, deviceService, cmsServcie);
  }

  protected isAvailableForUser(): Observable<boolean> {
    return this.cmsService.getSystemConfig().pipe(map(config => {
      return !this.userService.isMultiChannelUser() && this.userService.status && config && config.Connect && config.Connect.upgrade;
    }));
  }
}
