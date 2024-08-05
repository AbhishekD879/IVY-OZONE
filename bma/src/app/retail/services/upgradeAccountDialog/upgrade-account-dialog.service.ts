import { Observable, Observer } from 'rxjs';

import { map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { DialogService } from '@core/services/dialogService/dialog.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { ITrackEvent } from '@core/services/gtm/models';
import { StorageService } from '@core/services/storage/storage.service';
import { UserService } from '@core/services/user/user.service';
import { IVerticalMenu, IMenuActionResult } from '@app/core/services/cms/models';
import { IUpgradeDialogResult } from '@app/retail/services/upgradeAccountDialog/upgrade-account-dialog.model';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { UPGRADE_ACCOUNT_MENU_ITEMS } from '@app/retail/constants/retail.constant';
import { CmsService } from '@coreModule/services/cms/cms.service';

@Injectable({
  providedIn: 'root'
})
export class UpgradeAccountDialogService {
  private trackEventData: ITrackEvent = {
    event: 'trackEvent',
    eventCategory: 'cta',
    eventAction: 'upgrade account',
    eventLabel: null
  };

  constructor(
    protected dialogService: DialogService,
    protected gtmService: GtmService,
    protected storageService: StorageService,
    protected userService: UserService,
    protected router: Router,
    protected routingState: RoutingState,
    protected dynamicComponentLoader: DynamicLoaderService,
    protected deviceService: DeviceService,
    protected cmsService: CmsService
  ) { }

  /**
   * Open connect upgrade dialog for in-shop user
   *
   * @param {boolean} [handleNative=true] handle popup closing in native app
   * @returns {Observable<IUpgradeDialogResult>}
   * @memberof UpgradeAccountService
   */
  showUpgradeDialog(handleNative: boolean = true): Observable<IUpgradeDialogResult> {
    return Observable.create((observer: Observer<IUpgradeDialogResult>) => {
      this.isAvailableForUser().subscribe(() => {
          observer.next({});
          observer.complete();
      });
    });
  }

  /**
   * Assign open upgrade popup action to specific menu items.
   *
   * @param {IVerticalMenu} menuItem
   * @returns {IVerticalMenu}
   * @memberof UpgradeAccountService
   */
  decorateMenuAction(menuItem: IVerticalMenu): IVerticalMenu {
    if (UPGRADE_ACCOUNT_MENU_ITEMS.includes(menuItem.targetUri)
      && (this.deviceService.isMobile && this.userService.isInShopUser())) {
      menuItem.action = (): Observable<IMenuActionResult> => this.showUpgradeDialog(false);
      return menuItem;
    }
  }

  protected isAvailableForUser(): Observable<boolean> {
    return this.cmsService.getSystemConfig().pipe(map(config => {
      return this.userService.isInShopUser() && config && config.Connect && config.Connect.upgrade;
    }));
  }

  protected dialogUpgradeAction(observer) {
    this.trackEventData.eventLabel = 'yes - upgrade Account';
    this.gtmService.push(this.trackEventData.event, this.trackEventData);
    observer.next({ redirectUri: 'retail-registration' });
    observer.complete();
  }

  protected dialogCancelAction(observer, value: boolean) {
    this.trackEventData.eventLabel = 'no thanks';
    this.gtmService.push(this.trackEventData.event, this.trackEventData);
    observer.next({ cancelled: value });
    observer.complete();
  }
}
